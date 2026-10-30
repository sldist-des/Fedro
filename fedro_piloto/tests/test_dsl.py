"""Testes de dsl.py: U14, U15 e estrutura da linguagem (testam a implementação, não provam nada)."""
import unittest

from fedro_piloto.dsl import (BASES, BOOL, E0, E0MAIS, E0P, E0PMAIS, FUN, GENERICAS_E0, GENERICAS_E0MAIS,
                              GENERICAS_E0P, GENERICAS_E0PMAIS, GRADE, INSTANCIAS, LLP, LP, POS, TIPOS_TAREFA,
                              UNIVERSO_TIPOS, AP, C, ErroParse, ErroProveniencia, ErroTipo, FIX, LAM, L,
                              Primitiva, Tabela, V, entrada_biblioteca, exigir_tabela_de_descoberta, imprimir,
                              imprimir_legivel, parse, parse_tipo, tabela_resumo, tamanho, tipo_de, tipo_str)
from fedro_piloto import programas_referencia as PR
from fedro_piloto.tradutores import TAU, TAU_INV


class TestTamanho(unittest.TestCase):
    def test_U14_existe_preta(self):
        t = parse(r"(\ (g Grade) (nao (vazia?@P (pretas g))))")
        self.assertEqual(tamanho(t), 5)

    def test_U15_descartar(self):
        t = parse(r"(fix (\ (rec (-> LP LP LP)) (A LP) (B LP) (se@LP (vazia?@P A) B (rec (cauda@P A) (cauda@P B)))))")
        self.assertEqual(tamanho(t), 13)
        self.assertEqual(tipo_de(t, {}, E0), FUN(LP, LP, LP))

    def test_convencao(self):
        self.assertEqual(tamanho(C("x")), 1)
        self.assertEqual(tamanho(V("x")), 1)
        self.assertEqual(tamanho(AP(C("f"), V("x"), V("y"))), 3)  # aplicações não contam
        self.assertEqual(tamanho(LAM("x", BOOL, V("x"))), 2)
        self.assertEqual(tamanho(FIX(BOOL, LAM("x", BOOL, V("x")))), 3)  # fix = 1 folha


class TestParseImpressao(unittest.TestCase):
    def test_ida_e_volta_escada_e_traducoes(self):
        termos = [PR.termo(p, b) for p in PR.ESCADA for b in ("E0", "E0p", "E0mais", "E0pmais")]
        termos += list(TAU.values()) + list(TAU_INV.values())
        for t in termos:
            self.assertEqual(parse(imprimir(t)), t, imprimir(t))

    def test_lam_alternativas_e_livres(self):
        a = parse(r"(\ (x Bool) (nao x))")
        self.assertEqual(parse("(lam (x Bool) (nao x))"), a)
        self.assertEqual(parse("(λ (x Bool) (nao x))"), a)
        t = parse("(algum@P (celula g) (posicoes g))", livres=["g"])
        self.assertEqual(t[2], AP(C("posicoes"), V("g")))
        self.assertEqual(tipo_de(t, {"g": GRADE}, E0), BOOL)

    def test_fix_com_tipo_explicito(self):
        t = parse(r"(fix Bool (\ (x Bool) x))")
        self.assertEqual(t, FIX(BOOL, LAM("x", BOOL, V("x"))))
        self.assertEqual(imprimir(t), r"(fix (\ (x Bool) x))")

    def test_tipos(self):
        self.assertEqual(parse_tipo("(-> (-> Pos Bool) LP LP)"), FUN(FUN(POS, BOOL), LP, LP))
        self.assertEqual(parse_tipo("(L (L Pos))"), LLP)
        self.assertEqual(tipo_str(FUN(FUN(POS, BOOL), LP, LP)), "(Pos → Bool) → L Pos → L Pos")
        self.assertEqual(tipo_str(LLP), "L (L Pos)")

    def test_erros_de_parse(self):
        for txt in ["(nao", "nao)", "(fix (nao x))", "(\\ (x) x)", "()"]:
            with self.assertRaises(ErroParse, msg=txt):
                parse(txt)

    def test_legivel(self):
        t = PR.termo(PR.POR_NOME["vizPretos"])
        self.assertEqual(imprimir_legivel(t), "λg p. filtrar@P (celula g) (vizinhos g p)")


class TestTipos(unittest.TestCase):
    def test_erros(self):
        with self.assertRaises(ErroTipo):
            tipo_de(parse("(nao (pretas g))", ["g"]), {"g": GRADE}, E0)
        with self.assertRaises(ErroTipo):
            tipo_de(parse("(nao verdadeiro falso)"), {}, E0)
        with self.assertRaises(ErroTipo):
            tipo_de(C("linhaDe"), {}, E0)  # não pertence a E0
        with self.assertRaises(ErroTipo):
            tipo_de(C("mapear@P>LP"), {}, E0P)  # não pertence a E0'
        with self.assertRaises(ErroTipo):
            tipo_de(FIX(LP, LAM("x", BOOL, V("x"))), {}, E0)
        with self.assertRaises(ErroTipo):
            tipo_de(V("x"), {}, E0)

    def test_escada_bem_tipada_em_todas_as_bases(self):
        for b in ("E0", "E0p", "E0mais", "E0pmais"):
            tb = PR.tabela_referencia(b)
            for p in PR.ESCADA:
                self.assertEqual(tipo_de(PR.termo(p, b), {}, tb), p.tipo, (b, p.nome))


class TestTabelas(unittest.TestCase):
    def test_contagem_de_genericas(self):
        self.assertEqual(len(GENERICAS_E0), 29)
        self.assertEqual(len(GENERICAS_E0P), 20)
        for tb, gen in ((E0, GENERICAS_E0), (E0P, GENERICAS_E0P), (E0MAIS, GENERICAS_E0MAIS),
                        (E0PMAIS, GENERICAS_E0PMAIS)):
            self.assertEqual(tb.genericos() | {"fix"}, set(gen), tb.nome)

    def test_proveniencias_de_base(self):
        self.assertTrue(all(p.proveniencia == "E0" for p in E0))
        self.assertTrue(all(p.proveniencia == "E0p" for p in E0P))
        self.assertEqual({p.nome for p in E0MAIS if p.proveniencia == "E0mais"},
                         {p.nome for p in E0MAIS if p.generico in ("ateFixo", "dobraR")})
        self.assertEqual({p.nome for p in E0PMAIS if p.proveniencia == "E0mais"}, {"ateFixo@P"})

    def test_universo_de_tipos(self):
        for b in BASES.values():
            for p in b:
                self.assertIn(p.tipo, UNIVERSO_TIPOS)
        for t in TIPOS_TAREFA + [BOOL, POS, GRADE, LP, LLP]:
            self.assertIn(t, UNIVERSO_TIPOS)
        self.assertNotIn(L(BOOL), UNIVERSO_TIPOS)

    def test_resumo(self):
        r = tabela_resumo()
        for i in INSTANCIAS:
            self.assertIn(f"`{i.nome}`", r)

    def test_base_congelada(self):
        corpo = parse(r"(\ (g Grade) (pretas g))")
        with self.assertRaises(ErroProveniencia):
            E0.adicionar(Primitiva("x", FUN(GRADE, LP), None, "descoberta", corpo=corpo))


class TestProveniencia(unittest.TestCase):
    def _manual(self):
        return entrada_biblioteca("vizPretos", PR.termo(PR.POR_NOME["vizPretos"]), "manual-teste", E0)

    def _descoberta(self, nome="f1"):
        return entrada_biblioteca(nome, parse(r"(\ (g Grade) (nao (vazia?@P (pretas g))))"), "descoberta", E0)

    def test_aprendiz_recusa_manual(self):
        t = E0.para_aprendiz()
        self.assertTrue(t.modo_descoberta)
        with self.assertRaises(ErroProveniencia):
            t.adicionar(self._manual())
        # o rótulo "descoberta" sozinho não basta: sem certificado da Biblioteca autônoma é recusado
        with self.assertRaises(ErroProveniencia):
            t.adicionar(self._descoberta())
        p = self._descoberta("f2")
        p.certificado = object()           # certificado forjado também não verifica
        with self.assertRaises(ErroProveniencia):
            t.adicionar(p)
        with self.assertRaises(ErroProveniencia):
            Tabela("forjada", list(E0) + [self._descoberta("f3")], "descoberta")
        exigir_tabela_de_descoberta(t)

    def test_referencia_nao_origina_aprendiz(self):
        ref = PR.tabela_referencia("E0")
        self.assertEqual(ref.uso, "referencia")
        with self.assertRaises(ErroProveniencia):
            ref.para_aprendiz()
        with self.assertRaises(ErroProveniencia):
            exigir_tabela_de_descoberta(ref)
        with self.assertRaises(ErroProveniencia):
            Tabela("x", list(E0) + [self._manual()], "descoberta")

    def test_todas_as_entradas_manuais_marcadas(self):
        for b in ("E0", "E0p", "E0mais", "E0pmais"):
            for p in PR.entradas_manuais(b):
                self.assertEqual(p.proveniencia, "manual-teste")
                self.assertEqual(p.categoria(), "manual-teste")

    def test_reutilizacao(self):
        d = self._descoberta()
        self.assertEqual(d.categoria(), "descoberta")
        d.registrar_reutilizacao("tarefa:ParAdjacente")
        self.assertEqual(d.categoria(), "descoberta-reutilizada")
        self.assertTrue(d.eh_reutilizada)
        with self.assertRaises(ErroProveniencia):
            self._manual().registrar_reutilizacao("x")

    def test_validacao_primitiva(self):
        with self.assertRaises(ErroProveniencia):
            Primitiva("x", BOOL, None, "E0")  # fornecida sem impl
        with self.assertRaises(ErroProveniencia):
            Primitiva("x", BOOL, lambda ctx: True, "descoberta")  # biblioteca sem corpo
        with self.assertRaises(ErroProveniencia):
            Primitiva("x", BOOL, lambda ctx: True, "inventada")
        with self.assertRaises(ValueError):
            Primitiva("x", BOOL, None, "descoberta", corpo=V("y"))  # corpo aberto


if __name__ == "__main__":
    unittest.main()
