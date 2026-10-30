"""Referências do pacote de exemplo (ilustração de formato). Cada função recebe os argumentos na
ordem do tipo declarado e devolve um valor do tipo de resultado: bool, posição (i, j) ou coleção de
posições. Só pode usar a API de Grade descrita no contrato."""


def primeira_celula_preta(g):
    return bool(g.celula((1, 1)))


def eh_canto(g, p):
    n = g.n
    return p in {(1, 1), (1, n), (n, 1), (n, n)}


def identidade(g, S):
    return frozenset(S)


REFERENCIAS = {"primeiraCelulaPreta": primeira_celula_preta, "ehCanto": eh_canto, "identidade": identidade}

# segunda implementação independente (recomendada): o validador confere que coincide com REFERENCIAS
REFERENCIAS_B = {
    "primeiraCelulaPreta": lambda g: g.bits[0] == 1,
    "ehCanto": lambda g, p: p[0] in (1, g.n) and p[1] in (1, g.n),
    "identidade": lambda g, S: frozenset(S),
}

# gerador opcional de positivos para predicados raros na mistura natural: (n, rng) -> Grade ou None
# (aqui desnecessário, o predicado é equilibrado; fica como ilustração do formato)
def _positivo_primeira_celula(n, rng):
    from grade import Grade
    bits = [1 if rng.random() < 0.4 else 0 for _ in range(n * n)]
    bits[0] = 1
    return Grade(n, tuple(bits))


POSITIVOS = {"primeiraCelulaPreta": _positivo_primeira_celula}
