# Benchmark externo «grades-e0-independente» v1 — hash 9e600a4155844bc4…, 28 tarefas, semente 10007, B = 20000

| braço | aceitas | ids aceitas | custo prévio | custo benchmark | custo cumulativo | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha |
|---|---|---|---|---|---|---|---|---|
| previo/tamanho/L-fix | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, algumaLinhaCheia, tocaPreta | 256,054,993 | 1,882,334,319 | 2,138,389,312 | 0 | 0 (0) | True |
| previo/tamanho/L-lib+f | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, semPretaIsolada, tocaPreta, vizinhancaExterna, semPretasAdjacentes | 14,207,750 | 1,646,135,616 | 1,660,343,366 | 8 | 23 (9) | True |
| previo/tamanho/L-lib+f/lesao | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, tocaPreta, semPretasAdjacentes | 14,207,750 | 1,540,841,394 | 1,555,049,144 | 5 | 19 (6) | True |
| previo/unigrama/L-fix | 18/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, linhaTemPretaEm, semPretaIsolada, mesmoConjunto, tocaPreta | 267,421,419 | 2,286,259,390 | 2,553,680,809 | 0 | 0 (0) | True |
| previo/unigrama/L-lib+f | 19/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, linhaTemPretaEm, semPretaIsolada, mesmoConjunto, tocaPreta, vizinhancaExterna, semPretasAdjacentes | 27,904,405 | 1,959,017,673 | 1,986,922,078 | 10 | 25 (10) | True |
| previo/unigrama/L-lib+f/lesao | 18/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, linhaTemPretaEm, semPretaIsolada, mesmoConjunto, tocaPreta, semPretasAdjacentes | 27,904,405 | 1,885,470,112 | 1,913,374,517 | 7 | 21 (8) | True |

## previo/tamanho/L-lib+f vs previo/tamanho/L-fix
positivas 7, negativas 12, neutras 0, inconclusivas 9, com reuso 8

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 83,383 | 5 | [] | True | 63,212 | 5 | 0.76 | — | negativa |
| contidoEm | True | 881,524 | 6 | [] | True | 881,159 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 354 | 1 | ['abs1'] | True | 6,329,022 | 8 | 17878.59 | — | positiva |
| todaLinhaTemPreta | True | 4,154,875 | 7 | [] | True | 2,121,591 | 7 | 0.51 | — | negativa |
| complementoDe | True | 617,649 | 4 | [] | True | 38,898 | 4 | 0.06 | — | negativa |
| pretasPorColunas | True | 3,789,917 | 7 | [] | True | 1,869,005 | 7 | 0.49 | — | negativa |
| intersecaoOrdenada | True | 2,010,127 | 6 | [] | True | 1,596,085 | 6 | 0.79 | — | negativa |
| contemTodasPretas | True | 54,633 | 4 | ['abs4'] | True | 3,628,169 | 7 | 66.41 | — | positiva |
| colunaVazia | False | 54,514,904 | None | [] | True | 24,002,367 | 8 | — | ≤ 0.44 | negativa (só L-fix aceita; razão exata indefinida) |
| naBorda | True | 47,859,553 | 9 | [] | True | 31,918,531 | 9 | 0.67 | — | negativa |
| linhaDaPosicao | True | 10,626,426 | 8 | [] | True | 6,327,740 | 8 | 0.60 | — | negativa |
| juntarSemRepetir | True | 15,669,076 | 7 | [] | True | 6,988,104 | 7 | 0.45 | — | negativa |
| brancasDaLista | True | 6,952,605 | 6 | ['abs5', 'abs8'] | True | 779,063 | 6 | 0.11 | — | negativa |
| diferencaSimetrica | False | 127,413,741 | None | [] | False | 89,614,920 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasOrdemInversa | False | 64,340,165 | None | [] | False | 81,699,085 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 75,420,376 | None | [] | True | 71,510,199 | 9 | — | ≤ 0.95 | negativa (só L-fix aceita; razão exata indefinida) |
| linhaTemPretaEm | True | 15,335,182 | 8 | ['abs11'] | False | 165,333,141 | None | — | ≥ 10.78 | positiva (só L-lib+f aceita; razão exata indefinida) |
| semPretaIsolada | True | 13,577,858 | 7 | ['abs2', 'abs9'] | False | 138,836,817 | None | — | ≥ 10.23 | positiva (só L-lib+f aceita; razão exata indefinida) |
| colunasBrancas | False | 75,048,767 | None | [] | False | 80,059,991 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | False | 99,697,167 | None | [] | False | 199,395,688 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| tocaPreta | True | 22,923,741 | 7 | ['abs16', 'abs2'] | True | 88,733,656 | 9 | 3.87 | — | positiva |
| bordaPreta | False | 76,653,736 | None | [] | False | 81,696,513 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | True | 55,026,934 | 7 | ['abs2'] | False | 111,259,349 | None | — | ≥ 2.02 | positiva (só L-lib+f aceita; razão exata indefinida) |
| semPretasAdjacentes | True | 61,873 | 4 | ['abs19'] | False | 138,781,608 | None | — | ≥ 2243.01 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 325,861,944 | None | [] | False | 138,026,636 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 118,051,315 | None | [] | False | 138,778,100 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 108,557,601 | None | [] | False | 133,999,597 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 320,950,190 | None | [] | False | 138,066,073 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=14,291,133 → L-lib+f 1 vs L-fix 0; contidoEm: C=15,172,657 → L-lib+f 2 vs L-fix 0; vizinhosPretos: C=15,173,011 → L-lib+f 3 vs L-fix 0; todaLinhaTemPreta: C=19,327,886 → L-lib+f 4 vs L-fix 0; complementoDe: C=19,945,535 → L-lib+f 5 vs L-fix 0; pretasPorColunas: C=23,735,452 → L-lib+f 6 vs L-fix 0; intersecaoOrdenada: C=25,745,579 → L-lib+f 7 vs L-fix 0; contemTodasPretas: C=25,800,212 → L-lib+f 8 vs L-fix 0; naBorda: C=128,174,669 → L-lib+f 9 vs L-fix 0; linhaDaPosicao: C=138,801,095 → L-lib+f 10 vs L-fix 0; juntarSemRepetir: C=154,470,171 → L-lib+f 11 vs L-fix 0; brancasDaLista: C=161,422,776 → L-lib+f 12 vs L-fix 0; linhaTemPretaEm: C=443,932,240 → L-lib+f 13 vs L-fix 13; semPretaIsolada: C=457,510,098 → L-lib+f 14 vs L-fix 13; tocaPreta: C=655,179,773 → L-lib+f 15 vs L-fix 14; vizinhancaExterna: C=786,860,443 → L-lib+f 16 vs L-fix 14; semPretasAdjacentes: C=786,922,316 → L-lib+f 17 vs L-fix 14

## previo/tamanho/L-lib+f vs previo/tamanho/L-lib+f/lesao
{"tarefas_apos_lesao": 28, "aceitas_L-lib+f": 17, "aceitas_lesao": 15, "custo_L-lib+f": 1646135616, "custo_lesao": 1540841394, "entradas_removidas": 2, "sensivel": true}

## previo/unigrama/L-lib+f vs previo/unigrama/L-fix
positivas 9, negativas 11, neutras 0, inconclusivas 8, com reuso 10

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 4,523,482 | 5 | [] | True | 2,345,363 | 5 | 0.52 | — | negativa |
| contidoEm | True | 2,638,089 | 6 | [] | True | 2,637,734 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 355 | 1 | ['abs1'] | True | 1,058,542 | 8 | 2981.81 | — | positiva |
| todaLinhaTemPreta | True | 5,563,875 | 7 | [] | True | 3,077,901 | 7 | 0.55 | — | negativa |
| complementoDe | True | 1,851,429 | 5 | [] | True | 50,170 | 5 | 0.03 | — | negativa |
| pretasPorColunas | True | 6,385,948 | 7 | [] | True | 3,154,077 | 7 | 0.49 | — | negativa |
| intersecaoOrdenada | True | 2,034,825 | 6 | [] | True | 1,658,965 | 6 | 0.82 | — | negativa |
| contemTodasPretas | True | 35,442 | 4 | ['abs4'] | True | 1,547,890 | 7 | 43.67 | — | positiva |
| colunaVazia | True | 19,885,514 | 7 | ['abs5'] | True | 20,742,457 | 8 | 1.04 | — | positiva |
| naBorda | False | 97,212,837 | None | [] | True | 101,269,863 | 9 | — | ≤ 1.04 | negativa (só L-fix aceita; razão exata indefinida) |
| linhaDaPosicao | True | 11,670,761 | 8 | [] | True | 6,175,095 | 8 | 0.53 | — | negativa |
| juntarSemRepetir | True | 24,241,333 | 7 | [] | True | 14,641,371 | 7 | 0.60 | — | negativa |
| brancasDaLista | True | 5,515,716 | 6 | ['abs6', 'abs9'] | True | 405,728 | 6 | 0.07 | — | negativa |
| diferencaSimetrica | True | 115,070,678 | 9 | [] | True | 97,268,067 | 9 | 0.85 | — | negativa |
| pretasOrdemInversa | False | 98,521,752 | None | [] | False | 118,311,241 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 95,643,350 | None | [] | False | 132,572,303 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| linhaTemPretaEm | True | 1,287,419 | 7 | ['abs12', 'abs5'] | True | 54,496,399 | 11 | 42.33 | — | positiva |
| semPretaIsolada | True | 7,531,189 | 7 | ['abs10', 'abs2'] | True | 57,625,699 | 10 | 7.65 | — | positiva |
| colunasBrancas | False | 127,015,997 | None | [] | False | 113,735,004 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | True | 2,088,337 | 6 | ['abs17'] | True | 135,914,747 | 10 | 65.08 | — | positiva |
| tocaPreta | True | 16,870,159 | 7 | ['abs2', 'abs5'] | True | 30,318,744 | 9 | 1.80 | — | positiva |
| bordaPreta | False | 146,299,402 | None | [] | False | 118,306,291 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | True | 37,301,118 | 7 | ['abs2'] | False | 158,094,849 | None | — | ≥ 4.24 | positiva (só L-lib+f aceita; razão exata indefinida) |
| semPretasAdjacentes | True | 23,070 | 3 | ['abs20'] | False | 170,223,111 | None | — | ≥ 7378.55 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 387,278,027 | None | [] | False | 316,629,671 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 175,626,689 | None | [] | False | 142,045,866 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 181,493,925 | None | [] | False | 165,222,600 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 385,406,955 | None | [] | False | 316,729,642 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=32,427,887 → L-lib+f 1 vs L-fix 0; contidoEm: C=35,065,976 → L-lib+f 2 vs L-fix 0; vizinhosPretos: C=35,066,331 → L-lib+f 3 vs L-fix 0; todaLinhaTemPreta: C=40,630,206 → L-lib+f 4 vs L-fix 0; complementoDe: C=42,481,635 → L-lib+f 5 vs L-fix 0; pretasPorColunas: C=48,867,583 → L-lib+f 6 vs L-fix 0; intersecaoOrdenada: C=50,902,408 → L-lib+f 7 vs L-fix 0; contemTodasPretas: C=50,937,850 → L-lib+f 8 vs L-fix 0; colunaVazia: C=70,823,364 → L-lib+f 9 vs L-fix 0; linhaDaPosicao: C=179,706,962 → L-lib+f 10 vs L-fix 0; juntarSemRepetir: C=203,948,295 → L-lib+f 11 vs L-fix 0; brancasDaLista: C=209,464,011 → L-lib+f 12 vs L-fix 0; diferencaSimetrica: C=324,534,689 → L-lib+f 13 vs L-fix 9; linhaTemPretaEm: C=519,987,210 → L-lib+f 14 vs L-fix 13; semPretaIsolada: C=527,518,399 → L-lib+f 15 vs L-fix 14; mesmoConjunto: C=656,622,733 → L-lib+f 16 vs L-fix 14; tocaPreta: C=673,492,892 → L-lib+f 17 vs L-fix 14; vizinhancaExterna: C=857,093,412 → L-lib+f 18 vs L-fix 15; semPretasAdjacentes: C=857,116,482 → L-lib+f 19 vs L-fix 15

## previo/unigrama/L-lib+f vs previo/unigrama/L-lib+f/lesao
{"tarefas_apos_lesao": 28, "aceitas_L-lib+f": 19, "aceitas_lesao": 18, "custo_L-lib+f": 1959017673, "custo_lesao": 1885470112, "entradas_removidas": 2, "sensivel": true}

### Hipóteses — previo/tamanho/L-fix
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

### Hipóteses — previo/tamanho/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 83,383, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,524, reuso []
- vizinhosPretos: aceita=True (aceita), `abs1`, custo 354, reuso ['abs1']
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 4,154,875, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 617,649, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 3,789,917, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 2,010,127, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs4 (pretas x0)`, custo 54,633, reuso ['abs4']
- colunaVazia: aceita=False (orcamento_enumeracao), ``, custo 54,514,904, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 47,859,553, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 10,626,426, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 15,669,076, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs8 (abs5 x0 (pretas x0))`, custo 6,952,605, reuso ['abs5', 'abs8']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 127,413,741, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 64,340,165, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 75,420,376, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs11 x0 x1)`, custo 15,335,182, reuso ['abs11']
- semPretaIsolada: aceita=True (aceita), `λx0. abs9 x0 (abs2 x0 (pretas x0))`, custo 13,577,858, reuso ['abs2', 'abs9']
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 75,048,767, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 99,697,167, reuso []
- tocaPreta: aceita=True (aceita), `λx0 x1. abs16 x0 (abs2 x0 x1)`, custo 22,923,741, reuso ['abs16', 'abs2']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 76,653,736, reuso []
- vizinhancaExterna: aceita=True (aceita), `λx0 x1. diferenca (abs2 x0 x1) x1`, custo 55,026,934, reuso ['abs2']
- semPretasAdjacentes: aceita=True (aceita), `λx0. vazia?@P (abs19 x0)`, custo 61,873, reuso ['abs19']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 325,861,944, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 118,051,315, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 108,557,601, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 320,950,190, reuso []
  entradas de biblioteca: abs1 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'expandir': 1, 'bx:vizinhosPretos': 1}); abs2 = `λg1 l2. juntar (mapear@P>LP (abs1 g1) l2)` (descoberta, reut. {'ParAdjacente': 1, 'bx:semPretaIsolada': 1, 'bx:tocaPreta': 1, 'bx:vizinhancaExterna': 1}); abs3 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs4 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1}); abs5 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs6 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {}); abs7 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs8 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs9 = `λg1. abs4 (pretas g1)` (descoberta, reut. {'bx:semPretaIsolada': 1}); abs10 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs11 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs12 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs13 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs14 = `λg1. abs8 (abs5 g1 (pretas g1))` (descoberta, reut. {}); abs15 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs16 = `λg1. algum@P (celula g1)` (descoberta, reut. {'bx:tocaPreta': 1}); abs17 = `λg1 p2. abs16 g1 (abs11 g1 p2)` (descoberta, reut. {}); abs18 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs19 = `λg1. abs2 g1 (pretas g1)` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs20 = `λg1 l2. abs16 g1 (abs2 g1 l2)` (descoberta, reut. {}); abs21 = `λg1 l2. diferenca (abs2 g1 l2) l2` (descoberta, reut. {}); abs22 = `λf1 g2 l3. f1 g2 l3` (descoberta, reut. {}); abs23 = `λg1. vazia?@P (abs19 g1)` (descoberta, reut. {})

### Hipóteses — previo/tamanho/L-lib+f/lesao
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

### Hipóteses — previo/unigrama/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 2,345,363, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,637,734, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 1,058,542, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 3,077,901, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (juntar (linhas x0))`, custo 50,170, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 3,154,077, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,658,965, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 1,547,890, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 20,742,457, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 101,269,863, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 6,175,095, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 14,641,371, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 405,728, reuso []
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 97,268,067, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 118,311,241, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 132,572,303, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. todos@LP (algum@P (celula x0)) (filtrar@LP (pertence x1) (linhas x0))`, custo 54,496,399, reuso []
- semPretaIsolada: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (mapear@P>LP (vizinhos x0) (pretas x0))`, custo 57,625,699, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 113,735,004, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (concatenar@P (diferenca x0 x1) (diferenca x1 x0))`, custo 135,914,747, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 30,318,744, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 118,306,291, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 158,094,849, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 170,223,111, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 316,629,671, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 142,045,866, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 165,222,600, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 316,729,642, reuso []

### Hipóteses — previo/unigrama/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 4,523,482, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,638,089, reuso []
- vizinhosPretos: aceita=True (aceita), `abs1`, custo 355, reuso ['abs1']
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 5,563,875, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (juntar (linhas x0))`, custo 1,851,429, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 6,385,948, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 2,034,825, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs4 (pretas x0)`, custo 35,442, reuso ['abs4']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (abs5 x0) (colunas x0))`, custo 19,885,514, reuso ['abs5']
- naBorda: aceita=False (orcamento_enumeracao), ``, custo 97,212,837, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 11,670,761, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 24,241,333, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs9 (abs6 x0 (pretas x0))`, custo 5,515,716, reuso ['abs6', 'abs9']
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 115,070,678, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 98,521,752, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 95,643,350, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. abs5 x0 (abs12 x0 x1)`, custo 1,287,419, reuso ['abs12', 'abs5']
- semPretaIsolada: aceita=True (aceita), `λx0. abs10 x0 (abs2 x0 (pretas x0))`, custo 7,531,189, reuso ['abs10', 'abs2']
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 127,015,997, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (abs17 x0 x1)`, custo 2,088,337, reuso ['abs17']
- tocaPreta: aceita=True (aceita), `λx0 x1. abs5 x0 (abs2 x0 x1)`, custo 16,870,159, reuso ['abs2', 'abs5']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 146,299,402, reuso []
- vizinhancaExterna: aceita=True (aceita), `λx0 x1. diferenca (abs2 x0 x1) x1`, custo 37,301,118, reuso ['abs2']
- semPretasAdjacentes: aceita=True (aceita), `abs20 (λx0. vazia?@P)`, custo 23,070, reuso ['abs20']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 387,278,027, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 175,626,689, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 181,493,925, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 385,406,955, reuso []
  entradas de biblioteca: abs1 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'expandir': 1, 'bx:vizinhosPretos': 1}); abs2 = `λg1 l2. juntar (mapear@P>LP (abs1 g1) l2)` (descoberta, reut. {'ParAdjacente': 1, 'bx:semPretaIsolada': 1, 'bx:tocaPreta': 1, 'bx:vizinhancaExterna': 1}); abs3 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs4 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1}); abs5 = `λg1. algum@P (celula g1)` (descoberta, reut. {'bx:colunaVazia': 1, 'bx:linhaTemPretaEm': 1, 'bx:tocaPreta': 1}); abs6 = `λg1. diferenca (juntar (linhas g1))` (descoberta, reut. {'bx:brancasDaLista': 1}); abs7 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {}); abs8 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs9 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs10 = `λg1. abs4 (pretas g1)` (descoberta, reut. {'bx:semPretaIsolada': 1}); abs11 = `λg1 f2. todos@LP (abs5 g1) (f2 g1)` (descoberta, reut. {}); abs12 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs13 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs14 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs15 = `λg1. abs9 (abs6 g1 (pretas g1))` (descoberta, reut. {}); abs16 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs17 = `λl1 l2. concatenar@P (diferenca l1 l2) (diferenca l2 l1)` (descoberta, reut. {'bx:mesmoConjunto': 1}); abs18 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs19 = `λg1 p2. abs5 g1 (abs12 g1 p2)` (descoberta, reut. {}); abs20 = `λf1 g2. f1 g2 (abs2 g2 (pretas g2))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs21 = `λl1 l2. vazia?@P (abs17 l1 l2)` (descoberta, reut. {}); abs22 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs23 = `λg1 l2. abs5 g1 (abs2 g1 l2)` (descoberta, reut. {}); abs24 = `λg1 l2. diferenca (abs2 g1 l2) l2` (descoberta, reut. {}); abs25 = `λf1 g2 l3. f1 g2 l3` (descoberta, reut. {})

### Hipóteses — previo/unigrama/L-lib+f/lesao
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 2,345,420, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,637,827, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 1,082,611, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 4,045,400, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (juntar (linhas x0))`, custo 54,347, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 4,649,415, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,865,857, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (pretas x0)`, custo 26,126, reuso ['abs2']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 69,252,590, reuso []
- naBorda: aceita=False (orcamento_enumeracao), ``, custo 100,854,312, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 9,470,029, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 23,394,191, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (pretas x0))`, custo 3,429,541, reuso ['abs4', 'abs7']
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 112,213,087, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 103,382,731, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 90,804,691, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs10 x0 x1)`, custo 2,492,830, reuso ['abs10']
- semPretaIsolada: aceita=True (aceita), `λx0. abs9 x0 (λx1. mapear@P>LP (vizinhos x0) (pretas x0))`, custo 67,778,107, reuso ['abs9']
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 138,399,567, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (abs15 x0 x1)`, custo 1,829,479, reuso ['abs15']
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. nao (vazia?@P (abs3 x0 x1)))`, custo 43,903,489, reuso ['abs3']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 160,167,447, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 218,385,904, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs20 x0 (pretas x0))`, custo 3,428,624, reuso ['abs20']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 209,560,318, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 159,252,865, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 141,496,326, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 209,266,981, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'bx:tocaPreta': 1}); abs4 = `λg1. diferenca (juntar (linhas g1))` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs8 = `λg1. abs2 (pretas g1)` (descoberta, reut. {}); abs9 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {'bx:semPretaIsolada': 1}); abs10 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs11 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs12 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs13 = `λg1. abs7 (abs4 g1 (pretas g1))` (descoberta, reut. {}); abs14 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs15 = `λl1 l2. concatenar@P (diferenca l1 l2) (diferenca l2 l1)` (descoberta, reut. {'bx:mesmoConjunto': 1}); abs16 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs17 = `λg1 p2. algum@P (celula g1) (abs10 g1 p2)` (descoberta, reut. {}); abs18 = `λl1 l2. vazia?@P (abs15 l1 l2)` (descoberta, reut. {}); abs19 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs20 = `λg1. algum@P (λp2. nao (vazia?@P (abs3 g1 p2)))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs21 = `λf1 g2. f1 g2` (descoberta, reut. {})

## Medições
parede total 1639 s
- previo/tamanho/L-fix: parede 1333 s, CPU 992 s, memória 709620 KiB
- previo/tamanho/L-lib+f: parede 772 s, CPU 569 s, memória 1153700 KiB
- previo/tamanho/L-lib+f/lesao: parede 770 s, CPU 575 s, memória 1023632 KiB
- previo/unigrama/L-fix: parede 1566 s, CPU 1238 s, memória 753728 KiB
- previo/unigrama/L-lib+f: parede 834 s, CPU 685 s, memória 1247252 KiB
- previo/unigrama/L-lib+f/lesao: parede 855 s, CPU 703 s, memória 997188 KiB
