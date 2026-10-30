"""Aprendizes L-fix / L-lib (documento 02, 2.4 e 2.9): laço dialético, oráculo de função, barreiras
de proveniência (soluções manuais nunca entram na biblioteca de um aprendiz autônomo) e livro-razão."""
import unittest

from fedro_piloto import aprendizes as A
from fedro_piloto import geradores as G
from fedro_piloto import programas_referencia as PR
from fedro_piloto.avaliador import Contador, Contexto, aplicar, avaliar, compilar
from fedro_piloto.biblioteca import Biblioteca, Solucao
from fedro_piloto.dsl import E0, ErroProveniencia, parse
from fedro_piloto.grade import Grade, chave_minimalidade
from fedro_piloto.razao import LivroRazao

SEMENTE = 10_001
B = 3000


class TestSaidaConjunto(unittest.TestCase):
    def test_igualdade_de_conjunto(self):
        s = A.SaidaConjunto([(1, 1), (2, 2)])
        self.assertTrue(((2, 2), (1, 1)) == s)
        self.assertTrue(s == ((1, 1), (2, 2), (1, 1)))
        self.assertFalse(((1, 1),) == s)
        self.assertTrue(((1, 1),) != s)
        self.assertFalse(s == True)  # noqa: E712


class TestAmbiente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amb = A.Ambiente(SEMENTE, k_reservatorio=5, ns_reservatorio=(5,), num_teste=4)

    def test_semente_fora_do_piloto(self):
        with self.assertRaises(ValueError):
            A.Ambiente(20_000)

    def test_exemplos_iniciais_predicado(self):
        p = self.amb.preparar(A.TAREFAS_POR_ID["ParAdjacente"])
        rot = [y for _, y in p.exemplos]
        self.assertEqual(rot.count(True), 2)
        self.assertEqual(rot.count(False), 2)
        for (g,), y in p.exemplos:
            self.assertTrue(G.na_particao(g, A.PARTICAO_TREINO))
            self.assertEqual(G.REGISTRO["ParAdjacente"].rotulo(g), y)
        # emparelhados em densidade (mesmo número de pretas por par)
        gs = [a[0] for a, _ in p.exemplos]
        self.assertEqual(gs[0].contagem_pretas(), gs[1].contagem_pretas())

    def test_exemplos_iniciais_funcao(self):
        for tid in ("vizPretos", "passo", "descartar", "noMaximo"):
            t = A.TAREFAS_POR_ID[tid]
            p = self.amb.preparar(t)
            self.assertEqual(len(p.exemplos), 4)
            for args, y in p.exemplos:
                self.assertEqual(A.saida_referencia(t, args), y)
                for a in args:
                    if isinstance(a, Grade):
                        self.assertTrue(G.na_particao(a, A.PARTICAO_TREINO))

    def test_determinismo(self):
        b = A.Ambiente(SEMENTE, k_reservatorio=5, ns_reservatorio=(5,), num_teste=4)
        for tid in ("ExistePreta", "pretasDe"):
            self.assertEqual(self.amb.preparar(A.TAREFAS_POR_ID[tid]).como_dict(),
                             b.preparar(A.TAREFAS_POR_ID[tid]).como_dict())

    def test_programas_manuais_resolvem_as_tarefas_do_ambiente(self):
        """Coerência ambiente × programas manuais (só referência; nunca dados ao aprendiz)."""
        tb = PR.tabela_referencia("E0")
        gs = G.grades_da_particao(3, A.PARTICAO_TREINO)[:20]
        for tid in ("vizPretos", "passo", "pretasDe", "descartar", "mesmoNumero"):
            t = A.TAREFAS_POR_ID[tid]
            for g in gs:
                for args in A.entradas_da_grade(t, g):
                    v = aplicar(avaliar(parse(tid), {}, A.n_semantica(t, args), None, tb), *args)
                    self.assertTrue(v == A.saida_referencia(t, args), (tid, g.texto(), args))


class TestOraculoFuncao(unittest.TestCase):
    def test_contraexemplo_minimo_por_forca_bruta(self):
        t = A.TAREFAS_POR_ID["vizPretos"]
        rng = G.rng_piloto(SEMENTE)
        o = A.OraculoFuncao(t, rng, k_reservatorio=5)
        errada = parse("(\\ (g Grade) (p Pos) (vizinhos g p))")
        ev = compilar(errada)

        def h(args):
            return aplicar(ev({}, Contexto(args[0].n, Contador(), None)), *args)
        ce = o.contraexemplo(h)
        self.assertIsNotNone(ce)
        # força bruta independente: menor grade (ordem de minimalidade) com alguma posição discordante
        gs = sorted((g for n in (1, 2, 3) for g in G.grades_da_particao(n, "oraculo_treino")),
                    key=chave_minimalidade)
        esperado = None
        for g in gs:
            for p in g.posicoes():
                if tuple(g.vizinhos(p)) != A.REFERENCIAS_FUNCAO["vizPretos"](g, p):
                    esperado = (g, p)
                    break
            if esperado:
                break
        self.assertEqual(ce[0], esperado)
        self.assertEqual(o.contador.contraexemplos_devolvidos, 1)
        certa = parse("(\\ (g Grade) (p Pos) (filtrar@P (celula g) (vizinhos g p)))")
        ev2 = compilar(certa)
        self.assertIsNone(o.contraexemplo(lambda a: aplicar(ev2({}, Contexto(a[0].n, Contador(), None)), *a)))


class TestLacoDialetico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amb = A.Ambiente(SEMENTE, k_reservatorio=5, ns_reservatorio=(5,), num_teste=4)
        cls.livro = LivroRazao(SEMENTE)
        cls.fix = A.LFix(E0, cls.livro, B=B, K=6, kw_enumerador={"semente": SEMENTE})
        cls.res = cls.fix.executar([A.TAREFAS_POR_ID[t] for t in ("ExistePreta", "vizPretos")], cls.amb)

    def test_aceita_e_correto(self):
        r0, r1 = self.res
        self.assertTrue(r0.aceita)
        self.assertEqual(r0.tamanho, 5)
        self.assertTrue(r1.aceita)
        t = parse(r1.hipotese)
        ref = A.REFERENCIAS_FUNCAO["vizPretos"]
        for n in (2, 3):
            v = avaliar(t, {}, n)
            for g in G.grades_da_particao(n, "oraculo_treino")[:10]:
                for p in g.posicoes():
                    self.assertEqual(v(g)(p), ref(g, p))

    def test_livro_fecha_e_tem_custos(self):
        r = self.livro.verificar_fechamento()
        self.assertTrue(r.ok, r.problemas)
        for tid in ("ExistePreta", "vizPretos"):
            e = self.livro.entrada(tid, "L-fix@E0")
            self.assertGreater(e.busca_candidatos, 0)
            self.assertGreater(e.busca_passos, 0)
            self.assertGreater(e.oraculo_consultas, 0)
            self.assertGreater(e.geracao_grades, 0)
            self.assertEqual(e.compressao_subtermos, 0)
        self.assertTrue(self.livro.medicoes)

    def test_l_fix_exige_tabela_de_descoberta(self):
        ref = PR.tabela_referencia("E0")
        with self.assertRaises(ErroProveniencia):
            A.LFix(ref, LivroRazao(SEMENTE))

    def test_orcamento_esgotado(self):
        livro = LivroRazao(SEMENTE)
        ap = A.LFix(E0, livro, B=50, K=3, kw_enumerador={"semente": SEMENTE})
        r = ap.resolver(A.TAREFAS_POR_ID["ParAdjacente"], self.amb)
        self.assertFalse(r.aceita)
        self.assertEqual(r.motivo_fim, "orcamento_enumeracao")
        self.assertTrue(livro.verificar_fechamento().ok)


class TestLLib(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amb = A.Ambiente(SEMENTE, k_reservatorio=5, ns_reservatorio=(5,), num_teste=4)

    def test_compressao_so_com_solucoes_proprias(self):
        livro = LivroRazao(SEMENTE)
        lib = A.LLib(E0, livro, limiar=3, B=B, K=6, kw_enumerador={"semente": SEMENTE})
        self.assertEqual(lib.biblioteca.modo, "autonomo")
        self.assertEqual(lib.tabela_corrente().uso, "descoberta")
        lib.executar([A.TAREFAS_POR_ID[t] for t in ("vizPretos", "pretasDe")], self.amb)
        ents = A.abstracoes(lib)
        self.assertTrue(ents, "esperava ao menos uma abstração (filtrar@P (celula g))")
        for e in ents:
            self.assertEqual(e["proveniencia"], "descoberta")
        for s in lib.biblioteca.solucoes:
            self.assertEqual(s.proveniencia, "descoberta")
        self.assertGreater(livro.entrada("pretasDe", "L-lib@E0").compressao_subtermos, 0)
        self.assertTrue(livro.verificar_fechamento().ok)

    def test_barreiras_manual_teste(self):
        livro = LivroRazao(SEMENTE)
        lib = A.LLib(E0, livro)
        manual = Solucao(PR.termo(PR.POR_NOME["ExistePreta"]), "ExistePreta", "manual-teste")
        with self.assertRaises(ErroProveniencia):
            lib.biblioteca.comprimir([manual], 1)
        with self.assertRaises(ErroProveniencia):
            A.LLib(PR.tabela_referencia("E0"), livro)
        with self.assertRaises(ErroProveniencia):
            A.LLib(E0, livro, biblioteca=Biblioteca(E0, "mecanismo-teste"))
        with self.assertRaises(ErroProveniencia):
            lib.tabela_corrente().adicionar(PR.entradas_manuais("E0")[0])

    def test_variante_promove_solucao_de_funcao(self):
        livro = LivroRazao(SEMENTE)
        lib = A.LLib(E0, livro, promover_funcoes=True, B=B, K=6, kw_enumerador={"semente": SEMENTE})
        self.assertEqual(lib.aprendiz_id, "L-lib+f@E0")
        r = lib.resolver(A.TAREFAS_POR_ID["pretasDe"], self.amb)
        self.assertTrue(r.aceita)
        ents = A.abstracoes(lib)
        self.assertEqual(len(ents), 1)
        self.assertEqual(ents[0]["metodo"], "promocao-solucao")
        self.assertEqual(ents[0]["proveniencia"], "descoberta")
        # a "abstração" promovida É a solução inteira do degrau: marcada como tal, categoria própria
        self.assertEqual(ents[0]["categoria"], "promocao-solucao")
        self.assertEqual(ents[0]["coincide_com_solucao_de_tarefa"], ["pretasDe"])
        self.assertTrue(ents[0]["copia_de_solucao"])
        # reutilização registrada quando uma solução POSTERIOR, achada pela busca, a usa
        nome = ents[0]["nome"]
        r2 = lib.resolver(A.TAREFAS_POR_ID["vizPretos"], self.amb)
        self.assertTrue(r2.aceita)
        self.assertIn(nome, r2.constantes_biblioteca_usadas)
        self.assertEqual(r2.reutilizacoes.get(nome), 1)
        self.assertEqual(lib.tabela_corrente()[nome].categoria(), "descoberta-reutilizada")
        ents = {e["nome"]: e for e in A.abstracoes(lib)}
        self.assertEqual(ents[nome]["categoria"], "promocao-solucao-reutilizada")

    def test_solucao_descoberta_exige_certificado(self):
        """Um termo escrito à mão (parse) rotulado 'descoberta' é recusado: o rótulo não basta."""
        lib = A.LLib(E0, LivroRazao(SEMENTE))
        termo = PR.termo(PR.POR_NOME["ExistePreta"])
        with self.assertRaises(ErroProveniencia):
            Solucao(termo, "ExistePreta", "descoberta")
        with self.assertRaises(ErroProveniencia):
            lib.biblioteca.registrar_reuso(Solucao(termo, "ExistePreta", "manual-teste"), "ExistePreta")
        # Fragmento forjado com rótulo 'descoberta' e corpus vazio: recusado pela Biblioteca
        from fedro_piloto.biblioteca import Fragmento
        from fedro_piloto.dsl import tipo_de
        frag = Fragmento(termo, tipo_de(termo, {}, E0), 2, 4, ("ExistePreta",), 1, 0, "fechamento",
                         frozenset({"descoberta"}))
        with self.assertRaises(ErroProveniencia):
            lib.biblioteca.adicionar(frag, "descoberta")
        self.assertEqual(lib.tabela_corrente().biblioteca(), [])


if __name__ == "__main__":
    unittest.main()
