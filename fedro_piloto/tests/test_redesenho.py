"""Testes das intervenções do documento 05: custo de folha ponderado (política unigrama), lesão de
biblioteca, resumo de teste com detecção de conjunto degenerado, referências das tarefas novas e
aritmética da sonda de custo igual."""
import unittest

from fedro_piloto import aprendizes as A
from fedro_piloto import experimento_minimo as EM
from fedro_piloto.avaliador import Contador, Contexto, aplicar, compilar
from fedro_piloto.dsl import BASES, BOOL, FUN, GRADE, LP, POS, parse
from fedro_piloto.enumerador import Enumerador, Gramatica
from fedro_piloto.grade import Grade, todas_as_grades
from fedro_piloto.razao import LivroRazao
from fedro_piloto.referencias import REGISTRO


def _den(t, tabela, grades, tipo):
    """Assinatura de denotação de um termo fechado sobre grades (e, para Grade→Pos→·, todas as posições)."""
    ev = compilar(t)
    out = []
    for g in grades:
        v = ev({}, Contexto(g.n, Contador(50_000), tabela))
        if tipo == FUN(GRADE, BOOL):
            out.append(bool(aplicar(v, g)))
        else:
            out.append(tuple(A.valor_json(aplicar(v, g, p)) for p in g.posicoes()))
    return tuple(out)


class TestReferenciasNovas(unittest.TestCase):
    def test_expandir_e_controles(self):
        g = Grade.de_texto("#.#/.#./...")
        S = ((1, 1),)
        self.assertEqual(A.REFERENCIAS_FUNCAO["expandir"](g, S), frozenset())        # (1,2) e (2,1) são brancas
        S = ((2, 2),)
        self.assertEqual(A.REFERENCIAS_FUNCAO["expandir"](g, S), frozenset())        # vizinhas de (2,2) são brancas
        g2 = Grade.de_texto("##./.#./...")
        self.assertEqual(A.REFERENCIAS_FUNCAO["expandir"](g2, ((1, 1),)), frozenset({(1, 2)}))
        self.assertEqual(A.REFERENCIAS_FUNCAO["expandir"](g2, ((1, 2),)), frozenset({(1, 1), (2, 2)}))
        self.assertEqual(A.REFERENCIAS_FUNCAO["pretasColuna1"](g2, (3, 3)), ((1, 1),))
        self.assertEqual(A.REFERENCIAS_FUNCAO["semLinha1"](g2, ((1, 1), (2, 2))), frozenset({(2, 2)}))

    def test_expandir_nao_inclui_S(self):
        for g in list(todas_as_grades(3))[:200]:
            S = tuple(g.pretas())
            r = A.REFERENCIAS_FUNCAO["expandir"](g, S)
            for q in r:
                self.assertTrue(g.celula(q))
                self.assertTrue(any(q in g.vizinhos(p) for p in S))

    def test_programa_de_ParAdjacente_via_expandir(self):
        """A composição `nao (vazia? (expandir g (pretas g)))` denota ParAdjacente (verificação da
        escada do experimento; o programa é de teste, não do aprendiz)."""
        c = REGISTRO["ParAdjacente"]
        for g in todas_as_grades(3):
            r = A.REFERENCIAS_FUNCAO["expandir"](g, tuple(g.pretas()))
            self.assertEqual(bool(r), c.rotulo(g))

    def test_tarefas_do_experimento(self):
        self.assertEqual(set(EM.TAREFAS), {"vizPretos", "expandir", "ParAdjacente", "NenhumaIsolada",
                                           "pretasColuna1", "semLinha1"})
        for t in EM.TAREFAS.values():
            self.assertEqual(t.proveniencia, A.PROVENIENCIA_AMBIENTE)


class TestCustoPonderado(unittest.TestCase):
    def setUp(self):
        self.tab = BASES["E0"].para_aprendiz()
        self.grades = [g for g in todas_as_grades(3) if g.balde() >= 50][:40]   # amostra independente

    def test_custo_1_coincide_com_tamanho(self):
        a = Enumerador(self.tab, {}, FUN(GRADE, BOOL), orcamento=4000, auditoria=True)
        b = Enumerador(self.tab, {}, FUN(GRADE, BOOL), orcamento=4000, auditoria=True,
                       custos_folha={p.nome: 1 for p in self.tab})
        for s in range(1, 5):
            self.assertEqual([t for t, _ in a.representantes(s)], [t for t, _ in b.representantes(s)])

    def test_custo_ponderado_completo(self):
        """Com custos em {1,2}, todo termo de tamanho s tem custo <= 2s: as denotações alcançadas até
        o custo 2s contêm as alcançadas até o tamanho s (completude da ordem ponderada)."""
        tipo = FUN(GRADE, BOOL)
        custos = {p.nome: (2 if p.nome in ("pretas", "nao") else 1) for p in self.tab}
        a = Enumerador(self.tab, {}, tipo, orcamento=20_000, auditoria=True)
        b = Enumerador(self.tab, {}, tipo, orcamento=40_000, auditoria=True, custos_folha=custos)
        s = 3
        den_a = {_den(t, self.tab, self.grades, tipo) for k in range(1, s + 1) for t, _ in a.representantes(k)}
        den_b = {_den(t, self.tab, self.grades, tipo) for k in range(1, 2 * s + 1) for t, _ in b.representantes(k)}
        self.assertTrue(den_a <= den_b)
        # e a constante cara aparece numa camada de custo > tamanho
        t = parse("(\\ (g Grade) (nao (vazia?@P (pretas g))))")
        self.assertEqual(Gramatica(self.tab, custos_folha=custos).custo_folha("pretas"), 2)
        alvo = _den(t, self.tab, self.grades, tipo)
        custo_alvo = next((k for k in range(1, 8) for tt, _ in b.representantes(k)
                           if _den(tt, self.tab, self.grades, tipo) == alvo), None)
        self.assertIsNotNone(custo_alvo)

    def test_custo_invalido(self):
        with self.assertRaises(ValueError):
            Gramatica(self.tab, custos_folha={"nao": 0})


class TestPoliticaUnigrama(unittest.TestCase):
    def test_custos_apos_solucao(self):
        livro = LivroRazao(10_002)
        ap = A.LFix(BASES["E0"], livro, politica_busca="unigrama")
        self.assertEqual(ap.custos_folha_correntes(ap.tabela_corrente()), {})
        ap._constantes_usadas = {"nao", "vazia?@P", "pretas"}
        c = ap.custos_folha_correntes(ap.tabela_corrente())
        self.assertEqual(c["nao"], 1)
        self.assertEqual(c["pretas"], 1)
        self.assertEqual(c["juntar"], 2)
        self.assertEqual(set(c.values()), {1, 2})

    def test_politica_invalida(self):
        with self.assertRaises(ValueError):
            A.LFix(BASES["E0"], LivroRazao(10_002), politica_busca="x")


class TestLesao(unittest.TestCase):
    def test_lesao_remove_descobertas_e_mantem_fornecidas(self):
        livro = LivroRazao(10_002)
        ap = A.LLib(BASES["E0"], livro, promover_funcoes=True)
        tab0 = ap.tabela_corrente()
        n0 = len(tab0)
        removidas = ap.lesionar()
        self.assertEqual(removidas, [])             # nada descoberto ainda
        tab1 = ap.tabela_corrente()
        self.assertEqual(len(tab1), n0)
        self.assertTrue(all(p.eh_fornecida for p in tab1))
        self.assertEqual(tab1.uso, "descoberta")
        self.assertEqual(ap.relatorio()["lesionadas"], [])


class TestResumoTeste(unittest.TestCase):
    def test_conjunto_degenerado_e_balanceada(self):
        livro = LivroRazao(10_002)
        ap = A.LFix(BASES["E0"], livro)
        t = EM.TAREFAS["ParAdjacente"]
        termo = parse("(\\ (g Grade) verdadeiro)")
        pos = [((g,), True) for g in todas_as_grades(2) if REGISTRO["ParAdjacente"].rotulo(g)][:3]
        neg = [((g,), False) for g in todas_as_grades(2) if not REGISTRO["ParAdjacente"].rotulo(g)][:3]
        acc, _, r = ap._avaliar_teste_resumo(termo, t, pos, ap.tabela_corrente())
        self.assertEqual(acc, 1.0)
        self.assertTrue(r["degenerado"])
        self.assertIsNone(r["acuracia_balanceada"])
        self.assertIn("DEGENERADO", r["aviso"])
        acc2, _, r2 = ap._avaliar_teste_resumo(termo, t, pos + neg, ap.tabela_corrente())
        self.assertFalse(r2["degenerado"])
        self.assertAlmostEqual(r2["acuracia_balanceada"], 0.5)
        self.assertEqual(r2["positivos"], 3)
        self.assertEqual(r2["negativos"], 3)


class TestSondaCustoIgual(unittest.TestCase):
    def test_cum_antes(self):
        curva = [{"tarefa": "a", "cumulativo_enumeracao": 10}, {"tarefa": "b", "cumulativo_enumeracao": 25},
                 {"tarefa": "c", "cumulativo_enumeracao": 40}]
        self.assertEqual(EM._cum_antes(curva, "a"), 0)
        self.assertEqual(EM._cum_antes(curva, "c"), 25)
        self.assertEqual(EM._cum_antes(curva, "zz"), 40)


if __name__ == "__main__":
    unittest.main()


class TestAuditoriaOE(unittest.TestCase):
    def test_classe_alvo_presente_para_alvo_pequeno(self):
        """ExistePreta (tamanho 5) tem de estar entre os representantes OE; a comparação é numa
        amostra independente (teste_int) com 48 grades: um termo espúrio não deve coincidir."""
        tab = BASES["E0"].para_aprendiz()
        t = A.Tarefa("ExistePreta", FUN(GRADE, BOOL), "predicado", "EM-teste", "ExistePreta")
        r = EM.classe_alvo_presente(tab, t, 5, 5_000, 10_002)
        self.assertTrue(r["presente"])
        self.assertLessEqual(r["custo_do_alvo"], 5)
        self.assertEqual(r["entradas_independentes"], 48)


class TestPromocaoParametroNaoUsado(unittest.TestCase):
    def test_promocao_descarta_parametros_nao_usados(self):
        """Uma solução de Grade → Pos → L Pos que ignora p (controle pretasColuna1) é promovida como
        função só de g; uma solução constante não é promovida (registrado)."""
        from fedro_piloto.dsl import LAMS, variaveis_livres, parse
        t = parse("(\\ (g Grade) (p Pos) (filtrar@P (celula g) (cabeca@LP (colunas g))))")
        u = t
        binders = []
        while u[0] == "lam":
            binders.append((u[1], u[2])); u = u[3]
        usados = [b for b in binders if b[0] in set(variaveis_livres(u))]
        self.assertEqual([n for n, _ in usados], ["g"])
        self.assertEqual(LAMS(usados, u)[1], "g")
