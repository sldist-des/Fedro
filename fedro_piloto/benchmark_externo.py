"""Executor de benchmarks EXTERNOS (benchmark/protocolo-avaliacao.md).

Um pacote externo é uma pasta no formato do contrato público (benchmark/contrato-publico.md):
tarefas.json, referencias.py, opcionalmente testes_ocultos.json e testemunhas.json (selados), e
MANIFESTO.json com os hashes (congelamento). Este módulo:

  1. valida o pacote com o MESMO validador autónomo do kit do autor e confere o hash congelado;
  2. regista as tarefas no ambiente sob ids internos com prefixo "bx:" (nunca colidem com tarefas
     internas): predicados entram no REGISTRO como conceitos externos (duas referências quando o
     autor dá REFERENCIAS_B; gerador de positivos do autor quando dá POSITIVOS); funções entram em
     REFERENCIAS_FUNCAO com adaptação da saída ao tipo declarado;
  3. executa os braços do protocolo (L-fix, L-lib, L-lib+f, L-lib+f/lesao × políticas tamanho e
     unigrama) em dois modos: "zero" (biblioteca vazia; todo o custo é do benchmark) e "previo"
     (aquisição anterior das operações do documento 05 incluída no custo cumulativo); ordens: do
     autor, aleatória (sementes do seletor), autodirigida (curriculo_autodirigido);
  4. calcula as métricas pré-registadas (protocolo, §5) e escreve registros reproduzíveis.

Os aprendizes só acedem às tarefas pelo Ambiente (exemplos iniciais e contraexemplos do oráculo);
nunca veem referencias.py, os testes ocultos nem as testemunhas. Os ficheiros selados são lidos
apenas por `verificar_benchmark`, depois da execução.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import random
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from . import aprendizes as A
from . import geradores as G
from .dsl import BOOL, FUN, GRADE, LP, POS, tipo_str
from .experimento_minimo import CURRICULO, ConfigEM, _aprendiz, TAREFAS as TAREFAS_INTERNAS
from .grade import Grade
from .razao import LivroRazao
from .referencias import REGISTRO, Conceito

PREFIXO = "bx:"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(RAIZ, "benchmark", "kit-autor")
CADEIA_PREVIA = tuple(CURRICULO[:3])
BRACOS = ("L-fix", "L-lib", "L-lib+f", "L-lib+f/lesao")
MODOS = ("zero", "previo")
_TIPOS = {"Grade": GRADE, "Pos": POS, "Bool": BOOL, "L Pos": LP}

#: id interno → Tarefa, consultado por verificacao.tarefa_por_id
TAREFAS_EXTERNAS: Dict[str, A.Tarefa] = {}


class ErroIntegridade(Exception):
    pass


def _kit():
    """O validador autónomo do kit (mesmo código que o autor corre)."""
    if KIT not in sys.path:
        sys.path.insert(0, KIT)
    spec = importlib.util.spec_from_file_location("validar_pacote_kit", os.path.join(KIT, "validar_pacote.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _para_grade(g) -> Grade:
    """Converte uma Grade do kit (classe homónima) na Grade do pacote fedro_piloto."""
    if isinstance(g, Grade):
        return g
    return Grade(int(g.n), tuple(int(b) for b in g.bits))


def _adaptar_saida(f: Callable, resultado: str, comparacao: str) -> Callable:
    if resultado == "Bool":
        return lambda *a: bool(f(*a))
    if resultado == "Pos":
        return lambda *a: tuple(f(*a))
    if comparacao == "conjunto":
        return lambda *a: frozenset(tuple(p) for p in f(*a))
    return lambda *a: tuple(tuple(p) for p in f(*a))


@dataclass
class Pacote:
    caminho: str
    nome: str
    versao: str
    hash: str
    manifesto: dict
    tarefas: List[A.Tarefa]                 # na ordem do autor, ids internos
    autor_para_interno: Dict[str, str]
    interno_para_autor: Dict[str, str]
    descricoes: Dict[str, str]
    grupos: Dict[str, Optional[str]]
    validacao: dict = field(default_factory=dict)

    @property
    def ordem(self) -> List[str]:
        return [t.id for t in self.tarefas]

    def resumo(self) -> dict:
        return {"caminho": os.path.relpath(self.caminho, RAIZ), "nome": self.nome, "versao": self.versao,
                "hash": self.hash, "num_tarefas": len(self.tarefas),
                "tarefas": [{"id": self.interno_para_autor[t.id], "interno": t.id, "tipo": tipo_str(t.tipo),
                             "natureza": t.natureza, "comparacao": t.comparacao, "grupo": self.grupos.get(t.id)}
                            for t in self.tarefas]}


def validar_pacote(caminho: str) -> dict:
    kit = _kit()
    rel = kit.validar(caminho)
    return {"erros": rel.erros, "avisos": rel.avisos, "estatisticas": rel.estatisticas, "ok": rel.ok()}


def conferir_congelamento(caminho: str, hash_esperado: Optional[str] = None) -> dict:
    kit = _kit()
    cam = os.path.join(caminho, "MANIFESTO.json")
    if not os.path.exists(cam):
        raise ErroIntegridade("pacote sem MANIFESTO.json: não está congelado")
    with open(cam, encoding="utf-8") as f:
        man = json.load(f)
    hs = kit.hashes_do_pacote(caminho)
    h = kit.hash_pacote(hs)
    if h != man.get("hash_pacote"):
        raise ErroIntegridade(f"hash do pacote {h} ≠ hash do manifesto {man.get('hash_pacote')}: pacote alterado após o congelamento")
    if hs != man.get("arquivos"):
        raise ErroIntegridade("lista de ficheiros/hashes difere do manifesto")
    if hash_esperado is not None and h != hash_esperado:
        raise ErroIntegridade(f"hash do pacote {h} ≠ hash registado na execução {hash_esperado}")
    return man


def carregar_pacote(caminho: str, exigir_congelado: bool = True, hash_esperado: Optional[str] = None) -> Pacote:
    """Valida, confere o congelamento e regista as tarefas no ambiente (idempotente)."""
    caminho = os.path.abspath(caminho)
    val = validar_pacote(caminho)
    if not val["ok"]:
        raise ErroIntegridade("pacote inválido:\n" + "\n".join(val["erros"]))
    man = conferir_congelamento(caminho, hash_esperado) if exigir_congelado else {}
    kit = _kit()
    with open(os.path.join(caminho, "tarefas.json"), encoding="utf-8") as f:
        doc = json.load(f)
    mod = kit.carregar_modulo(os.path.join(caminho, "referencias.py"), f"referencias_{abs(hash(caminho))}")
    refs, refs_b, positivos = mod.REFERENCIAS, getattr(mod, "REFERENCIAS_B", {}) or {}, getattr(mod, "POSITIVOS", {}) or {}
    nome = doc.get("nome", os.path.basename(caminho))
    tarefas, a2i, i2a, desc, grupos = [], {}, {}, {}, {}
    for t in doc["tarefas"]:
        tid = t["id"]
        interno = PREFIXO + tid
        args, res = kit.TIPOS_ACEITOS[t["tipo"]]
        tipo = FUN(*[_TIPOS[a] for a in args], _TIPOS[res])
        comp = t.get("comparacao", "exata")
        f = refs[tid]
        if t["natureza"] == "predicado":
            fb = refs_b.get(tid, f)
            esquema = "externo"
            if tid in positivos:
                esquema = f"externo:{interno}"
                gen = positivos[tid]
                G._POR_ESQUEMA[esquema] = (lambda c, n, rng, _g=gen: (lambda x: None if x is None else _para_grade(x))(_g(n, rng)))
            REGISTRO[interno] = Conceito(interno, "externo", (lambda g, _f=f: bool(_f(g))), (lambda g, _f=fb: bool(_f(g))),
                                         esquema, [], {"pacote": nome})
            tarefa = A.Tarefa(interno, tipo, "predicado", f"externo:{nome}", interno)
        else:
            A.REFERENCIAS_FUNCAO[interno] = _adaptar_saida(f, res, comp)
            tarefa = A.Tarefa(interno, tipo, "funcao", f"externo:{nome}", comparacao=comp)
        tarefas.append(tarefa)
        a2i[tid], i2a[interno] = interno, tid
        desc[interno] = t.get("descricao", "")
        grupos[interno] = t.get("grupo")
        TAREFAS_EXTERNAS[interno] = tarefa
    return Pacote(caminho, nome, str(doc.get("versao", man.get("versao", "1"))), man.get("hash_pacote", val["estatisticas"]["hash_pacote"]),
                  man, tarefas, a2i, i2a, desc, grupos, val)


def carregar_selados(pacote: Pacote) -> dict:
    """Testes ocultos e testemunhas do autor: SÓ depois da execução (verificação)."""
    out = {"testes_ocultos": {}, "testemunhas": {}}
    cam = os.path.join(pacote.caminho, "testes_ocultos.json")
    if os.path.exists(cam):
        with open(cam, encoding="utf-8") as f:
            out["testes_ocultos"] = {pacote.autor_para_interno[k]: [Grade.de_texto(s) for s in v] for k, v in json.load(f).items()}
    cam = os.path.join(pacote.caminho, "testemunhas.json")
    if os.path.exists(cam):
        with open(cam, encoding="utf-8") as f:
            out["testemunhas"] = {pacote.autor_para_interno[k]: v for k, v in json.load(f).items()}
    return out


# ---------------------------------------------------------------- execução de um braço
def _resultado_dict(r: A.ResultadoTarefa, livro: LivroRazao, aid: str, autor_id: str) -> dict:
    e = livro.entrada(r.tarefa_id, aid)
    return {"tarefa": autor_id, "interno": r.tarefa_id, "aceita": r.aceita, "motivo": r.motivo_fim, "rodadas": r.rodadas,
            "hipotese": r.hipotese_legivel, "hipotese_bruta": r.hipotese, "tamanho": r.tamanho,
            "custo": e.total_aprendiz(), "enumeracao_candidatos": e.enumeracao_candidatos,
            "busca_candidatos": e.busca_candidatos, "biblioteca_usada": list(r.constantes_biblioteca_usadas),
            "reutilizacoes": dict(r.reutilizacoes), "abstracoes_novas": [a.get("nome") for a in r.abstracoes_novas],
            "acuracia_teste": r.acuracia_teste, "teste_resumo": r.teste_resumo,
            "tamanho_max_carregado": r.contador_busca.get("tamanho_max_carregado", 0),
            "inconclusivo_recurso": r.inconclusivo_recurso, "exemplos_finais": r.exemplos_finais}


def job_braco(aprendiz_nome: str, cfg: ConfigEM, caminho_pacote: str, hash_pacote: str, modo: str,
              ordem: Sequence[str], lesao_apos: Optional[int], k_reservatorio: int = 40,
              rotulo: Optional[str] = None) -> dict:
    """Um braço: (modo previo: cadeia do documento 05) → tarefas externas na ordem dada.
    lesao_apos: índice (0-based) da tarefa externa ANTES da qual a lesão é aplicada (só L-lib+f/lesao)."""
    try:
        return _job_braco(aprendiz_nome, cfg, caminho_pacote, hash_pacote, modo, list(ordem), lesao_apos, k_reservatorio, rotulo)
    except Exception as e:  # noqa: BLE001
        import traceback
        return {"deterministico": {"braco": rotulo or aprendiz_nome, "aprendiz": aprendiz_nome, "modo": modo,
                                   "politica": cfg.politica_busca, "falha": f"{type(e).__name__}: {e}",
                                   "traceback": traceback.format_exc(), "resultados": {}, "previo": [], "curva": [],
                                   "abstracoes": [], "eventos": []},
                "medicoes": {"tempo_parede_s": 0.0, "cpu_s": 0.0, "memoria_pico_kib": None, "memoria_escopo": None}}


def _job_braco(aprendiz_nome, cfg, caminho_pacote, hash_pacote, modo, ordem, lesao_apos, k_reservatorio, rotulo):
    from .medidas import medir_isolado
    from .piloto import limitar_memoria
    limitar_memoria(cfg.memoria_trabalhador_gb)
    pacote = carregar_pacote(caminho_pacote, hash_esperado=hash_pacote)
    rotulo = rotulo or f"{modo}/{cfg.politica_busca}/{aprendiz_nome}"
    amb = A.Ambiente(cfg.semente, num_teste=cfg.num_teste, k_reservatorio=k_reservatorio)
    livro = LivroRazao(cfg.semente, {"braco": rotulo, "experimento": "benchmark-externo", "pacote": pacote.hash})
    ap = _aprendiz(aprendiz_nome, cfg, livro, rotulo=f"{cfg.base}/{rotulo}")
    aid = ap.aprendiz_id
    previo, resultados, curva, eventos = [], {}, [], []
    cum = 0
    t0 = time.process_time()
    with medir_isolado(rotulo) as m:
        if modo == "previo":
            for tid in CADEIA_PREVIA:
                r = ap.resolver(TAREFAS_INTERNAS[tid], amb)
                d = _resultado_dict(r, livro, aid, tid)
                cum += d["custo"]
                d["cumulativo"] = cum
                previo.append(d)
            if aprendiz_nome == "L-lib+f/lesao":
                eventos.append({"antes_de": ordem[0] if ordem else None, "lesao": ap.lesionar(), "fase": "apos-previo"})
        for i, tid in enumerate(ordem):
            if aprendiz_nome == "L-lib+f/lesao" and modo == "zero" and lesao_apos is not None and i == lesao_apos:
                eventos.append({"antes_de": tid, "lesao": ap.lesionar(), "fase": f"apos-{i}-tarefas"})
            try:
                r = ap.resolver(TAREFAS_EXTERNAS[tid], amb)
                d = _resultado_dict(r, livro, aid, pacote.interno_para_autor[tid])
            except G.ConceitoDegenerado as ex:
                # tarefa inválida NO AMBIENTE (sem exemplos/pares suficientes na partição): registada como tal,
                # nunca contada como resolvida nem como falha do aprendiz; é um erro de integridade a devolver ao autor
                d = {"tarefa": pacote.interno_para_autor[tid], "interno": tid, "aceita": False, "motivo": "tarefa-degenerada-no-ambiente",
                     "detalhe": str(ex), "rodadas": 0, "hipotese": None, "hipotese_bruta": None, "tamanho": None,
                     "custo": livro.entrada(tid, aid).total_aprendiz(), "enumeracao_candidatos": 0, "busca_candidatos": 0,
                     "biblioteca_usada": [], "reutilizacoes": {}, "abstracoes_novas": [], "acuracia_teste": None,
                     "teste_resumo": {}, "tamanho_max_carregado": 0, "inconclusivo_recurso": False, "exemplos_finais": 0,
                     "invalida_no_ambiente": True}
            cum += d["custo"]
            d["cumulativo"] = cum
            d["indice"] = i
            resultados[tid] = d
            curva.append({"tarefa": pacote.interno_para_autor[tid], "interno": tid, "aceita": d["aceita"], "custo": d["custo"],
                          "cumulativo": cum, "biblioteca_usada": d["biblioteca_usada"]})
    det = {"braco": rotulo, "aprendiz": aprendiz_nome, "modo": modo, "politica": cfg.politica_busca, "semente": cfg.semente,
           "k_reservatorio": k_reservatorio, "ordem": [pacote.interno_para_autor[t] for t in ordem], "lesao_apos": lesao_apos,
           "previo": previo, "custo_previo": sum(d["custo"] for d in previo),
           "resultados": resultados, "curva": curva, "custo_cumulativo": cum,
           "abstracoes": A.abstracoes(ap), "eventos": eventos, "relatorio": ap.relatorio(),
           "livro": livro.deterministico_dict(incluir_diario=False)}
    med = {"tempo_parede_s": m.tempo_parede_s, "cpu_s": time.process_time() - t0,
           "memoria_pico_kib": m.memoria_pico_kib, "memoria_escopo": m.memoria_escopo}
    return {"deterministico": det, "medicoes": med}


# ---------------------------------------------------------------- métricas pré-registadas (protocolo §5)
def _fechamento(det: dict):
    """Custo total verificável: a soma das entradas do livro-razão (inclui a fase prévia) fecha com o cumulativo."""
    livro = det.get("livro")
    if not isinstance(livro, dict) or "entradas" not in livro:
        return None
    soma = sum(e.get("total_aprendiz", 0) for e in livro["entradas"])
    return soma == det["custo_cumulativo"]


def transferencia_por_tarefa(lib: dict, fix: dict) -> Dict[str, dict]:
    """Compara L-lib+f com L-fix (mesma política e modo) tarefa a tarefa, SEM razões exatas quando
    um dos dois não aceita dentro do orçamento (só limites inferiores declarados como tal)."""
    out = {}
    for tid, a in lib["resultados"].items():
        b = fix["resultados"].get(tid)
        if b is None:
            continue
        ca, cb = a["custo"], b["custo"]
        item = {"L-lib+f": {"aceita": a["aceita"], "custo": ca, "tamanho": a["tamanho"], "reuso": a["biblioteca_usada"]},
                "L-fix": {"aceita": b["aceita"], "custo": cb, "tamanho": b["tamanho"]}, "razao_exata": None, "razao_minima": None}
        if a["aceita"] and b["aceita"]:
            item["razao_exata"] = (cb / ca) if ca else None       # aceleração = custo L-fix / custo L-lib+f
            item["classe"] = "positiva" if ca < cb else ("neutra" if ca == cb else "negativa")
        elif a["aceita"] and not b["aceita"]:
            item["razao_minima"] = (cb / ca) if ca else None       # L-fix gastou cb sem aceitar: aceleração ≥ cb/ca
            item["classe"] = "positiva (só L-lib+f aceita; razão exata indefinida)"
        elif b["aceita"] and not a["aceita"]:
            item["razao_minima_inversa"] = (ca / cb) if cb else None
            item["classe"] = "negativa (só L-fix aceita; razão exata indefinida)"
        else:
            item["classe"] = "inconclusiva (nenhum aceita no orçamento)"
        item["reuso_verificavel"] = bool(a["biblioteca_usada"])
        out[tid] = item
    return out


def metricas(det: dict) -> dict:
    """Métricas pré-registadas por braço e comparações entre braços (protocolo §5)."""
    bracos = det["bracos"]
    por_braco = {}
    for k, b in bracos.items():
        if b.get("falha"):
            por_braco[k] = {"falha": b["falha"]}
            continue
        res = b["resultados"]
        aceitas = [t for t, r in res.items() if r["aceita"]]
        reuso = {t: r["biblioteca_usada"] for t, r in res.items() if r["aceita"] and r["biblioteca_usada"]}
        descobertas = [a for a in b["abstracoes"] if a.get("proveniencia") == "descoberta"]
        invalidas = [res[t]["tarefa"] for t, r in res.items() if r.get("invalida_no_ambiente")]
        por_braco[k] = {
            "tarefas": len(res), "tarefas_validas": len(res) - len(invalidas), "invalidas_no_ambiente": invalidas,
            "aceitas": len(aceitas), "ids_aceitas": [res[t]["tarefa"] for t in aceitas],
            "custo_benchmark": sum(r["custo"] for r in res.values()), "custo_previo": b.get("custo_previo", 0),
            "custo_cumulativo": b["custo_cumulativo"],
            "custo_por_aceita": (b["custo_cumulativo"] / len(aceitas)) if aceitas else None,
            "aceitas_por_1e8_passos": (len(aceitas) * 1e8 / b["custo_cumulativo"]) if b["custo_cumulativo"] else None,
            "reuso_verificavel": {res[t]["tarefa"]: v for t, v in reuso.items()}, "tarefas_com_reuso": len(reuso),
            "entradas_descobertas": len(descobertas),
            "entradas_reutilizadas": sum(1 for a in descobertas if a.get("reutilizacoes")),
            "livro_fecha": _fechamento(b), "falhas_recurso": sum(1 for r in res.values() if r.get("inconclusivo_recurso")),
            "degenerados_teste": sum(1 for r in res.values() if r["aceita"] and r.get("teste_resumo", {}).get("degenerado")),
        }
    comparacoes = {}
    for k, b in bracos.items():
        if b.get("falha") or b["aprendiz"] != "L-lib+f":
            continue
        kf = k.replace("L-lib+f", "L-fix")
        f = bracos.get(kf)
        if not f or f.get("falha"):
            continue
        tt = transferencia_por_tarefa(b, f)
        comparacoes[f"{k} vs {kf}"] = {
            "por_tarefa": {b["resultados"][t]["tarefa"]: v for t, v in tt.items()},
            "positivas": sum(v["classe"].startswith("positiva") for v in tt.values()),
            "negativas": sum(v["classe"].startswith("negativa") for v in tt.values()),
            "neutras": sum(v["classe"] == "neutra" for v in tt.values()),
            "inconclusivas": sum(v["classe"].startswith("inconclusiva") for v in tt.values()),
            "com_reuso": sum(v["reuso_verificavel"] for v in tt.values()),
            "aceitas_a_custo_cumulativo_igual": _custo_cumulativo_igual(b, f)}
        kl = k.replace("L-lib+f", "L-lib+f/lesao")
        le = bracos.get(kl)
        if le and not le.get("falha"):
            comparacoes[f"{k} vs {kl}"] = _sensibilidade_lesao(b, le)
    return {"por_braco": por_braco, "comparacoes": comparacoes}


def _custo_cumulativo_igual(lib: dict, fix: dict) -> List[dict]:
    out = []
    for p in lib["curva"]:
        if not p["aceita"]:
            continue
        C = p["cumulativo"]
        n_fix = sum(1 for q in fix["curva"] if q["aceita"] and q["cumulativo"] <= C)
        n_lib = sum(1 for q in lib["curva"] if q["aceita"] and q["cumulativo"] <= C)
        out.append({"tarefa": p["tarefa"], "custo_cumulativo": C, "aceitas_L-lib+f": n_lib, "aceitas_L-fix_ao_mesmo_custo": n_fix})
    return out


def _sensibilidade_lesao(lib: dict, les: dict) -> dict:
    depois = None
    for ev in les.get("eventos", []):
        if "lesao" in ev:
            depois = ev.get("antes_de")
    if depois is None:
        return {"nota": "sem evento de lesão"}
    ordem = [p["interno"] for p in les["curva"]]
    idx = ordem.index(depois) if depois in ordem else 0
    pos = ordem[idx:]
    a_l = sum(1 for t in pos if lib["resultados"].get(t, {}).get("aceita"))
    a_le = sum(1 for t in pos if les["resultados"].get(t, {}).get("aceita"))
    c_l = sum(lib["resultados"][t]["custo"] for t in pos if t in lib["resultados"])
    c_le = sum(les["resultados"][t]["custo"] for t in pos if t in les["resultados"])
    return {"tarefas_apos_lesao": len(pos), "aceitas_L-lib+f": a_l, "aceitas_lesao": a_le,
            "custo_L-lib+f": c_l, "custo_lesao": c_le, "entradas_removidas": len([x for ev in les["eventos"] for x in ev.get("lesao", [])]),
            "sensivel": (a_le < a_l) or (a_le == a_l and c_le > c_l)}


def agregar_sementes(execucoes: List[dict]) -> dict:
    """Robustez: min/mediana/max por braço (mesmo rótulo) sobre execuções com sementes distintas."""
    import statistics
    agg: Dict[str, dict] = {}
    for k in sorted({k for e in execucoes for k in e["metricas"]["por_braco"]}):
        xs = [e["metricas"]["por_braco"][k] for e in execucoes if k in e["metricas"]["por_braco"] and "falha" not in e["metricas"]["por_braco"][k]]
        if not xs:
            continue
        def st(campo):
            v = [x[campo] for x in xs if x.get(campo) is not None]
            return {"min": min(v), "mediana": statistics.median(v), "max": max(v), "n": len(v)} if v else None
        agg[k] = {"sementes": len(xs), "aceitas": st("aceitas"), "custo_cumulativo": st("custo_cumulativo"),
                  "tarefas_com_reuso": st("tarefas_com_reuso"),
                  "aceitas_em_todas": sorted(set.intersection(*[set(x["ids_aceitas"]) for x in xs])) if xs else []}
    return agg


# ---------------------------------------------------------------- execução completa
def executar(caminho_pacote: str, pasta: str, cfg: ConfigEM, bracos: Sequence[str] = BRACOS, politicas: Sequence[str] = ("tamanho", "unigrama"),
             modos: Sequence[str] = ("zero",), k_reservatorio: int = 40, processos: int = 4) -> dict:
    """Ordem do autor; um registro por (semente em cfg). Lesão no modo zero: antes da tarefa ⌊N/2⌋."""
    from .piloto import _executar_jobs, hash_fontes
    pacote = carregar_pacote(caminho_pacote)
    os.makedirs(pasta, exist_ok=True)
    N = len(pacote.ordem)
    lesao_apos = N // 2
    jobs, nomes = [], []
    for modo in modos:
        for pol in politicas:
            c = _replace(cfg, pol)
            for apn in bracos:
                rot = f"{modo}/{pol}/{apn}"
                jobs.append((job_braco, (apn, c, pacote.caminho, pacote.hash, modo, pacote.ordem, lesao_apos, k_reservatorio, rot)))
                nomes.append(rot)
    t0 = time.time()
    res = _executar_jobs(jobs, processos)
    out = dict(zip(nomes, res))
    det = {"pacote": pacote.resumo(), "config": cfg.como_dict(), "bracos_pedidos": list(bracos), "politicas": list(politicas),
           "modos": list(modos), "k_reservatorio": k_reservatorio, "lesao_apos": lesao_apos, "fontes": hash_fontes(),
           "bracos": {k: v["deterministico"] for k, v in out.items()}}
    det["metricas"] = metricas(det)
    med = {"parede_total_s": time.time() - t0, "bracos": {k: v["medicoes"] for k, v in out.items()}}
    _gravar(pasta, det, med)
    return {"deterministico": det, "medicoes": med}


def executar_ordens(caminho_pacote: str, pasta: str, cfg: ConfigEM, G_total: int, B_max: int,
                    seletores: Sequence[str] = ("autodirigido", "aleatorio", "manual"), aprendizes: Sequence[str] = ("L-lib+f", "L-fix"),
                    sementes_aleatorio: Sequence[int] = (1, 2, 3), processos: int = 4) -> dict:
    """Ordens autodirigida / aleatória / do autor ("manual" = ordem do autor) sobre o conjunto de tarefas
    do pacote, com curriculo_autodirigido (modo zero)."""
    from . import curriculo_autodirigido as C
    from .piloto import _executar_jobs, hash_fontes
    pacote = carregar_pacote(caminho_pacote)
    os.makedirs(pasta, exist_ok=True)
    jobs, nomes = [], []
    for s in seletores:
        for apn in aprendizes:
            sems = list(sementes_aleatorio) if s == "aleatorio" else [cfg.semente]
            for ss in sems:
                jobs.append((C.job_braco, (s, apn, cfg, G_total, B_max, ss, pacote.ordem, TAREFAS_EXTERNAS, pacote.ordem)))
                nomes.append(f"{s}#{ss}/{apn}" if s == "aleatorio" else f"{s}/{apn}")
    t0 = time.time()
    res = _executar_jobs(jobs, processos)
    out = dict(zip(nomes, res))
    for v in out.values():
        d = v["deterministico"]
        for p in d.get("passos", []):
            p["tarefa_autor"] = pacote.interno_para_autor.get(p["tarefa"], p["tarefa"])
    det = {"pacote": pacote.resumo(), "config": cfg.como_dict(), "G": G_total, "B_max": B_max, "fontes": hash_fontes(),
           "bracos": {k: v["deterministico"] for k, v in out.items()},
           "resumo": {k: {"aceitas": [pacote.interno_para_autor.get(t, t) for t in v["deterministico"]["aceitas"]],
                          "ordem": [pacote.interno_para_autor.get(t, t) for t in v["deterministico"]["ordem_aceitacao"]],
                          "custo_total": v["deterministico"]["custo_total"], "gasto_global": v["deterministico"]["gasto_global"],
                          "passos": len(v["deterministico"]["passos"]), "cadeia_reuso": v["deterministico"]["cadeia_reuso"],
                          "falha": v["deterministico"].get("falha")} for k, v in out.items()}}
    med = {"parede_total_s": time.time() - t0, "bracos": {k: v["medicoes"] for k, v in out.items()}}
    _gravar(pasta, det, med, ordens=True)
    return {"deterministico": det, "medicoes": med}


def _replace(cfg: ConfigEM, pol: str) -> ConfigEM:
    import dataclasses
    return dataclasses.replace(cfg, politica_busca=pol)


def _gravar(pasta: str, det: dict, med: dict, ordens: bool = False) -> None:
    with open(os.path.join(pasta, "deterministico.json"), "w", encoding="utf-8") as f:
        json.dump(det, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "medicoes.json"), "w", encoding="utf-8") as f:
        json.dump(med, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "relatorio.md"), "w", encoding="utf-8") as f:
        f.write(relatorio_ordens_md(det, med) if ordens else relatorio_md(det, med))


def relatorio_md(det: dict, med: dict) -> str:
    p = det["pacote"]
    L = [f"# Benchmark externo «{p['nome']}» v{p['versao']} — hash {p['hash'][:16]}…, {p['num_tarefas']} tarefas, semente {det['config']['semente']}, B = {det['config']['B']}", ""]
    L.append("| braço | aceitas | ids aceitas | custo prévio | custo benchmark | custo cumulativo | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for k, m in det["metricas"]["por_braco"].items():
        if "falha" in m:
            L.append(f"| {k} | FALHA | {m['falha']} | | | | | | |")
            continue
        L.append(f"| {k} | {m['aceitas']}/{m['tarefas']} | {', '.join(m['ids_aceitas'])} | {m['custo_previo']:,} | {m['custo_benchmark']:,} | {m['custo_cumulativo']:,} | {m['tarefas_com_reuso']} | {m['entradas_descobertas']} ({m['entradas_reutilizadas']}) | {m['livro_fecha']} |")
    L.append("")
    for k, c in det["metricas"]["comparacoes"].items():
        L.append(f"## {k}")
        if "por_tarefa" in c:
            L.append(f"positivas {c['positivas']}, negativas {c['negativas']}, neutras {c['neutras']}, inconclusivas {c['inconclusivas']}, com reuso {c['com_reuso']}")
            L.append("")
            L.append("| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |")
            L.append("|---|---|---|---|---|---|---|---|---|---|---|")
            for t, v in c["por_tarefa"].items():
                a, b = v["L-lib+f"], v["L-fix"]
                re_ = f"{v['razao_exata']:.2f}" if v.get("razao_exata") is not None else "—"
                rm = f"≥ {v['razao_minima']:.2f}" if v.get("razao_minima") is not None else ("≤ " + f"{1/v['razao_minima_inversa']:.2f}" if v.get("razao_minima_inversa") else "—")
                L.append(f"| {t} | {a['aceita']} | {a['custo']:,} | {a['tamanho']} | {a['reuso']} | {b['aceita']} | {b['custo']:,} | {b['tamanho']} | {re_} | {rm} | {v['classe']} |")
            L.append("")
            L.append("Custo cumulativo igual: " + "; ".join(f"{x['tarefa']}: C={x['custo_cumulativo']:,} → L-lib+f {x['aceitas_L-lib+f']} vs L-fix {x['aceitas_L-fix_ao_mesmo_custo']}" for x in c["aceitas_a_custo_cumulativo_igual"]))
        else:
            L.append(json.dumps(c, ensure_ascii=False))
        L.append("")
    for k, b in det["bracos"].items():
        if b.get("falha"):
            L.append(f"### {k}: FALHA {b['falha']}")
            continue
        L.append(f"### Hipóteses — {k}")
        for t, r in b["resultados"].items():
            L.append(f"- {r['tarefa']}: aceita={r['aceita']} ({r['motivo']}), `{r['hipotese'] or ''}`, custo {r['custo']:,}, reuso {r['biblioteca_usada']}")
        if b.get("abstracoes"):
            L.append("  entradas de biblioteca: " + "; ".join(f"{a['nome']} = `{a.get('legivel') or a.get('corpo')}` ({a.get('proveniencia')}, reut. {a.get('reutilizacoes')})" for a in b["abstracoes"]))
        L.append("")
    L.append("## Medições")
    L.append(f"parede total {med['parede_total_s']:.0f} s")
    for k, m in med["bracos"].items():
        L.append(f"- {k}: parede {m['tempo_parede_s']:.0f} s, CPU {m['cpu_s']:.0f} s, memória {m['memoria_pico_kib']} KiB")
    return "\n".join(L) + "\n"


def relatorio_ordens_md(det: dict, med: dict) -> str:
    p = det["pacote"]
    L = [f"# Benchmark externo «{p['nome']}» — ordens (G = {det['G']}, B_max = {det['B_max']}, semente {det['config']['semente']}, política {det['config']['politica_busca']})", ""]
    L.append("| braço | aceitas | ordem de aceitação | passos | custo total | gasto global | cadeia de reuso |")
    L.append("|---|---|---|---|---|---|---|")
    for k, v in det["resumo"].items():
        L.append(f"| {k} | {len(v['aceitas'])}: {', '.join(v['aceitas'])} | {' → '.join(v['ordem'])} | {v['passos']} | {v['custo_total']:,} | {v['gasto_global']:,} | {v['cadeia_reuso']} |")
    L.append("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- verificação pós-execução (selados)
def verificar_benchmark(pasta_run: str, ns_amostral: Sequence[int] = (5, 6, 7, 8, 9), k: int = 40, exaustivo: bool = True) -> dict:
    """Regimes de verificacao.py + testes ocultos do autor + testemunhas (exprimibilidade/tamanho)."""
    from . import verificacao as V
    from .avaliador import compilar
    from .dsl import BASES, parse, tamanho, tipo_de
    with open(os.path.join(pasta_run, "deterministico.json"), encoding="utf-8") as f:
        d = json.load(f)
    pacote = carregar_pacote(os.path.join(RAIZ, d["pacote"]["caminho"]), hash_esperado=d["pacote"]["hash"])
    res = V.verificar_execucao(pasta_run, ns_amostral, k, exaustivo=exaustivo)
    selados = carregar_selados(pacote)
    tabela = BASES["E0"].para_aprendiz()
    ocultos = []
    for h in res["hipoteses"]:
        tid = h["tarefa"]
        grades = selados["testes_ocultos"].get(tid, [])
        if not grades:
            continue
        b = d["bracos"][h["braco"]]
        t = V.expandir_entradas(parse(h["hipotese"]), V.corpos_do_braco(b, tid))
        ev = compilar(t)
        tarefa = TAREFAS_EXTERNAS[tid]
        pares = []
        for g in grades:
            for args in A.entradas_da_grade(tarefa, g):
                v, _, ind = V._avaliar(ev, tabela, tarefa, args, 2_000_000)
                pares.append((A.saida_referencia(tarefa, args), v, ind))
        r = V._resumo(pares)
        r.update({"braco": h["braco"], "tarefa": pacote.interno_para_autor[tid], "grades": len(grades)})
        ocultos.append(r)
    testemunhas = {}
    for tid, prog in selados["testemunhas"].items():
        try:
            t = parse(prog)
            tp = tipo_de(t, {}, tabela)
            tarefa = TAREFAS_EXTERNAS[tid]
            ok_tipo = tp == tarefa.tipo
            ver = V.verificar_exaustivo(t, tarefa, ns=(1, 2, 3), tabela=tabela)
            testemunhas[pacote.interno_para_autor[tid]] = {"tamanho": tamanho(t), "tipo_ok": ok_tipo, "erros_n_le_3": ver["erros"]}
        except Exception as e:  # noqa: BLE001
            testemunhas[pacote.interno_para_autor[tid]] = {"erro": f"{type(e).__name__}: {e}"}
    res["testes_ocultos_autor"] = ocultos
    res["testemunhas"] = testemunhas
    res["erros_previsao"] = {"exaustivo": sum(h["exaustivo"]["erros"] for h in res["hipoteses"] if "exaustivo" in h),
                             "amostral": sum(rn["natural"]["erros"] for h in res["hipoteses"] for rn in h["amostral"]["por_n"].values()),
                             "ocultos_autor": sum(o["erros"] for o in ocultos)}
    with open(os.path.join(pasta_run, "verificacao.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Executor de benchmarks externos (protocolo-avaliacao.md)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validar"); v.add_argument("pacote")
    e = sub.add_parser("executar")
    e.add_argument("pacote"); e.add_argument("--id", required=True); e.add_argument("--semente", type=int, default=10_007)
    e.add_argument("--B", type=int, default=20_000); e.add_argument("--bracos", default=",".join(BRACOS))
    e.add_argument("--politicas", default="tamanho,unigrama"); e.add_argument("--modos", default="zero")
    e.add_argument("--k-reservatorio", type=int, default=40); e.add_argument("--processos", type=int, default=4)
    o = sub.add_parser("ordens")
    o.add_argument("pacote"); o.add_argument("--id", required=True); o.add_argument("--semente", type=int, default=10_007)
    o.add_argument("--G", type=int, default=240_000); o.add_argument("--B-max", type=int, default=20_000)
    o.add_argument("--politica", default="tamanho"); o.add_argument("--seletores", default="autodirigido,aleatorio,manual")
    o.add_argument("--aprendizes", default="L-lib+f,L-fix"); o.add_argument("--sementes-aleatorio", default="1,2,3")
    o.add_argument("--processos", type=int, default=4)
    w = sub.add_parser("verificar"); w.add_argument("run"); w.add_argument("--sem-exaustivo", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "validar":
        val = validar_pacote(a.pacote)
        print(json.dumps(val, ensure_ascii=False, indent=1))
        return 0 if val["ok"] else 1
    if a.cmd == "executar":
        cfg = ConfigEM(semente=a.semente, B=a.B, processos=a.processos, sondas=False, auditoria_oe_orcamento=0)
        r = executar(a.pacote, os.path.join("runs", a.id), cfg, a.bracos.split(","), a.politicas.split(","), a.modos.split(","),
                     a.k_reservatorio, a.processos)
        print(json.dumps(r["deterministico"]["metricas"]["por_braco"], ensure_ascii=False, indent=1, default=str))
        return 0
    if a.cmd == "ordens":
        cfg = ConfigEM(semente=a.semente, B=a.B_max, politica_busca=a.politica, processos=a.processos, sondas=False, auditoria_oe_orcamento=0)
        r = executar_ordens(a.pacote, os.path.join("runs", a.id), cfg, a.G, a.B_max, a.seletores.split(","), a.aprendizes.split(","),
                            [int(x) for x in a.sementes_aleatorio.split(",")], a.processos)
        print(json.dumps(r["deterministico"]["resumo"], ensure_ascii=False, indent=1, default=str))
        return 0
    if a.cmd == "verificar":
        r = verificar_benchmark(a.run, exaustivo=not a.sem_exaustivo)
        print(json.dumps(r["erros_previsao"], ensure_ascii=False))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
