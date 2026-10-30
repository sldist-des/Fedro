# Experimento mínimo — registros (exploratoria-minima, semente 10005, B = 20000, política tamanho)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308491 | 6308491 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | False | 0 | orcamento_enumeracao |  | `` |  | 115514505 | 121822996 | 21282 |  /  /  |
| L-fix | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 139519024 | 261342020 | 41283 |  /  /  |
| L-fix | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 92665041 | 354007061 | 61284 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308584 | 6308584 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | False | 0 | orcamento_enumeracao |  | `` |  | 115514505 | 121823089 | 21282 |  /  /  |
| L-lib | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 139519024 | 261342113 | 41283 |  /  /  |
| L-lib | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 92665041 | 354007154 | 61284 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308599 | 6308599 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 4726747 | 11035346 | 3729 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 7 | `λx0. nao (vazia?@P (abs2 x0 (pretas x0)))` | abs2 | 3544078 | 14579424 | 5464 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 4 | orcamento_enumeracao |  | `` |  | 86510359 | 101089783 | 25465 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308599 | 6308599 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 4726747 | 11035346 | 3729 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 139519024 | 150554370 | 23730 |  /  /  |
| L-lib+f/lesao | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 92665041 | 243219411 | 43731 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6001544 | 6001544 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 4770343 | 10771887 | 4091 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 91195428 | 101967315 | 24092 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 77176891 | 179144206 | 44093 |  /  /  |

## Abstrações por braço (proveniência, origem, reutilização)
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
  "soma_livro": 101089783,
  "cumulativo_curva": 101089783,
  "fecha": true
 },
 "controles": {
  "L-lib+f/lesao:ParAdjacente": {
   "aceita": false,
   "custo": 139519024,
   "pior_que_L-lib+f": true
  },
  "L-lib+f/controle:ParAdjacente": {
   "aceita": false,
   "custo": 91195428,
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
   "custo_cumulativo": 11035346,
   "aceitas_L-lib+f": 2,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "ParAdjacente",
   "custo_cumulativo": 14579424,
   "aceitas_L-lib+f": 3,
   "aceitas_L-fix_ao_mesmo_custo": 1
  }
 ],
 "L-fix_resolveu_a_mesma_tarefa_no_orcamento_B": {
  "expandir": false,
  "ParAdjacente": false
 },
 "nota": "as sondas L-fix/orcamento-extra e L-fix/sonda-10x não entram no veredito: não preservam o histórico"
}
```
## Medições (tempo e memória; separadas dos contadores)
- L-fix: parede 230.0 s; CPU 185.1 s; memória de pico 449428 KiB (trecho)
- L-lib: parede 229.3 s; CPU 185.1 s; memória de pico 449592 KiB (trecho)
- L-lib+f: parede 75.1 s; CPU 55.5 s; memória de pico 420012 KiB (trecho)
- L-lib+f/lesao: parede 172.8 s; CPU 125.0 s; memória de pico 408248 KiB (trecho)
- L-lib+f/controle: parede 119.8 s; CPU 93.1 s; memória de pico 431764 KiB (trecho)
