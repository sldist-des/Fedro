# Benchmark externo «grades-e0-independente» v1 — hash 9e600a4155844bc4…, 28 tarefas, semente 10007, B = 20000

| braço | aceitas | ids aceitas | custo prévio | custo benchmark | custo cumulativo | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha |
|---|---|---|---|---|---|---|---|---|
| zero/tamanho/L-fix | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, algumaLinhaCheia, tocaPreta | 0 | 1,882,334,319 | 1,882,334,319 | 0 | 0 (0) | True |
| zero/tamanho/L-lib | 16/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, semPretaIsolada, mesmoConjunto, tocaPreta | 0 | 1,674,819,698 | 1,674,819,698 | 2 | 3 (2) | True |
| zero/tamanho/L-lib+f | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, tocaPreta, semPretasAdjacentes | 0 | 1,540,841,394 | 1,540,841,394 | 5 | 19 (6) | True |
| zero/tamanho/L-lib+f/lesao | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, algumaLinhaCheia, tocaPreta, semPretasAdjacentes | 0 | 1,859,823,021 | 1,859,823,021 | 3 | 1 (1) | True |
| zero/unigrama/L-fix | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, linhaTemPretaEm, mesmoConjunto, tocaPreta | 0 | 1,865,504,642 | 1,865,504,642 | 0 | 0 (0) | True |
| zero/unigrama/L-lib | 18/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, semPretaIsolada, mesmoConjunto, tocaPreta, semPretasAdjacentes | 0 | 1,529,471,393 | 1,529,471,393 | 3 | 7 (3) | True |
| zero/unigrama/L-lib+f | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, mesmoConjunto, tocaPreta, semPretasAdjacentes | 0 | 2,514,533,917 | 2,514,533,917 | 6 | 21 (7) | True |
| zero/unigrama/L-lib+f/lesao | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, mesmoConjunto, tocaPreta, semPretasAdjacentes | 0 | 2,609,254,305 | 2,609,254,305 | 3 | 3 (1) | True |

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

## zero/tamanho/L-lib+f vs zero/tamanho/L-lib+f/lesao
{"tarefas_apos_lesao": 14, "aceitas_L-lib+f": 3, "aceitas_lesao": 3, "custo_L-lib+f": 1277767282, "custo_lesao": 1596748909, "entradas_removidas": 13, "sensivel": true}

## zero/unigrama/L-lib+f vs zero/unigrama/L-fix
positivas 4, negativas 14, neutras 0, inconclusivas 10, com reuso 6

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 63,269 | 5 | [] | True | 63,212 | 5 | 1.00 | — | negativa |
| contidoEm | True | 2,533,471 | 6 | [] | True | 2,533,378 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 33,320,610 | 8 | [] | True | 25,205,259 | 8 | 0.76 | — | negativa |
| todaLinhaTemPreta | True | 8,897,078 | 7 | [] | True | 7,151,177 | 7 | 0.80 | — | negativa |
| complementoDe | True | 53,457 | 4 | [] | True | 49,302 | 4 | 0.92 | — | negativa |
| pretasPorColunas | True | 13,394,616 | 7 | [] | True | 9,488,132 | 7 | 0.71 | — | negativa |
| intersecaoOrdenada | True | 1,873,686 | 6 | [] | True | 1,656,031 | 6 | 0.88 | — | negativa |
| contemTodasPretas | True | 17,081 | 4 | ['abs2', 'abs5'] | True | 5,215,549 | 7 | 305.34 | — | positiva |
| colunaVazia | True | 72,260,695 | 8 | [] | True | 21,608,416 | 8 | 0.30 | — | negativa |
| naBorda | True | 163,626,094 | 9 | [] | True | 107,988,306 | 9 | 0.66 | — | negativa |
| linhaDaPosicao | True | 11,768,471 | 8 | [] | True | 5,823,963 | 8 | 0.49 | — | negativa |
| juntarSemRepetir | True | 34,597,798 | 7 | [] | True | 14,622,173 | 7 | 0.42 | — | negativa |
| brancasDaLista | True | 4,731,398 | 6 | ['abs4', 'abs5', 'abs7'] | True | 418,697 | 6 | 0.09 | — | negativa |
| diferencaSimetrica | False | 118,800,726 | None | [] | True | 97,217,593 | 9 | — | ≤ 0.82 | negativa (só L-fix aceita; razão exata indefinida) |
| pretasOrdemInversa | False | 103,066,320 | None | [] | False | 128,094,122 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 83,488,578 | None | [] | False | 117,976,801 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| linhaTemPretaEm | True | 3,947,145 | 8 | ['abs11'] | True | 58,627,128 | 11 | 14.85 | — | positiva |
| semPretaIsolada | False | 105,675,960 | None | [] | False | 132,951,369 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| colunasBrancas | False | 120,812,574 | None | [] | False | 122,571,966 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | True | 94,221,940 | 9 | ['abs2', 'abs7'] | True | 135,897,388 | 10 | 1.44 | — | positiva |
| tocaPreta | True | 80,312,555 | 8 | ['abs3'] | True | 34,189,249 | 9 | 0.43 | — | negativa |
| bordaPreta | False | 144,105,513 | None | [] | False | 128,091,011 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | False | 246,083,600 | None | [] | False | 73,070,629 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| semPretasAdjacentes | True | 4,543,707 | 6 | ['abs20', 'abs5'] | False | 132,928,549 | None | — | ≥ 29.26 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 366,266,501 | None | [] | False | 120,124,742 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 167,321,651 | None | [] | False | 132,911,173 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 162,793,507 | None | [] | False | 128,802,648 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 365,955,916 | None | [] | False | 120,226,679 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=63,269 → L-lib+f 1 vs L-fix 1; contidoEm: C=2,596,740 → L-lib+f 2 vs L-fix 2; vizinhosPretos: C=35,917,350 → L-lib+f 3 vs L-fix 5; todaLinhaTemPreta: C=44,814,428 → L-lib+f 4 vs L-fix 6; complementoDe: C=44,867,885 → L-lib+f 5 vs L-fix 6; pretasPorColunas: C=58,262,501 → L-lib+f 6 vs L-fix 8; intersecaoOrdenada: C=60,136,187 → L-lib+f 7 vs L-fix 8; contemTodasPretas: C=60,153,268 → L-lib+f 8 vs L-fix 8; colunaVazia: C=132,413,963 → L-lib+f 9 vs L-fix 9; naBorda: C=296,040,057 → L-lib+f 10 vs L-fix 13; linhaDaPosicao: C=307,808,528 → L-lib+f 11 vs L-fix 14; juntarSemRepetir: C=342,406,326 → L-lib+f 12 vs L-fix 14; brancasDaLista: C=347,137,724 → L-lib+f 13 vs L-fix 14; linhaTemPretaEm: C=656,440,493 → L-lib+f 14 vs L-fix 15; mesmoConjunto: C=977,150,967 → L-lib+f 15 vs L-fix 15; tocaPreta: C=1,057,463,522 → L-lib+f 16 vs L-fix 17; semPretasAdjacentes: C=1,452,196,342 → L-lib+f 17 vs L-fix 17

## zero/unigrama/L-lib+f vs zero/unigrama/L-lib+f/lesao
{"tarefas_apos_lesao": 14, "aceitas_L-lib+f": 4, "aceitas_lesao": 4, "custo_L-lib+f": 2048595467, "custo_lesao": 2143315855, "entradas_removidas": 14, "sensivel": true}

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

### Hipóteses — zero/tamanho/L-lib
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,260, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,269, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 6,329,231, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 2,121,894, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 39,254, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 1,870,008, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,616,739, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 3,692,877, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 44,429,952, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 34,024,340, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 6,988,562, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 8,423,679, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 1,626,743, reuso []
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 76,785,285, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 87,145,066, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 79,426,765, reuso []
- linhaTemPretaEm: aceita=False (orcamento_enumeracao), ``, custo 162,443,047, reuso []
- semPretaIsolada: aceita=True (aceita), `λx0. abs3 x0 (λx1. mapear@P>LP (vizinhos x0) (pretas x0))`, custo 80,773,129, reuso ['abs3']
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 85,562,121, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. e (abs2 x0 x1) (abs2 x1 x0)`, custo 155,946,702, reuso ['abs2']
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 113,008,796, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 87,181,296, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 48,822,487, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 95,185,263, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 153,721,979, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 91,118,754, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 91,832,079, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 153,759,121, reuso []
  entradas de biblioteca: abs1 = `λg1. filtrar@P (celula g1)` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:mesmoConjunto': 2}); abs3 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {'bx:semPretaIsolada': 1})

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

### Hipóteses — zero/tamanho/L-lib+f/lesao
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
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 81,699,085, reuso []
- algumaLinhaCheia: aceita=True (aceita), `λx0. nao (vazia?@LP (filtrar@LP (todos@P (celula x0)) (linhas x0)))`, custo 71,510,345, reuso []
- linhaTemPretaEm: aceita=False (orcamento_enumeracao), ``, custo 165,333,141, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 138,836,817, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 80,059,991, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 199,395,688, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 88,733,980, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 90,179,602, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 116,094,793, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs1 x0 (pretas x0))`, custo 570,238, reuso ['abs1']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 142,017,563, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 142,439,823, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 137,881,663, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 141,996,180, reuso []
  entradas de biblioteca: abs1 = `λg1. algum@P (λp2. algum@P (celula g1) (vizinhos g1 p2))` (descoberta, reut. {'bx:semPretasAdjacentes': 1})

### Hipóteses — zero/unigrama/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,212, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,378, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 25,205,259, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 7,151,177, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 49,302, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 9,488,132, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,656,031, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 5,215,549, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 21,608,416, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 107,988,306, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 5,823,963, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 14,622,173, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 418,697, reuso []
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 97,217,593, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 128,094,122, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 117,976,801, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. todos@LP (algum@P (celula x0)) (filtrar@LP (pertence x1) (linhas x0))`, custo 58,627,128, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 132,951,369, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 122,571,966, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (concatenar@P (diferenca x0 x1) (diferenca x1 x0))`, custo 135,897,388, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 34,189,249, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 128,091,011, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 73,070,629, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 132,928,549, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 120,124,742, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 132,911,173, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 128,802,648, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 120,226,679, reuso []

### Hipóteses — zero/unigrama/L-lib
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,260, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,488, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 25,205,468, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 7,151,480, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 49,658, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 9,489,135, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,678,481, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 5,343,132, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 39,954,324, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 122,421,521, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 7,233,117, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 15,874,251, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 1,248,846, reuso []
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 101,167,639, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 106,060,001, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 96,761,921, reuso []
- linhaTemPretaEm: aceita=False (orcamento_enumeracao), ``, custo 89,519,674, reuso []
- semPretaIsolada: aceita=True (aceita), `λx0. abs3 x0 (λx1. mapear@P>LP (vizinhos x0) (pretas x0))`, custo 93,109,621, reuso ['abs3']
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 99,215,391, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (abs4 (diferenca x0 x1) x1 x0)`, custo 59,788,198, reuso ['abs4']
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 56,635,512, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 89,744,295, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 102,693,175, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. vazia?@P (abs1 x0 (juntar (mapear@P>LP (vizinhos x0) (pretas x0))))`, custo 97,536,699, reuso ['abs1']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 69,875,674, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 83,183,932, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 76,046,155, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 69,887,345, reuso []
  entradas de biblioteca: abs1 = `λg1. filtrar@P (celula g1)` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {}); abs3 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {'bx:semPretaIsolada': 1}); abs4 = `λl1 l2 l3. concatenar@P l1 (diferenca l2 l3)` (descoberta, reut. {'bx:mesmoConjunto': 1}); abs5 = `λl1 l2. abs4 (diferenca l1 l2) l2 l1` (descoberta, reut. {}); abs6 = `λg1. mapear@P>LP (vizinhos g1) (pretas g1)` (descoberta, reut. {}); abs7 = `λg1 f2. abs1 g1 (juntar (f2 g1))` (descoberta, reut. {})

### Hipóteses — zero/unigrama/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,269, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,471, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 33,320,610, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 8,897,078, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 53,457, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 13,394,616, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,873,686, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (abs5 x0)`, custo 17,081, reuso ['abs2', 'abs5']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 72,260,695, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 163,626,094, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 11,768,471, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 34,597,798, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (abs5 x0))`, custo 4,731,398, reuso ['abs4', 'abs5', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 118,800,726, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 103,066,320, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 83,488,578, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs11 x0 x1)`, custo 3,947,145, reuso ['abs11']
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 105,675,960, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 120,812,574, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. abs2 (concatenar@P x0 x1) (abs7 x0 x1)`, custo 94,221,940, reuso ['abs2', 'abs7']
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. nao (vazia?@P (abs3 x0 x1)))`, custo 80,312,555, reuso ['abs3']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 144,105,513, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 246,083,600, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs20 x0 (abs5 x0))`, custo 4,543,707, reuso ['abs20', 'abs5']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 366,266,501, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 167,321,651, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 162,793,507, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 365,955,916, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1, 'bx:mesmoConjunto': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'bx:tocaPreta': 1}); abs4 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {'bx:contemTodasPretas': 1, 'bx:brancasDaLista': 1, 'bx:semPretasAdjacentes': 1}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1, 'bx:mesmoConjunto': 1}); abs8 = `λg1. abs2 (abs5 g1)` (descoberta, reut. {}); abs9 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {}); abs10 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs11 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs12 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs13 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs14 = `λg1. abs7 (abs4 g1 (abs5 g1))` (descoberta, reut. {}); abs15 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs16 = `λg1 p2. algum@P (celula g1) (abs11 g1 p2)` (descoberta, reut. {}); abs17 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs18 = `λl1 l2. abs2 (concatenar@P l1 l2) (abs7 l1 l2)` (descoberta, reut. {}); abs19 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs20 = `λg1. algum@P (λp2. nao (vazia?@P (abs3 g1 p2)))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs21 = `λf1 g2. f1 g2` (descoberta, reut. {})

### Hipóteses — zero/unigrama/L-lib+f/lesao
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,269, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,471, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 33,320,610, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 8,897,078, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 53,457, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 13,394,616, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,873,686, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (abs5 x0)`, custo 17,081, reuso ['abs2', 'abs5']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 72,260,695, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 163,626,094, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 11,768,471, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 34,597,798, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (abs5 x0))`, custo 4,731,398, reuso ['abs4', 'abs5', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 118,800,726, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 163,606,233, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 145,757,578, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. todos@LP (algum@P (celula x0)) (filtrar@LP (pertence x1) (linhas x0))`, custo 53,068,329, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 217,246,573, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 213,964,586, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (concatenar@P (diferenca x0 x1) (diferenca x1 x0))`, custo 136,258,220, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 56,883,155, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 193,073,535, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 272,112,884, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs3 x0 (pretas x0))`, custo 3,266,646, reuso ['abs3']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 184,986,015, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 161,523,631, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 156,621,065, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 184,947,405, reuso []
  entradas de biblioteca: abs1 = `λg1 p2. todos@LP (algum@P (celula g1)) (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (concatenar@P (diferenca l1 l2) (diferenca l2 l1))` (descoberta, reut. {}); abs3 = `λg1. algum@P (λp2. algum@P (celula g1) (vizinhos g1 p2))` (descoberta, reut. {'bx:semPretasAdjacentes': 1})

## Medições
parede total 1998 s
- zero/tamanho/L-fix: parede 850 s, CPU 840 s, memória 544080 KiB
- zero/tamanho/L-lib: parede 730 s, CPU 722 s, memória 499100 KiB
- zero/tamanho/L-lib+f: parede 572 s, CPU 565 s, memória 857428 KiB
- zero/tamanho/L-lib+f/lesao: parede 819 s, CPU 807 s, memória 674620 KiB
- zero/unigrama/L-fix: parede 884 s, CPU 873 s, memória 516472 KiB
- zero/unigrama/L-lib: parede 678 s, CPU 669 s, memória 576840 KiB
- zero/unigrama/L-lib+f: parede 846 s, CPU 833 s, memória 1283588 KiB
- zero/unigrama/L-lib+f/lesao: parede 1137 s, CPU 1123 s, memória 816400 KiB
