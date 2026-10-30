"""U1-U5 (documento 03, seção 5): implementações de referência.

Redução declarada: U3 usa 10^4 grades naturais por n (5..9) em vez de 10^5, mais um
complemento construtivo (positivos e negativos emparelhados) para cobrir conceitos raros.
"""
import random
import unittest

from fedro_piloto.grade import Grade, todas_as_grades
from fedro_piloto.referencias import (REGISTRO, componentes_a, componentes_b, regiao,
                                      transformar)
from fedro_piloto import geradores as G

AMOSTRAS_U3 = 10_000   # desvio declarado: 10^5 no documento 03
AMOSTRAS_U4 = 1_000


def _discordancias(c, grades):
    return [g.serializar() for g in grades if c.ref_a(g) != c.ref_b(g)]


class U1Exemplo(unittest.TestCase):
    def test_u1(self):
        g = Grade.de_linhas([[1, 1, 0], [0, 0, 0], [0, 0, 1]])
        self.assertEqual(len(componentes_a(g)), 2)
        self.assertEqual(len(componentes_b(g)), 2)
        self.assertFalse(REGISTRO["UmComponente"].rotulo(g))
        self.assertTrue(REGISTRO["DoisSeparados"].rotulo(g))
        self.assertTrue(REGISTRO["MaiorTocaBorda"].rotulo(g))


class U2Exaustivo(unittest.TestCase):
    def test_u2_n1_a_4(self):
        for n in range(1, 5):
            grades = list(todas_as_grades(n))
            for c in REGISTRO.values():
                with self.subTest(n=n, conceito=c.nome):
                    self.assertEqual(_discordancias(c, grades), [])


class U3Amostral(unittest.TestCase):
    def test_u3_n5_a_9(self):
        rng = G.rng_piloto(10_003)
        for n in range(5, 10):
            grades = [G.amostra_natural(n, rng) for _ in range(AMOSTRAS_U3)]
            # complemento construtivo: positivos e negativos emparelhados de cada conceito
            for c in REGISTRO.values():
                for _ in range(10):
                    g = G.gerar_positivo(c, n, None, rng, tentativas=200)
                    if g is None:
                        continue
                    grades.append(g)
                    neg = G.negativo_emparelhado(g, c, rng, None, "auto", tentativas_permutacao=30, L=100)
                    if neg is not None:
                        grades.append(neg[0])
            for c in REGISTRO.values():
                with self.subTest(n=n, conceito=c.nome):
                    self.assertEqual(_discordancias(c, grades), [])


class U4Invariancias(unittest.TestCase):
    def test_u4(self):
        rng = G.rng_piloto(10_004)
        for c in REGISTRO.values():
            grades = []
            while len(grades) < AMOSTRAS_U4:
                n = rng.randint(3, 6)
                if len(grades) % 2:
                    grades.append(G.amostra_natural(n, rng))
                else:
                    g = G.gerar_positivo(c, n, None, rng, tentativas=50)
                    grades.append(g if g is not None else G.amostra_natural(n, rng))
            for t in c.invariancias:
                with self.subTest(conceito=c.nome, transformacao=t):
                    falhas = [g.serializar() for g in grades if c.rotulo(g) != c.rotulo(transformar(g, t))]
                    self.assertEqual(falhas, [])

    def test_u4_transformacao_nao_declarada_pode_mudar_rotulo(self):
        # controle do próprio teste: TopoCheio não é invariante por transposição
        g = Grade.de_texto("###/.../...")
        c = REGISTRO["TopoCheio"]
        self.assertNotIn("transp", c.invariancias)
        self.assertNotEqual(c.rotulo(g), c.rotulo(transformar(g, "transp")))


# Valores de borda fixados aqui (U5); a confirmar no pré-registro. Convenções:
# TodosComp*, TodosMesmoTamanho e MaiorTocaBorda exigem pelo menos um componente;
# NoMaximoDois, NumCompIgual*, MaiorCompPeloMenosLinha1 e as comparações de cardinalidade
# valem na grade vazia (0 = 0, 0 <= 2, 0 >= 0); ColunaDoisVazia é falso para n = 1.
_SEMPRE_V_VAZIA = {"ColunaDoisVazia", "NoMaximoDois", "LinhasIguais", "ColunasIguais",
                   "NumCompIgualLinha1", "NumCompIgualCol1", "MaiorCompPeloMenosLinha1"}
_SEMPRE_V_VAZIA |= {k for k in REGISTRO if k.startswith(("Igual_", "NoMax_"))}

_CHEIA_3_FALSOS = {"ColunaDoisVazia", "DoisSeparados", "TresComponentes", "PeloMenosDois",
                   "ExisteCompReto", "TodosCompReto", "NumCompIgualLinha1", "NumCompIgualCol1"}

_UM_PRETO_N1_FALSOS = {"ParAdjacente", "ColunaDoisVazia", "DoisSeparados", "TresComponentes",
                       "PeloMenosDois", "ExisteCompMin3", "NenhumaIsolada"}


class U5Bordas(unittest.TestCase):
    def _verificar(self, g, verdadeiros):
        for nome, c in REGISTRO.items():
            with self.subTest(grade=g.serializar(), conceito=nome):
                self.assertEqual(c.rotulo(g), nome in verdadeiros)

    def test_vazia(self):
        for n in (2, 3, 6):
            self._verificar(Grade.vazia(n), _SEMPRE_V_VAZIA)

    def test_cheia(self):
        g = Grade(3, (1,) * 9)
        self._verificar(g, set(REGISTRO) - _CHEIA_3_FALSOS)

    def test_n1(self):
        self._verificar(Grade.de_texto("1:0"), _SEMPRE_V_VAZIA - {"ColunaDoisVazia"})
        self._verificar(Grade.de_texto("1:1"), set(REGISTRO) - _UM_PRETO_N1_FALSOS)

    def test_regioes_n1_se_sobrepoem(self):
        g = Grade.vazia(1)
        self.assertEqual(regiao("linha1", g), regiao("linhaN", g))
        self.assertEqual(regiao("metadeEsq", g), [])
        self.assertEqual(regiao("metadeDir", g), [])

    def test_metades_excluem_coluna_central(self):
        g = Grade.vazia(5)
        cols_e = {j for _, j in regiao("metadeEsq", g)}
        cols_d = {j for _, j in regiao("metadeDir", g)}
        self.assertEqual(cols_e, {1, 2})
        self.assertEqual(cols_d, {4, 5})


if __name__ == "__main__":
    unittest.main()
