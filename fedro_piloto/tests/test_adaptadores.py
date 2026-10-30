"""U18 (documento 03, seção 5) e testes dos adaptadores de portador (documento 02, 2.11.1).

U18: sequência 1101110 -> componentes = corridas {1,2}, {4,5,6}; grafo com 4 nós, arestas 1–2 e
3–4, nós pretos 1, 2, 3 -> componentes {1,2}, {3}.
Além disso: os programas da escada (manual-teste, só como teste) são avaliados SEM MODIFICAÇÃO
nos portadores, com a tabela adaptada, e concordam com os componentes de referência.
"""
import itertools
import unittest

from fedro_piloto import programas_referencia as PR
from fedro_piloto.adaptadores import (ADAPTADORES, GRAFO, PRIMITIVAS_PORTADOR, SEQUENCIA, Grafo,
                                      PrimitivaNaoDefinida, Sequencia, aplicar_no_portador,
                                      componentes_grafo_a, componentes_grafo_b, componentes_referencia,
                                      componentes_sequencia_a, componentes_sequencia_b, fecho_referencia,
                                      indices, n_semantica, pos)
from fedro_piloto.dsl import E0, BASES, F, parse
from fedro_piloto.geradores import rng_piloto
from fedro_piloto.grade import Grade

TABELAS = {b: PR.tabela_referencia(b) for b in ("E0", "E0p", "E0mais", "E0pmais")}
COMPONENTE_DE = parse("componenteDe")


def _componentes_dsl(portador, base="E0"):
    """Componentes pelo programa componenteDe da escada, avaliado no portador."""
    out = set()
    for p in portador.pretas():
        out.add(indices(aplicar_no_portador(COMPONENTE_DE, portador, p, tabela=TABELAS[base])))
    return out


def _grafo_aleatorio(rng, num_nos):
    arestas = [(a, b) for a in range(1, num_nos + 1) for b in range(a + 1, num_nos + 1) if rng.random() < 0.35]
    pretos = [i for i in range(1, num_nos + 1) if rng.random() < 0.6]
    return Grafo.de_lista(num_nos, arestas, pretos)


class TestU18(unittest.TestCase):
    def test_u18_sequencia(self):
        s = Sequencia.de_texto("1101110")
        esperado = (frozenset({1, 2}), frozenset({4, 5, 6}))
        self.assertEqual(componentes_referencia(s), esperado)
        self.assertEqual(set(componentes_sequencia_a(s)), set(esperado))
        self.assertEqual(set(componentes_sequencia_b(s)), set(esperado))
        for base in TABELAS:
            self.assertEqual(_componentes_dsl(s, base), set(esperado), base)

    def test_u18_grafo(self):
        gr = Grafo.de_lista(4, [(1, 2), (3, 4)], [1, 2, 3])
        esperado = (frozenset({1, 2}), frozenset({3}))
        self.assertEqual(componentes_referencia(gr), esperado)
        self.assertEqual(set(componentes_grafo_a(gr)), set(esperado))
        self.assertEqual(set(componentes_grafo_b(gr)), set(esperado))
        for base in TABELAS:
            self.assertEqual(_componentes_dsl(gr, base), set(esperado), base)


class TestReferenciasDosPortadores(unittest.TestCase):
    def test_sequencias_exaustivo_ate_12(self):
        for m in range(1, 13):
            for bits in itertools.product((0, 1), repeat=m):
                s = Sequencia(bits)
                a, b = componentes_sequencia_a(s), componentes_sequencia_b(s)
                self.assertEqual(set(a), set(b), s.texto())
                self.assertEqual(sum(map(len, a)), sum(bits))
                self.assertEqual(set().union(*a) if a else set(), {i + 1 for i, x in enumerate(bits) if x})

    def test_grafos_aleatorios(self):
        rng = rng_piloto(10_180)
        for _ in range(300):
            gr = _grafo_aleatorio(rng, rng.randint(1, 9))
            a, b = componentes_grafo_a(gr), componentes_grafo_b(gr)
            self.assertEqual(set(a), set(b))
            for c in a:
                self.assertEqual(fecho_referencia(gr, [min(c)]), c)


class TestProgramasNosPortadores(unittest.TestCase):
    """Programas da escada avaliados sem modificação (manual-teste: só verificação)."""

    def _conferir(self, portador, base="E0"):
        tab = TABELAS[base]
        comps = componentes_referencia(portador)
        self.assertEqual(_componentes_dsl(portador, base), set(comps))
        ex = aplicar_no_portador(parse("ExistePreta"), portador, tabela=tab)
        par = aplicar_no_portador(parse("ParAdjacente"), portador, tabela=tab)
        nen = aplicar_no_portador(parse("NenhumaIsolada"), portador, tabela=tab)
        um = aplicar_no_portador(parse("UmComponente"), portador, tabela=tab)
        self.assertEqual(ex, bool(comps))
        self.assertEqual(par, any(len(c) >= 2 for c in comps))
        self.assertEqual(nen, all(len(c) >= 2 for c in comps))   # programa do documento: vácuo na vazia
        self.assertEqual(um, len(comps) == 1)

    def test_todas_as_sequencias_ate_7(self):
        for m in range(1, 8):
            for bits in itertools.product((0, 1), repeat=m):
                self._conferir(Sequencia(bits))

    def test_sequencias_em_E0p_e_E0mais(self):
        for texto in ("1", "0", "10", "1101110", "0110100111", "111111111"):
            for base in ("E0p", "E0mais", "E0pmais"):
                s = Sequencia.de_texto(texto)
                self.assertEqual(_componentes_dsl(s, base), set(componentes_referencia(s)), (texto, base))

    def test_grafos_aleatorios(self):
        rng = rng_piloto(10_181)
        for _ in range(60):
            self._conferir(_grafo_aleatorio(rng, rng.randint(1, 7)))

    def test_degeneracoes_declaradas_em_sequencias(self):
        """2.11.2: LinhasIguais e PrimeiraUltimaIguais degeneram (uma única linha): sempre verdadeiros."""
        for texto in ("0", "1", "1101110", "0001", "1010101"):
            s = Sequencia.de_texto(texto)
            for base in ("E0", "E0p"):
                self.assertTrue(aplicar_no_portador(parse("LinhasIguais"), s, tabela=TABELAS[base]))
            self.assertTrue(aplicar_no_portador(parse("PrimeiraUltimaIguais"), s, tabela=TABELAS["E0"]))

    def test_linhas_e_colunas_indefinidas_em_grafos(self):
        gr = Grafo.de_lista(4, [(1, 2), (3, 4)], [1, 2, 3])
        for nome in ("linhas", "colunas"):
            with self.assertRaises(PrimitivaNaoDefinida):
                aplicar_no_portador(parse(nome), gr, tabela=E0)
        for nome in ("linhaDe", "colunaDe"):
            with self.assertRaises(PrimitivaNaoDefinida):
                aplicar_no_portador(parse(nome), gr, pos(1), tabela=BASES["E0p"])
        for programa in ("LinhasIguais", "PrimeiraUltimaIguais"):
            with self.assertRaises(PrimitivaNaoDefinida):
                aplicar_no_portador(parse(programa), gr, tabela=TABELAS["E0"])
        self.assertEqual(GRAFO.indefinidas, frozenset({"linhas", "colunas", "linhaDe", "colunaDe"}))
        self.assertEqual(SEQUENCIA.indefinidas, frozenset())


class TestTabelaAdaptada(unittest.TestCase):
    def test_so_primitivas_de_portador_mudam(self):
        for tab in (E0, BASES["E0p"], TABELAS["E0"], E0.para_aprendiz()):
            for ad in ADAPTADORES.values():
                t2 = ad.tabela(tab)
                self.assertEqual(t2.uso, tab.uso)
                for p in tab:
                    if p.nome in PRIMITIVAS_PORTADOR:
                        self.assertIsNot(t2[p.nome], p)
                        self.assertEqual(t2[p.nome].tipo, p.tipo)
                    else:
                        self.assertIs(t2[p.nome], p)   # biblioteca e demais primitivas intactas
                for nome in PRIMITIVAS_PORTADOR:      # as 8 sempre presentes (sem recurso à grade)
                    self.assertIn(nome, t2)
        # a tabela de um aprendiz continua de descoberta e sem entradas manual-teste
        t3 = SEQUENCIA.tabela(E0.para_aprendiz())
        self.assertEqual(t3.uso, "descoberta")
        self.assertFalse(any(p.proveniencia == "manual-teste" for p in t3))

    def test_primitivas_totais_e_portadores_nao_trocam(self):
        s = Sequencia.de_texto("101")
        gr = Grafo.de_lista(3, [(1, 3)], [1, 3])
        for port in (s, gr):
            self.assertFalse(port.celula((1, 99)))
            self.assertFalse(port.celula((2, 1)))
            self.assertEqual(port.vizinhos((1, 99)), ())
        self.assertEqual(s.vizinhos(pos(2)), (pos(1), pos(3)))
        self.assertEqual(s.linhas(), ((pos(1), pos(2), pos(3)),))
        self.assertEqual(s.colunas(), ((pos(1),), (pos(2),), (pos(3),)))
        self.assertEqual(gr.vizinhos(pos(1)), (pos(3),))
        with self.assertRaises(TypeError):     # o adaptador de sequência recusa uma grade
            SEQUENCIA.impl("pretas")(None, Grade.vazia(2))
        with self.assertRaises(TypeError):
            GRAFO.impl("pretas")(None, s)

    def test_n_semantica(self):
        for m, n in ((1, 1), (2, 2), (4, 2), (5, 3), (9, 3), (10, 4)):
            s = Sequencia((0,) * m)
            self.assertEqual(n_semantica(s), n)
            self.assertGreaterEqual(F(n_semantica(s)), m * m)

    def test_padrao_pos_e_o_primeiro_elemento(self):
        """cabeca de lista vazia devolve (1,1) = primeiro índice/nó, válido em qualquer portador."""
        gr = Grafo.de_lista(2, [], [])
        v = aplicar_no_portador(parse("(\\ (g Grade) (celula g (cabeca@P (pretas g))))"), gr, tabela=E0)
        self.assertFalse(v)
        self.assertIn((1, 1), gr.posicoes())


if __name__ == "__main__":
    unittest.main()
