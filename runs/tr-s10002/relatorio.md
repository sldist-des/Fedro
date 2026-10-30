# Transferência estrutural — famílias congeladas (hash 3b6646466e454592…), semente 10002, B = 20000

## Política tamanho
Custo da cadeia T1–T3: L-lib+f 14,620,489; L-fix 207,790,419. Abstrações de L-lib+f: [('abs1', 'λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)'), ('abs2', 'λg1 l2. juntar (mapear@P>LP (abs1 g1) l2)')]

| tarefa | família | L-lib+f aceita | custo | tamanho | reuso | L-fix aceita | custo | tamanho | razão custo | transferência |
|---|---|---|---|---|---|---|---|---|---|---|
| expandir2 | F-comp | True | 7,651,476 | 7 | ['abs2'] | False | 115,058,716 | None | 0.07 | positiva (só L-lib+f aceita) |
| fronteira | F-comp | True | 7,508,343 | 7 | ['abs2'] | False | 112,372,147 | None | 0.07 | positiva (só L-lib+f aceita) |
| isoladaP | F-comp | True | 143,960,780 | 10 | ['abs1'] | False | 161,484,096 | None | 0.89 | positiva (só L-lib+f aceita) |
| duasVizinhas | F-comp | True | 9,696,119 | 8 | ['abs1'] | False | 165,444,042 | None | 0.06 | positiva (só L-lib+f aceita) |
| pretasComVizinha | F-comp | True | 85,116 | 5 | ['abs2'] | False | 78,397,718 | None | 0.00 | positiva (só L-lib+f aceita) |
| TopoCheio | F-neg | True | 3,768,432 | 7 | [] | True | 2,131,330 | 7 | 1.77 | negativa |
| LinhaOcupada | F-neg | True | 3,766,313 | 7 | [] | True | 2,130,868 | 7 | 1.77 | negativa |
| pretasUltimaColuna | F-neg | True | 13,807,042 | 8 | [] | True | 9,736,727 | 8 | 1.42 | negativa |
| semColuna1 | F-neg | True | 7,658,966 | 7 | [] | True | 4,545,092 | 7 | 1.69 | negativa |

- F-comp: {"tarefas": 5, "aceitas_L-lib+f": 5, "aceitas_L-fix": 0, "com_reuso": 5, "positivas": 5, "negativas": 0, "custo_L-lib+f": 168901834, "custo_L-fix": 632756719}
- F-neg: {"tarefas": 4, "aceitas_L-lib+f": 4, "aceitas_L-fix": 4, "com_reuso": 0, "positivas": 0, "negativas": 4, "custo_L-lib+f": 29000753, "custo_L-fix": 18544017}

## Política unigrama
Custo da cadeia T1–T3: L-lib+f 28,326,647; L-fix 263,976,001. Abstrações de L-lib+f: [('abs1', 'λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)'), ('abs2', 'λg1 l2. juntar (mapear@P>LP (abs1 g1) l2)')]

| tarefa | família | L-lib+f aceita | custo | tamanho | reuso | L-fix aceita | custo | tamanho | razão custo | transferência |
|---|---|---|---|---|---|---|---|---|---|---|
| expandir2 | F-comp | True | 3,679,835 | 7 | ['abs2'] | False | 320,094,336 | None | 0.01 | positiva (só L-lib+f aceita) |
| fronteira | F-comp | True | 6,361,185 | 7 | ['abs2'] | False | 311,232,082 | None | 0.02 | positiva (só L-lib+f aceita) |
| isoladaP | F-comp | True | 53,149,130 | 10 | ['abs1'] | True | 620,788,343 | 13 | 0.09 | positiva |
| duasVizinhas | F-comp | True | 13,017,905 | 9 | ['abs1'] | True | 104,760,691 | 12 | 0.12 | positiva |
| pretasComVizinha | F-comp | True | 38,051 | 5 | ['abs2'] | True | 17,354,972 | 10 | 0.00 | positiva |
| TopoCheio | F-neg | True | 17,460,400 | 7 | [] | True | 13,091,327 | 7 | 1.33 | negativa |
| LinhaOcupada | F-neg | True | 8,504,843 | 7 | [] | True | 5,656,178 | 7 | 1.50 | negativa |
| pretasUltimaColuna | F-neg | True | 95,390,682 | 8 | [] | True | 63,954,577 | 8 | 1.49 | negativa |
| semColuna1 | F-neg | True | 46,797,701 | 7 | [] | True | 33,318,526 | 7 | 1.40 | negativa |

- F-comp: {"tarefas": 5, "aceitas_L-lib+f": 5, "aceitas_L-fix": 3, "com_reuso": 5, "positivas": 5, "negativas": 0, "custo_L-lib+f": 76246106, "custo_L-fix": 1374230424}
- F-neg: {"tarefas": 4, "aceitas_L-lib+f": 4, "aceitas_L-fix": 4, "com_reuso": 0, "positivas": 0, "negativas": 4, "custo_L-lib+f": 168153626, "custo_L-fix": 116020608}

### Hipóteses — tamanho/L-lib+f
- expandir2: aceita=True (aceita), `λx0 x1. abs2 x0 (abs2 x0 x1)`, custo 7,651,476, reuso ['abs2']
- fronteira: aceita=True (aceita), `λx0 x1. diferenca (abs2 x0 x1) x1`, custo 7,508,343, reuso ['abs2']
- isoladaP: aceita=True (aceita), `λx0 x1. e (celula x0 x1) (vazia?@P (abs1 x0 x1))`, custo 143,960,780, reuso ['abs1']
- duasVizinhas: aceita=True (aceita), `λx0 x1. nao (vazia?@P (cauda@P (abs1 x0 x1)))`, custo 9,696,119, reuso ['abs1']
- pretasComVizinha: aceita=True (aceita), `λx0. abs2 x0 (pretas x0)`, custo 85,116, reuso ['abs2']
- TopoCheio: aceita=True (aceita), `λx0. todos@P (celula x0) (cabeca@LP (linhas x0))`, custo 3,768,432, reuso []
- LinhaOcupada: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 3,766,313, reuso []
- pretasUltimaColuna: aceita=True (aceita), `λx0. filtrar@P (celula x0) (cabeca@LP (reverter@LP (colunas x0)))`, custo 13,807,042, reuso []
- semColuna1: aceita=True (aceita), `λx0 x1. diferenca x1 (cabeca@LP (colunas x0))`, custo 7,658,966, reuso []

### Hipóteses — tamanho/L-fix
- expandir2: aceita=False (orcamento_enumeracao), ``, custo 115,058,716, reuso []
- fronteira: aceita=False (orcamento_enumeracao), ``, custo 112,372,147, reuso []
- isoladaP: aceita=False (orcamento_enumeracao), ``, custo 161,484,096, reuso []
- duasVizinhas: aceita=False (orcamento_enumeracao), ``, custo 165,444,042, reuso []
- pretasComVizinha: aceita=False (orcamento_enumeracao), ``, custo 78,397,718, reuso []
- TopoCheio: aceita=True (aceita), `λx0. todos@P (celula x0) (cabeca@LP (linhas x0))`, custo 2,131,330, reuso []
- LinhaOcupada: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 2,130,868, reuso []
- pretasUltimaColuna: aceita=True (aceita), `λx0. filtrar@P (celula x0) (cabeca@LP (reverter@LP (colunas x0)))`, custo 9,736,727, reuso []
- semColuna1: aceita=True (aceita), `λx0 x1. diferenca x1 (cabeca@LP (colunas x0))`, custo 4,545,092, reuso []

### Hipóteses — unigrama/L-lib+f
- expandir2: aceita=True (aceita), `λx0 x1. abs2 x0 (abs2 x0 x1)`, custo 3,679,835, reuso ['abs2']
- fronteira: aceita=True (aceita), `λx0 x1. diferenca (abs2 x0 x1) x1`, custo 6,361,185, reuso ['abs2']
- isoladaP: aceita=True (aceita), `λx0 x1. e (celula x0 x1) (vazia?@P (abs1 x0 x1))`, custo 53,149,130, reuso ['abs1']
- duasVizinhas: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (cauda@P (abs1 x0 x1))`, custo 13,017,905, reuso ['abs1']
- pretasComVizinha: aceita=True (aceita), `λx0. abs2 x0 (pretas x0)`, custo 38,051, reuso ['abs2']
- TopoCheio: aceita=True (aceita), `λx0. todos@P (celula x0) (cabeca@LP (linhas x0))`, custo 17,460,400, reuso []
- LinhaOcupada: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 8,504,843, reuso []
- pretasUltimaColuna: aceita=True (aceita), `λx0. filtrar@P (celula x0) (cabeca@LP (reverter@LP (colunas x0)))`, custo 95,390,682, reuso []
- semColuna1: aceita=True (aceita), `λx0 x1. diferenca x1 (cabeca@LP (colunas x0))`, custo 46,797,701, reuso []

### Hipóteses — unigrama/L-fix
- expandir2: aceita=False (orcamento_enumeracao), ``, custo 320,094,336, reuso []
- fronteira: aceita=False (orcamento_enumeracao), ``, custo 311,232,082, reuso []
- isoladaP: aceita=True (aceita), `λx0 x1. pertence x1 (diferenca (pretas x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0))))`, custo 620,788,343, reuso []
- duasVizinhas: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (cauda@P (filtrar@P (celula x0) (vizinhos x0 x1)))`, custo 104,760,691, reuso []
- pretasComVizinha: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))`, custo 17,354,972, reuso []
- TopoCheio: aceita=True (aceita), `λx0. todos@P (celula x0) (cabeca@LP (linhas x0))`, custo 13,091,327, reuso []
- LinhaOcupada: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 5,656,178, reuso []
- pretasUltimaColuna: aceita=True (aceita), `λx0. filtrar@P (celula x0) (cabeca@LP (reverter@LP (colunas x0)))`, custo 63,954,577, reuso []
- semColuna1: aceita=True (aceita), `λx0 x1. diferenca x1 (cabeca@LP (colunas x0))`, custo 33,318,526, reuso []

## Medições
- tamanho/L-lib+f: parede 147 s, CPU 97 s, memória 352548 KiB (trecho)
- tamanho/L-fix: parede 526 s, CPU 427 s, memória 597652 KiB (trecho)
- unigrama/L-lib+f: parede 178 s, CPU 135 s, memória 367388 KiB (trecho)
- unigrama/L-fix: parede 874 s, CPU 857 s, memória 653164 KiB (trecho)
