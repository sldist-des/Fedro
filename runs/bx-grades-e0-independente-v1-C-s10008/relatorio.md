# Benchmark externo «grades-e0-independente» v1 — hash 9e600a4155844bc4…, 28 tarefas, semente 10008, B = 20000

| braço | aceitas | ids aceitas | custo prévio | custo benchmark | custo cumulativo | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha |
|---|---|---|---|---|---|---|---|---|
| zero/tamanho/L-fix | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, algumaLinhaCheia, tocaPreta | 0 | 1,877,112,558 | 1,877,112,558 | 0 | 0 (0) | True |
| zero/tamanho/L-lib+f | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, tocaPreta, semPretasAdjacentes | 0 | 1,549,616,144 | 1,549,616,144 | 5 | 19 (6) | True |
| zero/unigrama/L-fix | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, linhaTemPretaEm, mesmoConjunto, tocaPreta | 0 | 1,873,084,322 | 1,873,084,322 | 0 | 0 (0) | True |
| zero/unigrama/L-lib+f | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, mesmoConjunto, tocaPreta, semPretasAdjacentes | 0 | 2,517,585,977 | 2,517,585,977 | 6 | 21 (7) | True |

## zero/tamanho/L-lib+f vs zero/tamanho/L-fix
positivas 4, negativas 13, neutras 0, inconclusivas 11, com reuso 5

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 65,678 | 5 | [] | True | 65,621 | 5 | 1.00 | — | negativa |
| contidoEm | True | 881,070 | 6 | [] | True | 880,977 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 6,899,000 | 8 | [] | True | 6,154,389 | 8 | 0.89 | — | negativa |
| todaLinhaTemPreta | True | 3,004,342 | 7 | [] | True | 2,131,108 | 7 | 0.71 | — | negativa |
| complementoDe | True | 41,743 | 4 | [] | True | 38,373 | 4 | 0.92 | — | negativa |
| pretasPorColunas | True | 2,148,200 | 7 | [] | True | 1,845,144 | 7 | 0.86 | — | negativa |
| intersecaoOrdenada | True | 1,874,292 | 6 | [] | True | 1,598,313 | 6 | 0.85 | — | negativa |
| contemTodasPretas | True | 75,807 | 4 | ['abs2'] | True | 3,662,909 | 7 | 48.32 | — | positiva |
| colunaVazia | False | 53,545,538 | None | [] | True | 10,720,075 | 8 | — | ≤ 0.20 | negativa (só L-fix aceita; razão exata indefinida) |
| naBorda | True | 43,392,483 | 9 | [] | True | 32,057,601 | 9 | 0.74 | — | negativa |
| linhaDaPosicao | True | 9,467,770 | 8 | [] | True | 5,999,606 | 8 | 0.63 | — | negativa |
| juntarSemRepetir | True | 15,045,967 | 7 | [] | True | 7,000,167 | 7 | 0.47 | — | negativa |
| brancasDaLista | True | 4,941,237 | 6 | ['abs4', 'abs7'] | True | 815,845 | 6 | 0.17 | — | negativa |
| diferencaSimetrica | False | 125,366,281 | None | [] | False | 89,084,397 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasOrdemInversa | False | 57,269,339 | None | [] | False | 81,995,150 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 66,309,490 | None | [] | True | 72,181,991 | 9 | — | ≤ 1.09 | negativa (só L-fix aceita; razão exata indefinida) |
| linhaTemPretaEm | True | 13,201,870 | 8 | ['abs10'] | False | 161,568,638 | None | — | ≥ 12.24 | positiva (só L-lib+f aceita; razão exata indefinida) |
| semPretaIsolada | False | 93,334,331 | None | [] | False | 139,906,806 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| colunasBrancas | False | 70,171,682 | None | [] | False | 78,718,822 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | False | 100,867,031 | None | [] | False | 199,382,396 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| tocaPreta | True | 59,452,933 | 8 | ['abs15'] | True | 90,462,848 | 9 | 1.52 | — | positiva |
| bordaPreta | False | 72,583,074 | None | [] | False | 77,321,738 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | False | 162,572,322 | None | [] | False | 113,694,952 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| semPretasAdjacentes | True | 2,224,393 | 6 | ['abs18'] | False | 139,852,547 | None | — | ≥ 62.87 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 189,385,543 | None | [] | False | 138,381,560 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 101,441,051 | None | [] | False | 139,853,279 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 101,046,325 | None | [] | False | 139,843,022 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 193,007,352 | None | [] | False | 141,894,284 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=65,678 → L-lib+f 1 vs L-fix 1; contidoEm: C=946,748 → L-lib+f 2 vs L-fix 2; vizinhosPretos: C=7,845,748 → L-lib+f 3 vs L-fix 3; todaLinhaTemPreta: C=10,850,090 → L-lib+f 4 vs L-fix 5; complementoDe: C=10,891,833 → L-lib+f 5 vs L-fix 5; pretasPorColunas: C=13,040,033 → L-lib+f 6 vs L-fix 7; intersecaoOrdenada: C=14,914,325 → L-lib+f 7 vs L-fix 7; contemTodasPretas: C=14,990,132 → L-lib+f 8 vs L-fix 7; naBorda: C=111,928,153 → L-lib+f 9 vs L-fix 13; linhaDaPosicao: C=121,395,923 → L-lib+f 10 vs L-fix 13; juntarSemRepetir: C=136,441,890 → L-lib+f 11 vs L-fix 13; brancasDaLista: C=141,383,127 → L-lib+f 12 vs L-fix 13; linhaTemPretaEm: C=403,530,107 → L-lib+f 13 vs L-fix 14; tocaPreta: C=727,356,084 → L-lib+f 14 vs L-fix 14; semPretasAdjacentes: C=964,735,873 → L-lib+f 15 vs L-fix 14

## zero/unigrama/L-lib+f vs zero/unigrama/L-fix
positivas 4, negativas 14, neutras 0, inconclusivas 10, com reuso 6

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 65,678 | 5 | [] | True | 65,621 | 5 | 1.00 | — | negativa |
| contidoEm | True | 2,533,300 | 6 | [] | True | 2,533,207 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 32,346,226 | 8 | [] | True | 24,537,701 | 8 | 0.76 | — | negativa |
| todaLinhaTemPreta | True | 9,238,949 | 7 | [] | True | 7,177,251 | 7 | 0.78 | — | negativa |
| complementoDe | True | 52,718 | 4 | [] | True | 48,579 | 4 | 0.92 | — | negativa |
| pretasPorColunas | True | 13,436,706 | 7 | [] | True | 9,317,569 | 7 | 0.69 | — | negativa |
| intersecaoOrdenada | True | 1,876,219 | 6 | [] | True | 1,657,816 | 6 | 0.88 | — | negativa |
| contemTodasPretas | True | 38,249 | 4 | ['abs2', 'abs5'] | True | 5,269,063 | 7 | 137.76 | — | positiva |
| colunaVazia | True | 47,717,750 | 8 | [] | True | 21,760,399 | 8 | 0.46 | — | negativa |
| naBorda | True | 164,312,895 | 9 | [] | True | 108,185,128 | 9 | 0.66 | — | negativa |
| linhaDaPosicao | True | 11,659,419 | 8 | [] | True | 5,533,785 | 8 | 0.47 | — | negativa |
| juntarSemRepetir | True | 34,632,195 | 7 | [] | True | 14,629,252 | 7 | 0.42 | — | negativa |
| brancasDaLista | True | 4,241,901 | 6 | ['abs4', 'abs5', 'abs7'] | True | 437,913 | 6 | 0.10 | — | negativa |
| diferencaSimetrica | False | 118,677,637 | None | [] | True | 97,236,579 | 9 | — | ≤ 0.82 | negativa (só L-fix aceita; razão exata indefinida) |
| pretasOrdemInversa | False | 104,574,802 | None | [] | False | 129,155,883 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 83,701,917 | None | [] | False | 119,017,549 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| linhaTemPretaEm | True | 3,938,314 | 8 | ['abs11'] | True | 57,282,883 | 11 | 14.55 | — | positiva |
| semPretaIsolada | False | 103,941,716 | None | [] | False | 134,717,333 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| colunasBrancas | False | 115,609,023 | None | [] | False | 120,892,052 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | True | 94,227,046 | 9 | ['abs2', 'abs7'] | True | 136,607,835 | 10 | 1.45 | — | positiva |
| tocaPreta | True | 79,272,452 | 8 | ['abs3'] | True | 33,970,237 | 9 | 0.43 | — | negativa |
| bordaPreta | False | 123,408,367 | None | [] | False | 122,059,419 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | False | 253,499,892 | None | [] | False | 75,417,964 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| semPretasAdjacentes | True | 3,814,843 | 6 | ['abs20', 'abs5'] | False | 134,712,757 | None | — | ≥ 35.31 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 375,518,013 | None | [] | False | 119,340,544 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 176,834,074 | None | [] | False | 134,656,727 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 176,196,416 | None | [] | False | 134,626,652 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 382,219,260 | None | [] | False | 122,236,624 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=65,678 → L-lib+f 1 vs L-fix 1; contidoEm: C=2,598,978 → L-lib+f 2 vs L-fix 2; vizinhosPretos: C=34,945,204 → L-lib+f 3 vs L-fix 5; todaLinhaTemPreta: C=44,184,153 → L-lib+f 4 vs L-fix 6; complementoDe: C=44,236,871 → L-lib+f 5 vs L-fix 6; pretasPorColunas: C=57,673,577 → L-lib+f 6 vs L-fix 8; intersecaoOrdenada: C=59,549,796 → L-lib+f 7 vs L-fix 8; contemTodasPretas: C=59,588,045 → L-lib+f 8 vs L-fix 8; colunaVazia: C=107,305,795 → L-lib+f 9 vs L-fix 9; naBorda: C=271,618,690 → L-lib+f 10 vs L-fix 13; linhaDaPosicao: C=283,278,109 → L-lib+f 11 vs L-fix 13; juntarSemRepetir: C=317,910,304 → L-lib+f 12 vs L-fix 14; brancasDaLista: C=322,152,205 → L-lib+f 13 vs L-fix 14; linhaTemPretaEm: C=633,044,875 → L-lib+f 14 vs L-fix 15; mesmoConjunto: C=946,822,660 → L-lib+f 15 vs L-fix 15; tocaPreta: C=1,026,095,112 → L-lib+f 16 vs L-fix 16; semPretasAdjacentes: C=1,406,818,214 → L-lib+f 17 vs L-fix 17

### Hipóteses — zero/tamanho/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 65,621, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 880,977, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 6,154,389, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 2,131,108, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 38,373, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 1,845,144, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,598,313, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 3,662,909, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 10,720,075, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 32,057,601, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 5,999,606, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 7,000,167, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 815,845, reuso []
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 89,084,397, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 81,995,150, reuso []
- algumaLinhaCheia: aceita=True (aceita), `λx0. nao (vazia?@LP (filtrar@LP (todos@P (celula x0)) (linhas x0)))`, custo 72,181,991, reuso []
- linhaTemPretaEm: aceita=False (orcamento_enumeracao), ``, custo 161,568,638, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 139,906,806, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 78,718,822, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 199,382,396, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 90,462,848, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 77,321,738, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 113,694,952, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 139,852,547, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 138,381,560, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 139,853,279, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 139,843,022, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 141,894,284, reuso []

### Hipóteses — zero/tamanho/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 65,678, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,070, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 6,899,000, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 3,004,342, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 41,743, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 2,148,200, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,874,292, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (pretas x0)`, custo 75,807, reuso ['abs2']
- colunaVazia: aceita=False (orcamento_enumeracao), ``, custo 53,545,538, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 43,392,483, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 9,467,770, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 15,045,967, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (pretas x0))`, custo 4,941,237, reuso ['abs4', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 125,366,281, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 57,269,339, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 66,309,490, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs10 x0 x1)`, custo 13,201,870, reuso ['abs10']
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 93,334,331, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 70,171,682, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 100,867,031, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. abs15 x0 (vizinhos x0 x1))`, custo 59,452,933, reuso ['abs15']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 72,583,074, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 162,572,322, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs18 x0 (pretas x0))`, custo 2,224,393, reuso ['abs18']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 189,385,543, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 101,441,051, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 101,046,325, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 193,007,352, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {}); abs4 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs8 = `λg1. abs2 (pretas g1)` (descoberta, reut. {}); abs9 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs10 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs11 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs12 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs13 = `λg1. abs7 (abs4 g1 (pretas g1))` (descoberta, reut. {}); abs14 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs15 = `λg1. algum@P (celula g1)` (descoberta, reut. {'bx:tocaPreta': 1}); abs16 = `λg1 p2. abs15 g1 (abs10 g1 p2)` (descoberta, reut. {}); abs17 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs18 = `λg1. algum@P (λp2. abs15 g1 (vizinhos g1 p2))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs19 = `λf1 g2. f1 g2` (descoberta, reut. {})

### Hipóteses — zero/unigrama/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 65,621, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,207, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 24,537,701, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 7,177,251, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 48,579, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 9,317,569, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,657,816, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 5,269,063, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 21,760,399, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 108,185,128, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 5,533,785, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 14,629,252, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 437,913, reuso []
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 97,236,579, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 129,155,883, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 119,017,549, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. todos@LP (algum@P (celula x0)) (filtrar@LP (pertence x1) (linhas x0))`, custo 57,282,883, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 134,717,333, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 120,892,052, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (concatenar@P (diferenca x0 x1) (diferenca x1 x0))`, custo 136,607,835, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 33,970,237, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 122,059,419, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 75,417,964, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 134,712,757, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 119,340,544, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 134,656,727, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 134,626,652, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 122,236,624, reuso []

### Hipóteses — zero/unigrama/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 65,678, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,300, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 32,346,226, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 9,238,949, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 52,718, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 13,436,706, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,876,219, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (abs5 x0)`, custo 38,249, reuso ['abs2', 'abs5']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 47,717,750, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 164,312,895, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 11,659,419, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 34,632,195, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (abs5 x0))`, custo 4,241,901, reuso ['abs4', 'abs5', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 118,677,637, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 104,574,802, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 83,701,917, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs11 x0 x1)`, custo 3,938,314, reuso ['abs11']
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 103,941,716, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 115,609,023, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. abs2 (concatenar@P x0 x1) (abs7 x0 x1)`, custo 94,227,046, reuso ['abs2', 'abs7']
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. nao (vazia?@P (abs3 x0 x1)))`, custo 79,272,452, reuso ['abs3']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 123,408,367, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 253,499,892, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs20 x0 (abs5 x0))`, custo 3,814,843, reuso ['abs20', 'abs5']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 375,518,013, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 176,834,074, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 176,196,416, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 382,219,260, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1, 'bx:mesmoConjunto': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'bx:tocaPreta': 1}); abs4 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {'bx:contemTodasPretas': 1, 'bx:brancasDaLista': 1, 'bx:semPretasAdjacentes': 1}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1, 'bx:mesmoConjunto': 1}); abs8 = `λg1. abs2 (abs5 g1)` (descoberta, reut. {}); abs9 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {}); abs10 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs11 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs12 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs13 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs14 = `λg1. abs7 (abs4 g1 (abs5 g1))` (descoberta, reut. {}); abs15 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs16 = `λg1 p2. algum@P (celula g1) (abs11 g1 p2)` (descoberta, reut. {}); abs17 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs18 = `λl1 l2. abs2 (concatenar@P l1 l2) (abs7 l1 l2)` (descoberta, reut. {}); abs19 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs20 = `λg1. algum@P (λp2. nao (vazia?@P (abs3 g1 p2)))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs21 = `λf1 g2. f1 g2` (descoberta, reut. {})

## Medições
parede total 1420 s
- zero/tamanho/L-fix: parede 1347 s, CPU 864 s, memória 545064 KiB
- zero/tamanho/L-lib+f: parede 940 s, CPU 552 s, memória 877348 KiB
- zero/unigrama/L-fix: parede 1413 s, CPU 932 s, memória 511860 KiB
- zero/unigrama/L-lib+f: parede 1335 s, CPU 839 s, memória 1309352 KiB
