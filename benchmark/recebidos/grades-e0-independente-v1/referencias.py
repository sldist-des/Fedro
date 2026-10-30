"""Referências do benchmark "grades-e0-independente" (versão 1).

REFERENCIAS   : implementação principal de cada tarefa, escrita sobre a API de Grade (contrato §1.3).
REFERENCIAS_B : segunda implementação, escrita de outra maneira (aritmética de índices sobre g.bits,
                varrimentos explícitos, union-find, etc.), para conferência cruzada.
POSITIVOS     : geradores de positivos para os predicados cujos positivos são raros em n grande.

Todas as funções são puras, determinísticas e totais em qualquer grade 1 <= n <= 9 e em quaisquer
listas de posições válidas da grade (não só nas da bateria). Listas de posições chegam como tuplas.
"""
from grade import Grade


# =====================================================================================
# utilitários comuns (puros)
# =====================================================================================
def _componente(g, inicio):
    """Componente 4-conexo de células pretas que contém `inicio` (vazio se `inicio` é branca)."""
    if not g.celula(inicio):
        return set()
    vistos = {inicio}
    fila = [inicio]
    while fila:
        p = fila.pop()
        for q in g.vizinhos(p):
            if q not in vistos and g.celula(q):
                vistos.add(q)
                fila.append(q)
    return vistos


def _linha_de(g, p):
    return [q for q in g.posicoes() if q[0] == p[0]]


def _coluna_de(g, p):
    return [q for q in g.posicoes() if q[1] == p[1]]


# =====================================================================================
# REFERENCIAS (implementação A)
# =====================================================================================
# ---- Grade -> L Pos
def ultima_linha(g):
    return list(g.linhas()[-1])


def pretas_por_colunas(g):
    return [p for c in g.colunas() for p in c if g.celula(p)]


def pretas_ordem_inversa(g):
    return list(reversed(g.pretas()))


def colunas_brancas(g):
    return [p for c in g.colunas() if not any(g.celula(q) for q in c) for p in c]


def borda_preta(g):
    return [p for p in g.pretas() if any(not g.celula(q) for q in g.vizinhos(p))]


# ---- L Pos -> L Pos -> Bool
def contido_em(A, B):
    return set(A) <= set(B)


def mesmo_conjunto(A, B):
    return set(A) == set(B)


# ---- L Pos -> L Pos -> L Pos
def intersecao_ordenada(A, B):
    return [x for x in A if x in B]


def diferenca_simetrica(A, B):
    return set(A) ^ set(B)


def juntar_sem_repetir(A, B):
    return list(B) + [x for x in A if x not in B]


# ---- Grade -> Pos -> L Pos
def vizinhos_pretos(g, p):
    return {q for q in g.vizinhos(p) if g.celula(q)}


def linha_da_posicao(g, p):
    return [l for l in g.linhas() if p in l][0]


def cruz_da_posicao(g, p):
    return set(_linha_de(g, p)) | set(_coluna_de(g, p))


def componente_de(g, p):
    return _componente(g, p)


# ---- Grade -> Pos -> Bool
def na_borda(g, p):
    return p[0] in (1, g.n) or p[1] in (1, g.n)


def linha_tem_preta_em(g, p):
    return any(g.celula(q) for q in _linha_de(g, p))


# ---- Grade -> L Pos -> Bool
def contem_todas_pretas(g, S):
    return all(p in S for p in g.pretas())


def toca_preta(g, S):
    return any(g.celula(r) for q in S for r in g.vizinhos(q))


# ---- Grade -> L Pos -> L Pos
def complemento_de(g, S):
    return [p for p in g.posicoes() if p not in S]


def brancas_da_lista(g, S):
    return [q for q in S if not g.celula(q)]


def vizinhanca_externa(g, S):
    return {r for q in S for r in g.vizinhos(q) if g.celula(r) and r not in S}


# ---- Grade -> Bool
def toda_linha_tem_preta(g):
    return all(any(g.celula(p) for p in l) for l in g.linhas())


def coluna_vazia(g):
    return any(all(not g.celula(p) for p in c) for c in g.colunas())


def alguma_linha_cheia(g):
    return any(all(g.celula(p) for p in l) for l in g.linhas())


def sem_preta_isolada(g):
    return all(any(g.celula(q) for q in g.vizinhos(p)) for p in g.pretas())


def sem_pretas_adjacentes(g):
    return all(not g.celula(q) for p in g.pretas() for q in g.vizinhos(p))


def pretas_em_domino(g):
    return all(sum(1 for q in g.vizinhos(p) if g.celula(q)) == 1 for p in g.pretas())


def pretas_conexas(g):
    pr = g.pretas()
    if not pr:
        return True
    return len(_componente(g, pr[0])) == len(pr)


REFERENCIAS = {
    "ultimaLinha": ultima_linha,
    "contidoEm": contido_em,
    "vizinhosPretos": vizinhos_pretos,
    "todaLinhaTemPreta": toda_linha_tem_preta,
    "complementoDe": complemento_de,
    "pretasPorColunas": pretas_por_colunas,
    "intersecaoOrdenada": intersecao_ordenada,
    "contemTodasPretas": contem_todas_pretas,
    "colunaVazia": coluna_vazia,
    "naBorda": na_borda,
    "linhaDaPosicao": linha_da_posicao,
    "juntarSemRepetir": juntar_sem_repetir,
    "brancasDaLista": brancas_da_lista,
    "diferencaSimetrica": diferenca_simetrica,
    "pretasOrdemInversa": pretas_ordem_inversa,
    "algumaLinhaCheia": alguma_linha_cheia,
    "linhaTemPretaEm": linha_tem_preta_em,
    "semPretaIsolada": sem_preta_isolada,
    "colunasBrancas": colunas_brancas,
    "mesmoConjunto": mesmo_conjunto,
    "tocaPreta": toca_preta,
    "bordaPreta": borda_preta,
    "vizinhancaExterna": vizinhanca_externa,
    "semPretasAdjacentes": sem_pretas_adjacentes,
    "cruzDaPosicao": cruz_da_posicao,
    "pretasEmDomino": pretas_em_domino,
    "pretasConexas": pretas_conexas,
    "componenteDe": componente_de,
}


# =====================================================================================
# REFERENCIAS_B (implementação B: índices sobre g.bits, sem reutilizar o código de A)
# =====================================================================================
def _b(g, i, j):
    """bit da célula (i, j), 1-based; 0 fora da grade."""
    n = g.n
    if 1 <= i <= n and 1 <= j <= n:
        return g.bits[(i - 1) * n + (j - 1)]
    return 0


def _viz_b(g, i, j):
    n = g.n
    return [(a, b) for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if 1 <= a <= n and 1 <= b <= n]


def _pretas_b(g):
    n = g.n
    return [(k // n + 1, k % n + 1) for k, v in enumerate(g.bits) if v]


def _rotulos_uf(g):
    """union-find sobre as pretas; devolve dicionário posição -> raiz."""
    n = g.n
    pai = {}

    def raiz(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x
    for p in _pretas_b(g):
        pai[p] = p
    for (i, j) in list(pai):
        for (a, b) in ((i + 1, j), (i, j + 1)):
            if a <= n and b <= n and (a, b) in pai:
                ra, rb = raiz((i, j)), raiz((a, b))
                if ra != rb:
                    pai[max(ra, rb)] = min(ra, rb)
    return {p: raiz(p) for p in pai}


def _b_ultima_linha(g):
    return [(g.n, j) for j in range(1, g.n + 1)]


def _b_pretas_por_colunas(g):
    n = g.n
    return [(i, j) for j in range(1, n + 1) for i in range(1, n + 1) if _b(g, i, j)]


def _b_pretas_ordem_inversa(g):
    n = g.n
    return [(k // n + 1, k % n + 1) for k in range(n * n - 1, -1, -1) if g.bits[k]]


def _b_colunas_brancas(g):
    n = g.n
    out = []
    for j in range(1, n + 1):
        if sum(_b(g, i, j) for i in range(1, n + 1)) == 0:
            out.extend((i, j) for i in range(1, n + 1))
    return out


def _b_borda_preta(g):
    out = []
    for (i, j) in _pretas_b(g):
        if sum(_b(g, a, b) for a, b in _viz_b(g, i, j)) < len(_viz_b(g, i, j)):
            out.append((i, j))
    return out


def _b_contido_em(A, B):
    return all(x in B for x in A)


def _b_mesmo_conjunto(A, B):
    return all(x in B for x in A) and all(y in A for y in B)


def _b_intersecao_ordenada(A, B):
    sb = frozenset(B)
    return list(filter(lambda x: x in sb, A))


def _b_diferenca_simetrica(A, B):
    return frozenset([x for x in A if x not in B] + [y for y in B if y not in A])


def _b_juntar_sem_repetir(A, B):
    out = list(B)
    vistos = set(B)
    for x in A:
        if x not in vistos:
            out.append(x)
    return out


def _b_vizinhos_pretos(g, p):
    i, j = p
    return frozenset((a, b) for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if _b(g, a, b))


def _b_linha_da_posicao(g, p):
    return [(p[0], j) for j in range(1, g.n + 1)]


def _b_cruz_da_posicao(g, p):
    n = g.n
    return frozenset([(p[0], j) for j in range(1, n + 1)] + [(i, p[1]) for i in range(1, n + 1)])


def _b_componente_de(g, p):
    if not _b(g, p[0], p[1]):
        return frozenset()
    rot = _rotulos_uf(g)
    r = rot[p]
    return frozenset(q for q, rq in rot.items() if rq == r)


def _b_na_borda(g, p):
    return len(_viz_b(g, p[0], p[1])) < 4


def _b_linha_tem_preta_em(g, p):
    n = g.n
    return sum(g.bits[(p[0] - 1) * n:(p[0]) * n]) > 0


def _b_contem_todas_pretas(g, S):
    return set(_pretas_b(g)) - set(S) == set()


def _b_toca_preta(g, S):
    for (i, j) in S:
        if _b(g, i - 1, j) or _b(g, i + 1, j) or _b(g, i, j - 1) or _b(g, i, j + 1):
            return True
    return False


def _b_complemento_de(g, S):
    n = g.n
    s = set(S)
    return [(k // n + 1, k % n + 1) for k in range(n * n) if (k // n + 1, k % n + 1) not in s]


def _b_brancas_da_lista(g, S):
    return [q for q in S if _b(g, q[0], q[1]) == 0]


def _b_vizinhanca_externa(g, S):
    s = set(S)
    out = set()
    for (i, j) in S:
        for (a, b) in _viz_b(g, i, j):
            if _b(g, a, b) and (a, b) not in s:
                out.add((a, b))
    return frozenset(out)


def _b_toda_linha_tem_preta(g):
    n = g.n
    return all(sum(g.bits[k * n:(k + 1) * n]) > 0 for k in range(n))


def _b_coluna_vazia(g):
    n = g.n
    return any(sum(g.bits[j::n]) == 0 for j in range(n))


def _b_alguma_linha_cheia(g):
    n = g.n
    return any(sum(g.bits[k * n:(k + 1) * n]) == n for k in range(n))


def _b_contar_viz_pretos(g, i, j):
    return _b(g, i - 1, j) + _b(g, i + 1, j) + _b(g, i, j - 1) + _b(g, i, j + 1)


def _b_sem_preta_isolada(g):
    return all(_b_contar_viz_pretos(g, i, j) >= 1 for (i, j) in _pretas_b(g))


def _b_sem_pretas_adjacentes(g):
    n = g.n
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if _b(g, i, j) and (_b(g, i, j + 1) or _b(g, i + 1, j)):
                return False
    return True


def _b_pretas_em_domino(g):
    return all(_b_contar_viz_pretos(g, i, j) == 1 for (i, j) in _pretas_b(g))


def _b_pretas_conexas(g):
    return len(set(_rotulos_uf(g).values())) <= 1


REFERENCIAS_B = {
    "ultimaLinha": _b_ultima_linha,
    "contidoEm": _b_contido_em,
    "vizinhosPretos": _b_vizinhos_pretos,
    "todaLinhaTemPreta": _b_toda_linha_tem_preta,
    "complementoDe": _b_complemento_de,
    "pretasPorColunas": _b_pretas_por_colunas,
    "intersecaoOrdenada": _b_intersecao_ordenada,
    "contemTodasPretas": _b_contem_todas_pretas,
    "colunaVazia": _b_coluna_vazia,
    "naBorda": _b_na_borda,
    "linhaDaPosicao": _b_linha_da_posicao,
    "juntarSemRepetir": _b_juntar_sem_repetir,
    "brancasDaLista": _b_brancas_da_lista,
    "diferencaSimetrica": _b_diferenca_simetrica,
    "pretasOrdemInversa": _b_pretas_ordem_inversa,
    "algumaLinhaCheia": _b_alguma_linha_cheia,
    "linhaTemPretaEm": _b_linha_tem_preta_em,
    "semPretaIsolada": _b_sem_preta_isolada,
    "colunasBrancas": _b_colunas_brancas,
    "mesmoConjunto": _b_mesmo_conjunto,
    "tocaPreta": _b_toca_preta,
    "bordaPreta": _b_borda_preta,
    "vizinhancaExterna": _b_vizinhanca_externa,
    "semPretasAdjacentes": _b_sem_pretas_adjacentes,
    "cruzDaPosicao": _b_cruz_da_posicao,
    "pretasEmDomino": _b_pretas_em_domino,
    "pretasConexas": _b_pretas_conexas,
    "componenteDe": _b_componente_de,
}


# =====================================================================================
# POSITIVOS: geradores (n, rng) -> Grade de lado n (o rótulo é sempre conferido pela referência)
# =====================================================================================
def _pos_sem_adjacentes(n, rng):
    """Coloca pretas ao acaso, recusando as que tocariam numa preta já posta."""
    p = rng.choice((0.2, 0.35, 0.5, 0.65))
    bits = [0] * (n * n)
    ordem = list(range(n * n))
    rng.shuffle(ordem)
    for k in ordem:
        if rng.random() >= p:
            continue
        i, j = divmod(k, n)
        livre = True
        for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            if 0 <= a < n and 0 <= b < n and bits[a * n + b]:
                livre = False
        if livre:
            bits[k] = 1
    return Grade(n, tuple(bits))


def _pos_domino(n, rng):
    """Coloca dominós (pares de pretas vizinhas) sem que toquem noutras pretas."""
    if n < 2:
        return None
    bits = [0] * (n * n)
    tentativas = rng.randint(1, max(1, (n * n) // 3))
    for _ in range(tentativas):
        i, j = rng.randrange(n), rng.randrange(n)
        di, dj = rng.choice(((0, 1), (1, 0)))
        a, b = i + di, j + dj
        if a >= n or b >= n:
            continue
        celulas = ((i, j), (a, b))
        ok = True
        for (x, y) in celulas:
            if bits[x * n + y]:
                ok = False
            for (u, v) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= u < n and 0 <= v < n and (u, v) not in celulas and bits[u * n + v]:
                    ok = False
        if ok:
            for (x, y) in celulas:
                bits[x * n + y] = 1
    return Grade(n, tuple(bits))


def _pos_conexas(n, rng):
    """Cresce uma região conexa a partir de uma célula, até um tamanho sorteado."""
    alvo = rng.randint(1, n * n)
    i, j = rng.randrange(n), rng.randrange(n)
    regiao = {(i, j)}
    fronteira = [(i, j)]
    while len(regiao) < alvo and fronteira:
        x, y = rng.choice(fronteira)
        viz = [(u, v) for (u, v) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
               if 0 <= u < n and 0 <= v < n and (u, v) not in regiao]
        if not viz:
            fronteira.remove((x, y))
            continue
        c = rng.choice(viz)
        regiao.add(c)
        fronteira.append(c)
    return Grade(n, tuple(1 if (k // n, k % n) in regiao else 0 for k in range(n * n)))


POSITIVOS = {
    "semPretasAdjacentes": _pos_sem_adjacentes,
    "pretasEmDomino": _pos_domino,
    "pretasConexas": _pos_conexas,
}
