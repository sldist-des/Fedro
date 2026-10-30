"""Programas manuais da escada (documento 02, 2.8.1) contra as referências do ambiente.

Testa a implementação (avaliador + programas) contra referencias.REGISTRO e referencias.fecho_ref
em todas as grades de n ≤ 3 e em grades aleatórias de n = 4..6 (sementes do piloto): 300 por n em E0
e E0+; 300 no total (100 por n) em E0' e E0'+, cujos programas custam ~30× mais passos (pertence e
uniao viram dobras).
Custo: listas de comprimento > n² (até F(n)) entram em todas as grades de n ≤ 2 e numa fração fixa
(Grade.balde(16) == 0) das grades de n = 3; tarefas sem argumento Grade (descartar, noMaximo,
mesmoNumero) só dependem da grade pela bateria e usam esse mesmo subconjunto de grades de n = 3 e
as 20 primeiras grades aleatórias de cada n ≥ 4.
Também fixa os tamanhos e registra, sem ajustar programas, as discrepâncias com o documento.
"""
import random
import unittest

from fedro_piloto.avaliador import amostras_de_tipo, aplicar, avaliar
from fedro_piloto.dsl import LP, POS, C, F, tamanho
from fedro_piloto.grade import Grade, todas_as_grades
from fedro_piloto import programas_referencia as PR
from fedro_piloto.referencias import REGISTRO, fecho_ref
from fedro_piloto.tradutores import inline

SEMENTE = 10_101  # intervalo do piloto (10 000–19 999)


def grades_teste(aleatorias_por_n):
    gs = [g for n in (1, 2, 3) for g in todas_as_grades(n)]
    rng = random.Random(SEMENTE)
    for n in (4, 5, 6):
        for _ in range(aleatorias_por_n):
            p = rng.choice([0.2, 0.35, 0.5, 0.65])
            gs.append(Grade(n, tuple(1 if rng.random() < p else 0 for _ in range(n * n))))
    return gs


def _pretos(g, ps):
    return tuple(q for q in ps if g.celula(q))


# referências das tarefas de função (Python direto; conjuntos onde a ordem não é especificada)
FUNCOES = {
    "vizPretos": (lambda g, p: _pretos(g, g.vizinhos(p)), lambda a, b: a == b),
    "passo": (lambda g, S: frozenset(S) | {q for s in S for q in g.vizinhos(s) if g.celula(q)},
              lambda a, b: frozenset(a) == b),
    "fecho": (lambda g, S: fecho_ref(g, list(S)), lambda a, b: frozenset(a) == b),
    "componenteDe": (lambda g, p: fecho_ref(g, [p]), lambda a, b: frozenset(a) == b),
    "pretasDe": (lambda g, r: _pretos(g, r), lambda a, b: a == b),
    "descartar": (lambda A, B: B[len(A):], lambda a, b: a == b),
    "noMaximo": (lambda A, B: len(A) <= len(B), lambda a, b: a == b),
    "mesmoNumero": (lambda A, B: len(A) == len(B), lambda a, b: a == b),
}


def _completa(g):
    """Grades em que a bateria inclui listas longas (comprimento > n², até F(n))."""
    return g.n <= 2 or (g.n == 3 and g.balde(16) == 0)


def _listas(g):
    vals = amostras_de_tipo(LP, g)
    if not _completa(g):
        vals = [v for v in vals if len(v) <= g.n * g.n]
    return vals


def _segundo_argumento(p, g):
    """Posições (todas para n ≤ 3; cantos e centro para n ≥ 4) ou listas, conforme o tipo."""
    t = p.tipo[2][1]
    return amostras_de_tipo(POS, g, todas_posicoes=g.n <= 3) if t == POS else _listas(g)


class TestEscadaContraReferencias(unittest.TestCase):
    def _verificar_base(self, base, aleatorias_por_n):
        tb = PR.tabela_referencia(base)
        gs = grades_teste(aleatorias_por_n)
        contagem_n = {}
        valores = {}
        for p in PR.ESCADA:
            with self.subTest(base=base, programa=p.nome):
                erros = []
                for g in gs:
                    if (p.nome, g.n) not in valores:
                        valores[(p.nome, g.n)] = avaliar(C(p.nome), {}, g.n, None, tb)
                    v = valores[(p.nome, g.n)]
                    if p.conceito_ref:
                        obtido = v(g)
                        esperado = REGISTRO[p.conceito_ref].rotulo(g)
                        if p.nome == "NenhumaIsolada" and g.contagem_pretas() == 0:
                            self.assertIs(obtido, True)       # discrepância documentada
                            self.assertIs(esperado, False)
                            continue
                        if obtido != esperado:
                            erros.append(g.texto())
                    else:
                        ref, igual = FUNCOES[p.nome]
                        if p.tipo[1][0] == "Grade":
                            for x in _segundo_argumento(p, g):
                                if not igual(aplicar(v, g, x), ref(g, x)):
                                    erros.append((g.texto(), x))
                        else:  # LP → LP → ·: a grade só entra pela bateria
                            k = contagem_n[(p.nome, g.n)] = contagem_n.get((p.nome, g.n), 0) + 1
                            if g.n == 3 and not _completa(g) or g.n >= 4 and k > 20:
                                continue
                            vals = _listas(g)
                            for A in vals:
                                for B in vals:
                                    if not igual(aplicar(v, A, B), ref(A, B)):
                                        erros.append((g.texto(), A, B))
                    if len(erros) >= 3:
                        break
                self.assertEqual(erros, [])

    def test_E0(self):
        self._verificar_base("E0", 300)

    def test_E0p(self):
        self._verificar_base("E0p", 100)

    def test_E0mais(self):
        self._verificar_base("E0mais", 300)

    def test_E0pmais(self):
        self._verificar_base("E0pmais", 100)

    def test_nenhuma_isolada_corrigida(self):
        from fedro_piloto.dsl import entrada_biblioteca, parse
        tb = PR.tabela_referencia("E0")
        tb.adicionar(entrada_biblioteca("NenhumaIsoladaCorrigida", parse(PR.NENHUMA_ISOLADA_CORRIGIDA.texto_E0),
                                        "manual-teste", tb))
        self.assertEqual(tamanho(parse(PR.NENHUMA_ISOLADA_CORRIGIDA.texto_E0)), 15)
        for g in grades_teste(100):
            self.assertEqual(avaliar(C("NenhumaIsoladaCorrigida"), {}, g.n, None, tb)(g),
                             REGISTRO["NenhumaIsolada"].rotulo(g), g.texto())


class TestTamanhos(unittest.TestCase):
    def test_tamanhos_contra_documento(self):
        bib = PR.biblioteca_manual("E0")
        for p in PR.ESCADA:
            t = PR.termo(p, "E0")
            calc = tamanho(t)
            disc = PR.DISCREPANCIAS_DOC.get((p.nome, "com_biblioteca"))
            if disc:
                self.assertEqual((p.tamanho_doc, calc), (disc["doc"], disc["calculado"]), p.nome)
            else:
                self.assertEqual(calc, p.tamanho_doc, p.nome)
            anteriores = {k: v for k, v in bib.items() if list(bib).index(k) < list(bib).index(p.nome)}
            bruto = tamanho(inline(t, anteriores))
            if p.tamanho_bruto_doc is not None:
                disc = PR.DISCREPANCIAS_DOC.get((p.nome, "bruto"))
                if disc:
                    self.assertEqual((p.tamanho_bruto_doc, bruto), (disc["doc"], disc["calculado"]), p.nome)
                else:
                    self.assertEqual(bruto, p.tamanho_bruto_doc, p.nome)
            else:
                self.assertEqual(bruto, PR.BRUTOS_CALCULADOS_E0[p.nome], p.nome)

    def test_tamanhos_outras_bases(self):
        tam = lambda nome, base: tamanho(PR.termo(PR.POR_NOME[nome], base))
        self.assertEqual(tam("descartar", "E0p"), 9)
        self.assertEqual(tam("descartar", "E0mais"), 9)
        self.assertEqual(tam("fecho", "E0mais"), 4)
        self.assertEqual(tam("fecho", "E0pmais"), 4)
        self.assertEqual(tam("fecho", "E0p"), PR.DISCREPANCIAS_DOC[("fecho", "E0p")]["calculado"])


if __name__ == "__main__":
    unittest.main()
