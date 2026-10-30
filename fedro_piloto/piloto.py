"""Orquestração do piloto EXPLORATÓRIO (documento 03, seção 7), com orçamentos reduzidos.

Fases (numeração deste módulo; ver CONFIG e os desvios declarados em DESVIOS_ESCALA):
  1 referências + geradores: PM1 (ref_a = ref_b), PM2-PM5 (conjuntos de desenho), PM6 (frequências
    naturais contra analysis/audit_frequencias_saida.md), degeneração por (conceito, n);
  2 contagem N(s, τ) até s_max em 3 contextos (PM7);
  3 alcance s_reach(B) em E0, E0', E0+, E0'+ (tabelas CURADAS, D = 2) para 3 contextos e para os tipos
    fechados das tarefas; s_reach com a tabela SISTEMÁTICA (não curada); s_reach com D adequado à
    profundidade λ dos programas; s_reach com os degraus anteriores na tabela; auditoria da poda OE
    contra amostra independente (classes perdidas por tamanho); PM8, PM9;
  4 viabilidade da escada (PM10) e verificação dos programas MANUAIS (manual-teste) contra as
    referências do ambiente;
  5 MECANISMO (modo "mecanismo-teste", explicitamente rotulado): extração a partir de soluções
    manuais (PM11 = o que a compressão GULOSA insere). Nada desta fase é descoberta nem entra em
    biblioteca de aprendiz;
  6 EXECUÇÃO AUTÔNOMA: L-fix e L-lib (biblioteca vazia, modo "autonomo") nas escadas F2 e F3, em E0 e
    E0+; registro por tarefa; comparação a custo cumulativo TOTAL igual; PM12 (minimalidade do
    oráculo); conciliação do livro-razão com contadores independentes (PM14);
  7 decisão GO / E0+ / NO-GO (documento 03, seção 10) com a exigência adicional de descoberta e
    reutilização autônomas POR BASE; condições de interrupção I4/I6 e PM16 (estas em medicoes.*).

Registros em runs/<id>/: config.json (com SHA-256 das fontes), deterministico.json (contadores,
aceitações, termos; idêntico entre execuções com a mesma semente e o mesmo código), medicoes.json
(tempo, memória, latência, vazão, PM9/PM13/PM16/I6; NÃO determinístico), razao.json (livro-razão:
blocos "deterministico" e "medicoes"), hashes.json, abstracoes.json, relatorio.md (só
determinístico), medicoes.md e, com --comparar-com, pm15.json.
Nenhuma alegação científica sai daqui (documento 03, seção 0).
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import random
import re
import resource
import sys
import time
from dataclasses import asdict, dataclass, replace
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from . import aprendizes as A
from . import geradores as G
from . import programas_referencia as PR
from .avaliador import Contador, Contexto, OrcamentoEsgotado, aplicar, avaliar, compilar
from .biblioteca import Biblioteca, Solucao, extrair_fragmentos
from .dsl import (BASES, BASES_SISTEMATICAS, BOOL, FUN, GRADE, LP, TIPOS_TAREFA, C, Termo, entrada_biblioteca,
                  imprimir, imprimir_legivel, tamanho, tipo_str)
from .enumerador import contar_termos, enumerar_sem_poda, grades_amostra_oe
from .grade import Grade, todas_as_grades
from .razao import CAMPOS, LivroRazao, MedicaoRazao
from .referencias import REGISTRO
from .tradutores import comparar_denotacoes, inline

PROVENIENCIA_FASE5 = "manual-teste"
CONTEXTOS: Dict[str, Tuple[dict, tuple]] = {
    "{g} → Bool": ({"g": GRADE}, BOOL),
    "{g} → L Pos": ({"g": GRADE}, LP),
    "{g, S: L Pos} → L Pos": ({"g": GRADE, "S": LP}, LP),
}
#: nomes do relatório de auditoria (analysis/) → nomes em referencias.REGISTRO (só equivalências exatas)
MAPA_AUDITORIA = {
    "TopoCheio": "TopoCheio", "LinhaOcupada": "LinhaOcupada", "LinhasIguais": "LinhasIguais",
    "MetadesIguais": "Igual_metadeEsq_metadeDir", "PrimeiraUltimaIguais": "Igual_linha1_linhaN",
    "CantoSupEsq": "CantoSupEsq", "Diagonal": "Diagonal", "ColunaDoisVazia": "ColunaDoisVazia",
    "DoisSeparados": "DoisSeparados", "MaiorTocaBorda": "MaiorTocaBorda", "NenhumaIsolada": "NenhumaIsolada",
    "PeloMenosDois": "PeloMenosDois", "TodosMesmoTamanho": "TodosMesmoTamanho",
    "TresComponentes": "TresComponentes", "UmComponente": "UmComponente",
    "ComponentesIgualLinha1": "NumCompIgualLinha1",
}
CAMINHO_AUDITORIA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 "analysis", "audit_frequencias_saida.md")
BASE_NOME = {"E0": "E0", "E0p": "E0'", "E0mais": "E0+", "E0pmais": "E0'+"}
#: um representante de tarefa por tipo fechado (entradas da auditoria OE = baterias do ambiente)
TAREFA_DO_TIPO = {tipo_str(A.TAREFAS_POR_ID[t].tipo): t for t in ("ExistePreta", "vizPretos", "passo",
                                                                   "descartar", "noMaximo")}


# =====================================================================
# Configuração
# =====================================================================
@dataclass
class ConfigPiloto:
    semente: int = 10_001
    fases: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7)
    processos: int = 4
    # fase 1
    pm1_ns_exaustivo: Tuple[int, ...] = (1, 2, 3, 4)
    pm1_ns_amostra: Tuple[int, ...] = (5, 6, 7, 8, 9)
    pm1_amostras_por_n: int = 300
    pm2_conceitos: Tuple[str, ...] = ("ExistePreta", "ParAdjacente", "NenhumaIsolada", "UmComponente",
                                      "Igual_linha1_linhaN", "LinhasIguais", "TodosMesmoTamanho", "DoisSeparados")
    pm2_ns: Tuple[int, ...] = (3, 4, 5, 6)
    pm2_k_pares: int = 100
    pm6_conceitos: Tuple[str, ...] = tuple(MAPA_AUDITORIA)
    pm6_ns: Tuple[int, ...] = (3, 4, 5, 6)
    pm6_amostras: int = 1000
    degeneracao_conceitos: Tuple[str, ...] = ("ExistePreta", "ParAdjacente", "NenhumaIsolada", "UmComponente",
                                              "Igual_linha1_linhaN", "LinhasIguais")
    degeneracao_ns: Tuple[int, ...] = (1, 2, 3, 4, 5, 6)
    degeneracao_tentativas: int = 200
    # fase 2
    contagem_s_max: int = 10
    contagem_bases: Tuple[str, ...] = ("E0", "E0p", "E0mais", "E0pmais")
    # fase 3: (base, contexto) -> orçamentos; contextos ausentes usam alcance_orcamentos_reduzidos
    alcance_bases: Tuple[str, ...] = ("E0", "E0p", "E0mais", "E0pmais")
    alcance_orcamentos: Tuple[int, ...] = (10 ** 4, 10 ** 5)
    alcance_orcamentos_reduzidos: Tuple[int, ...] = (10 ** 4,)
    alcance_completos: Tuple[Tuple[str, str], ...] = (
        ("E0", "{g} → Bool"), ("E0", "{g, S: L Pos} → L Pos"), ("E0p", "{g} → Bool"), ("E0mais", "{g} → Bool"))
    alcance_s_max: int = 30
    processos_alcance: int = 3          # memória: uma medição a 10^5 em E0+ passou de 8 GB (OOM; ver desvios)
    #: RLIMIT_AS por trabalhador: ALTERA onde uma medição pode parar, logo faz parte da configuração
    memoria_trabalhador_gb: Optional[float] = 4.0
    alcance_fechado_B: int = 10 ** 4
    alcance_fechado_tipos: Tuple[str, ...] = tuple(tipo_str(t) for t in TIPOS_TAREFA)
    #: B ÚNICO da tabela PM10 (medido em todos os contextos, tabelas e D); B_max = 10^6 não medido (desvio)
    alcance_B_unico: int = 10 ** 4
    #: tabela sistemática (não curada; dsl.BASES_SISTEMATICAS) medida nestas bases, D = 2, B único
    alcance_sistematica_bases: Tuple[str, ...] = ("E0", "E0mais")
    #: s_reach com D = profundidade λ do programa (quando > 2), nestas bases, B único
    alcance_D_adequado_bases: Tuple[str, ...] = ("E0", "E0p", "E0mais", "E0pmais")
    #: s_reach com os degraus anteriores (manuais, modo auditoria) na tabela, nestas bases, B único
    alcance_com_anteriores_bases: Tuple[str, ...] = ("E0", "E0mais")
    #: auditoria da poda OE contra amostra independente (teste_int; baterias do ambiente), tabela E0
    auditoria_oe_tipos: Tuple[str, ...] = tuple(tipo_str(t) for t in TIPOS_TAREFA)
    auditoria_oe_s_max: int = 8
    auditoria_oe_s_max_reduzido: int = 7           # para L Pos → L Pos → L Pos (33 415 termos em s = 8)
    auditoria_oe_max_entradas: int = 120
    # fase 4
    verif_bases: Tuple[str, ...] = ("E0", "E0p", "E0mais", "E0pmais")
    verif_aleatorias_por_n: int = 10
    # fase 5
    pm11_grades_aleatorias_por_n: int = 10
    limiar_mecanismo: int = 5
    # fase 6
    tarefas: Tuple[str, ...] = tuple(t.id for t in A.ESCADA)
    bracos: Tuple[Tuple[str, str], ...] = (("L-fix", "E0"), ("L-lib", "E0"), ("L-lib+f", "E0"),
                                          ("L-fix", "E0mais"), ("L-lib", "E0mais"))
    B_tarefa: int = 10_000
    K: int = A.K_RODADAS
    limiar: int = A.LIMIAR_COMPRESSAO
    orcamento_passos: int = A.ORCAMENTO_PASSOS
    k_reservatorio: int = 40
    ns_reservatorio: Tuple[int, ...] = (5, 6)
    num_teste: int = 30
    custo_igual_max: int = 60_000
    pm12_pares: int = 50
    # fase 7 (pré-registrado ANTES desta execução): mínimo de tarefas, POR BASE, com reutilização de
    # abstração descoberta numa solução aceita em que L-fix (mesma base) não resolve a custo total igual
    aut_min_tarefas: int = 1
    # limiares de custo do plano (documento 03, seções 4, 8, 9)
    pm9_s_max: int = 8
    pm9_limiar: float = 2000.0
    i6_limiar: float = 200.0
    pm13_limiar_s: float = 2.0
    i3_limiar_s: float = 10.0
    pm16_tarefas: int = 60
    pm16_B: int = 10 ** 6
    pm16_sementes: int = 5
    pm16_bases: int = 2
    pm16_bracos: int = 10
    pm16_limiar_h: float = 2000.0
    # rótulo
    escala: str = "exploratoria-reduzida"

    def como_dict(self) -> dict:
        """Parâmetros que definem os resultados (sem `processos`/`processos_alcance`, que só mudam a
        execução; memoria_trabalhador_gb FICA: muda onde uma medição limitada por memória para)."""
        d = asdict(self)
        d.pop("processos")
        d.pop("processos_alcance")
        return json.loads(json.dumps(d, ensure_ascii=False))

    def verificar(self) -> None:
        if self.semente not in G.SEMENTES_PILOTO:
            raise ValueError(f"semente {self.semente} fora do intervalo do piloto (10 000 a 19 999)")


def config_mini(semente: int = 10_001) -> ConfigPiloto:
    """Configuração mínima (testes U26/U27): todas as fases, escala de segundos."""
    return ConfigPiloto(
        semente=semente, processos=1, pm1_ns_exaustivo=(1, 2), pm1_ns_amostra=(5,), pm1_amostras_por_n=5,
        pm2_conceitos=("ExistePreta",), pm2_ns=(3,), pm2_k_pares=4, pm6_conceitos=("TopoCheio",), pm6_ns=(3,),
        pm6_amostras=50, degeneracao_conceitos=("ExistePreta",), degeneracao_ns=(1, 2, 3),
        degeneracao_tentativas=10, contagem_s_max=5, contagem_bases=("E0",), alcance_bases=("E0",),
        alcance_orcamentos=(100, 300), alcance_orcamentos_reduzidos=(100,),
        alcance_completos=(("E0", "{g} → Bool"),), alcance_s_max=8, alcance_fechado_B=100, alcance_B_unico=100,
        alcance_fechado_tipos=(tipo_str(FUN(GRADE, BOOL)),), alcance_sistematica_bases=("E0",),
        alcance_D_adequado_bases=(), alcance_com_anteriores_bases=(),
        auditoria_oe_tipos=(tipo_str(FUN(GRADE, BOOL)),), auditoria_oe_s_max=4, auditoria_oe_s_max_reduzido=4,
        auditoria_oe_max_entradas=20, verif_bases=("E0",), verif_aleatorias_por_n=1,
        pm11_grades_aleatorias_por_n=1, tarefas=("ExistePreta", "vizPretos", "pretasDe"),
        bracos=(("L-fix", "E0"), ("L-lib", "E0")), B_tarefa=1500, K=4, k_reservatorio=3, ns_reservatorio=(5,),
        num_teste=3, custo_igual_max=2000, pm12_pares=6, escala="mini-teste")


DESVIOS_ESCALA = [
    "Piloto exploratório com orçamentos reduzidos para caber em poucas horas de CPU (documento 03, seção 8 "
    "previa até ~100 h): PM1 com amostras por n de 5 a 9 reduzidas (documento: 10^5); PM2-PM5 com k pares "
    "reduzido (documento: >= 1000 pares); PM6 com Monte Carlo reduzido; s_reach medido até B = 10^5 "
    "(documento: 10^6) só para os pares (base, contexto) listados em alcance_completos, os demais até 10^4; "
    "execução autônoma com B_tarefa por tarefa (documento: B_max = 10^6) e sem L-mem nem controles.",
    "B_max da regra de decisão (documento 03, seção 10: 10^6) substituído por UM ÚNICO B = alcance_B_unico "
    "(10^4), medido em todos os contextos, tabelas e profundidades da tabela PM10 (antes: o maior B medido "
    "em cada contexto, misturando 10^5 e 10^4 entre degraus). A decisão é tomada a B = 10^4, não a 10^6: "
    "um NO-GO por alcance a 10^4 não implica NO-GO a 10^6.",
    "Memória: a primeira execução completa foi abortada porque um trabalhador da medição de alcance em E0+ "
    "a B = 10^5 passou de 8 GB e foi morto pelo OOM do cgroup. Cada trabalhador tem RLIMIT_AS = "
    "memoria_trabalhador_gb (agora parte da configuração) e roda num processo novo por job "
    "(maxtasksperchild=1). Um MemoryError torna o resultado INCONCLUSIVO: o ponto de parada e os contadores "
    "ao parar vão para medicoes.json (bloco dependente_de_recurso); no determinístico ficam só os s_reach(B) "
    "já determinados e o prefixo do histórico até o maior desses B.",
    "CURADORIA DA TABELA DE PRIMITIVAS (achado de revisão): as instâncias monomórficas de dsl.INSTANCIAS "
    "foram escolhidas com base nos programas da escada (\"o MÍNIMO exigido\"), o que recorta o espaço de "
    "busca com conhecimento das soluções manuais e não vale para F4 nem para o distrator C6. O documento 02, "
    "2.3.2, define primitivas polimórficas. A curadoria é mantida nos braços da fase 6 e nas medições "
    "principais, e o seu efeito é medido: s_reach e PM10 também com dsl.BASES_SISTEMATICAS (critério fixado "
    "sem olhar a escada: elementos em {Pos, L Pos}, valores em {Bool, Pos, L Pos, L (L Pos)}), em "
    "alcance_sistematica_bases, a B único; a diferença está nas colunas 'sistemática' da tabela PM10.",
    "Profundidade λ (achado de revisão): com D = 2 os programas de E0' e E0'+ (profundidade 3 a 6) ficam "
    "fora da gramática para QUALQUER s_reach, o que tornava 'GO com E0' e 'GO com E0+' impossíveis por "
    "construção. A tabela PM10 passa a medir s_reach com D = max(2, profundidade do programa) "
    "(alcance_D_adequado_bases) e separa 'fora da gramática a D = 2' de 'acima de s_reach'. Os aprendizes "
    "da fase 6 continuam com D = 2 (E0, E0+: programas com anteriores têm profundidade ≤ 2, salvo descartar "
    "via dobraR em E0+, profundidade 4).",
    "PM10 com s_reach da tabela BASE é otimista (acrescentar constantes aumenta a ramificação): a coluna "
    "'com anteriores' mede s_reach com os degraus anteriores (manuais, modo auditoria, nunca aprendiz) na "
    "tabela, em alcance_com_anteriores_bases; a decisão principal segue a regra literal do documento 03 "
    "(s_reach da base) e a decisão 'conservadora' usa o menor s_reach medido.",
    "E0'+ só tem s_reach a B único (10^4); 'vale em E0+ e E0'+' é avaliado a esse B.",
    "Livro-razão: busca_candidatos conta só candidatos NO SENTIDO DO PROTOCOLO (documento 03, 2.3); os "
    "candidatos internos do enumerador (poda OE) vão para o campo novo enumeracao_candidatos (e "
    "enumeracao_passos). B_tarefa limita SEPARADAMENTE cada um dos dois (candidatos do protocolo; candidatos "
    "da enumeração, cumulativos na tarefa, inclusive refinamentos OE). A comparação a custo igual usa o "
    "custo TOTAL do aprendiz (total_aprendiz: busca, enumeração, passos, compressão, consultas). Campos "
    "novos do ambiente: oraculo_passos_hipotese, geracao_rotulos.",
    "Poda OE (achado de revisão): os mundos OE da busca são a amostra fixa MAIS as grades dos exemplos e "
    "contraexemplos recebidos (enumerador.EstadoBusca, refinamento com re-enumeração). Contextos aninhados "
    "seguem com os primeiros mundos-raiz e tarefas L Pos → L Pos → · não têm grades: incompletude residual "
    "medida pela auditoria OE da fase 3 (classes perdidas por tamanho).",
    "Oráculos: hipótese indefinida (orçamento de passos esgotado) numa entrada conta como discordância "
    "(sem aceitação vácua).",
]


# =====================================================================
# Utilidades
# =====================================================================
def _cpu() -> float:
    a = resource.getrusage(resource.RUSAGE_SELF)
    b = resource.getrusage(resource.RUSAGE_CHILDREN)
    return a.ru_utime + a.ru_stime + b.ru_utime + b.ru_stime


def _maxrss_principal() -> int:
    """Pico do PROCESSO PRINCIPAL desde o início (ru_maxrss, KiB). Não inclui trabalhadores (cada job
    mede o seu pico isolado num processo novo); nunca é a memória 'da fase'."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def hash_fontes() -> dict:
    """SHA-256 de cada fedro_piloto/*.py (sem testes) e da versão do Python: identifica o código que
    produziu os registros (o pacote pode estar fora do git)."""
    raiz = os.path.dirname(os.path.abspath(__file__))
    arquivos = {}
    for c in sorted(glob.glob(os.path.join(raiz, "*.py"))):
        with open(c, "rb") as f:
            arquivos[os.path.basename(c)] = hashlib.sha256(f.read()).hexdigest()
    total = hashlib.sha256(json.dumps(arquivos, sort_keys=True).encode()).hexdigest()
    return {"arquivos": arquivos, "sha256_total": total, "python": sys.version.split()[0]}


def _executar_jobs(jobs: List[Tuple[Callable, tuple]], processos: int) -> List[dict]:
    """Executa (função, argumentos) em ordem; com processos > 1, num Pool (fork) com
    maxtasksperchild=1: cada job roda num processo NOVO (sem heap de jobs anteriores; memória de pico
    atribuível ao job). Ordem dos resultados preservada."""
    if processos <= 1 or len(jobs) <= 1:
        return [f(*a) for f, a in jobs]
    import multiprocessing as mp
    ctx = mp.get_context("fork")
    with ctx.Pool(min(processos, len(jobs)), maxtasksperchild=1) as pool:
        return pool.starmap(_chamar, [(f, a) for f, a in jobs], chunksize=1)


def _chamar(f, a):
    return f(*a)


def _job(det: dict, med: dict, grades: Optional[Dict[str, List[str]]] = None) -> dict:
    return {"deterministico": det, "medicoes": med, "grades": grades or {}}


def _semente_derivada(semente: int, *partes) -> int:
    h = int(hashlib.sha256(repr((semente,) + partes).encode()).hexdigest()[:8], 16)
    return G.SEMENTES_PILOTO.start + (semente - G.SEMENTES_PILOTO.start + h) % len(G.SEMENTES_PILOTO)


def amostra_nao_confirmatoria(n: int, rng: random.Random, ps: Sequence[float] = G.PS_NATURAL) -> Grade:
    """Amostra natural rejeitando os baldes reservados ao confirmatório (U27)."""
    while True:
        g = G.amostra_natural(n, rng, ps)
        if not G.na_particao(g, G.PARTICAO_CONFIRMATORIA):
            return g


# =====================================================================
# Fase 1: referências e geradores
# =====================================================================
def job_pm1(nomes: Sequence[str], ns_exaustivo, ns_amostra, por_n: int, semente: int) -> dict:
    t0, c0 = time.perf_counter(), time.process_time()
    linhas = []
    for nome in nomes:
        c = REGISTRO[nome]
        exaust, amostr = {}, {}
        for n in ns_exaustivo:
            d = sum(1 for g in todas_as_grades(n) if c.ref_a(g) != c.ref_b(g))
            exaust[n] = {"grades": 2 ** (n * n), "discordancias": d}
        rng = G.rng_piloto(_semente_derivada(semente, "pm1", nome))
        for n in ns_amostra:
            d = 0
            for _ in range(por_n):
                g = amostra_nao_confirmatoria(n, rng)
                d += c.ref_a(g) != c.ref_b(g)
            amostr[n] = {"grades": por_n, "discordancias": d}
        linhas.append({"conceito": nome, "familia": c.familia, "exaustivo": exaust, "amostral": amostr,
                       "discordancias": sum(v["discordancias"] for v in list(exaust.values()) + list(amostr.values()))})
    return _job({"pm1": linhas}, {"tempo_parede_s": time.perf_counter() - t0, "cpu_s": time.process_time() - c0})


def job_pm2(nome: str, n: int, k_pares: int, semente: int) -> dict:
    rng = G.rng_piloto(semente)
    try:
        cj = G.conjunto_de_desenho(REGISTRO[nome], n, "oraculo_treino", k_pares, rng)
    except G.ConceitoDegenerado as e:
        return _job({"conceito": nome, "n": n, "degenerado": True, "motivo": e.info.get("motivo")}, {})
    meta = dict(cj.metadados)
    grades = [g for g, _ in cj.exemplos]
    det = {**meta, "degenerado": False, "contadores": {k: v.como_dict() for k, v in cj.contadores.items()},
           "fora_da_particao": sum(1 for g in grades if not G.na_particao(g, "oraculo_treino")),
           "rotulos_confirmados": all(REGISTRO[nome].rotulo(g) == r for g, r in cj.exemplos)}
    med = cj.medicao.como_dict()
    k = meta["k_pares_obtido"]
    med["pares_por_segundo"] = k / med["tempo_parede_s"] if med["tempo_parede_s"] > 0 else float("nan")
    med["projecao_s_1000_pares"] = 1000 / med["pares_por_segundo"] if med["pares_por_segundo"] > 0 else None
    return _job(det, med, {f"desenho:{nome}:n={n}": [g.serializar() for g in grades]})


def ler_auditoria(caminho: str = CAMINHO_AUDITORIA) -> Dict[str, dict]:
    """{nome: {"metodo": "exata"|"mc", "tabela": {n: {p: freq, "mistura": f}}}} do arquivo de auditoria."""
    out: Dict[str, dict] = {}
    metodo = None
    atual = None
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("## Fórmulas exatas"):
                metodo = "exata"
            elif linha.startswith("## Monte Carlo"):
                metodo = "mc"
            elif linha.startswith("## "):
                metodo = None
            m = re.match(r"^\*\*([^ (*]+)", linha)
            if m and metodo:
                atual = out.setdefault(m.group(1), {"metodo": metodo, "tabela": {}})
                continue
            if atual is not None and linha.startswith("|") and metodo:
                cel = [x.strip() for x in linha.strip("|").split("|")]
                if cel and cel[0].isdigit():
                    vals = [float(x) for x in cel[1:]]
                    atual["tabela"][int(cel[0])] = dict(zip(list(G.PS_NATURAL) + ["mistura"], vals))
    return out


def _frequencia_exata(c, n: int, p: float) -> float:
    """P(c | Bernoulli(p)) exata por enumeração de TODO o domínio de lado n <= 4 (auditoria, como PM1;
    nenhuma grade vira dado). Restringir aos baldes não confirmatórios enviesa domínios pequenos."""
    m = n * n
    rot = G._rotulos_exaustivos(c.nome, n)      # rótulos (ref_a = ref_b verificado) em cache, por grade
    ks = G._dominio(n)[2]
    por_k: Dict[int, int] = {}
    for r, k in zip(rot, ks):
        if r:
            por_k[k] = por_k.get(k, 0) + 1
    return sum(v * p ** k * (1 - p) ** (m - k) for k, v in sorted(por_k.items()))


def job_pm6(nome_aud: str, ns, amostras: int, semente: int, auditoria: dict) -> dict:
    nome = MAPA_AUDITORIA[nome_aud]
    c = REGISTRO[nome]
    aud = auditoria.get(nome_aud)
    rng = G.rng_piloto(_semente_derivada(semente, "pm6", nome))
    linhas = []
    for n in ns:
        ref = (aud or {}).get("tabela", {}).get(n)
        for p in G.PS_NATURAL:
            if n <= G.N_EXAUSTIVO_MAX:
                f, metodo, N = _frequencia_exata(c, n, p), "exata (domínio inteiro)", None
            else:
                pos = sum(c.rotulo(amostra_nao_confirmatoria(n, rng, (p,))) for _ in range(amostras))
                f, metodo, N = pos / amostras, "mc (baldes não confirmatórios)", amostras
            linha = {"conceito": nome, "nome_auditoria": nome_aud, "n": n, "p": p, "amostras": N,
                     "metodo_piloto": metodo, "frequencia": f}
            if ref is not None:
                fa = ref[p]
                # variância sob a hipótese de igualdade (frequência da auditoria): amostragem do piloto + MC da auditoria
                var = (fa * (1 - fa) / N if N else 0.0) + (fa * (1 - fa) / 20000 if aud["metodo"] == "mc" else 0.0)
                dp = var ** 0.5
                tol = 3 * dp + 0.0005 + 1e-9 + (fa * 0.05 if 0 < fa < 0.01 else 0)  # arredondamento a 3 casas / 2 sig.
                linha.update({"auditoria": fa, "metodo_auditoria": aud["metodo"], "dp": dp,
                              "dentro_3dp": abs(f - fa) <= tol})
            linhas.append(linha)
    return _job({"pm6": linhas}, {})


def job_degeneracao(nome: str, ns, tentativas: int, semente: int) -> dict:
    out = []
    for n in ns:
        rng = G.rng_piloto(_semente_derivada(semente, "deg", nome, n))
        d = G.degenerado(REGISTRO[nome], n, "oraculo_treino", rng, tentativas=tentativas)
        out.append({k: d[k] for k in ("conceito", "n", "exaustivo", "positivos_possiveis", "negativos_possiveis",
                                      "negativos_emparelhados_possiveis", "degenerado", "motivo")})
    return _job({"degeneracao": out}, {})


def fase1(cfg: ConfigPiloto) -> dict:
    jobs = []
    nomes = sorted(REGISTRO)
    lotes = [nomes[i::max(1, cfg.processos)] for i in range(max(1, cfg.processos))]
    for lote in lotes:
        if lote:
            jobs.append((job_pm1, (lote, cfg.pm1_ns_exaustivo, cfg.pm1_ns_amostra, cfg.pm1_amostras_por_n, cfg.semente)))
    k_pm1 = len(jobs)
    for nome in cfg.pm2_conceitos:
        for n in cfg.pm2_ns:
            jobs.append((job_pm2, (nome, n, cfg.pm2_k_pares, _semente_derivada(cfg.semente, "pm2", nome, n))))
    k_pm2 = len(jobs)
    aud = ler_auditoria()
    for nome in cfg.pm6_conceitos:
        jobs.append((job_pm6, (nome, cfg.pm6_ns, cfg.pm6_amostras, cfg.semente, aud)))
    k_pm6 = len(jobs)
    for nome in cfg.degeneracao_conceitos:
        jobs.append((job_degeneracao, (nome, cfg.degeneracao_ns, cfg.degeneracao_tentativas, cfg.semente)))
    res = _executar_jobs(jobs, cfg.processos)
    pm1 = sorted([l for r in res[:k_pm1] for l in r["deterministico"]["pm1"]], key=lambda l: l["conceito"])
    pm2 = [r["deterministico"] for r in res[k_pm1:k_pm2]]
    pm6 = [l for r in res[k_pm2:k_pm6] for l in r["deterministico"]["pm6"]]
    deg = [l for r in res[k_pm6:] for l in r["deterministico"]["degeneracao"]]
    grades = {}
    for r in res:
        grades.update(r["grades"])
    det = {"pm1": pm1, "pm1_total_discordancias": sum(l["discordancias"] for l in pm1),
           "pm2_pm5": pm2, "pm6": pm6,
           "pm6_fora_de_3dp": [l for l in pm6 if l.get("dentro_3dp") is False],
           "degeneracao": deg}
    med = {"pm1": [r["medicoes"] for r in res[:k_pm1]],
           "pm3": [{"conceito": d.get("conceito"), "n": d.get("n"), **r["medicoes"]}
                   for d, r in zip(pm2, res[k_pm1:k_pm2])]}
    return {"deterministico": det, "medicoes": med, "grades": grades}


# =====================================================================
# Fase 2: contagem N(s, τ)
# =====================================================================
def fase2(cfg: ConfigPiloto) -> dict:
    out = []
    t0 = time.perf_counter()
    for base in cfg.contagem_bases:
        for nome, (ctx, tau) in CONTEXTOS.items():
            c = contar_termos(BASES[base], tau, ctx, cfg.contagem_s_max)
            razoes = {s: (round(c[s] / c[s - 1], 4) if c.get(s - 1) else None) for s in range(2, cfg.contagem_s_max + 1)}
            out.append({"base": base, "contexto": nome, "contagens": c, "razoes": razoes})
    return {"deterministico": {"pm7": out}, "medicoes": {"tempo_parede_s": time.perf_counter() - t0}, "grades": {}}


# =====================================================================
# Fase 3: alcance
# =====================================================================
def limitar_memoria(gb: Optional[float]) -> None:
    """Limite de espaço de endereçamento (RLIMIT_AS) num processo TRABALHADOR do Pool: um excesso vira
    MemoryError (registrado) em vez de o processo ser morto pelo OOM do cgroup (o que travaria o Pool).
    Nunca aplicado ao processo principal."""
    import multiprocessing as mp
    if gb is None or mp.current_process().name == "MainProcess":
        return
    lim = int(gb * 2 ** 30)
    _, duro = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (lim, duro))


def tabela_alcance(espec: str, base: str):
    """(tabela, auditoria) para a medição de alcance. espec: "curada" (dsl.BASES), "sistematica"
    (dsl.BASES_SISTEMATICAS, não curada) ou "anteriores:<degrau>" (base + degraus MANUAIS anteriores
    como constantes; tabela de uso "referencia", só em modo auditoria, nunca de aprendiz)."""
    if espec == "curada":
        return BASES[base].para_aprendiz(), False
    if espec == "sistematica":
        return BASES_SISTEMATICAS[base].para_aprendiz(), False
    if espec.startswith("anteriores:"):
        degrau = espec.split(":", 1)[1]
        tb = BASES[base]
        ents: list = []
        for p in PR.ESCADA:
            if p.nome == degrau:
                break
            ents.append(entrada_biblioteca(p.nome, PR.termo(p, base), "manual-teste", tb, ents, p.tipo))
        return tb.para_referencia(ents, nome=f"{base}+anteriores-a-{degrau}"), True
    raise ValueError(espec)


def job_alcance(base: str, rotulo: str, contexto: dict, tipo, orcamentos, s_max: int, semente: int,
                memoria_gb: Optional[float] = None, espec: str = "curada", D: int = 2) -> dict:
    """s_reach(B) como enumerador.medir_alcance, com tabela `espec` e profundidade λ D. Um MemoryError
    sob o limite do trabalhador torna INCONCLUSIVOS os B ainda não ultrapassados: no determinístico ficam
    só os s_reach já determinados e o prefixo do histórico até o maior deles; ponto de parada e
    contadores ao parar vão para medicoes (dependente_de_recurso)."""
    from .enumerador import Enumerador, OrcamentoEnumeracaoEsgotado
    from .medidas import medir_isolado
    limitar_memoria(memoria_gb)
    tabela, aud = tabela_alcance(espec, base)
    B = max(orcamentos)
    en = Enumerador(tabela, contexto, tipo, None, orcamento=B, semente=semente, profundidade_lambda=D,
                    auditoria=aud)
    memoria = False
    tempos = []
    with medir_isolado(f"alcance {base} {rotulo} {espec} D={D}") as m:
        t0 = time.perf_counter()
        try:
            for s in range(1, s_max + 1):
                en.representantes(s)
                tempos.append({"s": s, "t_s": time.perf_counter() - t0,
                               "candidatos": en.cont.candidatos_avaliados})
        except OrcamentoEnumeracaoEsgotado:
            en.esgotado = True
        except (MemoryError, SystemError):
            # sob RLIMIT_AS, uma alocação negada dentro do interpretador às vezes aparece como
            # SystemError ("error return without exception set") em vez de MemoryError
            memoria = True
    hist = list(en.historico)
    gasto = en.cont.candidatos_avaliados
    determinados = [b for b in orcamentos if not memoria or b <= gasto]
    s_reach = {str(b): (max([h["s"] for h in hist if h["candidatos_avaliados"] <= b], default=0)
                        if b in determinados else None) for b in orcamentos}
    s_alvo = {str(b): (max([h["s"] for h in hist if h["candidatos_avaliados_alvo"] <= b], default=0)
                       if b in determinados else None) for b in orcamentos}
    r = {"tipo": tipo_str(tipo), "contexto": {nm: tipo_str(t) for nm, t in en.g.gamma0}, "tabela": tabela.nome,
         "tabela_espec": espec, "D": D, "orcamentos": list(orcamentos), "s_reach": s_reach,
         "s_reach_so_alvo": s_alvo, "base": base, "rotulo": rotulo}
    med = {"tempo_parede_s": m.tempo_parede_s, "memoria_pico_kib": m.memoria_pico_kib,
           "memoria_escopo": m.memoria_escopo,
           "candidatos_avaliados_por_segundo": gasto / m.tempo_parede_s if m.tempo_parede_s > 0 else float("nan"),
           "tempos_por_tamanho": tempos}
    if memoria:
        bdet = max(determinados, default=0)
        r.update({"por_tamanho": [h for h in hist if h["candidatos_avaliados"] <= bdet],
                  "s_completo": None, "esgotado": None, "contadores": None, "memoria_logica": None,
                  "nota_recurso": "B sem valor (None) = não determinado por limite de memória do trabalhador; "
                                  "ver medicoes (dependente_de_recurso)"})
        med["dependente_de_recurso"] = {"limitado_por_memoria": True, "limite_memoria_gb": memoria_gb,
                                        "candidatos_ao_parar": gasto, "s_completo_ao_parar": en.s_completo,
                                        "contadores_ao_parar": en.cont.como_dict()}
    else:
        ml = en.memoria_logica()
        r.update({"por_tamanho": hist, "s_completo": en.s_completo, "esgotado": en.esgotado,
                  "contadores": en.cont.como_dict(), "memoria_logica": ml})
        med["bytes_estimados"] = ml["bytes_estimados"]
    return _job(r, med)


# ---------------------------------------------------------------- auditoria da poda OE (achado de revisão)
def _valor_hashable(v):
    if isinstance(v, (tuple, list)):
        return tuple(_valor_hashable(x) for x in v)
    return v


def job_auditoria_oe(tipo_s: str, s_max: int, max_entradas: int, semente: int,
                     memoria_gb: Optional[float] = None) -> dict:
    """Auditoria OE (ver _auditoria_oe); um limite de memória do trabalhador vira registro inconclusivo."""
    limitar_memoria(memoria_gb)
    try:
        return _auditoria_oe(tipo_s, s_max, max_entradas, semente)
    except (MemoryError, SystemError):
        return _job({"tipo": tipo_s, "s_max": s_max, "inconclusivo_recurso": True, "entradas": None,
                     "termos_sem_poda": None, "representantes_oe": None, "classes": None, "perdidas_total": None,
                     "atrasadas_total": None, "por_tamanho": []},
                    {"dependente_de_recurso": {"limitado_por_memoria": True, "limite_memoria_gb": memoria_gb}})


def _auditoria_oe(tipo_s: str, s_max: int, max_entradas: int, semente: int) -> dict:
    """Classes perdidas pela poda OE (amostra de PRODUÇÃO: grades_amostra_oe, oraculo_treino) contra uma
    amostra INDEPENDENTE: entradas do ambiente (baterias da tarefa do tipo) sobre grades de teste_int
    n = 3..6. Classe = denotação nessas entradas. Para cada s: classes cujo tamanho mínimo (sem poda) é
    s; 'perdidas' = sem representante OE de tamanho ≤ s_max com essa denotação; 'atrasadas' =
    representadas só por termo maior que o mínimo. Tabela E0 curada, D = 2 (a do aprendiz)."""
    from .enumerador import Enumerador
    tarefa = A.TAREFAS_POR_ID[TAREFA_DO_TIPO[tipo_s]]
    tb = BASES["E0"].para_aprendiz()
    rng = G.rng_derivado(semente, "auditoria-oe", tipo_s)
    por_n = 6 if tarefa.natureza == "funcao" else -(-max_entradas // 4)   # predicado: 1 entrada por grade
    grades = [G.amostra_natural(n, rng, particao=A.PARTICAO_TESTE) for n in (3, 4, 5, 6) for _ in range(por_n)]
    vistas, entradas = set(), []
    for g in grades:
        for args in A.entradas_da_grade(tarefa, g):
            k = A._chave_entrada(args)
            if k not in vistas:
                vistas.add(k)
                entradas.append(args)
    if len(entradas) > max_entradas:
        idx = sorted(rng.sample(range(len(entradas)), max_entradas))
        entradas = [entradas[i] for i in idx]

    def den(t):
        ev = compilar(t)
        out = []
        for args in entradas:
            c = Contador(20_000)
            try:
                out.append(_valor_hashable(aplicar(ev({}, Contexto(A.n_semantica(tarefa, args), c, tb)), *args)))
            except (OrcamentoEsgotado, RecursionError):
                out.append("⊥")
        return tuple(out)
    t0 = time.perf_counter()
    en = Enumerador(tb, {}, tarefa.tipo, None, semente=semente)
    reps: Dict[tuple, int] = {}
    n_reps = 0
    for t, s in en.enumerar(s_max):
        n_reps += 1
        reps.setdefault(den(t), s)
    classes: Dict[tuple, int] = {}
    n_termos = 0
    for t, s in enumerar_sem_poda(tb, None, tarefa.tipo, s_max):
        n_termos += 1
        d = den(t)
        if d not in classes:
            classes[d] = s
    por = []
    for s in range(1, s_max + 1):
        novas = [d for d, sm in classes.items() if sm == s]
        perdidas = sum(1 for d in novas if d not in reps)
        atrasadas = sum(1 for d in novas if d in reps and reps[d] > s)
        por.append({"s": s, "classes_novas": len(novas), "perdidas": perdidas, "atrasadas": atrasadas,
                    "taxa_perdidas": (perdidas / len(novas)) if novas else None})
    det = {"tipo": tipo_s, "tarefa_bateria": tarefa.id, "s_max": s_max, "entradas": len(entradas),
           "grades_teste_int": len(grades), "hash_grades": G.hash_conjunto(grades),
           "termos_sem_poda": n_termos, "representantes_oe": n_reps, "classes": len(classes),
           "perdidas_total": sum(x["perdidas"] for x in por), "atrasadas_total": sum(x["atrasadas"] for x in por),
           "por_tamanho": por}
    return _job(det, {"tempo_parede_s": time.perf_counter() - t0},
                {f"auditoria_oe:{tipo_s}": [g.serializar() for g in grades]})


# ---------------------------------------------------------------- programas da tabela PM10
def profundidade_lambda(t: Termo) -> int:
    """Maior aninhamento de binders λ como a gramática do enumerador conta (o rec de fix não conta)."""
    k = t[0]
    if k == "lam":
        return 1 + profundidade_lambda(t[3])
    if k == "ap":
        return max(profundidade_lambda(t[1]), profundidade_lambda(t[2]))
    if k == "fix":
        f = t[2]
        return profundidade_lambda(f[3]) if f[0] == "lam" else profundidade_lambda(f)
    return 0


def _binders_topo(t: Termo) -> List[tuple]:
    out = []
    while t[0] == "lam":
        out.append(t[2])
        t = t[3]
    return out


def _sem_binders(t: Termo, k: int) -> Termo:
    for _ in range(k):
        t = t[3]
    return t


def programa_pm10(p, base: str) -> dict:
    """Programa MANUAL do degrau usado como limite superior em PM10. NenhumaIsolada usa a variante
    corrigida (o programa do documento dá verdadeiro na grade vazia; DISCREPANCIAS_DOC)."""
    usado = PR.NENHUMA_ISOLADA_CORRIGIDA if p.nome == "NenhumaIsolada" else p
    t = PR.termo(usado, base)
    bib = PR.biblioteca_manual(base)
    anteriores = {k: v for k, v in bib.items() if list(bib).index(k) < list(bib).index(p.nome)}
    bruto = inline(t, anteriores)
    binders = _binders_topo(t)
    if p.tipo == FUN(GRADE, BOOL):
        rotulo, desconto = "{g} → Bool", 1
    elif p.tipo == FUN(GRADE, LP, LP) and len(binders) >= 2 and binders[:2] == [GRADE, LP]:
        rotulo, desconto = "{g, S: L Pos} → L Pos", 2
    else:
        rotulo, desconto = "fechado " + tipo_str(p.tipo), 0
    prof_ctx = profundidade_lambda(_sem_binders(t, desconto))
    prof_bruto_ctx = profundidade_lambda(_sem_binders(bruto, desconto)) if len(_binders_topo(bruto)) >= desconto else None
    return {"degrau": p.nome, "programa": usado.nome, "termo": t, "bruto": bruto, "tipo": p.tipo,
            "rotulo": rotulo, "desconto": desconto, "tamanho": tamanho(t), "tamanho_bruto": tamanho(bruto),
            "profundidade": profundidade_lambda(t), "profundidade_contexto": prof_ctx,
            "profundidade_bruto_contexto": prof_bruto_ctx, "D_necessario": max(2, prof_ctx)}


def _contexto_de_rotulo(rotulo: str):
    if rotulo in CONTEXTOS:
        return CONTEXTOS[rotulo]
    nome = rotulo[len("fechado "):]
    tau = next(t for t in TIPOS_TAREFA if tipo_str(t) == nome)
    return {}, tau


def planejar_fase3(cfg: ConfigPiloto) -> List[Tuple[tuple, tuple]]:
    """[(chave, argumentos de job_alcance)] em ordem determinística. chave = (classe, base, rotulo, espec, D)."""
    plano = []
    vistos = set()

    def add(classe, base, rotulo, orc, espec="curada", D=2):
        chave = (classe, base, rotulo, espec, D)
        if chave in vistos:
            return
        vistos.add(chave)
        ctx, tau = _contexto_de_rotulo(rotulo)
        plano.append((chave, (base, rotulo, ctx, tau, tuple(orc), cfg.alcance_s_max, cfg.semente,
                              cfg.memoria_trabalhador_gb, espec, D)))
    fechados = [r for r in ("fechado " + t for t in cfg.alcance_fechado_tipos)]
    for base in cfg.alcance_bases:
        for nome in CONTEXTOS:
            orc = cfg.alcance_orcamentos if (base, nome) in cfg.alcance_completos else cfg.alcance_orcamentos_reduzidos
            add("contexto", base, nome, orc)
        for r in fechados:
            add("fechado", base, r, (cfg.alcance_fechado_B,))
    for base in cfg.alcance_sistematica_bases:
        for nome in CONTEXTOS:
            add("contexto", base, nome, (cfg.alcance_B_unico,), "sistematica")
        for r in fechados:
            add("fechado", base, r, (cfg.alcance_B_unico,), "sistematica")
    for base in cfg.alcance_D_adequado_bases:
        for p in PR.ESCADA:
            pr = programa_pm10(p, base)
            if pr["D_necessario"] > 2:
                add("contexto" if pr["desconto"] else "fechado", base, pr["rotulo"], (cfg.alcance_B_unico,),
                    "curada", pr["D_necessario"])
    for base in cfg.alcance_com_anteriores_bases:
        for p in PR.ESCADA[1:]:
            pr = programa_pm10(p, base)
            add("contexto" if pr["desconto"] else "fechado", base, pr["rotulo"], (cfg.alcance_B_unico,),
                f"anteriores:{p.nome}", pr["D_necessario"])
    return plano


def fase3(cfg: ConfigPiloto) -> dict:
    plano = planejar_fase3(cfg)
    jobs = [(job_alcance, args) for _, args in plano]
    for t in cfg.auditoria_oe_tipos:
        s_aud = cfg.auditoria_oe_s_max_reduzido if t == tipo_str(FUN(LP, LP, LP)) else cfg.auditoria_oe_s_max
        jobs.append((job_auditoria_oe, (t, s_aud, cfg.auditoria_oe_max_entradas, cfg.semente,
                                        cfg.memoria_trabalhador_gb)))
    custo = lambda j: (-max(j[1][4]) * (2 if j[1][0] in ("E0mais", "E0p") else 1) if j[0] is job_alcance
                       else -10 ** 5)
    ordem = sorted(range(len(jobs)), key=lambda i: custo(jobs[i]))   # os mais caros primeiro
    res_ord = _executar_jobs([jobs[i] for i in ordem], min(cfg.processos, cfg.processos_alcance))
    res = [None] * len(jobs)
    for i, r in zip(ordem, res_ord):
        res[i] = r
    det, med, aud, med_aud, grades = [], [], [], [], {}
    for (classe, base, rotulo, espec, D), r in zip([c for c, _ in plano], res[:len(plano)]):
        d = r["deterministico"]
        d["classe"] = classe
        det.append(d)
        med.append({**r["medicoes"], "classe": classe, "base": base, "rotulo": rotulo, "tabela_espec": espec, "D": D})
    for r in res[len(plano):]:
        aud.append(r["deterministico"])
        med_aud.append({"tipo": r["deterministico"]["tipo"], **r["medicoes"]})
        grades.update(r["grades"])
    grades["oe:grades_amostra_oe"] = [g.serializar() for g in grades_amostra_oe(cfg.semente)]
    return {"deterministico": {"pm8": det, "auditoria_oe": aud}, "medicoes": {"pm8_pm9": med, "auditoria_oe": med_aud},
            "grades": grades}


def s_reach_de(pm8: List[dict], base: str, rotulo: str, B: Optional[int] = None, espec: str = "curada",
               D: int = 2) -> Tuple[Optional[int], Optional[int]]:
    """(s_reach, B) para (base, rótulo, tabela, D); B = maior B DETERMINADO se None."""
    for d in pm8:
        if (d["base"] == base and d["rotulo"] == rotulo and d.get("tabela_espec", "curada") == espec
                and d.get("D", 2) == D):
            bs = sorted((int(b) for b, v in d["s_reach"].items() if v is not None), reverse=True)
            if B is not None:
                bs = [b for b in bs if b == B]
            if bs:
                return d["s_reach"][str(bs[0])], bs[0]
    return None, None


# =====================================================================
# Fase 4: viabilidade da escada e verificação dos programas manuais
# =====================================================================
def _grades_verificacao(cfg: ConfigPiloto, base: str) -> List[Grade]:
    ns = (1, 2, 3) if base in ("E0", "E0mais") else (1, 2)
    gs = [g for n in ns for g in todas_as_grades(n) if not G.na_particao(g, G.PARTICAO_CONFIRMATORIA)]
    rng = G.rng_piloto(_semente_derivada(cfg.semente, "verif", base))
    extra_ns = (3, 4, 5, 6) if base not in ("E0", "E0mais") else (4, 5, 6)
    for n in extra_ns:
        gs += [amostra_nao_confirmatoria(n, rng) for _ in range(cfg.verif_aleatorias_por_n)]
    return gs


def job_verificar_programas(base: str, cfg: ConfigPiloto) -> dict:
    """Programas MANUAIS (manual-teste) da escada e a variante corrigida de NenhumaIsolada, avaliados com
    tabela de uso 'referencia', contra as referências do ambiente nas mesmas baterias de entradas que o
    aprendiz enfrenta."""
    tb = PR.tabela_referencia(base)
    assert tb.uso == "referencia"
    gs = _grades_verificacao(cfg, base)
    programas = [(p.nome, p.nome, C(p.nome), p.proveniencia) for p in PR.ESCADA]
    nic = PR.NENHUMA_ISOLADA_CORRIGIDA
    programas.append((nic.nome, "NenhumaIsolada", PR.termo(nic, base), nic.proveniencia))
    linhas = []
    for nome, tarefa_id, termo, prov in programas:
        tarefa = A.TAREFAS_POR_ID[tarefa_id]
        valores = {}
        erros, verificadas = [], 0
        excecoes = documentadas = 0
        for g in gs:
            for args in A.entradas_da_grade(tarefa, g):
                n = A.n_semantica(tarefa, args)
                if n not in valores:
                    valores[n] = avaliar(termo, {}, n, None, tb)
                try:
                    v = aplicar(valores[n], *args)
                except RecursionError:
                    excecoes += 1
                    continue
                verificadas += 1
                if not (v == A.saida_referencia(tarefa, args)):
                    if nome == "NenhumaIsolada" and args[0].contagem_pretas() == 0:
                        documentadas += 1   # PR.DISCREPANCIAS_DOC[("NenhumaIsolada", "semantica")]
                    else:
                        erros.append(A.valor_json(args))
        linhas.append({"programa": nome, "tarefa": tarefa_id, "base": base, "proveniencia": prov,
                       "verificadas": verificadas, "discordancias": len(erros),
                       "primeiras_discordancias": erros[:3], "excecoes": excecoes,
                       "discordancias_documentadas": documentadas,
                       "nota": "grade sem pretas: programa do documento dá verdadeiro, referência falso "
                               "(DISCREPANCIAS_DOC)" if documentadas else ""})
    return _job({"verificacao": linhas}, {})


def tabela_pm10(pm8: List[dict], bases=("E0", "E0p", "E0mais", "E0pmais"), B: Optional[int] = None,
                verificacao: Optional[List[dict]] = None) -> List[dict]:
    """Para cada degrau e base: tamanho do programa manual com os degraus anteriores (limite superior),
    profundidade λ no contexto medido, e s_reach a UM ÚNICO B em quatro leituras:
      D2 (tabela curada, D = 2: a gramática do aprendiz); D (curada, D = max(2, profundidade));
      sistemática (tabela não curada, D = 2); com anteriores (degraus anteriores na tabela, D).
    alcancavel (regra do documento 03): tamanho − desconto ≤ s_reach(D adequado); None se não medido
    ou se o programa manual tem discordância com a referência (limite inválido). 'fora da gramática a
    D = 2' é separado de 'acima de s_reach'. B None = maior B determinado em cada contexto (legado)."""
    verif = {(v["programa"], v["base"]): v for v in (verificacao or [])}
    linhas = []
    for base in bases:
        for p in PR.ESCADA:
            pr = programa_pm10(p, base)
            desc, s_lib = pr["desconto"], pr["tamanho"]
            D = pr["D_necessario"]
            v = verif.get((pr["programa"], base))
            disc = None if v is None else v["discordancias"] + v["discordancias_documentadas"]
            invalido = bool(disc)
            sr2, B2 = s_reach_de(pm8, base, pr["rotulo"], B, "curada", 2)
            srD, BD = s_reach_de(pm8, base, pr["rotulo"], B, "curada", D)
            srS, _ = s_reach_de(pm8, base, pr["rotulo"], B, "sistematica", 2)
            srA, _ = s_reach_de(pm8, base, pr["rotulo"], B, f"anteriores:{p.nome}", D)
            alvo = s_lib - desc

            def ok(sr, exige_D2=False):
                if sr is None or invalido:
                    return None
                if exige_D2 and pr["profundidade_contexto"] > 2:
                    return False
                return alvo <= sr
            alc = ok(srD)
            medidos = [x for x in (srD, srA, srS if pr["profundidade_contexto"] <= 2 else None) if x is not None]
            conservador = None if (invalido or srD is None) else alvo <= min(medidos)
            if invalido:
                motivo = "limite inválido (programa manual discorda da referência)"
            elif srD is None:
                motivo = "s_reach não medido"
            elif alc:
                motivo = "alcançável"
            else:
                motivo = "acima de s_reach"
            linhas.append({
                "degrau": p.nome, "base": base, "tipo": tipo_str(p.tipo), "programa": pr["programa"],
                "proveniencia_programa": PR.PROVENIENCIA, "discordancias_programa": disc, "limite_invalido": invalido,
                "tamanho_com_anteriores": s_lib, "tamanho_bruto": pr["tamanho_bruto"],
                "profundidade_lambda": pr["profundidade"], "profundidade_contexto": pr["profundidade_contexto"],
                "profundidade_bruto_contexto": pr["profundidade_bruto_contexto"],
                "D_necessario": D, "fora_da_gramatica_D2": pr["profundidade_contexto"] > 2,
                "fonte_s_reach": pr["rotulo"], "desconto_binders": desc, "B": BD if BD is not None else B2,
                "s_reach_D2": sr2, "s_reach_D": srD, "s_reach_sistematica": srS, "s_reach_com_anteriores": srA,
                "alcancavel_com_anteriores": alc, "alcancavel_aprendiz_D2": ok(sr2, exige_D2=True),
                "alcancavel_sistematica": ok(srS, exige_D2=True), "alcancavel_tabela_com_anteriores": ok(srA),
                "alcancavel_conservador": conservador,
                "alcancavel_bruto": (None if sr2 is None or invalido or pr["profundidade_bruto_contexto"] is None
                                     or pr["profundidade_bruto_contexto"] > 2
                                     else pr["tamanho_bruto"] - desc <= sr2),
                "motivo": motivo})
    return linhas


def fase4(cfg: ConfigPiloto, pm8: List[dict]) -> dict:
    res = _executar_jobs([(job_verificar_programas, (b, cfg)) for b in cfg.verif_bases], cfg.processos)
    verif = [l for r in res for l in r["deterministico"]["verificacao"]]
    pm10 = tabela_pm10(pm8, B=cfg.alcance_B_unico, verificacao=verif)
    return {"deterministico": {"verificacao_programas_manuais": verif, "pm10": pm10,
                               "B_unico": cfg.alcance_B_unico}, "medicoes": {}, "grades": {}}


# =====================================================================
# Fase 5: MECANISMO (mecanismo-teste) — soluções MANUAIS, nunca descoberta
# =====================================================================
ALVOS_PM11 = {
    # alvo: soluções manuais (brutas, com a biblioteca manual inlined) de onde extrair
    "vizPretos": ("ParAdjacente", "NenhumaIsolada"),
    "passo": ("fecho",),
    "pretasDe": ("PrimeiraUltimaIguais", "LinhasIguais"),
}


def _permutacao_para(tipo_f, tipo_alvo) -> Optional[Tuple[int, ...]]:
    """perm tal que alvo(x_0..x_{k-1}) = f(x_perm[0], ...), se os tipos de argumento forem uma permutação
    dos do alvo com o mesmo resultado (identidade preferida); senão None."""
    import itertools
    from .dsl import argumentos_e_resultado
    af, rf = argumentos_e_resultado(tipo_f)
    aa, ra = argumentos_e_resultado(tipo_alvo)
    if rf != ra or sorted(map(repr, af)) != sorted(map(repr, aa)) or len(af) > 4:
        return None
    for perm in itertools.permutations(range(len(aa))):
        if all(af[i] == aa[perm[i]] for i in range(len(af))):
            return tuple(perm)
    return None


def _reordenar(termo: Termo, tipo_f, perm) -> Termo:
    """λx_0..x_{k-1} (tipos do alvo). termo x_perm[0] ... x_perm[k-1]; identidade devolve o termo."""
    from .dsl import AP, LAMS, V, argumentos_e_resultado
    if list(perm) == sorted(perm):
        return termo
    af, _ = argumentos_e_resultado(tipo_f)
    tipos_alvo = [None] * len(af)
    for i, j in enumerate(perm):
        tipos_alvo[j] = af[i]
    nomes = [f"_a{j}" for j in range(len(af))]
    return LAMS(list(zip(nomes, tipos_alvo)), AP(termo, *[V(nomes[perm[i]]) for i in range(len(af))]))


def _grades_pm11(cfg: ConfigPiloto) -> List[Grade]:
    gs = [g for n in (1, 2, 3) for g in G.grades_da_particao(n, "oraculo_treino")]
    rng = G.rng_piloto(_semente_derivada(cfg.semente, "pm11"))
    for n in (4, 5, 6):
        gs += [G.amostra_natural(n, rng, particao="oraculo_treino") for _ in range(cfg.pm11_grades_aleatorias_por_n)]
    return gs


def fase5(cfg: ConfigPiloto) -> dict:
    lib = PR.biblioteca_manual("E0")
    gs = _grades_pm11(cfg)
    linhas = []
    for alvo, fontes in ALVOS_PM11.items():
        sols = []
        for f in fontes:
            ant = {k: v for k, v in lib.items() if list(lib).index(k) < list(lib).index(f)}
            sols.append(Solucao(inline(PR.termo(PR.POR_NOME[f]), ant), f, PROVENIENCIA_FASE5))
        frags = extrair_fragmentos(sols)
        pa = PR.POR_NOME[alvo]
        alvo_t = PR.termo(pa)
        igual = (lambda a, b: frozenset(a) == frozenset(b)) if alvo == "passo" else None
        ref = PR.tabela_referencia("E0")   # o alvo manual usa os degraus anteriores como constantes
        cands = []
        for f in frags:
            perm = _permutacao_para(f.tipo, pa.tipo)
            if perm is not None:
                cands.append((f, perm))
        iguais = []
        for f, perm in cands:
            disc = comparar_denotacoes(_reordenar(f.termo_fechado, f.tipo, perm), alvo_t, pa.tipo, gs, tabela2=ref,
                                       max_combinacoes=40, igual=igual)
            if not disc:
                iguais.append((f, perm))
        # compressão gulosa no modo mecanismo-teste (tabela de uso "referencia")
        bib = Biblioteca(BASES["E0"], "mecanismo-teste")
        novas = bib.comprimir(sols, limiar=cfg.limiar_mecanismo)
        assert bib.tabela.uso == "referencia" and all(p.proveniencia == "manual-teste" for p in novas)
        gulosa_igual = []
        for p in novas:
            perm = _permutacao_para(p.tipo, pa.tipo)
            if perm is not None and not comparar_denotacoes(_reordenar(C(p.nome), p.tipo, perm), alvo_t, pa.tipo, gs,
                                                            tabela1=bib.tabela, tabela2=ref, max_combinacoes=40,
                                                            igual=igual):
                gulosa_igual.append({"nome": p.nome, "permutacao_argumentos": list(perm)})
        linhas.append({
            "alvo": alvo, "modo": "mecanismo-teste", "proveniencia": PROVENIENCIA_FASE5,
            "solucoes_fonte": list(fontes), "fragmentos": len(frags), "fragmentos_do_tipo": len(cands),
            # PM11 (achado de revisão): extraído = a compressão GULOSA (o mecanismo real de L-lib) insere
            # uma entrada comportamentalmente igual ao alvo; a presença no ranking é só diagnóstico
            "extraido": bool(gulosa_igual),
            "presente_no_ranking": bool(iguais),
            "fragmento_igual": iguais[0][0].como_dict() if iguais else None,
            "permutacao_argumentos": list(iguais[0][1]) if iguais else None,
            "igual_sem_permutar": bool(iguais) and list(iguais[0][1]) == sorted(iguais[0][1]),
            "posicao_no_ranking": (frags.index(iguais[0][0]) + 1) if iguais else None,
            "melhor_fragmento": frags[0].como_dict() if frags else None,
            "entradas_compressao_gulosa": [{"nome": p.nome, "legivel": imprimir_legivel(p.corpo),
                                            "tipo": tipo_str(p.tipo), "proveniencia": p.proveniencia}
                                           for p in novas],
            "gulosa_contem_alvo": gulosa_igual,
            "grades_comparacao": len(gs)})
    pm11 = sum(l["extraido"] for l in linhas) / len(linhas)
    presente = sum(l["presente_no_ranking"] for l in linhas) / len(linhas)
    viz = next((l for l in linhas if l["alvo"] == "vizPretos"), None)
    return {"deterministico": {"aviso": "MECANISMO com soluções MANUAIS (manual-teste); nada aqui é descoberta",
                               "pm11": linhas, "pm11_fracao": pm11,
                               "pm11_definicao": "fração de alvos que a compressão GULOSA (Biblioteca.comprimir) "
                                                 "insere como entrada comportamentalmente igual ao alvo",
                               "alvo_presente_no_ranking_fracao": presente,
                               "I4_disparada": (not viz["extraido"]) if viz is not None else None},
            "medicoes": {}, "grades": {"pm11:grades": [g.serializar() for g in gs]}}


# =====================================================================
# Fase 6: execução autônoma
# =====================================================================
def _criar_aprendiz(nome: str, base: str, livro: LivroRazao, cfg: ConfigPiloto, B: Optional[int] = None,
                    sufixo: str = ""):
    kw = dict(B=B or cfg.B_tarefa, K=cfg.K, orcamento_passos=cfg.orcamento_passos,
              kw_enumerador={"semente": cfg.semente})
    tab = BASES[base]
    rot = base + sufixo
    if nome == "L-fix":
        return A.LFix(tab, livro, rotulo_base=rot, **kw)
    if nome == "L-lib":
        return A.LLib(tab, livro, limiar=cfg.limiar, rotulo_base=rot, **kw)
    if nome == "L-lib+f":
        return A.LLib(tab, livro, limiar=cfg.limiar, promover_funcoes=True, rotulo_base=rot, **kw)
    raise ValueError(nome)


def _ambiente(cfg: ConfigPiloto) -> A.Ambiente:
    return A.Ambiente(cfg.semente, k_reservatorio=cfg.k_reservatorio, ns_reservatorio=cfg.ns_reservatorio,
                      num_teste=cfg.num_teste)


def job_braco(nome: str, base: str, cfg: ConfigPiloto, tarefas: Sequence[str], B: Optional[int] = None,
              sufixo: str = "") -> dict:
    from .medidas import medir_isolado
    limitar_memoria(cfg.memoria_trabalhador_gb)
    amb = _ambiente(cfg)
    livro = LivroRazao(cfg.semente, {"braco": f"{nome}@{base}{sufixo}"})
    ap = _criar_aprendiz(nome, base, livro, cfg, B, sufixo)
    c0 = time.process_time()
    with medir_isolado(f"{nome}@{base}{sufixo}") as m:
        for tid in tarefas:
            ap.resolver(A.TAREFAS_POR_ID[tid], amb)
    rel = ap.relatorio()
    grades: Dict[str, List[str]] = {}
    preparos = []
    for tid in tarefas:
        p = amb.preparar(A.TAREFAS_POR_ID[tid])
        preparos.append(p.como_dict())
        for k, v in p.grades().items():
            grades[f"tarefa:{tid}:{k}"] = sorted({g.serializar() for g in v})
    for r in ap.resultados:
        for h in r.hipoteses:
            ce = h["contraexemplo"]
            if ce:
                ent = ce["entrada"]
                for x in (ent if isinstance(ent, list) else [ent]):
                    if isinstance(x, str) and ":" in x:
                        grades.setdefault(f"contraexemplos:{nome}@{base}{sufixo}", []).append(x)
    grades["oe:grades_amostra_oe"] = [g.serializar() for g in grades_amostra_oe(cfg.semente)]
    det = {"relatorio": rel, "abstracoes": A.abstracoes(ap), "preparos": preparos,
           "livro": livro.deterministico_dict(incluir_diario=True),
           "dependente_de_recurso": any(r.inconclusivo_recurso for r in ap.resultados)}
    lat = [x for mo in ap.medicoes_oraculo for x in mo["latencias_s"]]
    med = {"livro": livro.medicoes_dict(), "tempo_parede_s": m.tempo_parede_s, "cpu_s": time.process_time() - c0,
           "memoria_pico_kib": m.memoria_pico_kib, "memoria_escopo": m.memoria_escopo,
           "oraculo_latencias_por_tarefa": ap.medicoes_oraculo,
           "oraculo_latencia_max_s": max(lat, default=0.0),
           "oraculo_latencia_media_s": (sum(lat) / len(lat)) if lat else None, "oraculo_consultas": len(lat)}
    return _job(det, med, grades)


def job_pm12(pares: int, semente: int, memoria_gb: Optional[float] = None) -> dict:
    """PM12 (documento 03, seção 4; U23): minimalidade do oráculo contra força bruta em n ≤ 4, para
    `pares` pares (h, c): h = termo aleatório de tamanho ≤ 6 em Grade → Bool (E0), c ∈ F1 ∪ F2.
    Latência por consulta (PM13) vai para as medições."""
    from .oraculo import Oraculo, contraexemplo_forca_bruta
    limitar_memoria(memoria_gb)
    rng = G.rng_derivado(semente, "pm12")
    termos = [t for t, _s in enumerar_sem_poda(BASES["E0"].para_aprendiz(), None, FUN(GRADE, BOOL), 6)]
    familias = sorted(n for n, c in REGISTRO.items() if c.familia in ("F1", "F2"))
    oraculos: Dict[str, object] = {}
    iguais, com_resposta, falhas, lat = 0, 0, [], []
    for _ in range(pares):
        t, c = rng.choice(termos), rng.choice(familias)
        o = oraculos.get(c)
        if o is None:
            o = oraculos[c] = Oraculo(c, "oraculo_treino", ns_reservatorio=())

        def h(g, t=t):
            return aplicar(avaliar(t, n=g.n, orcamento_passos=20_000), g)
        ordem = [n for _f, n in o.ordem_busca]
        r_or = o.contraexemplo(h)
        lat.append(o.medicao.latencias_s[-1])
        r_fb = contraexemplo_forca_bruta(h, c, n_max=4, particao="oraculo_treino", ns=ordem)
        if r_or == r_fb:
            iguais += 1
        else:
            falhas.append({"h": imprimir(t), "conceito": c})
        com_resposta += r_or is not None
    det = {"pares": pares, "iguais_forca_bruta": iguais, "com_contraexemplo": com_resposta,
           "falhas": falhas[:5], "limiar": f"{pares}/{pares}", "ok": iguais == pares}
    return _job(det, {"latencias_s": lat, "latencia_max_s": max(lat, default=0.0)})


def _custos_cumulativos(resultados: List[dict], livro_det: dict) -> List[dict]:
    """Por tarefa, em ordem: custo TOTAL do aprendiz (total_aprendiz: busca, enumeração OE, passos,
    compressão, consultas) e, como métricas secundárias, candidatos do protocolo e da enumeração."""
    por = {(e["tarefa_id"]): e for e in livro_det["entradas"]}
    cum = cum_c = cum_e = 0
    out = []
    for r in resultados:
        e = por[r["tarefa_id"]]
        cum += e["total_aprendiz"]
        cum_c += e["busca_candidatos"]
        cum_e += e["enumeracao_candidatos"]
        out.append({"tarefa": r["tarefa_id"], "aceita": r["aceita"],
                    "inconclusivo_recurso": r.get("inconclusivo_recurso", False),
                    "custo_aprendiz": e["total_aprendiz"], "candidatos": e["busca_candidatos"],
                    "enumeracao": e["enumeracao_candidatos"], "cumulativo": cum, "cumulativo_candidatos": cum_c,
                    "cumulativo_enumeracao": cum_e})
    return out


def comparar_custo_igual(cfg: ConfigPiloto, bracos: Dict[str, dict], livro: Optional[LivroRazao] = None,
                         grades: Optional[Dict[str, List[str]]] = None) -> List[dict]:
    """Para cada reutilização de abstração descoberta numa solução aceita de L-lib*, verifica se L-fix
    (mesma base) resolve a tarefa ao mesmo custo cumulativo TOTAL do aprendiz (documento 02, 2.5: custo
    anterior nunca afundado; compressão incluída). Métrica primária: total_aprendiz; candidatos ficam
    como secundária. Se L-fix falhou no B_tarefa gastando MENOS que o custo igual, roda-se L-fix nessa
    tarefa (L-fix não tem estado entre tarefas) com até custo_igual_max candidatos e julga-se pelo custo
    total gasto: aceita com custo ≤ orçamento → True; aceita acima, ou falha tendo gasto ≥ orçamento →
    False; falha antes disso → None (inconclusivo). MemoryError → None. As execuções extras entram no
    livro-razão global (aprendiz '<L-fix@base>#custo-igual') e nas grades."""
    out = []
    for chave, d in bracos.items():
        nome, base = chave.split("@")
        if not nome.startswith("L-lib"):
            continue
        fix = bracos.get(f"L-fix@{base}")
        if fix is None:
            continue
        cl, cf = d["curva"], fix["curva"]
        for i, r in enumerate(d["relatorio"]["resultados"]):
            if not (r["aceita"] and r["reutilizacoes"]):
                continue
            tid = r["tarefa_id"]
            c_lib = cl[i]["cumulativo"]
            j = next(k for k, x in enumerate(cf) if x["tarefa"] == tid)
            c_fix_antes = cf[j - 1]["cumulativo"] if j > 0 else 0
            orc = c_lib - c_fix_antes
            item = {"braco": chave, "base": base, "tarefa": tid, "abstracoes_reutilizadas": r["reutilizacoes"],
                    "metrica_primaria": "total_aprendiz",
                    "cumulativo_lib": c_lib, "cumulativo_fix_antes": c_fix_antes, "orcamento_custo_igual": orc,
                    "secundaria_cumulativo_candidatos_lib": cl[i]["cumulativo_candidatos"],
                    "secundaria_cumulativo_candidatos_fix": cf[j]["cumulativo_candidatos"],
                    "lfix_aceitou_no_B": cf[j]["aceita"],
                    "lfix_cumulativo_ao_aceitar": cf[j]["cumulativo"] if cf[j]["aceita"] else None}
            if cf[j]["inconclusivo_recurso"]:
                item["lfix_resolve_a_custo_igual"] = None
                item["metodo"] = "L-fix parou por limite de memória: inconclusivo"
            elif cf[j]["aceita"]:
                item["lfix_resolve_a_custo_igual"] = cf[j]["cumulativo"] <= c_lib
                item["metodo"] = "execucao principal"
            elif cf[j]["custo_aprendiz"] >= orc:
                item["lfix_resolve_a_custo_igual"] = False
                item["metodo"] = "L-fix falhou tendo gasto custo total ≥ orçamento de custo igual"
            else:
                rr = job_braco("L-fix", base, cfg, [tid], B=cfg.custo_igual_max, sufixo="#custo-igual")
                rx = rr["deterministico"]["relatorio"]["resultados"][0]
                ex = rr["deterministico"]["livro"]["entradas"][0]
                gasto = ex["total_aprendiz"]
                if rx.get("inconclusivo_recurso"):
                    v = None
                elif rx["aceita"]:
                    v = gasto <= orc
                else:
                    v = False if gasto >= orc else None
                item["lfix_resolve_a_custo_igual"] = v
                item["metodo"] = (f"execucao extra de L-fix com até {cfg.custo_igual_max} candidatos, julgada pelo "
                                  f"custo total ({gasto} contra orçamento {orc})")
                item["execucao_extra"] = {"aceita": rx["aceita"], "hipotese": rx["hipotese_legivel"],
                                          "motivo_fim": rx["motivo_fim"], "custo_total_aprendiz": gasto,
                                          "contador_busca": rx["contador_busca"]}
                if livro is not None:
                    ld = rr["deterministico"]["livro"]
                    for e in ld["entradas"]:
                        livro.entrada(e["tarefa_id"], e["aprendiz_id"])
                    for l in ld["diario"]:
                        livro.registrar(l["tarefa_id"], l["aprendiz_id"], l["campo"], l["quantidade"], l.get("nota", ""))
                if grades is not None:
                    grades.update(rr["grades"])
            out.append(item)
    return out


def conciliar_livro(bracos: Dict[str, dict]) -> dict:
    """PM14 (achado de revisão): confere cada entrada do livro-razão contra contadores INDEPENDENTES do
    diário: ContadorBusca (candidatos, enumeração, passos), contadores do oráculo (consultas, entradas
    examinadas), ContadorCompressao da tarefa e contadores de geração do preparo. diferenca = soma dos
    |livro − contador|; oraculo_passos_hipotese e geracao_rotulos não têm contador independente."""
    linhas, dif_total = [], 0
    for chave, d in bracos.items():
        entradas = {e["tarefa_id"]: e for e in d["livro_entradas"]}
        preparos = {p["tarefa"]: p for p in d["preparos"]}
        for r in d["relatorio"]["resultados"]:
            e = entradas[r["tarefa_id"]]
            cb, oc = r["contador_busca"], r["oraculo"]["contador"]
            exam = oc.get("entradas_examinadas", oc.get("grades_examinadas", 0))
            pp = preparos.get(r["tarefa_id"], {})
            pares = {
                "busca_candidatos": cb["candidatos_avaliados"],
                "enumeracao_candidatos": cb["enumeracao_candidatos_avaliados"],
                "busca_passos": cb["passos_avaliacao"], "enumeracao_passos": cb["enumeracao_passos"],
                "oraculo_consultas": oc["consultas_contraexemplo"] + oc.get("consultas_rotulo", 0),
                "oraculo_custo_ambiente": exam + oc.get("consultas_rotulo", 0),
                "compressao_subtermos": r.get("compressao_subtermos", 0),
                "geracao_grades": pp.get("grades_geradas", 0) + pp.get("geracao_reservatorios", 0),
                "avaliacao_passos": None}
            for campo, indep in pares.items():
                if indep is None:
                    continue
                dif = abs(e[campo] - indep)
                dif_total += dif
                if dif:
                    linhas.append({"braco": chave, "tarefa": r["tarefa_id"], "campo": campo, "livro": e[campo],
                                   "contador_independente": indep})
    return {"diferenca": dif_total, "divergencias": linhas[:50], "num_divergencias": len(linhas),
            "campos_sem_contador_independente": ["oraculo_passos_hipotese", "geracao_rotulos", "avaliacao_passos"]}


def fase6(cfg: ConfigPiloto) -> dict:
    jobs = [(job_braco, (nome, base, cfg, cfg.tarefas)) for nome, base in cfg.bracos]
    jobs.append((job_pm12, (cfg.pm12_pares, cfg.semente, cfg.memoria_trabalhador_gb)))
    res = _executar_jobs(jobs, cfg.processos)
    r_pm12 = res.pop()
    livro = LivroRazao(cfg.semente, {"tipo": "execucao autonoma do piloto", "escala": cfg.escala,
                                     "bracos": [f"{n}@{b}" for n, b in cfg.bracos]})
    bracos: Dict[str, dict] = {}
    med_bracos = {}
    grades: Dict[str, List[str]] = {}
    for (nome, base), r in zip(cfg.bracos, res):
        chave = f"{nome}@{base}"
        det = r["deterministico"]
        ld = det["livro"]
        for e in ld["entradas"]:
            livro.entrada(e["tarefa_id"], e["aprendiz_id"])
        for l in ld["diario"]:
            livro.registrar(l["tarefa_id"], l["aprendiz_id"], l["campo"], l["quantidade"], l.get("nota", ""))
        for m in r["medicoes"]["livro"]["por_entrada"]:
            livro.medicoes[(m["tarefa_id"], m["aprendiz_id"])] = MedicaoRazao(m["tempo_parede_s"], m["memoria_pico_kb"])
        det["curva"] = _custos_cumulativos(det["relatorio"]["resultados"], ld)
        det["livro_entradas"] = ld["entradas"]
        del det["livro"]
        bracos[chave] = det
        med_bracos[chave] = {k: v for k, v in r["medicoes"].items() if k != "livro"}
        grades.update(r["grades"])
    custo_igual = comparar_custo_igual(cfg, bracos, livro, grades)
    conc = conciliar_livro(bracos)
    for d in bracos.values():
        del d["livro_entradas"]
    fech = livro.verificar_fechamento()
    det = {"bracos": bracos, "custo_igual": custo_igual,
           "fechamento": {"ok": fech.ok, "diferenca": fech.diferenca, "problemas": fech.problemas,
                          "nota": "soma das partes = total (aritmética do livro)"},
           "pm14_conciliacao": conc, "pm12": r_pm12["deterministico"],
           "livro_total_por_aprendiz": livro.total_por_aprendiz(), "hash_diario": livro.hash_diario()}
    return {"deterministico": det, "medicoes": {"bracos": med_bracos, "pm12": r_pm12["medicoes"]},
            "grades": grades, "livro": livro}


# =====================================================================
# Fase 7: decisão
# =====================================================================
def decidir(pm10: List[dict], f6: Optional[dict], f5: Optional[dict] = None, aut_min_tarefas: int = 1,
            outras: Optional[dict] = None) -> dict:
    """Regra do documento 03, seção 10 (alcance pela tabela PM10, D adequado, B único) + exigência
    autônoma POR BASE: GO com E0 exige, em L-lib@E0, ≥ aut_min_tarefas tarefas com reutilização de
    abstração descoberta numa solução aceita em que L-fix@E0 não resolve a custo total igual (E0' não tem
    braço nesta escala: não verificado); GO com E0+ exige o mesmo em L-lib@E0mais. Também: decisão
    conservadora (menor s_reach medido), I4 (fase 5) e as interrupções verificáveis com dados
    determinísticos (I1, I7); I3/I6/PM16 dependem de medições e ficam em decidir_custo (medicoes)."""
    def todos(base, campo="alcancavel_com_anteriores"):
        ls = [l for l in pm10 if l["base"] == base]
        if not ls or any(l[campo] is None for l in ls):
            return None
        return all(l[campo] for l in ls)

    def falhas(base, campo="alcancavel_com_anteriores"):
        return [l["degrau"] for l in pm10 if l["base"] == base and l[campo] is False]

    def regra_sint(campo):
        sint = {b: todos(b, campo) for b in ("E0", "E0p", "E0mais", "E0pmais")}
        f0 = falhas("E0", campo)
        go0 = sint["E0"] is True and sint["E0p"] is True
        lacos = bool(f0) and set(f0) <= {"fecho", "descartar"}
        go_mais = (not go0) and lacos and sint["E0mais"] is True and sint["E0pmais"] is True
        return sint, f0, go0, lacos, go_mais
    sint, falhas_e0, go_e0_sint, so_lacos, go_e0mais_sint = regra_sint("alcancavel_com_anteriores")
    sint_c, falhas_c, go0_c, _, gom_c = regra_sint("alcancavel_conservador")
    evid = []
    descobertas, nao_copia = {}, {}
    if f6 is not None:
        for chave, d in f6["bracos"].items():
            base = chave.split("@")[1]
            for r in d["relatorio"]["resultados"]:
                if r["aceita"] and r["reutilizacoes"]:
                    ci = [c for c in f6["custo_igual"] if c["braco"] == chave and c["tarefa"] == r["tarefa_id"]]
                    evid.append({"braco": chave, "base": base, "tarefa": r["tarefa_id"],
                                 "reutilizadas": r["reutilizacoes"],
                                 "lfix_resolve_a_custo_igual": ci[0]["lfix_resolve_a_custo_igual"] if ci else None})
            descobertas[chave] = [a["nome"] for a in d["abstracoes"] if a["proveniencia"] == "descoberta"]
            nao_copia[chave] = [a["nome"] for a in d["abstracoes"]
                                if a["proveniencia"] == "descoberta" and not a.get("copia_de_solucao")]

    def autonomo(base, protocolo=True):
        ts = {e["tarefa"] for e in evid if e["base"] == base and e["lfix_resolve_a_custo_igual"] is False
              and (e["braco"].startswith("L-lib@") if protocolo else e["braco"].startswith("L-lib"))}
        return len(ts) >= aut_min_tarefas
    aut = {b: autonomo(b) for b in ("E0", "E0mais")}
    aut_var = {b: autonomo(b, False) for b in ("E0", "E0mais")}

    def regra(go0, gom, a):
        if go0 and a["E0"]:
            return "GO com E0"
        if gom and a["E0mais"]:
            return "GO com E0+"
        return "NO-GO"
    motivos = []
    if not go_e0_sint:
        motivos.append(f"alcance sintático (D adequado, B único) falha em E0 para {falhas_e0}" if falhas_e0 else
                       f"alcance sintático em E0/E0' não estabelecido (E0: {sint['E0']}, E0': {sint['E0p']})")
        if sint["E0p"] is not True:
            motivos.append(f"E0': {sint['E0p']} (falhas: {falhas('E0p')}; None = não medido ou limite inválido)")
    if not go_e0mais_sint:
        motivos.append(f"condição E0+ não satisfeita (só laços falham em E0: {so_lacos}; E0+: {sint['E0mais']}; "
                       f"E0'+: {sint['E0pmais']} — falhas E0+: {falhas('E0mais')}, E0'+: {falhas('E0pmais')})")
    if not any(descobertas.values()):
        motivos.append("NENHUMA abstração foi descoberta na execução autônoma")
    elif not any(nao_copia.values()):
        motivos.append("as abstrações 'descobertas' são todas cópias (α/η) de soluções de degraus; nenhuma "
                       "compressão entre tarefas distintas")
    if any(descobertas.values()) and not evid:
        motivos.append("abstrações foram descobertas, mas NENHUMA foi reutilizada numa solução aceita posterior")
    for b in ("E0", "E0mais"):
        if not aut[b]:
            motivos.append(f"exigência autônoma em {BASE_NOME[b]}: < {aut_min_tarefas} tarefa(s) com reutilização "
                           f"em L-lib@{b} e L-fix@{b} falhando a custo total igual")
    interrupcoes = {}
    if f5 is not None:
        interrupcoes["I4"] = {"disparada": f5.get("I4_disparada"),
                              "motivo": "compressão gulosa não extrai vizPretos de ParAdjacente + NenhumaIsolada "
                                        "(PM11 pela compressão efetiva)"}
        if f5.get("I4_disparada"):
            motivos.append("I4 (compressor) disparada: vizPretos não é extraído pela compressão gulosa")
    for k, v in (outras or {}).items():
        interrupcoes[k] = v
    return {"alcance_sintatico_por_base": sint, "degraus_inalcancaveis_E0": falhas_e0,
            "condicao_GO_E0": go_e0_sint, "condicao_GO_E0mais": go_e0mais_sint,
            "alcance_sintatico_conservador": sint_c, "degraus_inalcancaveis_E0_conservador": falhas_c,
            "abstracoes_descobertas": descobertas, "descobertas_nao_copia_de_solucao": nao_copia,
            "reutilizacoes_em_solucoes_aceitas": evid, "aut_min_tarefas": aut_min_tarefas,
            "exigencia_autonoma_por_base": aut, "exigencia_autonoma_por_base_com_variante": aut_var,
            "exigencia_autonoma_E0p": "não verificada (sem braço E0' nesta escala)",
            "decisao": regra(go_e0_sint, go_e0mais_sint, aut),
            "decisao_conservadora": regra(go0_c, gom_c, aut),
            "decisao_se_variante_contasse": regra(go_e0_sint, go_e0mais_sint, aut_var),
            "interrupcoes": interrupcoes, "motivos": motivos,
            "nota": "Decisão de viabilidade do piloto exploratório (documento 03, seção 10 + exigência de "
                    "descoberta e reutilização autônomas por base); não é resultado científico. Condições de "
                    "custo (I3, I6, PM16) em medicoes.json/medicoes.md."}


def decidir_custo(med: dict, det: dict, cfg: ConfigPiloto) -> dict:
    """Condições de custo a partir de MEDIÇÕES (não determinísticas): PM9 (vazão em tamanhos ≤ pm9_s_max,
    limiar pm9_limiar/s) e I6 (< i6_limiar/s), PM13 (latência do oráculo ≤ pm13_limiar_s) e I3
    (> i3_limiar_s), PM16 (custo projetado pelo modelo da seção 8 com o custo medido por candidato)."""
    out: dict = {}
    f3 = med.get("fases_detalhe", {}).get("3", {})
    vaz = []
    for x in f3.get("pm8_pm9", []):
        ts = [t for t in x.get("tempos_por_tamanho", []) if t["s"] <= cfg.pm9_s_max]
        if ts and ts[-1]["t_s"] > 0:
            vaz.append({"base": x["base"], "rotulo": x["rotulo"], "tabela": x.get("tabela_espec"), "D": x.get("D"),
                        "s_ate": ts[-1]["s"], "candidatos": ts[-1]["candidatos"],
                        "candidatos_por_segundo": ts[-1]["candidatos"] / ts[-1]["t_s"]})
    if vaz:
        vs = [v["candidatos_por_segundo"] for v in vaz]
        out["PM9"] = {"limiar": cfg.pm9_limiar, "s_max": cfg.pm9_s_max, "min": min(vs), "max": max(vs),
                      "mediana": sorted(vs)[len(vs) // 2], "abaixo_do_limiar": sum(v < cfg.pm9_limiar for v in vs),
                      "medicoes": len(vs), "ok": all(v >= cfg.pm9_limiar for v in vs), "por_job": vaz}
        out["I6"] = {"limiar": cfg.i6_limiar, "abaixo": sum(v < cfg.i6_limiar for v in vs), "de": len(vs),
                     "disparada": any(v < cfg.i6_limiar for v in vs),
                     "nota": "I6 exige vazão abaixo do limiar 'após otimização'; nenhuma otimização foi tentada"}
    f6m = med.get("fases_detalhe", {}).get("6", {})
    lat = [v["oraculo_latencia_max_s"] for v in f6m.get("bracos", {}).values() if "oraculo_latencia_max_s" in v]
    lat += [f6m.get("pm12", {}).get("latencia_max_s", 0.0)] if f6m.get("pm12") else []
    if lat:
        out["PM13"] = {"limiar_s": cfg.pm13_limiar_s, "latencia_max_s": max(lat), "ok": max(lat) <= cfg.pm13_limiar_s}
        out["I3_latencia"] = {"limiar_s": cfg.i3_limiar_s, "disparada": max(lat) > cfg.i3_limiar_s}
    f6 = det.get("fases", {}).get("6")
    if f6 and f6m.get("bracos"):
        cpu = sum(v["cpu_s"] for v in f6m["bracos"].values())
        tot = f6["livro_total_por_aprendiz"]
        cands = sum(v["busca_candidatos"] + v["enumeracao_candidatos"] for k, v in tot.items() if "#" not in k)
        cands_prot = sum(v["busca_candidatos"] for k, v in tot.items() if "#" not in k)
        rod = [r["rodadas"] for b in f6["bracos"].values() for r in b["relatorio"]["resultados"] if r["rodadas"]]
        K_med = sum(rod) / len(rod) if rod else 1.0
        if cands:
            s_por_cand = cpu / cands
            proj_s = cfg.pm16_tarefas * cfg.pm16_B * K_med * s_por_cand * cfg.pm16_sementes * cfg.pm16_bases * cfg.pm16_bracos
            out["PM16"] = {"segundos_cpu_fase6": cpu, "candidatos_total": cands, "candidatos_protocolo": cands_prot,
                           "s_por_candidato": s_por_cand, "K_medio_observado": K_med,
                           "modelo": "tarefas × B × K × s/candidato × sementes × bases × braços (documento 03, 8)",
                           "parametros": {"tarefas": cfg.pm16_tarefas, "B": cfg.pm16_B, "sementes": cfg.pm16_sementes,
                                          "bases": cfg.pm16_bases, "bracos": cfg.pm16_bracos},
                           "horas_cpu_projetadas": proj_s / 3600, "limiar_h": cfg.pm16_limiar_h,
                           "ok": proj_s / 3600 <= cfg.pm16_limiar_h,
                           "nota": "candidato = candidato do protocolo + candidato interno do enumerador "
                                   "(o custo de CPU inclui ambos); B aplicado como no piloto"}
    return out


# =====================================================================
# Separação do confirmatório (U27) e hashes
# =====================================================================
def verificar_separacao(grades: Dict[str, List[str]], semente: int) -> dict:
    conjuntos = {}
    total_conf = 0
    for nome in sorted(grades):
        gs = [Grade.de_texto(s) for s in grades[nome]]
        part: Dict[str, int] = {}
        for g in gs:
            p = G.particao_de(g)
            part[p] = part.get(p, 0) + 1
        conf = part.get(G.PARTICAO_CONFIRMATORIA, 0)
        total_conf += conf
        conjuntos[nome] = {"grades": len(gs), "hash": G.hash_conjunto(gs), "particoes": dict(sorted(part.items())),
                           "no_confirmatorio": conf}
    baldes = {k: [r.start, r.stop] for k, r in G.PARTICOES.items()}
    disj = all(set(G.PARTICOES[a]).isdisjoint(G.PARTICOES[b]) for a in G.PARTICOES for b in G.PARTICOES if a < b)
    return {"semente": semente, "semente_no_intervalo_piloto": semente in G.SEMENTES_PILOTO,
            "intervalo_sementes_piloto": [G.SEMENTES_PILOTO.start, G.SEMENTES_PILOTO.stop],
            "semente_min_confirmatorio": G.SEMENTE_MIN_CONFIRMATORIO, "baldes": baldes,
            "particoes_disjuntas": disj, "grades_no_confirmatorio": total_conf, "conjuntos": conjuntos,
            "nota": "PM1 exaustivo (n <= 4) audita as referências em TODO o domínio, inclusive baldes do "
                    "confirmatório; é auditoria de implementação, nenhuma dessas grades é dado do aprendiz "
                    "e não entra nestes conjuntos."}


# =====================================================================
# Relatório Markdown (determinístico) e medições
# =====================================================================
def _tab(cab: List[str], linhas: List[List]) -> str:
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for l in linhas:
        out.append("| " + " | ".join("" if x is None else str(x) for x in l) + " |")
    return "\n".join(out)


def relatorio_markdown(det: dict, cfg: ConfigPiloto) -> str:
    L = [f"# Piloto exploratório — registros determinísticos (semente {cfg.semente}, escala {cfg.escala})", "",
         "Nenhuma alegação científica: dados e hiperparâmetros expostos (documento 03, seção 0). "
         "Medições reais (tempo, memória, vazão PM9, latência PM13, custo PM16, I3/I6) ficam em `medicoes.md`.", ""]
    if "fontes" in det:
        L += [f"Código: SHA-256 das fontes de fedro_piloto/ = `{det['fontes']['sha256_total'][:16]}` "
              f"(Python {det['fontes']['python']}; por arquivo em config.json/deterministico.json).", ""]
    f = det.get("fases", {})
    if "1" in f:
        d = f["1"]
        L += ["## Fase 1 — referências e geradores", "",
              f"PM1: discordâncias ref_a ≠ ref_b no total = **{d['pm1_total_discordancias']}** "
              f"({len(d['pm1'])} conceitos; exaustivo n ∈ {list(cfg.pm1_ns_exaustivo)}, "
              f"{cfg.pm1_amostras_por_n} amostras por n ∈ {list(cfg.pm1_ns_amostra)}).", ""]
        L += [_tab(["conceito", "n", "k pares", "PM2 aceitação", "PM4 mesmo nº pretas", "PM5 M10", "métodos", "hash"],
                   [[x["conceito"], x["n"], x.get("k_pares_obtido"), _f(x.get("taxa_aceitacao")),
                     _f(x.get("fracao_mesmo_numero_pretas")), _f(x.get("m10")), x.get("metodos"),
                     (x.get("hash") or "")[:12]] if not x["degenerado"] else
                    [x["conceito"], x["n"], "degenerado", x.get("motivo"), "", "", "", ""] for x in d["pm2_pm5"]]), ""]
        fora = d["pm6_fora_de_3dp"]
        comp = [l for l in d["pm6"] if "auditoria" in l]
        L += [f"PM6: {len(comp)} comparações com a auditoria; fora de 3 DP: {len(fora)}.", ""]
        if fora:
            L += [_tab(["conceito", "n", "p", "piloto", "auditoria", "DP"],
                       [[l["conceito"], l["n"], l["p"], _f(l["frequencia"]), l["auditoria"], _f(l["dp"])] for l in fora]), ""]
        degs = [x for x in d["degeneracao"] if x["degenerado"]]
        L += ["Degeneração em oraculo_treino (só os degenerados):", "",
              _tab(["conceito", "n", "exaustivo", "motivo"], [[x["conceito"], x["n"], x["exaustivo"], x["motivo"]] for x in degs]), ""]
    if "2" in f:
        L += ["## Fase 2 — contagem N(s, τ) (PM7)", ""]
        for x in f["2"]["pm7"]:
            L.append(f"- {x['base']} {x['contexto']}: " + ", ".join(f"{s}:{v}" for s, v in x["contagens"].items()))
        L.append("")
    if "3" in f:
        L += ["## Fase 3 — alcance s_reach (PM8)", "",
              "Tabela 'curada' = dsl.BASES (instâncias escolhidas a partir da escada: desvio declarado); "
              "'sistematica' = dsl.BASES_SISTEMATICAS (critério fixado sem olhar a escada); "
              "'anteriores:X' = base + degraus manuais anteriores a X (modo auditoria). D = profundidade λ máxima. "
              "s_reach None = não determinado (limite de memória; ver medicoes).", "",
              _tab(["classe", "base", "contexto/tipo", "tabela", "D", "s_reach(B)", "s_reach só alvo", "s_completo",
                    "esgotado"],
                   [[x["classe"], x["base"], x["rotulo"], x.get("tabela_espec", "curada"), x.get("D", 2), x["s_reach"],
                     x["s_reach_so_alvo"], x["s_completo"], x["esgotado"]]
                    for x in f["3"]["pm8"]]), ""]
        if f["3"].get("auditoria_oe"):
            L += ["### Auditoria da poda OE contra amostra independente (teste_int, baterias do ambiente; E0, D = 2)", "",
                  "Classe = denotação nas entradas da amostra independente. 'perdidas' = classes de tamanho mínimo s "
                  "sem representante OE com essa denotação até s_max; 'atrasadas' = representadas só por termo maior.", "",
                  _tab(["tipo", "s_max", "entradas", "termos sem poda", "representantes", "classes", "perdidas",
                        "atrasadas", "perdidas por s (perdidas/novas)"],
                       [[a["tipo"], a["s_max"], a["entradas"], a["termos_sem_poda"], a["representantes_oe"], a["classes"],
                         a["perdidas_total"], a["atrasadas_total"],
                         ", ".join(f"{x['s']}:{x['perdidas']}/{x['classes_novas']}" for x in a["por_tamanho"]
                                   if x["classes_novas"])] for a in f["3"]["auditoria_oe"]]), ""]
    if "4" in f:
        d = f["4"]
        L += ["## Fase 4 — viabilidade da escada (PM10)", "",
              f"Programas da escada são MANUAIS (manual-teste): só limites superiores de tamanho. B único = "
              f"{d.get('B_unico')}. NenhumaIsolada usa a variante corrigida (o programa do documento discorda da "
              "referência na grade vazia). 'alcançável' = tamanho − binders do contexto ≤ s_reach(D adequado, tabela "
              "curada); colunas à direita: s_reach a D = 2 (gramática do aprendiz), com a tabela sistemática e com "
              "os degraus anteriores na tabela; 'conservador' usa o menor s_reach medido.", "",
              _tab(["degrau", "base", "programa", "tam. c/ ant.", "bruto", "prof. λ (contexto)", "D", "fonte s_reach",
                    "s_reach(D)", "alcançável", "motivo", "s_reach D=2", "s_reach sist.", "s_reach c/ ant. na tabela",
                    "conservador"],
                   [[x["degrau"], x["base"], x["programa"], x["tamanho_com_anteriores"], x["tamanho_bruto"],
                     x["profundidade_contexto"], x["D_necessario"], x["fonte_s_reach"], x["s_reach_D"],
                     x["alcancavel_com_anteriores"], x["motivo"], x["s_reach_D2"], x["s_reach_sistematica"],
                     x["s_reach_com_anteriores"], x["alcancavel_conservador"]]
                    for x in d["pm10"]]), "",
              "Verificação dos programas manuais contra as referências do ambiente:", "",
              _tab(["programa", "base", "entradas verificadas", "discordâncias", "documentadas", "nota"],
                   [[x["programa"], x["base"], x["verificadas"], x["discordancias"], x["discordancias_documentadas"],
                     x["nota"]]
                    for x in d["verificacao_programas_manuais"]]), ""]
    if "5" in f:
        d = f["5"]
        L += ["## Fase 5 — MECANISMO (modo mecanismo-teste; soluções MANUAIS; não é descoberta) — PM11", "",
              "PM11 = alvo inserido pela compressão GULOSA (mecanismo de L-lib). 'no ranking' é diagnóstico: o alvo "
              "aparece entre os fragmentos candidatos (escolhido com conhecimento do alvo).", "",
              _tab(["alvo", "fontes manuais", "extraído (gulosa)", "no ranking", "posição", "fragmento igual (ranking)",
                    "entradas gulosas (manual-teste)"],
                   [[x["alvo"], ", ".join(x["solucoes_fonte"]), x["extraido"], x.get("presente_no_ranking"),
                     x["posicao_no_ranking"],
                     x["fragmento_igual"]["legivel"] if x["fragmento_igual"] else None,
                     "; ".join(e["legivel"] for e in x["entradas_compressao_gulosa"])] for x in d["pm11"]]), "",
              f"PM11 = {d['pm11_fracao']:.2f} (alvo presente no ranking: "
              f"{d.get('alvo_presente_no_ranking_fracao', float('nan')):.2f}); I4 disparada: {d.get('I4_disparada')}", ""]
    if "6" in f:
        d = f["6"]
        conc = d.get("pm14_conciliacao", {})
        L += ["## Fase 6 — EXECUÇÃO AUTÔNOMA (biblioteca vazia, modo autonomo)", "",
              f"Fechamento aritmético do livro-razão: {d['fechamento']['ok']} (diferença {d['fechamento']['diferenca']}); "
              f"PM14 (conciliação com contadores independentes): diferença **{conc.get('diferenca')}** "
              f"({conc.get('num_divergencias')} divergências); hash do diário {d['hash_diario'][:16]}.", ""]
        if d.get("pm12"):
            p = d["pm12"]
            L += [f"PM12 (minimalidade do oráculo contra força bruta, n ≤ 4): {p['iguais_forca_bruta']}/{p['pares']} "
                  f"({p['com_contraexemplo']} com contraexemplo).", ""]
        for chave, b in d["bracos"].items():
            L += [f"### {chave}", "",
                  _tab(["tarefa", "aceita", "fim", "rodadas", "hipótese", "tam.", "custo aprendiz", "cumulativo",
                        "candidatos (protocolo) cum.", "enumeração cum.", "acurácia teste", "usa biblioteca",
                        "reutilizações", "novas abstrações"],
                       [[r["tarefa_id"], r["aceita"], r["motivo_fim"], r["rodadas"], r["hipotese_legivel"], r["tamanho"],
                         c["custo_aprendiz"], c["cumulativo"], c["cumulativo_candidatos"], c["cumulativo_enumeracao"],
                         _f(r["acuracia_teste"]),
                         ", ".join(r["constantes_biblioteca_usadas"]), r["reutilizacoes"] or "",
                         "; ".join(f"{a['nome']} = {a['legivel']} ({a['metodo']}; {a['categoria']})"
                                   for a in r["abstracoes_novas"])]
                        for r, c in zip(b["relatorio"]["resultados"], b["curva"])]), ""]
            if b["abstracoes"]:
                L += ["Abstrações (proveniência 'descoberta', com certificado do laço do aprendiz):", "",
                      _tab(["nome", "categoria", "tipo", "corpo", "método", "origem", "coincide com solução de",
                            "reutilizações"],
                           [[a["nome"], a["categoria"], a["tipo"], a["legivel"], a["metodo"], ", ".join(a["tarefas_origem"]),
                             ", ".join(a.get("coincide_com_solucao_de_tarefa", [])), a["reutilizacoes"] or ""]
                            for a in b["abstracoes"]]), ""]
        L += ["### Comparação a custo cumulativo TOTAL igual (reutilizações)", ""]
        if d["custo_igual"]:
            L += [_tab(["braço", "tarefa", "reutilizadas", "cum. total L-lib", "orçamento custo igual",
                        "L-fix resolve a custo igual", "método"],
                       [[x["braco"], x["tarefa"], x["abstracoes_reutilizadas"], x["cumulativo_lib"],
                         x["orcamento_custo_igual"], x["lfix_resolve_a_custo_igual"], x["metodo"]]
                        for x in d["custo_igual"]]), ""]
        else:
            L += ["Nenhuma solução aceita reutilizou abstração descoberta; nada a comparar.", ""]
    if "7" in f:
        d = f["7"]
        L += ["## Fase 7 — decisão", "", f"**Decisão (braços do protocolo, regra do documento 03): {d['decisao']}**", "",
              f"Decisão conservadora (menor s_reach medido): {d.get('decisao_conservadora')}", "",
              f"Decisão se a variante L-lib+f contasse: {d['decisao_se_variante_contasse']}", "",
              f"Exigência autônoma por base (mín. {d.get('aut_min_tarefas')} tarefa(s)): "
              f"{d.get('exigencia_autonoma_por_base')}; E0': {d.get('exigencia_autonoma_E0p')}", ""]
        L += [f"- {m}" for m in d["motivos"]] + [""]
        for k, v in d.get("interrupcoes", {}).items():
            L.append(f"- Interrupção {k}: {v}")
        L += ["", d["nota"], ""]
    if "separacao" in det:
        s = det["separacao"]
        L += ["## Separação do confirmatório (U27)", "",
              f"Semente {s['semente']} no intervalo do piloto: {s['semente_no_intervalo_piloto']}; partições disjuntas: "
              f"{s['particoes_disjuntas']}; grades no confirmatório: **{s['grades_no_confirmatorio']}**.", "",
              _tab(["conjunto", "grades", "hash"], [[k, v["grades"], v["hash"][:16]] for k, v in s["conjuntos"].items()]), ""]
    if "reaproveitamento" in det:
        r = det["reaproveitamento"]
        L += ["## Reaproveitamento de fases", "",
              f"Fases {r['fases_reaproveitadas']} copiadas da execução `{r['origem']}` (mesma configuração e mesmo "
              f"SHA-256 das fontes; deterministico.json de origem {r['sha256_deterministico_origem'][:16]}); "
              f"fases {r['fases_recalculadas']} recalculadas nesta execução. Cadeia de origens: {r.get('cadeia')}.", ""]
    L += ["## Desvios declarados", ""] + [f"- {x}" for x in det.get("desvios", [])] + [""]
    return "\n".join(L)


def _f(x):
    return None if x is None else (f"{x:.3f}" if isinstance(x, float) else x)


def medicoes_markdown(med: dict) -> str:
    L = ["# Piloto — medições reais (NÃO determinísticas)", "",
         "Tempo de parede, CPU e memória de pico. Memória de um job = pico do TRECHO (VmHWM reiniciado no início "
         "do job, num processo novo por job) quando 'trecho'; 'processo-desde-o-inicio' = ru_maxrss monotônico. "
         "A linha de cada fase dá só o pico do processo PRINCIPAL desde o início (não a memória da fase). "
         "Nada aqui entra no livro-razão.", ""]
    for k, v in med.get("fases", {}).items():
        L.append(f"- fase {k}: parede {v.get('tempo_parede_s', 0):.1f} s; CPU (processo + filhos) "
                 f"{v.get('cpu_s', 0):.1f} s{' (reaproveitada)' if v.get('reaproveitada') else ''}")
    L.append("")
    dc = med.get("decisao_custo", {})
    if dc:
        L += ["## Condições de custo (documento 03, seções 4, 8, 9)", ""]
        if "PM9" in dc:
            p = dc["PM9"]
            L.append(f"- PM9 (vazão em tamanhos ≤ {p['s_max']}): mín {p['min']:.0f}, mediana {p['mediana']:.0f}, "
                     f"máx {p['max']:.0f} candidatos/s; {p['abaixo_do_limiar']}/{p['medicoes']} abaixo do limiar "
                     f"{p['limiar']:.0f}/s → {'ok' if p['ok'] else 'FALHA'}")
        if "I6" in dc:
            p = dc["I6"]
            L.append(f"- I6 (vazão < {p['limiar']:.0f}/s): {p['abaixo']}/{p['de']} medições → "
                     f"{'DISPARADA' if p['disparada'] else 'não disparada'} ({p['nota']})")
        if "PM13" in dc:
            p = dc["PM13"]
            L.append(f"- PM13 (latência do oráculo ≤ {p['limiar_s']} s): máx {p['latencia_max_s']:.3f} s → "
                     f"{'ok' if p['ok'] else 'FALHA'}; I3 (> {dc['I3_latencia']['limiar_s']} s): "
                     f"{'DISPARADA' if dc['I3_latencia']['disparada'] else 'não disparada'}")
        if "PM16" in dc:
            p = dc["PM16"]
            L.append(f"- PM16 (custo projetado): {p['s_por_candidato'] * 1000:.3f} ms/candidato, K médio "
                     f"{p['K_medio_observado']:.2f} → {p['horas_cpu_projetadas']:.0f} h de CPU (limiar "
                     f"{p['limiar_h']:.0f} h) → {'ok' if p['ok'] else 'EXCEDE'}; {p['nota']}")
        L.append("")
    f3 = med.get("fases_detalhe", {}).get("3")
    if f3:
        L += ["## PM9 (vazão do enumerador por job)", "",
              _tab(["classe", "base", "contexto/tipo", "tabela", "D", "tempo (s)", "candidatos/s (total)",
                    "memória pico (KiB)", "escopo"],
                   [[x["classe"], x["base"], x["rotulo"], x.get("tabela_espec"), x.get("D"), _f(x["tempo_parede_s"]),
                     _f(x["candidatos_avaliados_por_segundo"]), x["memoria_pico_kib"], x.get("memoria_escopo")]
                    for x in f3["pm8_pm9"]]), ""]
        rec = [x for x in f3["pm8_pm9"] if x.get("dependente_de_recurso")]
        if rec:
            L += ["Medições limitadas por memória (dependente de recurso):", "",
                  _tab(["base", "contexto/tipo", "tabela", "D", "limite (GB)", "candidatos ao parar"],
                       [[x["base"], x["rotulo"], x.get("tabela_espec"), x.get("D"),
                         x["dependente_de_recurso"]["limite_memoria_gb"],
                         x["dependente_de_recurso"]["candidatos_ao_parar"]] for x in rec]), ""]
    f1 = med.get("fases_detalhe", {}).get("1")
    if f1:
        L += ["## PM3 (vazão dos geradores)", "",
              _tab(["conceito", "n", "tempo (s)", "pares/s", "projeção 1000 pares (s)"],
                   [[x["conceito"], x["n"], _f(x.get("tempo_parede_s")), _f(x.get("pares_por_segundo")),
                     _f(x.get("projecao_s_1000_pares"))] for x in f1["pm3"]]), ""]
    f6 = med.get("fases_detalhe", {}).get("6")
    if f6:
        L += ["## Execução autônoma", "",
              _tab(["braço", "parede (s)", "CPU (s)", "memória pico (KiB)", "escopo", "consultas ao oráculo",
                    "latência máx (s)", "latência média (s)"],
                   [[k, _f(v["tempo_parede_s"]), _f(v["cpu_s"]), v["memoria_pico_kib"], v.get("memoria_escopo"),
                     v.get("oraculo_consultas"), _f(v.get("oraculo_latencia_max_s")),
                     _f(v.get("oraculo_latencia_media_s"))] for k, v in f6["bracos"].items()]), ""]
    return "\n".join(L)


# =====================================================================
# PM15: comparação de duas execuções
# =====================================================================
def comparar_execucoes(dir_a: str, dir_b: str) -> dict:
    """PM15: compara os blocos determinísticos de duas execuções (fase a fase, só as fases CALCULADAS nas
    duas, não reaproveitadas) e os livros-razão (diário). Devolve o artefato gravado em pm15.json."""
    def ler(d):
        with open(os.path.join(d, "deterministico.json"), encoding="utf-8") as f:
            return json.load(f)
    a, b = ler(dir_a), ler(dir_b)
    reap = lambda x: set(x.get("reaproveitamento", {}).get("fases_reaproveitadas", []))
    comuns = sorted((set(a["fases"]) - reap(a)) & (set(b["fases"]) - reap(b)))
    fases = {k: _dump(a["fases"][k]) == _dump(b["fases"][k]) for k in comuns}
    livros = None
    ra, rb = os.path.join(dir_a, "razao.json"), os.path.join(dir_b, "razao.json")
    if os.path.exists(ra) and os.path.exists(rb) and "6" in comuns:
        livros = LivroRazao.carregar_json(ra).comparar_deterministico(LivroRazao.carregar_json(rb))
    return {"execucao_a": os.path.basename(os.path.normpath(dir_a)),
            "execucao_b": os.path.basename(os.path.normpath(dir_b)),
            "mesmo_codigo": a.get("fontes", {}).get("sha256_total") == b.get("fontes", {}).get("sha256_total"),
            "fases_comparadas": comuns, "fases_identicas": fases,
            "diferencas_livro_razao": livros, "identico": all(fases.values()) and not livros,
            "nota": "fases reaproveitadas não são comparadas (seriam idênticas por cópia)"}


# =====================================================================
# Execução
# =====================================================================
def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1, default=str)


def executar(cfg: ConfigPiloto, diretorio: Optional[str] = None, reaproveitar: Optional[str] = None,
             aceitar_codigo_diferente: bool = False) -> dict:
    """Executa as fases de cfg.fases; grava os registros em `diretorio` (se dado). Devolve
    {"deterministico", "medicoes"}. Com `reaproveitar` (pasta de uma execução anterior com a MESMA
    configuração E o MESMO SHA-256 das fontes), as fases ausentes de cfg.fases são copiadas dessa
    execução e o fato é registrado com a cadeia completa de origens (cada fase é função determinística
    da configuração e do código; a 4 depende da 3; a 7, da 4, 5 e 6). Código diferente é recusado, salvo
    aceitar_codigo_diferente=True, que registra a diferença por arquivo."""
    cfg.verificar()
    fontes = hash_fontes()
    det: dict = {"config": cfg.como_dict(), "fontes": fontes, "fases": {}, "desvios": list(DESVIOS_ESCALA)}
    anterior = None
    if reaproveitar is not None:
        with open(os.path.join(reaproveitar, "deterministico.json"), "rb") as f:
            bruto = f.read()
        anterior = json.loads(bruto)
        with open(os.path.join(reaproveitar, "medicoes.json"), encoding="utf-8") as f:
            med_ant = json.load(f)
        ca, cb = dict(anterior["config"]), dict(det["config"])
        ca.pop("fases"), cb.pop("fases")
        if ca != cb:
            raise ValueError("reaproveitamento exige a mesma configuração (exceto fases)")
        fa = anterior.get("fontes", {})
        dif_codigo = sorted(k for k in set(fa.get("arquivos", {})) | set(fontes["arquivos"])
                            if fa.get("arquivos", {}).get(k) != fontes["arquivos"].get(k))
        if (dif_codigo or fa.get("python") != fontes["python"]) and not aceitar_codigo_diferente:
            raise ValueError(f"reaproveitamento exige o mesmo código (SHA-256 das fontes difere em {dif_codigo or 'python'})")
        reaproveitadas = sorted(k for k in anterior["fases"] if int(k) not in cfg.fases)
        cadeia = list(anterior.get("reaproveitamento", {}).get("cadeia", [])) + [{
            "origem": os.path.basename(os.path.normpath(reaproveitar)),
            "sha256_deterministico": hashlib.sha256(bruto).hexdigest(),
            "sha256_fontes": fa.get("sha256_total"), "fases_calculadas_la": sorted(
                set(anterior["fases"]) - set(anterior.get("reaproveitamento", {}).get("fases_reaproveitadas", [])))}]
        det["reaproveitamento"] = {"origem": os.path.basename(os.path.normpath(reaproveitar)),
                                   "sha256_deterministico_origem": hashlib.sha256(bruto).hexdigest(),
                                   "fases_reaproveitadas": reaproveitadas,
                                   "fases_recalculadas": sorted(str(x) for x in cfg.fases),
                                   "codigo_diferente_arquivos": dif_codigo, "cadeia": cadeia}
    med: dict = {"fases": {}, "fases_detalhe": {}, "execucao": {"processos": cfg.processos,
                                                                "inicio": time.strftime("%Y-%m-%dT%H:%M:%S")}}
    grades: Dict[str, List[str]] = {}
    livro = None
    pm8: List[dict] = []
    f6 = None

    def rodar(k, fn):
        t0, c0 = time.perf_counter(), _cpu()
        r = fn()
        med["fases"][str(k)] = {"tempo_parede_s": time.perf_counter() - t0, "cpu_s": _cpu() - c0,
                                "memoria_pico_processo_principal_kib": _maxrss_principal()}
        det["fases"][str(k)] = r["deterministico"]
        med["fases_detalhe"][str(k)] = r["medicoes"]
        grades.update(r.get("grades", {}))
        return r

    if anterior is not None:
        for k in det["reaproveitamento"]["fases_reaproveitadas"]:
            det["fases"][k] = anterior["fases"][k]
            med["fases"][k] = dict(med_ant["fases"].get(k, {}), reaproveitada=True)
            med["fases_detalhe"][k] = med_ant["fases_detalhe"].get(k, {})
        if "3" in det["fases"]:
            pm8 = det["fases"]["3"]["pm8"]
    if 1 in cfg.fases:
        rodar(1, lambda: fase1(cfg))
    if 2 in cfg.fases:
        rodar(2, lambda: fase2(cfg))
    if 3 in cfg.fases:
        pm8 = rodar(3, lambda: fase3(cfg))["deterministico"]["pm8"]
    if 4 in cfg.fases:
        rodar(4, lambda: fase4(cfg, pm8))
    if 5 in cfg.fases:
        rodar(5, lambda: fase5(cfg))
    if 6 in cfg.fases:
        r6 = rodar(6, lambda: fase6(cfg))
        livro = r6["livro"]
        f6 = r6["deterministico"]
    elif "6" in det["fases"]:
        f6 = det["fases"]["6"]
        caminho_razao = os.path.join(reaproveitar, "razao.json") if reaproveitar else None
        if caminho_razao and os.path.exists(caminho_razao):
            livro = LivroRazao.carregar_json(caminho_razao)   # livro-razão da fase 6 reaproveitada
            if livro.hash_diario() != f6["hash_diario"]:
                raise ValueError("razao.json da origem não corresponde à fase 6 reaproveitada")
    if 7 in cfg.fases:
        pm10 = det["fases"].get("4", {}).get("pm10", [])
        f5 = det["fases"].get("5")
        outras = {}
        f1 = det["fases"].get("1")
        if f1 is not None:
            outras["I1_referencias"] = {"disparada": f1["pm1_total_discordancias"] > 0,
                                        "motivo": "PM1 > 0 (discordância entre referências)"}
        if f6 is not None:
            outras["I1_livro"] = {"disparada": (not f6["fechamento"]["ok"])
                                  or bool(f6.get("pm14_conciliacao", {}).get("diferenca")),
                                  "motivo": "livro-razão não fecha ou não concilia com contadores independentes"}
        rodar(7, lambda: {"deterministico": decidir(pm10, f6, f5, cfg.aut_min_tarefas, outras), "medicoes": {}})
    det["separacao"] = verificar_separacao(grades, cfg.semente)
    if anterior is not None:   # conjuntos das fases reaproveitadas (hashes da execução de origem)
        sep = det["separacao"]
        for nome, c in anterior["separacao"]["conjuntos"].items():
            if nome not in sep["conjuntos"]:
                sep["conjuntos"][nome] = dict(c, reaproveitado=True)
                sep["grades_no_confirmatorio"] += c["no_confirmatorio"]
        sep["conjuntos"] = dict(sorted(sep["conjuntos"].items()))
    if 7 in cfg.fases:
        det["fases"]["7"]["interrupcoes"]["I7_vazamento"] = {
            "disparada": det["separacao"]["grades_no_confirmatorio"] > 0,
            "motivo": "grade do confirmatório usada pelo piloto (U27)"}
    med["decisao_custo"] = decidir_custo(med, det, cfg)
    if diretorio is not None:
        gravar(diretorio, cfg, det, med, livro)
    return {"deterministico": det, "medicoes": med, "livro": livro}


def gravar(diretorio: str, cfg: ConfigPiloto, det: dict, med: dict, livro: Optional[LivroRazao]) -> None:
    os.makedirs(diretorio, exist_ok=True)

    def w(nome, txt):
        with open(os.path.join(diretorio, nome), "w", encoding="utf-8") as f:
            f.write(txt)

    w("config.json", _dump({**cfg.como_dict(), "fontes": det.get("fontes")}))
    w("deterministico.json", _dump(det))
    w("medicoes.json", _dump(med))
    if livro is not None:
        livro.serializar_json(os.path.join(diretorio, "razao.json"))
    w("hashes.json", _dump(det["separacao"]))
    abst = {}
    f6 = det["fases"].get("6")
    if f6:
        for k, b in f6["bracos"].items():
            abst[k] = {"proveniencia": "descoberta (execução autônoma; certificado do laço do aprendiz)",
                       "abstracoes": b["abstracoes"],
                       "descobertas_que_nao_sao_copia_de_solucao": [a["nome"] for a in b["abstracoes"]
                                                                     if not a.get("copia_de_solucao")]}
    f5 = det["fases"].get("5")
    if f5:
        abst["MECANISMO (mecanismo-teste, NÃO descoberta)"] = f5["pm11"]
    w("abstracoes.json", _dump(abst))
    w("relatorio.md", relatorio_markdown(det, cfg))
    w("medicoes.md", medicoes_markdown(med))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Piloto exploratório do experimento 1 (documento 03)")
    ap.add_argument("--id", default=None, help="identificador da execução (pasta runs/<id>)")
    ap.add_argument("--semente", type=int, default=10_001)
    ap.add_argument("--processos", type=int, default=4)
    ap.add_argument("--fases", default="1,2,3,4,5,6,7")
    ap.add_argument("--mini", action="store_true", help="configuração mínima (testes)")
    ap.add_argument("--raiz", default="runs")
    ap.add_argument("--reaproveitar", default=None,
                    help="pasta de execução anterior (mesma configuração e mesmo código) de onde copiar as fases não pedidas")
    ap.add_argument("--comparar-com", default=None,
                    help="pasta de outra execução: grava pm15.json com a comparação determinística (PM15)")
    a = ap.parse_args(argv)
    cfg = config_mini(a.semente) if a.mini else ConfigPiloto(semente=a.semente)
    cfg = replace(cfg, processos=a.processos, fases=tuple(int(x) for x in a.fases.split(",")))
    rid = a.id or f"piloto-s{a.semente}-{time.strftime('%Y%m%d-%H%M%S')}"
    d = os.path.join(a.raiz, rid)
    r = executar(cfg, d, a.reaproveitar)
    if a.comparar_com:
        with open(os.path.join(d, "pm15.json"), "w", encoding="utf-8") as f:
            f.write(_dump(comparar_execucoes(a.comparar_com, d)))
    dec = r["deterministico"]["fases"].get("7", {}).get("decisao")
    print(f"registros em {d}; decisão: {dec}")


if __name__ == "__main__":
    main()
