"""Programas da escada (documento 02, 2.8.1) escritos À MÃO como termos.

proveniencia = "manual-teste": servem só como referência de tamanho e como teste do avaliador,
dos tradutores e (fase 4) do compressor. NUNCA entram na biblioteca de um aprendiz em descoberta
autônoma: `tabela_referencia` devolve Tabela de uso "referencia", e Tabela de uso "descoberta"
recusa estas entradas por construção (dsl.ErroProveniencia).

Cada degrau usa os degraus anteriores como constantes de biblioteca (coluna "com os degraus
anteriores" da tabela 2.8.1). Versões por base: E0 (texto principal); E0' = beta_segura(τ(versão E0)),
salvo onde há versão manual própria (descartar via dobraR, do documento; fecho com teste de
comprimento via dobraR, deste módulo); E0+ e E0'+: fecho via ateFixo, descartar via dobraR, demais
iguais a E0 / E0'. As versões E0' são LIMITES SUPERIORES de tamanho, não mínimos.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .dsl import BASES, BOOL, FUN, GRADE, LP, POS, Primitiva, Tabela, Termo, Tipo, entrada_biblioteca, parse

PROVENIENCIA = "manual-teste"


@dataclass(frozen=True)
class ProgramaReferencia:
    nome: str
    tipo: Tipo
    texto_E0: str
    #: tamanhos da tabela do documento 02, 2.8.1 (None quando o documento dá só "≈")
    tamanho_doc: int
    tamanho_bruto_doc: Optional[int]
    tamanho_bruto_doc_aprox: Optional[int] = None
    texto_E0p: Optional[str] = None
    texto_E0mais: Optional[str] = None
    #: nome em referencias.REGISTRO quando o degrau é um conceito
    conceito_ref: Optional[str] = None
    proveniencia: str = PROVENIENCIA


_DESCARTAR_DOBRA = "(\\ (A LP) (B LP) (dobraR@P>LP (\\ (x Pos) (acc LP) (cauda@P acc)) B A))"
_FECHO_ATEFIXO = "(\\ (g Grade) (ateFixo@P (passo g)))"
#: E0': "nada novo" testado por comprimento (descartar |S| de passo g S), pois diferenca não é primitiva
_FECHO_E0P = ("(\\ (g Grade) (fix (\\ (rec (-> LP LP)) (S LP) (se@LP (vazia?@P (dobraR@P>LP (\\ (x Pos) (acc LP)"
              " (cauda@P acc)) (passo g S) S)) S (rec (passo g S))))))")

ESCADA: List[ProgramaReferencia] = [
    ProgramaReferencia("ExistePreta", FUN(GRADE, BOOL),
                       "(\\ (g Grade) (nao (vazia?@P (pretas g))))", 5, 5, conceito_ref="ExistePreta"),
    ProgramaReferencia("vizPretos", FUN(GRADE, POS, LP),
                       "(\\ (g Grade) (p Pos) (filtrar@P (celula g) (vizinhos g p)))", 8, 8),
    ProgramaReferencia("ParAdjacente", FUN(GRADE, BOOL),
                       "(\\ (g Grade) (algum@P (\\ (p Pos) (nao (vazia?@P (vizPretos g p)))) (pretas g)))",
                       10, 15, conceito_ref="ParAdjacente"),
    ProgramaReferencia("NenhumaIsolada", FUN(GRADE, BOOL),
                       "(\\ (g Grade) (todos@P (\\ (p Pos) (nao (vazia?@P (vizPretos g p)))) (pretas g)))",
                       10, 15, conceito_ref="NenhumaIsolada"),
    ProgramaReferencia("passo", FUN(GRADE, LP, LP),
                       "(\\ (g Grade) (S LP) (uniao S (juntar (mapear@P>LP (vizPretos g) S))))", 9, 14),
    ProgramaReferencia("fecho", FUN(GRADE, LP, LP),
                       "(\\ (g Grade) (fix (\\ (rec (-> LP LP)) (S LP)"
                       " (se@LP (vazia?@P (diferenca (passo g S) S)) S (rec (passo g S))))))",
                       16, None, 38, texto_E0p=_FECHO_E0P, texto_E0mais=_FECHO_ATEFIXO),
    ProgramaReferencia("componenteDe", FUN(GRADE, POS, LP),
                       "(\\ (g Grade) (p Pos) (fecho g (cons@P p vazio@P)))", 7, None, 44),
    ProgramaReferencia("UmComponente", FUN(GRADE, BOOL),
                       "(\\ (g Grade) (e (nao (vazia?@P (pretas g))) (todos@P (\\ (q Pos) (pertence q"
                       " (componenteDe g (cabeca@P (pretas g))))) (pretas g))))",
                       17, None, 60, conceito_ref="UmComponente"),
    ProgramaReferencia("pretasDe", FUN(GRADE, LP, LP),
                       "(\\ (g Grade) (r LP) (filtrar@P (celula g) r))", 6, 6),
    ProgramaReferencia("descartar", FUN(LP, LP, LP),
                       "(fix (\\ (rec (-> LP LP LP)) (A LP) (B LP) (se@LP (vazia?@P A) B (rec (cauda@P A) (cauda@P B)))))",
                       13, 13, texto_E0p=_DESCARTAR_DOBRA, texto_E0mais=_DESCARTAR_DOBRA),
    ProgramaReferencia("noMaximo", FUN(LP, LP, BOOL),
                       "(\\ (A LP) (B LP) (vazia?@P (descartar B A)))", 6, None, 18),
    ProgramaReferencia("mesmoNumero", FUN(LP, LP, BOOL),
                       "(\\ (A LP) (B LP) (e (noMaximo A B) (noMaximo B A)))", 7, None, 35),
    ProgramaReferencia("PrimeiraUltimaIguais", FUN(GRADE, BOOL),
                       "(\\ (g Grade) (mesmoNumero (pretasDe g (cabeca@LP (linhas g)))"
                       " (pretasDe g (cabeca@LP (reverter@LP (linhas g))))))",
                       13, None, 45, conceito_ref="Igual_linha1_linhaN"),
    ProgramaReferencia("LinhasIguais", FUN(GRADE, BOOL),
                       "(\\ (g Grade) (todos@LP (\\ (r LP) (mesmoNumero (pretasDe g r) (pretasDe g (cabeca@LP (linhas g)))))"
                       " (linhas g)))",
                       14, None, 45, conceito_ref="LinhasIguais"),
]

#: Variante corrigida (não faz parte da escada do documento): NenhumaIsolada da referência exige
#: ao menos um componente; o programa do documento devolve verdadeiro na grade vazia.
NENHUMA_ISOLADA_CORRIGIDA = ProgramaReferencia(
    "NenhumaIsoladaCorrigida", FUN(GRADE, BOOL),
    "(\\ (g Grade) (e (nao (vazia?@P (pretas g))) (todos@P (\\ (p Pos) (nao (vazia?@P (vizPretos g p))))"
    " (pretas g))))", 15, None, conceito_ref="NenhumaIsolada")

POR_NOME: Dict[str, ProgramaReferencia] = {p.nome: p for p in ESCADA}


def termo(p: ProgramaReferencia, base: str = "E0") -> Termo:
    """Termo do degrau na base ("E0", "E0p", "E0mais", "E0pmais"), com a biblioteca como constantes."""
    from .tradutores import beta_segura, tau
    if base == "E0":
        return parse(p.texto_E0)
    if base == "E0mais":
        return parse(p.texto_E0mais or p.texto_E0)
    if base == "E0p":
        return parse(p.texto_E0p) if p.texto_E0p else beta_segura(tau(parse(p.texto_E0)))
    if base == "E0pmais":
        if p.texto_E0mais:
            return parse(p.texto_E0mais)
        return parse(p.texto_E0p) if p.texto_E0p else beta_segura(tau(parse(p.texto_E0), mais=True))
    raise ValueError(base)


def biblioteca_manual(base: str = "E0", ate: Optional[str] = None) -> Dict[str, Termo]:
    """Dict ordenado nome → termo dos degraus (até `ate`, exclusive) na base dada."""
    out: Dict[str, Termo] = {}
    for p in ESCADA:
        if p.nome == ate:
            break
        out[p.nome] = termo(p, base)
    return out


def entradas_manuais(base: str = "E0") -> List[Primitiva]:
    """Entradas de biblioteca (proveniencia manual-teste), tipadas contra a base + anteriores."""
    tb = BASES[base]
    out: List[Primitiva] = []
    for p in ESCADA:
        out.append(entrada_biblioteca(p.nome, termo(p, base), PROVENIENCIA, tb, out, p.tipo))
    return out


def tabela_referencia(base: str = "E0") -> Tabela:
    """Base + degraus manuais, uso "referencia" (proibida a aprendizes)."""
    return BASES[base].para_referencia(entradas_manuais(base), nome=f"{base}+escada-manual")


#: Discrepâncias entre a tabela do documento 02, 2.8.1 e a contagem exata deste código.
#: Os programas NÃO foram alterados para forçar os números do documento.
#: "bruto" = tamanho após inlining da biblioteca com beta-redução segura (tradutores.inline).
DISCREPANCIAS_DOC = {
    ("mesmoNumero", "com_biblioteca"): {
        "doc": 7, "calculado": 9,
        "nota": "λA B. e (noMaximo A B) (noMaximo B A) tem 7 folhas e 2 abstrações = 9"},
    ("ParAdjacente", "bruto"): {
        "doc": 15, "calculado": 13,
        "nota": "inlining de vizPretos g p com beta: 10 − 3 + 6 = 13; sem beta seria 17; 15 não corresponde"},
    ("NenhumaIsolada", "bruto"): {
        "doc": 15, "calculado": 13, "nota": "idem ParAdjacente"},
    ("NenhumaIsolada", "semantica"): {
        "doc": "λg. todos (λp. nao (vazia? (vizPretos g p))) (pretas g)", "calculado": "verdadeiro na grade sem pretas",
        "nota": "referencias.NenhumaIsolada exige ≥ 1 componente (falso na grade vazia); variante corrigida "
                "NENHUMA_ISOLADA_CORRIGIDA tem tamanho 15 com biblioteca"},
    ("fecho", "E0p"): {
        "doc": "≈16 nas duas bases", "calculado": 20,
        "nota": "diferenca não é primitiva de E0'; versão manual com teste de comprimento via dobraR = 20; "
                "β-segura(τ(fecho)) = 33"},
}

#: Tamanhos "brutos" aproximados (≈) do documento, comparados aos calculados (informativo)
BRUTOS_CALCULADOS_E0 = {"fecho": 34, "componenteDe": 38, "UmComponente": 50, "noMaximo": 18, "mesmoNumero": 35,
                        "PrimeiraUltimaIguais": 49, "LinhasIguais": 51}
