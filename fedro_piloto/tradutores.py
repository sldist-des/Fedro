"""Traduções τ: E0 → E0' e τ': E0' → E0 (documento 02, 2.3.4), inlining de biblioteca e
verificação do lema de inlining (documento 02, 2.0).

τ e τ' são homomorfismos: fixam variáveis e fix, comutam com λ e aplicação, e levam cada
constante a um termo FECHADO da outra base (inserir termo fechado nunca captura variável).
Constantes de biblioteca (fora da base de origem) são mantidas; suas entradas são traduzidas à parte.

Os testes desta implementação (U16, U17) são amostrais: testam a IMPLEMENTAÇÃO contra Sem_n.
Não são a prova por primitiva exigida pelo pré-registro e não a substituem.
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from .dsl import (E0, E0P, E0MAIS, E0PMAIS, Tabela, Termo, Tipo, argumentos_e_resultado, constantes,
                  ocorrencias, parse, tamanho, todas_variaveis, variaveis_livres)

# =====================================================================
# Tabelas de tradução (termos fechados)
# =====================================================================
#: τ: E0 → E0' para as constantes de E0 ausentes de E0' (as comuns vão em si mesmas)
TAU_TEXTO: Dict[str, str] = {
    "linhas": "(\\ (g Grade) (dobraR@P>LLP (\\ (x Pos) (acc LLP) (cons@LP (linhaDe g x) acc)) vazio@LP"
              " (colunaDe g (cabeca@P (posicoes g)))))",
    "colunas": "(\\ (g Grade) (dobraR@P>LLP (\\ (x Pos) (acc LLP) (cons@LP (colunaDe g x) acc)) vazio@LP"
               " (linhaDe g (cabeca@P (posicoes g)))))",
    "mapear@P>LP": "(\\ (f (-> Pos LP)) (dobraR@P>LLP (\\ (x Pos) (acc LLP) (cons@LP (f x) acc)) vazio@LP))",
    "filtrar@P": "(\\ (f (-> Pos Bool)) (dobraR@P>LP (\\ (x Pos) (acc LP) (se@LP (f x) (cons@P x acc) acc)) vazio@P))",
    "filtrar@LP": "(\\ (f (-> LP Bool)) (dobraR@LP>LLP (\\ (x LP) (acc LLP) (se@LLP (f x) (cons@LP x acc) acc))"
                  " vazio@LP))",
    "algum@P": "(\\ (f (-> Pos Bool)) (dobraR@P>B (\\ (x Pos) (b Bool) (ou (f x) b)) falso))",
    "todos@P": "(\\ (f (-> Pos Bool)) (dobraR@P>B (\\ (x Pos) (b Bool) (e (f x) b)) verdadeiro))",
    "todos@LP": "(\\ (f (-> LP Bool)) (dobraR@LP>B (\\ (x LP) (b Bool) (e (f x) b)) verdadeiro))",
    "concatenar@P": "(\\ (A LP) (B LP) (dobraR@P>LP cons@P B A))",
    "juntar": "(dobraR@LP>LP (\\ (l LP) (acc LP) (dobraR@P>LP cons@P acc l)) vazio@P)",
    "reverter@LP": "(dobraR@LP>LLP (\\ (x LP) (acc LLP) (dobraR@LP>LLP cons@LP (cons@LP x vazio@LP) acc)) vazio@LP)",
    "pertence": "(\\ (p Pos) (dobraR@P>B (\\ (x Pos) (b Bool) (ou (igualP p x) b)) falso))",
    "uniao": "(\\ (A LP) (dobraR@P>LP (\\ (x Pos) (acc LP) (se@LP (dobraR@P>B (\\ (y Pos) (b Bool)"
             " (ou (igualP x y) b)) falso acc) acc (cons@P x acc))) A))",
    "diferenca": "(\\ (A LP) (B LP) (dobraR@P>LP (\\ (x Pos) (acc LP) (se@LP (dobraR@P>B (\\ (y Pos) (b Bool)"
                 " (ou (igualP x y) b)) falso B) acc (cons@P x acc))) vazio@P A))",
}


def _tau_inv_dobra(a: str, b: str) -> str:
    """dobraR@a>b em E0 via fix, COM antecipação do fim da lista: uma lista de comprimento m
    consome m níveis (não m+1), logo é exata também para m = F(n) (ver desvio D-tau-dobra)."""
    ta = {"P": "Pos", "LP": "LP"}[a]
    la = {"P": "LP", "LP": "LLP"}[a]
    tb = {"B": "Bool", "LP": "LP", "LLP": "LLP"}[b]
    return (f"(\\ (f (-> {ta} {tb} {tb})) (z {tb}) (fix (\\ (rec (-> {la} {tb})) (l {la})"
            f" (se@{b} (vazia?@{a} l) z (f (cabeca@{a} l) (se@{b} (vazia?@{a} (cauda@{a} l)) z"
            f" (rec (cauda@{a} l))))))))")


def _tau_inv_dobra_ingenua(a: str, b: str) -> str:
    """Versão ingênua (m+1 níveis). INCORRETA quando |L| = F(n); mantida só para o teste do desvio."""
    ta = {"P": "Pos", "LP": "LP"}[a]
    la = {"P": "LP", "LP": "LLP"}[a]
    tb = {"B": "Bool", "LP": "LP", "LLP": "LLP"}[b]
    return (f"(\\ (f (-> {ta} {tb} {tb})) (z {tb}) (fix (\\ (rec (-> {la} {tb})) (l {la})"
            f" (se@{b} (vazia?@{a} l) z (f (cabeca@{a} l) (rec (cauda@{a} l)))))))")


#: τ': E0' → E0 para as constantes de E0' ausentes de E0
TAU_INV_TEXTO: Dict[str, str] = {
    "linhaDe": "(\\ (g Grade) (p Pos) (cabeca@LP (filtrar@LP (pertence p) (linhas g))))",
    "colunaDe": "(\\ (g Grade) (p Pos) (cabeca@LP (filtrar@LP (pertence p) (colunas g))))",
}
for _a in ("P", "LP"):
    for _b in ("B", "LP", "LLP"):
        TAU_INV_TEXTO[f"dobraR@{_a}>{_b}"] = _tau_inv_dobra(_a, _b)


def _mapa(textos: Dict[str, str]) -> Dict[str, Termo]:
    return {k: parse(v) for k, v in textos.items()}


TAU: Dict[str, Termo] = _mapa(TAU_TEXTO)
TAU_INV: Dict[str, Termo] = _mapa(TAU_INV_TEXTO)


class ErroTraducao(ValueError):
    pass


def traduzir(t: Termo, mapa: Dict[str, Termo], origem: Tabela, destino: Tabela,
             manter_biblioteca: bool = True) -> Termo:
    """Homomorfismo genérico: constantes de `origem` → mapa[nome] ou a própria (se existir em destino)."""
    k = t[0]
    if k == "v":
        return t
    if k == "c":
        nome = t[1]
        if nome in mapa:
            return mapa[nome]
        if nome in destino:
            return t
        if nome in origem:
            raise ErroTraducao(f"constante {nome} de {origem.nome} sem tradução para {destino.nome}")
        if manter_biblioteca:
            return t
        raise ErroTraducao(f"constante desconhecida: {nome}")
    if k == "ap":
        return ("ap", traduzir(t[1], mapa, origem, destino, manter_biblioteca),
                traduzir(t[2], mapa, origem, destino, manter_biblioteca))
    if k == "lam":
        return ("lam", t[1], t[2], traduzir(t[3], mapa, origem, destino, manter_biblioteca))
    if k == "fix":
        return ("fix", t[1], traduzir(t[2], mapa, origem, destino, manter_biblioteca))
    raise ValueError(f"termo inválido: {t!r}")


def tau(t: Termo, mais: bool = False) -> Termo:
    """τ: E0 → E0' (ou E0+ → E0'+ com mais=True; ateFixo e dobraR vão em si mesmos)."""
    return traduzir(t, TAU, E0MAIS if mais else E0, E0PMAIS if mais else E0P)


def tau_inv(t: Termo, mais: bool = False) -> Termo:
    """τ': E0' → E0 (ou E0'+ → E0+ com mais=True; dobraR existe em E0+ e vai em si mesmo)."""
    mapa = {k: v for k, v in TAU_INV.items() if not (mais and k.startswith("dobraR@"))}
    return traduzir(t, mapa, E0PMAIS if mais else E0P, E0MAIS if mais else E0)


def constante_c() -> int:
    """c = max |τ(p)| sobre as constantes p de E0 (fix ↦ fix, tamanho 1)."""
    return max(tamanho(tau(("c", p.nome))) for p in E0)


def constante_c_linha() -> int:
    """c' = max |τ'(p)| sobre as constantes p de E0'."""
    return max(tamanho(tau_inv(("c", p.nome))) for p in E0P)


def tabela_constantes_traducao() -> List[Tuple[str, str, int]]:
    """(direção, constante, |tradução|) para todas as constantes não triviais."""
    out = [("τ", k, tamanho(v)) for k, v in TAU.items()]
    out += [("τ'", k, tamanho(v)) for k, v in TAU_INV.items()]
    return out


# =====================================================================
# Substituição sem captura, beta-redução e inlining
# =====================================================================
def _nome_fresco(base: str, proibidos: set) -> str:
    i = 1
    while f"{base}'{i}" in proibidos:
        i += 1
    return f"{base}'{i}"


def substituir(t: Termo, var: str, s: Termo) -> Termo:
    """t[var := s] sem captura (renomeia binders que capturariam variáveis livres de s)."""
    livres_s = variaveis_livres(s)
    return _subst(t, var, s, livres_s)


def _subst(t, var, s, livres_s):
    k = t[0]
    if k == "v":
        return s if t[1] == var else t
    if k == "c":
        return t
    if k == "ap":
        return ("ap", _subst(t[1], var, s, livres_s), _subst(t[2], var, s, livres_s))
    if k == "fix":
        return ("fix", t[1], _subst(t[2], var, s, livres_s))
    if k == "lam":
        x, tipo, corpo = t[1], t[2], t[3]
        if x == var:
            return t
        if var not in variaveis_livres(corpo):
            return t
        if x in livres_s:
            novo = _nome_fresco(x, livres_s | todas_variaveis(corpo) | {var})
            corpo = _subst(corpo, x, ("v", novo), {novo})
            x = novo
        return ("lam", x, tipo, _subst(corpo, var, s, livres_s))
    raise ValueError(f"termo inválido: {t!r}")


def contar_ocorrencias_var(t: Termo, var: str) -> int:
    k = t[0]
    if k == "v":
        return 1 if t[1] == var else 0
    if k == "c":
        return 0
    if k == "ap":
        return contar_ocorrencias_var(t[1], var) + contar_ocorrencias_var(t[2], var)
    if k == "lam":
        return 0 if t[1] == var else contar_ocorrencias_var(t[3], var)
    if k == "fix":
        return contar_ocorrencias_var(t[2], var)
    raise ValueError(t)


def _beta_segura_permitida(lam: Termo, arg: Termo) -> bool:
    """(λx.b) a → b[x:=a] não aumenta o tamanho: occ·(|a|−1) ≤ |a|+1."""
    occ = contar_ocorrencias_var(lam[3], lam[1])
    ta = tamanho(arg)
    return occ * (ta - 1) <= ta + 1


def beta_segura(t: Termo) -> Termo:
    """Reduz, de dentro para fora e até estabilizar, todo redex cuja redução não aumenta o tamanho.
    Termina (subconjunto da beta-redução do λ simplesmente tipado; fix não gera redex)."""
    while True:
        novo = _beta_passo(t)
        if novo == t:
            return t
        t = novo


def _beta_passo(t):
    k = t[0]
    if k in ("v", "c"):
        return t
    if k == "lam":
        return ("lam", t[1], t[2], _beta_passo(t[3]))
    if k == "fix":
        return ("fix", t[1], _beta_passo(t[2]))
    f, x = _beta_passo(t[1]), _beta_passo(t[2])
    if f[0] == "lam" and _beta_segura_permitida(f, x):
        return substituir(f[3], f[1], x)
    return ("ap", f, x)


def substituir_constante(t: Termo, nome: str, corpo: Termo) -> Termo:
    """Troca cada ocorrência da constante `nome` pelo termo FECHADO `corpo`."""
    k = t[0]
    if k == "c":
        return corpo if t[1] == nome else t
    if k == "v":
        return t
    if k == "ap":
        return ("ap", substituir_constante(t[1], nome, corpo), substituir_constante(t[2], nome, corpo))
    if k == "lam":
        return ("lam", t[1], t[2], substituir_constante(t[3], nome, corpo))
    if k == "fix":
        return ("fix", t[1], substituir_constante(t[2], nome, corpo))
    raise ValueError(t)


@dataclass
class PassoInlining:
    entrada: str
    ocorrencias: int
    tamanho_entrada: int
    tamanho_antes: int
    tamanho_depois: int
    limite_passo: int


@dataclass
class RelatorioInlining:
    termo: Termo
    tamanho_original: int
    tamanho_final: int
    limite: int
    passos: List[PassoInlining] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.tamanho_final <= self.limite and all(p.tamanho_depois <= p.limite_passo for p in self.passos)


def _normalizar_biblioteca(biblioteca) -> List[Tuple[str, Termo]]:
    if isinstance(biblioteca, dict):
        itens = list(biblioteca.items())
    else:
        itens = [(p.nome, p.corpo) for p in biblioteca]
    nomes = [n for n, _ in itens]
    for i, (n, corpo) in enumerate(itens):
        if variaveis_livres(corpo):
            raise ValueError(f"entrada {n} não é fechada")
        posteriores = set(nomes[i:])
        usados = set(constantes(corpo))
        if usados & posteriores:
            raise ValueError(f"entrada {n} usa entradas posteriores ou a si mesma: {usados & posteriores}")
    return itens


def inline(t: Termo, biblioteca, beta: str = "segura") -> Termo:
    """Substitui as constantes de biblioteca pelos corpos (da última para a primeira entrada).
    beta: "segura" (redexes que não aumentam tamanho) ou "nenhuma" (substituição pura)."""
    return verificar_lema_inlining(t, biblioteca, beta).termo


def verificar_lema_inlining(t: Termo, biblioteca, beta: str = "segura") -> RelatorioInlining:
    """Inlining sequencial com o limite do lema: a cada entrada ℓ (da última para a primeira),
    |depois| ≤ |antes| + k_ℓ·(|ℓ|−1), k_ℓ = ocorrências de ℓ no termo corrente e |ℓ| = tamanho do
    corpo como escrito (com as entradas anteriores como constantes). Limite total = soma dos passos.
    `biblioteca`: dict nome→corpo em ordem de definição, ou lista de Primitiva."""
    if beta not in ("segura", "nenhuma"):
        raise ValueError("beta deve ser 'segura' ou 'nenhuma'")
    itens = _normalizar_biblioteca(biblioteca)
    atual = t
    original = tamanho(t)
    limite = original
    passos = []
    for nome, corpo in reversed(itens):
        k = ocorrencias(atual, nome)
        if k == 0:
            continue
        antes = tamanho(atual)
        lim_passo = antes + k * (tamanho(corpo) - 1)
        atual = substituir_constante(atual, nome, corpo)
        if beta == "segura":
            atual = beta_segura(atual)
        depois = tamanho(atual)
        limite += k * (tamanho(corpo) - 1)
        passos.append(PassoInlining(nome, k, tamanho(corpo), antes, depois, lim_passo))
    return RelatorioInlining(atual, original, tamanho(atual), limite, passos)


# =====================================================================
# Comparação de denotações (teste de implementação)
# =====================================================================
def comparar_denotacoes(t1: Termo, t2: Termo, tipo: Tipo, grades: Iterable, tabela1=None, tabela2=None,
                        max_combinacoes: Optional[int] = None, semente: int = 10_007,
                        igual=None) -> List[tuple]:
    """Aplica t1 e t2 (fechados, de tipo `tipo`) à bateria de argumentos de `amostras_de_tipo` em
    cada grade e devolve as discrepâncias [(grade, índices dos argumentos, v1, v2)].
    Com max_combinacoes, sorteia (deterministicamente) no máximo esse número de combinações por grade."""
    from .avaliador import amostras_de_tipo, avaliar, aplicar, Contador
    args_t, _ = argumentos_e_resultado(tipo)
    igual = igual or (lambda a, b: a == b)
    rng = random.Random(semente)
    discrepancias = []
    cache_valores: Dict[int, tuple] = {}
    for g in grades:
        n = g.n
        if n not in cache_valores:
            cache_valores[n] = (avaliar(t1, {}, n, Contador(), tabela1), avaliar(t2, {}, n, Contador(), tabela2))
        v1, v2 = cache_valores[n]
        listas = [amostras_de_tipo(a, g) for a in args_t]
        total = 1
        for l in listas:
            total *= len(l)
        if max_combinacoes is not None and total > max_combinacoes:
            combos = [tuple(rng.randrange(len(l)) for l in listas) for _ in range(max_combinacoes)]
        else:
            combos = list(itertools.product(*[range(len(l)) for l in listas]))
        for idx in combos:
            args = [listas[i][j] for i, j in enumerate(idx)]
            r1 = aplicar(v1, *args)
            r2 = aplicar(v2, *args)
            if not igual(r1, r2):
                discrepancias.append((g, idx, r1, r2))
    return discrepancias
