"""Auditoria de frequência de positivos por conceito, tamanho de grade e parâmetro p.

Uso: python3 -I analysis/audit_frequencias.py [amostras_por_celula]
Sem dependências externas. Determinístico (semente fixa).
Fórmulas exatas onde existem; Monte Carlo para conceitos de componentes.
"""
import sys, math, random
from collections import deque

NS = [3, 4, 5, 6, 7, 8, 9]
PS = [0.20, 0.35, 0.50, 0.65]
SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
SEED = 12345

def binom_pmf(n, k, p):
    return math.comb(n, k) * p**k * (1-p)**(n-k)

# ---------- exatas ----------
def p_topo_cheio(n, p): return p**n
def p_linha_ocupada(n, p): return (1 - (1-p)**n)**n
def p_linhas_iguais(n, p): return sum(binom_pmf(n, k, p)**n for k in range(n+1))
def p_primeira_ultima(n, p): return sum(binom_pmf(n, k, p)**2 for k in range(n+1))
def p_metades_iguais(n, p):
    m = n * (n // 2)
    return sum(binom_pmf(m, k, p)**2 for k in range(m+1))
def p_canto(n, p): return p
def p_diagonal(n, p): return p**n
def p_coluna2_vazia(n, p): return (1-p)**n
def p_row_no_pair(n, p):
    # DP: strings of length n with no two consecutive 1s, weighted by Bernoulli(p)
    a, b = 1.0, 0.0  # a: ends in 0 (or empty), b: ends in 1
    for _ in range(n):
        a, b = (a + b) * (1-p), a * p
    return a + b
def p_par_direita(n, p): return 1 - p_row_no_pair(n, p)**n

EXACT = {
    "TopoCheio (F1)": p_topo_cheio,
    "ParDireita (F1)": p_par_direita,
    "LinhaOcupada (F1)": p_linha_ocupada,
    "LinhasIguais (F3)": p_linhas_iguais,
    "MetadesIguais (F3)": p_metades_iguais,
    "PrimeiraUltimaIguais (F3, proposta)": p_primeira_ultima,
    "CantoSupEsq (F1')": p_canto,
    "Diagonal (F1')": p_diagonal,
    "ColunaDoisVazia (F1')": p_coluna2_vazia,
}

# ---------- Monte Carlo ----------
def components(g, n):
    seen = [[False]*n for _ in range(n)]
    comps = []
    for i in range(n):
        for j in range(n):
            if g[i][j] and not seen[i][j]:
                q = deque([(i, j)]); seen[i][j] = True; cells = []
                while q:
                    a, b = q.popleft(); cells.append((a, b))
                    for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                        x, y = a+da, b+db
                        if 0 <= x < n and 0 <= y < n and g[x][y] and not seen[x][y]:
                            seen[x][y] = True; q.append((x, y))
                comps.append(cells)
    return comps

def mc_concepts(g, n, comps):
    sizes = [len(c) for c in comps]
    k = len(comps)
    touches_border = lambda c: any(a == 0 or a == n-1 or b == 0 or b == n-1 for a, b in c)
    maior = max(sizes) if sizes else 0
    empty_rows = sum(1 for i in range(n) if not any(g[i]))
    row1 = sum(g[0])
    straight = lambda c: len({a for a, b in c}) == 1 or len({b for a, b in c}) == 1
    return {
        "UmComponente (F2)": k == 1,
        "DoisSeparados (F2)": k == 2,
        "TresComponentes (F2, proposta)": k == 3,
        "PeloMenosDois (F2, proposta)": k >= 2,
        "MaiorTocaBorda (F2)": k > 0 and any(len(c) == maior and touches_border(c) for c in comps),
        "ExisteComponenteReto>=2 (F2, proposta)": any(len(c) >= 2 and straight(c) for c in comps),
        "NenhumaIsolada (F2, proposta)": k > 0 and min(sizes) >= 2,
        "TodosMesmoTamanho (F2xF3, proposta)": k > 0 and len(set(sizes)) == 1,
        "ComponentesVsVazias (F3, v0.1)": k == empty_rows,
        "ComponentesIgualLinha1 (F2xF3, proposta)": k == row1,
        "LinhaIgualColuna (F3, proposta)": all(sum(g[i]) == sum(g[j][i] for j in range(n)) for i in range(n)),
    }

def run_mc():
    rng = random.Random(SEED)
    out = {}  # name -> {(n,p): freq}
    for n in NS:
        for p in PS:
            counts = {}
            for _ in range(SAMPLES):
                g = [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(n)]
                res = mc_concepts(g, n, components(g, n))
                for name, v in res.items():
                    counts[name] = counts.get(name, 0) + (1 if v else 0)
            for name, c in counts.items():
                out.setdefault(name, {})[(n, p)] = c / SAMPLES
    return out

def fmt(x):
    if x == 0: return "0"
    if x < 1e-3: return f"{x:.1e}"
    return f"{x:.3f}"

def table(name, f):
    lines = [f"**{name}**", "", "| n | " + " | ".join(f"p={p}" for p in PS) + " | mistura |", "|---|" + "---|"*(len(PS)+1)]
    for n in NS:
        vals = [f(n, p) for p in PS]
        lines.append(f"| {n} | " + " | ".join(fmt(v) for v in vals) + f" | {fmt(sum(vals)/len(vals))} |")
    return "\n".join(lines) + "\n"

def sign_test_power(n, pi, alpha=0.05):
    # critical value: smallest c with P(Bin(n,0.5) >= c) <= alpha
    for c in range(n+1):
        if sum(binom_pmf(n, k, 0.5) for k in range(c, n+1)) <= alpha:
            return c, sum(binom_pmf(n, k, pi) for k in range(c, n+1))
    return n+1, 0.0

def main():
    print(f"# Saída da auditoria de frequências (amostras MC por célula: {SAMPLES}, semente {SEED})\n")
    print("Frequência de positivos sob Bernoulli(p) i.i.d. por célula; 'mistura' = média uniforme sobre p.\n")
    print("## Fórmulas exatas\n")
    for name, f in EXACT.items():
        print(table(name, f))
    print("## Monte Carlo\n")
    mc = run_mc()
    for name in sorted(mc):
        print(table(name, lambda n, p, name=name: mc[name][(n, p)]))
    print("## Potência do teste de sinal pareado por conceito (alpha = 0,05, unilateral)\n")
    print("| conceitos (k) | " + " | ".join(f"pi={pi}" for pi in (0.7, 0.8, 0.9)) + " |")
    print("|---|---|---|---|")
    for k in (3, 6, 10, 15, 20, 30):
        cells = []
        for pi in (0.7, 0.8, 0.9):
            c, pw = sign_test_power(k, pi)
            cells.append(f"{pw:.2f} (crít. {c}/{k})")
        print(f"| {k} | " + " | ".join(cells) + " |")

if __name__ == "__main__":
    main()
