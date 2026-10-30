"""Currículo autodirigido (documento 06, missão 3).

O ambiente disponibiliza um CONJUNTO de tarefas sem ordem. Um seletor escolhe a próxima tarefa usando
APENAS informação legitimamente disponível ao aprendiz: histórico de tentativas (quantas, com que
orçamento, aceita ou não, custo), a versão da biblioteca na última tentativa, e o maior tamanho
carregado na busca. O seletor NUNCA recebe soluções de referência, tamanhos mínimos de programas,
definições dos conceitos nem os objetos Tarefa (só o id, o tipo e o histórico). Isto é imposto pela
interface: `escolher(historicos, versao_biblioteca, rng)` recebe objetos HistoricoTarefa.

Seletores:
  manual        a ordem prescrita do documento 05 (T1 T2 T3 T4 U1 U2), uma passagem com B_max, repetindo
                uma tarefa só se a biblioteca mudou desde a sua última tentativa;
  aleatorio     ordem uniforme ao acaso entre as elegíveis (semente própria do seletor), mesma regra;
  autodirigido  aprofundamento iterativo com progresso: cada tarefa tem um orçamento próximo (começa em
                b0 e dobra a cada falha sem mudança de biblioteca; se a biblioteca mudou desde a última
                tentativa, repete-se o mesmo orçamento primeiro — "progresso de aprendizagem" = a tarefa
                pode ter ficado mais barata). Escolhe a tarefa de menor orçamento próximo; empate: a que
                tem biblioteca nova desde a última tentativa, depois menos tentativas, depois id.
Todos os braços têm o MESMO orçamento global G (candidatos de enumeração acumulados) e o mesmo limite
por tentativa B_max; o custo das sondas do seletor autodirigido conta.
Pergunta: a cadeia vizPretos → expandir → ParAdjacente aparece sem ser prescrita?
"""
from __future__ import annotations

import argparse
import json
import os
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from . import aprendizes as A
from . import geradores as G
from .dsl import BASES, tipo_str
from .experimento_minimo import TAREFAS, _aprendiz, ConfigEM
from .razao import LivroRazao

POOL = ["vizPretos", "expandir", "ParAdjacente", "NenhumaIsolada", "pretasColuna1", "semLinha1"]
ORDEM_MANUAL = list(POOL)


@dataclass
class HistoricoTarefa:
    """O que o seletor pode ver sobre uma tarefa. Nada de referências, tamanhos mínimos ou conceitos."""
    id: str
    tipo: str
    tentativas: int = 0
    aceita: bool = False
    custo_total: int = 0
    enumeracao_total: int = 0
    ultimo_B: int = 0
    ultimo_motivo: str = ""
    ultimo_tamanho_max: int = 0
    versao_bib_ultima: int = -1
    orcamento_proximo: int = 0
    exemplos_finais: int = 0


class Seletor:
    nome = "base"

    @staticmethod
    def elegiveis(hist: List[HistoricoTarefa], versao_bib: int) -> List[HistoricoTarefa]:
        """Pendentes nunca tentadas, ou tentadas antes da última mudança de biblioteca (progresso)."""
        return [h for h in hist if not h.aceita and (h.tentativas == 0 or h.versao_bib_ultima < versao_bib)]

    def escolher(self, hist: List[HistoricoTarefa], versao_bib: int, rng: random.Random, B_max: int) -> Optional[tuple]:
        """Devolve (id, B) ou None quando não há mais nada a tentar."""
        raise NotImplementedError

    def apos(self, h: HistoricoTarefa, versao_bib: int) -> None:
        pass


class SeletorManual(Seletor):
    """Ordem prescrita (documento 05), uma passagem com B_max; repete uma tarefa só se a biblioteca
    mudou desde a sua última tentativa."""
    nome = "manual"

    def __init__(self, ordem: Sequence[str]):
        self.ordem = list(ordem)

    def escolher(self, hist, versao_bib, rng, B_max):
        el = self.elegiveis(hist, versao_bib)
        if not el:
            return None
        el.sort(key=lambda h: self.ordem.index(h.id))
        return el[0].id, B_max


class SeletorAleatorio(Seletor):
    """Ordem uniforme ao acaso entre as elegíveis (semente própria do seletor), com B_max."""
    nome = "aleatorio"

    def escolher(self, hist, versao_bib, rng, B_max):
        el = self.elegiveis(hist, versao_bib)
        if not el:
            return None
        return rng.choice(sorted(el, key=lambda h: h.id)).id, B_max


class SeletorAutodirigido(Seletor):
    """Aprofundamento iterativo com progresso de aprendizagem.

    Cada tarefa pendente tem um orçamento próximo (b0 na primeira tentativa; dobra após cada falha).
    Se a biblioteca mudou desde a última tentativa da tarefa (versao_bib_ultima < versao atual), a
    tarefa pode ter ficado mais barata: oferece-se UMA repetição com o MESMO orçamento da última
    tentativa (uma por mudança de biblioteca, porque versao_bib_ultima é actualizada na tentativa).
    Escolhe a tarefa de menor orçamento efetivo; empate: repetição com biblioteca nova primeiro,
    depois menos tentativas, depois id. Só usa o histórico: nunca referências nem definições dos alvos."""
    nome = "autodirigido"

    def __init__(self, b0: int = 2_000):
        self.b0 = b0

    def orcamento_efetivo(self, h: HistoricoTarefa, versao_bib: int) -> int:
        if h.tentativas == 0:
            return self.b0
        if h.versao_bib_ultima < versao_bib:
            return h.ultimo_B
        return h.orcamento_proximo

    def escolher(self, hist, versao_bib, rng, B_max):
        pend = [h for h in hist if not h.aceita]
        cand = [(self.orcamento_efetivo(h, versao_bib), 0 if (h.tentativas and h.versao_bib_ultima < versao_bib) else 1,
                 h.tentativas, h.id, h) for h in pend]
        cand = [c for c in cand if c[0] <= B_max]
        if not cand:
            return None
        cand.sort(key=lambda c: c[:4])
        return cand[0][4].id, cand[0][0]

    def apos(self, h: HistoricoTarefa, versao_bib: int) -> None:
        if not h.aceita:
            h.orcamento_proximo = h.ultimo_B * 2


SELETORES = {"manual": lambda rng: SeletorManual(ORDEM_MANUAL), "aleatorio": lambda rng: SeletorAleatorio(),
             "autodirigido": lambda rng: SeletorAutodirigido()}


def _versao_biblioteca(ap) -> int:
    return len(ap.biblioteca.entradas) if isinstance(ap, A.LLib) else 0


def job_braco(seletor_nome: str, aprendiz_nome: str, cfg: ConfigEM, G_total: int, B_max: int,
              semente_seletor: int, pool: Sequence[str] = POOL) -> dict:
    from .medidas import medir_isolado
    from .piloto import limitar_memoria
    limitar_memoria(cfg.memoria_trabalhador_gb)
    amb = A.Ambiente(cfg.semente, num_teste=cfg.num_teste)
    rotulo = f"{seletor_nome}/{aprendiz_nome}"
    livro = LivroRazao(cfg.semente, {"braco": rotulo, "experimento": "curriculo-autodirigido"})
    ap = _aprendiz(aprendiz_nome, cfg, livro, rotulo=f"{cfg.base}/{rotulo}")
    rng = G.rng_derivado(semente_seletor, "curriculo", seletor_nome)
    sel = SELETORES[seletor_nome](rng)
    hist = {tid: HistoricoTarefa(tid, tipo_str(TAREFAS[tid].tipo)) for tid in pool}
    passos: List[dict] = []
    gasto = 0
    versao = _versao_biblioteca(ap)
    t0 = time.process_time()
    with medir_isolado(rotulo) as m:
        while gasto < G_total:
            esc = sel.escolher(list(hist.values()), versao, rng, B_max)
            if esc is None:
                break
            tid, B = esc
            B = min(B, G_total - gasto)
            if B <= 0:
                break
            h = hist[tid]
            ap.B = int(B)
            antes = livro.entrada(tid, ap.aprendiz_id).total_aprendiz()
            antes_e = livro.entrada(tid, ap.aprendiz_id).enumeracao_candidatos
            r = ap.resolver(TAREFAS[tid], amb)
            e = livro.entrada(tid, ap.aprendiz_id)
            custo = e.total_aprendiz() - antes
            enum = e.enumeracao_candidatos - antes_e
            gasto += max(enum, 1)
            h.tentativas += 1
            h.aceita = r.aceita
            h.custo_total += custo
            h.enumeracao_total += enum
            h.ultimo_B = int(B)
            h.ultimo_motivo = r.motivo_fim
            h.ultimo_tamanho_max = r.contador_busca.get("tamanho_max_carregado", 0)
            h.exemplos_finais = r.exemplos_finais
            versao = _versao_biblioteca(ap)
            sel.apos(h, versao)
            h.versao_bib_ultima = versao
            passos.append({"passo": len(passos) + 1, "tarefa": tid, "B": int(B), "aceita": r.aceita,
                           "motivo": r.motivo_fim, "custo": custo, "enumeracao": enum, "gasto_global": gasto,
                           "versao_biblioteca": versao, "hipotese": r.hipotese_legivel,
                           "biblioteca_usada": list(r.constantes_biblioteca_usadas),
                           "reutilizacoes": dict(r.reutilizacoes), "tamanho_max": h.ultimo_tamanho_max})
    det = {"braco": rotulo, "seletor": seletor_nome, "aprendiz": aprendiz_nome, "G": G_total, "B_max": B_max,
           "passos": passos, "historico": {k: v.__dict__ for k, v in hist.items()},
           "ordem_aceitacao": [p["tarefa"] for p in passos if p["aceita"]],
           "aceitas": sorted(k for k, v in hist.items() if v.aceita), "gasto_global": gasto,
           "custo_total": sum(p["custo"] for p in passos),
           "abstracoes": A.abstracoes(ap), "livro": livro.como_dict(incluir_diario=False),
           "cadeia_reuso": [(p["tarefa"], p["biblioteca_usada"]) for p in passos if p["aceita"] and p["biblioteca_usada"]]}
    med = {"tempo_parede_s": m.tempo_parede_s, "cpu_s": time.process_time() - t0,
           "memoria_pico_kib": m.memoria_pico_kib, "memoria_escopo": m.memoria_escopo}
    return {"deterministico": det, "medicoes": med}


def executar(pasta: str, cfg: ConfigEM, G_total: int, B_max: int, seletores: Sequence[str],
             aprendizes: Sequence[str], sementes_aleatorio: Sequence[int], processos: int = 4) -> dict:
    from .piloto import _executar_jobs, hash_fontes
    os.makedirs(pasta, exist_ok=True)
    jobs, nomes = [], []
    for s in seletores:
        for apn in aprendizes:
            if s == "aleatorio":
                for ss in sementes_aleatorio:
                    jobs.append((job_braco, (s, apn, cfg, G_total, B_max, ss)))
                    nomes.append(f"{s}#{ss}/{apn}")
            else:
                jobs.append((job_braco, (s, apn, cfg, G_total, B_max, cfg.semente)))
                nomes.append(f"{s}/{apn}")
    t0 = time.time()
    res = _executar_jobs(jobs, processos)
    bracos = dict(zip(nomes, res))
    det = {"config": cfg.como_dict(), "G": G_total, "B_max": B_max, "pool": POOL, "fontes": hash_fontes(),
           "bracos": {k: v["deterministico"] for k, v in bracos.items()},
           "resumo": {k: {"aceitas": v["deterministico"]["aceitas"], "ordem": v["deterministico"]["ordem_aceitacao"],
                          "custo_total": v["deterministico"]["custo_total"], "gasto_global": v["deterministico"]["gasto_global"],
                          "passos": len(v["deterministico"]["passos"]), "cadeia_reuso": v["deterministico"]["cadeia_reuso"]}
                      for k, v in bracos.items()}}
    med = {"parede_total_s": time.time() - t0, "bracos": {k: v["medicoes"] for k, v in bracos.items()}}
    with open(os.path.join(pasta, "deterministico.json"), "w", encoding="utf-8") as f:
        json.dump(det, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "medicoes.json"), "w", encoding="utf-8") as f:
        json.dump(med, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    with open(os.path.join(pasta, "relatorio.md"), "w", encoding="utf-8") as f:
        f.write(relatorio_md(det, med))
    return {"deterministico": det, "medicoes": med}


def relatorio_md(det, med) -> str:
    L = [f"# Currículo autodirigido — G = {det['G']}, B_max = {det['B_max']}, semente {det['config']['semente']}, política {det['config']['politica_busca']}", ""]
    L.append("| braço | aceitas | ordem de aceitação | passos | custo total | gasto global (enum.) | cadeia de reuso |")
    L.append("|---|---|---|---|---|---|---|")
    for k, v in det["resumo"].items():
        L.append(f"| {k} | {len(v['aceitas'])}: {', '.join(v['aceitas'])} | {' → '.join(v['ordem'])} | {v['passos']} | {v['custo_total']:,} | {v['gasto_global']:,} | {v['cadeia_reuso']} |")
    L.append("")
    for k, v in det["bracos"].items():
        L.append(f"## {k}")
        L.append("| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for p in v["passos"]:
            L.append(f"| {p['passo']} | {p['tarefa']} | {p['B']} | {p['aceita']} | {p['motivo']} | {p['custo']:,} | {p['enumeracao']} | {p['versao_biblioteca']} | `{p['hipotese'] or ''}` | {p['biblioteca_usada']} |")
        L.append("")
    L.append("## Medições")
    for k, m in med["bracos"].items():
        L.append(f"- {k}: parede {m['tempo_parede_s']:.0f} s, CPU {m['cpu_s']:.0f} s, memória {m['memoria_pico_kib']} KiB")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--semente", type=int, default=10_002)
    ap.add_argument("--G", type=int, default=120_000)
    ap.add_argument("--B-max", type=int, default=20_000)
    ap.add_argument("--politica", default="tamanho")
    ap.add_argument("--seletores", default="autodirigido,aleatorio,manual")
    ap.add_argument("--aprendizes", default="L-lib+f,L-fix")
    ap.add_argument("--sementes-aleatorio", default="1,2,3")
    ap.add_argument("--processos", type=int, default=4)
    a = ap.parse_args(argv)
    cfg = ConfigEM(semente=a.semente, B=a.B_max, politica_busca=a.politica, processos=a.processos, sondas=False,
                   auditoria_oe_orcamento=0)
    r = executar(os.path.join("runs", a.id), cfg, a.G, a.B_max, a.seletores.split(","), a.aprendizes.split(","),
                 [int(x) for x in a.sementes_aleatorio.split(",")], a.processos)
    print(json.dumps(r["deterministico"]["resumo"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
