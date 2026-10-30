# Experimento mínimo — registros (exploratoria-minima, semente 10004, B = 20000, política unigrama)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001226 | 6001226 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 181785099 | 187786325 | 8661 | 1.00 / 1.00 / False |
| L-fix | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84442628 | 272228953 | 13427 | 1.00 / 1.00 / False |
| L-fix | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 441307341 | 713536294 | 33428 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001319 | 6001319 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 181785627 | 187786946 | 8661 | 1.00 / 1.00 / False |
| L-lib | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84919983 | 272706929 | 13701 | 1.00 / 1.00 / False |
| L-lib | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 361698438 | 634405367 | 33702 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001334 | 6001334 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8720887 | 14722221 | 2336 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 8 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | abs2 | 12841055 | 27563276 | 4101 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 390195498 | 417758774 | 24102 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6001334 | 6001334 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8720887 | 14722221 | 2336 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84442770 | 99164991 | 7102 | 1.00 / 1.00 / False |
| L-lib+f/lesao | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 441307341 | 540472332 | 27103 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6308348 | 6308348 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 10538712 | 16847060 | 2966 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 1 | orcamento_enumeracao |  | `` |  | 320860827 | 337707887 | 22967 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 1 | orcamento_enumeracao |  | `` |  | 320787085 | 658494972 | 42968 |  /  /  |

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
  "soma_livro": 417758774,
  "cumulativo_curva": 417758774,
  "fecha": true
 },
 "controles": {
  "L-lib+f/lesao:ParAdjacente": {
   "aceita": true,
   "custo": 84442770,
   "pior_que_L-lib+f": true
  },
  "L-lib+f/controle:ParAdjacente": {
   "aceita": false,
   "custo": 320860827,
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
   "custo_cumulativo": 14722221,
   "aceitas_L-lib+f": 2,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "ParAdjacente",
   "custo_cumulativo": 27563276,
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
- L-fix: parede 652.4 s; CPU 358.7 s; memória de pico 590360 KiB (trecho)
- L-lib: parede 611.8 s; CPU 317.9 s; memória de pico 719588 KiB (trecho)
- L-lib+f: parede 469.7 s; CPU 204.3 s; memória de pico 680456 KiB (trecho)
- L-lib+f/lesao: parede 561.3 s; CPU 271.0 s; memória de pico 589904 KiB (trecho)
- L-lib+f/controle: parede 354.7 s; CPU 327.2 s; memória de pico 517252 KiB (trecho)
