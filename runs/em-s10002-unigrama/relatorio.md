# Experimento mínimo — registros (exploratoria-minima, semente 10002, B = 20000, política unigrama)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307717 | 6307717 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 173271908 | 179579625 | 8661 | 1.00 / 1.00 / False |
| L-fix | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84396376 | 263976001 | 13431 | 1.00 / 1.00 / False |
| L-fix | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 444507202 | 708483203 | 33432 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307810 | 6307810 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 173272436 | 179580246 | 8661 | 1.00 / 1.00 / False |
| L-lib | ParAdjacente | True | 2 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84847099 | 264427345 | 13712 | 1.00 / 1.00 / False |
| L-lib | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 369079419 | 633506764 | 33713 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307825 | 6307825 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8328388 | 14636213 | 2336 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 8 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | abs2 | 13690434 | 28326647 | 4109 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 410737060 | 439063707 | 24110 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6307825 | 6307825 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8328388 | 14636213 | 2336 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84396518 | 99032731 | 7106 | 1.00 / 1.00 / False |
| L-lib+f/lesao | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 444507202 | 543539933 | 27107 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6154228 | 6154228 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 11467804 | 17622032 | 2970 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 259557946 | 277179978 | 22971 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 0 | orcamento_enumeracao |  | `` |  | 278596119 | 555776097 | 42972 |  /  /  |
| L-fix/custo-igual | ParAdjacente | False | 3 | orcamento_enumeracao |  | `` |  | 91826937 | 91826937 | 20001 |  /  /  |
| L-fix/10x | ParAdjacente | True | 4 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 350840773 | 350840773 | 43498 | 1.00 / 1.00 / False |

## Abstrações por braço (proveniência, origem, reutilização)
- L-lib: `abs1` = `λg1. filtrar@P (celula g1)` (Grade → L Pos → L Pos; fechamento; proveniência descoberta; origem ['vizPretos', 'expandir']; reutilizações diretas {}; indiretas {}; cópia de solução: False)
- L-lib: `abs2` = `λg1 l2. juntar (mapear@P>LP (vizinhos g1) l2)` (Grade → L Pos → L Pos; fechamento; proveniência descoberta; origem ['expandir', 'ParAdjacente']; reutilizações diretas {}; indiretas {}; cópia de solução: False)
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
   "L-fix": 8661,
   "L-lib+f": 2336
  },
  "delta": -6325,
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
  "expandir": true,
  "ParAdjacente": true
 },
 "detalhe": "verificar também L-fix/custo-igual e L-fix/10x abaixo"
}
```
## Medições (tempo e memória; separadas dos contadores)
- L-fix: parede 362.3 s; CPU 338.1 s; memória de pico 589524 KiB (trecho)
- L-lib: parede 332.2 s; CPU 303.9 s; memória de pico 724912 KiB (trecho)
- L-lib+f: parede 224.1 s; CPU 200.8 s; memória de pico 690008 KiB (trecho)
- L-lib+f/lesao: parede 286.2 s; CPU 257.3 s; memória de pico 589036 KiB (trecho)
- L-lib+f/controle: parede 284.3 s; CPU 280.3 s; memória de pico 518396 KiB (trecho)
- L-fix/custo-igual: parede 47.7 s; CPU 47.1 s; memória de pico 304936 KiB (trecho)
- L-fix/10x: parede 156.5 s; CPU 154.6 s; memória de pico 516728 KiB (trecho)
