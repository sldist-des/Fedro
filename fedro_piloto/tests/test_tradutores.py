"""Testes de tradutores.py: U16 (τ, τ' por primitiva) e U17 (inlining).

São testes AMOSTRAIS da implementação contra Sem_n (todas as grades de n ≤ 3 e uma bateria fixa
de argumentos, inclusive funcionais e listas de comprimento F(n)). Não são a prova por primitiva
exigida pelo pré-registro (documento 02, 2.3.4) e não a substituem.
"""
import random
import unittest

from fedro_piloto.avaliador import Contador, aplicar, avaliar
from fedro_piloto.dsl import (E0, E0MAIS, E0P, E0PMAIS, FUN, GRADE, LP, POS, AP, C, LAM, V, F, constantes,
                              parse, tamanho, tipo_de)
from fedro_piloto.grade import Grade, todas_as_grades
from fedro_piloto import programas_referencia as PR
from fedro_piloto.tradutores import (TAU, TAU_INV, _tau_inv_dobra_ingenua, beta_segura, comparar_denotacoes,
                                     constante_c, constante_c_linha, inline, substituir, tau, tau_inv,
                                     verificar_lema_inlining)

GRADES_ATE_3 = [g for n in (1, 2, 3) for g in todas_as_grades(n)]
# para primitivas cujo tipo não contém Grade, a denotação não depende da grade: a grade só varia a
# bateria; usa-se um subconjunto fixo (todas para n ≤ 2, 32 sorteadas com semente fixa para n = 3)
_rng = random.Random(10_016)
GRADES_SEM_GRADE = ([g for n in (1, 2) for g in todas_as_grades(n)]
                    + _rng.sample(list(todas_as_grades(3)), 32))


def _contem_grade(t):
    if t == GRADE:
        return True
    return len(t) > 1 and any(isinstance(x, tuple) and _contem_grade(x) for x in t[1:])


class U16Traducoes(unittest.TestCase):
    def _verificar(self, origem, traduzir, destino):
        for p in origem:
            with self.subTest(primitiva=p.nome):
                t = traduzir(C(p.nome))
                self.assertTrue(all(c in destino for c in constantes(t)), p.nome)
                self.assertEqual(tipo_de(t, {}, destino), p.tipo)
                if p.aridade == 0:
                    for n in (1, 2, 3):
                        self.assertEqual(avaliar(t, {}, n), avaliar(C(p.nome), {}, n))
                    continue
                grades = GRADES_ATE_3 if _contem_grade(p.tipo) else GRADES_SEM_GRADE
                lim = 12 if _contem_grade(p.tipo) else 400
                disc = comparar_denotacoes(C(p.nome), t, p.tipo, grades, max_combinacoes=lim)
                self.assertEqual(disc[:3], [], p.nome)

    def test_U16_tau_E0_para_E0p(self):
        self._verificar(E0, tau, E0P)

    def test_U16_tau_inv_E0p_para_E0(self):
        self._verificar(E0P, tau_inv, E0)

    def test_U16_variantes_mais(self):
        for p in E0MAIS:
            t = tau(C(p.nome), mais=True)
            self.assertTrue(all(c in E0PMAIS for c in constantes(t)), p.nome)
            self.assertEqual(tipo_de(t, {}, E0PMAIS), p.tipo)
        for p in E0PMAIS:
            t = tau_inv(C(p.nome), mais=True)
            self.assertTrue(all(c in E0MAIS for c in constantes(t)), p.nome)
            self.assertEqual(tipo_de(t, {}, E0MAIS), p.tipo)
        self.assertEqual(tau(C("ateFixo@P"), mais=True), C("ateFixo@P"))
        self.assertEqual(tau_inv(C("dobraR@P>LP"), mais=True), C("dobraR@P>LP"))

    def test_constantes_c(self):
        self.assertEqual(constante_c(), 22)       # diferenca
        self.assertEqual(constante_c_linha(), 20)  # dobraR via fix (com antecipação)
        for p in PR.ESCADA:
            t = PR.termo(p, "E0")
            self.assertLessEqual(tamanho(tau(t)), constante_c() * tamanho(t))
            t2 = tau(t)
            self.assertLessEqual(tamanho(tau_inv(t2)), constante_c_linha() * tamanho(t2))

    def test_homomorfismo_preserva_denotacao_da_escada(self):
        """τ e τ'∘τ aplicados a programas inteiros da escada (n ≤ 2, todas as grades)."""
        tb0 = PR.tabela_referencia("E0")
        grades = [g for n in (1, 2) for g in todas_as_grades(n)]
        for p in PR.ESCADA:
            if p.conceito_ref is None:
                continue
            t = PR.termo(p, "E0")
            for u in (tau(t), tau_inv(tau(t))):
                self.assertEqual(comparar_denotacoes(t, u, p.tipo, grades, tb0, tb0), [], p.nome)

    def test_desvio_tau_inv_dobra_ingenua(self):
        """A tradução ingênua de dobraR por fix (m+1 níveis) erra quando |L| = F(n)."""
        ingenua = parse(_tau_inv_dobra_ingenua("P", "B"))
        correta = TAU_INV["dobraR@P>B"]
        f_e = lambda x: lambda b: b  # dobra com z = verdadeiro devolve z
        for n in (1, 2):
            l = tuple(Grade.vazia(n).posicoes()) * F(n)
            l = l[:F(n)]
            self.assertIs(aplicar(avaliar(C("dobraR@P>B"), {}, n), f_e, True, l), True)
            self.assertIs(aplicar(avaliar(correta, {}, n), f_e, True, l), True)
            self.assertIs(aplicar(avaliar(ingenua, {}, n), f_e, True, l), False)  # padrão falso
            self.assertIs(aplicar(avaliar(ingenua, {}, n), f_e, True, l[:-1]), True)


class U17Inlining(unittest.TestCase):
    def test_U17_escada(self):
        grades = GRADES_ATE_3
        for base in ("E0", "E0p", "E0mais", "E0pmais"):
            tb = PR.tabela_referencia(base)
            nomes = [p.nome for p in PR.ESCADA]
            for i, p in enumerate(PR.ESCADA):
                bib = PR.biblioteca_manual(base, ate=p.nome)
                t = PR.termo(p, base)
                for modo in ("segura", "nenhuma"):
                    with self.subTest(base=base, programa=p.nome, beta=modo):
                        rel = verificar_lema_inlining(t, bib, beta=modo)
                        self.assertTrue(rel.ok)
                        self.assertLessEqual(rel.tamanho_final, rel.limite)
                        self.assertFalse(set(constantes(rel.termo)) & set(nomes))
                        self.assertTrue(all(c in tb for c in constantes(rel.termo)))
                        self.assertEqual(tipo_de(rel.termo, {}, tb), p.tipo)
                        if modo == "nenhuma":
                            lim_exato = tamanho(t) + sum(s.ocorrencias * (s.tamanho_entrada - 1) for s in rel.passos)
                            self.assertEqual(rel.tamanho_final, lim_exato)
                        if modo == "segura" or base == "E0":
                            gs = grades if base in ("E0", "E0mais") else grades[:18] + grades[18::16]
                            disc = comparar_denotacoes(C(p.nome), rel.termo, p.tipo, gs, tb, None,
                                                       max_combinacoes=6)
                            self.assertEqual(disc[:2], [])

    def test_captura_evitada(self):
        # (λx. λp. f x p)[x := p] não pode capturar p
        t = LAM("p", POS, AP(V("f"), V("x"), V("p")))
        r = substituir(t, "x", V("p"))
        self.assertEqual(r[0], "lam")
        self.assertNotEqual(r[1], "p")
        self.assertEqual(r[3], AP(V("f"), V("p"), V(r[1])))
        # inlining de vizPretos com argumento chamado p e binder interno p
        bib = {"vizPretos": PR.termo(PR.POR_NOME["vizPretos"])}
        u = parse(r"(\ (q Pos) (g Grade) (vizPretos g q))")
        self.assertEqual(inline(u, bib), parse(r"(\ (q Pos) (g Grade) (filtrar@P (celula g) (vizinhos g q)))"))
        w = parse(r"(\ (p Pos) (g Grade) ((\ (g Grade) (p Pos) (vizPretos g p)) g p))")
        r2 = inline(w, bib)
        self.assertEqual(r2, parse(r"(\ (p Pos) (g Grade) (filtrar@P (celula g) (vizinhos g p)))"))

    def test_beta_segura_nao_aumenta(self):
        bib = PR.biblioteca_manual("E0")
        for p in PR.ESCADA:
            t = PR.termo(p, "E0")
            pura = inline(t, bib, beta="nenhuma")
            self.assertLessEqual(tamanho(beta_segura(pura)), tamanho(pura))

    def test_biblioteca_mal_ordenada(self):
        bib = {"b": parse(r"(\ (g Grade) (a g))"), "a": parse(r"(\ (g Grade) (pretas g))")}
        with self.assertRaises(ValueError):
            inline(parse("b"), bib)


if __name__ == "__main__":
    unittest.main()
