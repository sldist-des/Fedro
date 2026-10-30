"""Implementações de referência independentes (ref_a, ref_b) e registro de conceitos.

ref_a: busca em largura explícita e laços diretos.
ref_b: união-busca e formulações declarativas (conjuntos/contadores).
Estes programas são REFERÊNCIAS DO AMBIENTE. Nunca entram na biblioteca do aprendiz.
"""
from __future__ import annotations
from collections import Counter, deque
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Callable, Dict, FrozenSet, List, Optional, Tuple
from .grade import Grade, Pos

Comp = FrozenSet[Pos]


# ---------------- componentes ----------------
# Memoização por grade (só desempenho): cada implementação tem o seu próprio cache,
# de modo que ref_a continua a depender apenas de componentes_a e ref_b de componentes_b.
# Devolve tuplas (imutáveis) para que o valor em cache não possa ser alterado por quem chama.
@lru_cache(maxsize=1 << 17)
def componentes_a(g: Grade) -> Tuple[Comp, ...]:
    vistos = set()
    comps = []
    for p in g.pretas():
        if p in vistos:
            continue
        fila = deque([p]); vistos.add(p); cel = []
        while fila:
            q = fila.popleft(); cel.append(q)
            for r in g.vizinhos(q):
                if g.celula(r) and r not in vistos:
                    vistos.add(r); fila.append(r)
        comps.append(frozenset(cel))
    return tuple(comps)


@lru_cache(maxsize=1 << 17)
def componentes_b(g: Grade) -> Tuple[Comp, ...]:
    pai: Dict[Pos, Pos] = {p: p for p in g.pretas()}

    def raiz(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]; x = pai[x]
        return x

    for p in pai:
        i, j = p
        for q in ((i + 1, j), (i, j + 1)):
            if q in pai:
                a, b = raiz(p), raiz(q)
                if a != b:
                    pai[a] = b
    grupos: Dict[Pos, set] = {}
    for p in pai:
        grupos.setdefault(raiz(p), set()).add(p)
    return tuple(frozenset(s) for s in grupos.values())


# ---------------- regiões ----------------
def regiao(nome: str, g: Grade) -> List[Pos]:
    n = g.n
    if nome == "linha1":
        return [(1, j) for j in range(1, n + 1)]
    if nome == "linhaN":
        return [(n, j) for j in range(1, n + 1)]
    if nome == "col1":
        return [(i, 1) for i in range(1, n + 1)]
    if nome == "colN":
        return [(i, n) for i in range(1, n + 1)]
    if nome == "metadeEsq":
        return [(i, j) for i in range(1, n + 1) for j in range(1, n // 2 + 1)]
    if nome == "metadeDir":
        return [(i, j) for i in range(1, n + 1) for j in range(n - n // 2 + 1, n + 1)]
    raise KeyError(nome)


def toca_borda(c: Comp, n: int) -> bool:
    return any(i == 1 or i == n or j == 1 or j == n for i, j in c)


def contem_canto(c: Comp, n: int) -> bool:
    return any(p in c for p in ((1, 1), (1, n), (n, 1), (n, n)))


def reto(c: Comp) -> bool:
    return len({i for i, _ in c}) == 1 or len({j for _, j in c}) == 1


PROPRIEDADES = {
    "tocaBorda": lambda c, n: toca_borda(c, n),
    "contemCanto": lambda c, n: contem_canto(c, n),
    "reto": lambda c, n: reto(c),
    "min2": lambda c, n: len(c) >= 2,
    "min3": lambda c, n: len(c) >= 3,
}


# ---------------- conceitos ----------------
@dataclass
class Conceito:
    nome: str
    familia: str
    ref_a: Callable[[Grade], bool]
    ref_b: Callable[[Grade], bool]
    esquema: str
    invariancias: List[str] = field(default_factory=list)
    params: dict = field(default_factory=dict)

    def rotulo(self, g: Grade) -> bool:
        a, b = self.ref_a(g), self.ref_b(g)
        if a != b:
            raise AssertionError(f"referências discordam em {self.nome}: {g.serializar()}")
        return a


REGISTRO: Dict[str, Conceito] = {}


def _reg(c: Conceito):
    REGISTRO[c.nome] = c
    return c


TODAS = ["rot90", "refH", "refV", "transp"]
ROWSYM = ["refH"]
COLSYM = ["refV"]

# ---- F1 ----
_reg(Conceito("ExistePreta", "F1",
              lambda g: any(g.celula(p) for p in g.posicoes()),
              lambda g: g.contagem_pretas() > 0, "F1", TODAS))
_reg(Conceito("ParAdjacente", "F1",
              lambda g: any(g.celula(p) and any(g.celula(q) for q in g.vizinhos(p)) for p in g.posicoes()),
              lambda g: any(len(c) >= 2 for c in componentes_b(g)), "F1", TODAS))
_reg(Conceito("LinhaOcupada", "F1",
              lambda g: all(any(g.celula(p) for p in l) for l in g.linhas()),
              lambda g: len({i for i, _ in g.pretas()}) == g.n, "F1", ROWSYM + COLSYM))
_reg(Conceito("TopoCheio", "F1",
              lambda g: all(g.celula(p) for p in g.linhas()[0]),
              lambda g: sum(g.bits[: g.n]) == g.n, "F1", ROWSYM))
# ---- F1' (distratores) ----
_reg(Conceito("CantoSupEsq", "F1'", lambda g: bool(g.celula((1, 1))), lambda g: g.bits[0] == 1, "F1'", []))
_reg(Conceito("Diagonal", "F1'",
              lambda g: all(g.celula((i, i)) for i in range(1, g.n + 1)),
              lambda g: all(g.bits[k * g.n + k] for k in range(g.n)), "F1'", ["transp"]))
_reg(Conceito("ColunaDoisVazia", "F1'",
              lambda g: g.n >= 2 and not any(g.celula((i, 2)) for i in range(1, g.n + 1)),
              lambda g: g.n >= 2 and all(g.bits[k * g.n + 1] == 0 for k in range(g.n)), "F1'", COLSYM))


# ---- F2: número de componentes ----
def _numcomp(nome, teste_a, teste_b, params):
    _reg(Conceito(nome, "F2",
                  lambda g, t=teste_a: t(len(componentes_a(g))),
                  lambda g, t=teste_b: t(len(componentes_b(g))), "NumComp", TODAS, params))


_numcomp("UmComponente", lambda k: k == 1, lambda k: k == 1, {"S": "=1"})
_numcomp("DoisSeparados", lambda k: k == 2, lambda k: k == 2, {"S": "=2"})
_numcomp("TresComponentes", lambda k: k == 3, lambda k: k == 3, {"S": "=3"})
_numcomp("PeloMenosDois", lambda k: k >= 2, lambda k: not (k < 2), {"S": ">=2"})
_numcomp("NoMaximoDois", lambda k: k <= 2, lambda k: not (k > 2), {"S": "<=2"})


def _existe(nome, prop):
    _reg(Conceito(nome, "F2",
                  lambda g: any(PROPRIEDADES[prop](c, g.n) for c in componentes_a(g)),
                  lambda g: not all(not PROPRIEDADES[prop](c, g.n) for c in componentes_b(g)),
                  "ExisteComp", TODAS, {"P": prop}))


def _todos(nome, prop):
    _reg(Conceito(nome, "F2",
                  lambda g: len(componentes_a(g)) > 0 and all(PROPRIEDADES[prop](c, g.n) for c in componentes_a(g)),
                  lambda g: bool(componentes_b(g)) and not any(not PROPRIEDADES[prop](c, g.n) for c in componentes_b(g)),
                  "TodosComp", TODAS, {"P": prop}))


_existe("ExisteCompTocaBorda", "tocaBorda")
_existe("ExisteCompContemCanto", "contemCanto")
_existe("ExisteCompReto", "reto")
_existe("ExisteCompMin3", "min3")
_todos("TodosCompReto", "reto")
_todos("NenhumaIsolada", "min2")
_todos("TodosCompTocaBorda", "tocaBorda")
_reg(Conceito("MaiorTocaBorda", "F2",
              lambda g: (lambda cs: bool(cs) and any(len(c) == max(len(x) for x in cs) and toca_borda(c, g.n) for c in cs))(componentes_a(g)),
              lambda g: (lambda cs: bool(cs) and max(cs, key=lambda c: (len(c), toca_borda(c, g.n))).__len__() >= 0 and toca_borda(max(cs, key=lambda c: (len(c), toca_borda(c, g.n))), g.n))(componentes_b(g)),
              "MaiorTocaBorda", TODAS))


# ---- F3: comparação de cardinalidades ----
def _card_a(g, nome):
    return sum(1 for p in regiao(nome, g) if g.celula(p))


def _card_b(g, nome):
    return len(set(regiao(nome, g)) & set(g.pretas()))


PARES = [("linha1", "linhaN"), ("col1", "colN"), ("metadeEsq", "metadeDir")]
for A, B in PARES:
    _reg(Conceito(f"Igual_{A}_{B}", "F3",
                  lambda g, A=A, B=B: _card_a(g, A) == _card_a(g, B),
                  lambda g, A=A, B=B: _card_b(g, A) == _card_b(g, B), "CardIgual", [], {"A": A, "B": B}))
    _reg(Conceito(f"NoMax_{A}_{B}", "F3",
                  lambda g, A=A, B=B: _card_a(g, A) <= _card_a(g, B),
                  lambda g, A=A, B=B: not (_card_b(g, A) > _card_b(g, B)), "CardNoMax", [], {"A": A, "B": B}))
    _reg(Conceito(f"NoMax_{B}_{A}", "F3",
                  lambda g, A=A, B=B: _card_a(g, B) <= _card_a(g, A),
                  lambda g, A=A, B=B: not (_card_b(g, B) > _card_b(g, A)), "CardNoMax", [], {"A": B, "B": A}))
_reg(Conceito("LinhasIguais", "F3",
              lambda g: all(sum(g.celula(p) for p in l) == sum(g.celula(p) for p in g.linhas()[0]) for l in g.linhas()),
              lambda g: len({sum(g.bits[i * g.n:(i + 1) * g.n]) for i in range(g.n)}) == 1, "LinhasIguais", ROWSYM))
_reg(Conceito("ColunasIguais", "F3",
              lambda g: all(sum(g.celula(p) for p in c) == sum(g.celula(p) for p in g.colunas()[0]) for c in g.colunas()),
              lambda g: len({sum(g.bits[j::g.n]) for j in range(g.n)}) == 1, "ColunasIguais", COLSYM))

# ---- F2×F3 ----
_reg(Conceito("TodosMesmoTamanho", "F2xF3",
              lambda g: (lambda cs: bool(cs) and all(len(c) == len(cs[0]) for c in cs))(componentes_a(g)),
              lambda g: len({len(c) for c in componentes_b(g)}) == 1, "TodosMesmoTamanho", TODAS))
_reg(Conceito("NumCompIgualLinha1", "F2xF3",
              lambda g: len(componentes_a(g)) == _card_a(g, "linha1"),
              lambda g: len(componentes_b(g)) == _card_b(g, "linha1"), "NumCompIgualRegiao", ROWSYM, {"A": "linha1"}))
_reg(Conceito("NumCompIgualCol1", "F2xF3",
              lambda g: len(componentes_a(g)) == _card_a(g, "col1"),
              lambda g: len(componentes_b(g)) == _card_b(g, "col1"), "NumCompIgualRegiao", COLSYM, {"A": "col1"}))
_reg(Conceito("MaiorCompPeloMenosLinha1", "F2xF3",
              lambda g: (max((len(c) for c in componentes_a(g)), default=0)) >= _card_a(g, "linha1"),
              lambda g: not (max((len(c) for c in componentes_b(g)), default=0) < _card_b(g, "linha1")), "MaiorCompVsRegiao", ROWSYM, {"A": "linha1"}))


def conceitos(familias: Optional[List[str]] = None) -> List[Conceito]:
    return [c for c in REGISTRO.values() if familias is None or c.familia in familias]


def transformar(g: Grade, t: str) -> Grade:
    return {"rot90": g.rotacao90, "refH": g.reflexao_h, "refV": g.reflexao_v, "transp": g.transposta}[t]()


# ---- predicados auxiliares de referência (para identidade comportamental, M8) ----
def fecho_ref(g: Grade, semente: List[Pos]) -> FrozenSet[Pos]:
    """Conjunto alcançável a partir das sementes por vizinhança entre pretas (as sementes entram mesmo se brancas)."""
    vistos = set(semente); fila = deque(semente)
    while fila:
        q = fila.popleft()
        for r in g.vizinhos(q):
            if g.celula(r) and r not in vistos:
                vistos.add(r); fila.append(r)
    return frozenset(vistos)
