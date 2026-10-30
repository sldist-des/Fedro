"""Testes da interface de tarefas externas (benchmark/protocolo-avaliacao.md): validador autónomo do
kit, congelamento por hash, carregamento e registo de tarefas externas, execução com orçamento
mínimo, métricas (sem razões exatas quando um braço não aceita), verificação pós-execução com os
ficheiros selados e a auditoria de vazamento do contrato público."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from fedro_piloto import aprendizes as A
from fedro_piloto import benchmark_externo as BX
from fedro_piloto import verificacao as V
from fedro_piloto.experimento_minimo import ConfigEM

RAIZ = BX.RAIZ
EXEMPLO = os.path.join(RAIZ, "benchmark", "kit-autor", "exemplo-pacote")
VALIDADOR = os.path.join(RAIZ, "benchmark", "kit-autor", "validar_pacote.py")


def _copia(destino):
    shutil.copytree(EXEMPLO, destino)
    return destino


class TestValidadorKit(unittest.TestCase):
    def test_exemplo_valida_e_hash_coincide_com_manifesto(self):
        val = BX.validar_pacote(EXEMPLO)
        self.assertTrue(val["ok"], val["erros"])
        with open(os.path.join(EXEMPLO, "MANIFESTO.json"), encoding="utf-8") as f:
            man = json.load(f)
        self.assertEqual(val["estatisticas"]["hash_pacote"], man["hash_pacote"])
        self.assertEqual(val["estatisticas"]["num_tarefas"], 3)

    def test_validador_autonomo_corre_sem_o_pacote_fedro(self):
        r = subprocess.run([sys.executable, "-I", VALIDADOR, EXEMPLO], capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("erros: 0", r.stdout)

    def test_pacote_alterado_apos_congelamento_e_recusado(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _copia(os.path.join(tmp, "p"))
            with open(os.path.join(d, "tarefas.json"), "a", encoding="utf-8") as f:
                f.write("\n")
            with self.assertRaises(BX.ErroIntegridade):
                BX.carregar_pacote(d)
            os.remove(os.path.join(d, "MANIFESTO.json"))
            with self.assertRaises(BX.ErroIntegridade):
                BX.carregar_pacote(d)
            p = BX.carregar_pacote(d, exigir_congelado=False)
            self.assertEqual(len(p.tarefas), 3)

    def test_erros_de_formato_e_de_referencia(self):
        kit = BX._kit()
        with tempfile.TemporaryDirectory() as tmp:
            d = _copia(os.path.join(tmp, "p"))
            with open(os.path.join(d, "tarefas.json"), encoding="utf-8") as f:
                doc = json.load(f)
            doc["tarefas"][0]["tipo"] = "Grade -> Grade"                       # tipo não aceite
            with open(os.path.join(d, "tarefas.json"), "w", encoding="utf-8") as f:
                json.dump(doc, f)
            self.assertFalse(kit.validar(d).ok())
            d2 = _copia(os.path.join(tmp, "q"))
            with open(os.path.join(d2, "referencias.py"), "a", encoding="utf-8") as f:
                f.write("\nREFERENCIAS['ehCanto'] = lambda g, p: 1\n")          # saída não booleana
            rel = kit.validar(d2)
            self.assertFalse(rel.ok())
            self.assertTrue(any("ehCanto" in e for e in rel.erros))
            d3 = _copia(os.path.join(tmp, "r"))
            with open(os.path.join(d3, "referencias.py"), "a", encoding="utf-8") as f:
                f.write("\nREFERENCIAS['primeiraCelulaPreta'] = lambda g: True\nREFERENCIAS_B['primeiraCelulaPreta'] = lambda g: True\n")   # predicado degenerado
            rel = kit.validar(d3)
            self.assertTrue(any("degenerada" in e or "negativos" in e for e in rel.erros), rel.erros)
            d4 = _copia(os.path.join(tmp, "s"))
            with open(os.path.join(d4, "referencias.py"), "a", encoding="utf-8") as f:
                f.write("\nimport random\nREFERENCIAS['ehCanto'] = lambda g, p: random.random() < 0.5\n")
            rel = kit.validar(d4)
            self.assertTrue(any("determin" in e for e in rel.erros), rel.erros)


class TestCarregamento(unittest.TestCase):
    def test_tarefas_registadas_com_prefixo_e_sem_colisao(self):
        p = BX.carregar_pacote(EXEMPLO)
        ids = [t.id for t in p.tarefas]
        self.assertEqual(ids, ["bx:primeiraCelulaPreta", "bx:ehCanto", "bx:identidade"])
        self.assertIn("bx:primeiraCelulaPreta", A.REGISTRO if hasattr(A, "REGISTRO") else BX.REGISTRO)
        self.assertIn("bx:ehCanto", A.REFERENCIAS_FUNCAO)
        self.assertNotIn("ehCanto", A.REFERENCIAS_FUNCAO)        # o id do autor nunca entra sem prefixo
        self.assertIs(V.tarefa_por_id("bx:identidade"), BX.TAREFAS_EXTERNAS["bx:identidade"])
        g = A.Grade.de_texto("#../.#./...")
        self.assertEqual(A.saida_referencia(p.tarefas[1], (g, (1, 1))), True)
        self.assertEqual(A.saida_referencia(p.tarefas[2], (g, ((1, 1), (2, 2)))), frozenset({(1, 1), (2, 2)}))
        self.assertTrue(BX.REGISTRO["bx:primeiraCelulaPreta"].rotulo(g))

    def test_resumo_do_pacote_nao_expoe_referencias(self):
        p = BX.carregar_pacote(EXEMPLO)
        r = p.resumo()
        self.assertEqual(r["num_tarefas"], 3)
        self.assertNotIn("referencias", json.dumps(r))


class TestExecucaoMinima(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cfg = ConfigEM(semente=10_007, B=300, sondas=False, auditoria_oe_orcamento=0, memoria_trabalhador_gb=None)
        cls.r = BX.executar(EXEMPLO, cls.tmp, cfg, bracos=("L-fix", "L-lib+f", "L-lib+f/lesao"), politicas=("tamanho",),
                            modos=("zero",), processos=1)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_registro_e_metricas(self):
        d = self.r["deterministico"]
        self.assertEqual(d["pacote"]["hash"], BX.carregar_pacote(EXEMPLO).hash)
        for k, b in d["bracos"].items():
            self.assertIsNone(b.get("falha"), (k, b.get("traceback")))
            self.assertEqual([x["tarefa"] for x in b["curva"]], ["primeiraCelulaPreta", "ehCanto", "identidade"])
        m = d["metricas"]["por_braco"]["zero/tamanho/L-lib+f"]
        self.assertEqual(m["tarefas"], 3)
        self.assertTrue(m["livro_fecha"])
        self.assertEqual(m["custo_cumulativo"], d["bracos"]["zero/tamanho/L-lib+f"]["curva"][-1]["cumulativo"])
        comp = d["metricas"]["comparacoes"]["zero/tamanho/L-lib+f vs zero/tamanho/L-fix"]
        self.assertEqual(set(comp["por_tarefa"]), {"primeiraCelulaPreta", "ehCanto", "identidade"})
        for v in comp["por_tarefa"].values():
            if not (v["L-lib+f"]["aceita"] and v["L-fix"]["aceita"]):
                self.assertIsNone(v["razao_exata"])          # nunca razão exata sem as duas aceitações
        les = d["metricas"]["comparacoes"]["zero/tamanho/L-lib+f vs zero/tamanho/L-lib+f/lesao"]
        self.assertEqual(les["tarefas_apos_lesao"], 2)        # lesão antes da tarefa ⌊3/2⌋ = 1
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "relatorio.md")))

    def test_verificacao_pos_execucao_com_selados(self):
        v = BX.verificar_benchmark(self.tmp, ns_amostral=(5,), k=3, exaustivo=False)
        self.assertEqual(v["erros_previsao"]["amostral"], 0)
        self.assertEqual(v["erros_previsao"]["ocultos_autor"], 0)
        self.assertIn("primeiraCelulaPreta", v["testemunhas"])
        self.assertTrue(v["testemunhas"]["primeiraCelulaPreta"]["tipo_ok"])
        pares = [(h["braco"], h["tarefa"]) for h in v["hipoteses"]]
        self.assertEqual(len(pares), len(set(pares)))         # sem duplicados entre formatos de registro


class TestTransferenciaSemRazaoExata(unittest.TestCase):
    def test_classes(self):
        def braco(res):
            return {"resultados": {t: {"aceita": a, "custo": c, "tamanho": None, "biblioteca_usada": r} for t, (a, c, r) in res.items()},
                    "curva": []}
        lib = braco({"a": (True, 10, ["abs1"]), "b": (True, 50, []), "c": (False, 90, []), "d": (False, 90, [])})
        fix = braco({"a": (False, 100, []), "b": (True, 20, []), "c": (True, 30, []), "d": (False, 90, [])})
        tt = BX.transferencia_por_tarefa(lib, fix)
        self.assertIsNone(tt["a"]["razao_exata"]); self.assertAlmostEqual(tt["a"]["razao_minima"], 10.0)
        self.assertTrue(tt["a"]["classe"].startswith("positiva")); self.assertTrue(tt["a"]["reuso_verificavel"])
        self.assertEqual(tt["b"]["classe"], "negativa"); self.assertAlmostEqual(tt["b"]["razao_exata"], 0.4)
        self.assertTrue(tt["c"]["classe"].startswith("negativa")); self.assertIsNone(tt["c"]["razao_exata"])
        self.assertTrue(tt["d"]["classe"].startswith("inconclusiva"))


class TestAuditoriaVazamento(unittest.TestCase):
    def test_contrato_e_kit_sem_vazamento(self):
        sys.path.insert(0, os.path.join(RAIZ, "benchmark"))
        import auditoria_vazamento as AV
        rel = AV.auditar()
        self.assertEqual(rel["violacoes"], [], rel["violacoes"])

    def test_programas_do_contrato_nao_sao_solucoes_conhecidas(self):
        sys.path.insert(0, os.path.join(RAIZ, "benchmark"))
        import auditoria_vazamento as AV
        progs = AV.programas_enviados()
        self.assertGreaterEqual(len(progs), 2)                  # o exemplo do contrato e a testemunha do kit
        self.assertEqual(AV.programas_que_sao_solucoes(), [])
        conhecidas = AV.solucoes_conhecidas()
        self.assertGreater(len(conhecidas), 20)
        from fedro_piloto.biblioteca import canonizar
        from fedro_piloto.dsl import imprimir, parse
        # controlo positivo: um programa que É uma solução registada seria apanhado
        alguma = next(iter(conhecidas))
        self.assertIn(imprimir(canonizar(parse(alguma))), conhecidas)

    def test_auditoria_deteta_termo_proibido(self):
        sys.path.insert(0, os.path.join(RAIZ, "benchmark"))
        import auditoria_vazamento as AV
        proibidos = AV.termos_proibidos()
        self.assertGreater(len(proibidos["identificadores"]), 20)
        texto = "Esta tarefa compõe " + sorted(proibidos["identificadores"])[0] + " com outra."
        self.assertTrue(AV.violacoes_no_texto(texto, proibidos))
        self.assertFalse(AV.violacoes_no_texto("O enumerador usa filtrar@P e vizinhos.", proibidos))


if __name__ == "__main__":
    unittest.main()
