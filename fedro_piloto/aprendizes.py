"""Aprendizes L-fix e L-lib com o laço dialético (documento 02, 2.4 e 2.9; documento 03, fase 5).

PROVENIÊNCIA (distinção permanente, verificada por construção):
  - AMBIENTE (proveniencia "ambiente"): tarefas, referências das tarefas de função, baterias de
    entradas, exemplos iniciais, oráculos, conjuntos de teste. Nada disso entra na biblioteca do
    aprendiz; o aprendiz só recebe pares (entrada, saída) e contraexemplos.
  - APRENDIZ: busca (enumerador.buscar) numa Tabela de uso "descoberta" (exigir_tabela_de_descoberta
    antes de cada tarefa). L-lib comprime SÓ as soluções que ele mesmo encontrou (Solucao
    "descoberta"); a Biblioteca em modo "autonomo" recusa "manual-teste" (duas barreiras: Biblioteca e
    Tabela). Programas manuais (programas_referencia) não são importados por este módulo.

LAÇO DIALÉTICO (2.9): exemplos iniciais da partição oraculo_treino (predicado: 2 positivos + 2
negativos, emparelhados em densidade quando possível; função: 4 pares entrada-saída calculados
pelas referências do ambiente); busca incremental do menor termo consistente; contraexemplo
mínimo do oráculo; até K rodadas; orçamento por tarefa. Tudo é lançado no LivroRazao.

CUSTO: contadores determinísticos (ContadorBusca, ContadorOraculoFuncao, ContadorCompressao,
ContadorGeracao) vão para o livro-razão; tempo e memória só por LivroRazao.medir (bloco separado).
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from . import geradores as G
from .avaliador import Contador, Contexto, OrcamentoEsgotado, aplicar, compilar
from .biblioteca import Biblioteca, Fragmento, Solucao, canonizar
from .dsl import (BOOL, FUN, GRADE, LP, POS, ErroProveniencia, Tabela, Termo, Tipo,
                  argumentos_e_resultado, constantes, exigir_tabela_de_descoberta, imprimir,
                  imprimir_legivel, tamanho, tipo_de, tipo_str)
from .certificados import descoberta_valida, emitir_descoberta
from .enumerador import ContadorBusca, buscar
from .grade import Grade, chave_minimalidade
from .oraculo import MedicaoOraculo, Oraculo
from .razao import LivroRazao
from .referencias import REGISTRO, fecho_ref

PROVENIENCIA_AMBIENTE = "ambiente"
PARTICAO_TREINO = "oraculo_treino"
PARTICAO_TESTE = "teste_int"
#: hiperparâmetros (documento 02, 2.9: K = 12; B e limiar reduzidos/fixados no piloto exploratório)
K_RODADAS = 12
POLITICAS_BUSCA = ("tamanho", "unigrama")
B_TAREFA = 20_000
LIMIAR_COMPRESSAO = 3
ORCAMENTO_PASSOS = 100_000
S_MAX = 30
#: n de Sem_n para tarefas sem argumento Grade (listas do ambiente têm comprimento ≤ 16 ≤ F(3))
N_SEM_LISTAS = 3
#: oráculo de função: n exaustivos (grades da partição) e reservatório amostrado de n = 4
NS_EXAUSTIVO_FUNCAO = (1, 2, 3)
N_RESERVATORIO_FUNCAO = 4
K_RESERVATORIO_FUNCAO = 40
NATUREZAS = ("predicado", "funcao")


# =====================================================================
# AMBIENTE: saídas, tarefas e referências das tarefas de função
# =====================================================================
class SaidaConjunto(frozenset):
    """Saída esperada cuja ordem não é especificada pela tarefa: igualdade de CONJUNTO com a lista
    devolvida pelo programa (tuple == SaidaConjunto recorre a este __eq__)."""

    def __eq__(self, outro):
        try:
            return frozenset(self) == frozenset(outro)
        except TypeError:
            return NotImplemented

    def __ne__(self, outro):
        r = self.__eq__(outro)
        return r if r is NotImplemented else not r

    __hash__ = frozenset.__hash__

    def __repr__(self):
        return f"SaidaConjunto({sorted(self)})"


@dataclass(frozen=True)
class Tarefa:
    """Tarefa do currículo (ambiente). Predicado: rótulo de referencias.REGISTRO[conceito].
    Função: saída de REFERENCIAS_FUNCAO[id], comparada exatamente ou como conjunto."""
    id: str
    tipo: Tipo
    natureza: str
    escada: str
    conceito: Optional[str] = None
    comparacao: str = "exata"
    proveniencia: str = PROVENIENCIA_AMBIENTE

    def __post_init__(self):
        if self.natureza not in NATUREZAS:
            raise ValueError(f"natureza inválida: {self.natureza}")
        if self.natureza == "predicado" and (self.conceito not in REGISTRO or self.tipo != FUN(GRADE, BOOL)):
            raise ValueError(f"predicado {self.id}: conceito desconhecido ou tipo errado")
        if self.natureza == "funcao" and self.id not in REFERENCIAS_FUNCAO:
            raise ValueError(f"função {self.id} sem referência do ambiente")
        if self.comparacao not in ("exata", "conjunto"):
            raise ValueError(self.comparacao)

    @property
    def tem_grade(self) -> bool:
        return argumentos_e_resultado(self.tipo)[0][0] == GRADE

    def como_dict(self) -> dict:
        return {"id": self.id, "tipo": tipo_str(self.tipo), "natureza": self.natureza, "escada": self.escada,
                "conceito": self.conceito, "comparacao": self.comparacao, "proveniencia": self.proveniencia}


def _pretos(g: Grade, ps) -> tuple:
    return tuple(q for q in ps if g.celula(q))


#: referências do AMBIENTE para as tarefas de função (Python direto, independentes da DSL)
REFERENCIAS_FUNCAO: Dict[str, Callable] = {
    "vizPretos": lambda g, p: _pretos(g, g.vizinhos(p)),
    "passo": lambda g, S: frozenset(S) | {q for s in S for q in g.vizinhos(s) if g.celula(q)},
    "fecho": lambda g, S: fecho_ref(g, list(S)),
    "componenteDe": lambda g, p: fecho_ref(g, [p]),
    "pretasDe": lambda g, r: _pretos(g, r),
    "descartar": lambda A, B: tuple(B[len(A):]),
    "noMaximo": lambda A, B: len(A) <= len(B),
    "mesmoNumero": lambda A, B: len(A) == len(B),
    # documento 05 (experimento mínimo): vizinhança preta de um conjunto (um passo, SEM incluir S)
    "expandir": lambda g, S: frozenset(q for s in S for q in g.vizinhos(s) if g.celula(q)),
    # controles de currículo NÃO relacionado (documento 05): sem vizinhança
    "pretasColuna1": lambda g, p: _pretos(g, [(i, 1) for i in range(1, g.n + 1)]),
    "semLinha1": lambda g, S: frozenset(S) - {(1, j) for j in range(1, g.n + 1)},
}

_GP, _GL, _LL = FUN(GRADE, POS, LP), FUN(GRADE, LP, LP), FUN(LP, LP, LP)
_LB, _PB = FUN(LP, LP, BOOL), FUN(GRADE, BOOL)

ESCADA_F2: List[Tarefa] = [
    Tarefa("ExistePreta", _PB, "predicado", "F2", "ExistePreta"),
    Tarefa("vizPretos", _GP, "funcao", "F2"),
    Tarefa("ParAdjacente", _PB, "predicado", "F2", "ParAdjacente"),
    Tarefa("NenhumaIsolada", _PB, "predicado", "F2", "NenhumaIsolada"),
    Tarefa("passo", _GL, "funcao", "F2", comparacao="conjunto"),
    Tarefa("fecho", _GL, "funcao", "F2", comparacao="conjunto"),
    Tarefa("componenteDe", _GP, "funcao", "F2", comparacao="conjunto"),
    Tarefa("UmComponente", _PB, "predicado", "F2", "UmComponente"),
]
ESCADA_F3: List[Tarefa] = [
    Tarefa("pretasDe", _GL, "funcao", "F3"),
    Tarefa("descartar", _LL, "funcao", "F3"),
    Tarefa("noMaximo", _LB, "funcao", "F3"),
    Tarefa("mesmoNumero", _LB, "funcao", "F3"),
    Tarefa("PrimeiraUltimaIguais", _PB, "predicado", "F3", "Igual_linha1_linhaN"),
    Tarefa("LinhasIguais", _PB, "predicado", "F3", "LinhasIguais"),
]
ESCADA = ESCADA_F2 + ESCADA_F3
TAREFAS_POR_ID: Dict[str, Tarefa] = {t.id: t for t in ESCADA}


def _unicos(xs) -> list:
    out, vistos = [], set()
    for x in xs:
        if x not in vistos:
            vistos.add(x)
            out.append(x)
    return out


def bateria_lp(g: Grade) -> List[tuple]:
    """Listas de posições (argumento S / r) derivadas da grade, em ordem fixa (ambiente)."""
    pretas, pos = tuple(g.pretas()), tuple(g.posicoes())
    return _unicos([(), pretas[:1], pretas[-1:], pretas, pos]
                   + [tuple(l) for l in g.linhas()] + [tuple(c) for c in g.colunas()])


def bateria_listas_pretas(g: Grade) -> List[tuple]:
    """Listas de células pretas por região (linhas, colunas, todas), para tarefas LP → LP → ·."""
    return _unicos([()] + [_pretos(g, l) for l in g.linhas()] + [_pretos(g, c) for c in g.colunas()]
                   + [tuple(g.pretas())])


def entradas_da_grade(tarefa: Tarefa, g: Grade) -> List[tuple]:
    """Argumentos da tarefa gerados a partir da grade g, em ordem fixa (bateria do ambiente)."""
    args, _ = argumentos_e_resultado(tarefa.tipo)
    if args == [GRADE, POS]:
        return [(g, p) for p in g.posicoes()]
    if args == [GRADE, LP]:
        return [(g, S) for S in bateria_lp(g)]
    if args == [LP, LP]:
        ls = bateria_listas_pretas(g)
        return _unicos([(A, B) for A in ls for B in ls])
    if args == [GRADE]:
        return [(g,)]
    raise ValueError(f"tipo de tarefa sem bateria: {tipo_str(tarefa.tipo)}")


def saida_referencia(tarefa: Tarefa, args: tuple):
    """Saída esperada (ambiente). Conjunto quando tarefa.comparacao == 'conjunto'."""
    if tarefa.natureza == "predicado":
        return REGISTRO[tarefa.conceito].rotulo(args[0])
    v = REFERENCIAS_FUNCAO[tarefa.id](*args)
    if tarefa.comparacao == "conjunto":
        return SaidaConjunto(v)
    return v


def n_semantica(tarefa: Tarefa, args: tuple) -> int:
    """n de Sem_n em que a hipótese é avaliada nesta entrada."""
    for a in args:
        if isinstance(a, Grade):
            return a.n
    return N_SEM_LISTAS


def valor_json(v):
    """Serialização determinística de entradas/saídas para os registros."""
    if isinstance(v, Grade):
        return v.serializar()
    if isinstance(v, SaidaConjunto):
        return {"conjunto": [list(p) for p in sorted(v)]}
    if isinstance(v, bool):
        return v
    if isinstance(v, (tuple, list, frozenset)):
        if all(isinstance(x, int) for x in v) and len(v) == 2 and not isinstance(v, frozenset):
            return list(v)
        xs = sorted(v) if isinstance(v, frozenset) else v
        return [valor_json(x) for x in xs]
    return v


# =====================================================================
# AMBIENTE: oráculo de função (compara saídas com a referência)
# =====================================================================
@dataclass
class ContadorOraculoFuncao:
    """Contadores determinísticos do oráculo de função."""
    consultas_contraexemplo: int = 0
    contraexemplos_devolvidos: int = 0
    sem_contraexemplo: int = 0
    grades_examinadas: int = 0
    entradas_examinadas: int = 0
    h_indefinido: int = 0
    saidas_referencia_calculadas: int = 0
    grades_reservatorio_geradas: int = 0

    def como_dict(self) -> dict:
        return asdict(self)


class OraculoFuncao:
    """Contraexemplo para tarefas de função: a primeira entrada, na ordem (n, pretas, lexicográfica da
    grade; depois a ordem da bateria), em que a saída da hipótese difere da referência.
    Domínio: grades da partição para n em NS_EXAUSTIVO_FUNCAO (todas) e um reservatório fixo por
    semente de K grades de n = 4 (mínimo garantido só na parte exaustiva). Proveniência "ambiente"."""

    def __init__(self, tarefa: Tarefa, rng: Optional[random.Random] = None, particao: str = PARTICAO_TREINO,
                 ns_exaustivo: Sequence[int] = NS_EXAUSTIVO_FUNCAO, n_reservatorio: int = N_RESERVATORIO_FUNCAO,
                 k_reservatorio: int = K_RESERVATORIO_FUNCAO, reservatorio: Optional[List[Grade]] = None):
        if tarefa.natureza != "funcao":
            raise ValueError("OraculoFuncao só para tarefas de função")
        G.verificar_particao(particao)
        self.tarefa = tarefa
        self.particao = particao
        self.proveniencia = PROVENIENCIA_AMBIENTE
        self.contador = ContadorOraculoFuncao()
        self.medicao = MedicaoOraculo()
        self.historico: List[dict] = []
        self._mostradas: Dict[str, Grade] = {}
        dominio: List[Tuple[Grade, bool]] = []
        for n in sorted(ns_exaustivo):
            dominio += [(g, True) for g in sorted(G.grades_da_particao(n, particao), key=chave_minimalidade)]
        if reservatorio is None:
            if rng is None:
                raise ValueError("rng necessário para o reservatório do oráculo de função")
            reservatorio = construir_reservatorio_funcao(rng, particao, n_reservatorio, k_reservatorio,
                                                         self.contador)
        if any(not G.na_particao(g, particao) for g in reservatorio):
            raise ValueError("reservatório fora da partição")
        dominio += [(g, False) for g in sorted(reservatorio, key=chave_minimalidade)]
        self.dominio = dominio
        self._saidas: Dict[tuple, object] = {}

    def saida(self, args: tuple):
        k = tuple(a.serializar() if isinstance(a, Grade) else a for a in args)
        v = self._saidas.get(k)
        if v is None:
            self.contador.saidas_referencia_calculadas += 1
            v = self._saidas[k] = saida_referencia(self.tarefa, args)
        return v

    def registrar_mostradas(self, grades) -> None:
        for g in grades:
            self._mostradas.setdefault(g.hash_hex(), g)

    def grades_mostradas(self) -> List[Grade]:
        return list(self._mostradas.values())

    def contraexemplo(self, h: Callable, livro: Optional[LivroRazao] = None, tarefa_id: str = "",
                      aprendiz_id: str = ""):
        """((args), saída de referência) da primeira discordância, ou None. h(args) -> valor;
        OrcamentoEsgotado torna h indefinida nessa entrada, o que CONTA COMO DISCORDÂNCIA (a entrada é
        devolvida com a saída de referência; sem aceitação vácua, como no Oraculo)."""
        import time
        t0 = time.perf_counter()
        examinadas = grades = 0
        resposta = None
        minimo = False
        indefinida = False
        for g, exaustiva in self.dominio:
            grades += 1
            for args in entradas_da_grade(self.tarefa, g):
                examinadas += 1
                try:
                    v = h(args)
                except OrcamentoEsgotado:
                    self.contador.h_indefinido += 1
                    resposta, minimo, indefinida = (args, self.saida(args)), exaustiva, True
                    break
                esperado = self.saida(args)
                if not (v == esperado):
                    resposta, minimo = (args, esperado), exaustiva
                    break
            if resposta is not None:
                break
        dt = time.perf_counter() - t0
        self.medicao.latencias_s.append(dt)
        self.medicao.tempo_parede_s += dt
        self.contador.consultas_contraexemplo += 1
        self.contador.grades_examinadas += grades
        self.contador.entradas_examinadas += examinadas
        if resposta is None:
            self.contador.sem_contraexemplo += 1
        else:
            self.contador.contraexemplos_devolvidos += 1
            for a in resposta[0]:
                if isinstance(a, Grade):
                    self.registrar_mostradas([a])
        self.historico.append({"indice": len(self.historico),
                               "entrada": valor_json(resposta[0]) if resposta else None,
                               "saida": valor_json(resposta[1]) if resposta else None,
                               "entradas_examinadas": examinadas, "minimo_garantido": minimo,
                               "resposta_indefinida": indefinida})
        if livro is not None:
            livro.registrar_varios(tarefa_id, aprendiz_id, nota="oraculo-funcao:contraexemplo",
                                   oraculo_consultas=1, oraculo_custo_ambiente=examinadas)
        return resposta

    def estado_deterministico(self) -> dict:
        return {"tarefa": self.tarefa.id, "particao": self.particao, "proveniencia": self.proveniencia,
                "contador": self.contador.como_dict(), "historico": list(self.historico),
                "grades_dominio": len(self.dominio),
                "hash_dominio": G.hash_conjunto(g for g, _ in self.dominio)}


def construir_reservatorio_funcao(rng: random.Random, particao: str, n: int, k: int,
                                  contador: Optional[ContadorOraculoFuncao] = None) -> List[Grade]:
    """k grades distintas de tamanho n da partição (amostragem natural), ordenadas por minimalidade."""
    cg = G.ContadorGeracao()
    out: Dict[Grade, None] = {}
    tent = 0
    while len(out) < k and tent < 50 * k:
        tent += 1
        out.setdefault(G.amostra_natural(n, rng, particao=particao, contador=cg), None)
    if contador is not None:
        contador.grades_reservatorio_geradas += cg.grades_geradas
    return sorted(out, key=chave_minimalidade)


# =====================================================================
# AMBIENTE: preparação de uma tarefa (exemplos iniciais, oráculo, teste)
# =====================================================================
@dataclass
class PreparoTarefa:
    tarefa: Tarefa
    exemplos: List[Tuple[tuple, object]]
    metodos_exemplos: List[str]
    teste: List[Tuple[tuple, object]]
    grades_geradas: int
    reservatorios: dict                  # predicado: {n: Reservatorio}; função: {"grades": [Grade]}
    geracao_reservatorios: int
    #: rotulagem na geração (chamadas de rótulo, permutações, trocas, consultas de tabela exaustiva)
    rotulos_geracao: int = 0
    #: entradas de teste descartadas por coincidirem, por VALOR, com o domínio do oráculo ou os exemplos
    teste_sobreposicoes_excluidas: int = 0
    #: grades de onde vieram as entradas (inclui as tarefas LP → LP → ·, cujos argumentos não são grades)
    grades_fonte: Dict[str, List[Grade]] = field(default_factory=dict)

    def grades(self) -> Dict[str, List[Grade]]:
        def gs(pares):
            return [a for args, _ in pares for a in args if isinstance(a, Grade)]
        out = {"exemplos": gs(self.exemplos), "teste": gs(self.teste)}
        for k, v in self.grades_fonte.items():
            out[k] = list(v)
        if self.tarefa.natureza == "predicado":
            out["reservatorio_oraculo"] = [e[0] for r in self.reservatorios.values() for e in r.entradas]
        else:
            out["reservatorio_oraculo"] = list(self.reservatorios["grades"])
        return out

    def como_dict(self) -> dict:
        g = self.grades()
        return {"tarefa": self.tarefa.id,
                "exemplos": [{"entrada": valor_json(a), "saida": valor_json(s)} for a, s in self.exemplos],
                "metodos_exemplos": list(self.metodos_exemplos),
                "num_teste": len(self.teste), "grades_geradas": self.grades_geradas,
                "geracao_reservatorios": self.geracao_reservatorios, "rotulos_geracao": self.rotulos_geracao,
                "teste_entradas_distintas": len({_chave_entrada(a) for a, _ in self.teste}),
                "teste_sobreposicoes_excluidas": self.teste_sobreposicoes_excluidas,
                "hashes": {k: G.hash_conjunto(v) for k, v in sorted(g.items())}}


class Ambiente:
    """Gera, de forma determinística por semente, o que o aprendiz recebe de cada tarefa; cria
    oráculos novos (contadores próprios) por aprendiz, com reservatórios partilhados."""
    proveniencia = PROVENIENCIA_AMBIENTE

    def __init__(self, semente: int, particao: str = PARTICAO_TREINO, k_reservatorio: int = 40,
                 ns_reservatorio: Sequence[int] = (5, 6), num_teste: int = 30,
                 k_reservatorio_funcao: int = K_RESERVATORIO_FUNCAO):
        if semente not in G.SEMENTES_PILOTO:
            raise ValueError(f"semente {semente} fora do intervalo do piloto")
        G.verificar_particao(particao)
        self.semente = semente
        self.particao = particao
        self.k_reservatorio = k_reservatorio
        self.ns_reservatorio = tuple(ns_reservatorio)
        self.num_teste = num_teste
        self.k_reservatorio_funcao = k_reservatorio_funcao
        self._preparos: Dict[str, PreparoTarefa] = {}

    PAPEIS = ("exemplos", "teste", "reservatorio")

    def _rng_tarefa(self, tarefa: Tarefa, papel: str) -> random.Random:
        """Fluxo por (semente, papel, tarefa) derivado por SHA-256 (geradores.rng_derivado): papéis e
        sementes vizinhas não coincidem, e incluir um conceito no REGISTRO não desloca as sementes."""
        if papel not in self.PAPEIS:
            raise ValueError(papel)
        return G.rng_derivado(self.semente, "tarefa", papel, tarefa.id)

    def preparar(self, tarefa: Tarefa) -> PreparoTarefa:
        p = self._preparos.get(tarefa.id)
        if p is None:
            p = self._preparos[tarefa.id] = self._preparar(tarefa)
        return p

    def _preparar(self, tarefa: Tarefa) -> PreparoTarefa:
        rng = self._rng_tarefa(tarefa, "exemplos")
        cg = G.ContadorGeracao()
        fonte_ex: List[Grade] = []
        fonte_te: List[Grade] = []
        if tarefa.natureza == "predicado":
            exemplos, metodos = exemplos_iniciais_predicado(REGISTRO[tarefa.conceito], rng, self.particao, cg)
        else:
            exemplos, metodos = exemplos_iniciais_funcao(tarefa, rng, self.particao, cg, fontes=fonte_ex)
        rng_o = self._rng_tarefa(tarefa, "reservatorio")
        rot_res = 0
        if tarefa.natureza == "predicado":
            c = REGISTRO[tarefa.conceito]
            res = {n: G.reservatorio_oraculo(c, n, self.particao, rng_o, self.k_reservatorio)
                   for n in self.ns_reservatorio}
            ger = sum(r.contador.grades_geradas for r in res.values())
            rot_res = sum(rotulos_de_geracao(r.contador) for r in res.values())
            excluir = set()     # teste_int e oraculo_treino são disjuntos por balde: entradas com Grade nunca coincidem
        else:
            co = ContadorOraculoFuncao()
            res = {"grades": construir_reservatorio_funcao(rng_o, self.particao, N_RESERVATORIO_FUNCAO,
                                                          self.k_reservatorio_funcao, co)}
            ger = co.grades_reservatorio_geradas
            excluir = set()
            if not tarefa.tem_grade:
                # entradas L Pos → L Pos → ·: listas derivadas da grade coincidem entre partições; exclui
                # do teste, por VALOR, o domínio do oráculo e os exemplos (achado de revisão)
                dominio = [g for n in NS_EXAUSTIVO_FUNCAO for g in G.grades_da_particao(n, self.particao)]
                dominio += list(res["grades"])
                excluir = {_chave_entrada(a) for g in dominio for a in entradas_da_grade(tarefa, g)}
                excluir |= {_chave_entrada(a) for a, _ in exemplos}
        rng_t = self._rng_tarefa(tarefa, "teste")
        info: dict = {}
        teste = conjunto_teste(tarefa, rng_t, self.num_teste, cg, fontes=fonte_te, excluir=excluir, info=info)
        return PreparoTarefa(tarefa, exemplos, metodos, teste, cg.grades_geradas, res, ger,
                             rotulos_geracao=rotulos_de_geracao(cg) + rot_res,
                             teste_sobreposicoes_excluidas=info.get("excluidas", 0),
                             grades_fonte={"exemplos_fonte": fonte_ex, "teste_fonte": fonte_te})

    def oraculo(self, tarefa: Tarefa):
        """Oráculo novo (contadores zerados) com os reservatórios partilhados da tarefa."""
        p = self.preparar(tarefa)
        if tarefa.natureza == "predicado":
            return Oraculo(tarefa.conceito, self.particao, reservatorios=p.reservatorios,
                           ns_reservatorio=self.ns_reservatorio, k_reservatorio=self.k_reservatorio)
        return OraculoFuncao(tarefa, particao=self.particao, reservatorio=p.reservatorios["grades"])


def exemplos_iniciais_predicado(c, rng: random.Random, particao: str, cg: G.ContadorGeracao,
                                ns: Sequence[int] = (4, 3)) -> Tuple[List[Tuple[tuple, bool]], List[str]]:
    """2 positivos construtivos e 2 negativos emparelhados em densidade (permutação ou troca); se a
    partição não admite negativo emparelhado em nenhum n de `ns` (verificado exaustivamente), o
    negativo é sorteado entre os negativos da partição (método registrado "natural-sem-par")."""
    pos: List[Grade] = []
    neg: List[Grade] = []
    metodos: List[str] = []
    for n in ns:
        d = G.degenerado(c, n, particao, rng)
        if not d["positivos_possiveis"]:
            continue
        tent = 0
        while len(pos) < 2 and tent < 20:
            tent += 1
            g = G.gerar_positivo(c, n, particao, rng, cg, tentativas=500)
            if g is None or g in pos:
                continue
            pos.append(g)
            metodos.append(f"positivo-construtivo:n={n}")
            if d["negativos_emparelhados_possiveis"]:
                r = G.negativo_emparelhado(g, c, rng, particao, "auto", cg)
                if r is not None and r[0] not in neg:
                    neg.append(r[0])
                    metodos.append(f"negativo-{r[2]}:n={n}")
        if len(pos) >= 2:
            break
    for n in ns:
        if len(neg) >= 2:
            break
        candidatos = [g for g in G.grades_da_particao(n, particao) if not c.rotulo(g) and g not in neg]
        cg.consultas_tabela_exaustiva += len(G.grades_da_particao(n, particao))
        while candidatos and len(neg) < 2:
            g = candidatos.pop(rng.randrange(len(candidatos)))
            neg.append(g)
            metodos.append(f"negativo-natural-sem-par:n={n}")
    if len(neg) < 2:
        # capacidade da partição (p. ex. ExistePreta: o único negativo é a grade vazia, e só a de n = 3
        # está em oraculo_treino entre n = 3 e 4): usa os negativos existentes e registra o desvio
        metodos.append(f"negativos-insuficientes-na-particao:{len(neg)}")
    if len(pos) < 2 or not neg:
        raise G.ConceitoDegenerado({"conceito": c.nome, "motivo": "exemplos iniciais insuficientes"})
    exemplos: List[Tuple[tuple, bool]] = []
    for i in range(max(len(pos), len(neg))):
        if i < len(pos):
            exemplos.append(((pos[i],), True))
        if i < len(neg):
            exemplos.append(((neg[i],), False))
    return exemplos, metodos


def exemplos_iniciais_funcao(tarefa: Tarefa, rng: random.Random, particao: str, cg: G.ContadorGeracao,
                             ns: Sequence[int] = (3, 4), k: int = 4,
                             fontes: Optional[List[Grade]] = None) -> Tuple[List[Tuple[tuple, object]], List[str]]:
    """k pares (entrada, saída de referência) com grades naturais da partição. Saída Bool: metade
    verdadeiro, metade falso; saída lista: pelo menos k−1 saídas não vazias. Entradas distintas."""
    _, res = argumentos_e_resultado(tarefa.tipo)
    out: List[Tuple[tuple, object]] = []
    metodos: List[str] = []
    vistos = set()
    tent = 0
    while len(out) < k and tent < 2000:
        tent += 1
        n = ns[len(out) % len(ns)]
        g = G.amostra_natural(n, rng, particao=particao, contador=cg)
        ents = entradas_da_grade(tarefa, g)
        args = ents[rng.randrange(len(ents))]
        chave = (g, tuple(a for a in args if not isinstance(a, Grade)))
        if chave in vistos:
            continue
        s = saida_referencia(tarefa, args)
        if res == BOOL:
            if sum(1 for _, y in out if y == s) >= k // 2:
                continue
        elif len(s) == 0 and sum(1 for _, y in out if len(y) == 0) >= 1:
            continue
        vistos.add(chave)
        out.append((args, s))
        metodos.append(f"natural:n={n}")
        if fontes is not None:
            fontes.append(g)
    if len(out) < k:
        raise G.ConceitoDegenerado({"conceito": tarefa.id, "motivo": "exemplos iniciais insuficientes"})
    return out, metodos


def _chave_entrada(args: tuple) -> tuple:
    """Chave por VALOR de uma entrada (grades pela serialização; listas como tuplas)."""
    return tuple(a.serializar() if isinstance(a, Grade) else a for a in args)


def rotulos_de_geracao(cg: G.ContadorGeracao) -> int:
    """Custo de rotulagem da geração (campo geracao_rotulos do livro-razão)."""
    return cg.chamadas_rotulo + cg.permutacoes_avaliadas + cg.trocas_avaliadas + cg.consultas_tabela_exaustiva


def conjunto_teste(tarefa: Tarefa, rng: random.Random, num: int, cg: G.ContadorGeracao,
                   ns: Sequence[int] = (4, 5, 6), particao: str = PARTICAO_TESTE,
                   fontes: Optional[List[Grade]] = None, excluir: Optional[set] = None,
                   info: Optional[dict] = None) -> List[Tuple[tuple, object]]:
    """Pares de teste (partição teste_int, distribuição natural); funções: até 3 entradas por grade.
    Amostragem SEM reposição (entradas distintas por valor) e sem as entradas de `excluir` (por valor:
    domínio do oráculo e exemplos, para tarefas cujas entradas não contêm a grade)."""
    out = []
    usadas = set()
    excluir = excluir or set()
    excluidas = 0
    for i in range(num):
        g = G.amostra_natural(ns[i % len(ns)], rng, particao=particao, contador=cg)
        if fontes is not None:
            fontes.append(g)
        ents = entradas_da_grade(tarefa, g)
        livres = []
        for a in ents:
            k = _chave_entrada(a)
            if k in excluir:
                excluidas += 1
                continue
            if k not in usadas:
                livres.append(a)
        k_max = 1 if tarefa.natureza == "predicado" else 3
        for args in rng.sample(livres, min(k_max, len(livres))):
            usadas.add(_chave_entrada(args))
            out.append((args, saida_referencia(tarefa, args)))
    if info is not None:
        info["excluidas"] = excluidas
    return out


# =====================================================================
# APRENDIZES
# =====================================================================
@dataclass
class ResultadoTarefa:
    """Resultado determinístico de uma tarefa para um aprendiz (sem tempo nem memória)."""
    tarefa_id: str
    aprendiz_id: str
    aceita: bool
    motivo_fim: str
    rodadas: int
    hipotese: Optional[str]
    hipotese_legivel: Optional[str]
    tamanho: Optional[int]
    hipoteses: List[dict]
    contador_busca: dict
    custo_aprendiz: int
    custo_ambiente: int
    acuracia_teste: Optional[float]
    constantes_biblioteca_usadas: List[str] = field(default_factory=list)
    reutilizacoes: Dict[str, int] = field(default_factory=dict)
    abstracoes_novas: List[dict] = field(default_factory=list)
    oraculo: dict = field(default_factory=dict)
    exemplos_finais: int = 0
    #: True quando a busca parou por MemoryError (recurso da máquina): resultado não conta como falha
    inconclusivo_recurso: bool = False
    #: contador INDEPENDENTE da compressão desta tarefa (ContadorCompressao), para conciliação com o livro
    compressao_subtermos: int = 0
    #: resumo do conjunto de teste (documento 05, missão 3): classes presentes, acurácia balanceada e
    #: se o conjunto é DEGENERADO (uma só classe / uma só saída): nesse caso a acurácia não é evidência
    teste_resumo: dict = field(default_factory=dict)
    #: custos de folha em vigor na busca desta tarefa (política de busca "unigrama"); {} = tamanho
    custos_folha: dict = field(default_factory=dict)

    def como_dict(self) -> dict:
        return asdict(self)


class Hipotese:
    """Hipótese avaliável pelo oráculo: predicado h(g) ou função h(args). Acumula os passos de Sem_n
    gastos nas avaliações (inclusive as abortadas por orçamento), lançados como
    oraculo_passos_hipotese (custo do ambiente)."""

    def __init__(self, ev, tarefa: Tarefa, tabela: Tabela, orcamento_passos: int):
        self.ev, self.tarefa, self.tabela, self.orc = ev, tarefa, tabela, orcamento_passos
        self.passos = 0

    def __call__(self, x):
        args = (x,) if isinstance(x, Grade) else tuple(x)
        c = Contador(self.orc)
        try:
            return aplicar(self.ev({}, Contexto(n_semantica(self.tarefa, args), c, self.tabela)), *args)
        finally:
            self.passos += c.passos


def _rotulos_oraculo(o) -> int:
    """Rótulos/saídas de referência calculados pelo oráculo (planejamento incluído)."""
    if isinstance(o, OraculoFuncao):
        return o.contador.saidas_referencia_calculadas
    return o.contador.rotulos_calculados + getattr(o, "rotulos_planejamento", 0)


def _ultima_resposta_indefinida(o) -> bool:
    if not o.historico:
        return False
    h = o.historico[-1]
    return h.get("resposta_indefinida", False) if isinstance(h, dict) else getattr(h, "resposta_indefinida", False)


class AprendizBase:
    """Laço dialético comum. Subclasses definem `nome` e o que acontece após uma aceitação."""
    nome = "L-base"

    def __init__(self, tabela: Tabela, livro: LivroRazao, B: int = B_TAREFA, K: int = K_RODADAS,
                 orcamento_passos: int = ORCAMENTO_PASSOS, s_max: int = S_MAX, rotulo_base: Optional[str] = None,
                 kw_enumerador: Optional[dict] = None, politica_busca: str = "tamanho"):
        if tabela.uso == "base":
            tabela = tabela.para_aprendiz(f"{tabela.nome}/{self.nome}")
        if politica_busca not in POLITICAS_BUSCA:
            raise ValueError(f"política de busca inválida: {politica_busca!r}")
        #: "tamanho": enumeração por tamanho; "unigrama": custo de folha 1 para constantes já usadas em
        #: soluções aceitas DESTE aprendiz (e entradas da sua biblioteca), 2 para as demais. Igual para
        #: L-fix e L-lib: isola o efeito da biblioteca (documento 05, missão 4).
        self.politica_busca = politica_busca
        self._constantes_usadas: set = set()
        exigir_tabela_de_descoberta(tabela)
        self.tabela = tabela
        self.livro = livro
        self.B = int(B)
        self.K = int(K)
        self.orcamento_passos = orcamento_passos
        self.s_max = s_max
        self.base = rotulo_base or tabela.nome.split("/")[0]
        self.kw_enumerador = dict(kw_enumerador or {})
        self.resultados: List[ResultadoTarefa] = []
        #: MEDIÇÕES reais do oráculo por tarefa (latência por consulta); nunca no bloco determinístico
        self.medicoes_oraculo: List[dict] = []
        self._custo_compressao_ultima = 0

    @property
    def aprendiz_id(self) -> str:
        return f"{self.nome}@{self.base}"

    def tabela_corrente(self) -> Tabela:
        return self.tabela

    # ---------------------------------------------------------------- hipótese avaliada
    def _hipotese(self, termo: Termo, tarefa: Tarefa, tabela: Tabela) -> "Hipotese":
        return Hipotese(compilar(termo), tarefa, tabela, self.orcamento_passos)

    def _avaliar_teste(self, termo: Termo, tarefa: Tarefa, teste, tabela: Tabela) -> Tuple[float, int]:
        acc, passos, _ = self._avaliar_teste_resumo(termo, tarefa, teste, tabela)
        return acc, passos

    def _avaliar_teste_resumo(self, termo: Termo, tarefa: Tarefa, teste, tabela: Tabela) -> Tuple[float, int, dict]:
        """Acurácia, passos e RESUMO: por classe (predicados) ou por saída distinta (funções). Um
        conjunto com uma só classe (ou uma só saída) é marcado degenerado: a acurácia nele não informa
        generalização, e a acurácia balanceada é indefinida (documento 05, missão 3)."""
        ev = compilar(termo)
        acertos = passos = 0
        por_classe: Dict[str, List[int]] = {}
        for args, esperado in teste:
            c = Contador(self.orcamento_passos)
            ok = 0
            try:
                v = aplicar(ev({}, Contexto(n_semantica(tarefa, args), c, tabela)), *args)
                ok = int(v == esperado)
            except OrcamentoEsgotado:
                pass
            passos += c.passos
            acertos += ok
            chave = str(esperado) if tarefa.natureza == "predicado" else repr(valor_json(esperado))
            por_classe.setdefault(chave, [0, 0])
            por_classe[chave][0] += ok
            por_classe[chave][1] += 1
        acc = acertos / len(teste) if teste else float("nan")
        classes = {k: {"acertos": a, "total": t} for k, (a, t) in sorted(por_classe.items())}
        degenerado = len(por_classe) < 2
        bal = None if degenerado or not teste else sum(a / t for a, t in por_classe.values()) / len(por_classe)
        resumo = {"num": len(teste), "classes": classes if tarefa.natureza == "predicado" else len(por_classe),
                  "degenerado": degenerado, "acuracia": acc, "acuracia_balanceada": bal,
                  "aviso": ("conjunto de teste DEGENERADO: acurácia sem valor como evidência de generalização"
                            if degenerado else "")}
        if tarefa.natureza == "predicado":
            resumo["positivos"] = por_classe.get("True", [0, 0])[1]
            resumo["negativos"] = por_classe.get("False", [0, 0])[1]
        return acc, passos, resumo

    # ---------------------------------------------------------------- laço dialético
    def resolver(self, tarefa: Tarefa, ambiente: Ambiente) -> ResultadoTarefa:
        livro, tid, aid = self.livro, tarefa.id, self.aprendiz_id
        tabela = self.tabela_corrente()
        exigir_tabela_de_descoberta(tabela)
        prep = ambiente.preparar(tarefa)
        oraculo = ambiente.oraculo(tarefa)
        livro.registrar(tid, aid, "geracao_grades", prep.grades_geradas, "exemplos+teste")
        livro.registrar(tid, aid, "geracao_grades", prep.geracao_reservatorios, "oraculo:reservatorios")
        livro.registrar(tid, aid, "geracao_rotulos", prep.rotulos_geracao, "exemplos+teste+reservatorios")
        rot0 = 0   # o planejamento do oráculo (rótulos na construção) também é custo desta tarefa
        oraculo.registrar_mostradas([a for args, _ in prep.exemplos for a in args if isinstance(a, Grade)])
        exemplos = list(prep.exemplos)
        cb = ContadorBusca()
        estado = None
        hipoteses: List[dict] = []
        termo = None
        aceita = False
        motivo = "rodadas"
        inconclusivo = False
        kw = dict(s_max=self.s_max, orcamento_passos=self.orcamento_passos, orcamento_enumeracao=self.B)
        if not tarefa.tem_grade:
            kw["n"] = N_SEM_LISTAS
        kw.update(self.kw_enumerador)
        custos = self.custos_folha_correntes(tabela)
        if custos:
            kw["custos_folha"] = custos
        with livro.medir(tid, aid):
            for rodada in range(1, self.K + 1):
                restante = max(0, self.B - cb.candidatos_avaliados)
                try:
                    termo, estado = buscar(tabela, tarefa.tipo, exemplos, restante, cb, estado, **kw)
                except (MemoryError, SystemError):
                    # (SystemError: alocação negada sob RLIMIT_AS dentro do interpretador) limite de memória do processo (piloto.limitar_memoria): depende da máquina, do
                    # alocador e do escalonamento -> INCONCLUSIVO (nunca "falha"; achado de revisão)
                    termo, motivo, inconclusivo = None, "inconclusivo_recurso", True
                    break
                if termo is None:
                    if estado.enumeracao_esgotada():
                        motivo = "orcamento_enumeracao"
                    elif cb.candidatos_avaliados >= self.B:
                        motivo = "orcamento_exemplos"
                    else:
                        motivo = "s_max"
                    break
                h = self._hipotese(termo, tarefa, tabela)
                if tarefa.natureza == "predicado":
                    ce = oraculo.contraexemplo(h, livro=livro, tarefa_id=tid, aprendiz_id=aid)
                    novo = ((ce[0],), ce[1]) if ce is not None else None
                else:
                    novo = oraculo.contraexemplo(h, livro=livro, tarefa_id=tid, aprendiz_id=aid)
                livro.registrar(tid, aid, "oraculo_passos_hipotese", h.passos, "oraculo:passos-de-h")
                indef = bool(_ultima_resposta_indefinida(oraculo))
                hipoteses.append({"rodada": rodada, "termo": imprimir(termo), "legivel": imprimir_legivel(termo),
                                  "tamanho": tamanho(termo),
                                  "contraexemplo": None if novo is None else
                                  {"entrada": valor_json(novo[0]), "saida": valor_json(novo[1]),
                                   "hipotese_indefinida": indef}})
                if novo is None:
                    aceita, motivo = True, "aceita"
                    break
                exemplos.append(novo)
            livro.registrar(tid, aid, "busca_candidatos", cb.candidatos_avaliados, "exemplos")
            livro.registrar(tid, aid, "enumeracao_candidatos", cb.enumeracao_candidatos_avaliados, "enumeracao-oe")
            livro.registrar(tid, aid, "busca_passos", cb.passos_avaliacao, "exemplos")
            livro.registrar(tid, aid, "enumeracao_passos", cb.enumeracao_passos, "enumeracao-oe")
            livro.registrar(tid, aid, "geracao_rotulos", _rotulos_oraculo(oraculo) - rot0, "oraculo:rotulos")
            acc = None
            resumo_teste: dict = {}
            if aceita:
                acc, passos_teste, resumo_teste = self._avaliar_teste_resumo(termo, tarefa, prep.teste, tabela)
                livro.registrar(tid, aid, "avaliacao_passos", passos_teste, "teste_int")
                self._constantes_usadas |= set(constantes(termo))
            usadas = sorted({c for c in constantes(termo) if c in tabela and not tabela[c].eh_fornecida}) \
                if aceita else []
        e = livro.entrada(tid, aid)
        res = ResultadoTarefa(
            tid, aid, aceita, motivo, len(hipoteses), imprimir(termo) if aceita else None,
            imprimir_legivel(termo) if aceita else None, tamanho(termo) if aceita else None, hipoteses,
            cb.como_dict(), e.total_aprendiz(), e.total_ambiente(), acc, usadas, {}, [],
            oraculo.estado_deterministico(), len(exemplos), inconclusivo_recurso=inconclusivo,
            teste_resumo=resumo_teste, custos_folha=dict(custos))
        self.resultados.append(res)
        cert = None
        if aceita:
            # o termo saiu de enumerador.buscar (certificado de busca) e foi aceito pelo oráculo
            cert = emitir_descoberta(estado.certificado, termo, tid, aid, len(self.resultados) - 1)
        self._custo_compressao_ultima = 0
        with livro.medir(tid, aid):
            reuso, novas = self._apos_tarefa(tarefa, termo if aceita else None, cert)
        res.reutilizacoes, res.abstracoes_novas = reuso, novas
        res.compressao_subtermos = self._custo_compressao_ultima
        self.medicoes_oraculo.append({"tarefa_id": tid, "latencias_s": list(oraculo.medicao.latencias_s)})
        res.custo_aprendiz, res.custo_ambiente = e.total_aprendiz(), e.total_ambiente()
        return res

    def _apos_tarefa(self, tarefa: Tarefa, termo: Optional[Termo], certificado=None) -> Tuple[Dict[str, int], List[dict]]:
        return {}, []

    def custos_folha_correntes(self, tabela: Tabela) -> Dict[str, int]:
        """Custos de folha da política "unigrama" (vazio = tamanho). Só depende das soluções aceitas por
        ESTE aprendiz e da sua biblioteca; antes da primeira aceitação todas as constantes custam 1."""
        if self.politica_busca != "unigrama" or not self._constantes_usadas:
            return {}
        baratas = set(self._constantes_usadas)
        # entradas de biblioteca (descobertas) custam 1 se o seu corpo só usa constantes baratas
        mudou = True
        while mudou:
            mudou = False
            for p in tabela:
                if not p.eh_fornecida and p.nome not in baratas and p.corpo is not None and \
                        set(constantes(p.corpo)) <= baratas:
                    baratas.add(p.nome)
                    mudou = True
        return {p.nome: (1 if p.nome in baratas else 2) for p in tabela}

    def executar(self, tarefas: Sequence[Tarefa], ambiente: Ambiente) -> List[ResultadoTarefa]:
        return [self.resolver(t, ambiente) for t in tarefas]

    def relatorio(self) -> dict:
        return {"aprendiz": self.aprendiz_id, "nome": self.nome, "base": self.base, "B": self.B, "K": self.K,
                "tabela": self.tabela_corrente().nome, "uso_tabela": self.tabela_corrente().uso,
                "resultados": [r.como_dict() for r in self.resultados]}


class LFix(AprendizBase):
    """L-fix: busca em base fixa; recebe o mesmo currículo (inclusive tarefas de função)."""
    nome = "L-fix"


class LLib(AprendizBase):
    """L-lib: L-fix + compressão após cada tarefa aceita, só com as próprias soluções ("descoberta").

    promover_funcoes=True é uma VARIANTE declarada (desvio, não o braço do protocolo): a solução aceita
    de cada tarefa de FUNÇÃO entra também como entrada de biblioteca (metodo "promocao-solucao"),
    porque a regra de compressão (ocorrências ≥ 2) nunca transforma a solução isolada de um degrau em
    abstração, ao passo que a tabela 2.8.1 mede os degraus "com os degraus anteriores"."""
    nome = "L-lib"

    def __init__(self, tabela: Tabela, livro: LivroRazao, limiar: int = LIMIAR_COMPRESSAO,
                 biblioteca: Optional[Biblioteca] = None, promover_funcoes: bool = False,
                 max_novas: Optional[int] = None, max_pares: Optional[int] = 20_000, **kw):
        if biblioteca is None:
            biblioteca = Biblioteca(tabela, "autonomo", max_pares=max_pares)
        if biblioteca.modo != "autonomo":
            raise ErroProveniencia("L-lib exige Biblioteca em modo 'autonomo'")
        if promover_funcoes:
            self.nome = "L-lib+f"
        super().__init__(biblioteca.tabela, livro, rotulo_base=kw.pop("rotulo_base", tabela.nome.split("/")[0]),
                         **kw)
        self.biblioteca = biblioteca
        self.limiar = int(limiar)
        self.promover_funcoes = promover_funcoes
        self.max_novas = max_novas

    def tabela_corrente(self) -> Tabela:
        return self.biblioteca.tabela

    def _apos_tarefa(self, tarefa: Tarefa, termo: Optional[Termo], certificado=None):
        if termo is None:
            return {}, []
        if not descoberta_valida(certificado, termo=termo, tarefa_id=tarefa.id) or \
                certificado.aprendiz_id != self.aprendiz_id:
            raise ErroProveniencia(f"{tarefa.id}: solução sem certificado deste aprendiz")
        r = self.resultados[certificado.indice_resultado]
        if not (r.aceita and r.tarefa_id == tarefa.id and r.hipotese == imprimir(termo)):
            raise ErroProveniencia(f"{tarefa.id}: certificado não corresponde a um ResultadoTarefa aceito")
        bib = self.biblioteca
        antes = bib.contador.copia()
        sol = Solucao(termo, tarefa.id, "descoberta", certificado)
        reuso = bib.registrar_reuso(sol, tarefa.id)
        novas = bib.comprimir([sol], self.limiar, self.max_novas)
        if self.promover_funcoes and tarefa.natureza == "funcao":
            novas.append(self._promover(tarefa))
        custo = bib.contador.menos(antes).subtermos_examinados
        self._custo_compressao_ultima = custo
        self.livro.registrar(tarefa.id, self.aprendiz_id, "compressao_subtermos", custo, "compressao")
        return reuso, [_desc_entrada(bib, p.nome) for p in novas]

    def _promover(self, tarefa: Tarefa):
        bib = self.biblioteca
        corpus = next(s for s in bib.solucoes if s.tarefa_id == tarefa.id)
        t = canonizar(corpus.termo)
        k = 0
        u = t
        while u[0] == "lam":
            k += 1
            u = u[3]
        if not descoberta_valida(corpus.certificado, tarefa_id=tarefa.id):
            raise ErroProveniencia(f"{tarefa.id}: promoção exige solução certificada")
        # rótulo de origem conferido por Biblioteca._verificar_no_corpus (o fragmento é a solução certificada)
        frag = Fragmento(t, tipo_de(t, {}, bib.tabela), 1, 0, (tarefa.id,), k, 0, "promocao-solucao",
                         frozenset({"descoberta"}))
        return bib.adicionar(frag, "descoberta")

    def lesionar(self) -> List[dict]:
        """ABLAÇÃO (documento 05, missão 2): remove da tabela do aprendiz todas as entradas descobertas,
        sem apagar o registro do que foi descoberto. A biblioteca passa a uma tabela nova só com as
        primitivas fornecidas; as entradas removidas ficam listadas em `lesionadas`."""
        bib = self.biblioteca
        removidas = [_desc_entrada(bib, nome) for nome in bib.entradas]
        base = Tabela(bib.tabela.nome + "/lesao", [p for p in bib.tabela if p.eh_fornecida], "base")
        bib.tabela = base.para_aprendiz(bib.tabela.nome + "/lesao")
        bib.lesionadas = removidas
        bib.entradas = {}
        bib.solucoes = []           # o corpus também é esquecido: nada do antes da lesão pode ser recomprimido
        self._constantes_usadas = {c for c in self._constantes_usadas if c in bib.tabela}
        return removidas

    def relatorio(self) -> dict:
        d = super().relatorio()
        d["limiar"] = self.limiar
        d["promover_funcoes"] = self.promover_funcoes
        d["politica_busca"] = self.politica_busca
        d["biblioteca"] = self.biblioteca.relatorio()
        d["lesionadas"] = list(getattr(self.biblioteca, "lesionadas", []))
        return d


def _desc_entrada(bib: Biblioteca, nome: str) -> dict:
    reg = bib.entradas[nome]
    p = reg.primitiva
    return {"nome": nome, "proveniencia": p.proveniencia, "categoria": p.categoria(), "tipo": tipo_str(p.tipo),
            "corpo": imprimir(p.corpo), "legivel": imprimir_legivel(p.corpo), "tamanho": tamanho(p.corpo),
            "metodo": reg.fragmento.metodo, "pontuacao": reg.fragmento.pontuacao,
            "tarefas_origem": list(reg.tarefas_origem)}


def abstracoes(aprendiz: AprendizBase) -> List[dict]:
    """Entradas de biblioteca de um aprendiz com proveniência, origem e reutilizações."""
    if not isinstance(aprendiz, LLib):
        return []
    return aprendiz.biblioteca.relatorio()["entradas"]
