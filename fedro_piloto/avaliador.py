"""Avaliador de Sem_n (documento 02, 2.3.1): F(n) = n⁴, listas truncadas em F(n),
fix f = f^{F(n)}(padrão), todas as funções totais.

Estratégia (fixa, determinística, parte do modelo de custo):
- chamada por valor, esquerda para a direita (função antes do argumento);
- `se@T c a b` aplicado a três argumentos avalia só o ramo escolhido (o valor denotado é o
  mesmo, pois tudo é total; muda apenas a contagem de passos);
- fix em tipo de primeira ordem: laço iterativo de exatamente F(n) aplicações;
- fix em tipo funcional: preguiçoso. O nível k é a função x ↦ (f nível_{k−1}) x, nível 0 = padrão;
  isto é f^{F(n)}(padrão) em forma eta-expandida (mesma denotação). A profundidade usada é registrada.

Contagem (Contador, determinística): `passos` += 1 por nó avaliado (constante, variável, λ,
aplicação, fix) e += 1 por aplicação saturada de primitiva; `desdobramentos_fix` conta aplicações
de f por fix; `profundidade_fix_max` é o maior nível de fix efetivamente usado.
`orcamento_passos` é um recurso da BUSCA, não da semântica: ao excedê-lo a avaliação aborta com
OrcamentoEsgotado (o candidato é descartado pelo chamador); Sem_n em si é sempre total.
Medições reais (tempo, memória) ficam em `fedro_piloto.medidas`, nunca aqui.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from typing import Dict, List, Optional

from .dsl import BOOL, GRADE, LLP, LP, POS, FUN, F, Primitiva, REGISTRO_BASE, Tabela, Termo, Tipo, padrao, truncar
from .grade import Grade

if sys.getrecursionlimit() < 200_000:
    sys.setrecursionlimit(200_000)

_SEM_LIMITE = sys.maxsize


class OrcamentoEsgotado(Exception):
    """Limite de passos do chamador excedido (recurso da busca, não da semântica)."""


class Contador:
    """Contadores determinísticos de uma avaliação (nunca contém tempo nem memória)."""
    __slots__ = ("passos", "aplicacoes_primitivas", "desdobramentos_fix", "profundidade_fix_max",
                 "orcamento_passos", "_limite")

    def __init__(self, orcamento_passos: Optional[int] = None):
        self.passos = 0
        self.aplicacoes_primitivas = 0
        self.desdobramentos_fix = 0
        self.profundidade_fix_max = 0
        self.orcamento_passos = orcamento_passos
        self._limite = _SEM_LIMITE if orcamento_passos is None else int(orcamento_passos)

    def como_dict(self) -> dict:
        return {"passos": self.passos, "aplicacoes_primitivas": self.aplicacoes_primitivas,
                "desdobramentos_fix": self.desdobramentos_fix,
                "profundidade_fix_max": self.profundidade_fix_max,
                "orcamento_passos": self.orcamento_passos}

    def __repr__(self):
        return f"Contador({self.como_dict()})"


class Contexto:
    """Estado de uma avaliação sob Sem_n: n, F(n), contador, tabela e cache de constantes."""
    __slots__ = ("n", "F", "contador", "tabela", "_cache")

    def __init__(self, n: int, contador: Optional[Contador] = None, tabela=None):
        if not 1 <= n:
            raise ValueError("n ≥ 1")
        self.n = n
        self.F = F(n)
        self.contador = contador if contador is not None else Contador()
        self.tabela = tabela
        self._cache: Dict[str, object] = {}

    def primitiva(self, nome: str) -> Primitiva:
        p = None
        if self.tabela is not None:
            p = self.tabela.get(nome)
        if p is None:
            p = REGISTRO_BASE.get(nome)
        if p is None:
            raise KeyError(f"constante desconhecida: {nome}")
        return p

    def constante(self, nome: str):
        v = self._cache.get(nome, _AUSENTE)
        if v is _AUSENTE:
            p = self.primitiva(nome)
            if p.corpo is not None:
                v = compilar(p.corpo)({}, self)
            elif p.aridade == 0:
                v = p.impl(self)
            else:
                v = _curry(p.impl, p.aridade, self)
            self._cache[nome] = v
        return v


_AUSENTE = object()


def _curry(impl, k: int, ctx: Contexto):
    c = ctx.contador

    def saturar(args):
        c.passos += 1
        c.aplicacoes_primitivas += 1
        if c.passos > c._limite:
            raise OrcamentoEsgotado(c.passos)
        return impl(ctx, *args)

    if k == 1:
        def f1(a):
            return saturar((a,))
        return f1
    if k == 2:
        def f2(a):
            def f2b(b):
                return saturar((a, b))
            return f2b
        return f2
    if k == 3:
        def f3(a):
            def f3b(b):
                def f3c(x):
                    return saturar((a, b, x))
                return f3c
            return f3b
        return f3

    def coletar(args):
        def f(x):
            novos = args + (x,)
            if len(novos) == k:
                return saturar(novos)
            return coletar(novos)
        return f
    return coletar(())


def _eh_se(nome: str) -> bool:
    return nome == "se" or nome.startswith("se@")


@lru_cache(maxsize=8192)
def compilar(t: Termo):
    """Compila um termo numa função ev(env, ctx) -> valor (env: dict var → valor)."""
    k = t[0]
    if k == "v":
        nome = t[1]

        def ev_v(env, ctx):
            c = ctx.contador
            c.passos += 1
            if c.passos > c._limite:
                raise OrcamentoEsgotado(c.passos)
            return env[nome]
        return ev_v

    if k == "c":
        nome = t[1]

        def ev_c(env, ctx):
            c = ctx.contador
            c.passos += 1
            if c.passos > c._limite:
                raise OrcamentoEsgotado(c.passos)
            return ctx.constante(nome)
        return ev_c

    if k == "lam":
        var = t[1]
        corpo = compilar(t[3])

        def ev_lam(env, ctx):
            c = ctx.contador
            c.passos += 1
            if c.passos > c._limite:
                raise OrcamentoEsgotado(c.passos)

            def clos(x):
                e2 = env.copy()
                e2[var] = x
                return corpo(e2, ctx)
            return clos
        return ev_lam

    if k == "ap":
        # espinha: cabeça e argumentos
        args = []
        u = t
        while u[0] == "ap":
            args.append(u[2])
            u = u[1]
        args.reverse()
        if u[0] == "c" and _eh_se(u[1]) and len(args) >= 3:
            return _compilar_se(u[1], args)
        f_ev = compilar(t[1])
        x_ev = compilar(t[2])

        def ev_ap(env, ctx):
            c = ctx.contador
            c.passos += 1
            if c.passos > c._limite:
                raise OrcamentoEsgotado(c.passos)
            f = f_ev(env, ctx)
            return f(x_ev(env, ctx))
        return ev_ap

    if k == "fix":
        return _compilar_fix(t[1], compilar(t[2]))

    raise ValueError(f"termo inválido: {t!r}")


def _compilar_se(nome: str, args: List[Termo]):
    cond, a, b = (compilar(x) for x in args[:3])
    resto = [compilar(x) for x in args[3:]]

    def ev_se(env, ctx):
        c = ctx.contador
        # 3 nós de aplicação + 1 nó de constante + 1 aplicação de primitiva
        c.passos += 5
        c.aplicacoes_primitivas += 1
        if c.passos > c._limite:
            raise OrcamentoEsgotado(c.passos)
        v = a(env, ctx) if cond(env, ctx) else b(env, ctx)
        for r in resto:
            c.passos += 1
            if c.passos > c._limite:
                raise OrcamentoEsgotado(c.passos)
            v = v(r(env, ctx))
        return v
    return ev_se


def _compilar_fix(tipo: Tipo, f_ev):
    if tipo[0] != "Fun":
        def ev_fix1(env, ctx):
            c = ctx.contador
            c.passos += 1
            if c.passos > c._limite:
                raise OrcamentoEsgotado(c.passos)
            f = f_ev(env, ctx)
            v = padrao(tipo, ctx.n)
            Fn = ctx.F
            for _ in range(Fn):
                c.desdobramentos_fix += 1
                v = f(v)
            if Fn > c.profundidade_fix_max:
                c.profundidade_fix_max = Fn
            return v
        return ev_fix1

    def ev_fix(env, ctx):
        c = ctx.contador
        c.passos += 1
        if c.passos > c._limite:
            raise OrcamentoEsgotado(c.passos)
        f = f_ev(env, ctx)
        Fn = ctx.F
        pad = padrao(tipo, ctx.n)

        def nivel(k):
            if k == 0:
                return pad
            prof = Fn - k + 1

            def chamada(x):
                c.desdobramentos_fix += 1
                if prof > c.profundidade_fix_max:
                    c.profundidade_fix_max = prof
                return f(nivel(k - 1))(x)
            return chamada
        return nivel(Fn)
    return ev_fix


def avaliar(termo: Termo, env: Optional[dict] = None, n: int = 3, contador: Optional[Contador] = None,
            tabela: Optional[Tabela] = None, orcamento_passos: Optional[int] = None):
    """Valor de `termo` sob Sem_n no ambiente `env` (var → valor).

    Valores: bool; Pos = (i, j); Grade; listas = tuplas; funções = callables de um argumento.
    `tabela` resolve constantes de biblioteca (corpo); primitivas de base vêm de REGISTRO_BASE.
    Se `orcamento_passos` é dado (e `contador` não), cria um Contador com esse limite.
    """
    if contador is None:
        contador = Contador(orcamento_passos)
    ctx = Contexto(n, contador, tabela)
    return compilar(termo)(dict(env or {}), ctx)


def aplicar(valor, *args):
    for a in args:
        valor = valor(a)
    return valor


# =====================================================================
# Bateria fixa de valores por tipo (para testes de implementação; não é prova)
# =====================================================================
def _ciclar(base: tuple, comprimento: int) -> tuple:
    if not base:
        return ()
    out = []
    while len(out) < comprimento:
        out.extend(base)
    return tuple(out[:comprimento])


def amostras_de_tipo(tipo: Tipo, g: Grade, todas_posicoes: bool = True) -> list:
    """Valores de amostra determinísticos para `tipo`, dependentes da grade g (lado n)."""
    n = g.n
    Fn = F(n)
    pos = tuple(g.posicoes())
    pretas = tuple(g.pretas())
    brancas = tuple(p for p in pos if not g.celula(p))
    linhas = tuple(tuple(l) for l in g.linhas())
    colunas = tuple(tuple(c) for c in g.colunas())
    canto = (1, 1)

    def tr(x):
        return truncar(x, Fn)

    if tipo == BOOL:
        return [False, True]
    if tipo == POS:
        if todas_posicoes or n <= 3:
            return list(pos)
        return sorted({(1, 1), (1, n), (n, 1), (n, n), ((n + 1) // 2, (n + 1) // 2)})
    if tipo == GRADE:
        return [g]
    if tipo == LP:
        cands = [(), pos, pretas, brancas, pos[::-1], (pos[-1], pos[0], pos[-1]),
                 _ciclar(pos, Fn), _ciclar(pos, max(Fn - 1, 0))]
        return _unicos([tr(x) for x in cands])  # domínio de Sem_n: comprimento ≤ F(n)
    if tipo == LLP:
        cands = [(), linhas, colunas, (pretas,), (pretas, (), brancas), _ciclar(linhas, Fn)]
        return _unicos([tr(x) for x in cands])
    # funções
    if tipo == FUN(POS, BOOL):
        return [lambda p: g.celula(p) == 1, lambda p: g.celula(p) == 0, lambda p: False,
                lambda p: True, lambda p: p == canto]
    if tipo == FUN(POS, LP):
        return [lambda p: tuple(g.vizinhos(p)), lambda p: (p,), lambda p: (), lambda p: _ciclar(pos, Fn)]
    if tipo == FUN(LP, BOOL):
        return [lambda l: len(l) == 0, lambda l: canto in l, lambda l: True]
    if tipo == FUN(LP, LP):
        return [lambda l: l, lambda l: l[1:], lambda l: l[::-1], lambda l: tr((canto,) + l), lambda l: ()]
    if tipo == FUN(POS, LP, LP):
        return [lambda x: lambda a: tr((x,) + a), lambda x: lambda a: a[1:], lambda x: lambda a: a,
                lambda x: lambda a: tr((x,) + a) if g.celula(x) else a]
    if tipo == FUN(POS, BOOL, BOOL):
        return [lambda x: lambda b: b or g.celula(x) == 1, lambda x: lambda b: b and g.celula(x) == 1,
                lambda x: lambda b: not b]
    if tipo == FUN(POS, LLP, LLP):
        return [lambda x: lambda a: tr(((x,),) + a), lambda x: lambda a: a[1:]]
    if tipo == FUN(LP, BOOL, BOOL):
        return [lambda l: lambda b: b or len(l) == 0, lambda l: lambda b: not b]
    if tipo == FUN(LP, LP, LP):
        return [lambda l: lambda a: tr(l + a), lambda l: lambda a: l, lambda l: lambda a: a[1:]]
    if tipo == FUN(LP, LLP, LLP):
        return [lambda l: lambda a: tr((l,) + a), lambda l: lambda a: a]
    if tipo[0] == "Fun":
        # genérico: funções constantes nos dois primeiros valores do contradomínio
        res = amostras_de_tipo(tipo[2], g, todas_posicoes=False)[:2]
        return [(lambda v: (lambda _x: v))(v) for v in res]
    raise ValueError(f"sem amostras para o tipo {tipo!r}")


def _unicos(cands):
    out = []
    for c in cands:
        if c not in out:
            out.append(c)
    return out
