"""Medições REAIS (tempo de parede, memória de pico). Estrutura separada dos contadores
determinísticos (avaliador.Contador e afins): nunca entram no livro-razão de custo simbólico,
são reportadas ao lado (documento 02, 2.5)."""
from __future__ import annotations

import resource
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class MedicaoReal:
    tempo_parede_s: float = 0.0
    #: pico de memória residente do PROCESSO até o fim da medição (ru_maxrss não é reiniciável),
    #: em KiB (Linux) — não é o pico do trecho medido isoladamente.
    memoria_pico_kib: int = 0
    rotulo: str = ""
    #: "processo-desde-o-inicio" (ru_maxrss) ou "trecho" (VmHWM reiniciado no início; medir_isolado)
    memoria_escopo: str = "processo-desde-o-inicio"


def _maxrss_kib() -> int:
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r // 1024 if sys.platform == "darwin" else r  # macOS reporta bytes


@contextmanager
def medir(rotulo: str = ""):
    """with medir() as m: ...  -> m.tempo_parede_s, m.memoria_pico_kib preenchidos na saída."""
    m = MedicaoReal(rotulo=rotulo)
    t0 = time.perf_counter()
    try:
        yield m
    finally:
        m.tempo_parede_s = time.perf_counter() - t0
        m.memoria_pico_kib = _maxrss_kib()


def reiniciar_pico() -> bool:
    """Reinicia o pico de memória residente do processo (Linux: escrever 5 em /proc/self/clear_refs
    zera VmHWM). Devolve False se não suportado (então só há o pico desde o início do processo)."""
    try:
        with open("/proc/self/clear_refs", "w") as f:
            f.write("5")
        return True
    except OSError:
        return False


def pico_vmhwm_kib():
    """VmHWM do processo em KiB (Linux), ou None."""
    try:
        with open("/proc/self/status") as f:
            for linha in f:
                if linha.startswith("VmHWM:"):
                    return int(linha.split()[1])
    except OSError:
        pass
    return None


@contextmanager
def medir_isolado(rotulo: str = ""):
    """Como medir(), mas tenta isolar o pico de memória do TRECHO (reinicia VmHWM no início).
    m.memoria_escopo diz o que o número significa: 'trecho' (isolado) ou 'processo-desde-o-inicio'."""
    m = MedicaoReal(rotulo=rotulo)
    isolado = reiniciar_pico()
    t0 = time.perf_counter()
    try:
        yield m
    finally:
        m.tempo_parede_s = time.perf_counter() - t0
        v = pico_vmhwm_kib() if isolado else None
        m.memoria_pico_kib = v if v is not None else _maxrss_kib()
        m.memoria_escopo = "trecho" if v is not None else "processo-desde-o-inicio"
