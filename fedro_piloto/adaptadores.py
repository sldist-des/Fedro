"""Adaptadores de portador (documento 02, 2.11.1; documento 03, U18).

Um adaptador substitui APENAS as primitivas de portador (celula, posicoes, pretas, linhas, colunas,
vizinhos; em E0', linhaDe, colunaDe); a biblioteca aprendida e o programa são avaliados sem
modificação. No piloto os adaptadores só são testados unitariamente (a transferência não é executada).

Portadores:
  Sequencia: m >= 1 bits; posicoes = índices 1..m; vizinhos(i) = (i-1, i+1) dentro dos limites;
             linhas = uma única lista com todos os índices; colunas = lista de singletons;
             linhaDe(i) = todos os índices; colunaDe(i) = (i,).
  Grafo:     N >= 1 nós 1..N rotulados preto/branco, arestas não orientadas; vizinhos = adjacência
             em ordem crescente; linhas, colunas, linhaDe, colunaDe NÃO DEFINIDAS (levantam
             PrimitivaNaoDefinida): uma partição em linhas introduziria estrutura que o conceito
             pressupõe (critério de não-vazamento de 2.11.1).

Codificação de posições. Pos é opaco em E0/E0' (só igualP, pertence, uniao, diferenca o observam,
por igualdade). O índice/nó i é codificado como o par (1, i): assim o valor padrão (1,1) de Sem_n
(cabeca de lista vazia, fix em Pos) é o primeiro elemento na ordem fixa, como em grades. As funções
de referência (componentes) devolvem índices inteiros; `indices` converte.

Semântica: Sem_n exige um n. Para um portador com m elementos usa-se n_semantica = ceil(sqrt(m)),
logo F = n⁴ >= m² (para m = n², grade quadrada, coincide com grades). Todas as primitivas do
adaptador são totais em Pos (fora do portador: celula falso, vizinhos vazio, linhaDe vazio).

Componentes de referência (dois algoritmos independentes por portador, como ref_a/ref_b):
  sequência: corridas de uns por varrimento | por fronteiras de corrida (declarativa);
  grafo: busca em largura | união-busca.
"""
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from typing import Callable, Dict, FrozenSet, Iterable, List, Optional, Sequence, Tuple, Union

from .avaliador import Contador, aplicar, avaliar
from .dsl import REGISTRO_BASE, Primitiva, Tabela, Termo

PROVENIENCIA = "ambiente"
#: primitivas de portador substituídas por um adaptador (instâncias de E0 e de E0')
PRIMITIVAS_PORTADOR = ("celula", "posicoes", "pretas", "linhas", "colunas", "vizinhos", "linhaDe", "colunaDe")

Pos = Tuple[int, int]


class PrimitivaNaoDefinida(Exception):
    """Primitiva de portador sem equivalente legítimo neste portador (2.11.1)."""


def pos(i: int) -> Pos:
    """Codificação opaca do índice/nó i como Pos."""
    return (1, i)


def indice(p: Pos) -> int:
    return p[1]


def indices(ps: Iterable[Pos]) -> FrozenSet[int]:
    return frozenset(indice(p) for p in ps)


# ---------------------------------------------------------------- portadores
@dataclass(frozen=True)
class Sequencia:
    bits: Tuple[int, ...]

    def __post_init__(self):
        if not self.bits:
            raise ValueError("sequência vazia")
        if any(b not in (0, 1) for b in self.bits):
            raise ValueError("bits devem ser 0/1")

    @staticmethod
    def de_texto(txt: str) -> "Sequencia":
        return Sequencia(tuple(int(c) for c in txt))

    @property
    def m(self) -> int:
        return len(self.bits)

    def texto(self) -> str:
        return "".join(map(str, self.bits))

    def _dentro(self, p) -> bool:
        return isinstance(p, tuple) and len(p) == 2 and p[0] == 1 and 1 <= p[1] <= self.m

    # primitivas de portador
    def celula(self, p: Pos) -> bool:
        return self._dentro(p) and self.bits[p[1] - 1] == 1

    def posicoes(self) -> Tuple[Pos, ...]:
        return tuple(pos(i) for i in range(1, self.m + 1))

    def pretas(self) -> Tuple[Pos, ...]:
        return tuple(pos(i) for i in range(1, self.m + 1) if self.bits[i - 1])

    def vizinhos(self, p: Pos) -> Tuple[Pos, ...]:
        if not self._dentro(p):
            return ()
        i = p[1]
        return tuple(pos(j) for j in (i - 1, i + 1) if 1 <= j <= self.m)

    def linhas(self) -> Tuple[Tuple[Pos, ...], ...]:
        return (self.posicoes(),)

    def colunas(self) -> Tuple[Tuple[Pos, ...], ...]:
        return tuple((p,) for p in self.posicoes())

    def linhaDe(self, p: Pos) -> Tuple[Pos, ...]:
        return self.posicoes() if self._dentro(p) else ()

    def colunaDe(self, p: Pos) -> Tuple[Pos, ...]:
        return (p,) if self._dentro(p) else ()


@dataclass(frozen=True)
class Grafo:
    rotulos: Tuple[int, ...]                  # rótulo do nó i em rotulos[i-1]; 1 = preto
    arestas: FrozenSet[Tuple[int, int]]       # pares (a, b) com a < b

    def __post_init__(self):
        if not self.rotulos:
            raise ValueError("grafo sem nós")
        if any(b not in (0, 1) for b in self.rotulos):
            raise ValueError("rótulos devem ser 0/1")
        for a, b in self.arestas:
            if not (1 <= a < b <= len(self.rotulos)):
                raise ValueError(f"aresta inválida: {(a, b)}")

    @staticmethod
    def de_lista(num_nos: int, arestas: Iterable[Tuple[int, int]], pretos: Iterable[int]) -> "Grafo":
        pretos = set(pretos)
        norm = frozenset((min(a, b), max(a, b)) for a, b in arestas if a != b)
        return Grafo(tuple(1 if i in pretos else 0 for i in range(1, num_nos + 1)), norm)

    @property
    def m(self) -> int:
        return len(self.rotulos)

    def adjacentes(self, i: int) -> Tuple[int, ...]:
        return tuple(sorted({b for a, b in self.arestas if a == i} | {a for a, b in self.arestas if b == i}))

    def _dentro(self, p) -> bool:
        return isinstance(p, tuple) and len(p) == 2 and p[0] == 1 and 1 <= p[1] <= self.m

    # primitivas de portador
    def celula(self, p: Pos) -> bool:
        return self._dentro(p) and self.rotulos[p[1] - 1] == 1

    def posicoes(self) -> Tuple[Pos, ...]:
        return tuple(pos(i) for i in range(1, self.m + 1))

    def pretas(self) -> Tuple[Pos, ...]:
        return tuple(pos(i) for i in range(1, self.m + 1) if self.rotulos[i - 1])

    def vizinhos(self, p: Pos) -> Tuple[Pos, ...]:
        return tuple(pos(j) for j in self.adjacentes(p[1])) if self._dentro(p) else ()

    def linhas(self):
        raise PrimitivaNaoDefinida("linhas não é definida em grafos (2.11.1)")

    def colunas(self):
        raise PrimitivaNaoDefinida("colunas não é definida em grafos (2.11.1)")

    def linhaDe(self, p):
        raise PrimitivaNaoDefinida("linhaDe não é definida em grafos (2.11.1)")

    def colunaDe(self, p):
        raise PrimitivaNaoDefinida("colunaDe não é definida em grafos (2.11.1)")


Portador = Union[Sequencia, Grafo]


def n_semantica(portador: Portador) -> int:
    """n de Sem_n para o portador: ceil(sqrt(m)), de modo que F(n) = n⁴ >= m²."""
    m = portador.m
    return 1 if m <= 1 else math.isqrt(m - 1) + 1


# ---------------------------------------------------------------- componentes de referência
def componentes_sequencia_a(s: Sequencia) -> Tuple[FrozenSet[int], ...]:
    """Corridas de uns por varrimento da esquerda para a direita."""
    out, atual = [], []
    for i, b in enumerate(s.bits, start=1):
        if b:
            atual.append(i)
        elif atual:
            out.append(frozenset(atual)); atual = []
    if atual:
        out.append(frozenset(atual))
    return tuple(out)


def componentes_sequencia_b(s: Sequencia) -> Tuple[FrozenSet[int], ...]:
    """Declarativa: uma corrida começa em i com bit 1 e (i = 1 ou bit i-1 = 0) e termina no primeiro
    j >= i cujo sucessor é 0 ou não existe."""
    b = (0,) + s.bits + (0,)
    inicios = [i for i in range(1, s.m + 1) if b[i] and not b[i - 1]]
    fins = [j for j in range(1, s.m + 1) if b[j] and not b[j + 1]]
    return tuple(frozenset(range(i, j + 1)) for i, j in zip(inicios, fins))


def componentes_grafo_a(gr: Grafo) -> Tuple[FrozenSet[int], ...]:
    """Busca em largura sobre a adjacência restrita a nós pretos."""
    vistos, out = set(), []
    for i in range(1, gr.m + 1):
        if not gr.rotulos[i - 1] or i in vistos:
            continue
        fila, comp = deque([i]), []
        vistos.add(i)
        while fila:
            u = fila.popleft(); comp.append(u)
            for v in gr.adjacentes(u):
                if gr.rotulos[v - 1] and v not in vistos:
                    vistos.add(v); fila.append(v)
        out.append(frozenset(comp))
    return tuple(out)


def componentes_grafo_b(gr: Grafo) -> Tuple[FrozenSet[int], ...]:
    """União-busca sobre as arestas entre nós pretos."""
    pai = {i: i for i in range(1, gr.m + 1) if gr.rotulos[i - 1]}

    def raiz(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]; x = pai[x]
        return x

    for a, b in sorted(gr.arestas):
        if a in pai and b in pai:
            ra, rb = raiz(a), raiz(b)
            if ra != rb:
                pai[ra] = rb
    grupos: Dict[int, set] = {}
    for i in pai:
        grupos.setdefault(raiz(i), set()).add(i)
    return tuple(frozenset(s) for s in grupos.values())


def _canon(cs: Iterable[FrozenSet[int]]) -> Tuple[FrozenSet[int], ...]:
    return tuple(sorted(cs, key=lambda c: min(c)))


def componentes_referencia(portador: Portador) -> Tuple[FrozenSet[int], ...]:
    """Componentes (índices inteiros), conferidos pelas duas implementações; ordem pelo menor índice."""
    if isinstance(portador, Sequencia):
        a, b = componentes_sequencia_a(portador), componentes_sequencia_b(portador)
    elif isinstance(portador, Grafo):
        a, b = componentes_grafo_a(portador), componentes_grafo_b(portador)
    else:
        raise TypeError(f"portador desconhecido: {type(portador).__name__}")
    a, b = _canon(a), _canon(b)
    if set(a) != set(b):
        raise AssertionError(f"referências de componentes discordam: {a} != {b}")
    return a


def fecho_referencia(portador: Portador, sementes: Iterable[int]) -> FrozenSet[int]:
    """Alcançáveis a partir das sementes por vizinhança entre pretos (sementes entram sempre),
    como referencias.fecho_ref em grades."""
    vistos = set(sementes)
    fila = deque(vistos)
    while fila:
        u = fila.popleft()
        for q in portador.vizinhos(pos(u)):
            v = indice(q)
            if portador.celula(q) and v not in vistos:
                vistos.add(v); fila.append(v)
    return frozenset(vistos)


# ---------------------------------------------------------------- adaptadores
def _impl(metodo: str, tipo_portador: type, nome_adaptador: str) -> Callable:
    """impl(ctx, portador, *args) que delega no método do portador; recusa grades e outros portadores."""
    def impl(ctx, portador, *args):
        if not isinstance(portador, tipo_portador):
            raise TypeError(f"adaptador {nome_adaptador}: {metodo} recebeu {type(portador).__name__}")
        return getattr(portador, metodo)(*args)
    impl.__name__ = f"{nome_adaptador}_{metodo}"
    return impl


@dataclass(frozen=True)
class Adaptador:
    """Substituição publicada das primitivas de portador (só estas)."""
    nome: str
    tipo_portador: type
    indefinidas: FrozenSet[str]
    descricao: Tuple[Tuple[str, str], ...]

    def impl(self, nome_primitiva: str) -> Callable:
        if nome_primitiva not in PRIMITIVAS_PORTADOR:
            raise KeyError(f"{nome_primitiva} não é primitiva de portador")
        return _impl(nome_primitiva, self.tipo_portador, self.nome)

    def definida(self, nome_primitiva: str) -> bool:
        return nome_primitiva not in self.indefinidas

    def tabela(self, tabela: Tabela, nome: Optional[str] = None) -> Tabela:
        """Cópia de `tabela` (mesmo uso) com as primitivas de portador substituídas.

        As 8 primitivas de portador entram SEMPRE (mesmo as de outra base), para que o avaliador
        nunca recorra à implementação de grades (REGISTRO_BASE) com um portador não-grade.
        Entradas de biblioteca (descobertas ou manual-teste) são mantidas sem alteração."""
        novas: List[Primitiva] = []
        for p in tabela:
            if p.nome in PRIMITIVAS_PORTADOR:
                continue
            novas.append(p)
        substitutas = []
        for nome_p in PRIMITIVAS_PORTADOR:
            orig = tabela.get(nome_p) or REGISTRO_BASE[nome_p]
            substitutas.append(Primitiva(nome_p, orig.tipo, self.impl(nome_p), orig.proveniencia, orig.generico,
                                         motivo=f"adaptador {self.nome}" +
                                                ("" if self.definida(nome_p) else " (não definida)")))
        return Tabela(nome or f"{tabela.nome}@{self.nome}", substitutas + novas, tabela.uso)

    def tabela_markdown(self) -> str:
        linhas = [f"| primitiva | {self.nome} |", "|---|---|"]
        linhas += [f"| `{p}` | {d} |" for p, d in self.descricao]
        return "\n".join(linhas)


SEQUENCIA = Adaptador(
    "sequencia", Sequencia, frozenset(),
    (("posicoes", "índices 1..m"), ("celula", "valor no índice"), ("pretas", "índices com valor 1"),
     ("vizinhos", "{i−1, i+1} dentro dos limites"), ("linhas", "lista com uma única lista: todos os índices"),
     ("colunas", "lista de singletons"), ("linhaDe", "todos os índices"), ("colunaDe", "o singleton (i)")))

GRAFO = Adaptador(
    "grafo", Grafo, frozenset({"linhas", "colunas", "linhaDe", "colunaDe"}),
    (("posicoes", "nós em ordem fixa (1..N)"), ("celula", "rótulo do nó"), ("pretas", "nós pretos"),
     ("vizinhos", "adjacência, ordem crescente"), ("linhas", "não definida"), ("colunas", "não definida"),
     ("linhaDe", "não definida"), ("colunaDe", "não definida")))

ADAPTADORES: Dict[str, Adaptador] = {"sequencia": SEQUENCIA, "grafo": GRAFO}


def adaptador_de(portador: Portador) -> Adaptador:
    for a in ADAPTADORES.values():
        if isinstance(portador, a.tipo_portador):
            return a
    raise TypeError(f"portador desconhecido: {type(portador).__name__}")


def aplicar_no_portador(termo: Termo, portador: Portador, *args, tabela: Tabela,
                        contador: Optional[Contador] = None, orcamento_passos: Optional[int] = None):
    """Avalia o termo FECHADO sem modificação sob Sem_{n_semantica(portador)}, com a tabela adaptada
    (adaptador_de(portador).tabela(tabela)), e aplica-o ao portador e aos argumentos."""
    tab = adaptador_de(portador).tabela(tabela)
    if contador is None:
        contador = Contador(orcamento_passos)
    v = avaliar(termo, n=n_semantica(portador), contador=contador, tabela=tab)
    return aplicar(v, portador, *args)
