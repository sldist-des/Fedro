"""Experimento mínimo de aquisição e transferência (documento 05, missão 2).

Pergunta: um aprendiz que recebe SÓ exemplos e contraexemplos encontra uma operação intermediária,
consolida-a na sua biblioteca e a REUTILIZA numa tarefa posterior inédita, com economia de recursos
em relação ao mesmo aprendiz sem biblioteca, a custo cumulativo equivalente?

Currículo principal (todas as tarefas definidas pelo ambiente; nenhuma solução manual é dada):
  T1 vizPretos  (Grade → Pos → L Pos)   função: vizinhas pretas de p
  T2 expandir   (Grade → L Pos → L Pos) função: vizinhas pretas de um conjunto (um passo)
  T3 ParAdjacente (Grade → Bool)        predicado: existe par de pretas adjacentes
  T4 NenhumaIsolada (Grade → Bool)      predicado: toda preta tem vizinha preta
Currículo NÃO relacionado (controle): U1 pretasColuna1, U2 semLinha1, depois T3 e T4.

Braços (mesma informação de treino: exemplos, contraexemplos e teste são gerados por tarefa a partir
da mesma semente; mesma política de busca; só a biblioteca muda):
  L-fix            sem biblioteca
  L-lib            compressão por recorrência (só fragmentos repetidos entre soluções)
  L-lib+f          L-lib + promoção das soluções de tarefas de função a entradas de biblioteca
  L-lib+f/lesao    L-lib+f até T2; LESÃO (remove as entradas descobertas); depois T3, T4
  L-lib+f/controle L-lib+f no currículo não relacionado U1, U2, depois T3, T4
  L-fix/custo-igual L-fix só em T3, com orçamento = B + (custo cumulativo de L-lib+f antes de T3 −
                   custo cumulativo de L-fix antes de T3), se positivo
  L-fix/10x        L-fix só em T3 com 10·B (sonda de limite)

Tudo determinístico por semente; medições de tempo e memória em bloco separado. Nenhum resultado
aqui é evidência para H-B1: dados e hiperparâmetros expostos (documento 03, §0 e §11).
"""
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from . import aprendizes as A
from . import geradores as G
from .dsl import BASES, BOOL, FUN, GRADE, LP, POS, constantes
from .grade import Grade
from .razao import LivroRazao

_GP, _GL, _PB = FUN(GRADE, POS, LP), FUN(GRADE, LP, LP), FUN(GRADE, BOOL)

TAREFAS: Dict[str, A.Tarefa] = {t.id: t for t in [
    A.Tarefa("vizPretos", _GP, "funcao", "EM"),
    A.Tarefa("expandir", _GL, "funcao", "EM", comparacao="conjunto"),
    A.Tarefa("ParAdjacente", _PB, "predicado", "EM", "ParAdjacente"),
    A.Tarefa("NenhumaIsolada", _PB, "predicado", "EM", "NenhumaIsolada"),
    A.Tarefa("pretasColuna1", _GP, "funcao", "EM-controle"),
    A.Tarefa("semLinha1", _GL, "funcao", "EM-controle", comparacao="conjunto"),
]}
CURRICULO = ["vizPretos", "expandir", "ParAdjacente", "NenhumaIsolada"]
CURRICULO_CONTROLE = ["pretasColuna1", "semLinha1", "ParAdjacente", "NenhumaIsolada"]
BRACOS = ("L-fix", "L-lib", "L-lib+f", "L-lib+f/lesao", "L-lib+f/controle")


@dataclass
class ConfigEM:
    semente: int = 10_002
    base: str = "E0"
    B: int = 20_000
    K: int = 12
    limiar: int = 3
    politica_busca: str = "tamanho"
    orcamento_passos: int = 100_000
    bracos: Tuple[str, ...] = BRACOS
    sondas: bool = True            # L-fix/custo-igual e L-fix/10x
    processos: int = 4
    memoria_trabalhador_gb: Optional[float] = 6.0
    num_teste: int = 30
    auditoria_oe_orcamento: int = 30_000     # 0 desliga a auditoria OE dos alvos
    auditoria_oe_s_max: int = 8
    escala: str = "exploratoria-minima"

    def como_dict(self) -> dict:
        d = asdict(self)
        d.pop("processos")
        return d


def _ambiente(cfg: ConfigEM) -> A.Ambiente:
    return A.Ambiente(cfg.semente, num_teste=cfg.num_teste)


def _aprendiz(nome: str, cfg: ConfigEM, livro: LivroRazao, B: Optional[int] = None, rotulo: Optional[str] = None):
    kw = dict(B=B or cfg.B, K=cfg.K, orcamento_passos=cfg.orcamento_passos,
              kw_enumerador={"semente": cfg.semente}, politica_busca=cfg.politica_busca,
              rotulo_base=rotulo or cfg.base)
    tab = BASES[cfg.base]
    if nome.startswith("L-fix"):
        return A.LFix(tab, livro, **kw)
    promover = nome.startswith("L-lib+f")
    return A.LLib(tab, livro, limiar=cfg.limiar, promover_funcoes=promover, **kw)


def _curva(ap) -> List[dict]:
    """Custo cumulativo (total do aprendiz, candidatos de enumeração e do protocolo) tarefa a tarefa."""
    out, cum, cum_e, cum_c = [], 0, 0, 0
    for r in ap.resultados:
        e = ap.livro.entrada(r.tarefa_id, ap.aprendiz_id)
        cum += e.total_aprendiz(); cum_e += e.enumeracao_candidatos; cum_c += e.busca_candidatos
        out.append({"tarefa": r.tarefa_id, "aceita": r.aceita, "motivo": r.motivo_fim, "rodadas": r.rodadas,
                    "custo_aprendiz": e.total_aprendiz(), "cumulativo": cum,
                    "enumeracao_candidatos": e.enumeracao_candidatos, "cumulativo_enumeracao": cum_e,
                    "busca_candidatos": e.busca_candidatos, "cumulativo_busca": cum_c,
                    "compressao_subtermos": e.compressao_subtermos,
                    "hipotese": r.hipotese_legivel, "tamanho": r.tamanho,
                    "constantes_biblioteca_usadas": list(r.constantes_biblioteca_usadas),
                    "reutilizacoes": dict(r.reutilizacoes), "teste": r.teste_resumo,
                    "refinamentos_oe": r.contador_busca.get("refinamentos_oe"),
                    "custos_folha_distintos": sorted(set(r.custos_folha.values()))})
    return out


def _grades_de(amb: A.Ambiente, ids: Sequence[str]) -> Dict[str, List[str]]:
    out = {}
    for tid in ids:
        p = amb.preparar(TAREFAS[tid])
        for k, v in p.grades().items():
            out[f"tarefa:{tid}:{k}"] = sorted({g.serializar() for g in v})
    return out


def job_braco(nome: str, cfg: ConfigEM, B_por_tarefa: Optional[Dict[str, int]] = None,
              so_tarefas: Optional[Sequence[str]] = None) -> dict:
    """Executa um braço num processo próprio. Devolve {deterministico, medicoes, grades}."""
    from .medidas import medir_isolado
    from .piloto import limitar_memoria
    limitar_memoria(cfg.memoria_trabalhador_gb)
    amb = _ambiente(cfg)
    livro = LivroRazao(cfg.semente, {"braco": nome, "experimento": "minimo"})
    curr = CURRICULO_CONTROLE if nome == "L-lib+f/controle" else CURRICULO
    if so_tarefas:
        curr = list(so_tarefas)
    ap = _aprendiz(nome, cfg, livro, rotulo=f"{cfg.base}/{nome}")
    eventos: List[dict] = []
    c0 = time.process_time()
    with medir_isolado(nome) as m:
        for tid in curr:
            if nome == "L-lib+f/lesao" and tid == "ParAdjacente":
                removidas = ap.lesionar()
                eventos.append({"antes_de": tid, "lesao": removidas,
                                "tabela_apos": ap.tabela_corrente().nomes()})
            if B_por_tarefa and tid in B_por_tarefa:
                ap.B = int(B_por_tarefa[tid])
                eventos.append({"antes_de": tid, "B": ap.B})
            ap.resolver(TAREFAS[tid], amb)
    rel = ap.relatorio()
    det = {"braco": nome, "curriculo": curr, "relatorio": rel, "abstracoes": A.abstracoes(ap),
           "curva": _curva(ap), "eventos": eventos, "livro": livro.deterministico_dict(incluir_diario=True),
           "dependente_de_recurso": any(r.inconclusivo_recurso for r in ap.resultados),
           "preparos": [amb.preparar(TAREFAS[t]).como_dict() for t in curr]}
    med = {"livro": livro.medicoes_dict(), "tempo_parede_s": m.tempo_parede_s,
           "cpu_s": time.process_time() - c0, "memoria_pico_kib": m.memoria_pico_kib,
           "memoria_escopo": m.memoria_escopo}
    return {"deterministico": det, "medicoes": med, "grades": _grades_de(amb, curr)}


# ----------------------------------------------------------------------------------------------
# Auditoria da poda OE para os alvos do experimento (referências Python do ambiente; nenhum
# programa manual): a classe de denotação do alvo está entre os representantes OE até o custo c?
# ----------------------------------------------------------------------------------------------
def classe_alvo_presente(tabela, tarefa: A.Tarefa, s_max: int, orcamento: int, semente: int,
                         custos_folha: Optional[Dict[str, int]] = None) -> dict:
    """Enumera (com poda OE, mundos de oraculo_treino) até o custo s_max e verifica, numa amostra
    INDEPENDENTE (grades de teste_int), se algum representante denota a referência da tarefa. Uso de
    auditoria: a tabela pode conter entradas descobertas do braço; nunca entradas manuais."""
    from .avaliador import Contador, Contexto, aplicar, compilar
    from .enumerador import Enumerador
    rng = G.rng_derivado(semente, "em:auditoria-oe", tarefa.id)
    # amostra independente grande: 48 grades de teste_int (n = 3..6); com 6 grades um termo espúrio
    # coincidiu com a referência de ParAdjacente no teste de fumaça (registrado)
    grades = [G.amostra_natural(n, rng, particao="teste_int") for n in (3, 4, 5, 6) * 12]
    por_grade = 1 if tarefa.natureza == "predicado" else 4
    entradas = [a for g in grades for a in A.entradas_da_grade(tarefa, g)[:por_grade]]
    alvo = tuple(A.valor_json(A.saida_referencia(tarefa, a)) for a in entradas)
    en = Enumerador(tabela, {}, tarefa.tipo, orcamento=orcamento, semente=semente, auditoria=True,
                    custos_folha=custos_folha)
    presente, custo_do_alvo, termo_alvo = False, None, None
    try:
        for s in range(1, s_max + 1):
            for t, _ in en.representantes(s):
                ev = compilar(t)
                try:
                    sig = tuple(A.valor_json(aplicar(ev({}, Contexto(A.n_semantica(tarefa, a), Contador(100_000), tabela)), *a))
                                for a in entradas)
                except Exception:
                    continue
                if sig == alvo:
                    presente, custo_do_alvo, termo_alvo = True, s, t
                    break
            if presente:
                break
    except Exception as e:   # orçamento do enumerador esgotado
        return {"tarefa": tarefa.id, "presente": presente, "custo_do_alvo": custo_do_alvo,
                "ate_custo": en.s_completo, "interrompido": type(e).__name__, "candidatos": en.cont.candidatos_avaliados}
    from .dsl import imprimir_legivel
    return {"tarefa": tarefa.id, "presente": presente, "custo_do_alvo": custo_do_alvo,
            "termo": imprimir_legivel(termo_alvo) if termo_alvo else None, "ate_custo": en.s_completo,
            "candidatos": en.cont.candidatos_avaliados, "entradas_independentes": len(entradas)}


# ----------------------------------------------------------------------------------------------
# Orquestração
# ----------------------------------------------------------------------------------------------
def _executar(jobs, processos: int):
    from .piloto import _executar_jobs
    return _executar_jobs(jobs, processos)


def _cum_antes(curva: List[dict], tid: str, campo: str = "cumulativo_enumeracao") -> int:
    cum = 0
    for x in curva:
        if x["tarefa"] == tid:
            return cum
        cum = x[campo]
    return cum


def analisar(bracos: Dict[str, dict], cfg: ConfigEM) -> dict:
    """Critério central (documento 05): abstração encontrada pelo aprendiz, reutilizada numa tarefa
    posterior inédita, com proveniência verificável, e economia em relação a L-fix a custo equivalente."""
    out: Dict[str, dict] = {}
    for nome, d in bracos.items():
        det = d["deterministico"]
        abst = det["abstracoes"]
        reut = [a for a in abst if a.get("reutilizacoes") or a.get("reutilizacoes_indiretas")]
        aceitas = [x["tarefa"] for x in det["curva"] if x["aceita"]]
        reuso_em_aceitas = {}
        for x in det["curva"]:
            if x["aceita"] and x["constantes_biblioteca_usadas"]:
                reuso_em_aceitas[x["tarefa"]] = x["constantes_biblioteca_usadas"]
        out[nome] = {"aceitas": aceitas, "abstracoes": len(abst),
                     "abstracoes_reutilizadas": [a["nome"] for a in reut],
                     "reuso_em_solucoes_aceitas": reuso_em_aceitas,
                     "cadeia_indireta": {a["nome"]: a.get("reutilizacoes_indiretas") for a in abst
                                         if a.get("reutilizacoes_indiretas")},
                     "testes_degenerados": [x["tarefa"] for x in det["curva"] if x["aceita"] and x["teste"].get("degenerado")],
                     "curva": [(x["tarefa"], x["aceita"], x["cumulativo"]) for x in det["curva"]]}
    crit = {"abstracao_descoberta_e_reutilizada_em_tarefa_inedita": False, "braco": None, "detalhe": ""}
    for nome in ("L-lib+f", "L-lib"):
        if nome in out and out[nome]["reuso_em_solucoes_aceitas"]:
            tarefas_reuso = out[nome]["reuso_em_solucoes_aceitas"]
            # inédita = não é tarefa de origem de nenhuma entrada usada
            abst = {a["nome"]: a for a in bracos[nome]["deterministico"]["abstracoes"]}
            ineditas = {t: cs for t, cs in tarefas_reuso.items()
                        if all(t not in abst[c]["tarefas_origem"] for c in cs if c in abst)}
            if ineditas:
                fix_ok = {t: any(x["tarefa"] == t and x["aceita"] for x in bracos.get("L-fix", {"deterministico": {"curva": []}})["deterministico"]["curva"])
                          for t in ineditas}
                crit = {"abstracao_descoberta_e_reutilizada_em_tarefa_inedita": True, "braco": nome,
                        "tarefas": ineditas, "L-fix_resolveu_a_mesma_tarefa_no_orcamento_B": fix_ok,
                        "detalhe": "verificar também L-fix/custo-igual e L-fix/10x abaixo"}
                break
    return {"por_braco": out, "criterio_central": crit}


def executar(cfg: ConfigEM, pasta: str) -> dict:
    from .piloto import hash_fontes
    os.makedirs(pasta, exist_ok=True)
    t0 = time.time()
    jobs = [(job_braco, (b, cfg)) for b in cfg.bracos]
    res = _executar(jobs, cfg.processos)
    bracos = dict(zip(cfg.bracos, res))
    # sondas de custo igual (dependem das curvas de L-fix e L-lib+f)
    sondas = {}
    if cfg.sondas and "L-fix" in bracos and "L-lib+f" in bracos:
        cf = _cum_antes(bracos["L-fix"]["deterministico"]["curva"], "ParAdjacente")
        cl = _cum_antes(bracos["L-lib+f"]["deterministico"]["curva"], "ParAdjacente")
        delta = cl - cf
        plano = {"L-fix/custo-igual": {"ParAdjacente": cfg.B + max(0, delta)}, "L-fix/10x": {"ParAdjacente": 10 * cfg.B}}
        sondas["plano"] = {"cumulativo_enumeracao_antes_T3": {"L-fix": cf, "L-lib+f": cl}, "delta": delta,
                           "B_T3": {k: v["ParAdjacente"] for k, v in plano.items()},
                           "nota": "delta <= 0 significa que L-fix já gastou mais que L-lib+f antes de T3; a sonda roda com B"}
        js = [(job_braco, (k, cfg, v, ["ParAdjacente"])) for k, v in plano.items()]
        rs = _executar(js, min(cfg.processos, 2))
        for (k, _), r in zip(plano.items(), rs):
            bracos[k] = r
    # auditoria OE dos alvos (tabela base sem biblioteca e tabela de L-lib+f com as descobertas)
    aud = {}
    if cfg.auditoria_oe_orcamento > 0:
        try:
            tab_base = BASES[cfg.base].para_aprendiz()
            for tid in ("vizPretos", "expandir", "ParAdjacente"):
                aud[f"base:{tid}"] = classe_alvo_presente(tab_base, TAREFAS[tid], cfg.auditoria_oe_s_max,
                                                          cfg.auditoria_oe_orcamento, cfg.semente)
        except Exception as e:
            aud["erro"] = repr(e)
    analise = analisar(bracos, cfg)
    det = {"config": cfg.como_dict(), "fontes": hash_fontes(), "tarefas": {k: v.como_dict() for k, v in TAREFAS.items()},
           "bracos": {k: v["deterministico"] for k, v in bracos.items()}, "sondas": sondas,
           "auditoria_oe": aud, "analise": analise}
    med = {"tempo_parede_total_s": time.time() - t0,
           "bracos": {k: v["medicoes"] for k, v in bracos.items()}}
    grades = {k: v["grades"] for k, v in bracos.items()}
    hashes = {k: {kk: G.hash_conjunto([Grade.de_texto(x) for x in vv]) for kk, vv in v.items()} for k, v in grades.items()}
    with open(os.path.join(pasta, "deterministico.json"), "w", encoding="utf-8") as f:
        json.dump(det, f, ensure_ascii=False, sort_keys=True, indent=1, default=str)
    with open(os.path.join(pasta, "medicoes.json"), "w", encoding="utf-8") as f:
        json.dump(med, f, ensure_ascii=False, sort_keys=True, indent=1, default=str)
    with open(os.path.join(pasta, "hashes.json"), "w", encoding="utf-8") as f:
        json.dump(hashes, f, ensure_ascii=False, sort_keys=True, indent=1)
    with open(os.path.join(pasta, "relatorio.md"), "w", encoding="utf-8") as f:
        f.write(relatorio_md(det, med))
    return {"deterministico": det, "medicoes": med}


def relatorio_md(det: dict, med: dict) -> str:
    L = [f"# Experimento mínimo — registros ({det['config']['escala']}, semente {det['config']['semente']}, "
         f"B = {det['config']['B']}, política {det['config']['politica_busca']})", ""]
    L.append("| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nome, b in det["bracos"].items():
        for x in b["curva"]:
            t = x["teste"] or {}
            acc = t.get("acuracia"); bal = t.get("acuracia_balanceada")
            L.append(f"| {nome} | {x['tarefa']} | {x['aceita']} | {x['rodadas']} | {x['motivo']} | {x['tamanho'] or ''} | "
                     f"`{x['hipotese'] or ''}` | {', '.join(x['constantes_biblioteca_usadas'])} | {x['custo_aprendiz']} | "
                     f"{x['cumulativo']} | {x['cumulativo_enumeracao']} | "
                     f"{'' if acc is None else f'{acc:.2f}'} / {'' if bal is None else f'{bal:.2f}'} / {t.get('degenerado', '')} |")
    L.append("")
    L.append("## Abstrações por braço (proveniência, origem, reutilização)")
    for nome, b in det["bracos"].items():
        for a in b["abstracoes"]:
            L.append(f"- {nome}: `{a['nome']}` = `{a['legivel']}` ({a['tipo']}; {a['metodo']}; proveniência {a['proveniencia']}; "
                     f"origem {a['tarefas_origem']}; reutilizações diretas {a['reutilizacoes']}; indiretas {a.get('reutilizacoes_indiretas')}; "
                     f"cópia de solução: {a.get('copia_de_solucao')})")
        for ev in b.get("eventos", []):
            L.append(f"- {nome}: evento {json.dumps(ev, ensure_ascii=False)[:300]}")
    L.append("")
    L.append("## Sondas de custo igual")
    L.append("```\n" + json.dumps(det.get("sondas"), ensure_ascii=False, indent=1) + "\n```")
    L.append("## Auditoria OE dos alvos (tabela base)")
    L.append("```\n" + json.dumps(det.get("auditoria_oe"), ensure_ascii=False, indent=1) + "\n```")
    L.append("## Análise (critério central)")
    L.append("```\n" + json.dumps(det["analise"]["criterio_central"], ensure_ascii=False, indent=1) + "\n```")
    L.append("## Medições (tempo e memória; separadas dos contadores)")
    for nome, m in med["bracos"].items():
        L.append(f"- {nome}: parede {m['tempo_parede_s']:.1f} s; CPU {m['cpu_s']:.1f} s; memória de pico {m['memoria_pico_kib']} KiB ({m['memoria_escopo']})")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Experimento mínimo de aquisição e transferência (documento 05)")
    ap.add_argument("--id", required=True)
    ap.add_argument("--semente", type=int, default=10_002)
    ap.add_argument("--B", type=int, default=20_000)
    ap.add_argument("--politica", default="tamanho", choices=A.POLITICAS_BUSCA)
    ap.add_argument("--base", default="E0")
    ap.add_argument("--bracos", default=",".join(BRACOS))
    ap.add_argument("--sem-sondas", action="store_true")
    ap.add_argument("--processos", type=int, default=4)
    ap.add_argument("--memoria-gb", type=float, default=6.0)
    ap.add_argument("--auditoria-oe", type=int, default=30_000, help="orçamento da auditoria OE (0 desliga)")
    a = ap.parse_args(argv)
    cfg = ConfigEM(semente=a.semente, base=a.base, B=a.B, politica_busca=a.politica,
                   bracos=tuple(a.bracos.split(",")), sondas=not a.sem_sondas, processos=a.processos,
                   memoria_trabalhador_gb=a.memoria_gb, auditoria_oe_orcamento=a.auditoria_oe)
    pasta = os.path.join("runs", a.id)
    r = executar(cfg, pasta)
    print(json.dumps(r["deterministico"]["analise"], ensure_ascii=False, indent=1))
    print("registros em", pasta)


if __name__ == "__main__":
    main()
