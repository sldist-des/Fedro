"""Testes de avaliador.py: U11, U12, U13 e propriedades de Sem_n (testam a implementação)."""
import dataclasses
import unittest

from fedro_piloto.avaliador import Contador, OrcamentoEsgotado, amostras_de_tipo, aplicar, avaliar
from fedro_piloto.dsl import BOOL, FUN, GRADE, LLP, LP, POS, C, F, padrao, parse
from fedro_piloto.grade import Grade
from fedro_piloto.medidas import MedicaoReal, medir
from fedro_piloto import programas_referencia as PR
from fedro_piloto.referencias import fecho_ref
from fedro_piloto.tradutores import TAU_INV


def _ciclo(base, k):
    out = []
    while len(out) < k:
        out.extend(base)
    return tuple(out[:k])


class U11Fix(unittest.TestCase):
    def test_U11_fix_identidade_bool_n3(self):
        c = Contador()
        v = avaliar(parse(r"(fix (\ (x Bool) x))"), {}, 3, c)
        self.assertIs(v, False)
        self.assertEqual(c.desdobramentos_fix, F(3))
        self.assertEqual(F(3), 81)
        self.assertEqual(c.profundidade_fix_max, 81)
        # 1 (fix) + 1 (λ) + 81 avaliações do corpo `x`; valor fixado, estável entre execuções
        self.assertEqual(c.passos, 83)
        c2 = Contador()
        avaliar(parse(r"(fix (\ (x Bool) x))"), {}, 3, c2)
        self.assertEqual(c.como_dict(), c2.como_dict())

    def test_fix_primeira_ordem_outros_tipos(self):
        self.assertEqual(avaliar(parse(r"(fix (\ (x LP) x))"), {}, 2), ())
        self.assertEqual(avaliar(parse(r"(fix (\ (x Pos) x))"), {}, 2), (1, 1))
        # f^{F(n)}(padrão): nao aplicado 81 vezes a falso = verdadeiro (81 ímpar)
        self.assertIs(avaliar(parse(r"(fix (\ (x Bool) (nao x)))"), {}, 3), True)
        self.assertIs(avaliar(parse(r"(fix (\ (x Bool) (nao x)))"), {}, 2), False)  # 16 par
        # cresce uma lista: cons (1,1) iterado F(n) vezes, truncado em F(n)
        v = avaliar(parse(r"(\ (g Grade) (fix (\ (x LP) (cons@P (cabeca@P (posicoes g)) x))))"), {}, 2)
        self.assertEqual(len(v(Grade.vazia(2))), F(2))

    def test_fix_funcional_preguicoso_descartar_6x6(self):
        g = Grade.vazia(6)
        pos = tuple(g.posicoes())
        c = Contador()
        d = avaliar(PR.termo(PR.POR_NOME["descartar"]), {}, 6, c)
        self.assertEqual(aplicar(d, pos, pos), ())
        self.assertEqual(aplicar(d, pos[:10], pos), pos[10:])
        self.assertEqual(c.profundidade_fix_max, 37)  # 36 elementos + o nível que vê a lista vazia
        self.assertLess(c.desdobramentos_fix, 100)  # preguiçoso: nada perto de F(6) = 1296

    def test_fecho_6x6_serpentina(self):
        linhas = ["######", ".....#", "######", "#.....", "######", ".....#"]
        g = Grade.de_linhas([[1 if ch == "#" else 0 for ch in l] for l in linhas])
        tb = PR.tabela_referencia("E0")
        c = Contador()
        comp = avaliar(C("componenteDe"), {}, 6, c, tb)
        r = aplicar(comp, g, (1, 1))
        self.assertEqual(frozenset(r), fecho_ref(g, [(1, 1)]))
        self.assertEqual(len(set(r)), g.contagem_pretas())
        self.assertGreaterEqual(c.profundidade_fix_max, g.contagem_pretas() - 1)
        self.assertLessEqual(c.profundidade_fix_max, 36)

    def test_recursao_profunda_lista_de_comprimento_F(self):
        """τ'(dobraR) (via fix) sobre lista de comprimento F(4) = 256: recursão Python profunda."""
        n = 4
        g = Grade.vazia(n)
        l = _ciclo(tuple(g.posicoes()), F(n))
        dob = avaliar(TAU_INV["dobraR@P>B"], {}, n)
        todos_verdade = aplicar(dob, lambda x: lambda b: b, True, l)
        self.assertIs(todos_verdade, True)


class U12Truncamento(unittest.TestCase):
    def test_U12_concatenar(self):
        for n in (1, 2, 3):
            g = Grade.vazia(n)
            a = _ciclo(tuple(g.posicoes()), F(n))
            b = tuple(reversed(a))
            v = avaliar(C("concatenar@P"), {}, n)
            r = aplicar(v, a, b)
            self.assertEqual(len(r), F(n))
            self.assertEqual(r, a)

    def test_cons_juntar_uniao_truncam(self):
        n = 2
        g = Grade.vazia(n)
        a = _ciclo(tuple(g.posicoes()), F(n))
        self.assertEqual(aplicar(avaliar(C("cons@P"), {}, n), (2, 2), a), ((2, 2),) + a[:-1])
        self.assertEqual(len(aplicar(avaliar(C("juntar"), {}, n), (a, a, a))), F(n))
        lin = tuple(tuple(l) for l in g.linhas())
        self.assertEqual(len(aplicar(avaliar(C("cons@LP"), {}, n), (), _ciclo(lin, F(n)))), F(n))
        u = aplicar(avaliar(C("uniao"), {}, n), (), a)
        self.assertEqual(set(u), set(a))  # sem duplicatas vindas de B
        self.assertEqual(len(u), 4)


class U13Passos(unittest.TestCase):
    def test_U13_algum_celula_posicoes(self):
        g = Grade.vazia(3)
        t = parse("(algum@P (celula g) (posicoes g))", livres=["g"])
        resultados = []
        for _ in range(2):
            c = Contador()
            v = avaliar(t, {"g": g}, 3, c)
            resultados.append((v, c.como_dict()))
        self.assertIs(resultados[0][0], False)
        self.assertEqual(resultados[0], resultados[1])
        # 9 nós + posicoes (1) + algum (1) + 9 aplicações saturadas de celula = 20 (valor fixado)
        self.assertEqual(resultados[0][1]["passos"], 20)
        self.assertEqual(resultados[0][1]["aplicacoes_primitivas"], 11)


class TestSemantica(unittest.TestCase):
    def test_padroes_e_totalidade(self):
        self.assertEqual(avaliar(parse("(cabeca@P vazio@P)"), {}, 3), (1, 1))
        self.assertEqual(avaliar(parse("(cabeca@LP vazio@LP)"), {}, 3), ())
        self.assertEqual(avaliar(parse("(cauda@P vazio@P)"), {}, 3), ())
        self.assertEqual(padrao(GRADE, 2), Grade.vazia(2))
        self.assertEqual(padrao(FUN(POS, LP, BOOL), 2)((1, 1))(()), False)

    def test_se_preguicoso_so_muda_passos(self):
        caro = "(juntar (mapear@P>LP (vizinhos g) (posicoes g)))"
        t = parse(f"(se@LP verdadeiro (pretas g) {caro})", livres=["g"])
        g = Grade.de_texto("3:101010101")
        c1 = Contador()
        v1 = avaliar(t, {"g": g}, 3, c1)
        c2 = Contador()
        v2 = avaliar(parse(f"((\\ (b Bool) (se@LP b (pretas g) {caro})) verdadeiro)", livres=["g"]), {"g": g}, 3, c2)
        self.assertEqual(v1, tuple(g.pretas()))
        self.assertEqual(v1, v2)
        # se parcialmente aplicado como valor (estrito) dá o mesmo valor
        c3 = Contador()
        v3 = avaliar(parse(f"((\\ (s (-> Bool LP LP LP)) (s verdadeiro (pretas g) {caro})) se@LP)", livres=["g"]),
                     {"g": g}, 3, c3)
        self.assertEqual(v3, v1)
        self.assertGreater(c3.passos, c1.passos)

    def test_orcamento_de_busca(self):
        t = parse(r"(fix (\ (x Bool) x))")
        with self.assertRaises(OrcamentoEsgotado):
            avaliar(t, {}, 3, orcamento_passos=50)
        c = Contador(orcamento_passos=1000)
        self.assertIs(avaliar(t, {}, 3, c), False)
        self.assertEqual(c.passos, 83)

    def test_biblioteca_resolvida_pela_tabela(self):
        tb = PR.tabela_referencia("E0")
        g = Grade.de_texto("3:110000001")
        self.assertIs(avaliar(C("ParAdjacente"), {}, 3, None, tb)(g), True)
        self.assertIs(avaliar(C("UmComponente"), {}, 3, None, tb)(g), False)
        with self.assertRaises(KeyError):
            avaliar(C("ParAdjacente"), {}, 3)  # sem tabela, constante de biblioteca é desconhecida

    def test_amostras_bem_formadas(self):
        for g in (Grade.de_texto("1:1"), Grade.de_texto("2:1001"), Grade.de_texto("3:101010101")):
            for t in (BOOL, POS, GRADE, LP, LLP):
                for v in amostras_de_tipo(t, g):
                    if t in (LP, LLP):  # domínio de Sem_n: comprimento ≤ F(n)
                        self.assertLessEqual(len(v), F(g.n))
                    if t == LLP:
                        self.assertTrue(all(len(x) <= F(g.n) for x in v))


class TestSeparacaoContadorMedicao(unittest.TestCase):
    def test_estruturas_distintas(self):
        c = Contador()
        campos = set(c.como_dict())
        self.assertFalse(any("tempo" in k or "memoria" in k for k in campos))
        nomes_medicao = {f.name for f in dataclasses.fields(MedicaoReal)}
        self.assertFalse(nomes_medicao & campos)
        with medir("x") as m:
            avaliar(parse(r"(fix (\ (x Bool) x))"), {}, 3, c)
        self.assertGreaterEqual(m.tempo_parede_s, 0.0)
        self.assertGreater(m.memoria_pico_kib, 0)


if __name__ == "__main__":
    unittest.main()
