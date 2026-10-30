"""Enumerador tipado ascendente com poda por equivalência observacional (OE), contagem exata de
termos por programação dinâmica e busca de tarefa (documento 02, 2.3-2.5; documento 03, 2.4,
PQ5-PQ7, PM7-PM9, U19-U20).

GRAMÁTICA G(tabela, Γ0, T, D, β) — a MESMA para contar_termos, enumerar_sem_poda e Enumerador.
Contexto = Γ0 (variáveis livres dadas, com nomes do chamador) + binders de λ com nomes
canônicos x0, x1, ... (x_d é o binder na profundidade d). N_Γ(τ, s) = termos de tipo τ, tamanho s:
  folha    constante da tabela de tipo τ, ou variável de Γ de tipo τ             (s = 1)
  aplic.   f a, f ∈ N_Γ(α→τ, s1), a ∈ N_Γ(α, s2), s1 + s2 = s, para todo α com α ∈ T e α→τ ∈ T;
           sem redexes β (omissão, redexes_beta=False): f nunca é uma λ
  λ        λx_d:α. c, c ∈ N_{Γ,x_d:α}(β, s − 1), se τ = α→β e d < D
  fix      fix_τ (λrec:τ. λx_d:α1 ... λx_{d+k−1}:αk. c), c ∈ R(β, s − 2 − k), se τ = α1→…→αk→β
           (k ≥ 1, β não funcional), τ ∈ T e d + k ≤ D
R(σ, s) (termos que CONTÊM rec, rec : τ; "rec-profundidade 1": argumentos de rec não contêm rec):
  S (espinhas)  rec (s = 1, σ = τ) | f a com f ∈ S(α→σ), a ∈ N(α)
  O (as demais) f a com f ∈ O(α→σ) não-λ, a ∈ N ∪ R(α) | f ∈ N(α→σ) não-λ, a ∈ R(α) |
                λx_d:α. c, c ∈ R(β)
Decisões da gramática (documentadas, iguais nos três algoritmos):
  * T (tipos admitidos) = dsl.UNIVERSO_TIPOS ∪ subtipos(tabela, tipo-alvo, Γ0) por omissão: o
    MESMO universo em E0, E0', E0+ (o cálculo λ é comum; só as constantes mudam).
  * D = profundidade_lambda (omissão 2) limita o aninhamento de binders x_d (inclui os x de fix;
    não inclui rec nem Γ0). Ex.: λg. algum (λp. …) usa 2; fix de aridade 2 no topo usa 2.
  * Redexes β ((λx. c) a) excluídos por omissão: c[a/x] tem tamanho ≤ |c| − 1 + |a| quando x ocorre
    no máximo uma vez, logo nada se perde nesse caso; quando x ocorre ≥ 2 vezes (um "let") o redex
    pode ser menor que a forma normal e a exclusão pode aumentar o tamanho mínimo de uma classe.
    redexes_beta=True restaura a gramática literal (contagens: contar_termos(..., redexes_beta=True)).
  * Formas não η-longas (p. ex. `celula g` como Pos → Bool) e η-redexes são termos da gramática;
    os η-redexes λx. f x são descartados pela poda OE (equivalentes a f, menor).
  * fix só em tipos funcionais e só na forma η-longa acima, com rec ocorrendo ≥ 1 vez (sem rec,
    fix (λrec. λx. c) ≡ λx. c, maior em 2). fix em tipo de primeira ordem (permitido pela
    gramática do documento 02) NÃO é enumerado: desvio registrado.
  * fix aninhado é permitido em subtermos sem rec (o rec interno sombreia o externo).

PODA OE. Assinatura de um termo de Γ = tupla, sobre os mundos de amostra de Γ, do seu valor; para
tipo funcional, aplicado às amostras do tipo do argumento (recursivamente). Os mundos da raiz vêm
APENAS de grades da partição oraculo_treino (verificado; grades_amostra_oe). Mundos de Γ,x:α =
(mundo, a) com a nas amostras de α para a grade do mundo. Mantém-se o primeiro (menor)
representante por classe e por (Γ, τ). A assinatura de λx.c, c não funcional, é a de c reagrupada
por mundo (sem avaliar). Níveis de amostragem: binders Pos, listas e funções multiplicam os mundos
e sobem um nível; o contexto de nível k ≥ 1 só usa mundos vindos dos K_k primeiros mundos-raiz
(mundos_funcao). Dentro de cada contexto todas as assinaturas usam todos os seus mundos; a
aproximação fica na fronteira entre níveis (um corpo deduplicado em menos mundos que o pai).
Exatidão: amostras de Bool e Pos (todas as posições) são exaustivas e a de Grade é a própria grade;
para argumentos lista ou função as amostras são finitas e a poda é aproximada (poda_inexata=False a
desliga nesses tipos). Tipos funcionais: deduplicação em dois estágios EXATA (chave rápida nos
M_RAPIDA primeiros mundos; assinatura completa só quando a chave colide).
Corpos de fix: rec livre impede assinatura; termos R são construídos sem poda a partir dos
representantes OE dos subtermos sem rec (do contexto Γ,x1..xk), e só o termo fix completo é
deduplicado. Limitação: os x de fix recebem, na recursão, valores fora das amostras (p. ex. caudas),
logo a poda dos subtermos sem rec dentro do corpo pode perder classes de fix.
Limitação da partição [C]: nenhuma grade de oraculo_treino com n ≤ 4 tem uma única preta em (1,1);
`algum@P (celula g) (cauda@P (posicoes g))` e `nao (vazia?@P (pretas g))` coincidem em todas elas e
diferem em #../.../... — nenhuma amostra OE admissível separa essas classes.

CUSTO. ContadorEnumeracao e ContadorBusca são determinísticos (candidatos, passos, tamanhos de
tabela); tempo e memória de pico ficam em medidas.MedicaoReal, sempre em campo separado.
"""
from __future__ import annotations

import re
import sys
from dataclasses import asdict, dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from .avaliador import Contador, Contexto, OrcamentoEsgotado, amostras_de_tipo, aplicar, compilar
from .dsl import (BOOL, GRADE, LP, POS, FUN, UNIVERSO_TIPOS, C, FIX, LAM, LAMS, V, ErroProveniencia,
                  Tabela, Termo, Tipo, argumentos_e_resultado, exigir_tabela_de_descoberta,
                  subtipos, tipo_sexpr, tipo_str, tipo_valido, truncar, F)
from .grade import Grade
from .medidas import medir

REC = "rec"
#: mundos da chave rápida da deduplicação em dois estágios de tipos funcionais
M_RAPIDA = 4
PARTICAO_OE = "oraculo_treino"
_NOME_CANONICO = re.compile(r"^x\d+$")
TIPOS_EXATOS = frozenset({BOOL, POS, GRADE})


def nome_var(d: int) -> str:
    """Nome canônico do binder na profundidade d."""
    return f"x{d}"


# =====================================================================
# Gramática comum
# =====================================================================
def _normalizar_contexto(contexto) -> Tuple[Tuple[str, Tipo], ...]:
    if contexto is None:
        return ()
    itens = list(contexto.items()) if isinstance(contexto, dict) else list(contexto)
    for nome, t in itens:
        if not tipo_valido(t):
            raise ValueError(f"tipo inválido para {nome}: {t!r}")
        if nome == REC or _NOME_CANONICO.match(nome):
            raise ValueError(f"nome reservado no contexto: {nome}")
    if len({n for n, _ in itens}) != len(itens):
        raise ValueError("nomes repetidos no contexto")
    return tuple(itens)


class Gramatica:
    """Regras da gramática G (ver docstring do módulo), partilhadas pelos três algoritmos."""

    def __init__(self, tabela: Tabela, contexto=None, tipo_alvo: Optional[Tipo] = None,
                 profundidade_lambda: int = 2, tipos: Optional[Iterable[Tipo]] = None, fix: bool = True,
                 redexes_beta: bool = False, custos_folha: Optional[Dict[str, int]] = None):
        self.tabela = tabela
        self.beta = bool(redexes_beta)
        # CUSTO PONDERADO (documento 05, missão 4): custo inteiro >= 1 por constante; omissão 1 = tamanho.
        # Só o Enumerador (poda OE) usa custos; contar_termos e enumerar_sem_poda ficam em tamanho.
        self.custos: Dict[str, int] = {}
        for nome, c in (custos_folha or {}).items():
            if not isinstance(c, int) or isinstance(c, bool) or c < 1:
                raise ValueError(f"custo de folha inválido para {nome}: {c!r}")
            self.custos[nome] = c
        self.custo_max_folha = max([1] + list(self.custos.values()))
        self.gamma0 = _normalizar_contexto(contexto)
        self.D = int(profundidade_lambda)
        self.fix = bool(fix)
        for nome, _ in self.gamma0:
            if nome in tabela:
                raise ValueError(f"variável {nome} sombreia constante da tabela")
        extras = [t for _, t in self.gamma0] + ([tipo_alvo] if tipo_alvo else []) + [p.tipo for p in tabela]
        T = set(UNIVERSO_TIPOS if tipos is None else tipos)
        for t in extras:
            T |= subtipos(t)
        for t in list(T):
            T |= subtipos(t)
        self.T = frozenset(T)
        self.ordem_T = sorted(self.T, key=tipo_sexpr)
        self._consts: Dict[Tipo, List[str]] = {}
        for p in tabela:
            self._consts.setdefault(p.tipo, []).append(p.nome)
        self._args: Dict[Tipo, List[Tipo]] = {
            t: [a for a in self.ordem_T if FUN(a, t) in self.T] for t in self.ordem_T}

    def chave_tipos(self) -> tuple:
        return (tuple(sorted(tipo_sexpr(t) for t in self.T)), self.D, self.fix, self.beta)

    def variaveis(self, ctx: Tuple[Tipo, ...]) -> List[Tuple[str, Tipo]]:
        return list(self.gamma0) + [(nome_var(i), t) for i, t in enumerate(ctx)]

    def folhas(self, ctx: Tuple[Tipo, ...], tau: Tipo) -> List[Termo]:
        out = [C(c) for c in self._consts.get(tau, [])]
        out += [V(v) for v, t in self.variaveis(ctx) if t == tau]
        return out

    def custo_folha(self, nome: str) -> int:
        return self.custos.get(nome, 1)

    def folhas_de_custo(self, ctx: Tuple[Tipo, ...], tau: Tipo, s: int) -> List[Termo]:
        """Folhas de tipo tau cujo CUSTO é exatamente s (variáveis custam 1; constantes custam
        custo_folha). Sem custos (omissão) coincide com folhas() em s = 1 e [] nos demais."""
        out = [C(c) for c in self._consts.get(tau, []) if self.custo_folha(c) == s]
        if s == 1:
            out += [V(v) for v, t in self.variaveis(ctx) if t == tau]
        return out

    def args_para(self, tau: Tipo) -> List[Tipo]:
        return self._args.get(tau, [])

    def lam_ok(self, ctx, tau) -> bool:
        return tau[0] == "Fun" and len(ctx) < self.D

    def fix_info(self, ctx, tau):
        """(argumentos, resultado) se fix_τ é admitido na profundidade len(ctx); senão None."""
        if not self.fix or tau[0] != "Fun" or tau not in self.T:
            return None
        args, res = argumentos_e_resultado(tau)
        if len(ctx) + len(args) > self.D:
            return None
        return tuple(args), res

    @staticmethod
    def termo_fix(ctx, tau, args, corpo) -> Termo:
        d = len(ctx)
        binders = [(nome_var(d + i), a) for i, a in enumerate(args)]
        return FIX(tau, LAM(REC, tau, LAMS(binders, corpo)))


# =====================================================================
# 1. Contagem exata (programação dinâmica, sem avaliar)
# =====================================================================
class _Contagem:
    """N = NA (não-λ: folhas, aplicações, fix) + NL (λ). Sem redexes β, a função de uma aplicação
    é sempre NA. R = (S, OA, OL): espinhas de rec, demais não-λ, demais λ."""

    def __init__(self, g: Gramatica):
        self.g = g
        self._na: Dict[tuple, int] = {}
        self._r: Dict[tuple, Tuple[int, int, int]] = {}

    def N(self, ctx, tau, s) -> int:
        return self.NA(ctx, tau, s) + self.NL(ctx, tau, s)

    def NL(self, ctx, tau, s) -> int:
        if s >= 2 and self.g.lam_ok(ctx, tau):
            return self.N(ctx + (tau[1],), tau[2], s - 1)
        return 0

    def _Nf(self, ctx, tau, s) -> int:
        """Termos admitidos na posição de função de uma aplicação."""
        return self.N(ctx, tau, s) if self.g.beta else self.NA(ctx, tau, s)

    def NA(self, ctx, tau, s) -> int:
        if s < 1:
            return 0
        k = (ctx, tau, s)
        v = self._na.get(k)
        if v is not None:
            return v
        g = self.g
        total = len(g.folhas(ctx, tau)) if s == 1 else 0
        for a in g.args_para(tau):
            fa = FUN(a, tau)
            for s1 in range(1, s):
                nf = self._Nf(ctx, fa, s1)
                if nf:
                    total += nf * self.N(ctx, a, s - s1)
        fi = g.fix_info(ctx, tau)
        if fi is not None:
            args, res = fi
            sc = s - 2 - len(args)
            if sc >= 1:
                total += sum(self.R(ctx + args, tau, res, sc))
        self._na[k] = total
        return total

    def R(self, ctx, rho, sigma, s) -> Tuple[int, int, int]:
        """(S, OA, OL) de termos com rec : rho, tipo sigma, tamanho s."""
        k = (ctx, rho, sigma, s)
        v = self._r.get(k)
        if v is not None:
            return v
        g = self.g
        S = 1 if (s == 1 and sigma == rho) else 0
        OA = OL = 0
        for a in g.args_para(sigma):
            fa = FUN(a, sigma)
            for s1 in range(1, s):
                s2 = s - s1
                Sf, OAf, OLf = self.R(ctx, rho, fa, s1)
                Of = OAf + (OLf if g.beta else 0)
                Sa, OAa, OLa = self.R(ctx, rho, a, s2)
                Ra = Sa + OAa + OLa
                Na = self.N(ctx, a, s2)
                S += Sf * Na
                OA += Of * (Na + Ra) + self._Nf(ctx, fa, s1) * Ra
        if s >= 2 and g.lam_ok(ctx, sigma):
            OL += sum(self.R(ctx + (sigma[1],), rho, sigma[2], s - 1))
        self._r[k] = (S, OA, OL)
        return S, OA, OL


def contar_termos(tabela: Tabela, tipo: Tipo, contexto=None, s_max: int = 8, profundidade_lambda: int = 2,
                  tipos: Optional[Iterable[Tipo]] = None, fix: bool = True,
                  redexes_beta: bool = False) -> Dict[int, int]:
    """N(s, τ, Γ0) exato para s = 1..s_max na gramática G (contagem pura, nenhum termo avaliado)."""
    g = Gramatica(tabela, contexto, tipo, profundidade_lambda, tipos, fix, redexes_beta)
    c = _Contagem(g)
    return {s: c.N((), tipo, s) for s in range(1, s_max + 1)}


def tabela_contagens(tabela: Tabela, s_max: int = 12, tipos_tarefa: Optional[Sequence[Tipo]] = None,
                     **kw) -> List[dict]:
    """PM7: N(s, τ) de termos fechados para cada tipo de tarefa (omissão: dsl.TIPOS_TAREFA)."""
    from .dsl import TIPOS_TAREFA
    out = []
    for tau in (tipos_tarefa or TIPOS_TAREFA):
        c = contar_termos(tabela, tau, {}, s_max, **kw)
        razoes = {s: (c[s] / c[s - 1] if c.get(s - 1) else None) for s in range(2, s_max + 1)}
        out.append({"tabela": tabela.nome, "tipo": tipo_str(tau), "contagens": c, "razoes": razoes})
    return out


# =====================================================================
# 2. Construção de termos R (corpos de fix), comum ao sem-poda e ao com-poda
# =====================================================================
def _nao_lam(ts):
    return [t for t in ts if t[0] != "lam"]


class _GeradorR:
    """Mixin: gera R = S (espinhas) e O (demais) sintaticamente a partir de self._n_termos(ctx, τ, s)."""

    def _init_r(self):
        self._rmemo: Dict[tuple, Tuple[List[Termo], List[Termo]]] = {}

    def _r_termos(self, ctx, rho, sigma, s) -> Tuple[List[Termo], List[Termo]]:
        k = (ctx, rho, sigma, s)
        v = self._rmemo.get(k)
        if v is not None:
            return v
        g = self.g
        S: List[Termo] = [V(REC)] if (s == 1 and sigma == rho) else []
        O: List[Termo] = []
        for a in g.args_para(sigma):
            fa = FUN(a, sigma)
            for s1 in range(1, s):
                s2 = s - s1
                Sf, Of = self._r_termos(ctx, rho, fa, s1)
                Sa, Oa = self._r_termos(ctx, rho, a, s2)
                if not g.beta:
                    Of = _nao_lam(Of)
                if Sf or Of:
                    Na = self._n_termos(ctx, a, s2)
                    for f in Sf:
                        for x in Na:
                            S.append(("ap", f, x))
                    if Of:
                        todos = list(Na) + Sa + Oa
                        for f in Of:
                            for x in todos:
                                O.append(("ap", f, x))
                if Sa or Oa:
                    Nf = self._n_termos(ctx, fa, s1)
                    if not g.beta:
                        Nf = _nao_lam(Nf)
                    for f in Nf:
                        for x in Sa:
                            O.append(("ap", f, x))
                        for x in Oa:
                            O.append(("ap", f, x))
        if s >= 2 and g.lam_ok(ctx, sigma):
            Sb, Ob = self._r_termos(ctx + (sigma[1],), rho, sigma[2], s - 1)
            v_ = nome_var(len(ctx))
            O.extend(LAM(v_, sigma[1], b) for b in Sb + Ob)
        self._rmemo[k] = (S, O)
        self._contar_r(len(S) + len(O))
        return S, O

    def _contar_r(self, k: int) -> None:
        pass


# =====================================================================
# 3. Enumeração sem poda (todos os termos de G)
# =====================================================================
class _TodosTermos(_GeradorR):
    def __init__(self, g: Gramatica):
        self.g = g
        self._memo: Dict[tuple, List[Termo]] = {}
        self._init_r()

    def _n_termos(self, ctx, tau, s) -> List[Termo]:
        k = (ctx, tau, s)
        v = self._memo.get(k)
        if v is not None:
            return v
        g = self.g
        out: List[Termo] = list(g.folhas(ctx, tau)) if s == 1 else []
        for a in g.args_para(tau):
            fa = FUN(a, tau)
            for s1 in range(1, s):
                fs = self._n_termos(ctx, fa, s1)
                if not g.beta:
                    fs = _nao_lam(fs)
                if fs:
                    xs = self._n_termos(ctx, a, s - s1)
                    for f in fs:
                        for x in xs:
                            out.append(("ap", f, x))
        if s >= 2 and g.lam_ok(ctx, tau):
            v_ = nome_var(len(ctx))
            out.extend(LAM(v_, tau[1], b) for b in self._n_termos(ctx + (tau[1],), tau[2], s - 1))
        fi = g.fix_info(ctx, tau)
        if fi is not None:
            args, res = fi
            sc = s - 2 - len(args)
            if sc >= 1:
                S, O = self._r_termos(ctx + args, tau, res, sc)
                out.extend(Gramatica.termo_fix(ctx, tau, args, c) for c in S + O)
        self._memo[k] = out
        return out


def enumerar_sem_poda(tabela: Tabela, contexto, tipo: Tipo, s_max: int, profundidade_lambda: int = 2,
                      tipos: Optional[Iterable[Tipo]] = None, fix: bool = True,
                      redexes_beta: bool = False) -> Iterator[Tuple[Termo, int]]:
    """Todos os termos de G de tipo `tipo` em Γ0 = contexto, por tamanho crescente (validação)."""
    g = Gramatica(tabela, contexto, tipo, profundidade_lambda, tipos, fix, redexes_beta)
    t = _TodosTermos(g)
    for s in range(1, s_max + 1):
        for termo in t._n_termos((), tipo, s):
            yield termo, s


# =====================================================================
# 4. Amostras e mundos para a assinatura OE
# =====================================================================
_AMOSTRAS_CACHE: Dict[tuple, tuple] = {}
#: no nível ≥ 1 (argumentos aninhados e binders de contextos aninhados) as baterias de tipos
#: inexatos são truncadas a estes tamanhos; Bool, Pos e Grade ficam sempre exaustivos.
CAP_AMOSTRAS_ANINHADAS = {"Lista": 6, "Fun": 3}


def _memo1(f):
    cache: dict = {}

    def h(x):
        try:
            return cache[x]
        except KeyError:
            v = cache[x] = f(x)
            return v
        except TypeError:  # argumento não hasheável (função)
            return f(x)
    return h


def amostras_oe(tipo: Tipo, g: Grade, nivel: int = 0) -> tuple:
    """Valores de amostra de `tipo` na grade g (determinísticos). Bool e Pos: exaustivos; Grade: (g,);
    L Pos: bateria de avaliador.amostras_de_tipo (8 listas) mais a primeira preta, as pretas sem a
    primeira e a primeira linha (comprimento ≤ F(n)); demais: avaliador.amostras_de_tipo (funções
    memoizadas).
    Em nivel ≥ 1 as baterias de listas e funções são truncadas (CAP_AMOSTRAS_ANINHADAS)."""
    k = (tipo, g, nivel > 0)
    v = _AMOSTRAS_CACHE.get(k)
    if v is not None:
        return v
    if tipo == BOOL:
        out = [False, True]
    elif tipo == POS:
        out = list(g.posicoes())
    elif tipo == GRADE:
        out = [g]
    elif tipo == LP:
        base = list(amostras_de_tipo(LP, g))
        pretas, pos = tuple(g.pretas()), tuple(g.posicoes())
        brancas = tuple(p for p in pos if not g.celula(p))
        extra = [pretas[:1], pretas[1:], tuple(g.linhas()[0])]
        out = []
        for x in base + extra:
            x = truncar(x, F(g.n))
            if x not in out:
                out.append(x)
    elif tipo[0] == "Fun":
        out = [_memo1(f) for f in amostras_de_tipo(tipo, g, todas_posicoes=True)]
    else:
        out = list(amostras_de_tipo(tipo, g, todas_posicoes=True))
    if nivel > 0 and tipo[0] in CAP_AMOSTRAS_ANINHADAS:
        out = out[:CAP_AMOSTRAS_ANINHADAS[tipo[0]]]
    v = tuple(out)
    if len(_AMOSTRAS_CACHE) > 50000:
        _AMOSTRAS_CACHE.clear()
    _AMOSTRAS_CACHE[k] = v
    return v


def tipo_exato(tipo: Tipo) -> bool:
    """True se a assinatura OE de `tipo` é exata nos mundos (argumentos só Bool, Pos, Grade)."""
    while tipo[0] == "Fun":
        if tipo[1] not in TIPOS_EXATOS:
            return False
        tipo = tipo[2]
    return True


def grades_amostra_oe(semente: int = 10_001, por_contagem3: int = 3, k4_extremos: int = 6,
                      k4_meio: int = 4) -> List[Grade]:
    """Grades da partição oraculo_treino para os mundos OE (hiperparâmetro do piloto):
    todas as de n = 2 (3); n = 3 estratificadas por número de pretas (até por_contagem3 por contagem,
    0..9, sorteio com rng_derivado(semente, "oe:grades_amostra")); n = 4: k4_extremos com ≤ 2 ou ≥ 14 pretas e k4_meio por
    amostragem natural. Intercaladas (n = 2 e n = 3 primeiro, depois n = 3 e n = 4) para que todo
    prefixo seja diverso e a chave rápida (M_RAPIDA primeiros mundos) seja barata.
    Limitação [C]: nenhuma grade da partição com n ≤ 4 tem uma única preta em (1,1) (nem o
    complemento), logo termos que só diferem aí são indistinguíveis por QUALQUER amostra admissível."""
    from . import geradores as G
    rng = G.rng_derivado(semente, "oe:grades_amostra")   # fluxo próprio (não coincide com o de nenhuma tarefa)
    g2 = list(G.grades_da_particao(2, PARTICAO_OE))
    g3 = G.grades_da_particao(3, PARTICAO_OE)
    por_k: Dict[int, List[Grade]] = {}
    for g in g3:
        por_k.setdefault(sum(g.bits), []).append(g)
    n3: List[Grade] = []
    for k in sorted(por_k):
        l = por_k[k]
        n3 += l if len(l) <= por_contagem3 else rng.sample(l, por_contagem3)
    g4all = G.grades_da_particao(4, PARTICAO_OE)
    ext = [g for g in g4all if sum(g.bits) <= 2 or sum(g.bits) >= 14]
    n4 = rng.sample(ext, min(k4_extremos, len(ext)))
    tent = 0
    while len(n4) < k4_extremos + k4_meio and tent < 1000:
        tent += 1
        g = G.amostra_natural(4, rng, particao=PARTICAO_OE)
        if g not in n4:
            n4.append(g)
    # intercalação determinística: primeiro n = 2 e n = 3 alternados (os M_RAPIDA primeiros mundos
    # formam a chave rápida e convém que sejam baratos: F(2) = 16), depois n = 3 e n = 4 alternados;
    # n = 3 em ordem de contagem a partir do meio (densidades variadas em todo prefixo)
    n3.sort(key=lambda g: (abs(sum(g.bits) - 4.5), g.bits))
    out: List[Grade] = []
    while g2:
        out.append(g2.pop(0))
        if n3:
            out.append(n3.pop(0))
    filas = [n3, n4]
    while any(filas):
        for f in filas:
            if f:
                out.append(f.pop(0))
    return out


def ambientes_padrao(contexto, grades: Sequence[Grade], max_por_grade: int = 6) -> List[Tuple[Grade, dict]]:
    """Ambientes (grade, env) para Γ0: variáveis Grade recebem a grade; as demais recebem combinações
    das amostras OE (no máximo max_por_grade por grade, em ordem determinística)."""
    gamma = _normalizar_contexto(contexto)
    out = []
    for g in grades:
        combos = [dict()]
        for nome, t in gamma:
            if t == GRADE:
                for c in combos:
                    c[nome] = g
                continue
            novos = []
            for c in combos:
                for a in amostras_oe(t, g):
                    d = dict(c)
                    d[nome] = a
                    novos.append(d)
            combos = novos
        if len(combos) > max_por_grade:
            passo = len(combos) / max_por_grade
            combos = [combos[int(i * passo)] for i in range(max_por_grade)]
        out += [(g, c) for c in combos]
    return out


# =====================================================================
# 5. Enumerador com poda OE
# =====================================================================
class OrcamentoEnumeracaoEsgotado(Exception):
    """Orçamento de candidatos avaliados do enumerador excedido."""


@dataclass
class ContadorEnumeracao:
    """Contadores determinísticos do enumerador (nunca tempo nem memória real)."""
    candidatos_construidos: int = 0        # termos N montados (folhas, aplicações, λ, fix)
    candidatos_avaliados: int = 0          # termos com assinatura calculada (todos os contextos e tipos)
    candidatos_avaliados_alvo: int = 0     # idem, só no contexto raiz e tipo-alvo
    candidatos_lambda: int = 0
    candidatos_lambda_reagrupados: int = 0  # λ de corpo não funcional: assinatura sem avaliar (0 passos)
    candidatos_fix: int = 0
    descartados_equivalentes: int = 0
    descartados_orcamento_passos: int = 0
    descartados_recursao: int = 0
    termos_rec_construidos: int = 0        # corpos R de fix (sem poda)
    classes_distintas: int = 0             # representantes guardados (todas as tabelas)
    classes_alvo: int = 0
    passos_assinatura: int = 0             # passos do avaliador gastos em valores e assinaturas
    colisoes_rapidas: int = 0              # tipos funcionais: chave rápida repetida (exige completa)
    assinaturas_incompletas: int = 0       # completa abortada por orçamento: entrada nunca igualada
    contextos: int = 0
    mundos_total: int = 0

    def como_dict(self) -> dict:
        return asdict(self)


class _Mundo:
    __slots__ = ("env", "grade", "ctx", "r")

    def __init__(self, env, grade, ctx, r):
        self.env = env
        self.grade = grade
        self.ctx = ctx
        self.r = r          # índice do mundo-raiz de origem


class _Entrada:
    __slots__ = ("termo", "tam", "vals", "sig", "rapida")

    def __init__(self, termo, tam, vals, sig):
        self.termo = termo
        self.tam = tam
        self.vals = vals
        self.sig = sig          # assinatura completa (None = ainda não calculada; ver _completar)
        self.rapida = None      # chave rápida (tipos funcionais)


class _Ctx:
    __slots__ = ("chave", "nivel", "mundos", "grupos", "base_pai", "idx_f", "tabs", "feito", "vistos")

    def __init__(self, chave, nivel, mundos, grupos, base_pai, idx_f):
        self.chave = chave
        self.nivel = nivel            # nível de amostragem (sobe só com binders que multiplicam mundos)
        self.mundos = mundos
        self.grupos = grupos          # amostras por mundo-pai de base_pai, para reagrupar
        self.base_pai = base_pai      # índices dos mundos do pai de que este contexto foi construído
        self.idx_f = idx_f            # mundos das assinaturas de tipo funcional (todos, ver _novo_ctx)
        self.tabs: Dict[Tipo, List[List[_Entrada]]] = {}
        self.feito: Dict[Tipo, int] = {}
        self.vistos: Dict[Tipo, set] = {}


def _reagrupar(sig: tuple, grupos: List[int]) -> tuple:
    out = []
    i = 0
    for c in grupos:
        out.append(sig[i:i + c])
        i += c
    return tuple(out)


class Enumerador(_GeradorR):
    """Enumeração ascendente por tamanho e tipo, com poda OE sobre mundos de amostra fixos.

    Enumerador(tabela, contexto, tipo_alvo, ambientes_amostra=None, n=3, orcamento=None, ...)
    - tabela: Tabela de uso "descoberta" (exigir_tabela_de_descoberta), salvo auditoria=True;
    - contexto: {nome: tipo} (Γ0); tipo_alvo: tipo enumerado em Γ0;
    - ambientes_amostra: lista de Grade (Γ0 só com variáveis Grade) ou de (Grade, env); por omissão
      ambientes_padrao(contexto, grades_amostra_oe()). Toda grade deve estar em oraculo_treino
      (permitir_fora_particao exige auditoria=True: só para validar o mecanismo de poda);
    - n: reservado (o lado de cada mundo é o da sua grade);
    - orcamento: máximo de candidatos avaliados (todos os contextos); None = sem limite;
    - orcamento_passos_mundo: passos do avaliador por mundo avaliado (armado por etapa: valores,
      chave rápida, assinatura completa); excedido, o candidato é descartado e contado em
      descartados_orcamento_passos (fonte declarada de incompletude; None = sem limite);
    - mundos_funcao: (K1, K2, ...): um contexto de nível de amostragem k ≥ 1 é construído só com os
      mundos vindos dos K_k primeiros mundos-raiz (None = todos). O nível sobe 1 a cada binder que
      multiplica mundos (Pos, listas, funções); binders Grade e Bool não o alteram. Dentro de cada
      contexto todas as assinaturas usam todos os seus mundos (congruência local); a aproximação fica
      na fronteira entre níveis, e um λ cuja base de mundos difere da do pai é avaliado (não
      reagrupado). Hiperparâmetro OE do piloto.
    """

    def __init__(self, tabela: Tabela, contexto, tipo_alvo: Tipo, ambientes_amostra=None, n: int = 3,
                 orcamento: Optional[int] = None, *, profundidade_lambda: int = 2,
                 tipos: Optional[Iterable[Tipo]] = None, fix: bool = True, redexes_beta: bool = False,
                 orcamento_passos_mundo: Optional[int] = 10_000, poda_inexata: bool = True,
                 mundos_funcao: Sequence[Optional[int]] = (8, 3), auditoria: bool = False,
                 permitir_fora_particao: bool = False, semente: int = 10_001,
                 custos_folha: Optional[Dict[str, int]] = None):
        from . import geradores as G
        if not auditoria:
            exigir_tabela_de_descoberta(tabela)
        if permitir_fora_particao and not auditoria:
            raise ErroProveniencia("mundos OE fora de oraculo_treino só em auditoria (validação)")
        self.auditoria = auditoria
        self.proveniencia = "descoberta" if tabela.uso == "descoberta" else f"auditoria:{tabela.uso}"
        self.g = Gramatica(tabela, contexto, tipo_alvo, profundidade_lambda, tipos, fix, redexes_beta,
                           custos_folha)
        self.tabela = tabela
        self.tipo_alvo = tipo_alvo
        self.n = n
        self.orcamento = orcamento
        self.orc_passos = orcamento_passos_mundo
        self.poda_inexata = poda_inexata
        self.mundos_funcao = tuple(mundos_funcao) or (None,)
        self.cont = ContadorEnumeracao()
        self._cav = Contador()
        self._ctx_n: Dict[int, Contexto] = {}
        self._init_r()
        if ambientes_amostra is None:
            ambientes_amostra = ambientes_padrao(self.g.gamma0, grades_amostra_oe(semente))
        mundos = []
        nomes0 = [nm for nm, _ in self.g.gamma0]
        for item in ambientes_amostra:
            if isinstance(item, Grade):
                grade, env = item, {nm: item for nm, t in self.g.gamma0 if t == GRADE}
            else:
                grade, env = item
                env = dict(env)
            if not permitir_fora_particao and not G.na_particao(grade, PARTICAO_OE):
                raise ValueError(f"ambiente OE fora da partição {PARTICAO_OE}: {grade.serializar()}")
            if sorted(env) != sorted(nomes0):
                raise ValueError(f"ambiente com variáveis {sorted(env)}, esperado {sorted(nomes0)}")
            mundos.append(_Mundo(env, grade, self._contexto_n(grade.n), len(mundos)))
        if not mundos:
            raise ValueError("sem mundos de amostra")
        self.grades_amostra = tuple(dict.fromkeys(m.grade for m in mundos))
        self._ctxs: Dict[tuple, _Ctx] = {}
        self.raiz = self._novo_ctx((), 0, mundos, [], [])
        self.s_completo = 0
        self.historico: List[dict] = []
        self.esgotado = False

    # ---------------------------------------------------------- infraestrutura
    def _contexto_n(self, n):
        c = self._ctx_n.get(n)
        if c is None:
            c = self._ctx_n[n] = Contexto(n, self._cav, self.tabela)
        return c

    def _K(self, nivel):
        """Mundos-raiz admitidos no nível de amostragem `nivel` (None = todos)."""
        if nivel == 0:
            return None
        return self.mundos_funcao[min(nivel - 1, len(self.mundos_funcao) - 1)]

    def _novo_ctx(self, chave, nivel, mundos, grupos, base_pai) -> _Ctx:
        c = _Ctx(chave, nivel, mundos, grupos, base_pai, list(range(len(mundos))))
        self._ctxs[chave] = c
        self.cont.contextos += 1
        self.cont.mundos_total += len(mundos)
        return c

    def _ctx(self, chave: tuple) -> _Ctx:
        c = self._ctxs.get(chave)
        if c is not None:
            return c
        pai = self._ctx(chave[:-1])
        alfa = chave[-1]
        nome = nome_var(len(chave) - 1)
        nivel = self._nivel_seguinte(pai.nivel, alfa)
        K = self._K(nivel)
        base = [i for i in pai.idx_f if K is None or pai.mundos[i].r < K]
        if base == pai.idx_f:
            base = pai.idx_f
        mundos, grupos = [], []
        for i in base:
            w = pai.mundos[i]
            am = amostras_oe(alfa, w.grade, pai.nivel)
            grupos.append(len(am))
            for a in am:
                env = dict(w.env)
                env[nome] = a
                mundos.append(_Mundo(env, w.grade, w.ctx, w.r))
        return self._novo_ctx(chave, nivel, mundos, grupos, base)

    @staticmethod
    def _nivel_seguinte(nivel, alfa):
        """Binders Grade e Bool (≤ 2 amostras, exatas) não mudam o nível de amostragem."""
        return nivel if alfa in (GRADE, BOOL) else nivel + 1

    def _podavel(self, tau) -> bool:
        return self.poda_inexata or tipo_exato(tau)

    def _sig_valor(self, v, tau, grade, nivel):
        if tau[0] != "Fun":
            return v
        r = tau[2]
        n2 = self._nivel_seguinte(nivel, tau[1])
        return tuple(self._sig_valor(v(a), r, grade, n2) for a in amostras_oe(tau[1], grade, nivel))

    def _assinatura(self, C_: _Ctx, tau, vals):
        if tau[0] != "Fun":
            return tuple(vals)
        sv = self._sig_valor
        nv = C_.nivel
        ms = C_.mundos
        return tuple(sv(vals[i], tau, ms[i].grade, nv) for i in C_.idx_f)

    def _armar(self, mundos: int):
        """Limite de passos para avaliar `mundos` mundos: orcamento_passos_mundo × mundos (recurso da
        busca; excedido, o candidato é descartado e contado em descartados_orcamento_passos)."""
        self._cav._limite = (sys.maxsize if self.orc_passos is None
                             else self._cav.passos + self.orc_passos * max(1, mundos))

    def _novo_avaliado(self, raiz_alvo: bool):
        c = self.cont
        c.candidatos_avaliados += 1
        if raiz_alvo:
            c.candidatos_avaliados_alvo += 1
        if self.orcamento is not None and c.candidatos_avaliados > self.orcamento:
            raise OrcamentoEnumeracaoEsgotado(c.candidatos_avaliados)

    def _vals(self, C_: _Ctx, e: _Entrada):
        """Valores por mundo (fechos calculados sob demanda para λ)."""
        if e.vals is None:
            ev = compilar(e.termo)
            self._cav._limite = sys.maxsize
            e.vals = [ev(w.env, w.ctx) for w in C_.mundos]
        return e.vals

    def _contar_r(self, k):
        self.cont.termos_rec_construidos += k

    def _n_termos(self, chave, tau, s) -> List[Termo]:
        C_ = self._ctx(chave)
        self._garantir(C_, tau, s)
        return [e.termo for e in C_.tabs[tau][s]]

    def _garantir(self, C_: _Ctx, tau, s) -> None:
        feito = C_.feito.get(tau, 0)
        if feito >= s:
            return
        if tau not in C_.tabs:
            C_.tabs[tau] = [[]]
            C_.vistos[tau] = {} if (tau[0] == "Fun" and self._podavel(tau)) else set()
        for sz in range(feito + 1, s + 1):
            self._construir(C_, tau, sz)

    # ---------------------------------------------------------- construção de uma camada
    def _parcial(self, C_: _Ctx, tau, vals, idx):
        sv = self._sig_valor
        nv = C_.nivel
        ms = C_.mundos
        return tuple(sv(vals[i], tau, ms[i].grade, nv) for i in idx)

    def _completar(self, C_: _Ctx, tau, e: _Entrada) -> None:
        """Assinatura completa (preguiçosa) de uma entrada guardada só com a chave rápida."""
        vals = self._vals(C_, e)
        resto = C_.idx_f[M_RAPIDA:]
        self._armar(len(resto))
        p0 = self._cav.passos
        try:
            e.sig = e.rapida + self._parcial(C_, tau, vals, resto)
        except (OrcamentoEsgotado, RecursionError):
            self.cont.assinaturas_incompletas += 1
            e.sig = ("<incompleta>", id(e))      # nunca igual a outra: só pode duplicar, nunca perder
        finally:
            self.cont.passos_assinatura += self._cav.passos - p0

    def _construir(self, C_: _Ctx, tau, s) -> None:
        """Constrói a camada (C_, tau, s). Deduplicação: tipos não funcionais por assinatura completa;
        tipos funcionais em dois estágios exatos (chave rápida nos M_RAPIDA primeiros mundos; a
        assinatura completa só é calculada quando a chave rápida colide)."""
        g = self.g
        cont = self.cont
        raiz_alvo = C_ is self.raiz and tau == self.tipo_alvo
        vistos = C_.vistos[tau]
        podavel = self._podavel(tau)
        base = tau[0] != "Fun"
        estagiado = podavel and not base
        locais = {} if estagiado else set()
        novos: List[_Entrada] = []
        idx_r = C_.idx_f[:M_RAPIDA]
        idx_resto = C_.idx_f[M_RAPIDA:]

        def oferecer(termo, vals, sig):
            chave = sig if podavel else termo
            if chave in vistos or chave in locais:
                cont.descartados_equivalentes += 1
                return
            locais.add(chave)
            novos.append(_Entrada(termo, s, vals, sig))

        def oferecer_f(termo, vals, rapida, completa=None):
            lc = vistos.get(rapida)
            ll = locais.get(rapida)
            if lc or ll:
                cont.colisoes_rapidas += 1
                if completa is None:
                    self._armar(len(idx_resto))
                    completa = rapida + self._parcial(C_, tau, vals, idx_resto)
                for e in (lc or []) + (ll or []):
                    if e.sig is None:
                        self._completar(C_, tau, e)
                    if e.sig == completa:
                        cont.descartados_equivalentes += 1
                        return
            e = _Entrada(termo, s, vals, completa)
            e.rapida = rapida
            novos.append(e)
            locais.setdefault(rapida, []).append(e)

        def avaliado(termo, vals):
            """Oferece um termo com valores já calculados (folha, aplicação, λ avaliado, fix)."""
            if base:
                oferecer(termo, vals, tuple(vals))
            elif estagiado:
                self._armar(len(idx_r))
                oferecer_f(termo, vals, self._parcial(C_, tau, vals, idx_r))
            else:
                oferecer(termo, vals, None)

        mundos = C_.mundos
        # folhas (de CUSTO s: com custos_folha uma constante pode entrar numa camada s > 1)
        if s <= g.custo_max_folha:
            for t in g.folhas_de_custo(C_.chave, tau, s):
                cont.candidatos_construidos += 1
                self._novo_avaliado(raiz_alvo)
                self._armar(len(mundos))
                if t[0] == "c":
                    vals = [w.ctx.constante(t[1]) for w in mundos]
                else:
                    vals = [w.env[t[1]] for w in mundos]
                try:
                    avaliado(t, vals)
                except OrcamentoEsgotado:
                    cont.descartados_orcamento_passos += 1
        # aplicações (sem redexes β, a função nunca é λ)
        for a in g.args_para(tau):
            fa = FUN(a, tau)
            for s1 in range(1, s):
                s2 = s - s1
                self._garantir(C_, fa, s1)
                fs = C_.tabs[fa][s1]
                if not g.beta:
                    fs = [f for f in fs if f.termo[0] != "lam"]
                if not fs:
                    continue
                self._garantir(C_, a, s2)
                xs = C_.tabs[a][s2]
                if not xs:
                    continue
                for f in fs:
                    vf = self._vals(C_, f)
                    ft = f.termo
                    for x in xs:
                        va = self._vals(C_, x)
                        cont.candidatos_construidos += 1
                        self._novo_avaliado(raiz_alvo)
                        self._armar(len(mundos))
                        p0 = self._cav.passos
                        try:
                            avaliado(("ap", ft, x.termo), [f_(a_) for f_, a_ in zip(vf, va)])
                        except OrcamentoEsgotado:
                            cont.descartados_orcamento_passos += 1
                        except RecursionError:
                            cont.descartados_recursao += 1
                        finally:
                            cont.passos_assinatura += self._cav.passos - p0
        # λ
        if s >= 2 and g.lam_ok(C_.chave, tau):
            alfa, beta = tau[1], tau[2]
            C2 = self._ctx(C_.chave + (alfa,))
            self._garantir(C2, beta, s - 1)
            v_ = nome_var(len(C_.chave))
            reagrupa = podavel and beta[0] != "Fun" and C2.base_pai is C_.idx_f
            for b in C2.tabs[beta][s - 1]:
                termo = LAM(v_, alfa, b.termo)
                cont.candidatos_construidos += 1
                cont.candidatos_lambda += 1
                self._novo_avaliado(raiz_alvo)
                if reagrupa:
                    cont.candidatos_lambda_reagrupados += 1
                    sig = _reagrupar(b.sig, C2.grupos)
                    oferecer_f(termo, None, sig[:M_RAPIDA], sig)
                    continue
                self._avaliar_e_oferecer(C_, termo, avaliado)
        # fix
        fi = g.fix_info(C_.chave, tau)
        if fi is not None:
            args, res = fi
            sc = s - 2 - len(args)
            if sc >= 1:
                S, O = self._r_termos(C_.chave + args, tau, res, sc)
                for corpo in S + O:
                    termo = Gramatica.termo_fix(C_.chave, tau, args, corpo)
                    cont.candidatos_construidos += 1
                    cont.candidatos_fix += 1
                    self._novo_avaliado(raiz_alvo)
                    self._avaliar_e_oferecer(C_, termo, avaliado)
        # efetivar a camada (transacional: abortos de orçamento não deixam camadas parciais)
        tab = C_.tabs[tau]
        while len(tab) <= s:
            tab.append([])
        tab[s] = novos
        if estagiado:
            for k, l in locais.items():
                vistos.setdefault(k, []).extend(l)
        else:
            vistos |= locais
        C_.feito[tau] = s
        cont.classes_distintas += len(novos)
        if raiz_alvo:
            cont.classes_alvo += len(novos)

    def _avaliar_e_oferecer(self, C_, termo, avaliado) -> None:
        """λ não reagrupável e fix: fechos pelo avaliador em cada mundo, depois a assinatura."""
        self._armar(len(C_.mundos))
        p0 = self._cav.passos
        try:
            ev = compilar(termo)
            avaliado(termo, [ev(w.env, w.ctx) for w in C_.mundos])
        except OrcamentoEsgotado:
            self.cont.descartados_orcamento_passos += 1
        except RecursionError:
            self.cont.descartados_recursao += 1
        finally:
            self.cont.passos_assinatura += self._cav.passos - p0

    # ---------------------------------------------------------- interface pública
    def representantes(self, s: int) -> List[Tuple[Termo, int]]:
        """Representantes OE do tipo-alvo de tamanho exatamente s (constrói até s se preciso)."""
        self._garantir(self.raiz, self.tipo_alvo, s)
        if s > self.s_completo:
            for sz in range(self.s_completo + 1, s + 1):
                self.historico.append({"s": sz, "candidatos_avaliados": self.cont.candidatos_avaliados,
                                       "candidatos_avaliados_alvo": self.cont.candidatos_avaliados_alvo,
                                       "classes_alvo_tamanho": len(self.raiz.tabs[self.tipo_alvo][sz]),
                                       "classes_distintas": self.cont.classes_distintas})
            self.s_completo = s
        return [(e.termo, s) for e in self.raiz.tabs[self.tipo_alvo][s]]

    def enumerar(self, s_max: Optional[int] = None) -> Iterator[Tuple[Termo, int]]:
        """(termo, tamanho) dos representantes do tipo-alvo, por tamanho crescente, até s_max ou até
        esgotar o orçamento (então self.esgotado = True; o tamanho incompleto não é emitido)."""
        s = 1
        while s_max is None or s <= s_max:
            try:
                reps = self.representantes(s)
            except OrcamentoEnumeracaoEsgotado:
                self.esgotado = True
                return
            yield from reps
            s += 1

    def assinatura_alvo(self, termo: Termo) -> tuple:
        """Assinatura OE de um termo do tipo-alvo em Γ0 (para comparar com representantes)."""
        self._cav._limite = sys.maxsize
        ev = compilar(termo)
        vals = [ev(w.env, w.ctx) for w in self.raiz.mundos]
        return self._assinatura(self.raiz, self.tipo_alvo, vals)

    def memoria_logica(self) -> dict:
        """Tamanho das tabelas: entradas e bytes estimados (sys.getsizeof agregado, raso por objeto)."""
        ent = sig = byt = 0
        for C_ in self._ctxs.values():
            for tau, camadas in C_.tabs.items():
                for camada in camadas:
                    for e in camada:
                        ent += 1
                        byt += sys.getsizeof(e) + sys.getsizeof(e.termo) + sys.getsizeof(e.sig)
                        if e.vals is not None:
                            byt += sys.getsizeof(e.vals)
                byt += sys.getsizeof(C_.vistos[tau])
                sig += len(C_.vistos[tau])
        rterm = 0
        for S, O in self._rmemo.values():
            rterm += len(S) + len(O)
            byt += sys.getsizeof(S) + sys.getsizeof(O)
        return {"entradas_tabela": ent, "assinaturas_guardadas": sig, "termos_rec_guardados": rterm,
                "contextos": len(self._ctxs), "mundos_raiz": len(self.raiz.mundos),
                "mundos_total": sum(len(C_.mundos) for C_ in self._ctxs.values()), "bytes_estimados": byt}

    def relatorio(self) -> dict:
        return {"contadores": self.cont.como_dict(), "memoria_logica": self.memoria_logica(),
                "s_completo": self.s_completo, "historico": list(self.historico),
                "proveniencia": self.proveniencia, "tipo_alvo": tipo_str(self.tipo_alvo),
                "contexto": {nm: tipo_str(t) for nm, t in self.g.gamma0}, "D": self.g.D,
                "redexes_beta": self.g.beta, "mundos_funcao": list(self.mundos_funcao),
                "num_tipos": len(self.g.T), "grades_amostra": [g.serializar() for g in self.grades_amostra]}


# =====================================================================
# 6. Alcance s_reach
# =====================================================================
def medir_alcance(tabela: Tabela, contexto, tipo: Tipo, orcamentos: Sequence[int] = (10 ** 4, 10 ** 5),
                  s_max: int = 30, ambientes_amostra=None, **kw) -> dict:
    """s_reach(B) = maior s cujo tipo-alvo foi totalmente enumerado com ≤ B candidatos avaliados.

    Uma única execução determinística com orçamento max(orcamentos); o custo cumulativo ao completar
    cada tamanho dá s_reach para todos os B. Duas contagens: todos os candidatos avaliados (todos os
    contextos e tipos auxiliares; leitura conservadora do documento 03, 2.4) e só os do tipo-alvo.
    Contadores e medição real ficam em campos separados. Tabela base é convertida com para_aprendiz()."""
    if tabela.uso == "base":
        tabela = tabela.para_aprendiz()
    B = max(orcamentos)
    en = Enumerador(tabela, contexto, tipo, ambientes_amostra, orcamento=B, **kw)
    with medir(f"alcance {tipo_str(tipo)}") as m:
        for _ in en.enumerar(s_max):
            pass
    hist = en.historico
    s_reach = {b: max([h["s"] for h in hist if h["candidatos_avaliados"] <= b], default=0) for b in orcamentos}
    s_reach_alvo = {b: max([h["s"] for h in hist if h["candidatos_avaliados_alvo"] <= b], default=0)
                    for b in orcamentos}
    med = asdict(m)
    med["candidatos_avaliados_por_segundo"] = (en.cont.candidatos_avaliados / m.tempo_parede_s
                                               if m.tempo_parede_s > 0 else float("nan"))
    return {"tipo": tipo_str(tipo), "contexto": {nm: tipo_str(t) for nm, t in en.g.gamma0},
            "tabela": tabela.nome, "orcamentos": list(orcamentos), "s_reach": s_reach,
            "s_reach_so_alvo": s_reach_alvo, "esgotado": en.esgotado, "s_completo": en.s_completo,
            "por_tamanho": hist, "contadores": en.cont.como_dict(), "memoria_logica": en.memoria_logica(),
            "medicao": med}


# =====================================================================
# 7. Busca de tarefa com continuação incremental
# =====================================================================
@dataclass
class ContadorBusca:
    """Custo determinístico da busca (documento 02, 2.5; documento 03, 2.3). candidatos_avaliados conta
    um por termo fechado do tipo da tarefa submetido aos exemplos correntes (qualquer base);
    passos_avaliacao soma os passos de Sem_n sobre os exemplos. O custo interno do enumerador (poda OE)
    é registrado à parte em enumeracao_*."""
    candidatos_avaliados: int = 0
    passos_avaliacao: int = 0
    avaliacoes_exemplo: int = 0
    candidatos_esgotados_passos: int = 0
    chamadas: int = 0
    enumeracao_candidatos_avaliados: int = 0
    enumeracao_passos: int = 0
    refinamentos_oe: int = 0
    grades_extra_oe: int = 0

    @property
    def custo(self) -> int:
        return self.candidatos_avaliados + self.passos_avaliacao

    def como_dict(self) -> dict:
        d = asdict(self)
        d["custo"] = self.custo
        return d


class EstadoBusca:
    """Estado de uma busca: enumerador com poda OE, posição corrente e exemplos acumulados. Exemplos só
    crescem; por isso todo candidato anterior à posição continua rejeitado e a busca recomeça no
    último candidato consistente (só os exemplos novos são testados).

    REFINAMENTO OE (documento 02, 2.4: equivalência "sobre grades do reservatório de treino e do
    oráculo"; achado de revisão): os mundos OE são a amostra fixa grades_amostra_oe MAIS as grades de
    todos os exemplos e contraexemplos recebidos (as que estão em oraculo_treino), acrescentadas ao
    fim. Quando chega uma grade nova, o enumerador é RECONSTRUÍDO com os mundos ampliados e a busca
    recomeça do início (os termos já rejeitados são pulados sem nova avaliação: exemplos só crescem).
    Assim duas classes separadas por uma grade de exemplo nunca ficam fundidas NO NÍVEL DA RAIZ. Limites
    declarados: (i) contextos aninhados (nível ≥ 1) continuam a usar só os K_k primeiros mundos-raiz;
    (ii) tarefas sem argumento Grade (L Pos → L Pos → ·) não têm grades nos exemplos: sem refinamento.
    O custo dos enumeradores descartados continua contado (enumeracao_*) e o orçamento de enumeração é
    cumulativo na tarefa."""

    def __init__(self, tabela: Tabela, tipo: Tipo, s_max: int = 30, orcamento_passos: int = 100_000,
                 orcamento_enumeracao: Optional[int] = None, ambientes_amostra=None,
                 refinar_oe: Optional[bool] = None, semente: int = 10_001, **kw):
        exigir_tabela_de_descoberta(tabela)  # busca é sempre de aprendiz: nunca tabela manual
        self.tabela = tabela
        self.tipo = tipo
        self.s_max = s_max
        self.orcamento_passos = orcamento_passos
        self.orcamento_enumeracao = orcamento_enumeracao
        # omissão: refina com a amostra de produção; com amostra explícita só se pedido (lista de Grade)
        self.refinar_oe = (ambientes_amostra is None) if refinar_oe is None else bool(refinar_oe)
        if self.refinar_oe and ambientes_amostra is not None and not all(isinstance(x, Grade) for x in ambientes_amostra):
            raise ValueError("refinamento OE exige amostra de grades (Γ0 vazio)")
        self.semente = semente
        self._kw = dict(kw)
        self._amostra = list(ambientes_amostra) if ambientes_amostra is not None else list(grades_amostra_oe(semente))
        self.grades_extra: List[Grade] = []
        self._pendentes: List[Grade] = []
        self.grades_fora_particao = 0
        self.refinamentos = 0
        self._enum_gasto_anterior = 0
        self._enum_passos_anterior = 0
        self.enum: Optional[Enumerador] = None
        self.candidatos: List[Tuple[Termo, int]] = []
        self.tamanho_carregado = 0
        self.indice = 0
        self.verificados = 0         # exemplos já verificados no candidato da posição corrente
        self.exemplos: List[Tuple[tuple, object]] = []
        self.rejeitados: set = set()  # termos já avaliados e inconsistentes (continuam: exemplos só crescem)
        self.pulados_ja_rejeitados = 0
        self.hipotese: Optional[Termo] = None
        self.certificado = None       # certificados.CertificadoBusca do último termo devolvido
        self.historico: List[dict] = []
        if not self.refinar_oe:
            self._construir_enum()

    # ---------------------------------------------------------- mundos OE
    def _construir_enum(self) -> None:
        if self.enum is not None:
            self._enum_gasto_anterior += self.enum.cont.candidatos_avaliados
            self._enum_passos_anterior += self.enum.cont.passos_assinatura
        orc = None if self.orcamento_enumeracao is None else max(0, self.orcamento_enumeracao - self._enum_gasto_anterior)
        self.enum = Enumerador(self.tabela, {}, self.tipo, self._amostra + self.grades_extra, orcamento=orc,
                               semente=self.semente, **self._kw)
        self.candidatos, self.tamanho_carregado, self.indice, self.verificados = [], 0, 0, 0

    def _anotar_grades(self, entrada) -> None:
        from . import geradores as G
        if not self.refinar_oe:
            return
        conhecidas = set(self._amostra) | set(self.grades_extra) | set(self._pendentes)
        for a in entrada:
            if isinstance(a, Grade) and a not in conhecidas:
                if G.na_particao(a, PARTICAO_OE):
                    self._pendentes.append(a)
                    conhecidas.add(a)
                else:
                    self.grades_fora_particao += 1

    def _atualizar_enum(self) -> None:
        if self.enum is None or self._pendentes:
            if self.enum is not None:
                self.refinamentos += 1
            self.grades_extra += self._pendentes
            self._pendentes = []
            self._construir_enum()

    def enumeracao_candidatos(self) -> int:
        """Candidatos avaliados pelo(s) enumerador(es) desta busca (poda OE), cumulativo."""
        return self._enum_gasto_anterior + (self.enum.cont.candidatos_avaliados if self.enum else 0)

    def enumeracao_passos(self) -> int:
        return self._enum_passos_anterior + (self.enum.cont.passos_assinatura if self.enum else 0)

    def enumeracao_esgotada(self) -> bool:
        return self.orcamento_enumeracao is not None and self.enumeracao_candidatos() > self.orcamento_enumeracao

    def adicionar_exemplo(self, entrada, saida) -> None:
        ent = tuple(entrada) if isinstance(entrada, (tuple, list)) else (entrada,)
        self.exemplos.append((ent, saida))
        self._anotar_grades(ent)

    def _carregar_proximo(self) -> bool:
        if self.tamanho_carregado >= self.s_max:
            return False
        s = self.tamanho_carregado + 1
        self.candidatos.extend(self.enum.representantes(s))
        self.tamanho_carregado = s
        return True

    def _consistente(self, termo, contador: ContadorBusca, desde: int) -> bool:
        ev = compilar(termo)
        for args, esperado in self.exemplos[desde:]:
            n = next((a.n for a in args if isinstance(a, Grade)), self.enum.n)
            c = Contador(self.orcamento_passos)
            ctx = Contexto(n, c, self.tabela)
            try:
                v = ev({}, ctx)
                ok = aplicar(v, *args) == esperado
            except OrcamentoEsgotado:
                contador.passos_avaliacao += c.passos
                contador.candidatos_esgotados_passos += 1
                return False
            contador.passos_avaliacao += c.passos
            contador.avaliacoes_exemplo += 1
            if not ok:
                return False
        return True

    def buscar(self, orcamento: Optional[int], contador: ContadorBusca) -> Optional[Termo]:
        """Menor termo (na ordem do enumerador) consistente com todos os exemplos, ou None se o
        orçamento de candidatos avaliados (desta chamada) ou o enumerador se esgotar."""
        from .certificados import emitir_busca
        contador.chamadas += 1
        e0, p0 = self.enumeracao_candidatos(), self.enumeracao_passos()
        gastos = 0
        self.certificado = None
        try:
            self._atualizar_enum()
            while True:
                while self.indice >= len(self.candidatos):
                    if not self._carregar_proximo():
                        self.hipotese = None
                        return None
                termo, s = self.candidatos[self.indice]
                if termo in self.rejeitados:      # já avaliado antes do refinamento: continua rejeitado
                    self.pulados_ja_rejeitados += 1
                    self.indice += 1
                    self.verificados = 0
                    continue
                if orcamento is not None and gastos >= orcamento:
                    self.hipotese = None
                    return None
                gastos += 1
                contador.candidatos_avaliados += 1
                if self._consistente(termo, contador, self.verificados):
                    self.verificados = len(self.exemplos)
                    self.hipotese = termo
                    self.historico.append({"termo": termo, "tamanho": s, "indice": self.indice,
                                           "exemplos": len(self.exemplos), "refinamentos": self.refinamentos})
                    self.certificado = emitir_busca(termo, self.tipo, self.tabela.nome)
                    return termo
                self.rejeitados.add(termo)
                self.indice += 1
                self.verificados = 0
        except OrcamentoEnumeracaoEsgotado:
            self.hipotese = None
            return None
        finally:
            contador.enumeracao_candidatos_avaliados += self.enumeracao_candidatos() - e0
            contador.enumeracao_passos += self.enumeracao_passos() - p0
            contador.refinamentos_oe = self.refinamentos
            contador.grades_extra_oe = len(self.grades_extra)


def buscar(tabela: Tabela, tipo: Tipo, exemplos: Sequence[Tuple[object, object]], orcamento: Optional[int],
           contador: ContadorBusca, estado: Optional[EstadoBusca] = None, **kw):
    """Busca do menor termo fechado de tipo `tipo` consistente com `exemplos` [(entrada(s), saída)].

    Devolve (termo | None, estado). Para continuar após um contraexemplo, passe o mesmo estado com a
    lista de exemplos estendida (a anterior deve ser prefixo). `orcamento` limita os candidatos
    avaliados nesta chamada; o custo vai para `contador`."""
    if estado is None:
        estado = EstadoBusca(tabela, tipo, **kw)
    elif estado.tabela is not tabela or estado.tipo != tipo:
        raise ValueError("estado de outra busca")
    novos = [(tuple(e) if isinstance(e, (tuple, list)) else (e,), s) for e, s in exemplos]
    if novos[:len(estado.exemplos)] != estado.exemplos:
        raise ValueError("exemplos só podem crescer (a lista anterior deve ser prefixo)")
    for e, s in novos[len(estado.exemplos):]:
        estado.adicionar_exemplo(e, s)
    return estado.buscar(orcamento, contador), estado


def registrar_reutilizacoes(termo: Termo, tabela: Tabela, onde: str) -> List[str]:
    """Registra, nas abstrações descobertas usadas por `termo`, a reutilização em `onde`."""
    from .dsl import constantes
    usados = []
    for nome in dict.fromkeys(constantes(termo)):
        p = tabela.get(nome)
        if p is not None and p.proveniencia == "descoberta":
            p.registrar_reutilizacao(onde)
            usados.append(nome)
        elif p is not None and p.proveniencia == "manual-teste":
            raise ErroProveniencia(f"{nome}: entrada manual-teste num termo de aprendiz")
    return usados
