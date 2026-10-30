#!/usr/bin/env python3
"""Validador AUTÓNOMO de um pacote de benchmark para o ambiente de grades (contrato público, §6).

Uso:
    python3 validar_pacote.py <pasta-do-pacote>              # valida e imprime o relatório
    python3 validar_pacote.py <pasta-do-pacote> --congelar   # valida e escreve MANIFESTO.json com os hashes

Não depende de nada além dos módulos padrão do Python e de grade.py (ao lado). Verifica o formato de
tarefas.json, as referências de referencias.py (tipos das saídas, determinismo, totalidade na
bateria de entradas), a presença das duas classes nos predicados dentro da partição de treino,
os ficheiros selados opcionais (testes_ocultos.json, testemunhas.json) e calcula o hash do pacote.
O mesmo algoritmo de hash é usado pelo avaliador para conferir o congelamento.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import random
import re
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade import Grade  # noqa: E402

# ---------------------------------------------------------------- tipos aceites
TIPOS_ACEITOS: Dict[str, Tuple[List[str], str]] = {
    "Grade -> Bool": (["Grade"], "Bool"),
    "Grade -> Pos -> Bool": (["Grade", "Pos"], "Bool"),
    "Grade -> Pos -> L Pos": (["Grade", "Pos"], "L Pos"),
    "Grade -> L Pos -> Bool": (["Grade", "L Pos"], "Bool"),
    "Grade -> L Pos -> L Pos": (["Grade", "L Pos"], "L Pos"),
    "Grade -> L Pos": (["Grade"], "L Pos"),
    "L Pos -> L Pos -> Bool": (["L Pos", "L Pos"], "Bool"),
    "L Pos -> L Pos -> L Pos": (["L Pos", "L Pos"], "L Pos"),
}
NATUREZAS = ("predicado", "funcao")
COMPARACOES = ("exata", "conjunto")
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,31}$")
PARTICAO_TREINO = range(0, 20)          # baldes 0–19 (ver contrato, §2.4)
NUM_BALDES = 100
PS_NATURAL = (0.20, 0.35, 0.50, 0.65)

PRIMITIVAS_E0 = [
    "celula", "posicoes", "pretas", "linhas", "colunas", "vizinhos", "verdadeiro", "falso", "e", "ou", "nao",
    "se@B", "se@LP", "se@LLP", "igualP", "vazio@P", "vazio@LP", "cons@P", "cons@LP", "vazia?@P", "vazia?@LP",
    "cabeca@P", "cabeca@LP", "cauda@P", "cauda@LP", "mapear@P>LP", "filtrar@P", "filtrar@LP", "algum@P",
    "todos@P", "todos@LP", "concatenar@P", "juntar", "reverter@LP", "pertence", "uniao", "diferenca",
]


# ---------------------------------------------------------------- baterias de entradas (iguais às do ambiente)
def _unicos(xs):
    out, vistos = [], set()
    for x in xs:
        if x not in vistos:
            vistos.add(x)
            out.append(x)
    return out


def bateria_lp(g: Grade) -> List[tuple]:
    pretas, pos = tuple(g.pretas()), tuple(g.posicoes())
    return _unicos([(), pretas[:1], pretas[-1:], pretas, pos] + [tuple(l) for l in g.linhas()] + [tuple(c) for c in g.colunas()])


def bateria_listas_pretas(g: Grade) -> List[tuple]:
    def pretos(ps):
        return tuple(q for q in ps if g.celula(q))
    return _unicos([()] + [pretos(l) for l in g.linhas()] + [pretos(c) for c in g.colunas()] + [tuple(g.pretas())])


def entradas_da_grade(args: List[str], g: Grade) -> List[tuple]:
    if args == ["Grade", "Pos"]:
        return [(g, p) for p in g.posicoes()]
    if args == ["Grade", "L Pos"]:
        return [(g, S) for S in bateria_lp(g)]
    if args == ["L Pos", "L Pos"]:
        ls = bateria_listas_pretas(g)
        return _unicos([(A, B) for A in ls for B in ls])
    if args == ["Grade"]:
        return [(g,)]
    raise ValueError(args)


def todas_as_grades(n: int):
    total = n * n
    for k in range(1 << total):
        yield Grade(n, tuple((k >> (total - 1 - t)) & 1 for t in range(total)))


def amostra_natural(n: int, rng: random.Random) -> Grade:
    p = rng.choice(PS_NATURAL)
    return Grade(n, tuple(1 if rng.random() < p else 0 for _ in range(n * n)))


# ---------------------------------------------------------------- verificação de saídas
def _eh_pos(v, n: int) -> bool:
    return isinstance(v, tuple) and len(v) == 2 and all(isinstance(x, int) and not isinstance(x, bool) for x in v) \
        and 1 <= v[0] <= n and 1 <= v[1] <= n


def verificar_saida(v, resultado: str, comparacao: str, n: int) -> Optional[str]:
    """None se v tem o tipo declarado; senão a mensagem do problema."""
    if resultado == "Bool":
        return None if isinstance(v, bool) else f"saída {v!r} não é bool"
    if resultado == "Pos":
        return None if _eh_pos(v, n) else f"saída {v!r} não é uma posição válida"
    if resultado == "L Pos":
        if comparacao == "exata" and not isinstance(v, (list, tuple)):
            return f"saída {v!r}: comparação 'exata' exige lista/tupla ordenada"
        if not isinstance(v, (list, tuple, set, frozenset)):
            return f"saída {v!r} não é uma coleção de posições"
        for x in v:
            if not _eh_pos(x, n):
                return f"elemento {x!r} não é uma posição válida"
        return None
    return f"tipo de resultado desconhecido {resultado}"


# ---------------------------------------------------------------- carregamento
def carregar_modulo(caminho: str, nome: str):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def hash_ficheiro(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 16), b""):
            h.update(bloco)
    return h.hexdigest()


def ficheiros_do_pacote(pasta: str) -> List[str]:
    out = []
    for raiz, dirs, fich in os.walk(pasta):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__" and not d.startswith("."))
        for f in sorted(fich):
            if f == "MANIFESTO.json" or f.endswith(".pyc") or f.startswith("."):
                continue
            out.append(os.path.relpath(os.path.join(raiz, f), pasta).replace(os.sep, "/"))
    return sorted(out)


def hashes_do_pacote(pasta: str) -> Dict[str, str]:
    return {rel: hash_ficheiro(os.path.join(pasta, rel)) for rel in ficheiros_do_pacote(pasta)}


def hash_pacote(hashes: Dict[str, str]) -> str:
    linhas = "\n".join(f"{k}  {v}" for k, v in sorted(hashes.items()))
    return hashlib.sha256(linhas.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- validação
class Relatorio:
    def __init__(self):
        self.erros: List[str] = []
        self.avisos: List[str] = []
        self.estatisticas: Dict[str, Any] = {}

    def erro(self, m: str):
        self.erros.append(m)

    def aviso(self, m: str):
        self.avisos.append(m)

    def ok(self) -> bool:
        return not self.erros

    def texto(self) -> str:
        L = [f"erros: {len(self.erros)}", *[f"  ERRO  {e}" for e in self.erros],
             f"avisos: {len(self.avisos)}", *[f"  aviso {a}" for a in self.avisos],
             "estatísticas:", json.dumps(self.estatisticas, ensure_ascii=False, indent=1)]
        return "\n".join(L)


def validar(pasta: str, amostras_n5: int = 300, semente: int = 7) -> Relatorio:
    r = Relatorio()
    rng = random.Random(semente)
    # --- tarefas.json
    cam = os.path.join(pasta, "tarefas.json")
    if not os.path.exists(cam):
        r.erro("tarefas.json ausente")
        return r
    try:
        with open(cam, encoding="utf-8") as f:
            doc = json.load(f)
    except Exception as e:  # noqa: BLE001
        r.erro(f"tarefas.json inválido: {e}")
        return r
    tarefas = doc.get("tarefas")
    if not isinstance(tarefas, list) or not tarefas:
        r.erro("tarefas.json: campo 'tarefas' deve ser uma lista não vazia")
        return r
    ids = []
    for t in tarefas:
        tid = t.get("id")
        if not isinstance(tid, str) or not ID_RE.match(tid):
            r.erro(f"id inválido: {tid!r} (letras, dígitos e _, até 32 caracteres, começando por letra)")
            continue
        if tid in ids:
            r.erro(f"id repetido: {tid}")
        ids.append(tid)
        tipo = t.get("tipo")
        if tipo not in TIPOS_ACEITOS:
            r.erro(f"{tid}: tipo {tipo!r} não aceite; aceites: {sorted(TIPOS_ACEITOS)}")
            continue
        args, res = TIPOS_ACEITOS[tipo]
        nat = t.get("natureza")
        if nat not in NATUREZAS:
            r.erro(f"{tid}: natureza {nat!r} inválida")
        elif (nat == "predicado") != (tipo == "Grade -> Bool"):
            r.erro(f"{tid}: natureza 'predicado' se e só se o tipo é 'Grade -> Bool'")
        comp = t.get("comparacao", "exata")
        if comp not in COMPARACOES:
            r.erro(f"{tid}: comparacao {comp!r} inválida")
        if comp == "conjunto" and res != "L Pos":
            r.erro(f"{tid}: comparacao 'conjunto' só para resultado 'L Pos'")
        if not isinstance(t.get("descricao", ""), str):
            r.erro(f"{tid}: descricao deve ser texto")
    if r.erros:
        return r
    # --- referencias.py
    cam = os.path.join(pasta, "referencias.py")
    if not os.path.exists(cam):
        r.erro("referencias.py ausente")
        return r
    try:
        mod = carregar_modulo(cam, "referencias_pacote")
    except Exception as e:  # noqa: BLE001
        r.erro(f"referencias.py não importa: {type(e).__name__}: {e}")
        return r
    refs = getattr(mod, "REFERENCIAS", None)
    if not isinstance(refs, dict):
        r.erro("referencias.py deve definir o dicionário REFERENCIAS = {id: função}")
        return r
    refs_b = getattr(mod, "REFERENCIAS_B", {}) or {}
    positivos = getattr(mod, "POSITIVOS", {}) or {}
    faltam = [i for i in ids if i not in refs]
    extra = [i for i in refs if i not in ids]
    if faltam:
        r.erro(f"REFERENCIAS sem as tarefas: {faltam}")
    if extra:
        r.aviso(f"REFERENCIAS com ids que não estão em tarefas.json (ignorados): {extra}")
    for i, f in refs.items():
        if not callable(f):
            r.erro(f"REFERENCIAS[{i!r}] não é chamável")
    if r.erros:
        return r
    est: Dict[str, Any] = {}
    for t in tarefas:
        tid, tipo = t["id"], t["tipo"]
        args, res = TIPOS_ACEITOS[tipo]
        comp = t.get("comparacao", "exata")
        f = refs[tid]
        fb = refs_b.get(tid)
        e: Dict[str, Any] = {"entradas_verificadas": 0}
        # totalidade, tipo e determinismo em n = 1..3 (exaustivo) e amostras em n = 4, 5
        grades = [g for n in (1, 2, 3) for g in todas_as_grades(n)]
        grades += [amostra_natural(n, rng) for n in (4, 5) for _ in range(amostras_n5 // 2)]
        saidas_distintas = set()
        problema = None
        for g in grades:
            for a in entradas_da_grade(args, g):
                try:
                    v1 = f(*a)
                    v2 = f(*a)
                except Exception as ex:  # noqa: BLE001
                    problema = f"{tid}: referência levanta {type(ex).__name__} em {g.serializar()} {a[1:]!r}: {ex}"
                    break
                if v1 != v2:
                    problema = f"{tid}: referência não determinística em {g.serializar()}"
                    break
                m = verificar_saida(v1, res, comp, g.n)
                if m:
                    problema = f"{tid}: {m} (entrada {g.serializar()} {a[1:]!r})"
                    break
                if fb is not None:
                    vb = fb(*a)
                    iguais = (frozenset(v1) == frozenset(vb)) if (res == "L Pos" and comp == "conjunto") else (v1 == vb)
                    if not iguais:
                        problema = f"{tid}: REFERENCIAS e REFERENCIAS_B discordam em {g.serializar()} {a[1:]!r}"
                        break
                e["entradas_verificadas"] += 1
                chave = v1 if res != "L Pos" else (tuple(v1) if comp == "exata" else frozenset(v1))
                saidas_distintas.add(chave)
            if problema:
                break
        if problema:
            r.erro(problema)
            continue
        e["saidas_distintas"] = len(saidas_distintas)
        if len(saidas_distintas) <= 1:
            r.erro(f"{tid}: a referência devolve sempre a mesma saída em todas as entradas verificadas (tarefa degenerada)")
        # predicados: as duas classes na partição de treino em n = 3 e n = 4 (exaustivo) e frequência natural
        if t["natureza"] == "predicado":
            for n in (3, 4):
                pos = neg = 0
                pretas_pos, pretas_neg = set(), set()
                for g in todas_as_grades(n):
                    if g.balde(NUM_BALDES) not in PARTICAO_TREINO:
                        continue
                    if f(g):
                        pos += 1; pretas_pos.add(g.contagem_pretas())
                    else:
                        neg += 1; pretas_neg.add(g.contagem_pretas())
                e[f"n{n}_treino_positivos"], e[f"n{n}_treino_negativos"] = pos, neg
                e[f"n{n}_treino_pares_mesma_densidade"] = len(pretas_pos & pretas_neg)
            # o ambiente mostra 2 positivos e 2 negativos iniciais tirados da partição de treino em n = 4 ou 3
            if e["n3_treino_positivos"] + e["n4_treino_positivos"] < 2:
                r.erro(f"{tid}: menos de 2 positivos na partição de treino em n = 3 e n = 4 (o ambiente precisa de 2 exemplos positivos)")
            if e["n3_treino_negativos"] + e["n4_treino_negativos"] < 2:
                r.erro(f"{tid}: menos de 2 negativos na partição de treino em n = 3 e n = 4 (o ambiente precisa de 2 exemplos negativos)")
            if e["n3_treino_pares_mesma_densidade"] + e["n4_treino_pares_mesma_densidade"] == 0:
                r.aviso(f"{tid}: não há positivo e negativo com o mesmo número de pretas em n ≤ 4 (negativos emparelhados impossíveis)")
            for n in (5, 6):
                k = sum(1 for _ in range(amostras_n5) if f(amostra_natural(n, rng)))
                e[f"n{n}_freq_positivos_natural"] = round(k / amostras_n5, 3)
                if k == 0 or k == amostras_n5:
                    r.aviso(f"{tid}: uma só classe em {amostras_n5} grades naturais de n = {n} (freq. {k / amostras_n5:.2f})"
                            + ("" if tid in positivos else "; considere um gerador em POSITIVOS"))
            if tid in positivos:
                ok = tot = 0
                for _ in range(50):
                    g = positivos[tid](4, random.Random(rng.random()))
                    if g is None:
                        continue
                    tot += 1
                    if not isinstance(g, Grade) or g.n != 4:
                        r.erro(f"{tid}: POSITIVOS deve devolver Grade de lado n ou None"); break
                    ok += bool(f(g))
                e["positivos_gerador_taxa"] = round(ok / tot, 2) if tot else None
                if tot and ok == 0:
                    r.erro(f"{tid}: o gerador POSITIVOS nunca produz um positivo")
        if fb is None:
            r.aviso(f"{tid}: sem segunda implementação (REFERENCIAS_B); recomendada")
        est[tid] = e
    r.estatisticas["tarefas"] = est
    # --- selados opcionais
    cam = os.path.join(pasta, "testes_ocultos.json")
    if os.path.exists(cam):
        try:
            with open(cam, encoding="utf-8") as fh:
                oc = json.load(fh)
            n_oc = 0
            for tid, lista in oc.items():
                if tid not in ids:
                    r.erro(f"testes_ocultos.json: id desconhecido {tid}")
                    continue
                for s in lista:
                    g = Grade.de_texto(s)
                    if not 1 <= g.n <= 9:
                        r.erro(f"testes_ocultos.json[{tid}]: lado {g.n} fora de 1..9")
                    n_oc += 1
            r.estatisticas["testes_ocultos"] = n_oc
        except Exception as ex:  # noqa: BLE001
            r.erro(f"testes_ocultos.json inválido: {type(ex).__name__}: {ex}")
    cam = os.path.join(pasta, "testemunhas.json")
    if os.path.exists(cam):
        try:
            with open(cam, encoding="utf-8") as fh:
                tst = json.load(fh)
            for tid, prog in tst.items():
                if tid not in ids:
                    r.erro(f"testemunhas.json: id desconhecido {tid}")
                    continue
                if not isinstance(prog, str) or prog.count("(") != prog.count(")"):
                    r.erro(f"testemunhas.json[{tid}]: parênteses desequilibrados")
                    continue
                toks = [x for x in re.split(r"[\s()]+", prog) if x]
                desconhecidos = [x for x in toks if x not in PRIMITIVAS_E0 and x != "\\" and not re.match(r"^[a-z][A-Za-z0-9]*$", x)
                                 and x not in ("Grade", "Pos", "Bool", "LP", "LLP")]
                if desconhecidos:
                    r.aviso(f"testemunhas.json[{tid}]: símbolos fora de E0 (a confirmar pelo avaliador): {desconhecidos}")
            r.estatisticas["testemunhas"] = len(tst)
        except Exception as ex:  # noqa: BLE001
            r.erro(f"testemunhas.json inválido: {type(ex).__name__}: {ex}")
    # --- hash
    hs = hashes_do_pacote(pasta)
    r.estatisticas["ficheiros"] = sorted(hs)
    r.estatisticas["hash_pacote"] = hash_pacote(hs)
    r.estatisticas["num_tarefas"] = len(ids)
    r.estatisticas["por_tipo"] = {tp: sum(1 for t in tarefas if t["tipo"] == tp) for tp in TIPOS_ACEITOS if any(t["tipo"] == tp for t in tarefas)}
    return r


def congelar(pasta: str, relatorio: Relatorio) -> dict:
    """Escreve MANIFESTO.json (só se a validação não tem erros)."""
    if not relatorio.ok():
        raise SystemExit("não congelado: a validação tem erros")
    import datetime as dt
    hs = hashes_do_pacote(pasta)
    with open(os.path.join(pasta, "tarefas.json"), encoding="utf-8") as f:
        doc = json.load(f)
    man = {"nome": doc.get("nome", os.path.basename(os.path.abspath(pasta))), "versao": doc.get("versao", "1"),
           "autor": doc.get("autor", ""), "congelado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "num_tarefas": relatorio.estatisticas["num_tarefas"], "arquivos": hs, "hash_pacote": hash_pacote(hs),
           "algoritmo": "sha256 das linhas '<caminho>  <sha256 do ficheiro>' ordenadas, excluindo MANIFESTO.json"}
    with open(os.path.join(pasta, "MANIFESTO.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1, sort_keys=True)
    return man


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta")
    ap.add_argument("--congelar", action="store_true")
    a = ap.parse_args(argv)
    rel = validar(a.pasta)
    print(rel.texto())
    if a.congelar:
        man = congelar(a.pasta, rel)
        print("MANIFESTO.json escrito; hash do pacote:", man["hash_pacote"])
    return 0 if rel.ok() else 1


if __name__ == "__main__":
    sys.exit(main())
