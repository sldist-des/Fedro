"""Verificação das hipóteses aceitas de uma execução (documento 06, missão 1).

Três regimes, sempre reportados separadamente:
  1. EXAUSTIVO SOBRE GRADES, n = 1..4: todas as 2^(n²) grades. Para predicados é exaustivo no domínio.
     Para tarefas de função, exaustivo sobre as grades e sobre a BATERIA DE ARGUMENTOS do ambiente
     (entradas_da_grade): a bateria é uma amostra finita do domínio de listas, logo o regime chama-se
     "exaustivo em grades, bateria finita de argumentos" e não "exaustivo".
  2. AMOSTRAL EM DIMENSÕES NOVAS, n = 5..9, partição teste_ext (baldes 40–49, nunca usados no treino
     nem no teste interno): distribuição natural (mistura de Bernoulli) e, para predicados, positivos
     construtivos com negativos emparelhados em densidade (distribuição de desenho).
  3. Para cada regime: acurácia, acurácia balanceada (quando há as duas classes), contagens por classe
     e marca de conjunto degenerado.
As constantes de biblioteca das hipóteses são expandidas pelos corpos registrados (inclusive os de
entradas depois lesionadas). As referências usadas são as do AMBIENTE (Python), nunca programas manuais.
Uso: python3 -m fedro_piloto.verificacao --run runs/em-s10002-tamanho [--ns-amostral 5,6,7,8,9] [--k 40]
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List, Optional, Sequence

from . import aprendizes as A
from . import geradores as G
from .avaliador import Contador, Contexto, OrcamentoEsgotado, aplicar, compilar
from .dsl import BASES, Termo, parse
from .grade import Grade, todas_as_grades
from .referencias import REGISTRO

PARTICAO_NOVAS_DIMENSOES = "teste_ext"


def expandir_entradas(t: Termo, corpos: Dict[str, Termo]) -> Termo:
    """Substitui recursivamente as constantes de biblioteca pelos seus corpos (termos fechados)."""
    if t[0] == "c" and t[1] in corpos:
        return expandir_entradas(corpos[t[1]], corpos)
    if t[0] == "ap":
        return ("ap", expandir_entradas(t[1], corpos), expandir_entradas(t[2], corpos))
    if t[0] == "lam":
        return ("lam", t[1], t[2], expandir_entradas(t[3], corpos))
    if t[0] == "fix":
        return ("fix", t[1], expandir_entradas(t[2], corpos))
    return t


def corpos_do_braco(braco: dict, tarefa_id: Optional[str] = None) -> Dict[str, Termo]:
    """Corpos das entradas de biblioteca do braço, resolvidos NO TEMPO da tarefa `tarefa_id`.

    Depois de uma lesão a biblioteca recomeça a numerar as entradas (abs1, abs2, …), logo o mesmo nome
    pode designar corpos diferentes antes e depois da lesão. Para uma hipótese aceita ANTES da lesão
    (tarefa anterior a `antes_de` na ordem do braço) valem as entradas removidas pela lesão; para as
    posteriores valem as entradas finais. Sem `tarefa_id` (ou sem lesão), as finais prevalecem e as
    lesionadas só preenchem nomes ausentes (comportamento anterior; achado de revisão do documento 08)."""
    finais = {a["nome"]: parse(a["corpo"]) for a in braco.get("abstracoes", [])}
    lesoes = [ev for ev in braco.get("eventos", []) if ev.get("lesao")]
    if tarefa_id is not None and lesoes:
        ordem = _ordem_tarefas(braco)
        for ev in lesoes:
            antes = ev.get("antes_de")
            if antes in ordem and tarefa_id in ordem and ordem.index(tarefa_id) < ordem.index(antes):
                corpos = {a["nome"]: parse(a["corpo"]) for a in ev["lesao"]}
                for k, v in finais.items():
                    corpos.setdefault(k, v)
                return corpos
    corpos = dict(finais)
    for ev in lesoes:
        for a in ev["lesao"]:
            corpos.setdefault(a["nome"], parse(a["corpo"]))
    return corpos


def _ordem_tarefas(braco: dict) -> List[str]:
    """Ordem das tarefas do braço nos três formatos de registro (ids internos quando existem)."""
    previo = [p.get("interno") or p.get("tarefa") for p in braco.get("previo", [])]   # fase prévia (modo "previo")
    if braco.get("curva"):
        return previo + [p.get("interno") or p.get("tarefa") for p in braco["curva"]]
    if braco.get("relatorio", {}).get("resultados"):
        return [x["tarefa_id"] for x in braco["relatorio"]["resultados"]]
    if braco.get("passos"):
        out = []
        for p in braco["passos"]:
            if p["tarefa"] not in out:
                out.append(p["tarefa"])
        return out
    return []


def tarefa_por_id(tid: str) -> A.Tarefa:
    from .experimento_minimo import TAREFAS
    if tid in TAREFAS:
        return TAREFAS[tid]
    if tid.startswith("bx:"):            # tarefa de benchmark externo (benchmark_externo.carregar_pacote)
        from .benchmark_externo import TAREFAS_EXTERNAS
        return TAREFAS_EXTERNAS[tid]
    try:
        from .familias_transferencia import TAREFAS as TT
        if tid in TT:
            return TT[tid]
    except ImportError:
        pass
    return A.TAREFAS_POR_ID[tid]


def _avaliar(ev, tabela, tarefa, args, orcamento_passos: int):
    c = Contador(orcamento_passos)
    try:
        return aplicar(ev({}, Contexto(A.n_semantica(tarefa, args), c, tabela)), *args), c.passos, False
    except OrcamentoEsgotado:
        return None, c.passos, True


def _resumo(pares: List[tuple]) -> dict:
    """pares = [(esperado, obtido, indefinido)]. Acurácia, balanceada, contagens por classe."""
    por: Dict[str, List[int]] = {}
    indef = 0
    for esperado, obtido, ind in pares:
        k = str(esperado) if isinstance(esperado, bool) else "saida"
        por.setdefault(k, [0, 0])
        por[k][1] += 1
        if ind:
            indef += 1
        elif obtido == esperado:
            por[k][0] += 1
    n = sum(t for _, t in por.values())
    acertos = sum(a for a, _ in por.values())
    classes = {k: {"acertos": a, "total": t} for k, (a, t) in sorted(por.items())}
    degenerado = len(por) < 2
    bal = None if degenerado or n == 0 else sum(a / t for a, t in por.values()) / len(por)
    return {"n": n, "erros": n - acertos, "acuracia": (acertos / n) if n else None,
            "acuracia_balanceada": bal, "por_classe": classes, "degenerado": degenerado,
            "indefinidas_por_orcamento": indef}


def verificar_exaustivo(termo: Termo, tarefa: A.Tarefa, ns: Sequence[int] = (1, 2, 3, 4),
                        tabela=None, orcamento_passos: int = 2_000_000) -> dict:
    """Regime 1. Grades exaustivas; para funções, toda a bateria de argumentos de cada grade."""
    tabela = tabela or BASES["E0"].para_aprendiz()
    ev = compilar(termo)
    por_n = {}
    for n in ns:
        pares = []
        grades = 0
        for g in todas_as_grades(n):
            grades += 1
            for args in A.entradas_da_grade(tarefa, g):
                esperado = A.saida_referencia(tarefa, args)
                v, _, ind = _avaliar(ev, tabela, tarefa, args, orcamento_passos)
                pares.append((esperado, v, ind))
        r = _resumo(pares)
        r["grades"] = grades
        por_n[n] = r
    total = sum(r["n"] for r in por_n.values())
    erros = sum(r["erros"] for r in por_n.values())
    return {"regime": ("exaustivo em grades (n ≤ 4)" if tarefa.natureza == "predicado"
                       else "exaustivo em grades (n ≤ 4), bateria finita de argumentos do ambiente"),
            "bateria_argumentos": tarefa.natureza == "funcao", "por_n": por_n,
            "entradas": total, "erros": erros}


def validar_amostral(termo: Termo, tarefa: A.Tarefa, ns: Sequence[int] = (5, 6, 7, 8, 9), k: int = 40,
                     semente: int = 10_002, particao: str = PARTICAO_NOVAS_DIMENSOES, tabela=None,
                     orcamento_passos: int = 5_000_000) -> dict:
    """Regime 2. Por n: k grades naturais da partição (funções: até 4 entradas da bateria por grade) e,
    para predicados, k/2 positivos construtivos com negativos emparelhados (desenho)."""
    tabela = tabela or BASES["E0"].para_aprendiz()
    ev = compilar(termo)
    out = {}
    for n in ns:
        rng = G.rng_derivado(semente, "verificacao:amostral", tarefa.id, n)
        cg = G.ContadorGeracao()
        pares_nat = []
        for _ in range(k):
            g = G.amostra_natural(n, rng, particao=particao, contador=cg)
            ents = A.entradas_da_grade(tarefa, g)
            if tarefa.natureza != "predicado":
                ents = [ents[i] for i in sorted(rng.sample(range(len(ents)), min(4, len(ents))))]
            for args in ents:
                v, _, ind = _avaliar(ev, tabela, tarefa, args, orcamento_passos)
                pares_nat.append((A.saida_referencia(tarefa, args), v, ind))
        r = {"natural": _resumo(pares_nat), "grades_naturais": k}
        if tarefa.natureza == "predicado":
            c = REGISTRO[tarefa.conceito]
            pares_des = []
            pos = neg = 0
            for _ in range(k // 2):
                g = G.gerar_positivo(c, n, particao, rng, cg, tentativas=300)
                if g is None:
                    continue
                v, _, ind = _avaliar(ev, tabela, tarefa, (g,), orcamento_passos)
                pares_des.append((True, v, ind)); pos += 1
                par = G.negativo_emparelhado(g, c, rng, particao, "auto", cg)
                if par is not None:
                    v, _, ind = _avaliar(ev, tabela, tarefa, (par[0],), orcamento_passos)
                    pares_des.append((False, v, ind)); neg += 1
            r["desenho"] = _resumo(pares_des)
            r["desenho"]["positivos_construtivos"] = pos
            r["desenho"]["negativos_emparelhados"] = neg
        out[n] = r
    return {"regime": f"amostral em dimensões novas (n = {min(ns)}..{max(ns)}), partição {particao}",
            "por_n": out}


def hipoteses_aceitas(braco: dict) -> List[tuple]:
    """(tarefa_id, hipótese bruta) aceitas num braço, nos três formatos de registro: experimento mínimo
    (relatorio.resultados), transferência (resultados por tarefa) e currículo autodirigido (passos)."""
    out = []
    for x in braco.get("relatorio", {}).get("resultados", []):
        if x.get("aceita") and x.get("hipotese"):
            out.append((x["tarefa_id"], x["hipotese"]))
    for tid, x in (braco.get("resultados") or {}).items():
        if isinstance(x, dict) and x.get("aceita") and x.get("hipotese_bruta"):
            out.append((tid, x["hipotese_bruta"]))
    for x in braco.get("passos", []):
        if x.get("aceita") and x.get("hipotese_bruta"):
            out.append((x["tarefa"], x["hipotese_bruta"]))
    vistos, unicos = set(), []
    for par in out:                      # um registro pode ter a mesma hipótese em dois formatos
        if par not in vistos:
            vistos.add(par)
            unicos.append(par)
    return unicos


def verificar_execucao(pasta: str, ns_amostral: Sequence[int] = (5, 6, 7, 8, 9), k: int = 40,
                       exaustivo: bool = True) -> dict:
    with open(os.path.join(pasta, "deterministico.json"), encoding="utf-8") as f:
        d = json.load(f)
    if d.get("pacote"):                  # registro de benchmark externo: carrega (e confere) o pacote congelado
        from .benchmark_externo import RAIZ, carregar_pacote
        carregar_pacote(os.path.join(RAIZ, d["pacote"]["caminho"]), hash_esperado=d["pacote"]["hash"])
    semente = int(d.get("config", {}).get("semente", 10_002))
    tabela = BASES[d.get("config", {}).get("base", "E0")].para_aprendiz()
    res = {"execucao": pasta, "hipoteses": [], "parametros": {"ns_amostral": list(ns_amostral), "k": k,
                                                                 "particao": PARTICAO_NOVAS_DIMENSOES,
                                                                 "semente": semente}}
    for nome, b in d["bracos"].items():
        for tid, hip in hipoteses_aceitas(b):
            corpos = corpos_do_braco(b, tid)
            t = expandir_entradas(parse(hip), corpos)
            tarefa = tarefa_por_id(tid)
            item = {"braco": nome, "tarefa": tid, "hipotese": hip,
                    "entradas_expandidas": sorted(c for c in corpos if c in hip)}
            if exaustivo:
                item["exaustivo"] = verificar_exaustivo(t, tarefa, tabela=tabela)
            item["amostral"] = validar_amostral(t, tarefa, ns_amostral, k, semente, tabela=tabela)
            res["hipoteses"].append(item)
            print(nome, tid, "| exaustivo erros:", item.get("exaustivo", {}).get("erros"),
                  "| amostral:", {n: (r["natural"]["erros"], r.get("desenho", {}).get("erros"))
                                  for n, r in item["amostral"]["por_n"].items()}, flush=True)
    caminho = os.path.join(pasta, "verificacao.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Verificação exaustiva (n ≤ 4) e amostral (n = 5..9) das hipóteses aceitas")
    ap.add_argument("--run", required=True)
    ap.add_argument("--ns-amostral", default="5,6,7,8,9")
    ap.add_argument("--k", type=int, default=40)
    ap.add_argument("--sem-exaustivo", action="store_true")
    a = ap.parse_args(argv)
    ns = tuple(int(x) for x in a.ns_amostral.split(",") if x)
    verificar_execucao(a.run, ns, a.k, exaustivo=not a.sem_exaustivo)


if __name__ == "__main__":
    main()
