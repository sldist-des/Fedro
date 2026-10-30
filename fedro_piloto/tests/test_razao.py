"""U25 (documento 03, seção 5): execução seca com três tarefas; total = soma das partes; candidatos
iguais entre E0 e E0'; mesma semente ⇒ contadores idênticos (medições podem diferir).

A "busca" da execução seca é uma lista FIXA de candidatos por tarefa (sem enumerador), avaliada em
E0 e na sua tradução para E0' (β-segura ∘ τ). Os programas corretos da lista são manuais
(proveniencia "manual-teste"): a compressão roda em modo "mecanismo-teste", nunca "autonomo".
O "oráculo" é uma busca exaustiva em n ≤ 3 na ordem de minimalidade (n, pretas, lexicográfica).
"""
import json
import os
import tempfile
import unittest

from fedro_piloto import programas_referencia as PR
from fedro_piloto.avaliador import Contador, avaliar
from fedro_piloto.biblioteca import Biblioteca, Solucao
from fedro_piloto.dsl import BASES, parse
from fedro_piloto.geradores import ContadorGeracao, amostra_natural, rng_piloto
from fedro_piloto.grade import chave_minimalidade, todas_as_grades
from fedro_piloto.razao import CAMPOS, CAMPOS_AMBIENTE, CAMPOS_APRENDIZ, LivroRazao
from fedro_piloto.referencias import REGISTRO
from fedro_piloto.tradutores import beta_segura, inline, tau

SEMENTE = 10_025
LIB = PR.biblioteca_manual("E0", ate="passo")
ERRADOS = ["(\\ (g Grade) falso)", "(\\ (g Grade) verdadeiro)", "(\\ (g Grade) (vazia?@P (pretas g)))",
           "(\\ (g Grade) (nao (vazia?@P (posicoes g))))"]
TAREFAS = [("ExistePreta", PR.termo(PR.POR_NOME["ExistePreta"])),
           ("ParAdjacente", inline(PR.termo(PR.POR_NOME["ParAdjacente"]), LIB)),
           ("NenhumaIsolada", inline(PR.termo(PR.NENHUMA_ISOLADA_CORRIGIDA), LIB))]
DOMINIO_ORACULO = sorted((g for n in (1, 2, 3) for g in todas_as_grades(n)), key=chave_minimalidade)


def _na_base(t, base):
    return t if base == "E0" else beta_segura(tau(t))


def _avaliar_em(t, grades, contador):
    vals = {}
    for g in grades:
        if g.n not in vals:
            vals[g.n] = avaliar(t, n=g.n, contador=contador)
    return [vals[g.n](g) for g in grades]


def execucao_seca(semente: int, bases=("E0", "E0p")) -> LivroRazao:
    livro = LivroRazao(semente, {"tipo": "execucao-seca U25", "bases": list(bases)})
    for base in bases:
        aprendiz = f"seco@{base}"
        bib = Biblioteca(BASES[base], "mecanismo-teste")
        rng = rng_piloto(semente)  # mesma semente por base: mesmos exemplos nas duas bases
        for tarefa, correto in TAREFAS:
            conceito = REGISTRO[tarefa]
            with livro.medir(tarefa, aprendiz):
                cg = ContadorGeracao()
                exemplos = [amostra_natural(3, rng, contador=cg) for _ in range(4)]
                livro.registrar(tarefa, aprendiz, "geracao_grades", cg.grades_geradas, "treino")
                rotulos = [conceito.rotulo(g) for g in exemplos]
                aceito = None
                for texto in ERRADOS + [None]:
                    cand = _na_base(parse(texto) if texto else correto, base)
                    c = Contador()
                    saidas = _avaliar_em(cand, exemplos, c)
                    livro.registrar_candidato(tarefa, aprendiz, c.passos, base)
                    if saidas != rotulos:
                        continue
                    # consulta ao oráculo: menor contraexemplo em n ≤ 3
                    livro.registrar(tarefa, aprendiz, "oraculo_consultas", 1)
                    co = Contador()
                    examinadas = 0
                    contra = None
                    vals = {}
                    for g in DOMINIO_ORACULO:
                        examinadas += 1
                        if g.n not in vals:
                            vals[g.n] = avaliar(cand, n=g.n, contador=co)
                        if vals[g.n](g) != conceito.rotulo(g):
                            contra = g
                            break
                    # mesma definição da produção: grades examinadas e passos de h em campos separados
                    livro.registrar(tarefa, aprendiz, "oraculo_custo_ambiente", examinadas)
                    livro.registrar(tarefa, aprendiz, "oraculo_passos_hipotese", co.passos)
                    if contra is None:
                        aceito = cand
                        break
                    exemplos.append(contra)
                    rotulos.append(conceito.rotulo(contra))
                assert aceito is not None
                # avaliação em teste (grades naturais n = 4, geradas com a mesma semente)
                cg = ContadorGeracao()
                teste = [amostra_natural(4, rng, contador=cg) for _ in range(10)]
                livro.registrar(tarefa, aprendiz, "geracao_grades", cg.grades_geradas, "teste")
                ca = Contador()
                _avaliar_em(aceito, teste, ca)
                livro.registrar(tarefa, aprendiz, "avaliacao_passos", ca.passos)
                # compressão (mecanismo-teste: soluções manuais)
                bib.comprimir([Solucao(aceito, tarefa, "manual-teste")], limiar=5)
                livro.registrar(tarefa, aprendiz, "compressao_subtermos", bib.ultimo_custo.subtermos_examinados)
    return livro


class TestU25LivroRazao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.l1 = execucao_seca(SEMENTE)
        cls.l2 = execucao_seca(SEMENTE)

    def test_fechamento(self):
        r = self.l1.verificar_fechamento()
        self.assertTrue(r.ok, r.problemas)
        self.assertEqual(r.diferenca, 0)
        self.assertEqual(self.l1.total(), sum(self.l1.total_por_campo().values()))
        for e in self.l1.entradas():
            self.assertEqual(e.total(), sum(e.campos().values()))
            self.assertEqual(e.total(), e.total_aprendiz() + e.total_ambiente() + e.total_avaliacao())
        self.assertEqual(len(self.l1.entradas()), 6)

    def test_candidatos_iguais_entre_E0_e_E0p(self):
        for tarefa, _ in TAREFAS:
            a = self.l1.entrada(tarefa, "seco@E0")
            b = self.l1.entrada(tarefa, "seco@E0p")
            self.assertGreater(a.busca_candidatos, 0)
            self.assertEqual(a.busca_candidatos, b.busca_candidatos, tarefa)
            self.assertEqual(a.oraculo_consultas, b.oraculo_consultas, tarefa)
            self.assertEqual(a.geracao_grades, b.geracao_grades, tarefa)
        # passos diferem entre bases (mesma denotação, custo de avaliação distinto)
        self.assertTrue(any(self.l1.entrada(t, "seco@E0").busca_passos != self.l1.entrada(t, "seco@E0p").busca_passos
                            for t, _ in TAREFAS))

    def test_determinismo_mesma_semente(self):
        self.assertEqual(self.l1.comparar_deterministico(self.l2), [])
        self.assertEqual(self.l1.serializar_deterministico(), self.l2.serializar_deterministico())
        # medições existem, ficam fora da comparação e podem diferir
        self.assertTrue(self.l1.medicoes)
        k = next(iter(self.l2.medicoes))
        self.l2.medicoes[k].tempo_parede_s += 123.0
        self.assertEqual(self.l1.comparar_deterministico(self.l2), [])
        for m in self.l1.medicoes.values():
            self.assertGreater(m.tempo_parede_s, 0.0)
            self.assertGreater(m.memoria_pico_kb, 0)

    def test_diferenca_detectada(self):
        l3 = execucao_seca(SEMENTE, bases=("E0",))
        self.assertNotEqual(self.l1.comparar_deterministico(l3), [])
        l4 = execucao_seca(SEMENTE + 1, bases=("E0", "E0p"))
        self.assertNotEqual(self.l1.comparar_deterministico(l4), [])

    def test_serializacao_json(self):
        with tempfile.TemporaryDirectory() as d:
            caminho = os.path.join(d, "razao.json")
            txt = self.l1.serializar_json(caminho)
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
            self.assertEqual(set(dados), {"deterministico", "medicoes"})
            for e in dados["deterministico"]["entradas"]:
                self.assertNotIn("tempo_parede_s", e)
                self.assertNotIn("memoria_pico_kb", e)
            self.assertEqual(dados["deterministico"]["total"], self.l1.total())
            l5 = LivroRazao.carregar_json(caminho)
            self.assertEqual(self.l1.comparar_deterministico(l5), [])
            self.assertTrue(l5.verificar_fechamento().ok)
            self.assertEqual(l5.serializar_json(), txt)

    def test_nao_mistura_medicoes(self):
        l = LivroRazao(SEMENTE)
        with self.assertRaises(TypeError):
            l.registrar("t", "a", "busca_passos", 0.5)
        with self.assertRaises(TypeError):
            l.registrar("t", "a", "busca_passos", True)
        with self.assertRaises(KeyError):
            l.registrar("t", "a", "tempo_parede_s", 1)
        with self.assertRaises(ValueError):
            l.registrar("t", "a", "busca_passos", -1)
        self.assertEqual(set(CAMPOS), set(CAMPOS_APRENDIZ) | set(CAMPOS_AMBIENTE) | {"avaliacao_passos"})

    def test_adulteracao_quebra_fechamento(self):
        l = LivroRazao(SEMENTE)
        l.registrar_varios("t", "a", busca_candidatos=3, busca_passos=40)
        self.assertTrue(l.verificar_fechamento().ok)
        l.entrada("t", "a").busca_passos += 1   # escrita fora do diário
        r = l.verificar_fechamento()
        self.assertFalse(r.ok)
        self.assertTrue(any("busca_passos" in p for p in r.problemas))


if __name__ == "__main__":
    unittest.main()
