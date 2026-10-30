"""Testes de grade.py (fase 0): serialização, hash, balde, vizinhança, transformações."""
import hashlib
import random
import unittest

from fedro_piloto.grade import Grade, chave_minimalidade, todas_as_grades


class TestGrade(unittest.TestCase):
    def test_serializacao_ida_e_volta(self):
        rng = random.Random(10_001)
        for n in range(1, 10):
            g = Grade(n, tuple(rng.randint(0, 1) for _ in range(n * n)))
            self.assertEqual(Grade.de_texto(g.serializar()), g)
            self.assertEqual(Grade.de_texto(g.texto()), g)

    def test_hash_e_balde(self):
        g = Grade.de_texto("2:1001")
        self.assertEqual(g.serializar(), "2:1001")
        self.assertEqual(g.hash_hex(), hashlib.sha256(b"2:1001").hexdigest())
        self.assertEqual(g.balde(100), int(g.hash_hex()[:16], 16) % 100)
        self.assertTrue(0 <= g.balde(100) < 100)

    def test_validacao(self):
        with self.assertRaises(ValueError):
            Grade(2, (0, 1, 0))
        with self.assertRaises(ValueError):
            Grade(1, (2,))

    def test_posicoes_1_based_e_celula(self):
        g = Grade.de_texto("#../.../..#")
        self.assertEqual(g.pretas(), [(1, 1), (3, 3)])
        self.assertEqual(g.celula((1, 1)), 1)
        self.assertEqual(g.celula((2, 2)), 0)
        self.assertEqual(len(g.posicoes()), 9)
        self.assertEqual(g.posicoes()[:3], [(1, 1), (1, 2), (1, 3)])

    def test_vizinhos(self):
        g = Grade.vazia(3)
        self.assertEqual(g.vizinhos((1, 1)), [(2, 1), (1, 2)])
        self.assertEqual(sorted(g.vizinhos((2, 2))), [(1, 2), (2, 1), (2, 3), (3, 2)])
        self.assertEqual(Grade.vazia(1).vizinhos((1, 1)), [])

    def test_transformacoes(self):
        g = Grade.de_texto("##./.../..#")
        self.assertEqual(g.transposta().texto(), "#../#../..#")
        self.assertEqual(g.reflexao_h().texto(), ".##/.../#..")
        self.assertEqual(g.reflexao_v().texto(), "..#/.../##.")
        self.assertEqual(g.rotacao90().texto(), "..#/..#/#..")  # rotação horária
        r = g
        for _ in range(4):
            r = r.rotacao90()
        self.assertEqual(r, g)
        self.assertEqual(g.transposta().transposta(), g)

    def test_trocar_preserva_pretas(self):
        g = Grade.de_texto("#../.../...")
        h = g.trocar((1, 1), (3, 3))
        self.assertEqual(h.pretas(), [(3, 3)])
        self.assertEqual(h.contagem_pretas(), g.contagem_pretas())
        self.assertEqual(g.inverter((2, 2)).contagem_pretas(), 2)

    def test_todas_as_grades(self):
        for n in (1, 2, 3):
            gs = list(todas_as_grades(n))
            self.assertEqual(len(gs), 2 ** (n * n))
            self.assertEqual(len(set(gs)), len(gs))
            self.assertEqual(gs[0], Grade.vazia(n))

    def test_chave_minimalidade(self):
        a = Grade.de_texto("#./..")
        b = Grade.de_texto(".#/..")
        c = Grade.de_texto("##/..")
        self.assertLess(chave_minimalidade(b), chave_minimalidade(a))  # lexicográfica
        self.assertLess(chave_minimalidade(a), chave_minimalidade(c))  # menos pretas
        self.assertLess(chave_minimalidade(c), chave_minimalidade(Grade.vazia(3)))  # n primeiro


if __name__ == "__main__":
    unittest.main()
