#!/usr/bin/env python3
"""Insere/atualiza nas marcas <!-- TABELAS:X --> ... <!-- /TABELAS:X --> de docs/08 as tabelas geradas por
analysis/relatorio_bx.py para cada registro. Idempotente: substitui o bloco entre as marcas."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import relatorio_bx as R  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = {
    "A": "runs/bx-grades-e0-independente-v1-A-s10007",
    "B": "runs/bx-grades-e0-independente-v1-B-s10007",
    "C8": "runs/bx-grades-e0-independente-v1-C-s10008",
    "C9": "runs/bx-grades-e0-independente-v1-C-s10009",
    "D": "runs/bx-grades-e0-independente-v1-D-k20",
    "E": "runs/bx-grades-e0-independente-v1-E-ordens",
}


def main():
    cam = os.path.join(RAIZ, "docs", "08-relatorio-benchmark-cego.md")
    with open(cam, encoding="utf-8") as f:
        s = f.read()
    for chave, pasta in MAPA.items():
        p = os.path.join(RAIZ, pasta)
        if not os.path.exists(os.path.join(p, "deterministico.json")):
            continue
        tab = R.principal(p)
        bloco = f"<!-- TABELAS:{chave} -->\n{tab}\n<!-- /TABELAS:{chave} -->"
        padrao = re.compile(rf"<!-- TABELAS:{chave} -->.*?<!-- /TABELAS:{chave} -->", re.S)
        if padrao.search(s):
            s = padrao.sub(lambda _m: bloco, s)
        else:
            s = s.replace(f"<!-- TABELAS:{chave} -->", bloco)
    with open(cam, "w", encoding="utf-8") as f:
        f.write(s)
    print("docs/08 atualizado")


if __name__ == "__main__":
    main()
