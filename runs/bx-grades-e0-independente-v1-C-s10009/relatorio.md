# Benchmark externo «grades-e0-independente» v1 — hash 9e600a4155844bc4…, 28 tarefas, semente 10009, B = 20000

| braço | aceitas | ids aceitas | custo prévio | custo benchmark | custo cumulativo | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha |
|---|---|---|---|---|---|---|---|---|
| zero/tamanho/L-fix | 15/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, algumaLinhaCheia, tocaPreta | 0 | 1,870,886,226 | 1,870,886,226 | 0 | 0 (0) | True |
| zero/tamanho/L-lib+f | 16/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, tocaPreta, semPretasAdjacentes | 0 | 1,548,557,782 | 1,548,557,782 | 5 | 19 (6) | True |
| zero/unigrama/L-fix | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, diferencaSimetrica, linhaTemPretaEm, mesmoConjunto, tocaPreta | 0 | 1,894,030,870 | 1,894,030,870 | 0 | 0 (0) | True |
| zero/unigrama/L-lib+f | 17/28 | ultimaLinha, contidoEm, vizinhosPretos, todaLinhaTemPreta, complementoDe, pretasPorColunas, intersecaoOrdenada, contemTodasPretas, colunaVazia, naBorda, linhaDaPosicao, juntarSemRepetir, brancasDaLista, linhaTemPretaEm, mesmoConjunto, tocaPreta, semPretasAdjacentes | 0 | 2,554,246,679 | 2,554,246,679 | 6 | 21 (7) | True |

## zero/tamanho/L-lib+f vs zero/tamanho/L-fix
positivas 4, negativas 13, neutras 0, inconclusivas 11, com reuso 5

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 63,332 | 5 | [] | True | 63,275 | 5 | 1.00 | — | negativa |
| contidoEm | True | 881,144 | 6 | [] | True | 881,051 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 6,798,771 | 8 | [] | True | 6,001,042 | 8 | 0.88 | — | negativa |
| todaLinhaTemPreta | True | 3,199,229 | 7 | [] | True | 2,230,052 | 7 | 0.70 | — | negativa |
| complementoDe | True | 41,659 | 4 | [] | True | 38,289 | 4 | 0.92 | — | negativa |
| pretasPorColunas | True | 2,181,876 | 7 | [] | True | 1,874,039 | 7 | 0.86 | — | negativa |
| intersecaoOrdenada | True | 1,872,864 | 6 | [] | True | 1,597,301 | 6 | 0.85 | — | negativa |
| contemTodasPretas | True | 75,602 | 4 | ['abs2'] | True | 3,640,135 | 7 | 48.15 | — | positiva |
| colunaVazia | True | 35,490,883 | 8 | [] | True | 12,974,666 | 8 | 0.37 | — | negativa |
| naBorda | True | 42,962,528 | 9 | [] | True | 31,102,129 | 9 | 0.72 | — | negativa |
| linhaDaPosicao | True | 10,405,644 | 8 | [] | True | 5,999,662 | 8 | 0.58 | — | negativa |
| juntarSemRepetir | True | 15,143,939 | 7 | [] | True | 6,996,366 | 7 | 0.46 | — | negativa |
| brancasDaLista | True | 5,399,631 | 6 | ['abs4', 'abs7'] | True | 797,393 | 6 | 0.15 | — | negativa |
| diferencaSimetrica | False | 118,772,824 | None | [] | False | 89,707,896 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasOrdemInversa | False | 63,123,926 | None | [] | False | 81,679,866 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 79,608,646 | None | [] | True | 61,083,567 | 9 | — | ≤ 0.77 | negativa (só L-fix aceita; razão exata indefinida) |
| linhaTemPretaEm | True | 13,773,485 | 8 | ['abs11'] | False | 161,340,902 | None | — | ≥ 11.71 | positiva (só L-lib+f aceita; razão exata indefinida) |
| semPretaIsolada | False | 91,756,219 | None | [] | False | 139,253,767 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| colunasBrancas | False | 72,674,979 | None | [] | False | 78,408,039 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | False | 100,733,324 | None | [] | False | 199,459,741 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| tocaPreta | True | 57,964,818 | 8 | ['abs3'] | True | 92,535,296 | 9 | 1.60 | — | positiva |
| bordaPreta | False | 82,901,583 | None | [] | False | 80,055,631 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | False | 163,921,918 | None | [] | False | 116,720,587 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| semPretasAdjacentes | True | 2,415,992 | 6 | ['abs18'] | False | 139,249,310 | None | — | ≥ 57.64 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 184,963,121 | None | [] | False | 137,538,831 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 94,871,920 | None | [] | False | 139,232,746 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 108,007,922 | None | [] | False | 139,255,617 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 188,550,003 | None | [] | False | 141,169,030 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=63,332 → L-lib+f 1 vs L-fix 1; contidoEm: C=944,476 → L-lib+f 2 vs L-fix 2; vizinhosPretos: C=7,743,247 → L-lib+f 3 vs L-fix 3; todaLinhaTemPreta: C=10,942,476 → L-lib+f 4 vs L-fix 5; complementoDe: C=10,984,135 → L-lib+f 5 vs L-fix 5; pretasPorColunas: C=13,166,011 → L-lib+f 6 vs L-fix 7; intersecaoOrdenada: C=15,038,875 → L-lib+f 7 vs L-fix 7; contemTodasPretas: C=15,114,477 → L-lib+f 8 vs L-fix 7; colunaVazia: C=50,605,360 → L-lib+f 9 vs L-fix 9; naBorda: C=93,567,888 → L-lib+f 10 vs L-fix 13; linhaDaPosicao: C=103,973,532 → L-lib+f 11 vs L-fix 13; juntarSemRepetir: C=119,117,471 → L-lib+f 12 vs L-fix 13; brancasDaLista: C=124,517,102 → L-lib+f 13 vs L-fix 13; linhaTemPretaEm: C=399,795,983 → L-lib+f 14 vs L-fix 14; tocaPreta: C=722,925,323 → L-lib+f 15 vs L-fix 14; semPretasAdjacentes: C=972,164,816 → L-lib+f 16 vs L-fix 14

## zero/unigrama/L-lib+f vs zero/unigrama/L-fix
positivas 4, negativas 14, neutras 0, inconclusivas 10, com reuso 6

| tarefa | L-lib+f | custo | tamanho | reuso | L-fix | custo | tamanho | razão exata (L-fix/L-lib+f) | razão mínima | classe |
|---|---|---|---|---|---|---|---|---|---|---|
| ultimaLinha | True | 63,332 | 5 | [] | True | 63,275 | 5 | 1.00 | — | negativa |
| contidoEm | True | 2,533,421 | 6 | [] | True | 2,533,328 | 6 | 1.00 | — | negativa |
| vizinhosPretos | True | 31,571,833 | 8 | [] | True | 23,872,748 | 8 | 0.76 | — | negativa |
| todaLinhaTemPreta | True | 10,531,679 | 7 | [] | True | 8,213,725 | 7 | 0.78 | — | negativa |
| complementoDe | True | 52,637 | 4 | [] | True | 48,480 | 4 | 0.92 | — | negativa |
| pretasPorColunas | True | 13,700,008 | 7 | [] | True | 9,499,435 | 7 | 0.69 | — | negativa |
| intersecaoOrdenada | True | 1,875,022 | 6 | [] | True | 1,656,993 | 6 | 0.88 | — | negativa |
| contemTodasPretas | True | 38,248 | 4 | ['abs2', 'abs5'] | True | 5,260,503 | 7 | 137.54 | — | positiva |
| colunaVazia | True | 79,570,974 | 8 | [] | True | 21,701,978 | 8 | 0.27 | — | negativa |
| naBorda | True | 163,837,905 | 9 | [] | True | 106,309,353 | 9 | 0.65 | — | negativa |
| linhaDaPosicao | True | 12,520,419 | 8 | [] | True | 5,665,625 | 8 | 0.45 | — | negativa |
| juntarSemRepetir | True | 34,603,685 | 7 | [] | True | 14,626,962 | 7 | 0.42 | — | negativa |
| brancasDaLista | True | 4,583,173 | 6 | ['abs4', 'abs5', 'abs7'] | True | 428,250 | 6 | 0.09 | — | negativa |
| diferencaSimetrica | False | 118,793,165 | None | [] | True | 97,252,277 | 9 | — | ≤ 0.82 | negativa (só L-fix aceita; razão exata indefinida) |
| pretasOrdemInversa | False | 106,760,931 | None | [] | False | 129,616,520 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| algumaLinhaCheia | False | 84,717,827 | None | [] | False | 134,518,775 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| linhaTemPretaEm | True | 3,802,457 | 8 | ['abs11'] | True | 57,436,753 | 11 | 15.11 | — | positiva |
| semPretaIsolada | False | 100,374,725 | None | [] | False | 135,948,406 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| colunasBrancas | False | 114,445,094 | None | [] | False | 121,295,503 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| mesmoConjunto | True | 94,316,465 | 9 | ['abs2', 'abs7'] | True | 135,900,611 | 10 | 1.44 | — | positiva |
| tocaPreta | True | 79,075,952 | 8 | ['abs3'] | True | 35,105,416 | 9 | 0.44 | — | negativa |
| bordaPreta | False | 130,640,736 | None | [] | False | 124,065,835 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| vizinhancaExterna | False | 257,859,392 | None | [] | False | 77,881,817 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| semPretasAdjacentes | True | 3,832,792 | 6 | ['abs20', 'abs5'] | False | 135,902,547 | None | — | ≥ 35.46 | positiva (só L-lib+f aceita; razão exata indefinida) |
| cruzDaPosicao | False | 362,600,173 | None | [] | False | 117,195,940 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasEmDomino | False | 192,584,654 | None | [] | False | 135,899,589 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| pretasConexas | False | 179,798,831 | None | [] | False | 135,923,189 | None | — | — | inconclusiva (nenhum aceita no orçamento) |
| componenteDe | False | 369,161,149 | None | [] | False | 120,207,037 | None | — | — | inconclusiva (nenhum aceita no orçamento) |

Custo cumulativo igual: ultimaLinha: C=63,332 → L-lib+f 1 vs L-fix 1; contidoEm: C=2,596,753 → L-lib+f 2 vs L-fix 2; vizinhosPretos: C=34,168,586 → L-lib+f 3 vs L-fix 3; todaLinhaTemPreta: C=44,700,265 → L-lib+f 4 vs L-fix 6; complementoDe: C=44,752,902 → L-lib+f 5 vs L-fix 6; pretasPorColunas: C=58,452,910 → L-lib+f 6 vs L-fix 8; intersecaoOrdenada: C=60,327,932 → L-lib+f 7 vs L-fix 8; contemTodasPretas: C=60,366,180 → L-lib+f 8 vs L-fix 8; colunaVazia: C=139,937,154 → L-lib+f 9 vs L-fix 9; naBorda: C=303,775,059 → L-lib+f 10 vs L-fix 14; linhaDaPosicao: C=316,295,478 → L-lib+f 11 vs L-fix 14; juntarSemRepetir: C=350,899,163 → L-lib+f 12 vs L-fix 14; brancasDaLista: C=355,482,336 → L-lib+f 13 vs L-fix 14; linhaTemPretaEm: C=669,556,716 → L-lib+f 14 vs L-fix 15; mesmoConjunto: C=978,693,000 → L-lib+f 15 vs L-fix 15; tocaPreta: C=1,057,768,952 → L-lib+f 16 vs L-fix 17; semPretasAdjacentes: C=1,450,101,872 → L-lib+f 17 vs L-fix 17

### Hipóteses — zero/tamanho/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,275, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,051, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 6,001,042, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 2,230,052, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 38,289, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 1,874,039, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,597,301, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 3,640,135, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 12,974,666, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 31,102,129, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 5,999,662, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 6,996,366, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 797,393, reuso []
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 89,707,896, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 81,679,866, reuso []
- algumaLinhaCheia: aceita=True (aceita), `λx0. nao (vazia?@LP (filtrar@LP (todos@P (celula x0)) (linhas x0)))`, custo 61,083,567, reuso []
- linhaTemPretaEm: aceita=False (orcamento_enumeracao), ``, custo 161,340,902, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 139,253,767, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 78,408,039, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 199,459,741, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 92,535,296, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 80,055,631, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 116,720,587, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 139,249,310, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 137,538,831, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 139,232,746, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 139,255,617, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 141,169,030, reuso []

### Hipóteses — zero/tamanho/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,332, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 881,144, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 6,798,771, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 3,199,229, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 41,659, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 2,181,876, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,872,864, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (pretas x0)`, custo 75,602, reuso ['abs2']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 35,490,883, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 42,962,528, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 10,405,644, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 15,143,939, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (pretas x0))`, custo 5,399,631, reuso ['abs4', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 118,772,824, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 63,123,926, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 79,608,646, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs11 x0 x1)`, custo 13,773,485, reuso ['abs11']
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 91,756,219, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 72,674,979, reuso []
- mesmoConjunto: aceita=False (orcamento_enumeracao), ``, custo 100,733,324, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. nao (vazia?@P (abs3 x0 x1)))`, custo 57,964,818, reuso ['abs3']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 82,901,583, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 163,921,918, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs18 x0 (pretas x0))`, custo 2,415,992, reuso ['abs18']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 184,963,121, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 94,871,920, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 108,007,922, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 188,550,003, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'bx:tocaPreta': 1}); abs4 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs8 = `λg1. abs2 (pretas g1)` (descoberta, reut. {}); abs9 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {}); abs10 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs11 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs12 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs13 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs14 = `λg1. abs7 (abs4 g1 (pretas g1))` (descoberta, reut. {}); abs15 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs16 = `λg1 p2. algum@P (celula g1) (abs11 g1 p2)` (descoberta, reut. {}); abs17 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs18 = `λg1. algum@P (λp2. nao (vazia?@P (abs3 g1 p2)))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs19 = `λf1 g2. f1 g2` (descoberta, reut. {})

### Hipóteses — zero/unigrama/L-fix
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,275, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,328, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 23,872,748, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 8,213,725, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 48,480, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 9,499,435, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,656,993, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca (pretas x0) x1)`, custo 5,260,503, reuso []
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 21,701,978, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 106,309,353, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 5,665,625, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 14,626,962, reuso []
- brancasDaLista: aceita=True (aceita), `λx0 x1. diferenca x1 (pretas x0)`, custo 428,250, reuso []
- diferencaSimetrica: aceita=True (aceita), `λx0 x1. concatenar@P (diferenca x0 x1) (diferenca x1 x0)`, custo 97,252,277, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 129,616,520, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 134,518,775, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. todos@LP (algum@P (celula x0)) (filtrar@LP (pertence x1) (linhas x0))`, custo 57,436,753, reuso []
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 135,948,406, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 121,295,503, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. vazia?@P (concatenar@P (diferenca x0 x1) (diferenca x1 x0))`, custo 135,900,611, reuso []
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. algum@P (celula x0) (vizinhos x0 x1))`, custo 35,105,416, reuso []
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 124,065,835, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 77,881,817, reuso []
- semPretasAdjacentes: aceita=False (orcamento_enumeracao), ``, custo 135,902,547, reuso []
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 117,195,940, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 135,899,589, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 135,923,189, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 120,207,037, reuso []

### Hipóteses — zero/unigrama/L-lib+f
- ultimaLinha: aceita=True (aceita), `λx0. cabeca@LP (reverter@LP (linhas x0))`, custo 63,332, reuso []
- contidoEm: aceita=True (aceita), `λx0 x1. vazia?@P (diferenca x0 x1)`, custo 2,533,421, reuso []
- vizinhosPretos: aceita=True (aceita), `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`, custo 31,571,833, reuso []
- todaLinhaTemPreta: aceita=True (aceita), `λx0. todos@LP (algum@P (celula x0)) (linhas x0)`, custo 10,531,679, reuso []
- complementoDe: aceita=True (aceita), `λx0. diferenca (posicoes x0)`, custo 52,637, reuso []
- pretasPorColunas: aceita=True (aceita), `λx0. filtrar@P (celula x0) (juntar (colunas x0))`, custo 13,700,008, reuso []
- intersecaoOrdenada: aceita=True (aceita), `λx0. filtrar@P (λx1. pertence x1 x0)`, custo 1,875,022, reuso []
- contemTodasPretas: aceita=True (aceita), `λx0. abs2 (abs5 x0)`, custo 38,248, reuso ['abs2', 'abs5']
- colunaVazia: aceita=True (aceita), `λx0. nao (todos@LP (algum@P (celula x0)) (colunas x0))`, custo 79,570,974, reuso []
- naBorda: aceita=True (aceita), `λx0 x1. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos x0 x1))))`, custo 163,837,905, reuso []
- linhaDaPosicao: aceita=True (aceita), `λx0 x1. cabeca@LP (filtrar@LP (pertence x1) (linhas x0))`, custo 12,520,419, reuso []
- juntarSemRepetir: aceita=True (aceita), `λx0 x1. concatenar@P x1 (diferenca x0 x1)`, custo 34,603,685, reuso []
- brancasDaLista: aceita=True (aceita), `λx0. abs7 (abs4 x0 (abs5 x0))`, custo 4,583,173, reuso ['abs4', 'abs5', 'abs7']
- diferencaSimetrica: aceita=False (orcamento_enumeracao), ``, custo 118,793,165, reuso []
- pretasOrdemInversa: aceita=False (orcamento_enumeracao), ``, custo 106,760,931, reuso []
- algumaLinhaCheia: aceita=False (orcamento_enumeracao), ``, custo 84,717,827, reuso []
- linhaTemPretaEm: aceita=True (aceita), `λx0 x1. algum@P (celula x0) (abs11 x0 x1)`, custo 3,802,457, reuso ['abs11']
- semPretaIsolada: aceita=False (orcamento_enumeracao), ``, custo 100,374,725, reuso []
- colunasBrancas: aceita=False (orcamento_enumeracao), ``, custo 114,445,094, reuso []
- mesmoConjunto: aceita=True (aceita), `λx0 x1. abs2 (concatenar@P x0 x1) (abs7 x0 x1)`, custo 94,316,465, reuso ['abs2', 'abs7']
- tocaPreta: aceita=True (aceita), `λx0. algum@P (λx1. nao (vazia?@P (abs3 x0 x1)))`, custo 79,075,952, reuso ['abs3']
- bordaPreta: aceita=False (orcamento_enumeracao), ``, custo 130,640,736, reuso []
- vizinhancaExterna: aceita=False (orcamento_enumeracao), ``, custo 257,859,392, reuso []
- semPretasAdjacentes: aceita=True (aceita), `λx0. nao (abs20 x0 (abs5 x0))`, custo 3,832,792, reuso ['abs20', 'abs5']
- cruzDaPosicao: aceita=False (orcamento_enumeracao), ``, custo 362,600,173, reuso []
- pretasEmDomino: aceita=False (orcamento_enumeracao), ``, custo 192,584,654, reuso []
- pretasConexas: aceita=False (orcamento_enumeracao), ``, custo 179,798,831, reuso []
- componenteDe: aceita=False (orcamento_enumeracao), ``, custo 369,161,149, reuso []
  entradas de biblioteca: abs1 = `λg1. cabeca@LP (reverter@LP (linhas g1))` (descoberta, reut. {}); abs2 = `λl1 l2. vazia?@P (diferenca l1 l2)` (descoberta, reut. {'bx:contemTodasPretas': 1, 'bx:mesmoConjunto': 1}); abs3 = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (descoberta, reut. {'bx:tocaPreta': 1}); abs4 = `λg1. diferenca (posicoes g1)` (descoberta, reut. {'bx:brancasDaLista': 1}); abs5 = `λg1. filtrar@P (celula g1) (juntar (colunas g1))` (descoberta, reut. {'bx:contemTodasPretas': 1, 'bx:brancasDaLista': 1, 'bx:semPretasAdjacentes': 1}); abs6 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs7 = `λl1. filtrar@P (λp2. pertence p2 l1)` (descoberta, reut. {'bx:brancasDaLista': 1, 'bx:mesmoConjunto': 1}); abs8 = `λg1. abs2 (abs5 g1)` (descoberta, reut. {}); abs9 = `λg1 f2. todos@LP (algum@P (celula g1)) (f2 g1)` (descoberta, reut. {}); abs10 = `λg1 p2. vazia?@P (cauda@P (cauda@P (cauda@P (vizinhos g1 p2))))` (descoberta, reut. {}); abs11 = `λg1 p2. cabeca@LP (filtrar@LP (pertence p2) (linhas g1))` (descoberta, reut. {'bx:linhaTemPretaEm': 1}); abs12 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs13 = `λl1 l2. concatenar@P l2 (diferenca l1 l2)` (descoberta, reut. {}); abs14 = `λg1. abs7 (abs4 g1 (abs5 g1))` (descoberta, reut. {}); abs15 = `λf1 g2. f1 g2` (descoberta, reut. {}); abs16 = `λg1 p2. algum@P (celula g1) (abs11 g1 p2)` (descoberta, reut. {}); abs17 = `λf1 g2 p3. f1 g2 p3` (descoberta, reut. {}); abs18 = `λl1 l2. abs2 (concatenar@P l1 l2) (abs7 l1 l2)` (descoberta, reut. {}); abs19 = `λf1 l2 l3. f1 l2 l3` (descoberta, reut. {}); abs20 = `λg1. algum@P (λp2. nao (vazia?@P (abs3 g1 p2)))` (descoberta, reut. {'bx:semPretasAdjacentes': 1}); abs21 = `λf1 g2. f1 g2` (descoberta, reut. {})

## Medições
parede total 1173 s
- zero/tamanho/L-fix: parede 1076 s, CPU 825 s, memória 543816 KiB
- zero/tamanho/L-lib+f: parede 807 s, CPU 546 s, memória 853792 KiB
- zero/unigrama/L-fix: parede 1163 s, CPU 917 s, memória 521948 KiB
- zero/unigrama/L-lib+f: parede 1100 s, CPU 841 s, memória 1277984 KiB
