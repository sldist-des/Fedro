"""Famílias de transferência estrutural (documento 06, missão 4), definidas e CONGELADAS antes de
qualquer execução de avaliação.

A especificação — ids, tipos, natureza, comparação, código-fonte Python das referências do ambiente
e os programas de referência na DSL (em E0 puro e com as abstrações manuais absViz/absExp) — tem um
hash SHA-256 publicado no documento 06 ANTES dos resultados (HASH_CONGELADO). O teste unitário
confere que o módulo ainda produz esse hash: qualquer ajuste posterior da família quebra o teste.
Nada aqui consulta os registros do experimento mínimo. Os programas de referência na DSL servem só
para (a) provar que cada tarefa é exprimível em E0 e (b) dar um LIMITE SUPERIOR do tamanho com e
sem abstrações; são de proveniência manual-teste e nunca entram numa biblioteca de aprendiz.

F-comp — composições INÉDITAS das operações adquiridas na cadeia (vizPretos → expandir):
  expandir2         Grade → L Pos → L Pos  vizinhas pretas em dois passos (expandir ∘ expandir)
  fronteira         Grade → L Pos → L Pos  vizinhas pretas de S que não estão em S
  isoladaP          Grade → Pos → Bool     p é preta e não tem vizinha preta (NenhumaIsolada = ∀p ¬isoladaP)
  duasVizinhas      Grade → Pos → Bool     p tem pelo menos duas vizinhas pretas
  pretasComVizinha  Grade → L Pos          pretas com alguma vizinha preta (= expandir g (pretas g))
F-neg — tarefas em que as operações adquiridas são inúteis (linhas, colunas, bordas):
  TopoCheio         Grade → Bool           (REGISTRO)
  LinhaOcupada      Grade → Bool           (REGISTRO)
  pretasUltimaColuna Grade → L Pos         pretas da última coluna
  semColuna1        Grade → L Pos → L Pos  S sem as células da primeira coluna
"""
from __future__ import annotations

import hashlib
import inspect
import json
from typing import Dict, List

from . import aprendizes as A
from .dsl import BASES, BOOL, FUN, GRADE, LP, POS, Primitiva, Tabela, entrada_biblioteca, parse, tamanho


def _viz_pretas(g, S):
    return frozenset(q for s in S for q in g.vizinhos(s) if g.celula(q))


REFERENCIAS_FAMILIAS = {
    "expandir2": lambda g, S: _viz_pretas(g, _viz_pretas(g, S)),
    "fronteira": lambda g, S: _viz_pretas(g, S) - frozenset(S),
    "isoladaP": lambda g, p: bool(g.celula(p)) and not any(g.celula(q) for q in g.vizinhos(p)),
    "duasVizinhas": lambda g, p: sum(1 for q in g.vizinhos(p) if g.celula(q)) >= 2,
    "pretasComVizinha": lambda g: frozenset(p for p in g.pretas() if any(g.celula(q) for q in g.vizinhos(p))),
    "pretasUltimaColuna": lambda g: A._pretos(g, [(i, g.n) for i in range(1, g.n + 1)]),
    "semColuna1": lambda g, S: frozenset(S) - {(i, 1) for i in range(1, g.n + 1)},
}
# registo no ambiente (as referências de função vivem em aprendizes.REFERENCIAS_FUNCAO)
for _k, _f in REFERENCIAS_FAMILIAS.items():
    A.REFERENCIAS_FUNCAO.setdefault(_k, _f)

_GL, _GPB, _GLP, _PB = FUN(GRADE, LP, LP), FUN(GRADE, POS, BOOL), FUN(GRADE, LP), FUN(GRADE, BOOL)

TAREFAS: Dict[str, A.Tarefa] = {t.id: t for t in [
    A.Tarefa("expandir2", _GL, "funcao", "F-comp", comparacao="conjunto"),
    A.Tarefa("fronteira", _GL, "funcao", "F-comp", comparacao="conjunto"),
    A.Tarefa("isoladaP", _GPB, "funcao", "F-comp"),
    A.Tarefa("duasVizinhas", _GPB, "funcao", "F-comp"),
    A.Tarefa("pretasComVizinha", _GLP, "funcao", "F-comp", comparacao="conjunto"),
    A.Tarefa("TopoCheio", _PB, "predicado", "F-neg", "TopoCheio"),
    A.Tarefa("LinhaOcupada", _PB, "predicado", "F-neg", "LinhaOcupada"),
    A.Tarefa("pretasUltimaColuna", _GLP, "funcao", "F-neg"),
    A.Tarefa("semColuna1", _GL, "funcao", "F-neg", comparacao="conjunto"),
]}
F_COMP: List[str] = [t for t in TAREFAS if TAREFAS[t].escada == "F-comp"]
F_NEG: List[str] = [t for t in TAREFAS if TAREFAS[t].escada == "F-neg"]
ORDEM = F_COMP + F_NEG

#: abstrações MANUAIS equivalentes às adquiridas na cadeia do documento 05 (só para referência)
ABSTRACOES_MANUAIS = {
    "absViz": "(\\ (g Grade) (p Pos) (filtrar@P (celula g) (vizinhos g p)))",
    "absExp": "(\\ (g Grade) (S LP) (juntar (mapear@P>LP (absViz g) S)))",
}

#: programas de referência: "E0" puro e "abs" (com absViz/absExp); limites SUPERIORES de tamanho
REFERENCIAS_DSL = {
    "expandir2": {
        "E0": "(\\ (g Grade) (S LP) (juntar (mapear@P>LP (\\ (p Pos) (filtrar@P (celula g) (vizinhos g p))) "
              "(juntar (mapear@P>LP (\\ (p Pos) (filtrar@P (celula g) (vizinhos g p))) S)))))",
        "abs": "(\\ (g Grade) (S LP) (absExp g (absExp g S)))"},
    "fronteira": {
        "E0": "(\\ (g Grade) (S LP) (diferenca (juntar (mapear@P>LP (\\ (p Pos) (filtrar@P (celula g) (vizinhos g p))) S)) S))",
        "abs": "(\\ (g Grade) (S LP) (diferenca (absExp g S) S))"},
    "isoladaP": {
        "E0": "(\\ (g Grade) (p Pos) (e (celula g p) (vazia?@P (filtrar@P (celula g) (vizinhos g p)))))",
        "abs": "(\\ (g Grade) (p Pos) (e (celula g p) (vazia?@P (absViz g p))))"},
    "duasVizinhas": {
        "E0": "(\\ (g Grade) (p Pos) (nao (vazia?@P (cauda@P (filtrar@P (celula g) (vizinhos g p))))))",
        "abs": "(\\ (g Grade) (p Pos) (nao (vazia?@P (cauda@P (absViz g p)))))"},
    "pretasComVizinha": {
        "E0": "(\\ (g Grade) (filtrar@P (\\ (p Pos) (algum@P (celula g) (vizinhos g p))) (pretas g)))",
        "abs": "(\\ (g Grade) (absExp g (pretas g)))"},
    "TopoCheio": {
        "E0": "(\\ (g Grade) (todos@P (celula g) (cabeca@LP (linhas g))))",
        "abs": "(\\ (g Grade) (todos@P (celula g) (cabeca@LP (linhas g))))"},
    "LinhaOcupada": {   # toda linha tem pelo menos uma preta (REGISTRO)
        "E0": "(\\ (g Grade) (todos@LP (\\ (l LP) (algum@P (celula g) l)) (linhas g)))",
        "abs": "(\\ (g Grade) (todos@LP (\\ (l LP) (algum@P (celula g) l)) (linhas g)))"},
    "pretasUltimaColuna": {
        "E0": "(\\ (g Grade) (filtrar@P (celula g) (cabeca@LP (reverter@LP (colunas g)))))",
        "abs": "(\\ (g Grade) (filtrar@P (celula g) (cabeca@LP (reverter@LP (colunas g)))))"},
    "semColuna1": {
        "E0": "(\\ (g Grade) (S LP) (diferenca S (cabeca@LP (colunas g))))",
        "abs": "(\\ (g Grade) (S LP) (diferenca S (cabeca@LP (colunas g))))"},
}


def entradas_manuais(base: str = "E0") -> List[Primitiva]:
    tb = BASES[base]
    out: List[Primitiva] = []
    for nome, texto in ABSTRACOES_MANUAIS.items():
        out.append(entrada_biblioteca(nome, parse(texto), "manual-teste", tb, out))
    return out


def tabela_referencia(base: str = "E0") -> Tabela:
    """Base + absViz/absExp manuais, uso "referencia" (proibida a aprendizes)."""
    return BASES[base].para_referencia(entradas_manuais(base), nome=f"{base}+abs-manuais")


def tamanhos_referencia() -> Dict[str, Dict[str, int]]:
    return {k: {m: tamanho(parse(v[m])) for m in ("E0", "abs")} for k, v in REFERENCIAS_DSL.items()}


def especificacao() -> dict:
    """Especificação congelável: tarefas, código-fonte das referências Python, programas DSL."""
    fontes = {k: inspect.getsource(f).strip() for k, f in REFERENCIAS_FAMILIAS.items()}
    fontes["_viz_pretas"] = inspect.getsource(_viz_pretas).strip()
    return {"tarefas": {k: v.como_dict() for k, v in TAREFAS.items()}, "ordem": ORDEM,
            "referencias_python": fontes, "abstracoes_manuais": ABSTRACOES_MANUAIS,
            "referencias_dsl": REFERENCIAS_DSL, "tamanhos": tamanhos_referencia()}


def hash_especificacao() -> str:
    return hashlib.sha256(json.dumps(especificacao(), sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


#: hash publicado no documento 06 ANTES da execução de avaliação (tests/test_validacao.py confere)
HASH_CONGELADO = "3b6646466e4545926d2c0cd990c792d7a3775e7da294ea059a4eb1e2a1d74aca"


def verificar_referencias(ns=(1, 2, 3, 4)) -> Dict[str, Dict[str, int]]:
    """Confere exaustivamente (n ≤ 4) que os programas DSL coincidem com as referências Python."""
    from .verificacao import verificar_exaustivo
    tab = tabela_referencia()
    out = {}
    for k, v in REFERENCIAS_DSL.items():
        out[k] = {m: verificar_exaustivo(parse(v[m]), TAREFAS[k], ns=ns, tabela=tab)["erros"] for m in ("E0", "abs")}
    return out


if __name__ == "__main__":
    print(hash_especificacao())
    print(json.dumps(tamanhos_referencia()))
    print(json.dumps(verificar_referencias()))
