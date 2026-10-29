"""Grades binárias n×n, posições 1-based, serialização, hash e partição por instância."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Iterable, List, Tuple

Pos = Tuple[int, int]


@dataclass(frozen=True)
class Grade:
    n: int
    bits: Tuple[int, ...]  # ordem linha a linha, valores 0/1

    def __post_init__(self):
        if len(self.bits) != self.n * self.n:
            raise ValueError("bits incompatíveis com n")
        if any(b not in (0, 1) for b in self.bits):
            raise ValueError("bits devem ser 0/1")

    # ---- construção ----
    @staticmethod
    def de_linhas(linhas: Iterable[Iterable[int]]) -> "Grade":
        linhas = [list(l) for l in linhas]
        n = len(linhas)
        return Grade(n, tuple(int(b) for l in linhas for b in l))

    @staticmethod
    def de_texto(txt: str) -> "Grade":
        """'n:bits' ou linhas separadas por '/' com caracteres 0/1 ou ./#."""
        if ":" in txt:
            n, bits = txt.split(":")
            return Grade(int(n), tuple(int(c) for c in bits))
        linhas = [[1 if c in "1#" else 0 for c in l] for l in txt.split("/")]
        return Grade.de_linhas(linhas)

    @staticmethod
    def vazia(n: int) -> "Grade":
        return Grade(n, tuple([0] * (n * n)))

    # ---- acesso ----
    def celula(self, p: Pos) -> int:
        i, j = p
        return self.bits[(i - 1) * self.n + (j - 1)]

    def posicoes(self) -> List[Pos]:
        n = self.n
        return [(i, j) for i in range(1, n + 1) for j in range(1, n + 1)]

    def pretas(self) -> List[Pos]:
        return [p for p in self.posicoes() if self.celula(p)]

    def linhas(self) -> List[List[Pos]]:
        n = self.n
        return [[(i, j) for j in range(1, n + 1)] for i in range(1, n + 1)]

    def colunas(self) -> List[List[Pos]]:
        n = self.n
        return [[(i, j) for i in range(1, n + 1)] for j in range(1, n + 1)]

    def vizinhos(self, p: Pos) -> List[Pos]:
        i, j = p
        n = self.n
        out = []
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):  # cima, baixo, esquerda, direita
            a, b = i + di, j + dj
            if 1 <= a <= n and 1 <= b <= n:
                out.append((a, b))
        return out

    def dentro(self, p: Pos) -> bool:
        return 1 <= p[0] <= self.n and 1 <= p[1] <= self.n

    def contagem_pretas(self) -> int:
        return sum(self.bits)

    def densidade(self) -> float:
        return self.contagem_pretas() / (self.n * self.n)

    # ---- serialização ----
    def serializar(self) -> str:
        return f"{self.n}:{''.join(str(b) for b in self.bits)}"

    def hash_hex(self) -> str:
        return hashlib.sha256(self.serializar().encode("ascii")).hexdigest()

    def balde(self, k: int = 100) -> int:
        """Partição determinística por instância: inteiro em [0, k) derivado do hash."""
        return int(self.hash_hex()[:16], 16) % k

    def texto(self) -> str:
        n = self.n
        return "/".join("".join("#" if self.bits[i * n + j] else "." for j in range(n)) for i in range(n))

    # ---- transformações ----
    def com_bits(self, bits: Iterable[int]) -> "Grade":
        return Grade(self.n, tuple(bits))

    def transposta(self) -> "Grade":
        n = self.n
        return Grade(n, tuple(self.bits[j * n + i] for i in range(n) for j in range(n)))

    def reflexao_h(self) -> "Grade":  # espelha colunas (esquerda<->direita)
        n = self.n
        return Grade(n, tuple(self.bits[i * n + (n - 1 - j)] for i in range(n) for j in range(n)))

    def reflexao_v(self) -> "Grade":  # espelha linhas (cima<->baixo)
        n = self.n
        return Grade(n, tuple(self.bits[(n - 1 - i) * n + j] for i in range(n) for j in range(n)))

    def rotacao90(self) -> "Grade":
        return self.transposta().reflexao_h()

    def inverter(self, p: Pos) -> "Grade":
        i, j = p
        k = (i - 1) * self.n + (j - 1)
        bits = list(self.bits)
        bits[k] ^= 1
        return Grade(self.n, tuple(bits))

    def trocar(self, p: Pos, q: Pos) -> "Grade":
        a = (p[0] - 1) * self.n + (p[1] - 1)
        b = (q[0] - 1) * self.n + (q[1] - 1)
        bits = list(self.bits)
        bits[a], bits[b] = bits[b], bits[a]
        return Grade(self.n, tuple(bits))


def todas_as_grades(n: int):
    """Enumeração exaustiva das 2^(n²) grades, em ordem lexicográfica do vetor linha a linha."""
    total = n * n
    for k in range(1 << total):
        bits = tuple((k >> (total - 1 - t)) & 1 for t in range(total))
        yield Grade(n, bits)


def chave_minimalidade(g: Grade) -> Tuple[int, int, Tuple[int, ...]]:
    """Ordem (n, número de pretas, lexicográfica) usada pelo oráculo."""
    return (g.n, g.contagem_pretas(), g.bits)
