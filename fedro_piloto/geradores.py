"""Geradores do ambiente (documento 02, 2.2.2-2.2.3; documento 03, fase 1).

Tudo aqui pertence ao AMBIENTE (proveniência "ambiente"): amostragem natural,
geradores construtivos de positivos, negativos emparelhados em densidade,
quase-acertos por trocas, classificador por densidade (M10) e reservatório do
oráculo. Nada deste módulo é programa do aprendiz nem pode entrar na sua
biblioteca; os aprendizes recebem apenas grades rotuladas.

Partição por instância. O balde de uma grade, Grade.balde(100), derivado do
SHA-256 da serialização, decide a que conjunto ela pode pertencer (PARTICOES).
Isso dá disjunção por instância, não só por semente. Limitação combinatória:
o domínio de tamanho n tem 2^(n²) grades; n = 1 tem 2, n = 2 tem 16, n = 3 tem
512 e n = 4 tem 65 536. Uma partição de 10 % dos baldes recebe, em média,
0,2 / 1,6 / 51 / 6 554 grades. Para n <= 2 muitas partições ficam vazias ou com
uma ou duas grades; capacidade_particao e degenerado medem isso exatamente
(n <= 4) e os consumidores devem consultá-los antes de exigir exemplos.

Contadores determinísticos (ContadorGeracao) e medições reais
(MedicaoGeracao: tempo de parede, memória de pico) são estruturas distintas.
"""
from __future__ import annotations

import bisect
import hashlib
import random
import resource
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .grade import Grade, Pos, chave_minimalidade, todas_as_grades
from .referencias import REGISTRO, Conceito, regiao

PROVENIENCIA = "ambiente"  # nunca "descoberta" nem "manual-teste": isto não é biblioteca

# ---------------------------------------------------------------- constantes
PS_NATURAL: Tuple[float, ...] = (0.20, 0.35, 0.50, 0.65)
NUM_BALDES = 100
PARTICOES: Dict[str, range] = {
    "oraculo_treino": range(0, 20),
    "validacao": range(20, 30),
    "teste_int": range(30, 40),
    "teste_ext": range(40, 50),
    "reservado_confirmatorio": range(50, 100),
}
PARTICAO_CONFIRMATORIA = "reservado_confirmatorio"
SEMENTES_PILOTO = range(10_000, 20_000)
SEMENTE_MIN_CONFIRMATORIO = 20_000
N_EXAUSTIVO_MAX = 4


def _verificar_particoes_disjuntas() -> None:
    vistos: List[int] = []
    for r in PARTICOES.values():
        vistos.extend(r)
    assert sorted(vistos) == list(range(NUM_BALDES)), "PARTICOES deve particionar [0, 100)"


_verificar_particoes_disjuntas()


class ConceitoDegenerado(Exception):
    """Conceito sem positivos, sem negativos ou sem negativos emparelhados em (n, partição)."""

    def __init__(self, info: dict):
        super().__init__(info.get("motivo", "degenerado"))
        self.info = info


# ---------------------------------------------------------------- sementes e partições
def rng_piloto(semente: int) -> random.Random:
    """Gerador do piloto; recusa sementes fora de [10 000, 20 000)."""
    if semente not in SEMENTES_PILOTO:
        raise ValueError(f"semente {semente} fora do intervalo do piloto")
    return random.Random(semente)


def semente_derivada_64(semente: int, *partes) -> int:
    """Semente de 64 bits derivada por SHA-256 de (semente, *partes): fluxos de papéis diferentes
    (exemplos, teste, reservatório, mundos OE) e de sementes vizinhas não coincidem, e não dependem
    da posição de uma tarefa num registro (achado de revisão: derivação linear semente + 7·i + k)."""
    if semente not in SEMENTES_PILOTO:
        raise ValueError(f"semente {semente} fora do intervalo do piloto")
    return int(hashlib.sha256(repr((int(semente),) + tuple(partes)).encode("utf-8")).hexdigest()[:16], 16)


def rng_derivado(semente: int, *partes) -> random.Random:
    """random.Random independente por papel: semente do piloto (verificada) + rótulo do papel."""
    return random.Random(semente_derivada_64(semente, *partes))


def rng_confirmatorio(semente: int) -> random.Random:
    """Gerador do confirmatório; recusa sementes abaixo de 20 000."""
    if semente < SEMENTE_MIN_CONFIRMATORIO:
        raise ValueError(f"semente {semente} abaixo do intervalo confirmatório")
    return random.Random(semente)


def verificar_particao(particao: Optional[str], permitir_confirmatorio: bool = False) -> None:
    """Partição deve existir; a confirmatória exige permissão explícita."""
    if particao is None:
        return
    if particao not in PARTICOES:
        raise ValueError(f"partição desconhecida: {particao}")
    if particao == PARTICAO_CONFIRMATORIA and not permitir_confirmatorio:
        raise PermissionError("partição reservada ao confirmatório: uso proibido no piloto")


def na_particao(g: Grade, particao: Optional[str]) -> bool:
    """None significa domínio inteiro (só para auditorias, nunca para conjuntos de dados)."""
    return particao is None or g.balde(NUM_BALDES) in PARTICOES[particao]


def particao_de(g: Grade) -> str:
    b = g.balde(NUM_BALDES)
    for nome, r in PARTICOES.items():
        if b in r:
            return nome
    raise AssertionError("balde sem partição")


# ---------------------------------------------------------------- custo
@dataclass
class ContadorGeracao:
    """Contadores determinísticos de geração (dependem só da semente)."""
    grades_geradas: int = 0          # grades completas construídas
    falhas_construcao: int = 0       # construções abortadas (sem espaço, etc.)
    rejeitadas_particao: int = 0     # fora dos baldes da partição
    rejeitadas_rotulo: int = 0       # construídas, mas a verificação deu o rótulo errado
    aceitas: int = 0
    chamadas_rotulo: int = 0         # cada chamada executa ref_a e ref_b
    permutacoes_avaliadas: int = 0
    trocas_avaliadas: int = 0
    consultas_tabela_exaustiva: int = 0   # rótulos lidos da tabela exaustiva (n <= 4)
    tentativas_esgotadas: int = 0

    def somar(self, outro: "ContadorGeracao") -> "ContadorGeracao":
        for k, v in asdict(outro).items():
            setattr(self, k, getattr(self, k) + v)
        return self

    def taxa_aceitacao(self) -> float:
        """PM2: aceitas pelas referências / geradas dentro da partição."""
        d = self.aceitas + self.rejeitadas_rotulo
        return self.aceitas / d if d else float("nan")

    def taxa_particao(self) -> float:
        return 1 - self.rejeitadas_particao / self.grades_geradas if self.grades_geradas else float("nan")

    def como_dict(self) -> dict:
        return asdict(self)


@dataclass
class MedicaoGeracao:
    """Medições reais (não determinísticas). memoria_pico_kb é o ru_maxrss do processo."""
    tempo_parede_s: float = 0.0
    memoria_pico_kb: int = 0

    def como_dict(self) -> dict:
        return asdict(self)


@contextmanager
def medir(medicao: MedicaoGeracao):
    t0 = time.perf_counter()
    try:
        yield medicao
    finally:
        medicao.tempo_parede_s += time.perf_counter() - t0
        medicao.memoria_pico_kb = max(medicao.memoria_pico_kb,
                                      resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def _rotular(c: Conceito, g: Grade, contador: Optional[ContadorGeracao]) -> bool:
    if contador is not None:
        contador.chamadas_rotulo += 1
    return c.rotulo(g)  # levanta AssertionError se ref_a != ref_b


# ---------------------------------------------------------------- distribuição natural
def amostra_natural(n: int, rng: random.Random, ps: Sequence[float] = PS_NATURAL,
                    particao: Optional[str] = None, contador: Optional[ContadorGeracao] = None,
                    max_tentativas: int = 100_000) -> Grade:
    """Bernoulli(p) por célula, p uniforme em ps; com partição, rejeita fora dos baldes."""
    verificar_particao(particao)
    for _ in range(max_tentativas):
        p = rng.choice(ps)
        g = Grade(n, tuple(1 if rng.random() < p else 0 for _ in range(n * n)))
        if contador is not None:
            contador.grades_geradas += 1
        if na_particao(g, particao):
            return g
        if contador is not None:
            contador.rejeitadas_particao += 1
    raise ConceitoDegenerado({"motivo": f"partição {particao} sem grades alcançáveis em n={n}"})


# ---------------------------------------------------------------- utilidades de construção
@lru_cache(maxsize=None)
def _viz(n: int) -> Tuple[Tuple[int, ...], ...]:
    out = []
    for k in range(n * n):
        i, j = divmod(k, n)
        v = []
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            a, b = i + di, j + dj
            if 0 <= a < n and 0 <= b < n:
                v.append(a * n + b)
        out.append(tuple(v))
    return tuple(out)


def _idx(n: int, p: Pos) -> int:
    return (p[0] - 1) * n + (p[1] - 1)


def _borda(n: int) -> List[int]:
    return [k for k in range(n * n) if k // n in (0, n - 1) or k % n in (0, n - 1)]


def _cantos(n: int) -> List[int]:
    return sorted({0, n - 1, (n - 1) * n, n * n - 1})


def _preencher(bits: List[Optional[int]], p: float, rng: random.Random) -> Tuple[int, ...]:
    return tuple(b if b is not None else (1 if rng.random() < p else 0) for b in bits)


def _crescer(n: int, rng: random.Random, tamanho: int, proibidas: set,
             inicio: Optional[int] = None, permitidas: Optional[set] = None) -> Optional[set]:
    """Passeio aleatório auto-evitante que produz um componente de exatamente `tamanho` células
    fora de `proibidas`; quando a cabeça fica presa, salta para a fronteira do componente."""
    viz = _viz(n)

    def livre(k):
        return k not in proibidas and (permitidas is None or k in permitidas)

    if inicio is None:
        cand = [k for k in range(n * n) if livre(k)]
        if not cand:
            return None
        inicio = rng.choice(cand)
    elif not livre(inicio):
        return None
    comp = {inicio}
    cabeca = inicio
    while len(comp) < tamanho:
        cand = [k for k in viz[cabeca] if k not in comp and livre(k)]
        if not cand:
            cand = sorted({k for c in comp for k in viz[c] if k not in comp and livre(k)})
        if not cand:
            return None
        cabeca = rng.choice(cand)
        comp.add(cabeca)
    return comp


def _faixa(n: int, comp: Iterable[int]) -> set:
    viz = _viz(n)
    s = set(comp)
    for k in list(s):
        s.update(viz[k])
    return s


def _segmento(n: int, rng: random.Random, proibidas: set, comprimento: int,
              tentativas: int = 50) -> Optional[set]:
    """Segmento reto (horizontal ou vertical) fora de `proibidas`."""
    comprimento = max(1, min(comprimento, n))
    for _ in range(tentativas):
        horiz = rng.random() < 0.5
        fixo = rng.randrange(n)
        ini = rng.randrange(n - comprimento + 1)
        cel = {fixo * n + ini + t if horiz else (ini + t) * n + fixo for t in range(comprimento)}
        if not (cel & proibidas):
            return cel
    return None


def _semear(n: int, rng: random.Random, tamanhos: Sequence[int], inicios=None,
            permitidas: Optional[set] = None, proibidas0: Optional[set] = None,
            perto: bool = False) -> Optional[List[set]]:
    """Semeia componentes com faixa de separação de uma célula; None se faltar espaço.
    perto=True começa cada componente seguinte logo fora da faixa dos anteriores (distância 2)."""
    proibidas = set(proibidas0 or ())
    comps = []
    for t, L in enumerate(tamanhos):
        ini = None
        if inicios is not None:
            cands = [k for k in inicios[t] if k not in proibidas]
            if not cands:
                return None
            ini = rng.choice(cands)
        elif perto and comps:
            cands = sorted({v for u in proibidas for v in _viz(n)[u] if v not in proibidas
                            and (permitidas is None or v in permitidas)})
            if cands:
                ini = rng.choice(cands)
        c = _crescer(n, rng, L, proibidas, ini, permitidas)
        if c is None:
            return None
        comps.append(c)
        proibidas |= _faixa(n, c)
    return comps


def _grade_de(n: int, pretas: Iterable[int]) -> Grade:
    bits = [0] * (n * n)
    for k in pretas:
        bits[k] = 1
    return Grade(n, tuple(bits))


def _tam_max(n: int, m: int) -> int:
    return max(1, (n * n) // (2 * max(m, 1)))


# ---------------------------------------------------------------- geradores construtivos
def _g_f1(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    p = rng.choice(PS_NATURAL)
    bits: List[Optional[int]] = [None] * (n * n)
    nome = c.nome
    if nome == "ExistePreta":
        bits[rng.randrange(n * n)] = 1
    elif nome == "ParAdjacente":
        if n < 2:
            return None
        k = rng.randrange(n * n)
        par = (k, rng.choice(_viz(n)[k]))
        if rng.random() < 0.5:
            # modo esparso: conjunto independente aleatório mais um único par adjacente
            pretas = set(par)
            for q in rng.sample(range(n * n), n * n):
                if rng.random() < p and not any(v in pretas for v in _viz(n)[q]):
                    pretas.add(q)
            return _grade_de(n, pretas)
        bits[par[0]] = bits[par[1]] = 1
    elif nome == "LinhaOcupada":
        for i in range(n):
            bits[i * n + rng.randrange(n)] = 1
    elif nome == "TopoCheio":
        for j in range(n):
            bits[j] = 1
    elif nome == "CantoSupEsq":
        bits[0] = 1
    elif nome == "Diagonal":
        for i in range(n):
            bits[i * n + i] = 1
    elif nome == "ColunaDoisVazia":
        if n < 2:
            return None
        for i in range(n):
            bits[i * n + 1] = 0
    else:
        return None
    return Grade(n, _preencher(bits, p, rng))


def _g_numcomp(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    S = c.params["S"]
    if S.startswith("="):
        m = int(S[1:])
    elif S == ">=2":  # concentrado em m = 2 para que existam negativos emparelhados próximos
        m = rng.choice((2, 2, 2, 3, max(2, min(6, (n * n + 1) // 4))))
    elif S == "<=2":
        m = rng.choice((0, 1, 1, 2, 2, 2))
    else:
        return None
    tamanhos = [rng.randint(1, _tam_max(n, m)) for _ in range(m)]
    comps = _semear(n, rng, tamanhos, perto=rng.random() < 0.5)
    return None if comps is None else _grade_de(n, set().union(*comps) if comps else ())


def _componente_sob(P: str, n: int, rng: random.Random, proibidas: set) -> Optional[set]:
    if P == "reto":
        return _segmento(n, rng, proibidas, rng.randint(1, n))
    if P == "tocaBorda":
        cands = [k for k in _borda(n) if k not in proibidas]
        return _crescer(n, rng, rng.randint(1, _tam_max(n, 1)), proibidas, rng.choice(cands)) if cands else None
    if P == "contemCanto":
        cands = [k for k in _cantos(n) if k not in proibidas]
        return _crescer(n, rng, rng.randint(1, _tam_max(n, 1)), proibidas, rng.choice(cands)) if cands else None
    if P in ("min2", "min3"):
        minimo = 2 if P == "min2" else 3
        if n * n < minimo:
            return None
        return _crescer(n, rng, rng.randint(minimo, max(minimo, _tam_max(n, 1))), proibidas)
    return None


def _g_existe(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    """Um componente sob P mais ruído esparso. Em metade das construções de tocaBorda e
    contemCanto o ruído evita a borda (ou os cantos) e o componente toca a borda numa só célula,
    o que deixa positivos perto da fronteira do conceito (negativo a poucas trocas)."""
    P = c.params["P"]
    evitar: set = set()
    if P in ("reto", "min3") and rng.random() < 0.5:
        g = _existe_fronteira(P, n, rng)
        if g is not None:
            return g
    if P in ("tocaBorda", "contemCanto") and rng.random() < 0.5:
        evitar = set(_borda(n)) if P == "tocaBorda" else set(_cantos(n))
        ini = rng.choice(sorted(evitar))
        interior = set(range(n * n)) - set(_borda(n))
        comp = _crescer(n, rng, rng.randint(1, _tam_max(n, 1)), set(), ini, interior | {ini})
        if comp is None:
            comp = {ini}
    else:
        comp = _componente_sob(P, n, rng, set())
    if comp is None:
        return None
    pr = rng.choice((0.05, 0.10, 0.20))
    bits = [1 if k in comp else (1 if k not in evitar and rng.random() < pr else 0) for k in range(n * n)]
    return Grade(n, tuple(bits))


def _e_reto(n: int, comp: Iterable[int]) -> bool:
    comp = list(comp)
    return len({k // n for k in comp}) == 1 or len({k % n for k in comp}) == 1


def _existe_fronteira(P: str, n: int, rng: random.Random) -> Optional[Grade]:
    """Componentes de fundo que violam P mais exatamente um componente sob P, pequeno
    (segmento de 2 ou 3 células para reto; 3 células para min3): positivo perto da fronteira."""
    m = rng.randint(1, 3)
    if P == "reto":
        tamanhos = [rng.randint(3, max(3, _tam_max(n, m + 1))) for _ in range(m)]
    else:
        tamanhos = [rng.randint(1, 2) for _ in range(m)]
    fundo = _semear(n, rng, tamanhos) or []
    if P == "reto":
        fundo = [cp for cp in fundo if not _e_reto(n, cp)]
    proibidas = set()
    for cp in fundo:
        proibidas |= _faixa(n, cp)
    alvo = _segmento(n, rng, proibidas, rng.randint(2, 3)) if P == "reto" else _crescer(n, rng, 3, proibidas)
    if alvo is None:
        return None
    return _grade_de(n, set().union(alvo, *fundo))


def _g_todos(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    P = c.params["P"]
    m = rng.randint(1, 3)
    proibidas: set = set()
    pretas: set = set()
    for _ in range(m):
        comp = _componente_sob(P, n, rng, proibidas)
        if comp is None:
            break
        pretas |= comp
        proibidas |= _faixa(n, comp)
    return _grade_de(n, pretas) if pretas else None


def _g_maior_toca_borda(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    L = rng.randint(1, _tam_max(n, 1))
    m = rng.randint(0, 3)
    tamanhos = [L] + [rng.randint(1, L) for _ in range(m)]
    inicios = [_borda(n)] + [list(range(n * n))] * m
    comps = _semear(n, rng, tamanhos, inicios)
    if comps is None:
        comps = _semear(n, rng, [L], [_borda(n)])
    return None if comps is None else _grade_de(n, set().union(*comps))


def _regioes(c: Conceito, n: int) -> Tuple[List[int], List[int]]:
    g0 = Grade.vazia(n)
    A = [_idx(n, p) for p in regiao(c.params["A"], g0)]
    B = [_idx(n, p) for p in regiao(c.params["B"], g0)]
    return A, B


def _g_card(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    A, B = _regioes(c, n)
    if set(A) & set(B):
        return amostra_natural(n, rng)  # regiões sobrepostas (só n = 1): rejeição natural verificada
    if c.esquema == "CardIgual":
        kA = kB = rng.randint(0, min(len(A), len(B)))
    else:  # CardNoMax: |A ∩ pretas| <= |B ∩ pretas|
        kB = rng.randint(0, len(B))
        kA = rng.randint(0, min(kB, len(A)))
    bits: List[Optional[int]] = [None] * (n * n)
    for k in A:
        bits[k] = 0
    for k in B:
        bits[k] = 0
    for k in rng.sample(A, kA):
        bits[k] = 1
    for k in rng.sample(B, kB):
        bits[k] = 1
    return Grade(n, _preencher(bits, rng.choice(PS_NATURAL), rng))


def _g_linhas_iguais(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    k = rng.randint(0, n)
    bits = [0] * (n * n)
    for i in range(n):
        for j in rng.sample(range(n), k):
            bits[i * n + j] = 1
    g = Grade(n, tuple(bits))
    return g.transposta() if c.nome == "ColunasIguais" else g


def _g_mesmo_tamanho(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    m = rng.randint(1, max(1, min(4, (n * n + 1) // 4)))
    s = rng.randint(1, _tam_max(n, m))
    comps = _semear(n, rng, [s] * m)
    return None if comps is None else _grade_de(n, set().union(*comps))


def _g_numcomp_linha1(n: int, rng: random.Random) -> Optional[Grade]:
    """#componentes = #pretas na linha 1: cada corrida da linha 1 cresce para baixo; o déficit
    (pretas da linha 1 menos corridas) é coberto por componentes extra fora da linha 1."""
    k = rng.choice([0] + list(range(1, n + 1)) * 3)
    linha1 = sorted(rng.sample(range(n), k))
    corridas: List[List[int]] = []
    for j in linha1:
        if corridas and corridas[-1][-1] == j - 1:
            corridas[-1].append(j)
        else:
            corridas.append([j])
    resto = set(range(n, n * n))
    proibidas = set(range(n))  # linha 1 fica fixa
    pretas = set(linha1)
    for corr in corridas:
        comp = set(corr)
        extra = rng.randint(0, _tam_max(n, k or 1))
        for _ in range(extra):
            fronteira = sorted({v for u in comp for v in _viz(n)[u] if v in resto and v not in comp and v not in proibidas})
            if not fronteira:
                break
            comp.add(rng.choice(fronteira))
        pretas |= comp
        proibidas |= _faixa(n, comp)
    deficit = k - len(corridas)
    if deficit:
        tamanhos = [rng.randint(1, _tam_max(n, deficit + len(corridas))) for _ in range(deficit)]
        comps = _semear(n, rng, tamanhos, permitidas=resto, proibidas0=proibidas)
        if comps is None:
            return None
        for cmp_ in comps:
            pretas |= cmp_
    return _grade_de(n, pretas)


def _g_numcomp_regiao(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    g = _g_numcomp_linha1(n, rng)
    if g is None:
        return None
    return g.transposta() if c.params["A"] == "col1" else g


def _maior_vs_linha1_fronteira(n: int, rng: random.Random) -> Optional[Grade]:
    """k pretas isoladas na linha 1 (linha 2 vazia), um componente de exatamente k células e
    componentes menores nas linhas >= 3: maior = k, logo positivo a uma troca da fronteira."""
    if n < 4:
        return None
    k = rng.randint(2, (n + 1) // 2)
    livres = list(range(n))
    linha1: List[int] = []
    rng.shuffle(livres)
    for j in livres:
        if len(linha1) < k and all(abs(j - x) > 1 for x in linha1):
            linha1.append(j)
    k = len(linha1)
    baixo = set(range(2 * n, n * n))
    tamanhos = [k] + [rng.randint(1, k - 1) for _ in range(rng.randint(0, 3))]
    comps = _semear(n, rng, tamanhos, permitidas=baixo)
    if comps is None:
        return None
    return _grade_de(n, set(linha1).union(*comps))


def _g_maior_vs_linha1(c: Conceito, n: int, rng: random.Random) -> Optional[Grade]:
    if rng.random() < 0.5:
        g = _maior_vs_linha1_fronteira(n, rng)
        if g is not None:
            return g
    k = rng.randint(0, n)
    linha1 = rng.sample(range(n), k)
    if n == 1:
        return _grade_de(n, linha1)
    resto = set(range(n, n * n))
    L = rng.randint(max(1, k), max(k, _tam_max(n, 1)))
    comp = _crescer(n, rng, L, set(), permitidas=resto) if L <= len(resto) else None
    if comp is None:
        return None
    pr = rng.choice((0.05, 0.10, 0.20))
    pretas = set(linha1) | comp | {u for u in resto if rng.random() < pr}
    return _grade_de(n, pretas)


_POR_ESQUEMA = {
    "F1": _g_f1, "F1'": _g_f1,
    "NumComp": _g_numcomp,
    "ExisteComp": _g_existe,
    "TodosComp": _g_todos,
    "MaiorTocaBorda": _g_maior_toca_borda,
    "CardIgual": _g_card, "CardNoMax": _g_card,
    "LinhasIguais": _g_linhas_iguais, "ColunasIguais": _g_linhas_iguais,
    "TodosMesmoTamanho": _g_mesmo_tamanho,
    "NumCompIgualRegiao": _g_numcomp_regiao,
    "MaiorCompVsRegiao": _g_maior_vs_linha1,
}


def construir_positivo(c: Conceito, n: int, rng: random.Random) -> Tuple[Optional[Grade], str]:
    """Uma tentativa de construção (sem verificação); devolve (grade ou None, método)."""
    f = _POR_ESQUEMA.get(c.esquema)
    if f is None:  # esquema sem gerador construtivo: rejeição natural verificada
        return amostra_natural(n, rng), "rejeicao_natural"
    return f(c, n, rng), "construtivo:" + c.esquema


def gerar_positivo(c: Conceito, n: int, particao: Optional[str], rng: random.Random,
                   contador: Optional[ContadorGeracao] = None, tentativas: int = 2000,
                   permitir_confirmatorio: bool = False) -> Optional[Grade]:
    """Positivo construtivo verificado pelas duas referências, dentro da partição."""
    verificar_particao(particao, permitir_confirmatorio)
    contador = contador if contador is not None else ContadorGeracao()
    for _ in range(tentativas):
        g, _metodo = construir_positivo(c, n, rng)
        if g is None:
            contador.falhas_construcao += 1
            continue
        contador.grades_geradas += 1
        if not na_particao(g, particao):
            contador.rejeitadas_particao += 1
            continue
        if _rotular(c, g, contador):
            contador.aceitas += 1
            return g
        contador.rejeitadas_rotulo += 1
    contador.tentativas_esgotadas += 1
    return None


# ---------------------------------------------------------------- negativos emparelhados
@dataclass
class QuaseAcerto:
    grade: Grade                   # alvo, com rótulo invertido e o mesmo número de pretas
    trocas: List[Tuple[Pos, Pos]]  # sequência de trocas (preta, branca) aplicadas
    caminho: List[Grade]           # grade original, intermediárias, alvo
    minimo_garantido: bool         # True se nenhuma sequência mais curta existe na partição
    nivel: str  # "exato" (n <= 4), "troca1", "troca2-exaustiva", "troca2-amostral", "busca-local"


def _pos(n: int, k: int) -> Pos:
    return (k // n + 1, k % n + 1)


def quase_acerto(g: Grade, c: Conceito, rng: random.Random, particao: Optional[str],
                 contador: Optional[ContadorGeracao] = None, max_alvos_exaustivo: int = 6000,
                 L: int = 2000, permitir_confirmatorio: bool = False) -> Optional[QuaseAcerto]:
    """Menor número de trocas preta<->branca que inverte o rótulo (alvo na partição).

    Nível 1: todas as trocas simples em ordem aleatória (a primeira válida é uniforme entre as
    válidas). Nível 2: trocas duplas, exaustivas se houver <= max_alvos_exaustivo alvos, senão L
    sorteios; como o nível 1 foi exaustivo, achar no nível 2 também é mínimo. Nível 3: busca
    local por passeio de trocas com reinícios até L trocas, parando no primeiro rótulo invertido.
    Em todos os níveis a grade antes da última troca tem o rótulo original."""
    verificar_particao(particao, permitir_confirmatorio)
    contador = contador if contador is not None else ContadorGeracao()
    n = g.n
    if n <= N_EXAUSTIVO_MAX:
        return _quase_acerto_exato(g, c, rng, particao, contador)
    r0 = _rotular(c, g, contador)
    pretas = [k for k, b in enumerate(g.bits) if b]
    brancas = [k for k, b in enumerate(g.bits) if not b]
    if not pretas or not brancas:
        return None  # nenhuma troca possível: só existe uma grade com este número de pretas

    def trocar(h: Grade, a: int, b: int) -> Grade:
        contador.trocas_avaliadas += 1
        return h.trocar(_pos(n, a), _pos(n, b))

    def alvo_ok(t: Grade) -> bool:
        return na_particao(t, particao) and _rotular(c, t, contador) != r0

    # nível 1
    simples = [(a, b) for a in pretas for b in brancas]
    rng.shuffle(simples)
    for a, b in simples:
        t = trocar(g, a, b)
        if alvo_ok(t):
            return QuaseAcerto(t, [(_pos(n, a), _pos(n, b))], [g, t], True, "troca1")
    # nível 2
    if len(pretas) >= 2 and len(brancas) >= 2:
        def pares(xs):
            return [(xs[i], xs[j]) for i in range(len(xs)) for j in range(i + 1, len(xs))]
        npp, nbb = len(pretas) * (len(pretas) - 1) // 2, len(brancas) * (len(brancas) - 1) // 2
        exaustivo = npp * nbb <= max_alvos_exaustivo
        if exaustivo:
            alvos = [(pp, bb) for pp in pares(pretas) for bb in pares(brancas)]
            rng.shuffle(alvos)
        else:
            alvos = [(tuple(rng.sample(pretas, 2)), tuple(rng.sample(brancas, 2))) for _ in range(L)]
        for (a1, a2), (b1, b2) in alvos:
            h_opts = [((a1, b1), (a2, b2)), ((a1, b2), (a2, b1)), ((a2, b1), (a1, b2)), ((a2, b2), (a1, b1))]
            t = trocar(trocar(g, a1, b1), a2, b2)
            if not alvo_ok(t):
                continue
            for s1, s2 in h_opts:  # intermediária com o rótulo original
                h = trocar(g, *s1)
                if _rotular(c, h, contador) == r0:
                    return QuaseAcerto(t, [(_pos(n, s1[0]), _pos(n, s1[1])), (_pos(n, s2[0]), _pos(n, s2[1]))],
                                       [g, h, t], True, "troca2-exaustiva" if exaustivo else "troca2-amostral")
    # nível 3: busca local
    gastas = 0
    while gastas < L:
        h, caminho, trocas = g, [g], []
        for _ in range(n * n):
            pr = [k for k, b in enumerate(h.bits) if b]
            br = [k for k, b in enumerate(h.bits) if not b]
            a, b = rng.choice(pr), rng.choice(br)
            h = trocar(h, a, b)
            gastas += 1
            caminho.append(h)
            trocas.append((_pos(n, a), _pos(n, b)))
            if _rotular(c, h, contador) != r0:
                if na_particao(h, particao):
                    return QuaseAcerto(h, trocas, caminho, False, "busca-local")
                break  # invertido fora da partição: reinicia (mantém o invariante do caminho)
            if gastas >= L:
                break
    contador.tentativas_esgotadas += 1
    return None


def _indice(g: Grade) -> int:
    """Posição de g na enumeração de todas_as_grades(g.n)."""
    k = 0
    for b in g.bits:
        k = (k << 1) | b
    return k


def _quase_acerto_exato(g: Grade, c: Conceito, rng: random.Random, particao: Optional[str],
                        contador: ContadorGeracao) -> Optional[QuaseAcerto]:
    """n <= 4: alvo à menor distância em trocas (Hamming/2) entre os rótulos invertidos da partição
    com o mesmo número de pretas; ordem das trocas escolhida para que a penúltima grade tenha o
    rótulo original. minimo_garantido é True quando o alvo está à distância mínima."""
    n = g.n
    gs, _, _ = _dominio(n)
    rot = _rotulos_exaustivos(c.nome, n)
    r0 = _rotular(c, g, contador)
    k = sum(g.bits)
    cands = [i for i in _indices_por_pretas(n, particao).get(k, ()) if rot[i] != r0]
    contador.consultas_tabela_exaustiva += len(_indices_por_pretas(n, particao).get(k, ()))
    if not cands:
        return None
    por_dist: Dict[int, List[int]] = {}
    for i in cands:
        d = sum(x != y for x, y in zip(g.bits, gs[i].bits)) // 2
        por_dist.setdefault(d, []).append(i)
    dmin = min(por_dist)
    for d in sorted(por_dist):
        grupo = por_dist[d]
        rng.shuffle(grupo)
        for i in grupo:
            t = gs[i]
            sair = [q for q in range(n * n) if g.bits[q] and not t.bits[q]]
            entrar = [q for q in range(n * n) if t.bits[q] and not g.bits[q]]
            for _ in range(20):
                rng.shuffle(sair)
                rng.shuffle(entrar)
                caminho, h = [g], g
                for a, b in zip(sair, entrar):
                    h = h.trocar(_pos(n, a), _pos(n, b))
                    contador.trocas_avaliadas += 1
                    caminho.append(h)
                contador.consultas_tabela_exaustiva += 1
                if rot[_indice(caminho[-2])] == r0:
                    trocas = [(_pos(n, a), _pos(n, b)) for a, b in zip(sair, entrar)]
                    return QuaseAcerto(t, trocas, caminho, d == dmin, "exato")
    contador.tentativas_esgotadas += 1
    return None


def negativo_emparelhado(g: Grade, c: Conceito, rng: random.Random, particao: Optional[str],
                         metodo: str = "auto", contador: Optional[ContadorGeracao] = None,
                         tentativas_permutacao: int = 200, L: int = 2000,
                         permitir_confirmatorio: bool = False) -> Optional[Tuple[Grade, int, str]]:
    """Grade com o mesmo número de pretas e rótulo invertido, na partição.

    metodo: "permutacao" (embaralha as células e verifica), "troca" (quase-acerto) ou "auto"
    (permutação, depois troca). Devolve (grade, num_trocas, metodo) ou None. Para permutação,
    num_trocas é a distância em trocas (Hamming/2)."""
    verificar_particao(particao, permitir_confirmatorio)
    contador = contador if contador is not None else ContadorGeracao()
    r0 = _rotular(c, g, contador)
    if metodo in ("permutacao", "auto"):
        bits = list(g.bits)
        for _ in range(tentativas_permutacao):
            rng.shuffle(bits)
            contador.permutacoes_avaliadas += 1
            t = Grade(g.n, tuple(bits))
            if na_particao(t, particao) and _rotular(c, t, contador) != r0:
                return t, sum(x != y for x, y in zip(g.bits, t.bits)) // 2, "permutacao"
        if metodo == "permutacao":
            contador.tentativas_esgotadas += 1
            return None
    if metodo in ("troca", "auto"):
        qa = quase_acerto(g, c, rng, particao, contador, max_alvos_exaustivo=min(6000, 4 * L), L=L,
                          permitir_confirmatorio=permitir_confirmatorio)
        if qa is None:
            return None
        return qa.grade, len(qa.trocas), qa.nivel
    raise ValueError(f"método desconhecido: {metodo}")


# ---------------------------------------------------------------- exaustivo (n <= 4)
@lru_cache(maxsize=None)
def _dominio(n: int) -> Tuple[Tuple[Grade, ...], Tuple[int, ...], Tuple[int, ...]]:
    """(grades, baldes, número de pretas) de todo o domínio de tamanho n <= 4."""
    if n > N_EXAUSTIVO_MAX:
        raise ValueError("exaustivo só para n <= 4")
    gs = tuple(todas_as_grades(n))
    return gs, tuple(g.balde(NUM_BALDES) for g in gs), tuple(sum(g.bits) for g in gs)


@lru_cache(maxsize=None)
def _rotulos_exaustivos(nome: str, n: int) -> Tuple[bool, ...]:
    c = REGISTRO[nome]
    return tuple(c.rotulo(g) for g in _dominio(n)[0])


@lru_cache(maxsize=None)
def _indices_por_pretas(n: int, particao: Optional[str]) -> Dict[int, Tuple[int, ...]]:
    _, bs, ks = _dominio(n)
    out: Dict[int, List[int]] = {}
    for i, (b, k) in enumerate(zip(bs, ks)):
        if particao is None or b in PARTICOES[particao]:
            out.setdefault(k, []).append(i)
    return {k: tuple(v) for k, v in out.items()}


def grades_da_particao(n: int, particao: Optional[str]) -> List[Grade]:
    """Todas as grades de tamanho n (<= 4) na partição, em ordem lexicográfica."""
    gs, bs, _ = _dominio(n)
    return [g for g, b in zip(gs, bs) if particao is None or b in PARTICOES[particao]]


def capacidade_particao(n: int, particao: Optional[str], conceitos: Optional[Iterable[str]] = None,
                        permitir_confirmatorio: bool = False) -> dict:
    """Contagem exaustiva (n <= 4) de grades na partição e de positivos/negativos por conceito.

    positivos_com_par: positivos para os quais existe, na partição, um negativo com o mesmo
    número de pretas (pré-requisito do emparelhamento em densidade)."""
    verificar_particao(particao, permitir_confirmatorio)
    gs, bs, ks = _dominio(n)
    dentro = [particao is None or b in PARTICOES[particao] for b in bs]
    por_conceito = {}
    for nome in (conceitos if conceitos is not None else REGISTRO):
        rot = _rotulos_exaustivos(nome, n)
        pos_k: Dict[int, int] = {}
        neg_k: Dict[int, int] = {}
        for k, d, r in zip(ks, dentro, rot):
            if d:
                alvo = pos_k if r else neg_k
                alvo[k] = alvo.get(k, 0) + 1
        por_conceito[nome] = {
            "positivos": sum(pos_k.values()),
            "negativos": sum(neg_k.values()),
            "positivos_com_par": sum(v for k, v in pos_k.items() if neg_k.get(k)),
            "negativos_com_par": sum(v for k, v in neg_k.items() if pos_k.get(k)),
            "positivos_por_pretas": dict(sorted(pos_k.items())),
            "negativos_por_pretas": dict(sorted(neg_k.items())),
        }
    return {"n": n, "particao": particao, "total_dominio": len(gs),
            "grades_na_particao": sum(dentro), "por_conceito": por_conceito}


def degenerado(c: Conceito, n: int, particao: Optional[str], rng: random.Random,
               tentativas: int = 2000, permitir_confirmatorio: bool = False) -> dict:
    """Diagnóstico de degeneração de (conceito, n, partição); exaustivo para n <= 4.

    Para n >= 5 é por tentativas (gerador construtivo, amostragem natural, grades extremas e
    negativos emparelhados): uma ausência é "não encontrada", não "impossível"."""
    verificar_particao(particao, permitir_confirmatorio)
    if n <= N_EXAUSTIVO_MAX:
        cap = capacidade_particao(n, particao, [c.nome], permitir_confirmatorio)["por_conceito"][c.nome]
        pos, neg, par = cap["positivos"] > 0, cap["negativos"] > 0, cap["positivos_com_par"] > 0
        contagens = {k: cap[k] for k in ("positivos", "negativos", "positivos_com_par")}
        exaustivo = True
    else:
        cont = ContadorGeracao()
        positivos: List[Grade] = []
        negativos: List[Grade] = []
        extremas = [Grade.vazia(n), Grade(n, (1,) * (n * n))]
        for g in extremas:
            if na_particao(g, particao):
                (positivos if _rotular(c, g, cont) else negativos).append(g)
        for _ in range(tentativas):
            if len(positivos) >= 20 and negativos:
                break
            g = gerar_positivo(c, n, particao, rng, cont, tentativas=1)
            if g is not None:
                positivos.append(g)
            h = amostra_natural(n, rng, particao=particao, contador=cont)
            (positivos if _rotular(c, h, cont) else negativos).append(h)
        par = False
        for g in positivos[:20]:
            res = negativo_emparelhado(g, c, rng, particao, "auto", cont, tentativas_permutacao=50,
                                       L=tentativas // 4, permitir_confirmatorio=permitir_confirmatorio)
            if res is not None:
                par = True
                negativos.append(res[0])
                break
        pos, neg = bool(positivos), bool(negativos)
        contagens = {"positivos_encontrados": len(positivos), "negativos_encontrados": len(negativos),
                     "contador": cont.como_dict()}
        exaustivo = False
    motivos = []
    if not pos:
        motivos.append("sem positivos")
    if not neg:
        motivos.append("sem negativos")
    if pos and neg and not par:
        motivos.append("nenhum positivo tem negativo com o mesmo número de pretas")
    if motivos and not exaustivo:
        motivos.append(f"(por {tentativas} tentativas; ausência não provada)")
    return {"conceito": c.nome, "n": n, "particao": particao, "exaustivo": exaustivo,
            "positivos_possiveis": pos, "negativos_possiveis": neg,
            "negativos_emparelhados_possiveis": bool(pos and neg and par),
            "degenerado": not (pos and neg and par), "motivo": "; ".join(motivos), "contagens": contagens}


# ---------------------------------------------------------------- M10 e conjuntos de desenho
def m10(conjunto) -> float:
    """Acurácia balanceada do melhor limiar de densidade (qualquer polaridade), ajustado no conjunto."""
    exemplos = conjunto.exemplos if hasattr(conjunto, "exemplos") else conjunto
    pos = sorted(g.densidade() for g, r in exemplos if r)
    neg = sorted(g.densidade() for g, r in exemplos if not r)
    if not pos or not neg:
        raise ValueError("M10 exige as duas classes")
    melhor = 0.5
    for t in sorted(set(pos) | set(neg)) + [float("inf")]:
        tpr = (len(pos) - bisect.bisect_left(pos, t)) / len(pos)   # positivo se densidade >= t
        tnr = bisect.bisect_left(neg, t) / len(neg)
        ba = (tpr + tnr) / 2
        melhor = max(melhor, ba, 1 - ba)
    return melhor


def hash_conjunto(grades: Iterable[Grade]) -> str:
    """SHA-256 das serializações ordenadas (independe da ordem)."""
    h = hashlib.sha256()
    for s in sorted(g.serializar() for g in grades):
        h.update(s.encode("ascii") + b"\n")
    return h.hexdigest()


@dataclass
class ConjuntoDesenho:
    exemplos: List[Tuple[Grade, bool]]           # positivo, negativo, positivo, negativo, ...
    pares: List[dict]
    metadados: dict
    contadores: Dict[str, ContadorGeracao] = field(default_factory=dict)   # determinísticos
    medicao: MedicaoGeracao = field(default_factory=MedicaoGeracao)       # reais

    def __iter__(self):
        return iter(self.exemplos)

    def __len__(self):
        return len(self.exemplos)


def conjunto_de_desenho(c: Conceito, n: int, particao: str, k_pares: int, rng: random.Random,
                        max_tentativas: Optional[int] = None, permitir_confirmatorio: bool = False,
                        L: int = 200, max_falhas_por_pretas: int = 2) -> ConjuntoDesenho:
    """k_pares pares (positivo construtivo, negativo emparelhado), metade por permutação e metade
    por troca (com recurso ao outro método se um falhar). Positivos distintos.

    Para n <= 4 o número de pares é limitado pela capacidade exata da partição (registrado nos
    metadados) e, se o gerador construtivo estagnar (200 tentativas seguidas sem par novo), os
    positivos restantes vêm da enumeração exaustiva da partição (contados à parte).
    Para n >= 5, um número de pretas k que falhou pelo menos max_falhas_por_pretas vezes com taxa
    de sucesso abaixo de 20 % passa a ser pulado (heurística registrada em "pretas_puladas"): o emparelhamento em densidade
    restringe os positivos às densidades em que existem negativos.
    Levanta ConceitoDegenerado se não há como formar pares."""
    if particao is None:
        raise ValueError("conjuntos de dados exigem partição")
    verificar_particao(particao, permitir_confirmatorio)
    alvo = k_pares
    neg_por_k: Optional[Dict[int, int]] = None
    if n <= N_EXAUSTIVO_MAX:
        d = degenerado(c, n, particao, rng, permitir_confirmatorio=permitir_confirmatorio)
        if d["degenerado"]:
            raise ConceitoDegenerado(d)
        alvo = min(k_pares, d["contagens"]["positivos_com_par"])
        neg_por_k = capacidade_particao(n, particao, [c.nome], permitir_confirmatorio)[
            "por_conceito"][c.nome]["negativos_por_pretas"]
    cpos, cneg = ContadorGeracao(), ContadorGeracao()
    med = MedicaoGeracao()
    pares: List[dict] = []
    usados: set = set()
    sem_par_vistos: set = set()
    metodos: Dict[str, int] = {}
    sem_par = duplicados = por_enumeracao = 0
    falhas_k: Dict[int, int] = {}
    sucessos_k: Dict[int, int] = {}
    pulados_k: Dict[int, int] = {}
    max_tentativas = max_tentativas or (20 * k_pares + 2000)
    reserva: Optional[List[Grade]] = None
    with medir(med):
        tent = estagnado = 0
        while len(pares) < alvo and tent < max_tentativas:
            tent += 1
            if n <= N_EXAUSTIVO_MAX and estagnado >= 200:
                if reserva is None:  # positivos com par ainda não usados, em ordem aleatória
                    gs, _, _ = _dominio(n)
                    rot = _rotulos_exaustivos(c.nome, n)
                    reserva = [gs[i] for k, idx in _indices_por_pretas(n, particao).items()
                               if neg_por_k.get(k) for i in idx if rot[i] and gs[i] not in usados]
                    rng.shuffle(reserva)
                if not reserva:
                    break
                g = reserva.pop()
                por_enumeracao += 1
            else:
                g = gerar_positivo(c, n, particao, rng, cpos, tentativas=50,
                                   permitir_confirmatorio=permitir_confirmatorio)
            if g is None:
                estagnado += 1
                continue
            if g in usados or g in sem_par_vistos:
                duplicados += 1
                estagnado += 1
                continue
            k = g.contagem_pretas()
            if neg_por_k is not None and not neg_por_k.get(k):
                sem_par += 1
                sem_par_vistos.add(g)
                estagnado += 1
                continue
            if (neg_por_k is None and falhas_k.get(k, 0) >= max_falhas_por_pretas
                    and 4 * sucessos_k.get(k, 0) < falhas_k[k]):  # taxa de sucesso < 20 %
                sem_par += 1
                pulados_k[k] = pulados_k.get(k, 0) + 1
                estagnado += 1
                if not pares and sem_par >= 200:
                    break
                continue
            preferido = "permutacao" if len(pares) % 2 == 0 else "troca"
            neg = None
            for m in (preferido, "troca" if preferido == "permutacao" else "permutacao"):
                neg = negativo_emparelhado(g, c, rng, particao, m, cneg, tentativas_permutacao=60, L=L,
                                           permitir_confirmatorio=permitir_confirmatorio)
                if neg is not None:
                    break
            if neg is None:
                falhas_k[k] = falhas_k.get(k, 0) + 1
                sem_par += 1
                sem_par_vistos.add(g)
                estagnado += 1
                if not pares and sem_par >= 200:
                    break  # nenhum positivo admite negativo emparelhado: degenerado
                continue
            estagnado = 0
            sucessos_k[k] = sucessos_k.get(k, 0) + 1
            usados.add(g)
            t, num_trocas, metodo = neg
            metodos[metodo] = metodos.get(metodo, 0) + 1
            pares.append({"positivo": g, "negativo": t, "num_trocas": num_trocas, "metodo": metodo})
    if not pares:
        raise ConceitoDegenerado({"conceito": c.nome, "n": n, "particao": particao, "degenerado": True,
                                  "motivo": f"nenhum par formado ({tent} tentativas, {sem_par} positivos sem par)"})
    exemplos: List[Tuple[Grade, bool]] = []
    for p in pares:
        exemplos += [(p["positivo"], True), (p["negativo"], False)]
    mesmo = sum(p["positivo"].contagem_pretas() == p["negativo"].contagem_pretas() for p in pares)
    negs = [p["negativo"] for p in pares]
    meta = {
        "conceito": c.nome, "n": n, "particao": particao, "proveniencia": PROVENIENCIA,
        "k_pares_solicitado": k_pares, "k_pares_obtido": len(pares),
        "limitado_por_capacidade": alvo < k_pares,
        "taxa_aceitacao": cpos.taxa_aceitacao(), "taxa_particao": cpos.taxa_particao(),
        "densidade_media_positivos": sum(p["positivo"].densidade() for p in pares) / len(pares),
        "densidade_media_negativos": sum(g.densidade() for g in negs) / len(pares),
        "fracao_mesmo_numero_pretas": mesmo / len(pares),
        "m10": m10(exemplos), "metodos": dict(sorted(metodos.items())),
        "positivos_sem_par": sem_par, "positivos_duplicados": duplicados,
        "positivos_por_enumeracao": por_enumeracao,
        "pretas_puladas": dict(sorted(pulados_k.items())),
        "negativos_repetidos": len(negs) - len(set(negs)),
        "hash": hash_conjunto(g for g, _ in exemplos),
    }
    return ConjuntoDesenho(exemplos, pares, meta, {"positivos": cpos, "negativos": cneg}, med)


# ---------------------------------------------------------------- reservatório do oráculo
@dataclass
class Reservatorio:
    entradas: List[Tuple[Grade, bool, str]]   # (grade, rótulo, origem), por chave_minimalidade
    contador: ContadorGeracao
    medicao: MedicaoGeracao
    hash: str


def reservatorio_oraculo(c: Conceito, n: int, particao: str, rng: random.Random, k: int,
                         permitir_confirmatorio: bool = False) -> Reservatorio:
    """k positivos construtivos, um negativo emparelhado por permutação e um quase-acerto por
    trocas para cada um; sem repetição; ordenado por chave_minimalidade (n, pretas, lexicográfica)."""
    verificar_particao(particao, permitir_confirmatorio)
    cont, med = ContadorGeracao(), MedicaoGeracao()
    entradas: Dict[Grade, Tuple[Grade, bool, str]] = {}
    with medir(med):
        for _ in range(k):
            g = gerar_positivo(c, n, particao, rng, cont, permitir_confirmatorio=permitir_confirmatorio)
            if g is None:
                continue
            entradas.setdefault(g, (g, True, "positivo_construtivo"))
            neg = negativo_emparelhado(g, c, rng, particao, "permutacao", cont, tentativas_permutacao=60,
                                       permitir_confirmatorio=permitir_confirmatorio)
            if neg is not None:
                entradas.setdefault(neg[0], (neg[0], False, "negativo_emparelhado"))
            qa = quase_acerto(g, c, rng, particao, cont, max_alvos_exaustivo=1600, L=400,
                              permitir_confirmatorio=permitir_confirmatorio)
            if qa is not None:
                entradas.setdefault(qa.grade, (qa.grade, False, "quase_acerto"))
    lista = sorted(entradas.values(), key=lambda e: chave_minimalidade(e[0]))
    return Reservatorio(lista, cont, med, hash_conjunto(e[0] for e in lista))


# ---------------------------------------------------------------- auditoria (PM2-PM5)
def tabela_geradores(nomes: Iterable[str], ns: Iterable[int], particao: str, k_pares: int,
                     semente: int) -> List[dict]:
    """Uma linha por (conceito, n): PM2 aceitação, PM3 vazão, PM4 emparelhamento, PM5 M10.
    Contadores e medições ficam em colunas separadas ("contadores" / "medicao")."""
    linhas = []
    for nome in nomes:
        for n in ns:
            rng = rng_piloto(semente)
            try:
                cj = conjunto_de_desenho(REGISTRO[nome], n, particao, k_pares, rng)
            except ConceitoDegenerado as e:
                linhas.append({"conceito": nome, "n": n, "degenerado": True, "motivo": e.info.get("motivo")})
                continue
            linhas.append({**{k: cj.metadados[k] for k in ("conceito", "n", "k_pares_obtido", "taxa_aceitacao",
                                                           "fracao_mesmo_numero_pretas", "m10", "metodos")},
                           "degenerado": False,
                           "contadores": {k: v.como_dict() for k, v in cj.contadores.items()},
                           "medicao": cj.medicao.como_dict()})
    return linhas
