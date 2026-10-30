"""Linguagem do experimento 1 (documento 02, 2.3): tipos, termos, tamanho, impressão/parse,
verificação de tipos e tabelas de primitivas de E0, E0', E0+ e E0'+.

Distinção de proveniência (permanente, verificada por construção):
  (a) conceito explicitamente fornecido: proveniencia em {"E0", "E0p", "E0mais", "Lteto"};
  (b) programa manual usado só como referência ou teste: proveniencia "manual-teste";
  (c) abstração descoberta pelo aprendiz: proveniencia "descoberta";
  (d) abstração descoberta e reutilizada: "descoberta" com `reutilizacoes` não vazia.
Uma `Tabela` de uso "descoberta" recusa qualquer entrada "manual-teste" (asserção de construção).

Polimorfismo: as primitivas genéricas são instanciadas MONOMORFICAMENTE (ver INSTANCIAS).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from .grade import Grade

# =====================================================================
# Tipos
# =====================================================================
Tipo = tuple

BOOL: Tipo = ("Bool",)
POS: Tipo = ("Pos",)
GRADE: Tipo = ("Grade",)


def L(t: Tipo) -> Tipo:
    return ("Lista", t)


def FUN(*ts: Tipo) -> Tipo:
    """FUN(a, b, c) = a → (b → c) (associa à direita)."""
    if len(ts) < 2:
        raise ValueError("FUN exige ao menos dois tipos")
    r = ts[-1]
    for a in reversed(ts[:-1]):
        r = ("Fun", a, r)
    return r


LP: Tipo = L(POS)
LLP: Tipo = L(LP)

#: códigos curtos usados nos nomes das instâncias (mapear@P>LP etc.)
CODIGOS: Dict[str, Tipo] = {"B": BOOL, "P": POS, "LP": LP, "LLP": LLP}


def eh_funcao(t: Tipo) -> bool:
    return t[0] == "Fun"


def argumentos_e_resultado(t: Tipo) -> Tuple[List[Tipo], Tipo]:
    args = []
    while t[0] == "Fun":
        args.append(t[1])
        t = t[2]
    return args, t


def aridade_tipo(t: Tipo) -> int:
    return len(argumentos_e_resultado(t)[0])


def tipo_str(t: Tipo) -> str:
    """Forma legível: 'Grade → Pos → Bool', '(Pos → Bool) → L Pos → L Pos', 'L (L Pos)'."""
    k = t[0]
    if k in ("Bool", "Pos", "Grade"):
        return k
    if k == "Lista":
        s = tipo_str(t[1])
        return f"L ({s})" if " " in s else f"L {s}"
    if k == "Fun":
        a = tipo_str(t[1])
        if eh_funcao(t[1]):
            a = f"({a})"
        return f"{a} → {tipo_str(t[2])}"
    raise ValueError(f"tipo inválido: {t!r}")


def tipo_sexpr(t: Tipo) -> str:
    """Forma canônica usada por imprimir/parse: Bool, (L Pos), (-> Pos Bool)."""
    k = t[0]
    if k in ("Bool", "Pos", "Grade"):
        return k
    if k == "Lista":
        return f"(L {tipo_sexpr(t[1])})"
    if k == "Fun":
        args, res = argumentos_e_resultado(t)
        return "(-> " + " ".join(tipo_sexpr(a) for a in args + [res]) + ")"
    raise ValueError(f"tipo inválido: {t!r}")


def tipo_valido(t) -> bool:
    if not isinstance(t, tuple) or not t:
        return False
    if t in (BOOL, POS, GRADE):
        return True
    if t[0] == "Lista" and len(t) == 2:
        return tipo_valido(t[1])
    if t[0] == "Fun" and len(t) == 3:
        return tipo_valido(t[1]) and tipo_valido(t[2])
    return False


def subtipos(t: Tipo) -> set:
    """t e todos os seus subtipos (componentes de setas e de listas)."""
    out = {t}
    if t[0] == "Lista":
        out |= subtipos(t[1])
    elif t[0] == "Fun":
        out |= subtipos(t[1]) | subtipos(t[2])
    return out


# =====================================================================
# Termos
# =====================================================================
#   ('c', nome) | ('v', nome) | ('ap', f, x) | ('lam', var, tipo, corpo) | ('fix', tipo, f)
Termo = tuple


def C(nome: str) -> Termo:
    return ("c", nome)


def V(nome: str) -> Termo:
    return ("v", nome)


def AP(f: Termo, *xs: Termo) -> Termo:
    for x in xs:
        f = ("ap", f, x)
    return f


def LAM(var: str, tipo: Tipo, corpo: Termo) -> Termo:
    return ("lam", var, tipo, corpo)


def LAMS(binders: Sequence[Tuple[str, Tipo]], corpo: Termo) -> Termo:
    for v, t in reversed(list(binders)):
        corpo = ("lam", v, t, corpo)
    return corpo


def FIX(tipo: Tipo, f: Termo) -> Termo:
    return ("fix", tipo, f)


def tamanho(t: Termo) -> int:
    """|t| = folhas (constantes e variáveis) + abstrações; aplicações não contam; fix conta 1 folha."""
    k = t[0]
    if k == "c" or k == "v":
        return 1
    if k == "ap":
        return tamanho(t[1]) + tamanho(t[2])
    if k == "lam":
        return 1 + tamanho(t[3])
    if k == "fix":
        return 1 + tamanho(t[2])
    raise ValueError(f"termo inválido: {t!r}")


def variaveis_livres(t: Termo) -> set:
    k = t[0]
    if k == "v":
        return {t[1]}
    if k == "c":
        return set()
    if k == "ap":
        return variaveis_livres(t[1]) | variaveis_livres(t[2])
    if k == "lam":
        return variaveis_livres(t[3]) - {t[1]}
    if k == "fix":
        return variaveis_livres(t[2])
    raise ValueError(f"termo inválido: {t!r}")


def todas_variaveis(t: Termo) -> set:
    """Variáveis livres e ligadas (nomes)."""
    k = t[0]
    if k == "v":
        return {t[1]}
    if k == "c":
        return set()
    if k == "ap":
        return todas_variaveis(t[1]) | todas_variaveis(t[2])
    if k == "lam":
        return {t[1]} | todas_variaveis(t[3])
    if k == "fix":
        return todas_variaveis(t[2])
    raise ValueError(f"termo inválido: {t!r}")


def constantes(t: Termo) -> List[str]:
    """Nomes das constantes, com repetição, em ordem de ocorrência."""
    out: List[str] = []

    def rec(u):
        k = u[0]
        if k == "c":
            out.append(u[1])
        elif k == "ap":
            rec(u[1]); rec(u[2])
        elif k == "lam":
            rec(u[3])
        elif k == "fix":
            rec(u[2])
    rec(t)
    return out


def ocorrencias(t: Termo, nome: str) -> int:
    return sum(1 for c in constantes(t) if c == nome)


def eh_fechado(t: Termo) -> bool:
    return not variaveis_livres(t)


# ---------------------------------------------------------------------
# Impressão e parse (sintaxe prefixa com parênteses)
#   termo := ident | (f a1 ... ak) | (\ (x T) ... corpo) | (lam (x T) ... corpo)
#          | (fix T f) | (fix f)   [a segunda forma quando f é λ cujo parâmetro tem tipo T]
#   tipo  := Bool | Pos | Grade | (L T) | (-> T1 ... Tk R) | LP | LLP   (LP, LLP são atalhos)
# Identificadores livres viram constantes, salvo os declarados em `livres`.
# ---------------------------------------------------------------------
PALAVRAS_LAMBDA = ("\\", "lam", "λ")


def imprimir(t: Termo) -> str:
    """Impressão canônica; parse(imprimir(t)) == t para termos fechados."""
    k = t[0]
    if k in ("c", "v"):
        return t[1]
    if k == "lam":
        binders = []
        u = t
        while u[0] == "lam":
            binders.append(f"({u[1]} {tipo_sexpr(u[2])})")
            u = u[3]
        return "(\\ " + " ".join(binders) + " " + imprimir(u) + ")"
    if k == "ap":
        args = []
        u = t
        while u[0] == "ap":
            args.append(u[2])
            u = u[1]
        args.reverse()
        return "(" + " ".join([imprimir(u)] + [imprimir(a) for a in args]) + ")"
    if k == "fix":
        f = t[2]
        if f[0] == "lam" and f[2] == t[1]:
            return f"(fix {imprimir(f)})"
        return f"(fix {tipo_sexpr(t[1])} {imprimir(f)})"
    raise ValueError(f"termo inválido: {t!r}")


def imprimir_legivel(t: Termo) -> str:
    """Forma para relatórios: λg p. filtrar@P (celula g) (vizinhos g p)."""
    def atom(u):
        s = rec(u)
        return s if u[0] in ("c", "v") else f"({s})"

    def rec(u):
        k = u[0]
        if k in ("c", "v"):
            return u[1]
        if k == "lam":
            vs = []
            while u[0] == "lam":
                vs.append(u[1]); u = u[3]
            return "λ" + " ".join(vs) + ". " + rec(u)
        if k == "ap":
            args = []
            while u[0] == "ap":
                args.append(u[2]); u = u[1]
            args.reverse()
            return " ".join([atom(u)] + [atom(a) for a in args])
        if k == "fix":
            return "fix " + atom(u[2])
        raise ValueError(u)
    return rec(t)


class ErroParse(ValueError):
    pass


def _tokens(texto: str) -> List[str]:
    out, cur = [], []
    for ch in texto:
        if ch in "()":
            if cur:
                out.append("".join(cur)); cur = []
            out.append(ch)
        elif ch.isspace():
            if cur:
                out.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur))
    return out


def _sexpr(tokens: List[str]):
    pos = 0

    def ler():
        nonlocal pos
        if pos >= len(tokens):
            raise ErroParse("fim inesperado")
        tok = tokens[pos]; pos += 1
        if tok == "(":
            lst = []
            while True:
                if pos >= len(tokens):
                    raise ErroParse("parêntese não fechado")
                if tokens[pos] == ")":
                    pos += 1
                    return lst
                lst.append(ler())
        if tok == ")":
            raise ErroParse("')' inesperado")
        return tok
    s = ler()
    if pos != len(tokens):
        raise ErroParse("texto sobrando após o termo")
    return s


_ATALHOS_TIPO = {"Bool": BOOL, "Pos": POS, "Grade": GRADE, "LP": LP, "LLP": LLP}


def _tipo_de_sexpr(sx) -> Tipo:
    if isinstance(sx, str):
        if sx in _ATALHOS_TIPO:
            return _ATALHOS_TIPO[sx]
        raise ErroParse(f"tipo desconhecido: {sx}")
    if not sx:
        raise ErroParse("tipo vazio")
    if sx[0] == "L" and len(sx) == 2:
        return L(_tipo_de_sexpr(sx[1]))
    if sx[0] == "->" and len(sx) >= 3:
        return FUN(*[_tipo_de_sexpr(x) for x in sx[1:]])
    raise ErroParse(f"tipo malformado: {sx!r}")


def parse_tipo(texto: str) -> Tipo:
    return _tipo_de_sexpr(_sexpr(_tokens(texto)))


def parse(texto: str, livres: Iterable[str] = ()) -> Termo:
    """Inverso de `imprimir`. Identificadores não ligados viram constantes, salvo os de `livres`."""
    sx = _sexpr(_tokens(texto))
    return _termo_de_sexpr(sx, frozenset(livres))


def _termo_de_sexpr(sx, escopo: frozenset) -> Termo:
    if isinstance(sx, str):
        if sx in PALAVRAS_LAMBDA or sx == "fix":
            raise ErroParse(f"palavra reservada isolada: {sx}")
        return V(sx) if sx in escopo else C(sx)
    if not sx:
        raise ErroParse("lista vazia")
    cab = sx[0]
    if isinstance(cab, str) and cab in PALAVRAS_LAMBDA:
        if len(sx) < 3:
            raise ErroParse("λ exige ao menos um binder e um corpo")
        binders = []
        esc = escopo
        for b in sx[1:-1]:
            if not (isinstance(b, list) and len(b) == 2 and isinstance(b[0], str)):
                raise ErroParse(f"binder malformado: {b!r}")
            binders.append((b[0], _tipo_de_sexpr(b[1])))
            esc = esc | {b[0]}
        return LAMS(binders, _termo_de_sexpr(sx[-1], esc))
    if cab == "fix":
        if len(sx) == 3:
            return FIX(_tipo_de_sexpr(sx[1]), _termo_de_sexpr(sx[2], escopo))
        if len(sx) == 2:
            f = _termo_de_sexpr(sx[1], escopo)
            if f[0] != "lam":
                raise ErroParse("(fix f) sem tipo exige f = λ")
            return FIX(f[2], f)
        raise ErroParse("fix malformado")
    if len(sx) < 2:
        raise ErroParse(f"aplicação sem argumento: {sx!r}")
    f = _termo_de_sexpr(cab, escopo)
    return AP(f, *[_termo_de_sexpr(a, escopo) for a in sx[1:]])


# =====================================================================
# Semântica das primitivas sob Sem_n (usada pelo avaliador)
# =====================================================================
def F(n: int) -> int:
    """Combustível e comprimento máximo de lista: F(n) = n⁴."""
    return n ** 4


def truncar(lst: tuple, limite: int) -> tuple:
    return lst if len(lst) <= limite else lst[:limite]


_PADRAO_CACHE: dict = {}


def padrao(t: Tipo, n: int):
    """Valor padrão do tipo: falso, (1,1), vazio, grade vazia de lado n, função constante no padrão."""
    k = t[0]
    if k == "Bool":
        return False
    if k == "Pos":
        return (1, 1)
    if k == "Lista":
        return ()
    if k == "Grade":
        chave = (t, n)
        if chave not in _PADRAO_CACHE:
            _PADRAO_CACHE[chave] = Grade.vazia(n)
        return _PADRAO_CACHE[chave]
    if k == "Fun":
        v = padrao(t[2], n)

        def const(_x, _v=v):
            return _v
        return const
    raise ValueError(f"tipo inválido: {t!r}")


# Cada impl recebe (ctx, *args) com ctx.n e ctx.F. Argumentos funcionais são callables curried.
def _celula(ctx, g, p):
    return g.bits[(p[0] - 1) * g.n + p[1] - 1] == 1


def _posicoes(ctx, g):
    n = g.n
    return tuple((i, j) for i in range(1, n + 1) for j in range(1, n + 1))


def _pretas(ctx, g):
    n, b = g.n, g.bits
    return tuple((i, j) for i in range(1, n + 1) for j in range(1, n + 1) if b[(i - 1) * n + j - 1])


def _linhas(ctx, g):
    n = g.n
    return tuple(tuple((i, j) for j in range(1, n + 1)) for i in range(1, n + 1))


def _colunas(ctx, g):
    n = g.n
    return tuple(tuple((i, j) for i in range(1, n + 1)) for j in range(1, n + 1))


def _vizinhos(ctx, g, p):
    return tuple(g.vizinhos(p))


def _linhaDe(ctx, g, p):
    return tuple((p[0], j) for j in range(1, g.n + 1))


def _colunaDe(ctx, g, p):
    return tuple((i, p[1]) for i in range(1, g.n + 1))


def _cabeca(elem: Tipo):
    def impl(ctx, l):
        return l[0] if l else padrao(elem, ctx.n)
    return impl


def _cons(ctx, x, l):
    return truncar((x,) + l, ctx.F)


def _mapear(ctx, f, l):
    return tuple([f(x) for x in l])


def _filtrar(ctx, f, l):
    return tuple([x for x in l if f(x)])


def _algum(ctx, f, l):
    for x in l:  # laço explícito (curto-circuito determinístico, sem recursão em C)
        if f(x):
            return True
    return False


def _todos(ctx, f, l):
    for x in l:
        if not f(x):
            return False
    return True


def _concatenar(ctx, a, b):
    return truncar(a + b, ctx.F)


def _juntar(ctx, ls):
    out = ()
    for l in ls:
        out = out + l
        if len(out) >= ctx.F:
            break
    return truncar(out, ctx.F)


def _uniao(ctx, a, b):
    """Definição exata: dobraR (λx acc. se (pertence x acc) acc (cons x acc)) A B."""
    acc = a
    lim = ctx.F
    for x in reversed(b):
        if x not in acc:
            acc = truncar((x,) + acc, lim)
    return acc


def _diferenca(ctx, a, b):
    sb = set(b)
    return tuple([x for x in a if x not in sb])


def _dobraR(ctx, f, z, l):
    """Dobra à direita exata (listas já têm comprimento ≤ F(n))."""
    acc = z
    for x in reversed(l):
        acc = f(x)(acc)
    return acc


def _ateFixo(ctx, f, l):
    """Itera f a partir de l até f(x) = x, no máximo F(n) aplicações; devolve o último x."""
    x = l
    for _ in range(ctx.F):
        y = f(x)
        if y == x:
            return x
        x = y
    return x


# =====================================================================
# Primitivas e tabelas
# =====================================================================
PROVENIENCIAS_FORNECIDAS = frozenset({"E0", "E0p", "E0mais", "Lteto"})
PROVENIENCIAS = PROVENIENCIAS_FORNECIDAS | {"descoberta", "manual-teste"}


class ErroProveniencia(AssertionError):
    """Violação da separação fornecido / manual-teste / descoberta."""


@dataclass(eq=False)
class Primitiva:
    nome: str
    tipo: Tipo
    impl: Optional[Callable]
    proveniencia: str
    generico: str = ""
    corpo: Optional[Termo] = None
    motivo: str = ""
    reutilizacoes: List[str] = field(default_factory=list)
    #: certificados.CertificadoEntrada (só entradas "descoberta" de tabelas de aprendiz; ver Tabela.adicionar)
    certificado: Optional[object] = field(default=None, repr=False)

    def __post_init__(self):
        if self.proveniencia not in PROVENIENCIAS:
            raise ErroProveniencia(f"proveniência inválida: {self.proveniencia!r}")
        if not tipo_valido(self.tipo):
            raise ValueError(f"tipo inválido para {self.nome}: {self.tipo!r}")
        if self.proveniencia in PROVENIENCIAS_FORNECIDAS:
            if self.impl is None or self.corpo is not None:
                raise ErroProveniencia(f"{self.nome}: primitiva fornecida exige impl e nenhum corpo")
        else:
            if self.corpo is None or self.impl is not None:
                raise ErroProveniencia(f"{self.nome}: entrada de biblioteca exige corpo e nenhuma impl")
            if not eh_fechado(self.corpo):
                raise ValueError(f"{self.nome}: corpo de biblioteca deve ser fechado")
        if not self.generico:
            self.generico = self.nome.split("@")[0]

    @property
    def aridade(self) -> int:
        return aridade_tipo(self.tipo)

    @property
    def eh_fornecida(self) -> bool:
        return self.proveniencia in PROVENIENCIAS_FORNECIDAS

    @property
    def eh_reutilizada(self) -> bool:
        return self.proveniencia == "descoberta" and bool(self.reutilizacoes)

    def categoria(self) -> str:
        """'fornecida' | 'manual-teste' | 'descoberta' | 'descoberta-reutilizada'."""
        if self.eh_fornecida:
            return "fornecida"
        if self.proveniencia == "manual-teste":
            return "manual-teste"
        return "descoberta-reutilizada" if self.reutilizacoes else "descoberta"

    def registrar_reutilizacao(self, onde: str) -> None:
        if self.proveniencia != "descoberta":
            raise ErroProveniencia(f"{self.nome}: só abstrações descobertas registram reutilização")
        self.reutilizacoes.append(onde)


USOS_TABELA = ("base", "descoberta", "referencia")


class Tabela:
    """Conjunto nomeado de primitivas. uso:
    - "base": tabela fixa de uma linguagem (congelada);
    - "descoberta": biblioteca do aprendiz numa execução autônoma; RECUSA "manual-teste";
    - "referencia": testes e verificação de programas manuais; nunca dada a um aprendiz.
    """

    def __init__(self, nome: str, primitivas: Iterable[Primitiva], uso: str = "base"):
        if uso not in USOS_TABELA:
            raise ValueError(f"uso inválido: {uso}")
        self.nome = nome
        self._uso = uso
        self._prims: Dict[str, Primitiva] = {}
        self._congelada = False
        for p in primitivas:
            self._inserir(p)
        if uso == "base":
            self._congelada = True

    @property
    def uso(self) -> str:
        return self._uso

    @property
    def modo_descoberta(self) -> bool:
        return self._uso == "descoberta"

    def _inserir(self, p: Primitiva):
        if self._uso == "descoberta" and p.proveniencia == "manual-teste":
            raise ErroProveniencia(
                f"solução manual {p.nome!r} não pode entrar na biblioteca de um aprendiz em descoberta autônoma")
        if self._uso == "descoberta" and p.proveniencia == "descoberta" and not _entrada_certificada(p):
            raise ErroProveniencia(
                f"entrada {p.nome!r} rotulada 'descoberta' sem certificado da Biblioteca autônoma "
                "(o rótulo de texto não basta: ver certificados.py)")
        if self._uso == "base" and not p.eh_fornecida:
            raise ErroProveniencia(f"tabela base só aceita primitivas fornecidas: {p.nome}")
        if p.nome in self._prims:
            raise ValueError(f"nome repetido: {p.nome}")
        self._prims[p.nome] = p

    def adicionar(self, p: Primitiva, certificado: Optional[object] = None) -> None:
        """Acrescenta uma entrada de biblioteca. Numa tabela de uso "descoberta", uma entrada
        "descoberta" exige `certificado` (certificados.CertificadoEntrada emitido pela Biblioteca
        autônoma a partir de soluções com CertificadoDescoberta)."""
        if self._congelada:
            raise ErroProveniencia(f"tabela {self.nome} congelada")
        if p.eh_fornecida:
            raise ErroProveniencia("primitivas fornecidas só entram na construção da base")
        if certificado is not None:
            p.certificado = certificado
        self._inserir(p)

    # ---- derivação ----
    def para_aprendiz(self, nome: Optional[str] = None) -> "Tabela":
        """Cópia de uso "descoberta" com as primitivas fornecidas e eventuais descobertas."""
        prims = [p for p in self._prims.values() if p.proveniencia != "manual-teste"]
        if len(prims) != len(self._prims):
            raise ErroProveniencia("tabela contém entradas manual-teste; não pode originar tabela de aprendiz")
        return Tabela(nome or f"{self.nome}/aprendiz", prims, "descoberta")

    def para_referencia(self, entradas: Iterable[Primitiva] = (), nome: Optional[str] = None) -> "Tabela":
        t = Tabela(nome or f"{self.nome}/referencia", list(self._prims.values()), "referencia")
        for p in entradas:
            t.adicionar(p)
        return t

    # ---- acesso ----
    def __getitem__(self, nome: str) -> Primitiva:
        return self._prims[nome]

    def get(self, nome: str, padrao_=None):
        return self._prims.get(nome, padrao_)

    def __contains__(self, nome: str) -> bool:
        return nome in self._prims

    def __iter__(self) -> Iterator[Primitiva]:
        return iter(self._prims.values())

    def __len__(self) -> int:
        return len(self._prims)

    def nomes(self) -> List[str]:
        return list(self._prims)

    def fornecidas(self) -> List[Primitiva]:
        return [p for p in self._prims.values() if p.eh_fornecida]

    def biblioteca(self) -> List[Primitiva]:
        return [p for p in self._prims.values() if not p.eh_fornecida]

    def genericos(self) -> set:
        return {p.generico for p in self._prims.values() if p.eh_fornecida}

    def __repr__(self):
        return f"Tabela({self.nome!r}, {len(self)} entradas, uso={self._uso!r})"


def _entrada_certificada(p: Primitiva) -> bool:
    from .certificados import entrada_valida
    return entrada_valida(p.certificado, p.nome, p.corpo)


def exigir_tabela_de_descoberta(tabela: Tabela) -> None:
    """Para enumerador/aprendizes: aborta se a tabela não for de descoberta autônoma, se tiver
    entrada manual-teste ou entrada 'descoberta' sem certificado válido."""
    if not isinstance(tabela, Tabela) or tabela.uso != "descoberta":
        raise ErroProveniencia("aprendiz exige Tabela de uso 'descoberta'")
    for p in tabela:
        if p.proveniencia == "manual-teste":
            raise ErroProveniencia(f"entrada manual-teste {p.nome} numa tabela de descoberta")
        if p.proveniencia == "descoberta" and not _entrada_certificada(p):
            raise ErroProveniencia(f"entrada {p.nome} 'descoberta' sem certificado")


# ---------------------------------------------------------------------
# Instâncias monomórficas
# ---------------------------------------------------------------------
# Política: um elemento a ∈ {Pos, L Pos}; listas L Pos e L (L Pos); argumentos funcionais
# Pos→Bool, Pos→L Pos, L Pos→Bool, L Pos→L Pos (e os combinadores binários de dobraR).
# Dentro deste espaço, só se instancia o MÍNIMO exigido por: (i) os programas da escada
# (documento 02, 2.8.1) em E0, E0', E0+, E0'+; (ii) o fechamento das traduções τ e τ'.
# Coluna `bases`: subconjunto de {E0, E0p, E0mais, E0pmais}.
_E0 = "E0"; _E0p = "E0p"; _E0m = "E0mais"; _E0pm = "E0pmais"
TODAS_BASES = frozenset({_E0, _E0p, _E0m, _E0pm})
SO_E0 = frozenset({_E0, _E0m})
SO_E0p = frozenset({_E0p, _E0pm})


@dataclass(frozen=True)
class Instancia:
    nome: str
    generico: str
    tipo: Tipo
    impl: Callable
    bases: frozenset
    motivo: str


def _dobra_inst(a: str, b: str) -> Instancia:
    ta, tb = CODIGOS[a], CODIGOS[b]
    return Instancia(f"dobraR@{a}>{b}", "dobraR", FUN(FUN(ta, tb, tb), tb, L(ta), tb), _dobraR,
                     frozenset({_E0p, _E0pm, _E0m}), f"τ de primitivas de lista com elemento {a}, acumulador {b}")


INSTANCIAS: List[Instancia] = [
    # Grade
    Instancia("celula", "celula", FUN(GRADE, POS, BOOL), _celula, TODAS_BASES, "monomórfica"),
    Instancia("posicoes", "posicoes", FUN(GRADE, LP), _posicoes, TODAS_BASES, "monomórfica; ordem linha a linha"),
    Instancia("pretas", "pretas", FUN(GRADE, LP), _pretas, TODAS_BASES, "monomórfica; ordem linha a linha"),
    Instancia("linhas", "linhas", FUN(GRADE, LLP), _linhas, SO_E0, "monomórfica"),
    Instancia("colunas", "colunas", FUN(GRADE, LLP), _colunas, SO_E0, "monomórfica"),
    Instancia("linhaDe", "linhaDe", FUN(GRADE, POS, LP), _linhaDe, SO_E0p, "monomórfica (recebe a grade, como vizinhos)"),
    Instancia("colunaDe", "colunaDe", FUN(GRADE, POS, LP), _colunaDe, SO_E0p, "monomórfica"),
    Instancia("vizinhos", "vizinhos", FUN(GRADE, POS, LP), _vizinhos, TODAS_BASES, "monomórfica; cima, baixo, esquerda, direita"),
    # Bool
    Instancia("verdadeiro", "verdadeiro", BOOL, lambda ctx: True, TODAS_BASES, "monomórfica"),
    Instancia("falso", "falso", BOOL, lambda ctx: False, TODAS_BASES, "monomórfica"),
    Instancia("e", "e", FUN(BOOL, BOOL, BOOL), lambda ctx, a, b: a and b, TODAS_BASES, "monomórfica"),
    Instancia("ou", "ou", FUN(BOOL, BOOL, BOOL), lambda ctx, a, b: a or b, TODAS_BASES, "monomórfica"),
    Instancia("nao", "nao", FUN(BOOL, BOOL), lambda ctx, a: not a, TODAS_BASES, "monomórfica"),
    Instancia("se@B", "se", FUN(BOOL, BOOL, BOOL, BOOL), lambda ctx, c, a, b: a if c else b, TODAS_BASES,
              "τ' de dobraR com acumulador Bool"),
    Instancia("se@LP", "se", FUN(BOOL, LP, LP, LP), lambda ctx, c, a, b: a if c else b, TODAS_BASES,
              "fecho, descartar; τ de filtrar@P"),
    Instancia("se@LLP", "se", FUN(BOOL, LLP, LLP, LLP), lambda ctx, c, a, b: a if c else b, TODAS_BASES,
              "τ de filtrar@LP; τ' de dobraR com acumulador L (L Pos)"),
    # Pos
    Instancia("igualP", "igualP", FUN(POS, POS, BOOL), lambda ctx, p, q: p == q, TODAS_BASES, "monomórfica"),
    # Lista: construtores e destrutores
    Instancia("vazio@P", "vazio", LP, lambda ctx: (), TODAS_BASES, "componenteDe; τ"),
    Instancia("vazio@LP", "vazio", LLP, lambda ctx: (), TODAS_BASES, "τ de mapear/linhas"),
    Instancia("cons@P", "cons", FUN(POS, LP, LP), _cons, TODAS_BASES, "componenteDe; τ"),
    Instancia("cons@LP", "cons", FUN(LP, LLP, LLP), _cons, TODAS_BASES, "τ de mapear/linhas/reverter"),
    Instancia("vazia?@P", "vazia?", FUN(LP, BOOL), lambda ctx, l: len(l) == 0, TODAS_BASES, "escada"),
    Instancia("vazia?@LP", "vazia?", FUN(LLP, BOOL), lambda ctx, l: len(l) == 0, TODAS_BASES, "τ' de dobraR@LP>·"),
    Instancia("cabeca@P", "cabeca", FUN(LP, POS), _cabeca(POS), TODAS_BASES, "UmComponente; τ de linhas"),
    Instancia("cabeca@LP", "cabeca", FUN(LLP, LP), _cabeca(LP), TODAS_BASES, "PrimeiraUltimaIguais, LinhasIguais"),
    Instancia("cauda@P", "cauda", FUN(LP, LP), lambda ctx, l: l[1:], TODAS_BASES, "descartar"),
    Instancia("cauda@LP", "cauda", FUN(LLP, LLP), lambda ctx, l: l[1:], TODAS_BASES, "τ' de dobraR@LP>·"),
    # Lista: combinadores de E0
    Instancia("mapear@P>LP", "mapear", FUN(FUN(POS, LP), LP, LLP), _mapear, SO_E0, "passo"),
    Instancia("filtrar@P", "filtrar", FUN(FUN(POS, BOOL), LP, LP), _filtrar, SO_E0, "vizPretos, pretasDe"),
    Instancia("filtrar@LP", "filtrar", FUN(FUN(LP, BOOL), LLP, LLP), _filtrar, SO_E0, "τ' de linhaDe/colunaDe"),
    Instancia("algum@P", "algum", FUN(FUN(POS, BOOL), LP, BOOL), _algum, SO_E0, "ParAdjacente"),
    Instancia("todos@P", "todos", FUN(FUN(POS, BOOL), LP, BOOL), _todos, SO_E0, "NenhumaIsolada, UmComponente"),
    Instancia("todos@LP", "todos", FUN(FUN(LP, BOOL), LLP, BOOL), _todos, SO_E0, "LinhasIguais"),
    Instancia("concatenar@P", "concatenar", FUN(LP, LP, LP), _concatenar, SO_E0, "instância mínima (U12)"),
    Instancia("juntar", "juntar", FUN(LLP, LP), _juntar, SO_E0, "passo"),
    Instancia("reverter@LP", "reverter", FUN(LLP, LLP), lambda ctx, l: l[::-1], SO_E0, "PrimeiraUltimaIguais"),
    Instancia("pertence", "pertence", FUN(POS, LP, BOOL), lambda ctx, x, l: x in l, SO_E0, "UmComponente; Pos apenas (2.3.2)"),
    Instancia("uniao", "uniao", FUN(LP, LP, LP), _uniao, SO_E0, "passo; Pos apenas (2.3.2)"),
    Instancia("diferenca", "diferenca", FUN(LP, LP, LP), _diferenca, SO_E0, "fecho; Pos apenas (2.3.2)"),
    # dobraR: E0', E0'+ e E0+ (não E0)
    _dobra_inst("P", "B"), _dobra_inst("P", "LP"), _dobra_inst("P", "LLP"),
    _dobra_inst("LP", "B"), _dobra_inst("LP", "LP"), _dobra_inst("LP", "LLP"),
    # ateFixo (E0+, E0'+)
    Instancia("ateFixo@P", "ateFixo", FUN(FUN(LP, LP), LP, LP), _ateFixo, frozenset({_E0m, _E0pm}),
              "fecho em E0+ (2.8.3)"),
]

#: primitivas genéricas de cada base (documento 02, 2.3.2/2.3.3, 2.8.3); 'fix' é formador de termo
GENERICAS_E0 = ["celula", "posicoes", "pretas", "linhas", "colunas", "vizinhos",
                "verdadeiro", "falso", "e", "ou", "nao", "se", "igualP",
                "vazio", "cons", "vazia?", "cabeca", "cauda", "mapear", "filtrar", "algum", "todos",
                "concatenar", "juntar", "reverter", "pertence", "uniao", "diferenca", "fix"]
GENERICAS_E0P = ["celula", "posicoes", "pretas", "linhaDe", "colunaDe", "vizinhos",
                 "verdadeiro", "falso", "e", "ou", "nao", "se", "igualP",
                 "vazio", "cons", "vazia?", "cabeca", "cauda", "dobraR", "fix"]
GENERICAS_E0MAIS = GENERICAS_E0 + ["ateFixo", "dobraR"]
GENERICAS_E0PMAIS = GENERICAS_E0P + ["ateFixo"]

def _construir(base: str, prov_base: str, extras_mais: Iterable[str] = ()) -> Tabela:
    extras = set(extras_mais)
    prims = []
    for i in INSTANCIAS:
        if base in i.bases:
            prov = "E0mais" if i.generico in extras else prov_base
            prims.append(Primitiva(i.nome, i.tipo, i.impl, prov, i.generico, motivo=i.motivo))
    return Tabela(base, prims, "base")


E0 = _construir(_E0, "E0")
E0P = _construir(_E0p, "E0p")
E0MAIS = _construir(_E0m, "E0", extras_mais=("ateFixo", "dobraR"))
E0PMAIS = _construir(_E0pm, "E0p", extras_mais=("ateFixo",))

BASES: Dict[str, Tabela] = {"E0": E0, "E0p": E0P, "E0mais": E0MAIS, "E0pmais": E0PMAIS}

#: registro global por nome de instância (as implementações não dependem da base)
REGISTRO_BASE: Dict[str, Primitiva] = {}
for _t in (E0, E0P, E0MAIS, E0PMAIS):
    for _p in _t:
        REGISTRO_BASE.setdefault(_p.nome, _p)

# ---------------------------------------------------------------------
# Tabela SISTEMÁTICA (não curada) — achado de revisão
# ---------------------------------------------------------------------
# As INSTANCIAS acima foram escolhidas olhando os programas da escada ("o MÍNIMO exigido pelos programas
# da escada"): é uma curadoria que recorta o espaço de busca com conhecimento das soluções manuais
# (desvio declarado em piloto.DESVIOS_ESCALA). A tabela sistemática usa um critério fixado SEM olhar a
# escada, só a partir das assinaturas polimórficas do documento 02, 2.3.2/2.3.3/2.8.3:
#   elementos A = {Pos, L Pos} (os tipos de elemento que as primitivas de grade produzem);
#   valores   V = {Bool, Pos, L Pos, L (L Pos)};
#   toda primitiva polimórfica é instanciada em TODAS as escolhas de variáveis de tipo em A (elementos)
#   ou V (resultado de se, acumulador de dobraR) cujo tipo resultante só usa Grade, V e setas;
#   pertence, uniao, diferenca e igualP ficam só em Pos (o documento 02 as declara assim).
# Resultado: as instâncias curadas mais se@P, mapear@P>P, mapear@LP>P, mapear@LP>LP, algum@LP,
# concatenar@LP, reverter@P, dobraR@P>P, dobraR@LP>P e ateFixo@LP (juntar@LP exigiria L(L(L Pos)) ∉ V).
INSTANCIAS_EXTRA_SISTEMATICAS: List[Instancia] = [
    Instancia("se@P", "se", FUN(BOOL, POS, POS, POS), lambda ctx, c, a, b: a if c else b, TODAS_BASES,
              "sistemática: se em V"),
    Instancia("mapear@P>P", "mapear", FUN(FUN(POS, POS), LP, LP), _mapear, SO_E0, "sistemática: a, b ∈ A"),
    Instancia("mapear@LP>P", "mapear", FUN(FUN(LP, POS), LLP, LP), _mapear, SO_E0, "sistemática: a, b ∈ A"),
    Instancia("mapear@LP>LP", "mapear", FUN(FUN(LP, LP), LLP, LLP), _mapear, SO_E0, "sistemática: a, b ∈ A"),
    Instancia("algum@LP", "algum", FUN(FUN(LP, BOOL), LLP, BOOL), _algum, SO_E0, "sistemática: a ∈ A"),
    Instancia("concatenar@LP", "concatenar", FUN(LLP, LLP, LLP), _concatenar, SO_E0, "sistemática: a ∈ A"),
    Instancia("reverter@P", "reverter", FUN(LP, LP), lambda ctx, l: l[::-1], SO_E0, "sistemática: a ∈ A"),
    _dobra_inst("P", "P"), _dobra_inst("LP", "P"),
    Instancia("ateFixo@LP", "ateFixo", FUN(FUN(LLP, LLP), LLP, LLP), _ateFixo, frozenset({_E0m, _E0pm}),
              "sistemática: a ∈ A"),
]
INSTANCIAS_SISTEMATICAS: List[Instancia] = INSTANCIAS + INSTANCIAS_EXTRA_SISTEMATICAS


def _construir_sistematica(base: str, prov_base: str, extras_mais: Iterable[str] = ()) -> Tabela:
    extras = set(extras_mais)
    prims = [Primitiva(i.nome, i.tipo, i.impl, "E0mais" if i.generico in extras else prov_base, i.generico,
                       motivo=i.motivo) for i in INSTANCIAS_SISTEMATICAS if base in i.bases]
    return Tabela(f"{base}/sistematica", prims, "base")


#: tabelas NÃO curadas (critério acima), só para medir o efeito da curadoria em PM8/PM10
BASES_SISTEMATICAS: Dict[str, Tabela] = {
    "E0": _construir_sistematica(_E0, "E0"), "E0p": _construir_sistematica(_E0p, "E0p"),
    "E0mais": _construir_sistematica(_E0m, "E0", extras_mais=("ateFixo", "dobraR")),
    "E0pmais": _construir_sistematica(_E0pm, "E0p", extras_mais=("ateFixo",))}
for _t in BASES_SISTEMATICAS.values():
    for _p in _t:
        REGISTRO_BASE.setdefault(_p.nome, _p)

#: tipos das tarefas da escada (contextos de tipo do enumerador)
TIPOS_TAREFA = [FUN(GRADE, BOOL), FUN(GRADE, POS, LP), FUN(GRADE, LP, LP), FUN(LP, LP, LP), FUN(LP, LP, BOOL)]


def universo_tipos(tabelas: Iterable[Tabela], extras: Iterable[Tipo] = ()) -> frozenset:
    """Tipos base + tipos das assinaturas + `extras`, fechado por subtipos (componentes de setas)."""
    out = {BOOL, POS, GRADE, LP, LLP}
    for tb in tabelas:
        for p in tb:
            out |= subtipos(p.tipo)
    for t in extras:
        out |= subtipos(t)
    return frozenset(out)


#: conjunto finito usado pelo enumerador
UNIVERSO_TIPOS = universo_tipos(BASES.values(), TIPOS_TAREFA)


def tabela_resumo() -> str:
    """Tabela Markdown das instâncias por primitiva genérica e base."""
    linhas = ["| genérica | instância | tipo | E0 | E0' | E0+ | E0'+ | motivo |", "|---|---|---|---|---|---|---|---|"]
    for i in INSTANCIAS:
        marca = lambda b: "x" if b in i.bases else ""
        linhas.append(f"| {i.generico} | `{i.nome}` | {tipo_str(i.tipo)} | {marca(_E0)} | {marca(_E0p)} | "
                      f"{marca(_E0m)} | {marca(_E0pm)} | {i.motivo} |")
    linhas.append("| fix | `fix` (formador de termo) | (τ → τ) → τ, τ qualquer | x | x | x | x | recursão |")
    linhas.append("")
    for nome, tb in BASES.items():
        linhas.append(f"- {nome}: {len(tb)} instâncias + fix; {len(tb.genericos()) + 1} primitivas genéricas")
    return "\n".join(linhas)


# =====================================================================
# Verificação de tipos
# =====================================================================
class ErroTipo(TypeError):
    pass


def tipo_de(t: Termo, contexto: Optional[Dict[str, Tipo]] = None, tabela=None) -> Tipo:
    """Tipo de t no contexto (var → tipo) com constantes de `tabela` (Tabela ou dict nome→Primitiva).
    Sem tabela, usa REGISTRO_BASE (todas as instâncias de base). Levanta ErroTipo se mal tipado."""
    ctx = dict(contexto or {})
    tab = tabela if tabela is not None else REGISTRO_BASE
    return _tipo(t, ctx, tab)


def _tipo(t, ctx, tab):
    k = t[0]
    if k == "v":
        if t[1] not in ctx:
            raise ErroTipo(f"variável livre sem tipo: {t[1]}")
        return ctx[t[1]]
    if k == "c":
        p = tab.get(t[1]) if hasattr(tab, "get") else None
        if p is None:
            raise ErroTipo(f"constante desconhecida: {t[1]}")
        return p.tipo
    if k == "ap":
        tf = _tipo(t[1], ctx, tab)
        tx = _tipo(t[2], ctx, tab)
        if tf[0] != "Fun":
            raise ErroTipo(f"aplicação de não-função: {imprimir(t[1])} : {tipo_str(tf)}")
        if tf[1] != tx:
            raise ErroTipo(f"argumento de tipo {tipo_str(tx)} onde se esperava {tipo_str(tf[1])} em {imprimir(t)}")
        return tf[2]
    if k == "lam":
        if not tipo_valido(t[2]):
            raise ErroTipo(f"anotação inválida: {t[2]!r}")
        c2 = dict(ctx); c2[t[1]] = t[2]
        return FUN(t[2], _tipo(t[3], c2, tab))
    if k == "fix":
        if not tipo_valido(t[1]):
            raise ErroTipo(f"anotação de fix inválida: {t[1]!r}")
        tf = _tipo(t[2], ctx, tab)
        if tf != FUN(t[1], t[1]):
            raise ErroTipo(f"fix em {tipo_str(t[1])} exige f : τ → τ, obtido {tipo_str(tf)}")
        return t[1]
    raise ErroTipo(f"termo inválido: {t!r}")


def bem_tipado(t: Termo, tipo: Tipo, contexto=None, tabela=None) -> bool:
    try:
        return tipo_de(t, contexto, tabela) == tipo
    except ErroTipo:
        return False


def entrada_biblioteca(nome: str, corpo: Termo, proveniencia: str, base: Tabela,
                       anteriores: Iterable[Primitiva] = (), tipo: Optional[Tipo] = None) -> Primitiva:
    """Cria uma entrada de biblioteca (corpo fechado), verificando o tipo contra base + anteriores."""
    if proveniencia not in ("descoberta", "manual-teste"):
        raise ErroProveniencia("biblioteca aceita só 'descoberta' ou 'manual-teste'")
    tab = {p.nome: p for p in base}
    for p in anteriores:
        tab[p.nome] = p
    t = tipo_de(corpo, {}, tab)
    if tipo is not None and t != tipo:
        raise ErroTipo(f"{nome}: tipo declarado {tipo_str(tipo)} ≠ inferido {tipo_str(t)}")
    return Primitiva(nome, t, None, proveniencia, nome, corpo=corpo)
