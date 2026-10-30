#!/usr/bin/env python3
"""Auditoria de vazamento de informação do contrato público e do kit do autor (benchmark/).

NÃO ENVIAR ESTE FICHEIRO NEM O SEU RELATÓRIO AO AUTOR EXTERNO: ambos contêm os termos proibidos.

Constrói a lista de termos que não podem aparecer nos ficheiros enviados ao autor externo a partir do
próprio código (ids das tarefas do currículo, das famílias de transferência e da escada do piloto,
nomes dos conceitos do registo, nomes das entradas de biblioteca) e de uma lista fixa de termos de
mecanismo e de resultados, e procura-os, por fronteira de palavra, em cada ficheiro a enviar.
Escreve benchmark/auditoria-vazamento.md.
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, List

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

#: ficheiros que SERÃO enviados ao autor externo (e só estes)
FICHEIROS_ENVIADOS = [
    "benchmark/contrato-publico.md",
    "benchmark/kit-autor/validar_pacote.py",
    "benchmark/kit-autor/grade.py",
    "benchmark/kit-autor/exemplo-pacote/tarefas.json",
    "benchmark/kit-autor/exemplo-pacote/referencias.py",
    "benchmark/kit-autor/exemplo-pacote/testes_ocultos.json",
    "benchmark/kit-autor/exemplo-pacote/testemunhas.json",
    "benchmark/kit-autor/exemplo-pacote/MANIFESTO.json",
]

#: termos de MECANISMO e de RESULTADOS que revelariam o que esperamos do sistema (case-insensitive, radicais)
RADICAIS_MECANISMO = [
    "bibliotec", "abstra", "reutiliz", "reuso", "transfer", "promo", "compress", "lesão", "lesao", "currícul", "curricul",
    "autodirig", "consolid", "operação intermedi", "operacao intermedi", "L-fix", "L-lib", "unigrama", "no-go", "NO-GO",
    "documento 0", "docs/0", "doc. 0", "experimento mínimo", "experimento minimo", "replica", "veredito", "H-B1", "H-B2",
    "H-B3", "bootstrap", "emerg", "degrau", "escada", "Fedro", "Opus", "Fable", "Claude",
]

#: palavras do domínio que são PERMITIDAS embora contenham radicais acima (confere-se por igualdade de palavra)
EXCECOES_PALAVRA = {"grade", "grades", "degradar"}

#: identificadores internos que coincidem com palavras comuns do português usadas no sentido comum no
#: contrato ("passos de avaliação"); o programa homónimo da escada nunca é mencionado como programa.
#: Conferido manualmente: só é aceite fora de trechos de código (sem crases à volta).
EXCECOES_IDENTIFICADOR = {"passo"}


def termos_proibidos() -> Dict[str, List[str]]:
    from fedro_piloto import aprendizes as A
    from fedro_piloto import experimento_minimo as EM
    from fedro_piloto import familias_transferencia as F
    from fedro_piloto import programas_referencia as PR
    from fedro_piloto.referencias import REGISTRO
    ids = set(EM.TAREFAS) | set(F.TAREFAS) | set(REGISTRO) | {p.nome for p in PR.ESCADA} | set(A.TAREFAS_POR_ID)
    ids |= set(F.ABSTRACOES_MANUAIS) | {f"abs{i}" for i in range(1, 10)}
    ids |= set(A.REFERENCIAS_FUNCAO) - set()        # inclui expandir, pretasColuna1, semLinha1 e as famílias
    # nunca proibir uma primitiva de E0 nem palavras do ambiente
    from fedro_piloto.dsl import BASES
    prims = set(BASES["E0"].nomes()) | {p.split("@")[0] for p in BASES["E0"].nomes()}
    ids = {i for i in ids if i not in prims and not i.startswith("bx:")}
    return {"identificadores": sorted(ids), "radicais": list(RADICAIS_MECANISMO)}


def violacoes_no_texto(texto: str, proibidos: Dict[str, List[str]]) -> List[dict]:
    out = []
    for ident in proibidos["identificadores"]:
        for m in re.finditer(r"(?<![A-Za-z0-9_])" + re.escape(ident) + r"(?![A-Za-z0-9_])", texto):
            if ident in EXCECOES_IDENTIFICADOR and not (m.start() > 0 and texto[m.start() - 1] == "`"):
                continue            # palavra comum fora de código
            out.append({"tipo": "identificador", "termo": ident, "pos": m.start()})
    baixo = texto.lower()
    for rad in proibidos["radicais"]:
        for m in re.finditer(re.escape(rad.lower()), baixo):
            # palavra completa que contém o radical
            ini = m.start()
            while ini > 0 and (baixo[ini - 1].isalnum() or baixo[ini - 1] in "_-"):
                ini -= 1
            fim = m.end()
            while fim < len(baixo) and (baixo[fim].isalnum() or baixo[fim] in "_-"):
                fim += 1
            palavra = baixo[ini:fim]
            if palavra in EXCECOES_PALAVRA:
                continue
            out.append({"tipo": "radical", "termo": rad, "palavra": texto[ini:fim], "pos": ini})
    return out


def programas_enviados() -> List[str]:
    """Programas E0 em código nos ficheiros enviados (trechos `(\\ …)` do contrato e testemunhas do kit)."""
    progs = []
    for rel in FICHEIROS_ENVIADOS:
        cam = os.path.join(RAIZ, rel)
        if not os.path.exists(cam):
            continue
        with open(cam, encoding="utf-8") as f:
            txt = f.read()
        if rel.endswith("testemunhas.json"):
            progs += [v for v in json.loads(txt).values() if isinstance(v, str)]
        else:
            progs += re.findall(r"`(\(\\\\? [^`]*)`", txt)
    return [p.replace("\\\\", "\\") for p in progs]


def solucoes_conhecidas() -> set:
    """Formas canónicas de TODAS as hipóteses aceitas nos registros e dos programas de referência internos."""
    from fedro_piloto.biblioteca import canonizar
    from fedro_piloto.dsl import imprimir, parse
    from fedro_piloto import familias_transferencia as F
    from fedro_piloto import programas_referencia as PR
    from fedro_piloto.verificacao import hipoteses_aceitas
    textos = []
    for raiz, _, fich in os.walk(os.path.join(RAIZ, "runs")):
        if "deterministico.json" in fich:
            try:
                with open(os.path.join(raiz, "deterministico.json"), encoding="utf-8") as f:
                    d = json.load(f)
            except Exception:  # noqa: BLE001
                continue
            bracos = d.get("bracos", {})
            for b in bracos.values():
                if isinstance(b, dict):
                    textos += [h for _, h in hipoteses_aceitas(b)]
                    textos += [a.get("corpo") for a in b.get("abstracoes", []) if a.get("corpo")]
    textos += [p.texto_E0 for p in PR.ESCADA] + [v[m] for v in F.REFERENCIAS_DSL.values() for m in v] + list(F.ABSTRACOES_MANUAIS.values())
    out = set()
    for t in textos:
        try:
            out.add(imprimir(canonizar(parse(t))))
        except Exception:  # noqa: BLE001
            pass
    return out


def programas_que_sao_solucoes() -> List[str]:
    from fedro_piloto.biblioteca import canonizar
    from fedro_piloto.dsl import imprimir, parse
    conhecidas = solucoes_conhecidas()
    maus = []
    for p in programas_enviados():
        try:
            if imprimir(canonizar(parse(p))) in conhecidas:
                maus.append(p)
        except Exception:  # noqa: BLE001
            maus.append(p + "  (não analisável)")
    return maus


def auditar(escrever: bool = False) -> dict:
    proibidos = termos_proibidos()
    por_ficheiro = {}
    violacoes = []
    for rel in FICHEIROS_ENVIADOS:
        cam = os.path.join(RAIZ, rel)
        if not os.path.exists(cam):
            violacoes.append({"ficheiro": rel, "tipo": "ausente"})
            continue
        with open(cam, encoding="utf-8") as f:
            txt = f.read()
        vs = violacoes_no_texto(txt, proibidos)
        por_ficheiro[rel] = len(vs)
        for v in vs:
            linha = txt.count("\n", 0, v["pos"]) + 1
            violacoes.append({"ficheiro": rel, "linha": linha, **{k: v[k] for k in v if k != "pos"}})
    progs = programas_enviados()
    for p in programas_que_sao_solucoes():
        violacoes.append({"ficheiro": "(programas em código)", "tipo": "programa-e-solucao-conhecida", "programa": p})
    rel = {"ficheiros": por_ficheiro, "violacoes": violacoes, "num_identificadores": len(proibidos["identificadores"]),
           "num_radicais": len(proibidos["radicais"]), "programas_enviados": progs}
    if escrever:
        with open(os.path.join(RAIZ, "benchmark", "auditoria-vazamento.md"), "w", encoding="utf-8") as f:
            f.write(relatorio_md(rel, proibidos))
    return rel


def relatorio_md(rel: dict, proibidos: Dict[str, List[str]]) -> str:
    L = ["# Auditoria de vazamento — contrato público e kit do autor", "",
         "**NÃO ENVIAR ao autor externo**: este relatório lista os termos proibidos.", "",
         "## Ficheiros auditados (os únicos a enviar)", ""]
    for k, v in rel["ficheiros"].items():
        L.append(f"- `{k}`: {v} violações")
    L += ["", f"## Violações: {len(rel['violacoes'])}", ""]
    for v in rel["violacoes"]:
        L.append(f"- {json.dumps(v, ensure_ascii=False)}")
    if not rel["violacoes"]:
        L.append("Nenhuma.")
    L += ["", "## Verificação automática", "",
          f"- {rel['num_identificadores']} identificadores proibidos (tarefas do currículo, famílias de transferência, escada do piloto, conceitos do registo, nomes de entradas de biblioteca), com fronteira de palavra;",
          f"- {rel['num_radicais']} radicais de mecanismo/resultado (case-insensitive), com exceções de palavra {sorted(EXCECOES_PALAVRA)};",
          f"- identificadores que coincidem com palavras comuns e são aceites fora de código: {sorted(EXCECOES_IDENTIFICADOR)}.",
          "", "### Identificadores proibidos", "", "`" + "`, `".join(proibidos["identificadores"]) + "`", "",
          "### Radicais proibidos", "", "`" + "`, `".join(proibidos["radicais"]) + "`", "",
          "## Verificação manual (lista de conferência)", "",
          "1. O contrato descreve só o ambiente, os tipos, as primitivas de E0 e a sua semântica, as restrições computacionais, a interface, a integridade e a comunicação (contrato §1–§8).",
          "2. Nenhuma solução, nenhum programa de referência das nossas tarefas, nenhum nome de entrada de biblioteca, nenhum número de resultado.",
          f"3. Os programas em código nos ficheiros enviados ({len(rel['programas_enviados'])}: {rel['programas_enviados']}) não são α-equivalentes a nenhuma hipótese aceita em qualquer registro de runs/, a nenhuma entrada de biblioteca registada nem a nenhum programa de referência interno (conferido automaticamente: tipo de violação 'programa-e-solucao-conhecida').",
          "4. As tarefas do pacote de exemplo são triviais e não se parecem com nenhuma tarefa nossa (primeira célula preta; ser canto; identidade).",
          "5. O aprendiz é descrito apenas como 'um sistema de síntese de programas em E0 que pode manter estado interno entre tarefas'.",
          "6. A capacidade de busca é declarada como alcance medido da linguagem base (≈ 8–9 folhas), sem dizer o que gostaríamos que fosse resolvido.",
          ""]
    return "\n".join(L)


if __name__ == "__main__":
    r = auditar(escrever=True)
    print(json.dumps({"ficheiros": r["ficheiros"], "violacoes": len(r["violacoes"])}, ensure_ascii=False, indent=1))
    for v in r["violacoes"][:50]:
        print(" ", v)
    sys.exit(1 if r["violacoes"] else 0)
