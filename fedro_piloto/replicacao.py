"""Replicação do experimento mínimo com sementes novas (documento 06, missão 2).

Cruza políticas de busca {tamanho, unigrama} com os braços {L-fix, L-lib, L-lib+f, L-lib+f/lesao,
L-lib+f/controle}, sem sondas (que não preservam o histórico) e sem a auditoria OE (igual entre
sementes para a tabela base). Só sementes do intervalo exploratório ainda não usadas; nunca os baldes
reservados ao confirmatório (garantido pelos geradores). Agrega por (política, braço): tarefas aceitas,
custo cumulativo até T3 e final, reutilizações, falhas; mínimo, mediana e máximo entre sementes.
Uso: python3 -m fedro_piloto.replicacao --id rep-1 --sementes 10003,10004,10005,10006 --politicas tamanho,unigrama
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from typing import Dict, List

from . import experimento_minimo as EM
from . import geradores as G

SEMENTES_USADAS_ANTES = (10_001, 10_002)   # piloto (documento 04) e experimento mínimo (documento 05)


def executar(pasta: str, sementes: List[int], politicas: List[str], B: int = 20_000, processos: int = 4,
             bracos=EM.BRACOS) -> dict:
    os.makedirs(pasta, exist_ok=True)
    t0 = time.time()
    execucoes = []
    verificar_sementes(sementes)
    for sem in sementes:
        for pol in politicas:
            cfg = EM.ConfigEM(semente=sem, B=B, politica_busca=pol, bracos=tuple(bracos), sondas=False,
                              processos=processos, auditoria_oe_orcamento=0)
            sub = os.path.join(pasta, f"s{sem}-{pol}")
            r = EM.executar(cfg, sub)
            execucoes.append({"semente": sem, "politica": pol, "pasta": sub,
                              "analise": r["deterministico"]["analise"],
                              "bracos": {k: _resumo_braco(v) for k, v in r["deterministico"]["bracos"].items()},
                              "parede_s": r["medicoes"]["tempo_parede_total_s"]})
            print(f"[replicacao] semente {sem} política {pol}: veredito {r['deterministico']['analise']['criterio_central'].get('veredito')}", flush=True)
    agg = agregar(execucoes)
    out = {"sementes": sementes, "politicas": politicas, "B": B, "execucoes": execucoes, "agregado": agg,
           "parede_total_s": time.time() - t0}
    with open(os.path.join(pasta, "resumo.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "resumo.md"), "w", encoding="utf-8") as f:
        f.write(resumo_md(out))
    return out


def verificar_sementes(sementes) -> None:
    """Só sementes do intervalo exploratório (geradores.SEMENTES_PILOTO) e nunca usadas antes."""
    for sem in sementes:
        if sem in SEMENTES_USADAS_ANTES:
            raise ValueError(f"semente {sem} já usada em experimentos anteriores")
        if sem not in G.SEMENTES_PILOTO:
            raise ValueError(f"semente {sem} fora do intervalo exploratório {G.SEMENTES_PILOTO}")


def _resumo_braco(det: dict) -> dict:
    curva = det["curva"]
    aceitas = [x["tarefa"] for x in curva if x["aceita"]]
    ate_t3 = next((x["cumulativo"] for x in curva if x["tarefa"] == "ParAdjacente"), None)
    reut = [(a["nome"], a["reutilizacoes"], a.get("reutilizacoes_indiretas")) for a in det["abstracoes"]
            if a.get("reutilizacoes") or a.get("reutilizacoes_indiretas")]
    return {"aceitas": aceitas, "num_aceitas": len(aceitas), "cumulativo_ate_T3": ate_t3,
            "cumulativo_final": curva[-1]["cumulativo"] if curva else None,
            "enumeracao_final": curva[-1]["cumulativo_enumeracao"] if curva else None,
            "abstracoes": len(det["abstracoes"]), "reutilizadas": reut, "falha": det.get("falha"),
            "hipoteses": {x["tarefa"]: x["hipotese"] for x in curva if x["aceita"]}}


def _stats(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    return {"min": min(xs), "mediana": statistics.median(xs), "max": max(xs), "n": len(xs)}


def agregar(execucoes: List[dict]) -> dict:
    agg: Dict[str, dict] = {}
    for pol in sorted({e["politica"] for e in execucoes}):
        for braco in sorted({b for e in execucoes for b in e["bracos"]}):
            rs = [e["bracos"][braco] for e in execucoes if e["politica"] == pol and braco in e["bracos"]]
            if not rs:
                continue
            agg[f"{pol}|{braco}"] = {
                "sementes": len(rs),
                "tarefas_aceitas": _stats([r["num_aceitas"] for r in rs]),
                "aceitas_por_tarefa": {t: sum(1 for r in rs if t in r["aceitas"]) for t in EM.CURRICULO + EM.CURRICULO_CONTROLE[:2]},
                "cumulativo_ate_T3": _stats([r["cumulativo_ate_T3"] for r in rs]),
                "cumulativo_final": _stats([r["cumulativo_final"] for r in rs]),
                "com_reutilizacao": sum(1 for r in rs if r["reutilizadas"]),
                "falhas": sum(1 for r in rs if r["falha"]),
                "hipoteses_distintas_por_tarefa": {t: sorted({r["hipoteses"][t] for r in rs if t in r["hipoteses"]})
                                                   for t in EM.CURRICULO + EM.CURRICULO_CONTROLE[:2]},
            }
    vered = {pol: [e["analise"]["criterio_central"].get("veredito") for e in execucoes if e["politica"] == pol]
             for pol in sorted({e["politica"] for e in execucoes})}
    return {"por_politica_braco": agg, "veredito_por_politica": vered}


def resumo_md(out: dict) -> str:
    L = [f"# Replicação — sementes {out['sementes']}, políticas {out['politicas']}, B = {out['B']}", ""]
    L.append("| política \\| braço | sementes | tarefas aceitas (min/med/max) | aceitas por tarefa | cumul. até T3 (min/med/max) | com reutilização | falhas |")
    L.append("|---|---|---|---|---|---|---|")
    for k, v in out["agregado"]["por_politica_braco"].items():
        ta, c3 = v["tarefas_aceitas"], v["cumulativo_ate_T3"]
        L.append(f"| {k} | {v['sementes']} | {ta['min']}/{ta['mediana']}/{ta['max']} | {v['aceitas_por_tarefa']} | "
                 f"{'' if not c3 else f'{c3['min']:,}/{int(c3['mediana']):,}/{c3['max']:,}'} | {v['com_reutilizacao']} | {v['falhas']} |")
    L.append("")
    L.append("Vereditos (critério central de cinco condições) por política: " + json.dumps(out["agregado"]["veredito_por_politica"]))
    L.append("")
    L.append("## Hipóteses aceitas distintas por tarefa")
    for k, v in out["agregado"]["por_politica_braco"].items():
        for t, hs in v["hipoteses_distintas_por_tarefa"].items():
            if hs:
                L.append(f"- {k} / {t}: " + "; ".join(f"`{h}`" for h in hs))
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--sementes", default="10003,10004,10005,10006")
    ap.add_argument("--politicas", default="tamanho,unigrama")
    ap.add_argument("--B", type=int, default=20_000)
    ap.add_argument("--processos", type=int, default=4)
    a = ap.parse_args(argv)
    executar(os.path.join("runs", a.id), [int(x) for x in a.sementes.split(",")], a.politicas.split(","), a.B, a.processos)


if __name__ == "__main__":
    main()
