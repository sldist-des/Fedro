"""U26 e U27 (documento 03, seção 5).

U26: duas execuções com a semente 10 001 dão registros determinísticos idênticos byte a byte (duas
execuções em PROCESSOS distintos, com PYTHONHASHSEED diferentes e número de processos diferente);
os tempos podem diferir e ficam fora da comparação.
U27: intervalos de sementes e hashes dos conjuntos do piloto contra os reservados ao confirmatório:
disjuntos; nenhuma grade usada pelo piloto está nos baldes do confirmatório.
A configuração é a mínima (piloto.config_mini): todas as fases, escala de segundos.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from fedro_piloto import geradores as G
from fedro_piloto import piloto as P
from fedro_piloto.grade import Grade
from fedro_piloto.razao import LivroRazao

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEMENTE = 10_001


def _rodar(diretorio, rid, hashseed, processos):
    env = dict(os.environ, PYTHONHASHSEED=str(hashseed), PYTHONPATH=RAIZ)
    subprocess.run([sys.executable, "-m", "fedro_piloto.piloto", "--mini", "--semente", str(SEMENTE),
                    "--id", rid, "--raiz", diretorio, "--processos", str(processos)],
                   check=True, cwd=RAIZ, env=env, stdout=subprocess.DEVNULL)
    return os.path.join(diretorio, rid)


class TestU26Determinismo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.d1 = _rodar(cls.tmp.name, "a", 1, 2)
        cls.d2 = _rodar(cls.tmp.name, "b", 4242, 1)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _ler(self, d, nome, modo="rb"):
        with open(os.path.join(d, nome), modo) as f:
            return f.read()

    def test_registros_identicos_byte_a_byte(self):
        for nome in ("deterministico.json", "relatorio.md", "hashes.json", "abstracoes.json", "config.json"):
            self.assertEqual(self._ler(self.d1, nome), self._ler(self.d2, nome), nome)

    def test_livro_razao_identico_medicoes_separadas(self):
        l1 = LivroRazao.carregar_json(os.path.join(self.d1, "razao.json"))
        l2 = LivroRazao.carregar_json(os.path.join(self.d2, "razao.json"))
        self.assertEqual(l1.comparar_deterministico(l2), [])
        self.assertEqual(l1.serializar_deterministico(), l2.serializar_deterministico())
        self.assertTrue(l1.verificar_fechamento().ok)
        dados = json.loads(self._ler(self.d1, "razao.json", "r"))
        self.assertEqual(set(dados), {"deterministico", "medicoes"})
        det = self._ler(self.d1, "deterministico.json", "r")
        for chave in ("tempo_parede_s", "memoria_pico", "latencia", "cpu_s"):
            self.assertNotIn(chave, det, chave)
        med = json.loads(self._ler(self.d1, "medicoes.json", "r"))
        self.assertIn("fases", med)

    def test_todas_as_fases_presentes(self):
        det = json.loads(self._ler(self.d1, "deterministico.json", "r"))
        self.assertEqual(sorted(det["fases"]), [str(i) for i in range(1, 8)])
        self.assertTrue(det["fases"]["6"]["fechamento"]["ok"])
        self.assertEqual(det["fases"]["6"]["pm14_conciliacao"]["diferenca"], 0)
        self.assertTrue(det["fases"]["6"]["pm12"]["ok"])
        # PM11 pela compressão gulosa; I4 registrada
        self.assertIn("I4_disparada", det["fases"]["5"])
        self.assertIn("fontes", det)
        self.assertIn(det["fases"]["7"]["decisao"], ("GO com E0", "GO com E0+", "NO-GO"))
        # fase 5 é explicitamente mecanismo-teste
        for l in det["fases"]["5"]["pm11"]:
            self.assertEqual(l["modo"], "mecanismo-teste")
            self.assertEqual(l["proveniencia"], "manual-teste")
        # abstrações da execução autônoma: só 'descoberta'
        for b in det["fases"]["6"]["bracos"].values():
            for a in b["abstracoes"]:
                self.assertEqual(a["proveniencia"], "descoberta")


class TestReaproveitamento(unittest.TestCase):
    def test_fases_recalculadas_iguais(self):
        """Recalcular 1, 6, 7 reaproveitando 2-5 de uma execução anterior dá as mesmas fases."""
        with tempfile.TemporaryDirectory() as d:
            a = os.path.join(d, "a")
            ra = P.executar(P.config_mini(SEMENTE), a)
            cfg = P.config_mini(SEMENTE)
            cfg.fases = (1, 6, 7)
            rb = P.executar(cfg, os.path.join(d, "b"), reaproveitar=a)
            norm = lambda x: json.loads(P._dump(x))   # como gravado (chaves int viram texto)
            self.assertEqual(norm(ra["deterministico"]["fases"]), norm(rb["deterministico"]["fases"]))
            self.assertEqual(rb["deterministico"]["reaproveitamento"]["fases_reaproveitadas"], ["2", "3", "4", "5"])
            outra = P.config_mini(SEMENTE)
            outra.B_tarefa += 1
            with self.assertRaises(ValueError):
                P.executar(outra, None, reaproveitar=a)


class TestU27Separacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = P.executar(P.config_mini(SEMENTE))

    def test_sementes(self):
        self.assertTrue(set(G.SEMENTES_PILOTO).isdisjoint(range(G.SEMENTE_MIN_CONFIRMATORIO,
                                                                G.SEMENTE_MIN_CONFIRMATORIO + 10 ** 6)))
        with self.assertRaises(ValueError):
            G.rng_confirmatorio(SEMENTE)
        with self.assertRaises(ValueError):
            G.rng_piloto(G.SEMENTE_MIN_CONFIRMATORIO)
        with self.assertRaises(ValueError):
            P.executar(P.config_mini(G.SEMENTE_MIN_CONFIRMATORIO))
        with self.assertRaises(PermissionError):
            G.verificar_particao(G.PARTICAO_CONFIRMATORIA)

    def test_particoes_disjuntas(self):
        s = self.r["deterministico"]["separacao"]
        self.assertTrue(s["particoes_disjuntas"])
        baldes = [b for r in G.PARTICOES.values() for b in r]
        self.assertEqual(sorted(baldes), list(range(G.NUM_BALDES)))

    def test_nenhuma_grade_do_confirmatorio(self):
        s = self.r["deterministico"]["separacao"]
        self.assertEqual(s["grades_no_confirmatorio"], 0)
        self.assertGreater(len(s["conjuntos"]), 5)
        for nome, c in s["conjuntos"].items():
            self.assertEqual(c["no_confirmatorio"], 0, nome)
            self.assertNotIn(G.PARTICAO_CONFIRMATORIA, c["particoes"], nome)

    def test_hashes_disjuntos_de_um_conjunto_confirmatorio(self):
        """Grades do piloto × uma amostra gerada com semente e partição confirmatórias: disjuntas."""
        rng = G.rng_confirmatorio(G.SEMENTE_MIN_CONFIRMATORIO)
        conf = set()
        for n in (3, 4, 5):
            for _ in range(200):
                while True:
                    g = G.amostra_natural(n, rng)
                    if G.na_particao(g, G.PARTICAO_CONFIRMATORIA):
                        break
                conf.add(g.hash_hex())
        piloto = set()
        det = self.r["deterministico"]
        for b in det["fases"]["6"]["bracos"].values():
            for p in b["preparos"]:
                for e in p["exemplos"]:
                    ent = e["entrada"]
                    for x in (ent if isinstance(ent, list) else [ent]):
                        if isinstance(x, str) and ":" in x:
                            piloto.add(Grade.de_texto(x).hash_hex())
        self.assertTrue(piloto)
        self.assertTrue(piloto.isdisjoint(conf))

    def test_oraculo_recusa_particao_confirmatoria(self):
        from fedro_piloto import aprendizes as A
        with self.assertRaises(PermissionError):
            A.OraculoFuncao(A.TAREFAS_POR_ID["vizPretos"], G.rng_piloto(SEMENTE), particao=G.PARTICAO_CONFIRMATORIA)


if __name__ == "__main__":
    unittest.main()
