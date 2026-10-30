# Experimento mínimo — registros (exploratoria-minima, semente 10006, B = 20000, política unigrama)

| braço | tarefa | aceita | rodadas | motivo | tamanho | hipótese | biblioteca usada | custo tarefa | cumulativo | enum. cumul. | teste (acc / bal / degen.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308325 | 6308325 | 1281 | 1.00 / 1.00 / False |
| L-fix | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 177656733 | 183965058 | 8660 | 1.00 / 1.00 / False |
| L-fix | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84404321 | 268369379 | 13429 | 1.00 / 1.00 / False |
| L-fix | NenhumaIsolada | False | 3 | orcamento_enumeracao |  | `` |  | 443302414 | 711671793 | 33430 |  /  /  |
| L-lib | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308418 | 6308418 | 1281 | 1.00 / 1.00 / False |
| L-lib | expandir | True | 1 | aceita | 10 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` |  | 177657261 | 183965679 | 8660 | 1.00 / 1.00 / False |
| L-lib | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84864543 | 268830222 | 13707 | 1.00 / 1.00 / False |
| L-lib | NenhumaIsolada | False | 3 | orcamento_enumeracao |  | `` |  | 361501140 | 630331362 | 33708 |  /  /  |
| L-lib+f | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308433 | 6308433 | 1281 | 1.00 / 1.00 / False |
| L-lib+f | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8521191 | 14829624 | 2336 | 1.00 / 1.00 / False |
| L-lib+f | ParAdjacente | True | 1 | aceita | 8 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | abs2 | 12820731 | 27650355 | 4103 | 1.00 / 1.00 / False |
| L-lib+f | NenhumaIsolada | False | 3 | orcamento_enumeracao |  | `` |  | 388380108 | 416030463 | 24104 |  /  /  |
| L-lib+f/lesao | vizPretos | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` |  | 6308433 | 6308433 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/lesao | expandir | True | 1 | aceita | 7 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | abs1 | 8521191 | 14829624 | 2336 | 1.00 / 1.00 / False |
| L-lib+f/lesao | ParAdjacente | True | 1 | aceita | 10 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` |  | 84404463 | 99234087 | 7105 | 1.00 / 1.00 / False |
| L-lib+f/lesao | NenhumaIsolada | False | 3 | orcamento_enumeracao |  | `` |  | 443302414 | 542536501 | 27106 |  /  /  |
| L-lib+f/controle | pretasColuna1 | True | 1 | aceita | 8 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` |  | 6001347 | 6001347 | 1281 | 1.00 / 1.00 / False |
| L-lib+f/controle | semLinha1 | True | 1 | aceita | 7 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` |  | 11490055 | 17491402 | 2972 | 1.00 / 1.00 / False |
| L-lib+f/controle | ParAdjacente | False | 2 | orcamento_enumeracao |  | `` |  | 258204027 | 275695429 | 22973 |  /  /  |
| L-lib+f/controle | NenhumaIsolada | False | 2 | orcamento_enumeracao |  | `` |  | 269462957 | 545158386 | 42974 |  /  /  |

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
  "soma_livro": 416030463,
  "cumulativo_curva": 416030463,
  "fecha": true
 },
 "controles": {
  "L-lib+f/lesao:ParAdjacente": {
   "aceita": true,
   "custo": 84404463,
   "pior_que_L-lib+f": true
  },
  "L-lib+f/controle:ParAdjacente": {
   "aceita": false,
   "custo": 258204027,
   "pior_que_L-lib+f": true
  }
 },
 "custo_cumulativo_igual": [
  {
   "tarefa": "vizPretos",
   "custo_cumulativo": 6308433,
   "aceitas_L-lib+f": 1,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "expandir",
   "custo_cumulativo": 14829624,
   "aceitas_L-lib+f": 2,
   "aceitas_L-fix_ao_mesmo_custo": 1
  },
  {
   "tarefa": "ParAdjacente",
   "custo_cumulativo": 27650355,
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
- L-fix: parede 552.2 s; CPU 377.4 s; memória de pico 603004 KiB (trecho)
- L-lib: parede 506.4 s; CPU 335.5 s; memória de pico 734352 KiB (trecho)
- L-lib+f: parede 309.4 s; CPU 201.7 s; memória de pico 691684 KiB (trecho)
- L-lib+f/lesao: parede 420.7 s; CPU 278.3 s; memória de pico 602504 KiB (trecho)
- L-lib+f/controle: parede 388.2 s; CPU 319.3 s; memória de pico 527948 KiB (trecho)
