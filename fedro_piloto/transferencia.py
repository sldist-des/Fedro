"""Transferência estrutural (documento 06, missão 4): avalia as famílias CONGELADAS de
familias_transferencia com aprendizes que passaram pela cadeia do documento 05 (T1 vizPretos →
T2 expandir → T3 ParAdjacente) — a mesma exposição para L-lib+f e L-fix; só o mecanismo de
biblioteca difere. Depois da cadeia o aprendiz é FOTOGRAFADO (deepcopy) e cada tarefa da família é
tentada a partir da mesma fotografia, independentemente das outras (sem efeitos de ordem; a
biblioteca não recebe soluções das tarefas de avaliação). Nenhuma solução manual entra na biblioteca.

Medidas por tarefa e braço: aceita, custo (livro), reutilizações de entradas da biblioteca,
hipótese; por família: razão de custo L-lib+f / L-fix (F-neg: transferência negativa se > 1 ou se
L-lib+f falha onde L-fix aceita). O hash da especificação da família é registado em cada execução
e conferido contra familias_transferencia.HASH_CONGELADO.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import time
from typing import Dict, List, Optional, Sequence

from . import aprendizes as A
from . import familias_transferencia as F
from .experimento_minimo import TAREFAS as TAREFAS_EM, CURRICULO, ConfigEM, _aprendiz
from .razao import LivroRazao

CADEIA = CURRICULO[:3]      # vizPretos, expandir, ParAdjacente


def job_braco(aprendiz_nome: str, cfg: ConfigEM, tarefas: Sequence[str], cadeia: Sequence[str] = CADEIA) -> dict:
    from .medidas import medir_isolado
    from .piloto import limitar_memoria
    limitar_memoria(cfg.memoria_trabalhador_gb)
    amb = A.Ambiente(cfg.semente, num_teste=cfg.num_teste)
    rotulo = f"{cfg.politica_busca}/{aprendiz_nome}"
    livro = LivroRazao(cfg.semente, {"braco": rotulo, "experimento": "transferencia"})
    ap = _aprendiz(aprendiz_nome, cfg, livro, rotulo=f"{cfg.base}/{rotulo}")
    t0 = time.process_time()
    with medir_isolado(rotulo) as m:
        cadeia_res = []
        for tid in cadeia:
            r = ap.resolver(TAREFAS_EM[tid], amb)
            cadeia_res.append({"tarefa": tid, "aceita": r.aceita, "motivo": r.motivo_fim, "hipotese": r.hipotese_legivel,
                               "custo": livro.entrada(tid, ap.aprendiz_id).total_aprendiz(),
                               "biblioteca_usada": list(r.constantes_biblioteca_usadas)})
        foto = ap                       # fotografia: cada tarefa parte de uma cópia profunda
        abstracoes = A.abstracoes(ap)
        custo_cadeia = sum(c["custo"] for c in cadeia_res)
        resultados = {}
        for tid in tarefas:
            apt = copy.deepcopy(foto)
            tarefa = F.TAREFAS[tid]
            r = apt.resolver(tarefa, amb)
            e = apt.livro.entrada(tid, apt.aprendiz_id)
            resultados[tid] = {"familia": tarefa.escada, "aceita": r.aceita, "motivo": r.motivo_fim, "rodadas": r.rodadas,
                               "hipotese": r.hipotese_legivel, "hipotese_bruta": r.hipotese, "tamanho": r.tamanho,
                               "custo": e.total_aprendiz(), "enumeracao_candidatos": e.enumeracao_candidatos,
                               "biblioteca_usada": list(r.constantes_biblioteca_usadas),
                               "reutilizacoes": dict(r.reutilizacoes), "acuracia_teste": r.acuracia_teste,
                               "teste_resumo": r.teste_resumo, "contador_busca": r.contador_busca,
                               "tamanho_max_carregado": r.contador_busca.get("tamanho_max_carregado", 0),
                               "inconclusivo_recurso": r.inconclusivo_recurso,
                               "custos_folha": r.custos_folha}
    det = {"braco": rotulo, "aprendiz": aprendiz_nome, "politica": cfg.politica_busca, "cadeia": cadeia_res,
           "custo_cadeia": custo_cadeia, "abstracoes": abstracoes, "resultados": resultados,
           "livro_cadeia": livro.como_dict(incluir_diario=False)}
    med = {"tempo_parede_s": m.tempo_parede_s, "cpu_s": time.process_time() - t0,
           "memoria_pico_kib": m.memoria_pico_kib, "memoria_escopo": m.memoria_escopo}
    return {"deterministico": det, "medicoes": med}


def analisar(bracos: Dict[str, dict]) -> dict:
    """Por política: razão de custo e transferência por tarefa; resumo por família."""
    out = {}
    pols = sorted({v["deterministico"]["politica"] for v in bracos.values()})
    for pol in pols:
        lib = next((v["deterministico"] for v in bracos.values() if v["deterministico"]["politica"] == pol and v["deterministico"]["aprendiz"] == "L-lib+f"), None)
        fix = next((v["deterministico"] for v in bracos.values() if v["deterministico"]["politica"] == pol and v["deterministico"]["aprendiz"] == "L-fix"), None)
        if not lib or not fix:
            continue
        por_tarefa = {}
        for tid in F.ORDEM:
            a, b = lib["resultados"].get(tid), fix["resultados"].get(tid)
            if not a or not b:
                continue
            razao = (a["custo"] / b["custo"]) if b["custo"] else None
            if a["aceita"] and b["aceita"]:
                veredito = "positiva" if a["custo"] < b["custo"] else ("neutra" if a["custo"] == b["custo"] else "negativa")
            elif a["aceita"] and not b["aceita"]:
                veredito = "positiva (só L-lib+f aceita)"
            elif b["aceita"] and not a["aceita"]:
                veredito = "negativa (só L-fix aceita)"
            else:
                veredito = "inconclusiva (nenhum aceita)"
            por_tarefa[tid] = {"familia": F.TAREFAS[tid].escada, "L-lib+f": {"aceita": a["aceita"], "custo": a["custo"], "reuso": a["biblioteca_usada"], "tamanho": a["tamanho"]},
                               "L-fix": {"aceita": b["aceita"], "custo": b["custo"], "tamanho": b["tamanho"]},
                               "razao_custo": razao, "transferencia": veredito,
                               "reuso_em_L-lib+f": bool(a["biblioteca_usada"])}
        def fam(nome):
            ts = [t for t in por_tarefa if por_tarefa[t]["familia"] == nome]
            return {"tarefas": len(ts),
                    "aceitas_L-lib+f": sum(por_tarefa[t]["L-lib+f"]["aceita"] for t in ts),
                    "aceitas_L-fix": sum(por_tarefa[t]["L-fix"]["aceita"] for t in ts),
                    "com_reuso": sum(por_tarefa[t]["reuso_em_L-lib+f"] for t in ts),
                    "positivas": sum(por_tarefa[t]["transferencia"].startswith("positiva") for t in ts),
                    "negativas": sum(por_tarefa[t]["transferencia"].startswith("negativa") for t in ts),
                    "custo_L-lib+f": sum(por_tarefa[t]["L-lib+f"]["custo"] for t in ts),
                    "custo_L-fix": sum(por_tarefa[t]["L-fix"]["custo"] for t in ts)}
        out[pol] = {"por_tarefa": por_tarefa, "F-comp": fam("F-comp"), "F-neg": fam("F-neg"),
                    "custo_cadeia": {"L-lib+f": lib["custo_cadeia"], "L-fix": fix["custo_cadeia"]},
                    "abstracoes_L-lib+f": lib["abstracoes"]}
    return out


def executar(pasta: str, cfg_base: ConfigEM, politicas: Sequence[str], aprendizes: Sequence[str] = ("L-lib+f", "L-fix"),
             tarefas: Sequence[str] = F.ORDEM, processos: int = 4) -> dict:
    from .piloto import _executar_jobs, hash_fontes
    if F.hash_especificacao() != F.HASH_CONGELADO:
        raise RuntimeError("especificação das famílias difere do hash congelado; não executar")
    os.makedirs(pasta, exist_ok=True)
    jobs, nomes = [], []
    for pol in politicas:
        cfg = copy.replace(cfg_base, politica_busca=pol) if hasattr(copy, "replace") else _replace(cfg_base, pol)
        for apn in aprendizes:
            jobs.append((job_braco, (apn, cfg, list(tarefas))))
            nomes.append(f"{pol}/{apn}")
    t0 = time.time()
    res = _executar_jobs(jobs, processos)
    bracos = dict(zip(nomes, res))
    det = {"config": cfg_base.como_dict(), "politicas": list(politicas), "tarefas": list(tarefas),
           "hash_familias": F.hash_especificacao(), "hash_congelado": F.HASH_CONGELADO, "fontes": hash_fontes(),
           "bracos": {k: v["deterministico"] for k, v in bracos.items()}, "analise": analisar(bracos)}
    med = {"parede_total_s": time.time() - t0, "bracos": {k: v["medicoes"] for k, v in bracos.items()}}
    with open(os.path.join(pasta, "deterministico.json"), "w", encoding="utf-8") as f:
        json.dump(det, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "medicoes.json"), "w", encoding="utf-8") as f:
        json.dump(med, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "relatorio.md"), "w", encoding="utf-8") as f:
        f.write(relatorio_md(det, med))
    return {"deterministico": det, "medicoes": med}


def _replace(cfg: ConfigEM, pol: str) -> ConfigEM:
    import dataclasses
    return dataclasses.replace(cfg, politica_busca=pol)


def relatorio_md(det, med) -> str:
    L = [f"# Transferência estrutural — famílias congeladas (hash {det['hash_familias'][:16]}…), semente {det['config']['semente']}, B = {det['config']['B']}", ""]
    for pol, an in det["analise"].items():
        L.append(f"## Política {pol}")
        L.append(f"Custo da cadeia T1–T3: L-lib+f {an['custo_cadeia']['L-lib+f']:,}; L-fix {an['custo_cadeia']['L-fix']:,}. Abstrações de L-lib+f: {[(a.get('nome'), a.get('legivel') or a.get('corpo')) for a in an['abstracoes_L-lib+f']]}")
        L.append("")
        L.append("| tarefa | família | L-lib+f aceita | custo | tamanho | reuso | L-fix aceita | custo | tamanho | razão custo | transferência |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for t, r in an["por_tarefa"].items():
            a, b = r["L-lib+f"], r["L-fix"]
            rz = f"{r['razao_custo']:.2f}" if r["razao_custo"] is not None else "—"
            L.append(f"| {t} | {r['familia']} | {a['aceita']} | {a['custo']:,} | {a['tamanho']} | {a['reuso']} | {b['aceita']} | {b['custo']:,} | {b['tamanho']} | {rz} | {r['transferencia']} |")
        L.append("")
        for fam in ("F-comp", "F-neg"):
            L.append(f"- {fam}: {json.dumps(an[fam], ensure_ascii=False)}")
        L.append("")
    for k, v in det["bracos"].items():
        L.append(f"### Hipóteses — {k}")
        for t, r in v["resultados"].items():
            L.append(f"- {t}: aceita={r['aceita']} ({r['motivo']}), `{r['hipotese'] or ''}`, custo {r['custo']:,}, reuso {r['biblioteca_usada']}")
        L.append("")
    L.append("## Medições")
    for k, m in med["bracos"].items():
        L.append(f"- {k}: parede {m['tempo_parede_s']:.0f} s, CPU {m['cpu_s']:.0f} s, memória {m['memoria_pico_kib']} KiB ({m['memoria_escopo']})")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--semente", type=int, default=10_002)
    ap.add_argument("--B", type=int, default=20_000)
    ap.add_argument("--politicas", default="tamanho,unigrama")
    ap.add_argument("--aprendizes", default="L-lib+f,L-fix")
    ap.add_argument("--tarefas", default=",".join(F.ORDEM))
    ap.add_argument("--processos", type=int, default=4)
    a = ap.parse_args(argv)
    cfg = ConfigEM(semente=a.semente, B=a.B, processos=a.processos, sondas=False, auditoria_oe_orcamento=0)
    r = executar(os.path.join("runs", a.id), cfg, a.politicas.split(","), a.aprendizes.split(","), a.tarefas.split(","), a.processos)
    print(json.dumps({p: {f: v[f] for f in ("F-comp", "F-neg")} for p, v in r["deterministico"]["analise"].items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
