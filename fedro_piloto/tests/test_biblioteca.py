"""U21–U22 (documento 03, seção 5) e barreiras de proveniência da biblioteca.

U21/U22 testam o MECANISMO de extração a partir de soluções MANUAIS (proveniencia "manual-teste",
modo "mecanismo-teste"). Nada aqui é descoberta autônoma; as entradas criadas a partir dessas
soluções são "manual-teste" e ficam numa Tabela de uso "referencia".
"""
import random
import unittest

from fedro_piloto import programas_referencia as PR
from fedro_piloto.avaliador import avaliar
from fedro_piloto.biblioteca import (Biblioteca, ContadorCompressao, Solucao, canonizar, extrair_fragmentos,
                                     reescrever)
from fedro_piloto.dsl import (E0, E0P, FUN, GRADE, LP, POS, BOOL, ErroProveniencia, entrada_biblioteca, parse,
                              tamanho, constantes)
from fedro_piloto.grade import Grade, todas_as_grades
from fedro_piloto.referencias import REGISTRO
from fedro_piloto.tradutores import comparar_denotacoes, inline

SEMENTE = 10_121  # intervalo do piloto

LIB_E0 = PR.biblioteca_manual("E0", ate="mesmoNumero")

#: soluções manuais das duas tarefas "no máximo" (escada F3: noMaximo aplicado a pretasDe de regiões)
NOMAX_LINHAS = ("(\\ (g Grade) (noMaximo (pretasDe g (cabeca@LP (linhas g)))"
                " (pretasDe g (cabeca@LP (reverter@LP (linhas g))))))")
NOMAX_COLUNAS = ("(\\ (g Grade) (noMaximo (pretasDe g (cabeca@LP (colunas g)))"
                 " (pretasDe g (cabeca@LP (reverter@LP (colunas g))))))")


def _bruto(termo):
    """Solução manual com a biblioteca manual inlined (o mecanismo não pode ver vizPretos etc.)."""
    t = inline(termo, LIB_E0)
    assert not set(constantes(t)) & set(LIB_E0), "inlining incompleto"
    return t


def _grades_ate_3():
    return [g for n in (1, 2, 3) for g in todas_as_grades(n)]


def _grades_aleatorias(ns=(4, 5, 6), por_n=30):
    rng = random.Random(SEMENTE)
    out = []
    for n in ns:
        for _ in range(por_n):
            p = rng.choice([0.2, 0.35, 0.5, 0.65])
            out.append(Grade(n, tuple(1 if rng.random() < p else 0 for _ in range(n * n))))
    return out


def _grades_listas():
    """Para funções sobre listas (a grade só entra pela bateria): n ≤ 2 inteiro, fração fixa de n = 3."""
    return [g for g in _grades_ate_3() if g.n <= 2 or g.balde(16) == 0]


def _solucoes_u21():
    return [Solucao(_bruto(PR.termo(PR.POR_NOME[n])), n, "manual-teste") for n in ("ParAdjacente", "NenhumaIsolada")]


def _solucoes_u22():
    return [Solucao(_bruto(parse(NOMAX_LINHAS)), "NoMax_linha1_linhaN", "manual-teste"),
            Solucao(_bruto(parse(NOMAX_COLUNAS)), "NoMax_col1_colN", "manual-teste")]


class TestU21VizPretos(unittest.TestCase):
    def test_u21_fragmento_igual_a_vizPretos(self):
        sols = _solucoes_u21()
        frags = extrair_fragmentos(sols)
        alvo = PR.termo(PR.POR_NOME["vizPretos"])
        tipo = FUN(GRADE, POS, LP)
        cands = [f for f in frags if f.tipo == tipo]
        self.assertTrue(cands, "nenhum fragmento do tipo de vizPretos")
        grades = _grades_ate_3() + _grades_aleatorias()
        iguais = [f for f in cands if not comparar_denotacoes(f.termo_fechado, alvo, tipo, grades)]
        self.assertTrue(iguais, [f.legivel() for f in cands])
        f = iguais[0]
        self.assertEqual(f.ocorrencias, 2)
        self.assertEqual(set(f.origem_ids), {"ParAdjacente", "NenhumaIsolada"})
        self.assertEqual(f.proveniencias_origem, frozenset({"manual-teste"}))
        self.assertEqual(f.tamanho, 8)
        self.assertEqual(f.pontuacao, (2 - 1) * (8 - 1))

    def test_u21_ranking_registrado(self):
        """Registro (não aceitação): o fragmento de maior pontuação não é vizPretos (ver relatório)."""
        frags = extrair_fragmentos(_solucoes_u21())
        self.assertGreater(frags[0].pontuacao, 7)
        self.assertEqual(frags[0].tipo, FUN(FUN(FUN(POS, BOOL), LP, BOOL), GRADE, BOOL))

    def test_mecanismo_teste_comprimir(self):
        bib = Biblioteca(E0, "mecanismo-teste")
        originais = {s.tarefa_id: s.termo for s in _solucoes_u21()}
        novas = bib.comprimir(_solucoes_u21(), limiar=7)
        self.assertTrue(novas)
        self.assertEqual(bib.tabela.uso, "referencia")
        for p in novas:
            self.assertEqual(p.proveniencia, "manual-teste")
            self.assertEqual(p.categoria(), "manual-teste")
        with self.assertRaises(ErroProveniencia):
            bib.tabela.para_aprendiz()  # tabela com entradas manuais nunca vira tabela de aprendiz
        # reescrita: tamanho menor e mesma denotação em todas as grades n ≤ 3
        for s in bib.solucoes:
            orig = originais[s.tarefa_id]
            self.assertLess(tamanho(s.termo), tamanho(orig))
            for n in (1, 2, 3):
                v1 = avaliar(orig, n=n)
                v2 = avaliar(s.termo, n=n, tabela=bib.tabela)
                for g in todas_as_grades(n):
                    self.assertEqual(v1(g), v2(g))
        self.assertGreater(bib.ultimo_custo.subtermos_examinados, 0)
        c = bib.contador
        self.assertEqual(c.subtermos_examinados, c.nos_enumerados + c.nos_antiunificacao + c.nos_casamento)

    def test_reuso_registrado(self):
        bib = Biblioteca(E0, "mecanismo-teste")
        bib.comprimir(_solucoes_u21(), limiar=7)
        nome = next(iter(bib.entradas))
        reg = bib.entradas[nome]
        self.assertEqual(reg.usos_na_origem, 2)
        # solução posterior (outra tarefa) que usa a entrada: reutilização
        p = bib.entradas[nome].primitiva
        self.assertEqual(p.tipo, FUN(FUN(FUN(POS, BOOL), LP, BOOL), GRADE, BOOL))  # ver test_u21_ranking
        posterior = parse(f"(\\ (g Grade) (nao ({nome} todos@P g)))")
        usos = bib.registrar_reuso(posterior, "AlgumaIsolada")
        self.assertEqual(usos, {nome: 1})
        bib.registrar_reuso(posterior, "ParAdjacente")  # tarefa de origem: não é reutilização
        rel = bib.relatorio()
        e = next(x for x in rel["entradas"] if x["nome"] == nome)
        self.assertEqual(e["reutilizacoes"], {"AlgumaIsolada": 1})
        self.assertEqual(e["usos_em_origem_posteriores"], {"ParAdjacente": 1})
        self.assertEqual(e["tarefas_origem"], ["ParAdjacente", "NenhumaIsolada"])
        self.assertEqual(e["categoria"], "manual-teste")  # manual nunca vira "descoberta-reutilizada"
        self.assertEqual(p.reutilizacoes, [])


class TestU22NoMaximo(unittest.TestCase):
    def test_solucoes_manuais_corretas(self):
        tab = PR.tabela_referencia("E0")
        for s, nome in zip(_solucoes_u22(), ("NoMax_linha1_linhaN", "NoMax_col1_colN")):
            for n in (1, 2, 3):
                v = avaliar(s.termo, n=n, tabela=tab)
                for g in todas_as_grades(n):
                    self.assertEqual(v(g), REGISTRO[nome].rotulo(g), (nome, g.serializar()))

    def test_u22_fragmento_igual_a_descartar(self):
        frags = extrair_fragmentos(_solucoes_u22())
        alvo = PR.termo(PR.POR_NOME["descartar"])
        tipo = FUN(LP, LP, LP)
        cands = [f for f in frags if f.tipo == tipo]
        iguais = [f for f in cands if not comparar_denotacoes(f.termo_fechado, alvo, tipo, _grades_listas())]
        self.assertTrue(iguais, [f.legivel() for f in cands])
        f = iguais[0]
        self.assertEqual(f.num_parametros, 0)        # subtermo fechado recorrente
        self.assertEqual(f.tamanho, 13)
        self.assertEqual(f.pontuacao, 12)
        self.assertEqual(canonizar(f.termo_fechado), canonizar(alvo))  # α-igual ao manual

    def test_u22_pretasDe_eta(self):
        """PH8 também pede pretasDe: o fragmento λg. filtrar@P (celula g) é η-igual a ele."""
        frags = extrair_fragmentos(_solucoes_u22())
        alvo = PR.termo(PR.POR_NOME["pretasDe"])
        tipo = FUN(GRADE, LP, LP)
        cands = [f for f in frags if f.tipo == tipo]
        iguais = [f for f in cands if not comparar_denotacoes(f.termo_fechado, alvo, tipo, _grades_listas())]
        self.assertTrue(iguais, [f.legivel() for f in cands])

    def test_antiunificacao_um_buraco(self):
        """O par (linhas, colunas) vira um único buraco reaproveitado nas duas posições."""
        frags = extrair_fragmentos(_solucoes_u22(), max_buracos=1)
        topo = frags[0]
        self.assertEqual(topo.metodo, "antiunificacao")
        self.assertEqual(topo.num_buracos, 1)
        self.assertEqual(topo.ocorrencias, 2)
        sem = extrair_fragmentos(_solucoes_u22(), max_buracos=0)
        self.assertTrue(all(f.num_buracos == 0 for f in sem))


class TestPH8EscadaCompleta(unittest.TestCase):
    """Registro para PM11/PH8 (não é U21/U22): compressão gulosa (limiar 6) de TODA a escada manual,
    inlined, em modo mecanismo-teste. Entradas comparadas, a menos da ordem dos argumentos, com os
    degraus manuais. vizPretos NÃO aparece como entrada (ver relatório do módulo)."""

    @classmethod
    def setUpClass(cls):
        lib = PR.biblioteca_manual("E0")
        cls.bib = Biblioteca(E0, "mecanismo-teste")
        cls.bib.comprimir([Solucao(inline(PR.termo(p), lib), p.nome, "manual-teste") for p in PR.ESCADA], limiar=6)
        cls.ref = PR.tabela_referencia("E0")

    def _existe(self, texto_ref, tipo):
        alvo = parse(texto_ref)
        for nome, reg in self.bib.entradas.items():
            if reg.primitiva.tipo == tipo and not comparar_denotacoes(
                    ("c", nome), alvo, tipo, _grades_listas(), self.bib.tabela, self.ref):
                return nome
        return None

    def test_noMaximo_passo_pretasDe(self):
        self.assertIsNotNone(self._existe("(\\ (B LP) (A LP) (noMaximo A B))", FUN(LP, LP, BOOL)))
        self.assertIsNotNone(self._existe("(\\ (S LP) (g Grade) (passo g S))", FUN(LP, GRADE, LP)))
        self.assertIsNotNone(self._existe("(\\ (g Grade) (r LP) (pretasDe g r))", FUN(GRADE, LP, LP)))
        for reg in self.bib.entradas.values():
            self.assertEqual(reg.primitiva.proveniencia, "manual-teste")


class TestExtracaoPropriedades(unittest.TestCase):
    def test_determinismo_e_alfa(self):
        sols = _solucoes_u21()
        c1, c2 = ContadorCompressao(), ContadorCompressao()
        a = extrair_fragmentos(sols, contador=c1)
        b = extrair_fragmentos(sols, contador=c2)
        self.assertEqual(a, b)
        self.assertEqual(c1.como_dict(), c2.como_dict())
        # renomear variáveis ligadas não muda os fragmentos
        ren = [parse("(\\ (h Grade) (algum@P (\\ (q Pos) (nao (vazia?@P (filtrar@P (celula h) (vizinhos h q)))))"
                     " (pretas h)))"),
               parse("(\\ (k Grade) (todos@P (\\ (r Pos) (nao (vazia?@P (filtrar@P (celula k) (vizinhos k r)))))"
                     " (pretas k)))")]
        c = extrair_fragmentos(ren)
        self.assertEqual([f.termo_fechado for f in a], [f.termo_fechado for f in c])

    def test_reescrever_preserva_denotacao(self):
        sols = _solucoes_u22()
        f = extrair_fragmentos(sols)[0]
        prim = entrada_biblioteca("frag", f.termo_fechado, "manual-teste", E0)
        tab = E0.para_referencia([prim])
        for s in sols:
            t2, k = reescrever(s.termo, "frag", f.termo_fechado, f.num_parametros, tab)
            self.assertEqual(k, 1)
            self.assertLess(tamanho(t2), tamanho(s.termo))
            for n in (1, 2, 3):
                v1, v2 = avaliar(s.termo, n=n), avaliar(t2, n=n, tabela=tab)
                for g in todas_as_grades(n):
                    self.assertEqual(v1(g), v2(g))

    def test_minimos(self):
        frags = extrair_fragmentos(_solucoes_u21(), min_ocorrencias=3)
        self.assertEqual(frags, [])
        for f in extrair_fragmentos(_solucoes_u22()):
            self.assertGreaterEqual(f.ocorrencias, 2)
            self.assertEqual(f.pontuacao, (f.ocorrencias - 1) * (f.tamanho - 1))
            self.assertGreaterEqual(tamanho(f.corpo), 3)


class TestModoAutonomo(unittest.TestCase):
    def test_tabela_de_descoberta(self):
        bib = Biblioteca(E0, "autonomo")
        self.assertEqual(bib.tabela.uso, "descoberta")
        self.assertEqual(bib.comprimir([], limiar=1), [])

    def test_rejeita_adicionar_manual(self):
        bib = Biblioteca(E0, "autonomo")
        f = extrair_fragmentos(_solucoes_u21())[0]
        with self.assertRaises(ErroProveniencia):
            bib.adicionar(f, "manual-teste")
        # nem rotulando como descoberta: as origens do fragmento são manuais
        with self.assertRaises(ErroProveniencia):
            bib.adicionar(f, "descoberta")
        f_sem_rotulo = extrair_fragmentos([s.termo for s in _solucoes_u21()])[0]
        with self.assertRaises(ErroProveniencia):
            bib.adicionar(f_sem_rotulo, "descoberta")
        self.assertEqual(len(bib.entradas), 0)
        self.assertEqual(bib.tabela.biblioteca(), [])

    def test_rejeita_solucoes_manuais_ou_sem_marca(self):
        bib = Biblioteca(E0, "autonomo")
        with self.assertRaises(ErroProveniencia):
            bib.comprimir(_solucoes_u21(), limiar=1)
        with self.assertRaises(ErroProveniencia):
            bib.comprimir([s.termo for s in _solucoes_u21()], limiar=1)
        self.assertEqual(bib.solucoes, [])

    def test_segunda_barreira_tabela(self):
        bib = Biblioteca(E0, "autonomo")
        prim = entrada_biblioteca("x", parse("(\\ (g Grade) (pretas g))"), "manual-teste", E0)
        with self.assertRaises(ErroProveniencia):
            bib.tabela.adicionar(prim)

    def test_base_com_manuais_proibida(self):
        with self.assertRaises(ErroProveniencia):
            Biblioteca(PR.tabela_referencia("E0"), "autonomo")

    def test_mecanismo_teste_nunca_descoberta(self):
        bib = Biblioteca(E0P, "mecanismo-teste")
        f = extrair_fragmentos(_solucoes_u22())[0]
        with self.assertRaises(ErroProveniencia):
            bib.adicionar(f, "descoberta")

    def test_modo_invalido(self):
        with self.assertRaises(ValueError):
            Biblioteca(E0, "misto")


if __name__ == "__main__":
    unittest.main()
