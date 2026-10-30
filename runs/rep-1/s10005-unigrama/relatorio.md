# Experimento mínimo — registros (exploratoria-minima, semente 10005, B = 20000, política unigrama)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308491 | 6308491 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 182222058 | 188530549 | 8664 | 1.00 / 1.00 / False |
| L-fix | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84363807 | 272894356 | 13437 | 1.00 / 1.00 / False |
| L-fix | NenhumaIsolada | False | 4 | orcamento_enumeracao |  | `` |  | 420668444 | 693562800 | 33438 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308584 | 6308584 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 182222586 | 188531170 | 8664 | 1.00 / 1.00 / False |
| L-lib | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84797817 | 273328987 | 13714 | 1.00 / 1.00 / False |
| L-lib | NenhumaIsolada | False | 4 | orcamento_enumeracao |  | `` |  | 354625772 | 627954759 | 33715 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308599 | 6308599 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8726704 | 15035303 | 2336 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 8 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | abs2 | 12431094 | 27466397 | 4099 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 4 | orcamento_enumeracao |  | `` |  | 375822252 | 403288649 | 24100 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308599 | 6308599 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8726704 | 15035303 | 2336 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84363949 | 99399252 | 7109 | 1.00 / 1.00 / False |
| L-lib+f/lesao | NenhumaIsolada | False | 4 | orcamento_enumeracao |  | `` |  | 420668444 | 520067696 | 27110 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6001544 | 6001544 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 10236649 | 16238193 | 2966 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 0 | orcamento_enumeracao |  | `` |  | 323427540 | 339665733 | 22967 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 323493089 | 663158822 | 42968 |  /  /  |

## Abstrações por braço (proveniência, origem, reutilização)
- L-lib: `abs1` = `λg1. filtrar@P (celula g1)` (Grade → L Pos → L Pos; fechamento; proveniência descoberta; origem ['vizPretos', 'expandir']; reutilizações diretas {}; indiretas {}; cópia de solução: False)
- L-lib: `abs2` = `λg1 l2. juntar (mapear@P>LP (vizinhos g1) l2)` (Grade → L Pos → L Pos; fechamento; proveniência descoberta; origem ['expandir', 'ParAdjacente']; reutilizações diretas {}; indiretas {}; cópia de solução: False)
- L-lib+f: `abs1` = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (Grade → Pos → L Pos; promocao-solucao; proveniência descoberta; origem ['vizPretos']; reutilizações diretas {'expandir': 1}; indiretas {'ParAdjacente': 1}; cópia de solução: True)
- L-lib+f: `abs2` = `λg1 l2. juntar (mapear@P>LP (abs1 g1) l2)` (Grade → L Pos → L Pos; promocao-solucao; proveniência descoberta; origem ['expandir']; reutilizações diretas {'ParAdjacente': 1}; indiretas {}; cópia de solução: True)
- L-lib+f/lesao: evento {"antes_de": "ParAdjacente", "lesao": [{"nome": "abs1", "proveniencia": "descoberta", "categoria": "descoberta-reutilizada", "tipo": "Grade → Pos → L Pos", "corpo": "(\\ (g1 Grade) (p2 Pos) (filtrar@P (celula g1) (vizinhos g1 p2)))", "legivel": "λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)", "tama
- L-lib+f/controle: `abs1` = `λg1. filtrar@P (celula g1) (cabeca@LP (colunas g1))` (Grade → L Pos; promocao-solucao; proveniência descoberta; origem ['pretasColuna1']; reutilizações diretas {}; indiretas {}; cópia de solução: True)
- L-lib+f/controle: `abs2` = `λg1 l2. diferenca l2 (cabeca@LP (linhas g1))` (Grade → L Pos → L Pos; promocao-solucao; proveniência descoberta; origem ['semLinha1']; reutilizações diretas {}; indiretas {}; cópia de solução: True)

## Sondas de orçamento (não são custo igual; não preservam o histórico)
```
{}
```
## Auditoria OE dos alvos (tabela base)
```
{}
```
## Análise (critério central)
```
{
 "veredito": true,
 "braco": "L-lib+f",
 "condicoes": {
  "1_reuso_em_tarefa_inedita": true,
  "2_procedencia": true,
  "3_custo_total_verificavel": true,
  "4_controles_piores": true,
  "5_mais_tarefas_que_L-fix_a_custo_cumulativo_igual": true
 },
 "tarefas_de_reuso": {
  "expandir": [
   "abs1"
  ],
  "ParAdjacente": [
   "abs2"
  ]
 },
 "fechamento": {
  "soma_livro": 403288649,
  "cumulativo_curva": 403288649,
  "fecha": true
 },
 "controles": {
  "L-lib+f/lesao:ParAdjacente": {
   "aceita": true,
   "custo": 84363949,
   "pior_que_L-lib+f": true
  },
  "L-lib+f/controle:ParAdjacente": {
   "aceita": false,
   "custo": 323427540,
   "pior_que_L-lib+f": true
  }
 },
 "custo_cumulativo_igual": [
  {
   "tarefa": "vizPretos",
   "custo_cumulativo": 6308599,
   "aceitas_L-lib+f": 1,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "expandir",
   "custo_cumulativo": 15035303,
   "aceitas_L-lib+f": 2,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "ParAdjacente",
   "custo_cumulativo": 27466397,
   "aceitas_L-lib+f": 3,
   "aceitas_L-fix_ao_mesmo_custo": 1
  }
 ],
 "L-fix_resolveu_a_mesma_tarefa_no_orcamento_B": {
  "expandir": true,
  "ParAdjacente": true
 },
 "nota": "as sondas L-fix/orcamento-extra e L-fix/sonda-10x não entram no veredito: não preservam o histórico"
}
```
## Medições (tempo e memória; separadas dos contadores)
- L-fix: parede 615.5 s; CPU 368.5 s; memória de pico 442864 KiB (trecho)
- L-lib: parede 566.7 s; CPU 332.9 s; memória de pico 562256 KiB (trecho)
- L-lib+f: parede 265.1 s; CPU 206.6 s; memória de pico 527932 KiB (trecho)
- L-lib+f/lesao: parede 449.5 s; CPU 277.8 s; memória de pico 441680 KiB (trecho)
- L-lib+f/controle: parede 524.6 s; CPU 335.3 s; memória de pico 501224 KiB (trecho)
