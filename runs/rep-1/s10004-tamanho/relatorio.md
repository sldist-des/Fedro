# Experimento mínimo — registros (exploratoria-minima, semente 10004, B = 20000, política tamanho)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001226 | 6001226 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | False | 0 | orcamento_enumeracao |  | `` |  | 114902235 | 120903461 | 21282 |  /  /  |
| L-fix | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 139320713 | 260224174 | 41283 |  /  /  |
| L-fix | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 139318746 | 399542920 | 61284 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001319 | 6001319 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | False | 0 | orcamento_enumeracao |  | `` |  | 114902235 | 120903554 | 21282 |  /  /  |
| L-lib | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 139320713 | 260224267 | 41283 |  /  /  |
| L-lib | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 139318746 | 399543013 | 61284 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001334 | 6001334 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 4752834 | 10754168 | 3729 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 7 | `λx0. nao (vazia?@P (abs2 x0 (pretas x0)))` | abs2 | 3554080 | 14308248 | 5465 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 96263063 | 110571311 | 25466 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001334 | 6001334 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 4752834 | 10754168 | 3729 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 139320713 | 150074881 | 23730 |  /  /  |
| L-lib+f/lesao | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 139318746 | 289393627 | 43731 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6308348 | 6308348 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 4906214 | 11214562 | 4091 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 90074260 | 101288822 | 24092 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 90073600 | 191362422 | 44093 |  /  /  |

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
  "soma_livro": 110571311,
  "cumulativo_curva": 110571311,
  "fecha": true
 },
 "controles": {
  "L-lib+f/lesao:ParAdjacente": {
   "aceita": false,
   "custo": 139320713,
   "pior_que_L-lib+f": true
  },
  "L-lib+f/controle:ParAdjacente": {
   "aceita": false,
   "custo": 90074260,
   "pior_que_L-lib+f": true
  }
 },
 "custo_cumulativo_igual": [
  {
   "tarefa": "vizPretos",
   "custo_cumulativo": 6001334,
   "aceitas_L-lib+f": 1,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "expandir",
   "custo_cumulativo": 10754168,
   "aceitas_L-lib+f": 2,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "ParAdjacente",
   "custo_cumulativo": 14308248,
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
- L-fix: parede 316.1 s; CPU 194.5 s; memória de pico 534660 KiB (trecho)
- L-lib: parede 320.2 s; CPU 192.7 s; memória de pico 534824 KiB (trecho)
- L-lib+f: parede 76.3 s; CPU 56.1 s; memória de pico 544340 KiB (trecho)
- L-lib+f/lesao: parede 232.7 s; CPU 137.5 s; memória de pico 518264 KiB (trecho)
- L-lib+f/controle: parede 177.5 s; CPU 94.8 s; memória de pico 539964 KiB (trecho)
