"""Testes das correções dos achados de revisão (barreira por construção, oráculos sem aceitação
vácua, refinamento OE, auditoria OE dos tipos fechados, sementes, teste sem sobreposição, regras de
PM10/PM11/decisão/custo igual/conciliação, reaproveitamento com hash do código, tabela sistemática)."""
import json
import os
import tempfile
import unittest

from fedro_piloto import aprendizes as A
from fedro_piloto import certificados as CERT
from fedro_piloto import geradores as G
from fedro_piloto import piloto as P
from fedro_piloto import programas_referencia as PR
from fedro_piloto.avaliador import OrcamentoEsgotado, aplicar, avaliar
from fedro_piloto.biblioteca import Biblioteca, Solucao
from fedro_piloto.dsl import (BASES, BASES_SISTEMATICAS, BOOL, E0, FUN, GRADE, INSTANCIAS, ErroProveniencia, imprimir,
                              tipo_str)
from fedro_piloto.enumerador import ContadorBusca, Enumerador, EstadoBusca, buscar, enumerar_sem_poda, grades_amostra_oe
from fedro_piloto.razao import LivroRazao

SEMENTE = 10_001
E0D = E0.para_aprendiz()
GB = FUN(GRADE, BOOL)


class TestBarreiraPorConstrucao(unittest.TestCase):
    def test_emissao_restrita_ao_laco(self):
        with self.assertRaises(CERT.ErroCertificado):
            CERT.emitir_busca(("c", "verdadeiro"), BOOL, "E0")
        with self.assertRaises(CERT.ErroCertificado):
            CERT.emitir_entrada("x", ("c", "verdadeiro"), 1)
        falso = CERT.CertificadoBusca(("c", "verdadeiro"), BOOL, "E0", "0" * 64)
        self.assertFalse(CERT.busca_valida(falso))

    def test_certificado_de_outro_termo_recusado(self):
        """Um certificado legítimo não pode ser reaproveitado para um termo manual."""
        amb = A.Ambiente(SEMENTE, k_reservatorio=3, ns_reservatorio=(5,), num_teste=3)
        lib = A.LLib(E0, LivroRazao(SEMENTE), B=3000, K=3, kw_enumerador={"semente": SEMENTE})
        r = lib.resolver(A.TAREFAS_POR_ID["ExistePreta"], amb)
        self.assertTrue(r.aceita)
        cert = lib.biblioteca.solucoes[0].certificado
        self.assertTrue(CERT.descoberta_valida(cert, tarefa_id="ExistePreta"))
        manual = PR.termo(PR.POR_NOME["ParAdjacente"])
        s = Solucao(manual, "ExistePreta", "descoberta", cert)   # integridade ok, termo diferente
        with self.assertRaises(ErroProveniencia):
            lib.biblioteca.comprimir([s], 1)
        with self.assertRaises(ErroProveniencia):
            Solucao(manual, "ParAdjacente", "descoberta", cert)  # tarefa diferente

    def test_comprimir_solucao_manual_rotulada_descoberta(self):
        """Cenário do achado: LLib(E0) + comprimir([Solucao(inline(PR...), 'descoberta')]) → recusado."""
        from fedro_piloto.tradutores import inline
        lib = A.LLib(E0, LivroRazao(SEMENTE))
        bib = PR.biblioteca_manual("E0")
        with self.assertRaises(ErroProveniencia):
            lib.biblioteca.comprimir([Solucao(inline(PR.termo(PR.POR_NOME["ParAdjacente"]), bib), "ParAdjacente",
                                              "descoberta")], 3)
        self.assertEqual(lib.tabela_corrente().biblioteca(), [])


class TestOraculoFuncaoSemAceitacaoVacua(unittest.TestCase):
    def test_h_indefinida_em_tudo(self):
        t = A.TAREFAS_POR_ID["vizPretos"]
        o = A.OraculoFuncao(t, rng=G.rng_piloto(SEMENTE), k_reservatorio=3)

        def h(_args):
            raise OrcamentoEsgotado(0)
        r = o.contraexemplo(h)
        self.assertIsNotNone(r)
        self.assertTrue(o.historico[-1]["resposta_indefinida"])
        self.assertEqual(r[1], A.saida_referencia(t, r[0]))


class TestRefinamentoOE(unittest.TestCase):
    def test_grades_dos_exemplos_entram_nos_mundos(self):
        amostra = set(grades_amostra_oe(SEMENTE))
        g = next(x for x in G.grades_da_particao(4, "oraculo_treino") if x not in amostra)
        h = next(x for x in G.grades_da_particao(4, "oraculo_treino") if x not in amostra and x != g)
        cb = ContadorBusca()
        rot = lambda x: x.contagem_pretas() > 0
        t, est = buscar(E0D, GB, [((g,), rot(g))], 2000, cb, semente=SEMENTE)
        self.assertIn(g, est.enum.grades_amostra)
        self.assertEqual(est.refinamentos, 0)
        t, est = buscar(E0D, GB, [((g,), rot(g)), ((h,), not rot(h))], 2000, cb, est, semente=SEMENTE)
        self.assertIn(h, est.enum.grades_amostra)
        self.assertEqual(est.refinamentos, 1)
        self.assertEqual(cb.refinamentos_oe, 1)
        self.assertGreater(cb.enumeracao_candidatos_avaliados, 0)

    def test_menor_consistente_nao_se_perde(self):
        """Amostra OE fixa mínima (2 grades n = 2: quase tudo fica fundido) e 4 exemplos de CantoSupEsq em
        grades da partição. Com refinamento (grades dos exemplos nos mundos) a busca devolve um termo do
        MESMO tamanho que o menor termo consistente da enumeração sem poda; sem refinamento, não."""
        amostra = list(G.grades_da_particao(2, "oraculo_treino"))[:2]
        c = A.REGISTRO["CantoSupEsq"]
        gs = [g for n in (3, 4) for g in G.grades_da_particao(n, "oraculo_treino")]
        pos = [g for g in gs if c.rotulo(g)][:2]
        neg = [g for g in gs if not c.rotulo(g) and g.contagem_pretas() >= 2][:2]
        exemplos = [((g,), c.rotulo(g)) for g in pos + neg]
        ev = lambda t, x: aplicar(avaliar(t, n=x.n, orcamento_passos=20_000), x)

        def consistente(t):
            try:
                return all(ev(t, g) == v for (g,), v in exemplos)
            except OrcamentoEsgotado:
                return False
        minimo = next(s for t, s in enumerar_sem_poda(E0D, None, GB, 7) if consistente(t))
        t1, e1 = buscar(E0D, GB, exemplos, 50_000, ContadorBusca(), ambientes_amostra=amostra, refinar_oe=True)
        self.assertIsNotNone(t1)
        self.assertTrue(consistente(t1))
        self.assertEqual(P.tamanho(t1), minimo)
        self.assertEqual(len(e1.enum.grades_amostra), 2 + 4)
        t0, _ = buscar(E0D, GB, exemplos, 50_000, ContadorBusca(), ambientes_amostra=amostra, refinar_oe=False)
        self.assertTrue(t0 is None or P.tamanho(t0) > minimo)


class TestAuditoriaOETiposFechados(unittest.TestCase):
    """Validação da poda OE contra amostra INDEPENDENTE (teste_int, baterias do ambiente) nos tipos
    fechados das tarefas (o V1 de test_enumerador cobre só {g} ⊢ Bool e {g} ⊢ L Pos). Tamanhos aqui
    até 5 (rápido); a fase 3 do piloto vai até 8 (7 em L Pos → L Pos → L Pos) e registra as taxas."""

    def test_cinco_tipos_fechados(self):
        for tipo in P.TAREFA_DO_TIPO:
            r = P.job_auditoria_oe(tipo, 5, 60, SEMENTE)["deterministico"]
            self.assertGreater(r["classes"], 0, tipo)
            self.assertEqual(sum(x["classes_novas"] for x in r["por_tamanho"]), r["classes"])
            self.assertEqual(r["perdidas_total"], 0, (tipo, r["por_tamanho"]))


class TestSementesIndependentes(unittest.TestCase):
    def test_fluxos_por_papel_e_semente(self):
        a, b = A.Ambiente(SEMENTE), A.Ambiente(SEMENTE + 1)
        t = A.TAREFAS_POR_ID["componenteDe"]
        xs = lambda r: [r.random() for _ in range(5)]
        self.assertNotEqual(xs(a._rng_tarefa(t, "teste")), xs(b._rng_tarefa(t, "exemplos")))
        self.assertNotEqual(xs(a._rng_tarefa(t, "exemplos")), xs(G.rng_piloto(SEMENTE)))
        self.assertEqual(xs(a._rng_tarefa(t, "teste")), xs(A.Ambiente(SEMENTE)._rng_tarefa(t, "teste")))


class TestTesteSemSobreposicao(unittest.TestCase):
    def test_listas_fora_do_dominio_do_oraculo(self):
        amb = A.Ambiente(SEMENTE, num_teste=30)
        t = A.TAREFAS_POR_ID["descartar"]
        p = amb.preparar(t)
        o = amb.oraculo(t)
        dominio = {A._chave_entrada(a) for g, _ in o.dominio for a in A.entradas_da_grade(t, g)}
        chaves = [A._chave_entrada(a) for a, _ in p.teste]
        self.assertEqual(len(chaves), len(set(chaves)))          # sem reposição
        self.assertTrue(set(chaves).isdisjoint(dominio))          # nenhuma entrada do domínio do oráculo
        self.assertTrue(set(chaves).isdisjoint({A._chave_entrada(a) for a, _ in p.exemplos}))
        self.assertGreater(p.teste_sobreposicoes_excluidas, 0)


class TestTabelaSistematica(unittest.TestCase):
    def test_superconjunto_por_criterio(self):
        for b, tb in BASES.items():
            self.assertTrue(set(tb.nomes()) <= set(BASES_SISTEMATICAS[b].nomes()), b)
        nomes = set(BASES_SISTEMATICAS["E0"].nomes())
        for n in ("mapear@P>P", "mapear@LP>P", "mapear@LP>LP", "algum@LP", "concatenar@LP", "reverter@P", "se@P"):
            self.assertIn(n, nomes)
        self.assertIn("ateFixo@LP", BASES_SISTEMATICAS["E0mais"].nomes())


def _pm8_constante(valor=99, Ds=(2, 4, 6)):
    rotulos = list(P.CONTEXTOS) + ["fechado " + tipo_str(t) for t in P.TIPOS_TAREFA]
    return [{"base": b, "rotulo": r, "tabela_espec": "curada", "D": D, "s_reach": {"10000": valor}}
            for b in ("E0", "E0p", "E0mais", "E0pmais") for r in rotulos for D in Ds]


class TestRegrasPiloto(unittest.TestCase):
    def test_pm10_E0p_alcancavel_com_D_adequado(self):
        """Com s_reach grande em todos os D, E0' e E0'+ deixam de ser inalcançáveis por construção."""
        pm10 = P.tabela_pm10(_pm8_constante(), B=10_000)
        dec = P.decidir(pm10, None)
        self.assertTrue(dec["alcance_sintatico_por_base"]["E0p"])
        self.assertTrue(dec["alcance_sintatico_por_base"]["E0pmais"])
        self.assertTrue(dec["condicao_GO_E0"])
        self.assertEqual(dec["decisao"], "NO-GO")          # sem evidência autônoma
        so_D2 = P.tabela_pm10(_pm8_constante(Ds=(2,)), B=10_000)
        self.assertTrue(any(l["fora_da_gramatica_D2"] for l in so_D2 if l["base"] == "E0p"))
        self.assertTrue(all(l["motivo"] in ("alcançável", "s_reach não medido") for l in so_D2))

    def test_pm10_limite_invalido(self):
        verif = [{"programa": "NenhumaIsoladaCorrigida", "base": "E0", "discordancias": 0, "discordancias_documentadas": 0},
                 {"programa": "ParAdjacente", "base": "E0", "discordancias": 0, "discordancias_documentadas": 2}]
        pm10 = P.tabela_pm10(_pm8_constante(), bases=("E0",), B=10_000, verificacao=verif)
        por = {l["degrau"]: l for l in pm10}
        self.assertEqual(por["NenhumaIsolada"]["programa"], "NenhumaIsoladaCorrigida")
        self.assertEqual(por["NenhumaIsolada"]["tamanho_com_anteriores"], 15)
        self.assertTrue(por["ParAdjacente"]["limite_invalido"])
        self.assertIsNone(por["ParAdjacente"]["alcancavel_com_anteriores"])

    def _f6(self, evid_braco, lfix_resolve=False):
        res = {"tarefa_id": "passo", "aceita": True, "reutilizacoes": {"abs1": 1}}
        bracos = {evid_braco: {"relatorio": {"resultados": [res]},
                               "abstracoes": [{"nome": "abs1", "proveniencia": "descoberta", "copia_de_solucao": False}]}}
        return {"bracos": bracos, "custo_igual": [{"braco": evid_braco, "tarefa": "passo",
                                                    "lfix_resolve_a_custo_igual": lfix_resolve}]}

    def test_exigencia_autonoma_por_base(self):
        pm10 = P.tabela_pm10(_pm8_constante(), B=10_000)
        self.assertEqual(P.decidir(pm10, self._f6("L-lib@E0mais"))["decisao"], "NO-GO")
        self.assertEqual(P.decidir(pm10, self._f6("L-lib@E0"))["decisao"], "GO com E0")
        self.assertEqual(P.decidir(pm10, self._f6("L-lib@E0"), aut_min_tarefas=2)["decisao"], "NO-GO")
        self.assertEqual(P.decidir(pm10, self._f6("L-lib@E0", None))["decisao"], "NO-GO")   # inconclusivo

    def test_custo_igual_usa_custo_total(self):
        """L-lib com menos candidatos mas compressão cara: pelo custo TOTAL, L-fix resolve a custo igual."""
        def curva(cands, totais, aceitas):
            out, cum, cumc = [], 0, 0
            for t, (c, tot, ac) in zip(("a", "b"), zip(cands, totais, aceitas)):
                cum += tot
                cumc += c
                out.append({"tarefa": t, "aceita": ac, "inconclusivo_recurso": False, "custo_aprendiz": tot,
                            "candidatos": c, "enumeracao": 0, "cumulativo": cum, "cumulativo_candidatos": cumc,
                            "cumulativo_enumeracao": 0})
            return out
        lib = {"curva": curva((10, 5), (100, 10_000), (True, True)),
               "relatorio": {"resultados": [{"tarefa_id": "a", "aceita": True, "reutilizacoes": {}},
                                            {"tarefa_id": "b", "aceita": True, "reutilizacoes": {"abs1": 1}}]}}
        fix = {"curva": curva((10, 50), (100, 2_000), (True, True)), "relatorio": {"resultados": []}}
        out = P.comparar_custo_igual(P.config_mini(), {"L-lib@E0": lib, "L-fix@E0": fix})
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["metrica_primaria"], "total_aprendiz")
        self.assertTrue(out[0]["lfix_resolve_a_custo_igual"])     # 2 100 ≤ 10 100
        self.assertLess(out[0]["secundaria_cumulativo_candidatos_lib"], out[0]["secundaria_cumulativo_candidatos_fix"])

    def test_conciliacao_detecta_lancamento_omitido(self):
        livro = LivroRazao(SEMENTE)
        amb = A.Ambiente(SEMENTE, k_reservatorio=3, ns_reservatorio=(5,), num_teste=3)
        ap = A.LFix(E0, livro, B=2000, K=3, kw_enumerador={"semente": SEMENTE})
        ap.resolver(A.TAREFAS_POR_ID["ExistePreta"], amb)
        braco = {"relatorio": ap.relatorio(), "preparos": [amb.preparar(A.TAREFAS_POR_ID["ExistePreta"]).como_dict()],
                 "livro_entradas": livro.deterministico_dict()["entradas"]}
        self.assertEqual(P.conciliar_livro({"L-fix@E0": braco})["diferenca"], 0)
        braco["livro_entradas"][0]["busca_candidatos"] -= 1      # lançamento omitido na origem
        self.assertEqual(P.conciliar_livro({"L-fix@E0": braco})["diferenca"], 1)

    def test_reaproveitamento_exige_mesmo_codigo(self):
        with tempfile.TemporaryDirectory() as d:
            a = os.path.join(d, "a")
            cfg = P.config_mini(SEMENTE)
            cfg.fases = (2,)
            P.executar(cfg, a)
            caminho = os.path.join(a, "deterministico.json")
            with open(caminho, encoding="utf-8") as f:
                det = json.load(f)
            det["fontes"]["arquivos"]["piloto.py"] = "0" * 64
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(det, f)
            cfg2 = P.config_mini(SEMENTE)
            cfg2.fases = (7,)
            with self.assertRaises(ValueError):
                P.executar(cfg2, None, reaproveitar=a)
            r = P.executar(cfg2, None, reaproveitar=a, aceitar_codigo_diferente=True)
            self.assertEqual(r["deterministico"]["reaproveitamento"]["codigo_diferente_arquivos"], ["piloto.py"])
            self.assertEqual(r["deterministico"]["reaproveitamento"]["cadeia"][0]["origem"], "a")

    def test_memoria_trabalhador_na_configuracao(self):
        self.assertIn("memoria_trabalhador_gb", P.ConfigPiloto().como_dict())


if __name__ == "__main__":
    unittest.main()
