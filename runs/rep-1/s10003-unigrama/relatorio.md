# Experimento mínimo — registros (exploratoria-minima, semente 10003, B = 20000, política unigrama)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6321152 | 6321152 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 178813159 | 185134311 | 8661 | 1.00 / 1.00 / False |
| L-fix | ParAdjacente | True | 2 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 85843951 | 270978262 | 13431 | 1.00 / 1.00 / False |
| L-fix | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 418721889 | 689700151 | 33432 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6321245 | 6321245 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 178813687 | 185134932 | 8661 | 1.00 / 1.00 / False |
| L-lib | ParAdjacente | True | 2 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 85612515 | 270747447 | 13709 | 1.00 / 1.00 / False |
| L-lib | NenhumaIsolada | False | 3 | orcamento_enumeracao |  | `` |  | 358742485 | 629489932 | 33710 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6321260 | 6321260 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8877274 | 15198534 | 2336 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 2 | aceita | 8 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | abs2 | 13167993 | 28366527 | 4102 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 380427246 | 408793773 | 24103 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6321260 | 6321260 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8877274 | 15198534 | 2336 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | True | 2 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 85844093 | 101042627 | 7106 | 1.00 / 1.00 / False |
| L-lib+f/lesao | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 418721889 | 519764516 | 27107 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6321159 | 6321159 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 11150802 | 17471961 | 2966 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 2 | orcamento_enumeracao |  | `` |  | 324126172 | 341598133 | 22967 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 0 | orcamento_enumeracao |  | `` |  | 324343876 | 665942009 | 42968 |  /  /  |

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
  "soma_livro": 408793773,
  "cumulativo_curva": 408793773,
  "fecha": true
 },
 "controles": {
  "L-lib+f/lesao:ParAdjacente": {
   "aceita": true,
   "custo": 85844093,
   "pior_que_L-lib+f": true
  },
  "L-lib+f/controle:ParAdjacente": {
   "aceita": false,
   "custo": 324126172,
   "pior_que_L-lib+f": true
  }
 },
 "custo_cumulativo_igual": [
  {
   "tarefa": "vizPretos",
   "custo_cumulativo": 6321260,
   "aceitas_L-lib+f": 1,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "expandir",
   "custo_cumulativo": 15198534,
   "aceitas_L-lib+f": 2,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "ParAdjacente",
   "custo_cumulativo": 28366527,
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
- L-fix: parede 356.1 s; CPU 349.8 s; memória de pico 571764 KiB (trecho)
- L-lib: parede 329.3 s; CPU 322.7 s; memória de pico 581072 KiB (trecho)
- L-lib+f: parede 203.5 s; CPU 200.2 s; memória de pico 576300 KiB (trecho)
- L-lib+f/lesao: parede 271.4 s; CPU 265.4 s; memória de pico 571784 KiB (trecho)
- L-lib+f/controle: parede 344.6 s; CPU 338.2 s; memória de pico 514188 KiB (trecho)
