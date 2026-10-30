"""Testes de enumerador.py: U19, U20 e a validação obrigatória da poda OE (correção 3).

Tamanhos máximos verificados (registrados aqui e nos atributos das classes):
  U19 força bruta independente (gera-e-testa ascendente + dsl.tipo_de): s ≤ 4 em Grade → Bool
      (fechado) e em {g:Grade} ⊢ Bool, com e sem redexes β;
  contagem DP = enumeração sem poda: s ≤ 7 em {g} ⊢ Bool e {g} ⊢ L Pos; s ≤ 8 em L Pos → L Pos
      (fechado, inclui fix); s ≤ 7 em L Pos → L Pos → L Pos;
  V1 (mecanismo; mundos OE = todas as 512 grades n = 3, modo auditoria): s ≤ 6 em {g} ⊢ Bool e
      {g} ⊢ L Pos — denotações sobre as 512 grades n = 3 iguais às do sem-poda, tamanho mínimo igual;
  V2 (amostra de produção, só oraculo_treino): s ≤ 7 em {g} ⊢ Bool, s ≤ 6 em {g} ⊢ L Pos — todo
      termo do sem-poda tem representante com a mesma assinatura OE e tamanho ≤.
"""
import random
import unittest
from collections import Counter

from fedro_piloto import enumerador as EN
from fedro_piloto import geradores as G
from fedro_piloto import programas_referencia as PR
from fedro_piloto.avaliador import Contador, Contexto, aplicar, avaliar, compilar
from fedro_piloto.dsl import (BOOL, E0, E0P, GRADE, LP, POS, FUN, AP, C, LAM, V, ErroProveniencia,
                              entrada_biblioteca, imprimir, parse, subtipos, tamanho, tipo_de)
from fedro_piloto.enumerador import (ContadorBusca, ContadorEnumeracao, Enumerador, EstadoBusca, Gramatica,
                                     buscar, contar_termos, enumerar_sem_poda, grades_amostra_oe,
                                     medir_alcance, registrar_reutilizacoes, tabela_contagens)
from fedro_piloto.grade import Grade, todas_as_grades
from fedro_piloto.referencias import REGISTRO

E0D = E0.para_aprendiz()
GR3 = list(todas_as_grades(3))


# ---------------------------------------------------------------- força bruta independente (U19)
def forca_bruta(tabela, gamma0, alvo, s_max, D=2, beta=False):
    """Gera-e-testa ascendente, sem direção por tipo: todos os pares (f, a) de termos já gerados no
    mesmo contexto são combinados e testados; binders λ percorrem os tipos-argumento de T e a λ é
    mantida se o seu tipo está em T. Sem fix (fix tem tamanho ≥ 5). Cada termo final é verificado
    por dsl.tipo_de. Devolve {s: set(termos de tipo alvo)}."""
    T = Gramatica(tabela, gamma0, alvo, D).T
    A = sorted({t[1] for t in T if t[0] == "Fun"}, key=repr)
    consts = [(C(p.nome), p.tipo) for p in tabela]
    memo = {}

    def termos(ctx, s):
        k = (ctx, s)
        if k in memo:
            return memo[k]
        out = []
        if s == 1:
            out += consts + [(V(n), t) for n, t in gamma0] + [(V(f"x{i}"), t) for i, t in enumerate(ctx)]
        else:
            for s1 in range(1, s):
                xs = termos(ctx, s - s1)
                for f, tf in termos(ctx, s1):
                    if tf[0] != "Fun" or (not beta and f[0] == "lam"):
                        continue
                    for x, tx in xs:
                        if tf[1] == tx:
                            out.append((("ap", f, x), tf[2]))
            if len(ctx) < D:
                for a in A:
                    for c, tc in termos(ctx + (a,), s - 1):
                        if FUN(a, tc) in T:
                            out.append((LAM(f"x{len(ctx)}", a, c), FUN(a, tc)))
        memo[k] = out
        return out

    res = {}
    for s in range(1, s_max + 1):
        sel = {t for t, ty in termos((), s) if ty == alvo}
        for t in sel:
            assert tipo_de(t, dict(gamma0), tabela) == alvo
        res[s] = sel
    return res


class U19ContagemEForcaBruta(unittest.TestCase):
    S_FORCA_BRUTA = 4

    def _compara(self, gamma0, alvo, beta):
        fb = forca_bruta(E0D, gamma0, alvo, self.S_FORCA_BRUTA, beta=beta)
        sp = {}
        for t, s in enumerar_sem_poda(E0D, dict(gamma0), alvo, self.S_FORCA_BRUTA, redexes_beta=beta):
            sp.setdefault(s, []).append(t)
        dp = contar_termos(E0D, alvo, dict(gamma0), self.S_FORCA_BRUTA, redexes_beta=beta)
        for s in range(1, self.S_FORCA_BRUTA + 1):
            l = sp.get(s, [])
            self.assertEqual(len(l), len(set(l)), "sem-poda gerou duplicatas")
            self.assertEqual(set(l), fb[s], f"s={s}")
            self.assertEqual(dp[s], len(fb[s]), f"s={s}")
            for t in l:
                self.assertEqual(tamanho(t), s)
        return dp

    def test_U19_grade_bool_fechado(self):
        dp = self._compara((), FUN(GRADE, BOOL), beta=False)
        self.assertEqual(dp, {1: 0, 2: 2, 3: 4, 4: 22})
        dp_beta = self._compara((), FUN(GRADE, BOOL), beta=True)
        self.assertEqual(dp_beta, {1: 0, 2: 2, 3: 4, 4: 34})

    def test_U19_contexto_g_bool(self):
        self._compara((("g", GRADE),), BOOL, beta=False)
        self._compara((("g", GRADE),), BOOL, beta=True)

    def test_fix_ausente_ate_4(self):
        for alvo in (FUN(GRADE, BOOL), FUN(LP, LP)):
            self.assertEqual(contar_termos(E0D, alvo, {}, 4), contar_termos(E0D, alvo, {}, 4, fix=False))
        # fix (λrec x0. rec x0) é o menor fix: tamanho 5
        self.assertGreater(contar_termos(E0D, FUN(LP, LP), {}, 5)[5],
                           contar_termos(E0D, FUN(LP, LP), {}, 5, fix=False)[5])

    def test_dp_igual_sem_poda(self):
        casos = [({"g": GRADE}, BOOL, 7), ({"g": GRADE}, LP, 7), ({}, FUN(LP, LP), 8),
                 ({}, FUN(LP, LP, LP), 7), ({}, FUN(GRADE, BOOL), 7)]
        for ctx, alvo, smax in casos:
            for beta in (False, True):
                if beta and smax > 6:
                    smax = 6
                dp = contar_termos(E0D, alvo, ctx, smax, redexes_beta=beta)
                sp = Counter(s for _, s in enumerar_sem_poda(E0D, ctx, alvo, smax, redexes_beta=beta))
                self.assertEqual({s: sp.get(s, 0) for s in dp}, dp, (ctx, alvo, beta))

    def test_estrutura_fix(self):
        """Todo fix gerado: forma canônica, rec ocorre, argumentos de rec sem rec, bem tipado."""
        n_fix = 0
        for t, s in enumerar_sem_poda(E0D, {}, FUN(LP, LP, BOOL), 7):
            self.assertEqual(tamanho(t), s)
            self.assertEqual(tipo_de(t, {}, E0D), FUN(LP, LP, BOOL))
            for u in _subtermos(t):
                if u[0] != "fix":
                    continue
                n_fix += 1
                f = u[2]
                self.assertEqual((f[0], f[1]), ("lam", EN.REC))
                corpo = f[3]
                for _ in range(len(_args(u[1]))):
                    self.assertEqual(corpo[0], "lam")
                    corpo = corpo[3]
                self.assertIn(EN.REC, _livres(corpo))
                for w in _subtermos(corpo):
                    if w[0] == "ap" and _cabeca(w) == V(EN.REC):
                        for arg in _argumentos(w):
                            self.assertNotIn(EN.REC, _livres(arg))
        self.assertGreater(n_fix, 0)

    def test_PM7_tabela_contagens(self):
        for tb in (E0D, E0P):
            linhas = tabela_contagens(tb, 12)
            self.assertEqual(len(linhas), 5)
            for l in linhas:
                self.assertGreater(l["contagens"][12], 0)
                for s in range(9, 13):
                    self.assertTrue(3 < l["razoes"][s] < 12, (l["tipo"], s, l["razoes"][s]))


def _subtermos(t):
    yield t
    if t[0] == "ap":
        yield from _subtermos(t[1]); yield from _subtermos(t[2])
    elif t[0] == "lam":
        yield from _subtermos(t[3])
    elif t[0] == "fix":
        yield from _subtermos(t[2])


def _livres(t):
    from fedro_piloto.dsl import variaveis_livres
    return variaveis_livres(t)


def _cabeca(t):
    while t[0] == "ap":
        t = t[1]
    return t


def _argumentos(t):
    out = []
    while t[0] == "ap":
        out.append(t[2]); t = t[1]
    return out


def _args(tipo):
    from fedro_piloto.dsl import argumentos_e_resultado
    return argumentos_e_resultado(tipo)[0]


# ---------------------------------------------------------------- denotação vetorial (validação)
class _Denot:
    """Valores de termos de {g:Grade} sobre uma lista de grades n = 3, por composição memoizada
    (apenas subtermos de tamanho ≤ 4) com as primitivas do avaliador; λ e fix pelo avaliador."""

    def __init__(self, grades, tabela):
        self.gr = grades
        self.ctx = Contexto(3, Contador(), tabela)
        self.memo = {}

    def __call__(self, t):
        r = self.memo.get(t)
        if r is not None:
            return r
        k = t[0]
        if k == "v":
            r = self.gr
        elif k == "c":
            r = [self.ctx.constante(t[1])] * len(self.gr)
        elif k == "ap":
            r = [f(x) for f, x in zip(self(t[1]), self(t[2]))]
        else:
            ev = compilar(t)
            r = [ev({"g": g}, self.ctx) for g in self.gr]
        if tamanho(t) <= 4:
            self.memo[t] = r
        return r


class U20PodaOE(unittest.TestCase):
    """Validação obrigatória da poda OE (correção 3)."""
    S_V1 = {BOOL: 6, LP: 6}
    S_V2 = {BOOL: 7, LP: 6}

    @classmethod
    def setUpClass(cls):
        cls.den = _Denot(GR3, E0D)
        cls.sem_poda = {}
        for tau in (BOOL, LP):
            smax = max(cls.S_V1[tau], cls.S_V2[tau])
            cls.sem_poda[tau] = list(enumerar_sem_poda(E0D, {"g": GRADE}, tau, smax))

    def test_denotacao_vetorial_confere_com_avaliar(self):
        rng = random.Random(10_007)
        termos = [t for t, _ in self.sem_poda[BOOL] + self.sem_poda[LP]]
        for t in rng.sample(termos, 150):
            v = self.den(t)
            for i in rng.sample(range(len(GR3)), 12):
                self.assertEqual(v[i], avaliar(t, {"g": GR3[i]}, 3, tabela=E0D))

    def test_V1_mecanismo_igual_ao_sem_poda_em_todas_as_grades_n3(self):
        """(a) mesmas denotações nas 512 grades n = 3; (b) mesmo tamanho mínimo por denotação;
        (c) contagem do sem-poda = DP. Mundos OE = as 512 grades (auditoria) para isolar o mecanismo
        da adequação da amostra (ver test_limitacao_particao)."""
        for tau in (BOOL, LP):
            smax = self.S_V1[tau]
            sp = {}
            cont = Counter()
            for t, s in self.sem_poda[tau]:
                if s > smax:
                    continue
                cont[s] += 1
                sp.setdefault(tuple(self.den(t)), s)
            dp = contar_termos(E0D, tau, {"g": GRADE}, smax)
            self.assertEqual({s: cont.get(s, 0) for s in dp}, dp)
            en = Enumerador(E0D, {"g": GRADE}, tau, ambientes_amostra=GR3, auditoria=True,
                            permitir_fora_particao=True)
            cp = {}
            for t, s in en.enumerar(smax):
                cp.setdefault(tuple(self.den(t)), s)
            self.assertEqual(set(cp), set(sp), f"{tau}: classes perdidas ou espúrias")
            self.assertEqual(cp, sp, f"{tau}: tamanho mínimo diferente")

    def test_V2_amostra_de_producao_nao_perde_classe_OE(self):
        for tau in (BOOL, LP):
            smax = self.S_V2[tau]
            en = Enumerador(E0D, {"g": GRADE}, tau)
            reps = {}
            for t, s in en.enumerar(smax):
                sg = en.assinatura_alvo(t)
                self.assertNotIn(sg, reps, "dois representantes na mesma classe")
                reps[sg] = s
            for t, s in self.sem_poda[tau]:
                if s > smax:
                    continue
                sg = en.assinatura_alvo(t)
                self.assertIn(sg, reps, imprimir(t))
                self.assertLessEqual(reps[sg], s, imprimir(t))

    def test_limitacao_particao(self):
        """Desvio documentado: nenhuma amostra só de oraculo_treino (n ≤ 4) separa estes termos,
        que diferem em #../.../... ; por isso V1 usa mundos de auditoria e V2 compara em OE."""
        a = parse("(algum@P (celula g) (cauda@P (posicoes g)))", livres=["g"])
        b = parse("(nao (vazia?@P (pretas g)))", livres=["g"])
        for n in (2, 3, 4):
            for g in G.grades_da_particao(n, "oraculo_treino"):
                self.assertEqual(avaliar(a, {"g": g}, n), avaliar(b, {"g": g}, n))
        g = Grade.de_texto("#../.../...")
        self.assertNotEqual(avaliar(a, {"g": g}, 3), avaliar(b, {"g": g}, 3))
        self.assertNotEqual(G.particao_de(g), "oraculo_treino")


class TestEnumerador(unittest.TestCase):
    def test_ordem_tipos_e_unicidade(self):
        en = Enumerador(E0D, {"g": GRADE}, LP)
        vistos = set()
        ult = 0
        for t, s in en.enumerar(5):
            self.assertGreaterEqual(s, ult); ult = s
            self.assertEqual(tamanho(t), s)
            self.assertEqual(tipo_de(t, {"g": GRADE}, E0D), LP)
            sg = en.assinatura_alvo(t)
            self.assertNotIn(sg, vistos)
            vistos.add(sg)
        self.assertEqual(en.cont.classes_alvo, len(vistos))

    def test_deduplicacao_em_dois_estagios_e_exata(self):
        a = [t for t, _ in Enumerador(E0D, {"g": GRADE}, BOOL).enumerar(6)]
        velho = EN.M_RAPIDA
        try:
            EN.M_RAPIDA = 10 ** 9          # chave rápida = assinatura completa
            b = [t for t, _ in Enumerador(E0D, {"g": GRADE}, BOOL).enumerar(6)]
        finally:
            EN.M_RAPIDA = velho
        self.assertEqual(a, b)

    def test_determinismo(self):
        r = []
        for _ in range(2):
            en = Enumerador(E0D, {}, FUN(GRADE, BOOL))
            r.append(([t for t, _ in en.enumerar(6)], en.cont.como_dict(), en.memoria_logica()))
        self.assertEqual(r[0], r[1])

    def test_mundos_so_de_oraculo_treino(self):
        for g in grades_amostra_oe():
            self.assertTrue(G.na_particao(g, "oraculo_treino"))
        fora = next(g for g in GR3 if not G.na_particao(g, "oraculo_treino"))
        with self.assertRaises(ValueError):
            Enumerador(E0D, {"g": GRADE}, BOOL, ambientes_amostra=[fora])
        with self.assertRaises(ErroProveniencia):
            Enumerador(E0D, {"g": GRADE}, BOOL, ambientes_amostra=[fora], permitir_fora_particao=True)

    def test_proveniencia(self):
        with self.assertRaises(ErroProveniencia):
            Enumerador(E0, {"g": GRADE}, BOOL)                       # base: use para_aprendiz()
        ref = PR.tabela_referencia("E0")
        with self.assertRaises(ErroProveniencia):
            Enumerador(ref, {"g": GRADE}, BOOL)                      # manual-teste: nunca em descoberta
        with self.assertRaises(ErroProveniencia):
            EstadoBusca(ref, FUN(GRADE, BOOL))
        en = Enumerador(ref, {"g": GRADE}, BOOL, auditoria=True)     # auditoria explícita
        self.assertEqual(en.proveniencia, "auditoria:referencia")
        with self.assertRaises(ErroProveniencia):
            registrar_reutilizacoes(PR.termo(PR.POR_NOME["ParAdjacente"]), ref, "teste")

    def test_biblioteca_descoberta_e_reutilizacao(self):
        """Uma abstração descoberta pelo laço do aprendiz (L-lib+f promove a solução de pretasDe, achada
        por buscar) entra como constante de tamanho 1, absorve a classe do seu corpo e registra
        reutilização. Uma entrada 'descoberta' sem certificado não entra na tabela."""
        from fedro_piloto import aprendizes as A
        from fedro_piloto.razao import LivroRazao
        tb0 = E0.para_aprendiz("E0/aprendiz-teste")
        corpo = parse(r"(\ (g Grade) (filtrar@P (celula g)))")
        with self.assertRaises(ErroProveniencia):
            tb0.adicionar(entrada_biblioteca("forjada", corpo, "descoberta", E0))
        amb = A.Ambiente(10_001, k_reservatorio=5, ns_reservatorio=(5,), num_teste=4)
        lib = A.LLib(E0, LivroRazao(10_001), promover_funcoes=True, B=5000, K=4,
                     kw_enumerador={"semente": 10_001})
        self.assertTrue(lib.resolver(A.TAREFAS_POR_ID["pretasDe"], amb).aceita)
        tb = lib.tabela_corrente()
        nome = tb.biblioteca()[0].nome
        p = tb[nome]
        en = Enumerador(tb, {}, FUN(GRADE, LP, LP))
        out = list(en.enumerar(4))
        self.assertIn((C(nome), 1), out)
        sg = en.assinatura_alvo(C(nome))
        self.assertFalse([t for t, s in out if s > 1 and en.assinatura_alvo(t) == sg])
        self.assertEqual(registrar_reutilizacoes(AP(AP(C(nome), V("g")), AP(C("pretas"), V("g"))), tb,
                                                 "tarefa-x"), [nome])
        self.assertEqual(p.categoria(), "descoberta-reutilizada")

    def test_fix_valores_conferem_com_avaliar(self):
        en = Enumerador(E0D, {}, FUN(LP, LP), profundidade_lambda=1)
        fixes = [t for t, _ in en.enumerar(7) if t[0] == "fix"]
        self.assertTrue(fixes)
        # fix (λrec x0. rec x0) ≡ λx0. vazio@P (padrão): mesmo representante, o menor
        t = parse(r"(fix (\ (rec (-> LP LP)) (x0 LP) (rec x0)))")
        self.assertEqual(en.assinatura_alvo(t), en.assinatura_alvo(parse(r"(\ (x0 LP) vazio@P)")))
        g = Grade.de_texto("##./.#./..#")
        for f in fixes:
            v = avaliar(f, {}, 3, tabela=E0D)
            for l in EN.amostras_oe(LP, g):
                self.assertEqual(v(l), aplicar(avaliar(f, {}, 3), l))

    def test_poda_inexata_desligada_e_superconjunto(self):
        a = Enumerador(E0D, {"g": GRADE}, BOOL)
        b = Enumerador(E0D, {"g": GRADE}, BOOL, poda_inexata=False)
        sa = {a.assinatura_alvo(t) for t, _ in a.enumerar(5)}
        sb = {a.assinatura_alvo(t) for t, _ in b.enumerar(5)}
        self.assertTrue(sa <= sb)
        self.assertGreaterEqual(b.cont.classes_distintas, a.cont.classes_distintas)


class TestAlcanceECusto(unittest.TestCase):
    def test_medir_alcance(self):
        r = medir_alcance(E0, {"g": GRADE}, BOOL, orcamentos=(100, 1000))
        self.assertLessEqual(r["s_reach"][100], r["s_reach"][1000])
        hist = {h["s"]: h for h in r["por_tamanho"]}
        for B, s in r["s_reach"].items():
            self.assertLessEqual(hist[s]["candidatos_avaliados"], B)
            if s + 1 in hist:
                self.assertGreater(hist[s + 1]["candidatos_avaliados"], B)
        self.assertTrue(r["esgotado"])
        # contadores determinísticos e medição real em estruturas separadas
        self.assertNotIn("tempo_parede_s", r["contadores"])
        self.assertIn("tempo_parede_s", r["medicao"])
        self.assertIn("bytes_estimados", r["memoria_logica"])
        r2 = medir_alcance(E0, {"g": GRADE}, BOOL, orcamentos=(100, 1000))
        self.assertEqual((r["s_reach"], r["contadores"], r["por_tamanho"]),
                         (r2["s_reach"], r2["contadores"], r2["por_tamanho"]))

    def test_contadores_sem_tempo(self):
        for campo in ContadorEnumeracao().como_dict():
            self.assertNotIn("tempo", campo)
            self.assertNotIn("memoria", campo)
        for campo in ContadorBusca().como_dict():
            self.assertNotIn("tempo", campo)


class TestBusca(unittest.TestCase):
    TIPO = FUN(GRADE, BOOL)

    @classmethod
    def setUpClass(cls):
        cls.gs = G.grades_da_particao(3, "oraculo_treino")

    def test_existe_preta(self):
        c = REGISTRO["ExistePreta"]
        ex = [((g,), c.rotulo(g)) for g in self.gs[:3]]
        cont = ContadorBusca()
        h, est = buscar(E0D, self.TIPO, ex, 10 ** 4, cont)
        self.assertIsNotNone(h)
        self.assertEqual(tamanho(h), 5)
        for (g,), y in ex:
            self.assertEqual(avaliar(h, {}, 3)(g), y)
        self.assertEqual(cont.custo, cont.candidatos_avaliados + cont.passos_avaliacao)
        self.assertGreater(cont.enumeracao_candidatos_avaliados, 0)

    def _laco(self, nome, orcamento=10 ** 4, rodadas=10):
        c = REGISTRO[nome]
        ex = [((g,), c.rotulo(g)) for g in self.gs[:2]]
        cont = ContadorBusca()
        h, est = buscar(E0D, self.TIPO, ex, orcamento, cont)
        for _ in range(rodadas):
            self.assertIsNotNone(h)
            f = avaliar(h, {}, 3)
            ce = [g for g in self.gs if f(g) != c.rotulo(g)]
            if not ce:
                break
            ex = ex + [((ce[0],), c.rotulo(ce[0]))]
            h, est = buscar(E0D, self.TIPO, ex, orcamento, cont, est)
        return h, ex, cont, est

    def test_continuacao_incremental_igual_a_busca_do_zero(self):
        h, ex, cont, est = self._laco("TopoCheio")
        self.assertIsNotNone(h)
        cont0 = ContadorBusca()
        h0, _ = buscar(E0D, self.TIPO, ex, 10 ** 5, cont0)
        self.assertEqual(h, h0)
        # incremental: cada candidato rejeitado é avaliado uma vez; só as hipóteses são reavaliadas
        self.assertLessEqual(cont.candidatos_avaliados, cont0.candidatos_avaliados + len(est.historico))
        for (g,), y in ex:
            self.assertEqual(avaliar(h, {}, 3)(g), y)

    def test_orcamento_esgotado_e_retomada(self):
        c = REGISTRO["TopoCheio"]
        positiva = next(g for g in self.gs if c.rotulo(g))
        ex = [((g,), c.rotulo(g)) for g in [positiva] + self.gs[:5]]
        cont = ContadorBusca()
        h, est = buscar(E0D, self.TIPO, ex, 3, cont)
        self.assertIsNone(h)
        self.assertEqual(cont.candidatos_avaliados, 3)
        h, est = buscar(E0D, self.TIPO, ex, 10 ** 5, cont, est)
        h0, _ = buscar(E0D, self.TIPO, ex, 10 ** 5, ContadorBusca())
        self.assertEqual(h, h0)

    def test_exemplos_so_crescem(self):
        c = REGISTRO["ExistePreta"]
        ex = [((g,), c.rotulo(g)) for g in self.gs[:3]]
        cont = ContadorBusca()
        _, est = buscar(E0D, self.TIPO, ex, 10 ** 4, cont)
        with self.assertRaises(ValueError):
            buscar(E0D, self.TIPO, ex[1:], 10 ** 4, cont, est)


if __name__ == "__main__":
    unittest.main()
