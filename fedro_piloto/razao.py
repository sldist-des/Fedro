"""Livro-razão de custo (documento 02, 2.5; documento 03, 2.3, PQ10, PM14, PM15, U25).

Duas estruturas que nunca se misturam:
  - CONTADORES determinísticos por (tarefa_id, aprendiz_id), só inteiros, lançados num diário
    (lista ordenada de lançamentos). Duas execuções com a mesma semente devem dar contadores e
    diário idênticos (comparar_deterministico).
  - MEDIÇÕES reais (tempo de parede, memória de pico = ru_maxrss do processo), em bloco separado;
    podem diferir entre execuções e são ignoradas na comparação determinística.

Unidade: um candidato avaliado conta 1 em qualquer base (E0, E0', E0+, E0'+). Os campos têm
unidades diferentes (candidatos, passos, nós, consultas, grades); total() é a soma declarada pelo
protocolo e é sempre reportado ao lado dos subtotais por grupo (aprendiz, ambiente, avaliação).
"""
from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from .medidas import medir as _medir_real

#: campos determinísticos, na ordem de serialização
#: busca_candidatos = candidatos NO SENTIDO DO PROTOCOLO (documento 03, 2.3: termo fechado do tipo da
#: tarefa submetido aos exemplos); enumeracao_candidatos = candidatos internos do enumerador (subtermos
#: de todos os tipos avaliados nos mundos OE). Unidades diferentes: campos separados (achado de revisão).
#: oraculo_custo_ambiente = entradas (grades) examinadas pelo oráculo; oraculo_passos_hipotese = passos de
#: Sem_n da hipótese nessas entradas; geracao_rotulos = chamadas de rótulo/permutações/trocas/consultas
#: de tabela exaustiva na geração e no planejamento do oráculo.
CAMPOS = ("busca_candidatos", "enumeracao_candidatos", "busca_passos", "enumeracao_passos",
          "compressao_subtermos", "oraculo_consultas", "oraculo_custo_ambiente", "oraculo_passos_hipotese",
          "avaliacao_passos", "geracao_grades", "geracao_rotulos")
#: custo do próprio aprendiz (busca, enumeração OE, compressão, consultas que ele faz)
CAMPOS_APRENDIZ = ("busca_candidatos", "enumeracao_candidatos", "busca_passos", "enumeracao_passos",
                   "compressao_subtermos", "oraculo_consultas")
#: custo do ambiente (busca de contraexemplo, geração de grades): reportado à parte (2.5)
CAMPOS_AMBIENTE = ("oraculo_custo_ambiente", "oraculo_passos_hipotese", "geracao_grades", "geracao_rotulos")
#: avaliação em teste (medida, não aprendizagem)
CAMPOS_AVALIACAO = ("avaliacao_passos",)
assert set(CAMPOS) == set(CAMPOS_APRENDIZ) | set(CAMPOS_AMBIENTE) | set(CAMPOS_AVALIACAO)

Chave = Tuple[str, str]


@dataclass
class EntradaRazao:
    """Contadores determinísticos de uma (tarefa, aprendiz). Só inteiros."""
    tarefa_id: str
    aprendiz_id: str
    busca_candidatos: int = 0
    enumeracao_candidatos: int = 0
    busca_passos: int = 0
    enumeracao_passos: int = 0
    compressao_subtermos: int = 0
    oraculo_consultas: int = 0
    oraculo_custo_ambiente: int = 0
    oraculo_passos_hipotese: int = 0
    avaliacao_passos: int = 0
    geracao_grades: int = 0
    geracao_rotulos: int = 0

    def total(self) -> int:
        return sum(getattr(self, c) for c in CAMPOS)

    def total_aprendiz(self) -> int:
        return sum(getattr(self, c) for c in CAMPOS_APRENDIZ)

    def total_ambiente(self) -> int:
        return sum(getattr(self, c) for c in CAMPOS_AMBIENTE)

    def total_avaliacao(self) -> int:
        return sum(getattr(self, c) for c in CAMPOS_AVALIACAO)

    def campos(self) -> Dict[str, int]:
        return {c: getattr(self, c) for c in CAMPOS}

    def como_dict(self) -> dict:
        d = {"tarefa_id": self.tarefa_id, "aprendiz_id": self.aprendiz_id}
        d.update(self.campos())
        d["total"] = self.total()
        d["total_aprendiz"] = self.total_aprendiz()
        d["total_ambiente"] = self.total_ambiente()
        d["total_avaliacao"] = self.total_avaliacao()
        return d


@dataclass
class MedicaoRazao:
    """Medições reais de uma (tarefa, aprendiz). memoria_pico_kb = ru_maxrss do PROCESSO (KiB no Linux)."""
    tempo_parede_s: float = 0.0
    memoria_pico_kb: int = 0

    def como_dict(self) -> dict:
        d = asdict(self)
        d["memoria_escopo"] = "pico do PROCESSO desde o início (monotônico; não isolável por tarefa)"
        return d


@dataclass(frozen=True)
class Lancamento:
    tarefa_id: str
    aprendiz_id: str
    campo: str
    quantidade: int
    nota: str = ""


@dataclass
class ResultadoFechamento:
    ok: bool
    total_diario: int
    total_entradas: int
    soma_campos: int
    problemas: List[str] = field(default_factory=list)

    @property
    def diferenca(self) -> int:
        """PM14: total − soma das partes (deve ser 0)."""
        return self.total_entradas - self.soma_campos


def _inteiro(q) -> int:
    if isinstance(q, bool) or not isinstance(q, int):
        raise TypeError(f"contador determinístico exige int, recebeu {type(q).__name__} (medições vão em medir())")
    if q < 0:
        raise ValueError("quantidade negativa")
    return q


class LivroRazao:
    """Livro-razão por (tarefa_id, aprendiz_id) com diário de lançamentos e medições separadas."""

    def __init__(self, semente: Optional[int] = None, metadados: Optional[dict] = None):
        self.semente = semente
        self.metadados = dict(metadados or {})
        self._entradas: Dict[Chave, EntradaRazao] = {}
        self.diario: List[Lancamento] = []
        self.medicoes: Dict[Chave, MedicaoRazao] = {}

    # ---------------- lançamentos (determinísticos) ----------------
    def entrada(self, tarefa_id, aprendiz_id) -> EntradaRazao:
        k = (str(tarefa_id), str(aprendiz_id))
        if k not in self._entradas:
            self._entradas[k] = EntradaRazao(*k)
        return self._entradas[k]

    def registrar(self, tarefa_id, aprendiz_id, campo: str, quantidade: int, nota: str = "") -> None:
        if campo not in CAMPOS:
            raise KeyError(f"campo desconhecido: {campo!r}")
        q = _inteiro(quantidade)
        e = self.entrada(tarefa_id, aprendiz_id)
        setattr(e, campo, getattr(e, campo) + q)
        self.diario.append(Lancamento(e.tarefa_id, e.aprendiz_id, campo, q, nota))

    def registrar_varios(self, tarefa_id, aprendiz_id, nota: str = "", **campos: int) -> None:
        for c in CAMPOS:          # ordem fixa: o diário não depende da ordem dos kwargs
            if c in campos:
                self.registrar(tarefa_id, aprendiz_id, c, campos.pop(c), nota)
        if campos:
            raise KeyError(f"campos desconhecidos: {sorted(campos)}")

    def registrar_candidato(self, tarefa_id, aprendiz_id, passos: int, base: str = "") -> None:
        """Um candidato avaliado: +1 candidato (qualquer base) e +passos de avaliação na busca."""
        self.registrar(tarefa_id, aprendiz_id, "busca_candidatos", 1, base)
        self.registrar(tarefa_id, aprendiz_id, "busca_passos", passos, base)

    # ---------------- medições (reais, separadas) ----------------
    @contextmanager
    def medir(self, tarefa_id, aprendiz_id):
        """with livro.medir(t, a): ...  acumula tempo de parede e atualiza a memória de pico."""
        k = (str(tarefa_id), str(aprendiz_id))
        m = self.medicoes.setdefault(k, MedicaoRazao())
        with _medir_real(f"{k[0]}/{k[1]}") as real:
            yield m
        m.tempo_parede_s += real.tempo_parede_s
        m.memoria_pico_kb = max(m.memoria_pico_kb, real.memoria_pico_kib)

    # ---------------- consulta ----------------
    def entradas(self) -> List[EntradaRazao]:
        return list(self._entradas.values())

    def total(self) -> int:
        return sum(e.total() for e in self._entradas.values())

    def total_por_campo(self) -> Dict[str, int]:
        return {c: sum(getattr(e, c) for e in self._entradas.values()) for c in CAMPOS}

    def total_por_aprendiz(self) -> Dict[str, Dict[str, int]]:
        out: Dict[str, Dict[str, int]] = {}
        for e in self._entradas.values():
            d = out.setdefault(e.aprendiz_id, {c: 0 for c in CAMPOS})
            for c in CAMPOS:
                d[c] += getattr(e, c)
        for d in out.values():
            d["total"] = sum(d[c] for c in CAMPOS)
        return out

    def hash_diario(self) -> str:
        h = hashlib.sha256()
        for l in self.diario:
            h.update(f"{l.tarefa_id}\t{l.aprendiz_id}\t{l.campo}\t{l.quantidade}\t{l.nota}\n".encode("utf-8"))
        return h.hexdigest()

    # ---------------- fechamento ----------------
    def verificar_fechamento(self) -> ResultadoFechamento:
        """Refaz cada entrada a partir do diário e confere: entradas = diário campo a campo;
        total = soma das partes (por entrada e global); só inteiros não negativos."""
        problemas: List[str] = []
        refeito: Dict[Chave, Dict[str, int]] = {}
        total_diario = 0
        for l in self.diario:
            d = refeito.setdefault((l.tarefa_id, l.aprendiz_id), {c: 0 for c in CAMPOS})
            d[l.campo] += l.quantidade
            total_diario += l.quantidade
        soma_campos = 0
        for k, e in self._entradas.items():
            for c in CAMPOS:
                v = getattr(e, c)
                if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                    problemas.append(f"{k} {c}: valor não inteiro ou negativo ({v!r})")
                    continue
                soma_campos += v
                esperado = refeito.get(k, {}).get(c, 0)
                if v != esperado:
                    problemas.append(f"{k} {c}: entrada {v} ≠ diário {esperado}")
        for k in refeito:
            if k not in self._entradas:
                problemas.append(f"{k}: lançamentos sem entrada")
        try:
            total_entradas = self.total()
        except TypeError:
            total_entradas = -1
            problemas.append("total não computável")
        if total_entradas != soma_campos:
            problemas.append(f"total {total_entradas} ≠ soma dos campos {soma_campos}")
        if total_diario != soma_campos:
            problemas.append(f"diário {total_diario} ≠ soma dos campos {soma_campos}")
        return ResultadoFechamento(not problemas, total_diario, total_entradas, soma_campos, problemas)

    # ---------------- serialização ----------------
    def deterministico_dict(self, incluir_diario: bool = False) -> dict:
        d = {"semente": self.semente, "metadados": self.metadados,
             "campos": list(CAMPOS),
             "entradas": [e.como_dict() for e in self._entradas.values()],
             "total_por_campo": self.total_por_campo(),
             "total": self.total(),
             "num_lancamentos": len(self.diario),
             "hash_diario": self.hash_diario()}
        if incluir_diario:
            d["diario"] = [asdict(l) for l in self.diario]
        return d

    def medicoes_dict(self) -> dict:
        return {"aviso": "medições reais; não determinísticas; fora da comparação e do total",
                "por_entrada": [{"tarefa_id": k[0], "aprendiz_id": k[1], **m.como_dict()}
                                for k, m in self.medicoes.items()]}

    def como_dict(self, incluir_diario: bool = False) -> dict:
        return {"deterministico": self.deterministico_dict(incluir_diario), "medicoes": self.medicoes_dict()}

    def serializar_json(self, caminho: Optional[str] = None, incluir_diario: bool = True) -> str:
        """JSON com blocos separados "deterministico" e "medicoes" (chaves ordenadas). Grava em
        `caminho` se dado; devolve o texto."""
        txt = json.dumps(self.como_dict(incluir_diario), ensure_ascii=False, sort_keys=True, indent=1)
        if caminho is not None:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(txt)
        return txt

    def serializar_deterministico(self) -> str:
        """Só o bloco determinístico (igual byte a byte entre execuções com a mesma semente)."""
        return json.dumps(self.deterministico_dict(incluir_diario=True), ensure_ascii=False, sort_keys=True, indent=1)

    @classmethod
    def carregar_json(cls, caminho: str) -> "LivroRazao":
        """Reconstrói o livro a partir de um JSON com diário (serializar_json(incluir_diario=True))."""
        with open(caminho, encoding="utf-8") as f:
            d = json.load(f)
        det = d["deterministico"]
        if "diario" not in det:
            raise ValueError("JSON sem diário: não é possível reconstruir o livro")
        livro = cls(det.get("semente"), det.get("metadados"))
        for e in det["entradas"]:
            livro.entrada(e["tarefa_id"], e["aprendiz_id"])  # preserva a ordem das entradas
        for l in det["diario"]:
            livro.registrar(l["tarefa_id"], l["aprendiz_id"], l["campo"], l["quantidade"], l.get("nota", ""))
        for m in d.get("medicoes", {}).get("por_entrada", []):
            livro.medicoes[(m["tarefa_id"], m["aprendiz_id"])] = MedicaoRazao(m["tempo_parede_s"], m["memoria_pico_kb"])
        return livro

    # ---------------- comparação ----------------
    def comparar_deterministico(self, outro: "LivroRazao") -> List[str]:
        """Diferenças nos contadores determinísticos (entradas, ordem, diário); ignora medições.
        Lista vazia = livros determinísticos idênticos (PM15)."""
        dif: List[str] = []
        if self.semente != outro.semente:
            dif.append(f"semente {self.semente} ≠ {outro.semente}")
        ka, kb = list(self._entradas), list(outro._entradas)
        if ka != kb:
            dif.append(f"chaves/ordem das entradas diferem: {ka} ≠ {kb}")
        for k in ka:
            if k in outro._entradas:
                a, b = self._entradas[k].campos(), outro._entradas[k].campos()
                for c in CAMPOS:
                    if a[c] != b[c]:
                        dif.append(f"{k} {c}: {a[c]} ≠ {b[c]}")
        if len(self.diario) != len(outro.diario):
            dif.append(f"diário: {len(self.diario)} ≠ {len(outro.diario)} lançamentos")
        elif self.hash_diario() != outro.hash_diario():
            for i, (x, y) in enumerate(zip(self.diario, outro.diario)):
                if x != y:
                    dif.append(f"diário difere a partir do lançamento {i}: {x} ≠ {y}")
                    break
        return dif

    def tabela_markdown(self) -> str:
        cab = "| tarefa | aprendiz | " + " | ".join(CAMPOS) + " | total | aprendiz | ambiente |"
        linhas = [cab, "|" + "---|" * (len(CAMPOS) + 5)]
        for e in self._entradas.values():
            linhas.append(f"| {e.tarefa_id} | {e.aprendiz_id} | " + " | ".join(str(getattr(e, c)) for c in CAMPOS)
                          + f" | {e.total()} | {e.total_aprendiz()} | {e.total_ambiente()} |")
        return "\n".join(linhas)
