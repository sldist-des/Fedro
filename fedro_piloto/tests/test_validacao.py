"""Testes do documento 06: verificação exaustiva/amostral, replicação (guarda de sementes e
agregação), currículo autodirigido (legalidade do seletor e regra de progresso), famílias de
transferência congeladas (hash, tipos, coerência com o REGISTRO) e análise de transferência."""
import inspect
import unittest

from fedro_piloto import aprendizes as A
from fedro_piloto import curriculo_autodirigido as C
from fedro_piloto import experimento_minimo as EM
from fedro_piloto import familias_transferencia as F
from fedro_piloto import replicacao as R
from fedro_piloto import transferencia as T
from fedro_piloto import verificacao as V
from fedro_piloto.dsl import BOOL, FUN, GRADE, LP, POS, parse, tipo_de
from fedro_piloto.grade import todas_as_grades
from fedro_piloto.referencias import REGISTRO


class TestVerificacao(unittest.TestCase):
    def test_exaustivo_funcao_correta_e_incorreta(self):
        t_ok = parse("(\\ (g Grade) (p Pos) (filtrar@P (celula g) (vizinhos g p)))")
        t_mau = parse("(\\ (g Grade) (p Pos) (vizinhos g p))")
        r = V.verificar_exaustivo(t_ok, EM.TAREFAS["vizPretos"], ns=(1, 2, 3))
        self.assertEqual(r["erros"], 0)
        self.assertTrue(r["bateria_argumentos"])
        self.assertIn("bateria finita", r["regime"])
        self.assertEqual(r["por_n"][3]["grades"], 512)
        r2 = V.verificar_exaustivo(t_mau, EM.TAREFAS["vizPretos"], ns=(2, 3))
        self.assertGreater(r2["erros"], 0)

    def test_exaustivo_predicado_sem_bateria(self):
        t = parse("(\\ (g Grade) (todos@P (celula g) (cabeca@LP (linhas g))))")
        r = V.verificar_exaustivo(t, F.TAREFAS["TopoCheio"], ns=(1, 2, 3))
        self.assertEqual(r["erros"], 0)
        self.assertFalse(r["bateria_argumentos"])
        self.assertNotIn("bateria", r["regime"])

    def test_amostral_usa_teste_ext(self):
        t = parse("(\\ (g Grade) (todos@P (celula g) (cabeca@LP (linhas g))))")
        r = V.validar_amostral(t, F.TAREFAS["TopoCheio"], ns=(5,), k=8, semente=10_002)
        self.assertIn("teste_ext", r["regime"])
        self.assertEqual(sum(x["natural"]["erros"] + x["desenho"]["erros"] for x in r["por_n"].values()), 0)
        self.assertEqual(r["por_n"][5]["grades_naturais"], 8)


class TestReplicacao(unittest.TestCase):
    def test_guarda_de_sementes(self):
        for sem in (10_001, 10_002):
            with self.assertRaises(ValueError):
                R.verificar_sementes([sem])
        with self.assertRaises(ValueError):
            R.verificar_sementes([20_000])      # fora do intervalo exploratório
        with self.assertRaises(ValueError):
            R.verificar_sementes([50])          # bucket/semente fora do piloto
        R.verificar_sementes([10_003, 10_006])

    def test_agregar(self):
        def exe(sem, pol, aceitas, custo, reuso, veredito):
            return {"semente": sem, "politica": pol, "analise": {"criterio_central": {"veredito": veredito}},
                    "bracos": {"L-lib+f": {"aceitas": aceitas, "num_aceitas": len(aceitas), "cumulativo_ate_T3": custo,
                                           "cumulativo_final": custo, "enumeracao_final": 1, "abstracoes": len(reuso),
                                           "reutilizadas": reuso, "falha": None,
                                           "hipoteses": {t: f"h{t}" for t in aceitas}}}}
        out = R.agregar([exe(10_003, "tamanho", ["vizPretos", "expandir"], 100, [], False),
                         exe(10_004, "tamanho", ["vizPretos", "expandir", "ParAdjacente"], 300, [("abs2", 1, 0)], True)])
        k = out["por_politica_braco"]["tamanho|L-lib+f"]
        self.assertEqual(k["sementes"], 2)
        self.assertEqual(k["cumulativo_final"]["min"], 100)
        self.assertEqual(k["cumulativo_final"]["max"], 300)
        self.assertEqual(k["aceitas_por_tarefa"]["ParAdjacente"], 1)
        self.assertEqual(k["com_reutilizacao"], 1)
        self.assertEqual(out["veredito_por_politica"]["tamanho"], [False, True])


class TestCurriculoAutodirigido(unittest.TestCase):
    PROIBIDOS = ("REFERENCIAS_FUNCAO", "REGISTRO", "saida_referencia", "programas_referencia",
                 "tamanho_doc", "conceito", "TAREFAS", "REFERENCIAS_DSL", "fecho_ref", "rotulo(")

    @staticmethod
    def _codigo_sem_docstrings(obj) -> str:
        import ast
        arvore = ast.parse(inspect.getsource(obj))
        for no in ast.walk(arvore):
            corpo = getattr(no, "body", None)
            if isinstance(corpo, list) and corpo and isinstance(corpo[0], ast.Expr) \
                    and isinstance(getattr(corpo[0], "value", None), ast.Constant) and isinstance(corpo[0].value.value, str):
                corpo.pop(0)
        return ast.unparse(arvore)

    def test_seletores_nao_consultam_referencias(self):
        for cls in (C.Seletor, C.SeletorManual, C.SeletorAleatorio, C.SeletorAutodirigido, C.HistoricoTarefa):
            src = self._codigo_sem_docstrings(cls)
            for p in self.PROIBIDOS:
                self.assertNotIn(p, src, f"{cls.__name__} consulta {p}")
        campos = set(C.HistoricoTarefa.__dataclass_fields__)
        self.assertTrue(campos <= {"id", "tipo", "tentativas", "aceita", "custo_total", "enumeracao_total", "ultimo_B",
                                   "ultimo_motivo", "ultimo_tamanho_max", "versao_bib_ultima", "orcamento_proximo",
                                   "exemplos_finais"})

    def _hist(self):
        return [C.HistoricoTarefa(t, "τ") for t in ("b", "a", "c")]

    def test_autodirigido_aprofundamento_e_progresso(self):
        import random
        sel = C.SeletorAutodirigido(b0=100)
        hist = self._hist()
        rng = random.Random(0)
        tid, B = sel.escolher(hist, 0, rng, 1_000)
        self.assertEqual((tid, B), ("a", 100))              # empate: id
        h = next(x for x in hist if x.id == tid)
        h.tentativas, h.ultimo_B, h.versao_bib_ultima = 1, 100, 0
        sel.apos(h, 0, 1_000)
        self.assertEqual(h.orcamento_proximo, 200)
        # o último degrau é exatamente B_max; depois de falhar a B_max a tarefa fica esgotada
        h2 = C.HistoricoTarefa("z", "τ", tentativas=1, ultimo_B=700)
        sel.apos(h2, 0, 1_000)
        self.assertEqual(h2.orcamento_proximo, 1_000)
        h2.ultimo_B = 1_000
        sel.apos(h2, 0, 1_000)
        self.assertGreater(h2.orcamento_proximo, 1_000)
        # as outras ainda estão em b0: escolhe-as antes de dobrar "a"
        self.assertEqual(sel.escolher(hist, 0, rng, 1_000), ("b", 100))
        for x in hist:
            x.tentativas, x.ultimo_B, x.versao_bib_ultima, x.orcamento_proximo = 1, 100, 0, 200
        self.assertEqual(sel.escolher(hist, 0, rng, 1_000), ("a", 200))
        # biblioteca mudou (versão 1): repete-se o MESMO orçamento (100) uma vez, antes de dobrar
        self.assertEqual(sel.escolher(hist, 1, rng, 1_000), ("a", 100))
        hist[1].versao_bib_ultima = 1
        self.assertEqual(sel.escolher(hist, 1, rng, 1_000), ("b", 100))
        # orçamento acima de B_max: nada a escolher
        for x in hist:
            x.versao_bib_ultima, x.orcamento_proximo = 1, 5_000
        self.assertIsNone(sel.escolher(hist, 1, rng, 1_000))

    def test_manual_e_aleatorio(self):
        import random
        hist = self._hist()
        sel = C.SeletorManual(["c", "a", "b"])
        self.assertEqual(sel.escolher(hist, 0, random.Random(0), 10), ("c", 10))
        hist[2].tentativas, hist[2].versao_bib_ultima = 1, 0
        self.assertEqual(sel.escolher(hist, 0, random.Random(0), 10)[0], "a")
        for x in hist:
            x.tentativas, x.versao_bib_ultima = 1, 0
        self.assertIsNone(sel.escolher(hist, 0, random.Random(0), 10))      # uma passagem: nada mais
        self.assertEqual(sel.escolher(hist, 1, random.Random(0), 10)[0], "c")  # biblioteca mudou: repete
        al = C.SeletorAleatorio()
        seq1 = [al.escolher(self._hist(), 0, random.Random(7), 10)[0] for _ in range(5)]
        seq2 = [al.escolher(self._hist(), 0, random.Random(7), 10)[0] for _ in range(5)]
        self.assertEqual(seq1, seq2)
        self.assertTrue(all(s in ("a", "b", "c") for s in seq1))

    def test_laco_termina_e_regista(self):
        cfg = EM.ConfigEM(B=200, sondas=False, auditoria_oe_orcamento=0, memoria_trabalhador_gb=0)
        r = C.job_braco("manual", "L-fix", cfg, G_total=400, B_max=200, semente_seletor=10_002, pool=["vizPretos", "pretasColuna1"])
        d = r["deterministico"]
        self.assertGreaterEqual(len(d["passos"]), 1)
        self.assertLessEqual(d["gasto_global"], 400 + 200)
        self.assertEqual(d["passos"][0]["tarefa"], "vizPretos")
        self.assertIn("custo_total", d)


class TestFamiliasCongeladas(unittest.TestCase):
    def test_hash_congelado(self):
        self.assertEqual(F.hash_especificacao(), F.HASH_CONGELADO)

    def test_tipos_das_referencias_dsl(self):
        tab = F.tabela_referencia()
        for tid, refs in F.REFERENCIAS_DSL.items():
            for modo in ("E0", "abs"):
                self.assertEqual(tipo_de(parse(refs[modo]), {}, tab), F.TAREFAS[tid].tipo, f"{tid}/{modo}")
        self.assertEqual(set(F.REFERENCIAS_DSL), set(F.TAREFAS))

    def test_coerencia_com_registro(self):
        iso = F.REFERENCIAS_FAMILIAS["isoladaP"]
        pcv = F.REFERENCIAS_FAMILIAS["pretasComVizinha"]
        exp = A.REFERENCIAS_FUNCAO["expandir"]
        for g in todas_as_grades(3):
            nenhuma = REGISTRO["NenhumaIsolada"].rotulo(g)
            if g.pretas():          # o conceito do REGISTRO é falso na grade sem pretas (quantificação não vazia)
                self.assertEqual(nenhuma, not any(iso(g, p) for p in g.posicoes()), g)
            self.assertEqual(frozenset(pcv(g)), frozenset(exp(g, tuple(g.pretas()))), g)
            S = tuple(g.pretas())[:2]
            fr = F.REFERENCIAS_FAMILIAS["fronteira"](g, S)
            self.assertTrue(fr.isdisjoint(S))
            self.assertTrue(fr <= exp(g, S))

    def test_familias_nao_repetem_tarefas_do_curriculo(self):
        self.assertFalse(set(F.TAREFAS) & set(EM.TAREFAS))
        self.assertEqual(len(F.F_COMP), 5)
        self.assertEqual(len(F.F_NEG), 4)


class TestAnaliseTransferencia(unittest.TestCase):
    def test_analisar(self):
        def res(aceita, custo, reuso=(), tam=None):
            return {"aceita": aceita, "custo": custo, "biblioteca_usada": list(reuso), "tamanho": tam}
        lib = {"politica": "tamanho", "aprendiz": "L-lib+f", "custo_cadeia": 10, "abstracoes": [],
               "resultados": {"expandir2": res(True, 5, ("abs2",), 7), "TopoCheio": res(True, 20, (), 7),
                              "semColuna1": res(False, 50), "isoladaP": res(False, 60)}}
        fix = {"politica": "tamanho", "aprendiz": "L-fix", "custo_cadeia": 30, "abstracoes": [],
               "resultados": {"expandir2": res(False, 50), "TopoCheio": res(True, 10, (), 7),
                              "semColuna1": res(True, 10, (), 7), "isoladaP": res(False, 60)}}
        an = T.analisar({"tamanho/L-lib+f": {"deterministico": lib}, "tamanho/L-fix": {"deterministico": fix}})["tamanho"]
        pt = an["por_tarefa"]
        self.assertEqual(pt["expandir2"]["transferencia"], "positiva (só L-lib+f aceita)")
        self.assertEqual(pt["TopoCheio"]["transferencia"], "negativa")
        self.assertEqual(pt["semColuna1"]["transferencia"], "negativa (só L-fix aceita)")
        self.assertEqual(pt["isoladaP"]["transferencia"], "inconclusiva (nenhum aceita)")
        self.assertEqual(an["F-comp"]["com_reuso"], 1)
        self.assertEqual(an["F-neg"]["negativas"], 2)


if __name__ == "__main__":
    unittest.main()
