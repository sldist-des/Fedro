"""U23-U24 (documento 03, seção 5) e testes do oráculo (PQ9, PM12-PM13).

U23: 50 pares (h, c), c em F1 ∪ F2, n <= 4, partição oraculo_treino. h vem de duas fontes (25 cada):
  (a) termos fechados de E0 de tipo Grade -> Bool e tamanho <= 6, sorteados da enumeração completa
      sem poda (enumerador.enumerar_sem_poda), avaliados com orçamento de passos;
  (b) predicados Python aleatórios simples (densidade, células, rótulos de outros conceitos do
      REGISTRO e combinações).
  O contraexemplo do oráculo restrito à partição deve ser igual ao mínimo por força bruta restrito à
  MESMA partição (contraexemplo_forca_bruta, implementação independente).
U24: c = LinhasIguais, h = λg. falso, n = 5: o contraexemplo é o positivo construtivo com o menor
  número de pretas (desempate lexicográfico) do reservatório.
"""
import random
import unittest

from fedro_piloto import geradores as G
from fedro_piloto.avaliador import OrcamentoEsgotado, aplicar, avaliar
from fedro_piloto.dsl import BOOL, E0, FUN, GRADE, imprimir, parse
from fedro_piloto.enumerador import enumerar_sem_poda
from fedro_piloto.grade import Grade, chave_minimalidade
from fedro_piloto.oraculo import (ContadorOraculo, MedicaoOraculo, Oraculo, contraexemplo_forca_bruta)
from fedro_piloto.razao import LivroRazao
from fedro_piloto.referencias import REGISTRO

PARTICAO = "oraculo_treino"
ORCAMENTO_H = 20_000
F1_F2 = sorted(n for n, c in REGISTRO.items() if c.familia in ("F1", "F2"))
_ORACULOS = {}


def _oraculo_exaustivo(nome, criterio="sem_par"):
    """Um oráculo por (conceito, critério), só n <= 4 (sem reservatório), partilhado entre testes."""
    if (nome, criterio) not in _ORACULOS:
        _ORACULOS[nome, criterio] = Oraculo(nome, PARTICAO, ns_reservatorio=(), criterio_degenerado=criterio)
    return _ORACULOS[nome, criterio]


def h_de_termo(termo):
    """h: Grade -> bool a partir de um termo fechado; orçamento esgotado = indefinido (exceção)."""
    def h(g):
        return aplicar(avaliar(termo, n=g.n, orcamento_passos=ORCAMENTO_H), g)
    h.descricao = imprimir(termo)
    return h


def _predicado_python(rng, alvo):
    """Predicado Python aleatório simples (determinístico dada a semente). Os tipos "perturbado" e
    "correto" partem da referência do conceito-alvo, para haver contraexemplos só em n = 3 ou 4 e
    hipóteses sem contraexemplo."""
    outros = sorted(REGISTRO)
    tipo = rng.choice(["densidade", "celula", "conceito", "e", "ou_nao", "pretas_mod",
                       "perturbado", "perturbado", "perturbado", "correto"])
    if tipo == "perturbado":
        n0, k0, i, j = rng.choice([3, 4]), rng.randint(1, 6), rng.randint(1, 3), rng.randint(1, 3)
        f = (lambda g, a=alvo, n0=n0, k0=k0, i=i, j=j: REGISTRO[a].ref_b(g) != (
            g.n == n0 and g.contagem_pretas() == k0 and bool(g.celula((i, j)))))
        d = f"{alvo} trocado se n={n0}, pretas={k0}, celula ({i},{j})"
    elif tipo == "correto":
        f = (lambda g, a=alvo: REGISTRO[a].ref_a(g))
        d = f"{alvo} (correta)"
    elif tipo == "densidade":
        t, maior = rng.choice([0.1, 0.25, 0.4, 0.5, 0.6, 0.75]), rng.random() < 0.5
        f = (lambda g, t=t, m=maior: (g.densidade() >= t) if m else (g.densidade() < t))
        d = f"densidade {'>=' if maior else '<'} {t}"
    elif tipo == "celula":
        i, j = rng.randint(1, 4), rng.randint(1, 4)
        f = (lambda g, i=i, j=j: g.dentro((i, j)) and bool(g.celula((i, j))))
        d = f"celula ({i},{j})"
    elif tipo == "conceito":
        nome = rng.choice(outros)
        f = (lambda g, nome=nome: REGISTRO[nome].ref_a(g))
        d = f"conceito {nome}"
    elif tipo == "e":
        a, b = rng.sample(outros, 2)
        f = (lambda g, a=a, b=b: REGISTRO[a].ref_a(g) and REGISTRO[b].ref_b(g))
        d = f"{a} e {b}"
    elif tipo == "ou_nao":
        a = rng.choice(outros)
        i, j = rng.randint(1, 3), rng.randint(1, 3)
        f = (lambda g, a=a, i=i, j=j: (not REGISTRO[a].ref_a(g)) or (g.dentro((i, j)) and bool(g.celula((i, j)))))
        d = f"nao {a} ou celula ({i},{j})"
    else:
        m, r = rng.choice([2, 3]), rng.randint(0, 1)
        f = (lambda g, m=m, r=r: g.contagem_pretas() % m == r)
        d = f"pretas % {m} == {r}"
    f.descricao = d
    return f


class TestU23Minimalidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rng = G.rng_piloto(10_230)
        termos = [t for t, _s in enumerar_sem_poda(E0.para_aprendiz(), None, FUN(GRADE, BOOL), 6)]
        cls.pares = [(h_de_termo(t), rng.choice(F1_F2)) for t in rng.sample(termos, 25)]
        for _ in range(25):
            c = rng.choice(F1_F2)
            cls.pares.append((_predicado_python(rng, c), c))

    def _u23(self, criterio):
        iguais, falhas, com_resposta, por_n = 0, [], 0, {}
        for h, nome in self.pares:
            o = _oraculo_exaustivo(nome, criterio)
            ordem = [n for _f, n in o.ordem_busca]          # tamanhos degenerados no fim
            self.assertEqual(sorted(ordem), [1, 2, 3, 4])
            r_or = o.contraexemplo(h)
            r_fb = contraexemplo_forca_bruta(h, nome, n_max=4, particao=PARTICAO, ns=ordem)
            if r_or == r_fb:
                iguais += 1
            else:
                falhas.append((h.descricao, nome, r_or, r_fb))
            if r_or is not None:
                com_resposta += 1
                g, rot = r_or
                por_n[g.n] = por_n.get(g.n, 0) + 1
                self.assertTrue(G.na_particao(g, PARTICAO))
                self.assertEqual(rot, REGISTRO[nome].rotulo(g))
                self.assertTrue(o.historico[-1].minimo_garantido)
        indef = sum(o.contador.h_indefinido for (_n, c), o in _ORACULOS.items() if c == criterio)
        print(f"\n[U23/PM12, critério {criterio}] {iguais}/50 iguais à força bruta; {com_resposta} com "
              f"contraexemplo; por n: {dict(sorted(por_n.items()))}; grades com h indefinida: {indef}")
        self.assertEqual(len(self.pares), 50)
        self.assertEqual(iguais, 50, falhas[:5])
        self.assertGreaterEqual(com_resposta, 25)   # o teste não é trivial:
        self.assertLess(com_resposta, 50)           # há hipóteses corretas na partição
        self.assertTrue(por_n.get(3, 0) + por_n.get(4, 0) >= 5)   # e contraexemplos em n = 3, 4

    def test_u23_cinquenta_pares_iguais_a_forca_bruta(self):
        """Omissão (degenerados adiados): força bruta com a mesma ordem de tamanhos."""
        self._u23("sem_par")

    def test_u23_sem_criterio_ordem_natural(self):
        """criterio_degenerado="nenhum": ordem (n, pretas, lexicográfica) pura, n = 1..4."""
        o = _oraculo_exaustivo("UmComponente", "nenhum")
        self.assertEqual([n for _f, n in o.ordem_busca], [1, 2, 3, 4])
        self._u23("nenhum")

    def test_forca_bruta_sem_particao(self):
        """Sem partição, a força bruta percorre o domínio inteiro (auditoria)."""
        r = contraexemplo_forca_bruta(lambda g: False, "ExistePreta", n_max=2)
        self.assertEqual(r, (Grade.de_texto("1:1"), True))
        r = contraexemplo_forca_bruta(lambda g: True, "ExistePreta", n_max=2)
        self.assertEqual(r, (Grade.de_texto("1:0"), False))
        with self.assertRaises(ValueError):
            contraexemplo_forca_bruta(lambda g: True, "ExistePreta", ns=[5])
        with self.assertRaises(PermissionError):
            contraexemplo_forca_bruta(lambda g: True, "ExistePreta", particao=G.PARTICAO_CONFIRMATORIA)


class TestU24Reservatorio(unittest.TestCase):
    def test_u24_linhas_iguais_sempre_falso_n5(self):
        h = h_de_termo(parse("(\\ (g Grade) falso)"))
        for semente, n in ((10_240, 5), (10_241, 6)):
            o = Oraculo("LinhasIguais", PARTICAO, G.rng_piloto(semente), ns_reservatorio=(n,))
            r = o.contraexemplo(h, ns=(n,))
            self.assertIsNotNone(r)
            g, rot = r
            self.assertTrue(rot)
            self.assertTrue(REGISTRO["LinhasIguais"].ref_a(g) and REGISTRO["LinhasIguais"].ref_b(g))
            positivos = [e for e in o.reservatorios[n].entradas if e[1]]
            self.assertTrue(positivos)
            minimo = min(positivos, key=lambda e: chave_minimalidade(e[0]))
            self.assertEqual(g, minimo[0])
            self.assertEqual(g.contagem_pretas(), min(e[0].contagem_pretas() for e in positivos))
            self.assertEqual(minimo[2], "positivo_construtivo")
            reg = o.historico[-1]
            self.assertEqual(reg.fonte, "reservatorio:positivo_construtivo")
            self.assertEqual(reg.n, n)
            self.assertFalse(reg.minimo_garantido)

    def test_ordem_global_exaustivo_antes_do_reservatorio(self):
        o = Oraculo("LinhasIguais", PARTICAO, G.rng_piloto(10_242), ns_reservatorio=(5,))
        r = o.contraexemplo(lambda g: False)
        self.assertLessEqual(r[0].n, 4)
        ordem = [n for f, n in o.ordem_busca if f == "exaustivo"]
        self.assertEqual(r, contraexemplo_forca_bruta(lambda g: False, "LinhasIguais", particao=PARTICAO, ns=ordem))

    def test_busca_local_depois_do_reservatorio(self):
        c = REGISTRO["UmComponente"]
        o = Oraculo(c, PARTICAO, G.rng_piloto(10_243), ns_reservatorio=(5,), max_busca_local=200)
        reserv = {e[0] for e in o.reservatorios[5].entradas}
        pretas_reserv = {g.contagem_pretas() for g in reserv}

        def h(g):  # correta em n <= 4 e no reservatório; errada fora dele em n = 5
            v = c.ref_a(g)
            return v if (g.n < 5 or g in reserv) else not v
        r = o.contraexemplo(h)
        self.assertIsNotNone(r)
        g, rot = r
        self.assertEqual(g.n, 5)
        self.assertNotIn(g, reserv)
        self.assertIn(g.contagem_pretas(), pretas_reserv)        # trocas preservam o número de pretas
        self.assertTrue(G.na_particao(g, PARTICAO))
        self.assertEqual(rot, c.rotulo(g))
        self.assertEqual(o.historico[-1].fonte, "busca_local")
        self.assertLessEqual(o.contador.grades_busca_local, 200)
        # sem busca local, h parece correta (nenhuma discordância no domínio examinado)
        o2 = Oraculo(c, PARTICAO, reservatorios=o.reservatorios, ns_reservatorio=(5,), busca_local=False)
        self.assertIsNone(o2.contraexemplo(h))


def _ordenadas_teste(nome):
    """Grades da partição em n = 4 em ordem decrescente de minimalidade (para escolher uma grade 'tardia')."""
    return sorted(G.grades_da_particao(4, PARTICAO), key=chave_minimalidade, reverse=True)


class TestOraculoComportamento(unittest.TestCase):
    def test_indefinido_conta_como_discordancia(self):
        """h indefinida numa grade = discordância: a grade é o contraexemplo (sem aceitação vácua)."""
        nome = "ParAdjacente"
        o = _oraculo_exaustivo(nome)
        ordem = [n for _f, n in o.ordem_busca]
        alvo = contraexemplo_forca_bruta(lambda g: False, nome, particao=PARTICAO, ns=ordem)
        self.assertIsNotNone(alvo)
        # h correta em toda parte, exceto indefinida numa grade grande (positiva) da ordem
        positiva = next(g for g in _ordenadas_teste(nome) if REGISTRO[nome].rotulo(g))

        def h(g):
            if g == positiva:
                raise OrcamentoEsgotado(0)
            return REGISTRO[nome].rotulo(g)
        r = o.contraexemplo(h)
        self.assertEqual(r, (positiva, True))
        self.assertTrue(o.historico[-1].resposta_indefinida)
        self.assertIn(positiva.serializar(), o.historico[-1].indefinidas)
        self.assertEqual(r, contraexemplo_forca_bruta(h, nome, particao=PARTICAO, ns=ordem))

    def test_h_indefinida_em_tudo_nao_e_aceita(self):
        o = _oraculo_exaustivo("ParAdjacente")

        def h(g):
            raise OrcamentoEsgotado(0)
        r = o.contraexemplo(h)
        self.assertIsNotNone(r)
        self.assertTrue(o.historico[-1].resposta_indefinida)

    def test_indefinido_pula_grade_se_desligado(self):
        nome = "ParAdjacente"
        o = Oraculo(nome, PARTICAO, G.rng_piloto(10_001), ns_reservatorio=(), indefinida_discorda=False)
        ordem = [n for _f, n in o.ordem_busca]
        alvo = contraexemplo_forca_bruta(lambda g: False, nome, particao=PARTICAO, ns=ordem)

        def h(g):
            if g == alvo[0]:
                raise OrcamentoEsgotado(0)
            return False
        r = o.contraexemplo(h)
        self.assertNotEqual(r[0], alvo[0])
        self.assertIn(alvo[0].serializar(), o.historico[-1].indefinidas)
        self.assertGreaterEqual(o.contador.h_indefinido, 1)
        self.assertEqual(r, contraexemplo_forca_bruta(h, nome, particao=PARTICAO, ns=ordem,
                                                      indefinida_discorda=False))
        self.assertLess(chave_minimalidade(alvo[0]), chave_minimalidade(r[0]))

    def test_outras_excecoes_propagam_e_tipo(self):
        o = _oraculo_exaustivo("ParAdjacente")
        with self.assertRaises(ZeroDivisionError):
            o.contraexemplo(lambda g: 1 / 0)
        with self.assertRaises(TypeError):
            o.contraexemplo(lambda g: 1)

    def test_h_correta_sem_contraexemplo_e_latencia(self):
        c = REGISTRO["UmComponente"]
        o = Oraculo(c, PARTICAO, G.rng_piloto(10_244))
        self.assertIsNone(o.contraexemplo(c.ref_a))
        reg = o.historico[-1]
        esperadas = sum(len(G.grades_da_particao(n, PARTICAO)) for n in (1, 2, 3, 4))
        self.assertGreaterEqual(reg.grades_examinadas, esperadas)
        lat = o.medicao.latencias_s[-1]
        print(f"\n[PM13] latência de uma rodada sem contraexemplo (h Python): {lat:.3f} s "
              f"({reg.grades_examinadas} grades)")
        self.assertLess(lat, 10.0)   # I3: interrupção acima de 10 s por rodada

    def test_rotulo_restrito_a_particao(self):
        o = _oraculo_exaustivo("ExistePreta")
        dentro = G.grades_da_particao(3, PARTICAO)[0]
        fora = next(g for g in G.grades_da_particao(3, None) if not G.na_particao(g, PARTICAO))
        self.assertEqual(o.rotulo(dentro), REGISTRO["ExistePreta"].rotulo(dentro))
        with self.assertRaises(PermissionError):
            o.rotulo(fora)
        with self.assertRaises(PermissionError):
            Oraculo("ExistePreta", G.PARTICAO_CONFIRMATORIA, ns_reservatorio=())
        with self.assertRaises(ValueError):
            Oraculo("ExistePreta", PARTICAO)          # sem rng nem reservatórios para n = 5, 6

    def test_grades_mostradas_e_exclusao(self):
        o = Oraculo("DoisSeparados", PARTICAO, ns_reservatorio=())
        r = o.contraexemplo(lambda g: False)
        g0 = G.grades_da_particao(4, PARTICAO)[7]
        o.rotulo(g0)
        extra = G.grades_da_particao(4, PARTICAO)[9]
        o.registrar_mostradas([extra], "exemplo_inicial")
        hs = o.hashes_mostrados()
        self.assertEqual(hs, frozenset({r[0].hash_hex(), g0.hash_hex(), extra.hash_hex()}))
        conjunto = G.grades_da_particao(4, PARTICAO)[:12]
        restantes = o.excluir_mostradas(conjunto)
        self.assertEqual(len(restantes), len(conjunto) - 2)
        pares = o.excluir_mostradas([(g, True) for g in conjunto])
        self.assertEqual(len(pares), len(conjunto) - 2)
        self.assertEqual(o.hash_mostradas(), G.hash_conjunto([r[0], g0, extra]))

    def test_livro_razao_e_separacao_de_custos(self):
        o = Oraculo("TopoCheio", PARTICAO, G.rng_piloto(10_245), ns_reservatorio=(5,))
        livro = LivroRazao(10_245)
        o.lancar_construcao(livro, "TopoCheio", "L-fix")
        o.contraexemplo(lambda g: False, livro=livro, tarefa_id="TopoCheio", aprendiz_id="L-fix")
        o.contraexemplo(REGISTRO["TopoCheio"].ref_b, livro=livro, tarefa_id="TopoCheio", aprendiz_id="L-fix")
        o.rotulo(G.grades_da_particao(3, PARTICAO)[0], livro=livro, tarefa_id="TopoCheio", aprendiz_id="L-fix")
        e = livro.entrada("TopoCheio", "L-fix")
        self.assertEqual(e.oraculo_consultas, 3)
        self.assertEqual(e.oraculo_custo_ambiente, sum(r.grades_examinadas for r in o.historico) + 1)
        self.assertEqual(e.oraculo_custo_ambiente - 1, o.contador.grades_examinadas)
        self.assertEqual(e.geracao_grades, o.contador_construcao.grades_geradas)
        self.assertTrue(livro.verificar_fechamento().ok)
        # contadores só inteiros; medições em estrutura separada
        self.assertTrue(all(isinstance(v, int) for v in o.contador.como_dict().values()))
        self.assertIsInstance(o.medicao, MedicaoOraculo)
        self.assertNotIsInstance(o.contador, MedicaoOraculo)
        det = repr(o.estado_deterministico())
        for chave in ("tempo", "memoria", "latencia"):
            self.assertNotIn(chave, det)
        self.assertEqual(o.proveniencia, "ambiente")

    def test_determinismo_por_semente(self):
        def rodar():
            o = Oraculo("NenhumaIsolada", PARTICAO, G.rng_piloto(10_246))
            o.contraexemplo(lambda g: False)
            o.contraexemplo(lambda g: g.contagem_pretas() >= 2)
            o.contraexemplo(REGISTRO["NenhumaIsolada"].ref_a)
            return o.estado_deterministico()
        self.assertEqual(rodar(), rodar())

    def test_degenerado_nunca_descarta(self):
        """ExistePreta: todos os n <= 4 são degenerados pelo critério 'sem_par' (o único negativo, a
        grade vazia, não tem par). Descartá-los faria h = falso parecer correta em n <= 4; o oráculo
        adia-os, e continua a devolver o mínimo."""
        o = Oraculo("ExistePreta", PARTICAO, ns_reservatorio=(), criterio_degenerado="sem_par")
        self.assertEqual(o.tamanhos_adiados(), [1, 2, 3, 4])
        r = o.contraexemplo(lambda g: False)
        self.assertIsNotNone(r)
        self.assertEqual(r, contraexemplo_forca_bruta(lambda g: False, "ExistePreta", particao=PARTICAO))
        self.assertTrue(o.diagnostico[4]["degenerado"])
        # degenerados adiados: n = 1, 2 vão para depois de n = 3, 4
        o2 = _oraculo_exaustivo("UmComponente")
        self.assertEqual(o2.tamanhos_adiados(), [1, 2])
        self.assertEqual([n for _f, n in o2.ordem_busca], [3, 4, 1, 2])
        # reservatório externo de outro conceito é recusado
        o3 = Oraculo("LinhasIguais", PARTICAO, G.rng_piloto(10_247), ns_reservatorio=(5,))
        with self.assertRaises(ValueError):
            Oraculo("UmComponente", PARTICAO, reservatorios=o3.reservatorios, ns_reservatorio=(5,))


if __name__ == "__main__":
    unittest.main()
