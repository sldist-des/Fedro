#!/usr/bin/env python3
"""Tabelas em Markdown para o relatório do benchmark cego (docs/08) a partir dos registros runs/bx-*.

Uso: python3 analysis/relatorio_bx.py runs/bx-<id> [runs/bx-<id> ...]
Gera, por registro: tabela por braço, tabela tarefa a tarefa (L-lib+f vs L-fix por política), lesão,
custo cumulativo igual, verificação (se verificacao.json existir) e, para registros de ordens, o resumo.
Só lê os registros; não recalcula nada do protocolo."""
import json
import os
import sys


def M(x):
    return f"{x / 1e6:.1f} M" if isinstance(x, (int, float)) else "—"


def por_braco(det):
    L = ["| braço | aceitas | custo prévio | custo benchmark | custo cumulativo | custo por aceita | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha | inválidas |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for k, m in det["metricas"]["por_braco"].items():
        if "falha" in m:
            L.append(f"| {k} | FALHA: {m['falha']} | | | | | | | | |")
            continue
        L.append(f"| {k} | {m['aceitas']}/{m['tarefas_validas']} | {M(m['custo_previo'])} | {M(m['custo_benchmark'])} | {M(m['custo_cumulativo'])} | {M(m['custo_por_aceita'])} | {m['tarefas_com_reuso']} | {m['entradas_descobertas']} ({m['entradas_reutilizadas']}) | {m['livro_fecha']} | {len(m['invalidas_no_ambiente'])} |")
    return "\n".join(L)


def por_tarefa(det, ordem_tarefas):
    comps = {k: v for k, v in det["metricas"]["comparacoes"].items() if "por_tarefa" in v}
    pols = sorted({k.split("/")[1] for k in comps})
    L = ["| tarefa | " + " | ".join(f"{p}: L-lib+f | L-fix | classe" for p in pols) + " |",
         "|---|" + "---|" * (3 * len(pols))]
    for t in ordem_tarefas:
        celulas = []
        for p in pols:
            c = next((v for k, v in comps.items() if f"/{p}/" in k), None)
            v = c["por_tarefa"].get(t) if c else None
            if not v:
                celulas += ["—", "—", "—"]
                continue
            a, b = v["L-lib+f"], v["L-fix"]
            fa = ("✔" if a["aceita"] else "✘") + f" {M(a['custo'])}" + (f" ({a['tamanho']})" if a["tamanho"] else "") + (f" reuso {','.join(a['reuso'])}" if a["reuso"] else "")
            fb = ("✔" if b["aceita"] else "✘") + f" {M(b['custo'])}" + (f" ({b['tamanho']})" if b["tamanho"] else "")
            cl = v["classe"].split(" (")[0]
            if v.get("razao_exata") is not None:
                cl += f" ×{v['razao_exata']:.2f}"
            elif v.get("razao_minima") is not None:
                cl += f" ≥×{v['razao_minima']:.1f}"
            celulas += [fa, fb, cl]
        L.append(f"| {t} | " + " | ".join(celulas) + " |")
    return "\n".join(L)


def resumo_comparacoes(det):
    L = ["| comparação | positivas | negativas | neutras | inconclusivas | com reuso |", "|---|---|---|---|---|---|"]
    for k, v in det["metricas"]["comparacoes"].items():
        if "por_tarefa" in v:
            L.append(f"| {k} | {v['positivas']} | {v['negativas']} | {v['neutras']} | {v['inconclusivas']} | {v['com_reuso']} |")
    L += ["", "| lesão | tarefas após a lesão | aceitas L-lib+f | aceitas lesão | custo L-lib+f | custo lesão | entradas removidas | sensível |", "|---|---|---|---|---|---|---|---|"]
    for k, v in det["metricas"]["comparacoes"].items():
        if "tarefas_apos_lesao" in v:
            L.append(f"| {k} | {v['tarefas_apos_lesao']} | {v['aceitas_L-lib+f']} | {v['aceitas_lesao']} | {M(v['custo_L-lib+f'])} | {M(v['custo_lesao'])} | {v['entradas_removidas']} | {v['sensivel']} |")
    return "\n".join(L)


def custo_igual(det):
    L = []
    for k, v in det["metricas"]["comparacoes"].items():
        if "aceitas_a_custo_cumulativo_igual" in v:
            xs = v["aceitas_a_custo_cumulativo_igual"]
            fim = xs[-1] if xs else None
            L.append(f"- {k}: " + ("; ".join(f"{x['tarefa']} C={M(x['custo_cumulativo'])} → {x['aceitas_L-lib+f']} vs {x['aceitas_L-fix_ao_mesmo_custo']}" for x in xs) if xs else "—"))
    return "\n".join(L)


def verificacao(pasta):
    cam = os.path.join(pasta, "verificacao.json")
    if not os.path.exists(cam):
        return "(verificação ainda não executada)"
    v = json.load(open(cam, encoding="utf-8"))
    ex = sum(h["exaustivo"]["entradas"] for h in v["hipoteses"] if "exaustivo" in h)
    exe = sum(h["exaustivo"]["erros"] for h in v["hipoteses"] if "exaustivo" in h)
    am = sum(rn["natural"]["n"] for h in v["hipoteses"] for rn in h["amostral"]["por_n"].values())
    ame = sum(rn["natural"]["erros"] for h in v["hipoteses"] for rn in h["amostral"]["por_n"].values())
    des = sum(rn["desenho"]["n"] for h in v["hipoteses"] for rn in h["amostral"]["por_n"].values() if rn.get("desenho"))
    dese = sum(rn["desenho"]["erros"] for h in v["hipoteses"] for rn in h["amostral"]["por_n"].values() if rn.get("desenho"))
    oc = v.get("testes_ocultos_autor", [])
    ocn, oce = sum(o["n"] for o in oc), sum(o["erros"] for o in oc)
    degen = sum(1 for h in v["hipoteses"] for rn in h["amostral"]["por_n"].values() if rn["natural"].get("degenerado"))
    L = [f"| hipóteses aceitas verificadas | exaustivo n ≤ 4 (entradas / erros) | amostral n = 5..9 teste_ext (entradas / erros) | desenho (entradas / erros) | testes ocultos do autor (entradas / erros) | conjuntos amostrais degenerados |",
         "|---|---|---|---|---|---|",
         f"| {len(v['hipoteses'])} | {ex:,} / {exe} | {am:,} / {ame} | {des:,} / {dese} | {ocn:,} / {oce} | {degen} |"]
    maus = [(h["braco"], h["tarefa"]) for h in v["hipoteses"] if h.get("exaustivo", {}).get("erros", 0) or any(rn["natural"]["erros"] for rn in h["amostral"]["por_n"].values())]
    if maus or oce:
        L.append("")
        L.append("Hipóteses com erro de previsão: " + ", ".join(f"{b}/{t}" for b, t in maus) + (f"; ocultos do autor com erro: {[(o['braco'], o['tarefa'], o['erros']) for o in oc if o['erros']]}" if oce else ""))
    if v.get("testemunhas"):
        L.append("")
        L.append("Testemunhas do autor (tamanho em E0 pela nossa contagem; tipo; erros em n ≤ 3): " + "; ".join(
            f"{t}: {x.get('tamanho', '?')}{'' if x.get('tipo_ok', True) else ' TIPO≠'}{'' if not x.get('erros_n_le_3') else f' ERROS={x[chr(101)+chr(114)+chr(114)+chr(111)+chr(115)+chr(95)+chr(110)+chr(95)+chr(108)+chr(101)+chr(95)+chr(51)]}'}{(' ' + x['erro']) if 'erro' in x else ''}" for t, x in sorted(v["testemunhas"].items())))
    return "\n".join(L)


def principal(pasta):
    det = json.load(open(os.path.join(pasta, "deterministico.json"), encoding="utf-8"))
    med = json.load(open(os.path.join(pasta, "medicoes.json"), encoding="utf-8"))
    out = [f"### Registro `{os.path.basename(pasta)}`", ""]
    if "resumo" in det and "G" in det:
        out += ["| braço | aceitas | ordem de aceitação | passos | custo total | gasto global | cadeia de reuso |", "|---|---|---|---|---|---|---|"]
        for k, v in det["resumo"].items():
            out.append(f"| {k} | {len(v['aceitas'])}: {', '.join(v['aceitas'])} | {' → '.join(v['ordem'])} | {v['passos']} | {M(v['custo_total'])} | {v['gasto_global']:,} | {v['cadeia_reuso']} |")
        out += ["", f"Parede total: {med['parede_total_s']:.0f} s."]
        return "\n".join(out)
    ordem = [t["id"] for t in det["pacote"]["tarefas"]]
    out += [f"Pacote {det['pacote']['nome']} v{det['pacote']['versao']}, hash `{det['pacote']['hash'][:16]}…`; semente {det['config']['semente']}; B = {det['config']['B']}; modos {det['modos']}; k_reservatorio = {det['k_reservatorio']}; parede total {med['parede_total_s']:.0f} s.", ""]
    out += [por_braco(det), "", resumo_comparacoes(det), "", "Tarefas aceitas a custo cumulativo igual (para cada aceitação de L-lib+f ao custo C, aceitas de L-lib+f vs de L-fix com custo ≤ C):", custo_igual(det), ""]
    out += ["Tarefa a tarefa (✔ aceita / ✘ não; custo em passos; tamanho da hipótese entre parênteses; classe de transferência com razão exata ×, ou limite inferior ≥× quando L-fix não aceita):", "", por_tarefa(det, ordem), ""]
    out += ["Verificação pós-execução:", "", verificacao(pasta)]
    return "\n".join(out)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(principal(p))
        print()
