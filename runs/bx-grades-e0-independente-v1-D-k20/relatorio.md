# Benchmark externo «grades-e0-independente» v1 — hash 9e600a4155844bc4…, 28 tarefas, semente 10007, B = 20000

| braço | aceitas | ids aceitas | custo prévio | custo benchmark | custo cumulativo | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha |
|---|---|---|---|---|---|---|---|---|
| zero/tamanho/L-fix | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, algumaLinhaCheia, tocaPreta | 0 | 1,882,334,319 | 1,882,334,319 | 0 | 0 (0) | True |
| zero/tamanho/L-lib+f | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, tocaPreta, semPretasAdjacentes | 0 | 1,540,841,394 | 1,540,841,394 | 5 | 19 (6) | True |

## zero/tamanho/L-lib+f vs zero/tamanho/L-fix
positivas 4, negativas 13, neutras 0, inconclusivas 11, com reuso 5

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 63,269 | 5 | [] | True | 63,212 | 5 | 1.00 | — | negativa |
| contidoEm | True | 881,252 | 6 | [] | True | 881,159 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 7,217,868 | 8 | [] | True | 6,329,022 | 8 | 0.88 | — | negativa |
| todaLinhaTemPreta | True | 2,782,785 | 7 | [] | True | 2,121,591 | 7 | 0.76 | — | negativa |
| complementoDe | True | 42,283 | 4 | [] | True | 38,898 | 4 | 0.92 | — | negativa |
| pretasPorColunas | True | 2,166,130 | 7 | [] | True | 1,869,005 | 7 | 0.86 | — | negativa |
| intersecaoOrdenada | True | 1,871,096 | 6 | [] | True | 1,596,085 | 6 | 0.85 | — | negativa |
| contemTodasPretas | True | 54,391 | 4 | ['abs2'] | True | 3,628,169 | 7 | 66.71 | — | positiva |
| colunaVazia | False | 49,358,860 | None | [] | True | 24,002,367 | 8 | — | ≤ 0.49 | negativa (só L-fix aceita; razão exata indefinida) |
| naBorda | True | 43,317,207 | 9 | [] | True | 31,918,531 | 9 | 0.74 | — | negativa |
| linhaDaPosicao | True | 9,603,136 | 8 | [] | True | 6,327,740 | 8 | 0.66 | — | negativa |
| juntarSemRepetir | True | 15,001,688 | 7 | [] | True | 6,988,104 | 7 | 0.47 | — | negativa |
| brancasDaLista | True | 4,777,483 | 6 | ['abs4', 'abs7'] | True | 779,063 | 6 | 0.16 | — | negativa |
| diferencaSimetrica | False | 125,936,664 | None | [] | False | 89,614,920 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasOrdemInversa | False | 57,335,720 | None | [] | False | 81,699,085 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 69,796,564 | None | [] | True | 71,510,199 | 9 | — | ≤ 1.02 | negativa (só L-fix aceita; razão exata indefinida) |
| linhaTemPretaEm | True | 13,400,257 | 8 | ['abs10'] | False | 165,333,141 | None | — | ≥ 12.34 | positiva (só L-lib+f aceita; razão exata indefinida) |
| semPretaIsolada | False | 94,186,831 | None | [] | False | 138,836,817 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| colunasBrancas | False | 71,936,432 | None | [] | False | 80,059,991 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | False | 100,763,908 | None | [] | False | 199,395,688 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| tocaPreta | True | 56,867,405 | 8 | ['abs15'] | True | 88,733,656 | 9 | 1.56 | — | positiva |
| bordaPreta | False | 76,368,530 | None | [] | False | 81,696,513 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | False | 163,287,345 | None | [] | False | 111,259,349 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| semPretasAdjacentes | True | 3,326,127 | 6 | ['abs18'] | False | 138,781,608 | None | — | ≥ 41.72 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 186,726,674 | None | [] | False | 138,026,636 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 100,198,331 | None | [] | False | 138,778,100 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 97,042,146 | None | [] | False | 133,999,597 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 186,531,012 | None | [] | False | 138,066,073 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=63,269 → L-lib+f 1 vs L-fix 1; contidoEm: C=944,521 → L-lib+f 2 vs L-fix 2; vizinhosPretos: C=8,162,389 → L-lib+f 3 vs L-fix 3; todaLinhaTemPreta: C=10,945,174 → L-lib+f 4 vs L-fix 5; complementoDe: C=10,987,457 → L-lib+f 5 vs L-fix 5; pretasPorColunas: C=13,153,587 → L-lib+f 6 vs L-fix 7; intersecaoOrdenada: C=15,024,683 → L-lib+f 7 vs L-fix 7; contemTodasPretas: C=15,079,074 → L-lib+f 8 vs L-fix 7; naBorda: C=107,755,141 → L-lib+f 9 vs L-fix 13; linhaDaPosicao: C=117,358,277 → L-lib+f 10 vs L-fix 13; juntarSemRepetir: C=132,359,965 → L-lib+f 11 vs L-fix 13; brancasDaLista: C=137,137,448 → L-lib+f 12 vs L-fix 13; linhaTemPretaEm: C=403,606,653 → L-lib+f 13 vs L-fix 14; tocaPreta: C=727,361,229 → L-lib+f 14 vs L-fix 14; semPretasAdjacentes: C=970,343,231 → L-lib+f 15 vs L-fix 14

### Hipóteses — zero/tamanho/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,212, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,159, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 6,329,022, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 2,121,591, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 38,898, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 1,869,005, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,596,085, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 3,628,169, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 24,002,367, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 31,918,531, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 6,327,740, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 6,988,104, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 779,063, reuso []
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 89,614,920, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 81,699,085, reuso []
- algumaLinhaCheia: aceita=True (aceita), `λx0. nao (vazia?@LP (filtrar@LP (todos@P (celula x0)) (linhas x0)))`, custo 71,510,199, reuso []
- linhaTemPretaEm: aceita=False (orcamento_enumeracao), ``, custo 165,333,141, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 138,836,817, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 80,059,991, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 199,395,688, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 88,733,656, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 81,696,513, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 111,259,349, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 138,781,608, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 138,026,636, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 138,778,100, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 133,999,597, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 138,066,073, reuso []

### Hipóteses — zero/tamanho/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,269, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,252, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 7,217,868, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 2,782,785, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 42,283, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 2,166,130, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,871,096, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (pretas x0)`, custo 54,391, reuso ['abs2']
- colunaVazia: aceita=False (orcamento_enumeracao), ``, custo 49,358,860, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 43,317,207, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 9,603,136, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 15,001,688, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (pretas x0))`, custo 4,777,483, reuso ['abs4', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 125,936,664, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 57,335,720, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 69,796,564, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs10 x0 x1)`, custo 13,400,257, reuso ['abs10']
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 94,186,831, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 71,936,432, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 100,763,908, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. abs15 x0 (vizinhos x0 x1))`, custo 56,867,405, reuso ['abs15']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 76,368,530, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 163,287,345, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs18 x0 (pretas x0))`, custo 3,326,127, reuso ['abs18']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 186,726,674, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 100,198,331, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 97,042,146, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 186,531,012, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {}); abs4 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs8 = `λg1. abs2 (pretas g1)` (descoberta, reut. {}); abs9 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs10 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs11 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs12 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs13 = `λg1. abs7 (abs4 g1 (pretas g1))` (descoberta, reut. {}); abs14 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs15 = `λg1. algum@P (celula g1)` (descoberta, reut. {'bx:tocaPreta': 1}); abs16 = `λg1 p2. abs15 g1 (abs10 g1 p2)` (descoberta, reut. {}); abs17 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs18 = `λg1. algum@P (λp2. abs15 g1 (vizinhos g1 p2))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs19 = `λf1 g2. f1 g2` (descoberta, reut. {})

## Medições
parede total 863 s
- zero/tamanho/L-fix: parede 859 s, CPU 849 s, memória 544020 KiB
- zero/tamanho/L-lib+f: parede 548 s, CPU 542 s, memória 856964 KiB
