"""U6-U10 (documento 03, seção 5) e testes de partição por instância e degeneração.

Reduções declaradas (para a suíte rodar em minutos):
- U7: 300 positivos por (conceito, n) em vez de 1 000, n de 1 a 6, partição oraculo_treino
  (para n <= 4 limitado pelo número de positivos distintos existentes na partição).
- U8: 30 positivos por (conceito, n), n de 3 a 6.
- U9: 8 positivos por (conceito, n), n = 3 e 4 com força bruta; n = 5 só invariantes do caminho.
- U10: 100 pares por (conceito, n), n de 3 a 6. Vazão (PM3) medida para 3 conceitos em n = 6.
"""
import math
import unittest

from fedro_piloto.grade import Grade, chave_minimalidade, todas_as_grades
from fedro_piloto.referencias import REGISTRO
from fedro_piloto import geradores as G

PARTICAO = "oraculo_treino"


def _ambas(c, g):
    a, b = c.ref_a(g), c.ref_b(g)
    assert a == b, (c.nome, g.serializar())
    return a


class TestParticoes(unittest.TestCase):
    def test_particoes_disjuntas_e_completas(self):
        baldes = [b for r in G.PARTICOES.values() for b in r]
        self.assertEqual(sorted(baldes), list(range(100)))

    def test_confirmatoria_bloqueada(self):
        rng = G.rng_piloto(10_010)
        c = REGISTRO["UmComponente"]
        with self.assertRaises(PermissionError):
            G.gerar_positivo(c, 5, G.PARTICAO_CONFIRMATORIA, rng)
        with self.assertRaises(PermissionError):
            G.conjunto_de_desenho(c, 5, G.PARTICAO_CONFIRMATORIA, 5, rng)
        with self.assertRaises(PermissionError):
            G.capacidade_particao(3, G.PARTICAO_CONFIRMATORIA)
        with self.assertRaises(ValueError):
            G.verificar_particao("treino")

    def test_sementes(self):
        G.rng_piloto(10_000)
        G.rng_piloto(19_999)
        for s in (9_999, 20_000):
            with self.assertRaises(ValueError):
                G.rng_piloto(s)
        with self.assertRaises(ValueError):
            G.rng_confirmatorio(19_999)
        G.rng_confirmatorio(20_000)

    def test_geradores_respeitam_particao(self):
        rng = G.rng_piloto(10_011)
        for part in ("oraculo_treino", "validacao", "teste_int", "teste_ext"):
            for n in (3, 5, 7):
                c = REGISTRO["NoMaximoDois"]
                negs = []
                for _ in range(10):  # um positivo isolado pode não ter par na partição (n = 3)
                    g = G.gerar_positivo(c, n, part, rng)
                    self.assertEqual(G.particao_de(g), part)
                    neg = G.negativo_emparelhado(g, c, rng, part, "auto", L=300)
                    if neg is not None:
                        negs.append(neg[0])
                self.assertTrue(negs)
                self.assertTrue(all(G.particao_de(t) == part for t in negs))
                self.assertEqual(G.particao_de(G.amostra_natural(n, rng, particao=part)), part)

    def test_disjuncao_por_instancia_entre_conjuntos(self):
        rng = G.rng_piloto(10_012)
        c = REGISTRO["ParAdjacente"]
        a = G.conjunto_de_desenho(c, 5, "oraculo_treino", 50, rng)
        b = G.conjunto_de_desenho(c, 5, "teste_int", 50, rng)
        self.assertFalse({g for g, _ in a} & {g for g, _ in b})


class TestCapacidadeEDegeneracao(unittest.TestCase):
    def test_capacidade_contagens_fecham(self):
        total = 0
        for part in G.PARTICOES:
            cap = G.capacidade_particao(3, part, permitir_confirmatorio=True)
            total += cap["grades_na_particao"]
            for nome, d in cap["por_conceito"].items():
                self.assertEqual(d["positivos"] + d["negativos"], cap["grades_na_particao"], nome)
                self.assertLessEqual(d["positivos_com_par"], d["positivos"])
        self.assertEqual(total, 512)
        dom = G.capacidade_particao(3, None)
        self.assertEqual(dom["grades_na_particao"], 512)
        direto = sum(REGISTRO["UmComponente"].ref_a(g) for g in todas_as_grades(3))
        self.assertEqual(dom["por_conceito"]["UmComponente"]["positivos"], direto)

    def test_linhas_iguais_n1_sem_negativos(self):
        cap = G.capacidade_particao(1, None, ["LinhasIguais"])
        self.assertEqual(cap["total_dominio"], 2)
        self.assertEqual(cap["por_conceito"]["LinhasIguais"]["negativos"], 0)
        rng = G.rng_piloto(10_020)
        for part in ("oraculo_treino", "validacao", "teste_int", "teste_ext"):
            d = G.degenerado(REGISTRO["LinhasIguais"], 1, part, rng)
            self.assertTrue(d["degenerado"])
            self.assertTrue(d["exaustivo"])
            self.assertFalse(d["negativos_possiveis"])

    def test_dois_separados_n1_sem_positivos(self):
        cap = G.capacidade_particao(1, None, ["DoisSeparados"])
        self.assertEqual(cap["por_conceito"]["DoisSeparados"]["positivos"], 0)
        d = G.degenerado(REGISTRO["DoisSeparados"], 1, None, G.rng_piloto(10_021))
        self.assertTrue(d["degenerado"])
        self.assertFalse(d["positivos_possiveis"])
        self.assertIn("sem positivos", d["motivo"])

    def test_tres_componentes_n2_impossivel(self):
        d = G.degenerado(REGISTRO["TresComponentes"], 2, None, G.rng_piloto(10_022))
        self.assertFalse(d["positivos_possiveis"])

    def test_existe_preta_nunca_emparelhavel(self):
        # o único negativo de ExistePreta é a grade vazia: nenhum par com o mesmo número de pretas
        c = REGISTRO["ExistePreta"]
        for n in (2, 3, 4):
            self.assertFalse(G.degenerado(c, n, None, G.rng_piloto(10_023))["negativos_emparelhados_possiveis"])
        d5 = G.degenerado(c, 5, PARTICAO, G.rng_piloto(10_023), tentativas=200)
        self.assertTrue(d5["degenerado"])
        self.assertFalse(d5["exaustivo"])
        with self.assertRaises(G.ConceitoDegenerado):
            G.conjunto_de_desenho(c, 5, PARTICAO, 10, G.rng_piloto(10_023))

    def test_nao_degenerado(self):
        rng = G.rng_piloto(10_024)
        for nome in ("UmComponente", "LinhasIguais", "NoMax_metadeEsq_metadeDir"):
            self.assertFalse(G.degenerado(REGISTRO[nome], 4, PARTICAO, rng)["degenerado"], nome)
            self.assertFalse(G.degenerado(REGISTRO[nome], 6, PARTICAO, rng, tentativas=300)["degenerado"], nome)

    def test_conjunto_recusa_degenerado(self):
        with self.assertRaises(G.ConceitoDegenerado):
            G.conjunto_de_desenho(REGISTRO["LinhasIguais"], 1, PARTICAO, 5, G.rng_piloto(10_025))


class U6Frequencia(unittest.TestCase):
    def test_u6_linhas_iguais_n4_p05(self):
        exato = sum((math.comb(4, k) / 16) ** 4 for k in range(5))
        self.assertAlmostEqual(exato, 1810 / 65536)
        self.assertAlmostEqual(exato, 0.028, places=3)
        cap = G.capacidade_particao(4, None, ["LinhasIguais"])
        self.assertEqual(cap["por_conceito"]["LinhasIguais"]["positivos"], 1810)
        rng = G.rng_piloto(10_006)
        N = 100_000
        c = REGISTRO["LinhasIguais"]
        k = sum(c.rotulo(G.amostra_natural(4, rng, ps=(0.5,))) for _ in range(N))
        dp = math.sqrt(exato * (1 - exato) / N)
        self.assertLess(abs(k / N - exato), 3 * dp)


class U7Positivos(unittest.TestCase):
    N = 300

    def test_u7(self):
        rng = G.rng_piloto(10_007)
        for c in REGISTRO.values():
            for n in range(1, 7):
                d = G.degenerado(c, n, PARTICAO, rng, tentativas=300)
                if not d["positivos_possiveis"]:
                    continue
                cont = G.ContadorGeracao()
                alvo = self.N if n > 4 else min(self.N, d["contagens"]["positivos"])
                gs = []
                for _ in range(alvo):
                    g = G.gerar_positivo(c, n, PARTICAO, rng, cont, tentativas=300)
                    if g is not None:
                        gs.append(g)
                with self.subTest(conceito=c.nome, n=n):
                    self.assertTrue(gs)
                    self.assertTrue(all(_ambas(c, g) for g in gs))
                    self.assertTrue(all(G.particao_de(g) == PARTICAO for g in gs))
                    if n >= 3:  # PM2
                        self.assertGreaterEqual(cont.taxa_aceitacao(), 0.5)


class U8Emparelhados(unittest.TestCase):
    def test_u8(self):
        rng = G.rng_piloto(10_008)
        for c in REGISTRO.values():
            for n in range(3, 7):
                for i in range(30):
                    g = G.gerar_positivo(c, n, PARTICAO, rng, tentativas=300)
                    if g is None:
                        break
                    neg = G.negativo_emparelhado(g, c, rng, PARTICAO, ("permutacao", "troca")[i % 2], L=300)
                    if neg is None:
                        continue
                    t, num_trocas, metodo = neg
                    with self.subTest(conceito=c.nome, n=n, metodo=metodo):
                        self.assertEqual(t.contagem_pretas(), g.contagem_pretas())
                        self.assertFalse(_ambas(c, t))
                        self.assertEqual(G.particao_de(t), PARTICAO)
                        self.assertEqual(num_trocas, sum(a != b for a, b in zip(g.bits, t.bits)) // 2
                                         if metodo == "permutacao" else num_trocas)


def _forca_bruta(c, n, particao):
    """Por número de pretas: lista de grades negativas na partição (refs chamadas diretamente)."""
    por_k = {}
    for t in todas_as_grades(n):
        if G.na_particao(t, particao) and not _ambas(c, t):
            por_k.setdefault(t.contagem_pretas(), []).append(t)
    return por_k


class U9QuaseAcerto(unittest.TestCase):
    def _caminho_valido(self, c, g, qa):
        self.assertEqual(qa.caminho[0], g)
        self.assertEqual(qa.caminho[-1], qa.grade)
        self.assertEqual(len(qa.trocas), len(qa.caminho) - 1)
        for (p, q), a, b in zip(qa.trocas, qa.caminho, qa.caminho[1:]):
            self.assertEqual(a.celula(p), 1)
            self.assertEqual(a.celula(q), 0)
            self.assertEqual(a.trocar(p, q), b)
        self.assertTrue(_ambas(c, qa.caminho[-2]))   # antes da última troca: positiva
        self.assertFalse(_ambas(c, qa.caminho[-1]))  # depois: negativa

    def test_u9_minimo_por_forca_bruta(self):
        rng = G.rng_piloto(10_009)
        for n in (3, 4):
            for c in REGISTRO.values():
                bruta = None
                for _ in range(8):
                    g = G.gerar_positivo(c, n, PARTICAO, rng, tentativas=300)
                    if g is None:
                        break
                    if bruta is None:
                        bruta = _forca_bruta(c, n, PARTICAO)
                    alvos = bruta.get(g.contagem_pretas(), [])
                    qa = G.quase_acerto(g, c, rng, PARTICAO)
                    with self.subTest(conceito=c.nome, n=n, g=g.serializar()):
                        if not alvos:
                            self.assertIsNone(qa)
                            continue
                        self.assertIsNotNone(qa)
                        self._caminho_valido(c, g, qa)
                        minimo = min(sum(a != b for a, b in zip(g.bits, t.bits)) // 2 for t in alvos)
                        if qa.minimo_garantido:
                            self.assertEqual(len(qa.trocas), minimo)
                        else:
                            self.assertGreaterEqual(len(qa.trocas), minimo)

    def test_u9_caminho_n5(self):
        rng = G.rng_piloto(10_019)
        for c in REGISTRO.values():
            for _ in range(3):
                g = G.gerar_positivo(c, 5, PARTICAO, rng, tentativas=300)
                if g is None:
                    break
                qa = G.quase_acerto(g, c, rng, PARTICAO, L=500)
                if qa is None:
                    continue
                with self.subTest(conceito=c.nome, nivel=qa.nivel):
                    self._caminho_valido(c, g, qa)
                    self.assertEqual(G.particao_de(qa.grade), PARTICAO)
                    if qa.nivel == "troca1":
                        self.assertTrue(qa.minimo_garantido)


class U10M10(unittest.TestCase):
    def test_m10_unidade(self):
        a, b = Grade.de_texto("2:1000"), Grade.de_texto("2:0001")
        self.assertEqual(G.m10([(a, True), (b, False)]), 0.5)
        cheia, vazia = Grade.de_texto("2:1111"), Grade.de_texto("2:0000")
        self.assertEqual(G.m10([(cheia, True), (vazia, False)]), 1.0)
        self.assertEqual(G.m10([(cheia, False), (vazia, True)]), 1.0)  # polaridade invertida
        with self.assertRaises(ValueError):
            G.m10([(a, True)])

    def test_m10_detecta_confundidor(self):
        # conjunto balanceado por rejeição natural: positivos de UmComponente em n = 6 são densos
        rng = G.rng_piloto(10_030)
        c = REGISTRO["UmComponente"]
        pos, neg = [], []
        while len(pos) < 100 or len(neg) < 100:
            g = G.amostra_natural(6, rng)
            (pos if c.rotulo(g) else neg).append(g)
        exemplos = [(g, True) for g in pos[:100]] + [(g, False) for g in neg[:100]]
        self.assertGreater(G.m10(exemplos), 0.55)

    def test_u10_conjuntos_de_desenho(self):
        for c in REGISTRO.values():
            for n in (3, 4, 5, 6):
                rng = G.rng_piloto(10_100 + n)
                try:
                    cj = G.conjunto_de_desenho(c, n, PARTICAO, 100, rng)
                except G.ConceitoDegenerado as e:
                    with self.subTest(conceito=c.nome, n=n, degenerado=e.info.get("motivo")):
                        if n <= 4:  # coerência com o diagnóstico exaustivo
                            self.assertTrue(G.degenerado(c, n, PARTICAO, rng)["degenerado"])
                        else:
                            self.assertEqual(c.nome, "ExistePreta")
                    continue
                m = cj.metadados
                with self.subTest(conceito=c.nome, n=n):
                    self.assertLessEqual(m["m10"], 0.55)
                    self.assertEqual(m["fracao_mesmo_numero_pretas"], 1.0)
                    self.assertEqual(sum(r for _, r in cj), len(cj) // 2)
                    self.assertTrue(all(_ambas(c, g) == r for g, r in cj))
                    self.assertTrue(all(G.particao_de(g) == PARTICAO for g, _ in cj))
                    positivos = [g for g, r in cj if r]
                    self.assertEqual(len(set(positivos)), len(positivos))
                    if n >= 5:
                        self.assertEqual(m["k_pares_obtido"], 100)

    def test_pm3_vazao(self):
        for nome in ("UmComponente", "LinhasIguais", "NoMax_metadeEsq_metadeDir"):
            cj = G.conjunto_de_desenho(REGISTRO[nome], 6, PARTICAO, 1000, G.rng_piloto(10_200))
            with self.subTest(conceito=nome):
                self.assertEqual(cj.metadados["k_pares_obtido"], 1000)
                self.assertLessEqual(cj.medicao.tempo_parede_s, 60.0)  # medição real, não contador


class TestReservatorioECusto(unittest.TestCase):
    def test_reservatorio_ordenado(self):
        c = REGISTRO["LinhasIguais"]
        res = G.reservatorio_oraculo(c, 5, PARTICAO, G.rng_piloto(10_040), 30)
        chaves = [chave_minimalidade(g) for g, _, _ in res.entradas]
        self.assertEqual(chaves, sorted(chaves))
        self.assertEqual(len({g for g, _, _ in res.entradas}), len(res.entradas))
        origens = {o for _, _, o in res.entradas}
        self.assertTrue({"positivo_construtivo", "quase_acerto"} <= origens)
        for g, r, _ in res.entradas:
            self.assertEqual(_ambas(c, g), r)
            self.assertEqual(G.particao_de(g), PARTICAO)

    def test_determinismo_e_separacao_contador_medicao(self):
        c = REGISTRO["NenhumaIsolada"]
        a = G.conjunto_de_desenho(c, 5, PARTICAO, 40, G.rng_piloto(10_050))
        b = G.conjunto_de_desenho(c, 5, PARTICAO, 40, G.rng_piloto(10_050))
        self.assertEqual(a.metadados["hash"], b.metadados["hash"])
        self.assertEqual([g for g, _ in a], [g for g, _ in b])
        self.assertEqual({k: v.como_dict() for k, v in a.contadores.items()},
                         {k: v.como_dict() for k, v in b.contadores.items()})
        campos_contador = set(G.ContadorGeracao().como_dict())
        campos_medicao = set(G.MedicaoGeracao().como_dict())
        self.assertFalse(campos_contador & campos_medicao)
        self.assertNotIn("tempo_parede_s", a.metadados)
        self.assertGreater(a.contadores["positivos"].chamadas_rotulo, 0)

    def test_proveniencia_ambiente(self):
        cj = G.conjunto_de_desenho(REGISTRO["ParAdjacente"], 4, PARTICAO, 10, G.rng_piloto(10_060))
        self.assertEqual(cj.metadados["proveniencia"], "ambiente")
        self.assertEqual(G.PROVENIENCIA, "ambiente")


if __name__ == "__main__":
    unittest.main()
