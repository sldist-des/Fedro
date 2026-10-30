# Experimento mínimo — registros (exploratoria-minima, semente 10002, B = 20000, política tamanho)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307717 | 6307717 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | False | 0 | orcamento_enumeracao |  | `` |  | 109655765 | 115963482 | 21282 |  /  /  |
| L-fix | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 91826937 | 207790419 | 41283 |  /  /  |
| L-fix | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 138795451 | 346585870 | 61284 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307810 | 6307810 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | False | 0 | orcamento_enumeracao |  | `` |  | 109655765 | 115963575 | 21282 |  /  /  |
| L-lib | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 91826937 | 207790512 | 41283 |  /  /  |
| L-lib | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 138795451 | 346585963 | 61284 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307825 | 6307825 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 4550621 | 10858446 | 3729 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 7 | `λx0. nao (vazia?@P (abs2 x0 (pretas x0)))` | abs2 | 3762043 | 14620489 | 5465 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 100061162 | 114681651 | 25466 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307825 | 6307825 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 4550621 | 10858446 | 3729 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 91826937 | 102685383 | 23730 |  /  /  |
| L-lib+f/lesao | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 138795451 | 241480834 | 43731 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6154228 | 6154228 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 5873897 | 12028125 | 4094 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 78632505 | 90660630 | 24095 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 91793613 | 182454243 | 44096 |  /  /  |
| L-fix/custo-igual | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 91826937 | 91826937 | 20001 |  /  /  |
| L-fix/10x | ParAdjacente | True | 4 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 350840773 | 350840773 | 43498 | 1.00 / 1.00 / False |

## Abstrações por braço (proveniência, origem, reutilização)
- L-lib+f: `abs1` = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (Grade → Pos → L Pos; promocao-solucao; proveniência descoberta; origem ['vizPretos']; reutilizações diretas {'expandir': 1}; indiretas {'ParAdjacente': 1}; cópia de solução: True)
- L-lib+f: `abs2` = `λg1 l2. juntar (mapear@P>LP (abs1 g1) l2)` (Grade → L Pos → L Pos; promocao-solucao; proveniência descoberta; origem ['expandir']; reutilizações diretas {'ParAdjacente': 1}; indiretas {}; cópia de solução: True)
- L-lib+f/lesao: evento {"antes_de": "ParAdjacente", "lesao": [{"nome": "abs1", "proveniencia": "descoberta", "categoria": "descoberta-reutilizada", "tipo": "Grade → Pos → L Pos", "corpo": "(\\ (g1 Grade) (p2 Pos) (filtrar@P (celula g1) (vizinhos g1 p2)))", "legivel": "λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)", "tama
- L-lib+f/controle: `abs1` = `λg1. filtrar@P (celula g1) (cabeca@LP (colunas g1))` (Grade → L Pos; promocao-solucao; proveniência descoberta; origem ['pretasColuna1']; reutilizações diretas {}; indiretas {}; cópia de solução: True)
- L-lib+f/controle: `abs2` = `λg1 l2. diferenca l2 (cabeca@LP (linhas g1))` (Grade → L Pos → L Pos; promocao-solucao; proveniência descoberta; origem ['semLinha1']; reutilizações diretas {}; indiretas {}; cópia de solução: True)
- L-fix/custo-igual: evento {"antes_de": "ParAdjacente", "B": 20000}
- L-fix/10x: evento {"antes_de": "ParAdjacente", "B": 200000}

## Sondas de custo igual
```
{
 "plano": {
  "cumulativo_enumeracao_antes_T3": {
   "L-fix": 21282,
   "L-lib+f": 3729
  },
  "delta": -17553,
  "B_T3": {
   "L-fix/custo-igual": 20000,
   "L-fix/10x": 200000
  },
  "nota": "delta <= 0 significa que L-fix já gastou mais que L-lib+f antes de T3; a sonda roda com B"
 }
}
```
## Auditoria OE dos alvos (tabela base)
```
{
 "base:vizPretos": {
  "tarefa": "vizPretos",
  "presente": true,
  "custo_do_alvo": 8,
  "termo": "λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)",
  "ate_custo": 8,
  "candidatos": 1281,
  "entradas_independentes": 192
 },
 "base:expandir": {
  "tarefa": "expandir",
  "presente": false,
  "custo_do_alvo": null,
  "termo": null,
  "ate_custo": 8,
  "candidatos": 6951,
  "entradas_independentes": 192
 },
 "base:ParAdjacente": {
  "tarefa": "ParAdjacente",
  "presente": false,
  "custo_do_alvo": null,
  "termo": null,
  "ate_custo": 8,
  "candidatos": 4097,
  "entradas_independentes": 48
 }
}
```
## Análise (critério central)
```
{
 "abstracao_descoberta_e_reutilizada_em_tarefa_inedita": true,
 "braco": "L-lib+f",
 "tarefas": {
  "expandir": [
   "abs1"
  ],
  "ParAdjacente": [
   "abs2"
  ]
 },
 "L-fix_resolveu_a_mesma_tarefa_no_orcamento_B": {
  "expandir": false,
  "ParAdjacente": false
 },
 "detalhe": "verificar também L-fix/custo-igual e L-fix/10x abaixo"
}
```
## Medições (tempo e memória; separadas dos contadores)
- L-fix: parede 216.5 s; CPU 171.4 s; memória de pico 530736 KiB (trecho)
- L-lib: parede 219.4 s; CPU 174.3 s; memória de pico 530876 KiB (trecho)
- L-lib+f: parede 80.4 s; CPU 59.1 s; memória de pico 540664 KiB (trecho)
- L-lib+f/lesao: parede 165.6 s; CPU 122.1 s; memória de pico 518124 KiB (trecho)
- L-lib+f/controle: parede 116.0 s; CPU 90.4 s; memória de pico 535348 KiB (trecho)
- L-fix/custo-igual: parede 45.5 s; CPU 45.0 s; memória de pico 305024 KiB (trecho)
- L-fix/10x: parede 152.2 s; CPU 150.6 s; memória de pico 516824 KiB (trecho)
