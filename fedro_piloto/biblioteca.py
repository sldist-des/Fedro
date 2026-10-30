"""Compressão do aprendiz L-lib (documento 02, 2.4; documento 03, seção 3 e U21–U22).

Extração de fragmentos a partir de soluções (termos fechados):
  - fechamento: cada subtermo, com as variáveis livres (ligadas acima dele) fechadas em parâmetros
    λ na ordem de ocorrência;
  - anti-unificação de pares de subtermos (generalização mínima) com até `max_buracos` buracos,
    cada buraco virando um parâmetro extra (variáveis livres pareadas não contam como buraco).
Os fragmentos são canonizados (renomeação α determinística dos binders) e suas ocorrências são
contadas, entre TODAS as soluções, por casamento de padrão módulo renomeação (ocorrências não
sobrepostas, na mesma ordem em que a reescrita as substituiria).
Pontuação = (ocorrências − 1) × (tamanho − 1), tamanho = |termo fechado| (documento 03, seção 3).

Proveniência (distinção permanente):
  - Solucao.proveniencia "descoberta" = encontrada pelo aprendiz; "manual-teste" = escrita à mão;
  - Biblioteca(modo="autonomo"): tabela de uso "descoberta"; só aceita Solucao "descoberta" e só
    cria entradas "descoberta" (manual-teste é recusado aqui E pela própria Tabela: duas barreiras);
  - Biblioteca(modo="mecanismo-teste"): tabela de uso "referencia" (nunca dada a aprendizes);
    toda entrada é "manual-teste", mesmo que extraída de soluções declaradas "descoberta".
Custo: ContadorCompressao (determinístico, nós examinados). Nenhuma medição real aqui.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass, field
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Tuple

from .dsl import (AP, C, ErroProveniencia, ErroTipo, LAMS, Primitiva, REGISTRO_BASE, Tabela, Termo, Tipo,
                  constantes, eh_fechado, entrada_biblioteca, exigir_tabela_de_descoberta, imprimir,
                  imprimir_legivel, ocorrencias, tamanho, tipo_de, tipo_str, variaveis_livres)

MODOS = ("autonomo", "mecanismo-teste")
PROVENIENCIAS_SOLUCAO = ("descoberta", "manual-teste")
#: termos passados sem Solucao (só permitido fora do modo autônomo)
NAO_DECLARADA = "nao-declarada"


# =====================================================================
# Soluções, contador e fragmentos
# =====================================================================
@dataclass(frozen=True)
class Solucao:
    """Solução aceita de uma tarefa. proveniencia: "descoberta" (encontrada pelo aprendiz) ou
    "manual-teste" (programa escrito à mão, só para testar o mecanismo).

    "descoberta" exige `certificado` (certificados.CertificadoDescoberta, emitido só por
    AprendizBase.resolver para um termo devolvido por enumerador.buscar e aceito pelo oráculo) da
    MESMA tarefa; o rótulo de texto sozinho é recusado. O termo pode diferir do certificado só nas
    reescritas internas da Biblioteca (constantes novas); na entrada do corpus deve ser igual."""
    termo: Termo
    tarefa_id: str
    proveniencia: str
    certificado: Optional[object] = field(default=None, compare=False, repr=False)

    def __post_init__(self):
        from .certificados import descoberta_valida
        if self.proveniencia not in PROVENIENCIAS_SOLUCAO:
            raise ErroProveniencia(f"proveniência de solução inválida: {self.proveniencia!r}")
        if not eh_fechado(self.termo):
            raise ValueError(f"solução de {self.tarefa_id} não é fechada")
        if self.proveniencia == "descoberta" and not descoberta_valida(self.certificado, tarefa_id=self.tarefa_id):
            raise ErroProveniencia(
                f"solução {self.tarefa_id!r} rotulada 'descoberta' sem certificado do laço do aprendiz")

    @property
    def termo_aceito(self) -> Optional[Termo]:
        """Termo exatamente como foi aceito (do certificado), antes de reescritas da biblioteca."""
        return self.certificado.termo if self.certificado is not None else None


@dataclass
class ContadorCompressao:
    """Custo determinístico da compressão, em nós de termo examinados."""
    nos_enumerados: int = 0        # subtermos visitados ao indexar o corpus
    nos_antiunificacao: int = 0    # pares de nós comparados na anti-unificação
    nos_casamento: int = 0         # pares de nós comparados no casamento e na reescrita
    pares_antiunificacao: int = 0  # pares de subtermos anti-unificados
    pares_omitidos: int = 0        # pares não examinados por causa de max_pares
    candidatos_distintos: int = 0
    fragmentos_adicionados: int = 0

    @property
    def subtermos_examinados(self) -> int:
        """Unidade do livro-razão (campo compressao_subtermos)."""
        return self.nos_enumerados + self.nos_antiunificacao + self.nos_casamento

    def somar(self, outro: "ContadorCompressao") -> "ContadorCompressao":
        for k, v in asdict(outro).items():
            setattr(self, k, getattr(self, k) + v)
        return self

    def menos(self, anterior: "ContadorCompressao") -> "ContadorCompressao":
        return ContadorCompressao(**{k: v - getattr(anterior, k) for k, v in asdict(self).items()})

    def copia(self) -> "ContadorCompressao":
        return ContadorCompressao(**asdict(self))

    def como_dict(self) -> dict:
        d = asdict(self)
        d["subtermos_examinados"] = self.subtermos_examinados
        return d


@dataclass(frozen=True)
class Fragmento:
    """Abstração candidata: termo fechado canônico λx1..xk. corpo (k = num_parametros)."""
    termo_fechado: Termo
    tipo: Tipo
    ocorrencias: int
    pontuacao: int
    origem_ids: Tuple[str, ...]
    num_parametros: int = 0
    num_buracos: int = 0
    metodo: str = "fechamento"                 # "fechamento" | "antiunificacao"
    proveniencias_origem: FrozenSet[str] = frozenset()

    @property
    def tamanho(self) -> int:
        return tamanho(self.termo_fechado)

    @property
    def corpo(self) -> Termo:
        return _separar(self.termo_fechado, self.num_parametros)[1]

    def legivel(self) -> str:
        return imprimir_legivel(self.termo_fechado)

    def como_dict(self) -> dict:
        return {"termo": imprimir(self.termo_fechado), "legivel": self.legivel(), "tipo": tipo_str(self.tipo),
                "tamanho": self.tamanho, "ocorrencias": self.ocorrencias, "pontuacao": self.pontuacao,
                "origem_ids": list(self.origem_ids), "num_parametros": self.num_parametros,
                "num_buracos": self.num_buracos, "metodo": self.metodo,
                "proveniencias_origem": sorted(self.proveniencias_origem)}


def pontuacao(ocorr: int, tam: int) -> int:
    """(ocorrências − 1) × (tamanho − 1)."""
    return (ocorr - 1) * (tam - 1)


# =====================================================================
# Utilidades sobre termos
# =====================================================================
_PREFIXO_TIPO = {"Grade": "g", "Pos": "p", "Bool": "b", "Lista": "l", "Fun": "f"}


def canonizar(t: Termo) -> Termo:
    """Renomeação α determinística: binders renomeados em pré-ordem (g1, p2, l3, ...).
    Dois termos α-equivalentes têm a mesma forma canônica. Variáveis livres não mudam."""
    cont = [0]

    def rec(u, env):
        k = u[0]
        if k == "v":
            return ("v", env.get(u[1], u[1]))
        if k == "c":
            return u
        if k == "ap":
            return ("ap", rec(u[1], env), rec(u[2], env))
        if k == "lam":
            cont[0] += 1
            novo = f"{_PREFIXO_TIPO[u[2][0]]}{cont[0]}"
            e2 = dict(env)
            e2[u[1]] = novo
            return ("lam", novo, u[2], rec(u[3], e2))
        if k == "fix":
            return ("fix", u[1], rec(u[2], env))
        raise ValueError(f"termo inválido: {u!r}")
    return rec(t, {})


def eta_reduzir(t: Termo) -> Termo:
    """Forma η-normal: λx. f x ↦ f quando x não ocorre livre em f (recursivo, de dentro para fora)."""
    k = t[0]
    if k in ("v", "c"):
        return t
    if k == "ap":
        return ("ap", eta_reduzir(t[1]), eta_reduzir(t[2]))
    if k == "fix":
        return ("fix", t[1], eta_reduzir(t[2]))
    corpo = eta_reduzir(t[3])
    if corpo[0] == "ap" and corpo[2] == ("v", t[1]) and t[1] not in variaveis_livres(corpo[1]):
        return corpo[1]
    return ("lam", t[1], t[2], corpo)


def forma_alfa_eta(t: Termo) -> Termo:
    """Representante canônico módulo α e η (para comparar abstrações com soluções)."""
    return canonizar(eta_reduzir(t))


def _separar(fechado: Termo, k: int) -> Tuple[List[Tuple[str, Tipo]], Termo]:
    params = []
    u = fechado
    for _ in range(k):
        if u[0] != "lam":
            raise ValueError("número de parâmetros maior que a cadeia de λ")
        params.append((u[1], u[2]))
        u = u[3]
    return params, u


def _espinha(t: Termo) -> Tuple[Termo, List[Termo]]:
    args = []
    while t[0] == "ap":
        args.append(t[2])
        t = t[1]
    args.reverse()
    return t, args


def _assinatura(t: Termo) -> tuple:
    k = t[0]
    if k == "ap":
        cab, args = _espinha(t)
        ck = ("c", cab[1]) if cab[0] == "c" else (cab[0],)
        return ("ap", ck, len(args))
    if k == "lam":
        return ("lam", t[2])
    if k == "fix":
        return ("fix", t[1])
    if k == "c":
        return ("c", t[1])
    return ("v",)


def _eta_redutivel(params: List[Tuple[str, Tipo]], corpo: Termo) -> bool:
    """λx1..xk. h xk com xk ausente de h: equivale a um fragmento com menos parâmetros."""
    if not params or corpo[0] != "ap":
        return False
    ultimo = params[-1][0]
    return corpo[2] == ("v", ultimo) and ultimo not in variaveis_livres(corpo[1])


def _nos_nao_parametro(corpo: Termo, nomes_params: set) -> int:
    """Folhas e abstrações do corpo que não são parâmetros."""
    k = corpo[0]
    if k == "v":
        return 0 if corpo[1] in nomes_params else 1
    if k == "c":
        return 1
    if k == "ap":
        return _nos_nao_parametro(corpo[1], nomes_params) + _nos_nao_parametro(corpo[2], nomes_params)
    if k == "lam":
        return 1 + _nos_nao_parametro(corpo[3], nomes_params)
    return 1 + _nos_nao_parametro(corpo[2], nomes_params)


def _tipo_ou_none(t: Termo, ctx: dict, tabela) -> Optional[Tipo]:
    try:
        return tipo_de(t, ctx, tabela)
    except (ErroTipo, KeyError):
        return None


# =====================================================================
# Corpus indexado
# =====================================================================
@dataclass
class _Oc:
    sol: int
    caminho: tuple
    termo: Termo
    ctx: dict           # tipos das variáveis ligadas ACIMA do subtermo
    tam: int


class _Corpus:
    def __init__(self, termos: Sequence[Termo], contador: ContadorCompressao):
        self.termos = list(termos)
        self.ocs: List[_Oc] = []
        self.por_assinatura: Dict[tuple, List[int]] = defaultdict(list)
        self.aps_por_espinha: Dict[int, List[int]] = defaultdict(list)
        for si, t in enumerate(self.termos):
            self._enumerar(si, t, {}, (), contador)
        for i, oc in enumerate(self.ocs):
            a = _assinatura(oc.termo)
            self.por_assinatura[a].append(i)
            if a[0] == "ap":
                self.aps_por_espinha[a[2]].append(i)

    def _enumerar(self, si, t, ctx, caminho, contador):
        pilha = [(t, ctx, caminho)]
        # pré-ordem explícita (sem recursão): filhos empilhados em ordem inversa
        while pilha:
            u, c, cam = pilha.pop()
            contador.nos_enumerados += 1
            self.ocs.append(_Oc(si, cam, u, c, tamanho(u)))
            k = u[0]
            if k == "ap":
                pilha.append((u[2], c, cam + (1,)))
                pilha.append((u[1], c, cam + (0,)))
            elif k == "lam":
                c2 = dict(c)
                c2[u[1]] = u[2]
                pilha.append((u[3], c2, cam + (0,)))
            elif k == "fix":
                pilha.append((u[2], c, cam + (0,)))

    def posicoes_para(self, corpo: Termo, nomes_params: set) -> List[int]:
        a = _assinatura(corpo)
        if a[0] == "ap":
            cab, args = _espinha(corpo)
            if cab[0] == "v" and cab[1] in nomes_params:
                # cabeça é parâmetro: casa com qualquer aplicação de espinha ≥ len(args)
                out = []
                for m, idx in self.aps_por_espinha.items():
                    if m >= len(args):
                        out.extend(idx)
                return sorted(out)
            if cab[0] == "v":
                a = ("ap", ("v",), len(args))
        elif a[0] == "v":
            return []
        return self.por_assinatura.get(a, [])


# =====================================================================
# Anti-unificação (generalização mínima) com buracos limitados
# =====================================================================
class _Falha(Exception):
    pass


class _AntiUnificador:
    """lgg de dois subtermos abertos. Variáveis livres pareadas → parâmetro de variável;
    pares divergentes sem variáveis ligadas internamente → buraco (parâmetro extra)."""

    def __init__(self, oc1: _Oc, oc2: _Oc, max_buracos: int, tabela, contador: ContadorCompressao):
        self.oc1, self.oc2 = oc1, oc2
        self.max_buracos = max_buracos
        self.tabela = tabela
        self.contador = contador
        self.params: List[Tuple[str, Tipo, str]] = []   # (nome, tipo, "var" | "buraco")
        self.chaves: Dict[tuple, str] = {}
        self.buracos = 0
        self.nb = 0     # contador de binders internos

    def _estado(self):
        return (list(self.params), dict(self.chaves), self.buracos)

    def _restaurar(self, e):
        self.params, self.chaves, self.buracos = list(e[0]), dict(e[1]), e[2]

    def _param(self, chave, tipo, tipo_param):
        if chave in self.chaves:
            nome = self.chaves[chave]
            if next(t for n, t, _ in self.params if n == nome) != tipo:
                raise _Falha()
            return ("v", nome)
        if tipo_param == "buraco":
            if self.buracos >= self.max_buracos:
                raise _Falha()
            self.buracos += 1
        nome = f"#x{len(self.params) + 1}"
        self.params.append((nome, tipo, tipo_param))
        self.chaves[chave] = nome
        return ("v", nome)

    def _buraco(self, a, b, m1, m2):
        fa, fb = variaveis_livres(a), variaveis_livres(b)
        if any(v in m1 for v in fa) or any(v in m2 for v in fb):
            raise _Falha()  # o par usa variáveis ligadas dentro do fragmento
        ta = _tipo_ou_none(a, self.oc1.ctx, self.tabela)
        tb = _tipo_ou_none(b, self.oc2.ctx, self.tabela)
        if ta is None or ta != tb:
            raise _Falha()
        return self._param(("b", a, b), ta, "buraco")

    def rodar(self) -> Optional[Tuple[Termo, List[Tuple[str, Tipo, str]], int]]:
        try:
            corpo = self._lgg(self.oc1.termo, self.oc2.termo, {}, {})
        except _Falha:
            return None
        return corpo, self.params, self.buracos

    def _lgg(self, a, b, m1, m2):
        self.contador.nos_antiunificacao += 1
        ka, kb = a[0], b[0]
        if ka == "v" and kb == "v":
            ia, ib = a[1] in m1, b[1] in m2
            if ia and ib:
                if m1[a[1]] != m2[b[1]]:
                    raise _Falha()
                return ("v", m1[a[1]])
            if not ia and not ib:
                ta, tb = self.oc1.ctx.get(a[1]), self.oc2.ctx.get(b[1])
                if ta is None or ta != tb:
                    raise _Falha()
                return self._param(("v", a[1], b[1]), ta, "var")
            raise _Falha()
        if ka == "c" and kb == "c" and a[1] == b[1]:
            return a
        if ka == "lam" and kb == "lam" and a[2] == b[2]:
            self.nb += 1
            y = f"#y{self.nb}"
            m1b, m2b = dict(m1), dict(m2)
            m1b[a[1]] = y
            m2b[b[1]] = y
            return ("lam", y, a[2], self._lgg(a[3], b[3], m1b, m2b))
        if ka == "fix" and kb == "fix" and a[1] == b[1]:
            return ("fix", a[1], self._lgg(a[2], b[2], m1, m2))
        if ka == "ap" and kb == "ap":
            ca, xa = _espinha(a)
            cb, xb = _espinha(b)
            if len(xa) == len(xb):
                e = self._estado()
                try:
                    if ca[0] == "c" and cb[0] == "c" and ca[1] != cb[1]:
                        cab = self._buraco(ca, cb, m1, m2)   # buraco na cabeça (mesmo tipo)
                    else:
                        cab = self._lgg(ca, cb, m1, m2)
                    return AP(cab, *[self._lgg(x, y, m1, m2) for x, y in zip(xa, xb)])
                except _Falha:
                    self._restaurar(e)
        return self._buraco(a, b, m1, m2)


def _fechar(corpo: Termo, params: List[Tuple[str, Tipo, str]]) -> Tuple[Termo, int, int]:
    """λ-fecha o padrão (parâmetros na ordem de criação = ordem de ocorrência) e canoniza."""
    fechado = LAMS([(n, t) for n, t, _ in params], corpo)
    return canonizar(fechado), len(params), sum(1 for _, _, k in params if k == "buraco")


# =====================================================================
# Casamento de padrão e reescrita
# =====================================================================
def _alfa_igual(a: Termo, b: Termo) -> bool:
    return a == b or canonizar(a) == canonizar(b)


def _casar(corpo: Termo, params: List[Tuple[str, Tipo]], s: Termo, ctx: dict, tabela,
           contador: ContadorCompressao) -> Optional[Tuple[Dict[str, Termo], List[tuple]]]:
    """Casa `corpo` (parâmetros = variáveis livres listadas em params) com o subtermo s.
    Devolve (substituição, caminhos relativos dos argumentos) ou None."""
    nomes = {n for n, _ in params}
    subst: Dict[str, Termo] = {}
    caminhos: List[tuple] = []
    prox = [0]

    def rec(p, u, penv, senv, cam):
        contador.nos_casamento += 1
        k = p[0]
        if k == "v":
            if p[1] in nomes:
                if any(v in senv for v in variaveis_livres(u)):
                    return False
                if p[1] in subst:
                    return _alfa_igual(subst[p[1]], u)
                subst[p[1]] = u
                caminhos.append(cam)
                return True
            return u[0] == "v" and u[1] in senv and senv[u[1]] == penv.get(p[1])
        if k == "c":
            return u[0] == "c" and u[1] == p[1]
        if k == "ap":
            return u[0] == "ap" and rec(p[1], u[1], penv, senv, cam + (0,)) and rec(p[2], u[2], penv, senv, cam + (1,))
        if k == "lam":
            if u[0] != "lam" or u[2] != p[2]:
                return False
            prox[0] += 1
            pe, se = dict(penv), dict(senv)
            pe[p[1]] = prox[0]
            se[u[1]] = prox[0]
            return rec(p[3], u[3], pe, se, cam + (0,))
        if k == "fix":
            return u[0] == "fix" and u[1] == p[1] and rec(p[2], u[2], penv, senv, cam + (0,))
        return False

    if not rec(corpo, s, {}, {}, ()):
        return None
    for n, t in params:
        if n not in subst:          # parâmetro não usado no corpo: não casa (fragmento malformado)
            return None
        if _tipo_ou_none(subst[n], ctx, tabela) != t:
            return None
    return subst, caminhos


def reescrever(termo: Termo, nome: str, fragmento_fechado: Termo, num_parametros: int, tabela=None,
               contador: Optional[ContadorCompressao] = None) -> Tuple[Termo, int]:
    """Substitui as ocorrências (externas primeiro, depois dentro dos argumentos) do fragmento
    pela constante `nome` aplicada aos argumentos. Devolve (termo reescrito, nº de substituições).
    A denotação é preservada (β-equivalência sob Sem_n)."""
    contador = contador if contador is not None else ContadorCompressao()
    tabela = tabela if tabela is not None else REGISTRO_BASE
    params, corpo = _separar(fragmento_fechado, num_parametros)
    total = [0]

    def rec(u, ctx):
        m = _casar(corpo, params, u, ctx, tabela, contador)
        if m is not None:
            subst, _ = m
            total[0] += 1
            return AP(C(nome), *[rec(subst[n], ctx) for n, _ in params])
        k = u[0]
        if k == "ap":
            return ("ap", rec(u[1], ctx), rec(u[2], ctx))
        if k == "lam":
            c2 = dict(ctx)
            c2[u[1]] = u[2]
            return ("lam", u[1], u[2], rec(u[3], c2))
        if k == "fix":
            return ("fix", u[1], rec(u[2], ctx))
        return u

    novo = rec(termo, {})
    return novo, total[0]


def _contar(corpus: _Corpus, fechado: Termo, k: int, tabela, contador) -> Tuple[int, List[int]]:
    """Ocorrências não sobrepostas (mesma regra da reescrita) e soluções onde ocorrem."""
    params, corpo = _separar(fechado, k)
    nomes = {n for n, _ in params}
    aceitas: Dict[int, List[Tuple[tuple, List[tuple]]]] = defaultdict(list)
    idx = sorted(corpus.posicoes_para(corpo, nomes), key=lambda i: (corpus.ocs[i].sol, corpus.ocs[i].caminho))
    n_oc = 0
    for i in idx:
        oc = corpus.ocs[i]
        q = oc.caminho
        dentro = False
        for p, pps in aceitas[oc.sol]:
            if q[:len(p)] == p and not any(q[:len(p) + len(pp)] == p + pp for pp in pps):
                dentro = True
                break
        if dentro:
            continue
        m = _casar(corpo, params, oc.termo, oc.ctx, tabela, contador)
        if m is None:
            continue
        aceitas[oc.sol].append((q, m[1]))
        n_oc += 1
    return n_oc, sorted(s for s, v in aceitas.items() if v)


# =====================================================================
# Extração
# =====================================================================
def _normalizar_solucoes(solucoes) -> Tuple[List[Termo], List[str], List[str]]:
    termos, ids, provs = [], [], []
    for i, s in enumerate(solucoes):
        if isinstance(s, Solucao):
            termos.append(s.termo); ids.append(str(s.tarefa_id)); provs.append(s.proveniencia)
        else:
            if not eh_fechado(s):
                raise ValueError(f"solução {i} não é fechada")
            termos.append(s); ids.append(str(i)); provs.append(NAO_DECLARADA)
    return termos, ids, provs


def extrair_fragmentos(solucoes, min_tamanho: int = 3, min_ocorrencias: int = 2, max_buracos: int = 1,
                       tabela=None, contador: Optional[ContadorCompressao] = None,
                       max_pares: Optional[int] = None) -> List[Fragmento]:
    """Fragmentos recorrentes nas soluções (termos fechados ou Solucao), por pontuação decrescente.

    Candidatos: fechamento de cada subtermo de tamanho ≥ min_tamanho; anti-unificação de pares de
    subtermos com a mesma assinatura de raiz (até max_buracos buracos; 0 desliga). Filtros: corpo
    de tamanho ≥ min_tamanho, com ao menos um nó que não é parâmetro, não η-redutível, e que encurta
    cada ocorrência (|corpo| > 1 + nº de parâmetros, o que garante o término da compressão gulosa).
    `tabela` (Tabela ou dict nome → Primitiva) tipa as constantes; padrão: dsl.REGISTRO_BASE.
    `max_pares` limita, deterministicamente, os pares anti-unificados (os omitidos são contados)."""
    contador = contador if contador is not None else ContadorCompressao()
    tabela = tabela if tabela is not None else REGISTRO_BASE
    termos, ids, provs = _normalizar_solucoes(solucoes)
    corpus = _Corpus(termos, contador)

    # candidatos: termo canônico → {k: (num_buracos, metodo)}
    cands: Dict[Termo, Dict[int, Tuple[int, str]]] = {}

    def registrar(res, metodo):
        if res is None:
            return
        corpo, params, _ = res
        fechado, k, nb = _fechar(corpo, params)
        vs = cands.setdefault(fechado, {})
        if k not in vs or nb < vs[k][0]:
            vs[k] = (nb, metodo if nb else "fechamento")

    grandes = [i for i, oc in enumerate(corpus.ocs) if oc.tam >= min_tamanho]
    for i in grandes:
        oc = corpus.ocs[i]
        registrar(_AntiUnificador(oc, oc, 0, tabela, contador).rodar(), "fechamento")

    if max_buracos > 0:
        pares_feitos = 0
        for assin in sorted(corpus.por_assinatura, key=repr):
            idx = [i for i in corpus.por_assinatura[assin] if corpus.ocs[i].tam >= min_tamanho]
            for a in range(len(idx)):
                for b in range(a + 1, len(idx)):
                    if max_pares is not None and pares_feitos >= max_pares:
                        contador.pares_omitidos += 1
                        continue
                    o1, o2 = corpus.ocs[idx[a]], corpus.ocs[idx[b]]
                    if o1.termo == o2.termo:
                        continue  # idêntico: já coberto pelo fechamento
                    pares_feitos += 1
                    contador.pares_antiunificacao += 1
                    registrar(_AntiUnificador(o1, o2, max_buracos, tabela, contador).rodar(), "antiunificacao")

    contador.candidatos_distintos += len(cands)
    out: List[Fragmento] = []
    for fechado, variantes in cands.items():
        melhor = None
        for k in sorted(variantes):
            params, corpo = _separar(fechado, k)
            nomes = {n for n, _ in params}
            tc = tamanho(corpo)
            if tc < min_tamanho or tc <= 1 + k or _nos_nao_parametro(corpo, nomes) == 0:
                continue
            if _eta_redutivel(params, corpo):
                continue
            n_oc, sols = _contar(corpus, fechado, k, tabela, contador)
            if n_oc < min_ocorrencias:
                continue
            if melhor is None or n_oc > melhor[0]:
                melhor = (n_oc, k, sols)
        if melhor is None:
            continue
        n_oc, k, sols = melhor
        tipo = _tipo_ou_none(fechado, {}, tabela)
        if tipo is None:
            continue
        nb, metodo = variantes[k]
        out.append(Fragmento(fechado, tipo, n_oc, pontuacao(n_oc, tamanho(fechado)),
                             tuple(ids[s] for s in sols), k, nb, metodo,
                             frozenset(provs[s] for s in sols)))
    out.sort(key=lambda f: (-f.pontuacao, -f.tamanho, f.num_parametros, imprimir(f.termo_fechado)))
    return out


# =====================================================================
# Biblioteca
# =====================================================================
@dataclass
class RegistroEntrada:
    primitiva: Primitiva
    fragmento: Fragmento
    num_parametros: int
    tarefas_origem: Tuple[str, ...]
    usos_na_origem: int = 0                              # substituições na reescrita do corpus
    reutilizacoes: Dict[str, int] = field(default_factory=dict)          # tarefa → ocorrências diretas
    reutilizacoes_indiretas: Dict[str, int] = field(default_factory=dict)  # via corpo de outra entrada
    usos_em_origem_posteriores: Dict[str, int] = field(default_factory=dict)


class Biblioteca:
    """Biblioteca de L-lib sobre uma tabela base. modo "autonomo" (aprendiz) ou "mecanismo-teste"."""

    def __init__(self, tabela_base: Tabela, modo: str, prefixo: str = "abs", min_tamanho: int = 3,
                 min_ocorrencias: int = 2, max_buracos: int = 1, max_pares: Optional[int] = None):
        if modo not in MODOS:
            raise ValueError(f"modo inválido: {modo!r}")
        self.modo = modo
        if modo == "autonomo":
            self.tabela = tabela_base.para_aprendiz(f"{tabela_base.nome}/L-lib")
            exigir_tabela_de_descoberta(self.tabela)
        else:
            self.tabela = tabela_base.para_referencia(nome=f"{tabela_base.nome}/mecanismo-teste")
        self.prefixo = prefixo
        self.min_tamanho = min_tamanho
        self.min_ocorrencias = min_ocorrencias
        self.max_buracos = max_buracos
        self.max_pares = max_pares
        self.contador = ContadorCompressao()
        self.ultimo_custo = ContadorCompressao()
        self.entradas: Dict[str, RegistroEntrada] = {}
        self.solucoes: List[Solucao] = []

    @property
    def proveniencia_entradas(self) -> str:
        return "descoberta" if self.modo == "autonomo" else "manual-teste"

    # ---------------- validação ----------------
    def _validar_solucao(self, s) -> Solucao:
        from .certificados import descoberta_valida
        if self.modo == "autonomo":
            if not isinstance(s, Solucao):
                raise ErroProveniencia("modo autônomo exige Solucao marcada como encontrada pelo aprendiz")
            if s.proveniencia != "descoberta":
                raise ErroProveniencia(
                    f"solução {s.tarefa_id!r} com proveniência {s.proveniencia!r} recusada no modo autônomo")
            if not descoberta_valida(s.certificado, termo=s.termo, tarefa_id=s.tarefa_id):
                raise ErroProveniencia(f"solução {s.tarefa_id!r}: certificado não corresponde ao termo")
        elif not isinstance(s, Solucao):
            s = Solucao(s, f"s{len(self.solucoes)}", "manual-teste")
        for nome in constantes(s.termo):
            if nome not in self.tabela:
                raise ErroProveniencia(f"solução {s.tarefa_id!r} usa constante fora da tabela: {nome}")
        return s

    def _validar_proveniencia(self, fragmento: Fragmento, proveniencia: str) -> None:
        if proveniencia not in ("descoberta", "manual-teste"):
            raise ErroProveniencia(f"proveniência inválida: {proveniencia!r}")
        if self.modo == "autonomo":
            if proveniencia != "descoberta":
                raise ErroProveniencia("modo autônomo: proibido adicionar fragmento 'manual-teste'")
            if fragmento.proveniencias_origem != frozenset({"descoberta"}):
                raise ErroProveniencia(
                    f"modo autônomo: fragmento com origens {sorted(fragmento.proveniencias_origem)} "
                    "não pode ser declarado descoberta")
        elif proveniencia != "manual-teste":
            raise ErroProveniencia("modo mecanismo-teste: toda entrada é 'manual-teste' (nunca 'descoberta')")

    # ---------------- operações ----------------
    def _novo_nome(self) -> str:
        i = len(self.entradas) + 1
        while f"{self.prefixo}{i}" in self.tabela:
            i += 1
        return f"{self.prefixo}{i}"

    def _verificar_no_corpus(self, fragmento: Fragmento) -> None:
        """Modo autônomo: o fragmento tem de OCORRER no corpus certificado (soluções do próprio aprendiz,
        todas com CertificadoDescoberta), e as tarefas de origem declaradas têm de ser as dessas
        ocorrências. Um Fragmento construído à mão com proveniencias_origem={'descoberta'} não passa.
        Custo desta verificação num contador à parte (não é aprendizagem; não entra no livro-razão)."""
        from .certificados import descoberta_valida
        if not self.solucoes:
            raise ErroProveniencia("modo autônomo: corpus vazio; nada pode ser declarado descoberta")
        for s_ in self.solucoes:
            if s_.proveniencia != "descoberta" or not descoberta_valida(s_.certificado, tarefa_id=s_.tarefa_id):
                raise ErroProveniencia(f"corpus com solução não certificada: {s_.tarefa_id}")
        corpus = _Corpus([s_.termo for s_ in self.solucoes], ContadorCompressao())
        n_oc, sols = _contar(corpus, fragmento.termo_fechado, fragmento.num_parametros, self.tabela,
                             ContadorCompressao())
        if n_oc < 1:
            raise ErroProveniencia("modo autônomo: fragmento não ocorre nas soluções certificadas do aprendiz")
        origem = {self.solucoes[i].tarefa_id for i in sols}
        if not set(fragmento.origem_ids) <= origem:
            raise ErroProveniencia(f"modo autônomo: origens declaradas {list(fragmento.origem_ids)} ≠ ocorrências "
                                   f"{sorted(origem)}")

    def adicionar(self, fragmento: Fragmento, proveniencia: str, nome: Optional[str] = None) -> Primitiva:
        """Cria a entrada (Primitiva com corpo = termo fechado; a denotação vem do avaliador, ver
        `denotacao`), registra a proveniência e reescreve as soluções do corpus com a nova constante.
        No modo autônomo emite o certificados.CertificadoEntrada exigido pela Tabela de descoberta."""
        from .certificados import emitir_entrada
        self._validar_proveniencia(fragmento, proveniencia)
        if self.modo == "autonomo":
            self._verificar_no_corpus(fragmento)
        nome = nome or self._novo_nome()
        prim = entrada_biblioteca(nome, fragmento.termo_fechado, proveniencia, self.tabela, tipo=fragmento.tipo)
        prim.motivo = f"{fragmento.metodo}; pontuação {fragmento.pontuacao}; origem {list(fragmento.origem_ids)}"
        cert = emitir_entrada(nome, prim.corpo, id(self)) if self.modo == "autonomo" else None
        self.tabela.adicionar(prim, certificado=cert)   # Tabela "descoberta" recusa manual-teste e sem certificado
        reg = RegistroEntrada(prim, fragmento, fragmento.num_parametros, tuple(fragmento.origem_ids))
        self.entradas[nome] = reg
        self.contador.fragmentos_adicionados += 1
        novas = []
        for s in self.solucoes:
            t2, k = reescrever(s.termo, nome, fragmento.termo_fechado, fragmento.num_parametros,
                               self.tabela, self.contador)
            reg.usos_na_origem += k
            novas.append(Solucao(t2, s.tarefa_id, s.proveniencia, s.certificado))
        self.solucoes = novas
        return prim

    def comprimir(self, solucoes, limiar: int, max_novas: Optional[int] = None) -> List[Primitiva]:
        """Acrescenta as soluções ao corpus e adiciona, gulosamente, o fragmento de maior pontuação
        (≥ limiar) até não haver mais; cada adição reescreve o corpus. Custo em self.contador
        (e o desta chamada em self.ultimo_custo)."""
        inicio = self.contador.copia()
        if self.modo == "autonomo":
            exigir_tabela_de_descoberta(self.tabela)
        for s in solucoes:
            s = self._validar_solucao(s)
            self.solucoes = [x for x in self.solucoes if x.tarefa_id != s.tarefa_id] + [s]
        adicionadas: List[Primitiva] = []
        while max_novas is None or len(adicionadas) < max_novas:
            frags = extrair_fragmentos(self.solucoes, self.min_tamanho, self.min_ocorrencias, self.max_buracos,
                                       self.tabela, self.contador, self.max_pares)
            frags = [f for f in frags if f.pontuacao >= limiar]
            if self.modo == "autonomo":
                frags = [f for f in frags if f.proveniencias_origem == frozenset({"descoberta"})]
            if not frags:
                break
            adicionadas.append(self.adicionar(frags[0], self.proveniencia_entradas))
        self.ultimo_custo = self.contador.menos(inicio)
        return adicionadas

    def registrar_reuso(self, termo, tarefa_id: str) -> Dict[str, int]:
        """Conta as ocorrências de cada constante da biblioteca numa solução posterior. Uso numa
        tarefa fora das de origem = reutilização (registrada também na Primitiva, se descoberta)."""
        if isinstance(termo, Solucao):
            if self.modo == "autonomo" and termo.proveniencia != "descoberta":
                raise ErroProveniencia("modo autônomo: reuso só se registra em soluções do aprendiz")
            termo = termo.termo
        tarefa_id = str(tarefa_id)
        diretas = {n: ocorrencias(termo, n) for n in self.entradas}
        diretas = {n: k for n, k in diretas.items() if k}
        # uso indireto: entradas chamadas pelos corpos das entradas usadas
        indiretas: Dict[str, int] = defaultdict(int)
        fila = list(diretas.items())
        while fila:
            n, k = fila.pop()
            for m in constantes(self.entradas[n].primitiva.corpo):
                if m in self.entradas:
                    indiretas[m] += k
                    fila.append((m, k))
        for n, k in diretas.items():
            reg = self.entradas[n]
            if tarefa_id in reg.tarefas_origem:
                reg.usos_em_origem_posteriores[tarefa_id] = reg.usos_em_origem_posteriores.get(tarefa_id, 0) + k
                continue
            reg.reutilizacoes[tarefa_id] = reg.reutilizacoes.get(tarefa_id, 0) + k
            if reg.primitiva.proveniencia == "descoberta" and tarefa_id not in reg.primitiva.reutilizacoes:
                reg.primitiva.registrar_reutilizacao(tarefa_id)
        for n, k in indiretas.items():
            reg = self.entradas[n]
            if tarefa_id not in reg.tarefas_origem:
                reg.reutilizacoes_indiretas[tarefa_id] = reg.reutilizacoes_indiretas.get(tarefa_id, 0) + k
        return diretas

    def denotacao(self, nome: str, n: int):
        """Valor da entrada sob Sem_n, obtido pelo avaliador a partir do corpo fechado."""
        from .avaliador import avaliar
        return avaliar(C(nome), n=n, tabela=self.tabela)

    def coincide_com_solucoes(self, nome: str) -> List[str]:
        """Tarefas cuja solução ACEITA (termo do certificado, ou o termo do corpus fora do modo autônomo)
        é igual, módulo α/η e com as entradas da biblioteca expandidas, ao corpo da entrada `nome`:
        nesse caso a "abstração" é a solução inteira de um degrau, não uma compressão entre tarefas."""
        from .tradutores import inline
        lib = [r.primitiva for r in self.entradas.values()]
        alvo = forma_alfa_eta(inline(self.entradas[nome].primitiva.corpo, lib, beta="nenhuma"))
        out = []
        for s_ in self.solucoes:
            t = s_.termo_aceito if s_.termo_aceito is not None else s_.termo
            if forma_alfa_eta(inline(t, lib, beta="nenhuma")) == alvo:
                out.append(s_.tarefa_id)
        return out

    def relatorio(self) -> dict:
        """Descobertas (ou entradas de teste do mecanismo) e reutilizações, com tarefas de origem e de reuso."""
        ents = []
        for nome, reg in self.entradas.items():
            p = reg.primitiva
            coincide = self.coincide_com_solucoes(nome)
            cat = p.categoria()
            if reg.fragmento.metodo == "promocao-solucao":
                cat = "promocao-solucao" + ("-reutilizada" if reg.reutilizacoes else "")
            ents.append({
                "nome": nome, "proveniencia": p.proveniencia, "categoria": cat,
                "coincide_com_solucao_de_tarefa": coincide,
                "copia_de_solucao": bool(coincide) or reg.fragmento.metodo == "promocao-solucao",
                "tipo": tipo_str(p.tipo), "corpo": imprimir(p.corpo), "legivel": imprimir_legivel(p.corpo),
                "tamanho": tamanho(p.corpo), "ocorrencias": reg.fragmento.ocorrencias,
                "pontuacao": reg.fragmento.pontuacao, "metodo": reg.fragmento.metodo,
                "num_parametros": reg.num_parametros, "num_buracos": reg.fragmento.num_buracos,
                "tarefas_origem": list(reg.tarefas_origem), "usos_na_origem": reg.usos_na_origem,
                "reutilizacoes": dict(reg.reutilizacoes),
                "reutilizacoes_indiretas": dict(reg.reutilizacoes_indiretas),
                "usos_em_origem_posteriores": dict(reg.usos_em_origem_posteriores),
                "reutilizada": bool(reg.reutilizacoes),
            })
        return {"modo": self.modo, "tabela": self.tabela.nome, "uso_tabela": self.tabela.uso,
                "entradas": ents, "custo": self.contador.como_dict(),
                "solucoes": [{"tarefa_id": s.tarefa_id, "proveniencia": s.proveniencia,
                              "termo": imprimir(s.termo), "tamanho": tamanho(s.termo)} for s in self.solucoes]}
