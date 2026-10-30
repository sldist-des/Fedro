"""Oráculo do ambiente (documento 02, 2.2.3 e 2.9; documento 03, PQ9, PM12-PM13, U23-U24).

Responde rotulo(g) e contraexemplo(h): a menor grade, na ordem de minimalidade
(n, número de pretas, lexicográfica linha a linha), em que a hipótese h e o conceito c discordam.

Domínio de busca (restrito aos baldes da partição do oráculo, por omissão "oraculo_treino"):
  1. n em ns_exaustivo (1 a 4): todas as grades da partição, na ordem de minimalidade (exato);
  2. n em ns_reservatorio (5, 6): o reservatório fixo por semente de geradores.reservatorio_oraculo
     (positivos construtivos, negativos emparelhados, quase-acertos), na mesma ordem;
     seguido, se nada discordar, de busca local por UMA troca preta<->branca a partir das grades do
     reservatório (mantém o número de pretas de cada semente), com orçamento fixo de grades.
Para n >= 5 o mínimo é o mínimo DENTRO do conjunto examinado, não do domínio (minimo_garantido=False).
Tamanhos degenerados (geradores.degenerado; critério "sem_par" por omissão) são pulados na ordem
normal e examinados só no fim (adiados, nunca descartados); a ordem efetiva é Oraculo.ordem_busca e a
minimalidade vale nessa ordem (a força bruta de U23 recebe a mesma ordem de tamanhos).

h é um callable Grade -> bool (o aprendiz passa o seu termo avaliado com orçamento de passos).
Exceções de orçamento (avaliador.OrcamentoEsgotado, por omissão) tornam h INDEFINIDA na grade:
o oráculo pula a grade e regista-a; não conta como discordância. Outras exceções propagam.

Tudo aqui é AMBIENTE (proveniência "ambiente"): nada deste módulo entra na biblioteca do aprendiz.
Custo: ContadorOraculo (determinístico) e MedicaoOraculo (tempo de parede, memória de pico) são
estruturas distintas; o livro-razão recebe só os contadores (oraculo_consultas,
oraculo_custo_ambiente = grades examinadas na consulta, geracao_grades da construção).
"""
from __future__ import annotations

import random
import resource
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

from . import geradores as G
from .avaliador import OrcamentoEsgotado
from .grade import Grade, chave_minimalidade, todas_as_grades
from .referencias import REGISTRO, Conceito

PROVENIENCIA = "ambiente"
#: hiperparâmetros do piloto (documento 03, seção 6: "tamanho do reservatório do oráculo")
K_RESERVATORIO = 40
MAX_BUSCA_LOCAL = 500
NS_EXAUSTIVO = (1, 2, 3, 4)
NS_RESERVATORIO = (5, 6)
#: critérios de degeneração aceites (ver Oraculo.__init__)
CRITERIOS_DEGENERADO = ("nenhum", "rotulo_constante", "sem_par")

Hipotese = Callable[[Grade], bool]
Resposta = Optional[Tuple[Grade, bool]]


# ---------------------------------------------------------------- custo
@dataclass
class ContadorOraculo:
    """Contadores determinísticos do oráculo (dependem só da semente e das consultas)."""
    consultas_rotulo: int = 0
    consultas_contraexemplo: int = 0
    contraexemplos_devolvidos: int = 0
    sem_contraexemplo: int = 0
    grades_examinadas: int = 0          # grades em que h foi avaliada (custo do ambiente)
    grades_exaustivo: int = 0
    grades_reservatorio: int = 0
    grades_busca_local: int = 0
    vizinhos_gerados_busca_local: int = 0
    h_indefinido: int = 0               # avaliações de h abortadas por orçamento (grade pulada)
    rotulos_calculados: int = 0         # chamadas c.rotulo (ref_a e ref_b) fora do reservatório

    def como_dict(self) -> dict:
        return asdict(self)


@dataclass
class MedicaoOraculo:
    """Medições reais (não determinísticas): nunca entram no livro-razão nem nas comparações."""
    tempo_parede_s: float = 0.0
    memoria_pico_kb: int = 0            # ru_maxrss do PROCESSO (KiB no Linux)
    latencias_s: List[float] = field(default_factory=list)   # uma por consulta de contraexemplo
    tempo_construcao_s: float = 0.0

    def latencia_max(self) -> float:
        return max(self.latencias_s, default=0.0)

    def como_dict(self) -> dict:
        return {"tempo_parede_s": self.tempo_parede_s, "memoria_pico_kb": self.memoria_pico_kb,
                "latencia_max_s": self.latencia_max(), "num_latencias": len(self.latencias_s),
                "tempo_construcao_s": self.tempo_construcao_s}


@dataclass(frozen=True)
class RegistroConsulta:
    """Registo determinístico de uma consulta (vai para o histórico)."""
    indice: int
    tipo: str                        # "rotulo" | "contraexemplo"
    grade: Optional[str]             # serialização da grade devolvida/consultada
    rotulo: Optional[bool]
    fonte: Optional[str]             # "exaustivo" | "reservatorio:<origem>" | "busca_local"
    n: Optional[int]
    grades_examinadas: int
    indefinidas: Tuple[str, ...]     # grades em que h ficou indefinida (puladas, ou a própria resposta)
    minimo_garantido: bool           # True só para resposta na parte exaustiva (n <= 4)
    resposta_indefinida: bool = False  # a resposta é uma grade em que h ficou INDEFINIDA (não aceita)


@lru_cache(maxsize=None)
def _ordenadas(n: int, particao: Optional[str]) -> Tuple[Grade, ...]:
    """Grades de tamanho n (<= 4) na partição, na ordem (pretas, lexicográfica)."""
    return tuple(sorted(G.grades_da_particao(n, particao), key=chave_minimalidade))


def _resolver(conceito: Union[str, Conceito]) -> Conceito:
    return REGISTRO[conceito] if isinstance(conceito, str) else conceito


# ---------------------------------------------------------------- oráculo
class Oraculo:
    """Oráculo de um conceito numa partição.

    Parâmetros principais:
      conceito: Conceito ou nome em referencias.REGISTRO;
      particao: partição de geradores.PARTICOES (a confirmatória exige permitir_confirmatorio);
      rng: random.Random do piloto (geradores.rng_piloto); usado SÓ na construção dos reservatórios,
           na ordem de ns_reservatorio, logo o oráculo é determinístico por semente;
      reservatorios: {n: geradores.Reservatorio} já construídos (dispensa rng);
      criterio_degenerado: "sem_par" (omissão: geradores.degenerado(...)["degenerado"]; para n >= 5,
        reservatório sem uma das classes), "rotulo_constante" (só falta de positivos ou negativos) ou
        "nenhum". Os tamanhos degenerados são PULADOS na ordem normal e examinados no FIM da busca,
        nunca descartados: descartá-los faria o oráculo declarar correta uma h errada (p. ex.
        ExistePreta é degenerado em todo n <= 4 e h = falso não teria contraexemplo; ver desvios).
        A ordem efetiva fica em self.ordem_busca.
    """

    def __init__(self, conceito: Union[str, Conceito], particao: str = "oraculo_treino",
                 rng: Optional[random.Random] = None, *, ns_exaustivo: Sequence[int] = NS_EXAUSTIVO,
                 ns_reservatorio: Sequence[int] = NS_RESERVATORIO, k_reservatorio: int = K_RESERVATORIO,
                 reservatorios: Optional[Dict[int, G.Reservatorio]] = None,
                 criterio_degenerado: str = "sem_par", busca_local: bool = True,
                 max_busca_local: int = MAX_BUSCA_LOCAL,
                 excecoes_indefinidas: Tuple[type, ...] = (OrcamentoEsgotado,),
                 restringir_rotulo: bool = True, permitir_confirmatorio: bool = False,
                 indefinida_discorda: bool = True):
        G.verificar_particao(particao, permitir_confirmatorio)
        if particao is None:
            raise ValueError("o oráculo exige uma partição (None é só para auditoria)")
        if criterio_degenerado not in CRITERIOS_DEGENERADO:
            raise ValueError(f"critério desconhecido: {criterio_degenerado}")
        ns_exaustivo, ns_reservatorio = tuple(sorted(ns_exaustivo)), tuple(sorted(ns_reservatorio))
        if any(not 1 <= n <= G.N_EXAUSTIVO_MAX for n in ns_exaustivo):
            raise ValueError("ns_exaustivo deve estar em 1..4")
        if any(n <= G.N_EXAUSTIVO_MAX for n in ns_reservatorio):
            raise ValueError("ns_reservatorio deve ser > 4")
        self.conceito = _resolver(conceito)
        self.particao = particao
        self.permitir_confirmatorio = permitir_confirmatorio
        self.ns_exaustivo = ns_exaustivo
        self.ns_reservatorio = ns_reservatorio
        self.k_reservatorio = k_reservatorio
        self.criterio_degenerado = criterio_degenerado
        self.busca_local = busca_local
        self.max_busca_local = max_busca_local
        self.excecoes_indefinidas = tuple(excecoes_indefinidas)
        #: h indefinida numa grade (orçamento de passos esgotado) conta como DISCORDÂNCIA: a grade é
        #: devolvida como contraexemplo com o rótulo verdadeiro. Sem isso, uma h que estoura o orçamento
        #: em todo o domínio seria aceita sem verificação (aceitação vácua; achado de revisão).
        self.indefinida_discorda = bool(indefinida_discorda)
        self.restringir_rotulo = restringir_rotulo
        self.proveniencia = PROVENIENCIA
        self.contador = ContadorOraculo()
        #: grades rotuladas no planejamento (diagnóstico exaustivo de degeneração, n <= 4): custo do ambiente
        self.rotulos_planejamento = 0
        self.medicao = MedicaoOraculo()
        self.historico: List[RegistroConsulta] = []
        self._rotulos: Dict[Grade, bool] = {}
        self._mostradas: Dict[str, Grade] = {}
        self._origem_mostrada: Dict[str, str] = {}
        # ---- construção (custo de geração em estruturas próprias) ----
        self.contador_construcao = G.ContadorGeracao()
        self.medicao_construcao = G.MedicaoGeracao()
        t0 = time.perf_counter()
        self.reservatorios: Dict[int, G.Reservatorio] = {}
        for n in ns_reservatorio:
            if reservatorios is not None and n in reservatorios:
                r = reservatorios[n]
            else:
                if rng is None:
                    raise ValueError(f"rng necessário para construir o reservatório de n={n}")
                r = G.reservatorio_oraculo(self.conceito, n, particao, rng, k_reservatorio,
                                           permitir_confirmatorio=permitir_confirmatorio)
            if any(not G.na_particao(e[0], particao) or e[0].n != n for e in r.entradas):
                raise ValueError(f"reservatório de n={n} com grades fora da partição ou do tamanho")
            if reservatorios is not None and n in reservatorios:
                for g, rot, _o in r.entradas:   # reservatório externo: confere o conceito
                    if self.conceito.rotulo(g) != rot:
                        raise ValueError(f"reservatório de n={n} não corresponde a {self.conceito.nome}")
            self.reservatorios[n] = r
            self.contador_construcao.somar(r.contador)
            self.medicao_construcao.tempo_parede_s += r.medicao.tempo_parede_s
            self.medicao_construcao.memoria_pico_kb = max(self.medicao_construcao.memoria_pico_kb,
                                                          r.medicao.memoria_pico_kb)
        for r in self.reservatorios.values():
            for g, rot, _ in r.entradas:
                self._rotulos[g] = rot
        # ---- ordem de busca (o diagnóstico de degeneração só é calculado se usado) ----
        self._diagnostico: Dict[int, dict] = {}
        self.ordem_busca: List[Tuple[str, int]] = self._planejar()
        self.medicao.tempo_construcao_s = time.perf_counter() - t0

    # ---------------- plano de busca ----------------
    def _diagnosticar(self, n: int) -> dict:
        d = self._diagnostico.get(n)
        if d is not None:
            return d
        if n in self.ns_exaustivo:
            rng_inerte = random.Random(G.SEMENTES_PILOTO.start)   # degenerado() não usa rng para n <= 4
            d = G.degenerado(self.conceito, n, self.particao, rng_inerte,
                             permitir_confirmatorio=self.permitir_confirmatorio)
            d["grades_na_particao"] = len(_ordenadas(n, self.particao))
            self.rotulos_planejamento += d["grades_na_particao"]
        else:
            r = self.reservatorios[n]
            pos = sum(1 for e in r.entradas if e[1])
            neg = len(r.entradas) - pos
            d = {"conceito": self.conceito.nome, "n": n, "particao": self.particao, "exaustivo": False,
                 "positivos_possiveis": pos > 0, "negativos_possiveis": neg > 0,
                 "negativos_emparelhados_possiveis": pos > 0 and neg > 0,
                 "degenerado": not (pos and neg), "grades_no_reservatorio": len(r.entradas),
                 "motivo": "; ".join(m for m, f in (("sem positivos no reservatório", not pos),
                                                    ("sem negativos no reservatório", not neg)) if f),
                 "hash_reservatorio": r.hash}
        self._diagnostico[n] = d
        return d

    @property
    def diagnostico(self) -> Dict[int, dict]:
        """Degeneração por tamanho: geradores.degenerado (exaustivo, n <= 4); composição do
        reservatório (n >= 5: degenerado se faltar uma das classes)."""
        return {n: self._diagnosticar(n) for n in self.ns_exaustivo + self.ns_reservatorio}

    def _eh_degenerado(self, n: int) -> bool:
        if self.criterio_degenerado == "nenhum":
            return False
        d = self._diagnosticar(n)
        if self.criterio_degenerado == "rotulo_constante":
            return not (d["positivos_possiveis"] and d["negativos_possiveis"])
        return bool(d["degenerado"])          # "sem_par"

    def _planejar(self) -> List[Tuple[str, int]]:
        normais, adiados = [], []
        for n in self.ns_exaustivo:
            (adiados if self._eh_degenerado(n) else normais).append(("exaustivo", n))
        for n in self.ns_reservatorio:
            passos = [("reservatorio", n)] + ([("busca_local", n)] if self.busca_local else [])
            (adiados if self._eh_degenerado(n) else normais).extend(passos)
        return normais + adiados

    def tamanhos_adiados(self) -> List[int]:
        """Tamanhos degenerados (pelo critério) que ficam no fim da ordem de busca."""
        return [n for n in self.ns_exaustivo + self.ns_reservatorio if self._eh_degenerado(n)]

    # ---------------- rótulos ----------------
    def _rotulo_interno(self, g: Grade) -> bool:
        r = self._rotulos.get(g)
        if r is None:
            self.contador.rotulos_calculados += 1
            r = self.conceito.rotulo(g)   # levanta AssertionError se ref_a != ref_b
            self._rotulos[g] = r
        return r

    def rotulo(self, g: Grade, livro=None, tarefa_id: str = "", aprendiz_id: str = "") -> bool:
        """Rótulo verdadeiro de g (só grades da partição, se restringir_rotulo); g passa a 'mostrada'."""
        if self.restringir_rotulo and not G.na_particao(g, self.particao):
            raise PermissionError(f"grade fora da partição {self.particao}: {g.serializar()}")
        with self._medir():
            r = self._rotulo_interno(g)
        self.contador.consultas_rotulo += 1
        self._mostrar(g, "rotulo")
        self.historico.append(RegistroConsulta(len(self.historico), "rotulo", g.serializar(), r, None, g.n,
                                               0, (), True))
        if livro is not None:
            livro.registrar_varios(tarefa_id, aprendiz_id, nota="oraculo:rotulo",
                                   oraculo_consultas=1, oraculo_custo_ambiente=1)
        return r

    # ---------------- contraexemplo ----------------
    def _candidatos(self, fonte: str, n: int, vistos: set) -> Iterable[Tuple[Grade, str]]:
        if fonte == "exaustivo":
            for g in _ordenadas(n, self.particao):
                yield g, "exaustivo"
        elif fonte == "reservatorio":
            for g, _rot, origem in self.reservatorios[n].entradas:
                yield g, "reservatorio:" + origem
        else:
            yield from ((g, "busca_local") for g in self._vizinhanca(n, vistos))

    def _vizinhanca(self, n: int, vistos: set) -> List[Grade]:
        """Grades a uma troca das grades do reservatório (mesmo número de pretas), na partição,
        fora do reservatório; até max_busca_local, depois ordenadas por chave de minimalidade."""
        reserv = {e[0] for e in self.reservatorios[n].entradas}
        cands: Dict[Grade, None] = {}
        for semente, _rot, _o in self.reservatorios[n].entradas:
            if len(cands) >= self.max_busca_local:
                break
            pretas = [k for k, b in enumerate(semente.bits) if b]
            brancas = [k for k, b in enumerate(semente.bits) if not b]
            for a in pretas:
                if len(cands) >= self.max_busca_local:
                    break
                for b in brancas:
                    bits = list(semente.bits)
                    bits[a], bits[b] = 0, 1
                    t = Grade(n, tuple(bits))
                    self.contador.vizinhos_gerados_busca_local += 1
                    if t in reserv or t in cands or t in vistos or not G.na_particao(t, self.particao):
                        continue
                    cands[t] = None
                    if len(cands) >= self.max_busca_local:
                        break
        return sorted(cands, key=chave_minimalidade)

    def contraexemplo(self, h: Hipotese, ns: Optional[Iterable[int]] = None, livro=None,
                      tarefa_id: str = "", aprendiz_id: str = "") -> Resposta:
        """(grade, rótulo verdadeiro) da menor discordância entre h e o conceito, ou None.

        ns restringe os tamanhos examinados (mantendo a ordem do plano)."""
        filtro = None if ns is None else set(ns)
        examinadas = 0
        indefinidas: List[str] = []
        resposta: Resposta = None
        fonte_resp, minimo = None, False
        resp_indef = False
        vistos: set = set()
        with self._medir() as t:
            for fonte, n in self.ordem_busca:
                if filtro is not None and n not in filtro:
                    continue
                for g, rot_fonte in self._candidatos(fonte, n, vistos):
                    if g in vistos:
                        continue
                    vistos.add(g)
                    examinadas += 1
                    if fonte == "exaustivo":
                        self.contador.grades_exaustivo += 1
                    elif fonte == "reservatorio":
                        self.contador.grades_reservatorio += 1
                    else:
                        self.contador.grades_busca_local += 1
                    try:
                        v = h(g)
                    except self.excecoes_indefinidas:
                        self.contador.h_indefinido += 1
                        indefinidas.append(g.serializar())
                        if self.indefinida_discorda:
                            resposta, fonte_resp, minimo = (g, self._rotulo_interno(g)), rot_fonte, fonte == "exaustivo"
                            resp_indef = True
                            break
                        continue
                    if not isinstance(v, bool):
                        raise TypeError(f"h deve devolver bool, devolveu {type(v).__name__}")
                    r = self._rotulo_interno(g)
                    if v != r:
                        resposta, fonte_resp, minimo = (g, r), rot_fonte, fonte == "exaustivo"
                        break
                if resposta is not None:
                    break
        self.medicao.latencias_s.append(t[0])
        self.contador.consultas_contraexemplo += 1
        self.contador.grades_examinadas += examinadas
        if resposta is None:
            self.contador.sem_contraexemplo += 1
        else:
            self.contador.contraexemplos_devolvidos += 1
            self._mostrar(resposta[0], "contraexemplo")
        self.historico.append(RegistroConsulta(
            len(self.historico), "contraexemplo", resposta[0].serializar() if resposta else None,
            resposta[1] if resposta else None, fonte_resp, resposta[0].n if resposta else None,
            examinadas, tuple(indefinidas), minimo, resp_indef))
        if livro is not None:
            livro.registrar_varios(tarefa_id, aprendiz_id, nota="oraculo:contraexemplo",
                                   oraculo_consultas=1, oraculo_custo_ambiente=examinadas)
        return resposta

    # ---------------- grades mostradas (separação por instância) ----------------
    def _mostrar(self, g: Grade, origem: str) -> None:
        k = g.hash_hex()
        if k not in self._mostradas:
            self._mostradas[k] = g
            self._origem_mostrada[k] = origem

    def registrar_mostradas(self, grades: Iterable[Grade], origem: str = "exemplo") -> None:
        """Regista grades vistas pelo aprendiz por outra via (exemplos iniciais do protocolo 2.9)."""
        for g in grades:
            self._mostrar(g, origem)

    def hashes_mostrados(self) -> frozenset:
        return frozenset(self._mostradas)

    def grades_mostradas(self) -> List[Grade]:
        return list(self._mostradas.values())

    def hash_mostradas(self) -> str:
        return G.hash_conjunto(self._mostradas.values())

    def excluir_mostradas(self, grades: Iterable) -> list:
        """Filtra grades (ou pares (grade, rótulo)) já mostradas ao aprendiz."""
        out = []
        for x in grades:
            g = x[0] if isinstance(x, tuple) else x
            if g.hash_hex() not in self._mostradas:
                out.append(x)
        return out

    # ---------------- custo e livro-razão ----------------
    @contextmanager
    def _medir(self):
        """Mede tempo de parede e memória de pico (só MedicaoOraculo); devolve [segundos] na saída."""
        caixa = [0.0]
        t0 = time.perf_counter()
        try:
            yield caixa
        finally:
            caixa[0] = time.perf_counter() - t0
            self.medicao.tempo_parede_s += caixa[0]
            self.medicao.memoria_pico_kb = max(self.medicao.memoria_pico_kb,
                                               resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    def lancar_construcao(self, livro, tarefa_id: str, aprendiz_id: str) -> None:
        """Lança no livro-razão o custo de geração dos reservatórios (custo do ambiente)."""
        livro.registrar(tarefa_id, aprendiz_id, "geracao_grades", self.contador_construcao.grades_geradas,
                        "oraculo:reservatorios")

    def hashes_reservatorios(self) -> Dict[int, str]:
        return {n: r.hash for n, r in self.reservatorios.items()}

    def estado_deterministico(self) -> dict:
        """Tudo o que deve ser idêntico entre execuções com a mesma semente (sem medições)."""
        return {"conceito": self.conceito.nome, "particao": self.particao, "proveniencia": self.proveniencia,
                "ordem_busca": [list(x) for x in self.ordem_busca],
                "criterio_degenerado": self.criterio_degenerado,
                "hashes_reservatorios": {str(n): h for n, h in self.hashes_reservatorios().items()},
                "contador": self.contador.como_dict(),
                "contador_construcao": self.contador_construcao.como_dict(),
                "rotulos_planejamento": self.rotulos_planejamento,
                "historico": [asdict(r) for r in self.historico],
                "hash_mostradas": self.hash_mostradas()}

    def resumo(self) -> dict:
        """Contadores e medições em blocos separados."""
        return {"deterministico": self.estado_deterministico(),
                "medicoes": {"consultas": self.medicao.como_dict(),
                             "construcao": self.medicao_construcao.como_dict()}}


# ---------------------------------------------------------------- força bruta (testes, U23)
def contraexemplo_forca_bruta(h: Hipotese, conceito: Union[str, Conceito], n_max: int = 4,
                              particao: Optional[str] = None, ns: Optional[Sequence[int]] = None,
                              excecoes_indefinidas: Tuple[type, ...] = (OrcamentoEsgotado,),
                              permitir_confirmatorio: bool = False, indefinida_discorda: bool = True) -> Resposta:
    """Mínimo por força bruta, implementação independente do Oraculo (todas_as_grades + min).

    Sem partição por omissão (domínio inteiro, auditoria); com `particao`, só os seus baldes.
    `ns` dá os tamanhos E a ordem em que são considerados (omissão: 1..n_max). Grades em que h
    levanta uma das excecoes_indefinidas contam como discordância (indefinida_discorda=True, como no
    oráculo) ou são puladas (False)."""
    G.verificar_particao(particao, permitir_confirmatorio)
    c = _resolver(conceito)
    ordem = list(ns) if ns is not None else list(range(1, n_max + 1))
    if any(n > G.N_EXAUSTIVO_MAX for n in ordem):
        raise ValueError("força bruta só para n <= 4")
    for n in ordem:
        discordancias = []
        for g in todas_as_grades(n):
            if not G.na_particao(g, particao):
                continue
            try:
                v = h(g)
            except excecoes_indefinidas:
                if indefinida_discorda:
                    discordancias.append((chave_minimalidade(g), g, c.rotulo(g)))
                continue
            r = c.rotulo(g)
            if bool(v) != r:
                discordancias.append((chave_minimalidade(g), g, r))
        if discordancias:
            _, g, r = min(discordancias, key=lambda x: x[0])
            return g, r
    return None
