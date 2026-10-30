# Currículo autodirigido — G = 240000, B_max = 20000, semente 10002, política tamanho

| braço | aceitas | ordem de aceitação | passos | custo total | gasto global (enum.) | cadeia de reuso |
|---|---|---|---|---|---|---|
| autodirigido/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | pretasColuna1 → vizPretos → semLinha1 → expandir → ParAdjacente | 26 | 270,319,595 | 98,906 | [('expandir', ['abs2']), ('ParAdjacente', ['abs4'])] |
| autodirigido/L-fix | 3: pretasColuna1, semLinha1, vizPretos | pretasColuna1 → vizPretos → semLinha1 | 19 | 667,963,881 | 156,944 | [] |

## autodirigido/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,526,184 | 2001 | 0 | `` | [] |
| 2 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,525,830 | 2001 | 0 | `` | [] |
| 3 | expandir | 2000 | False | orcamento_enumeracao | 1,505,228 | 2001 | 0 | `` | [] |
| 4 | pretasColuna1 | 2000 | True | aceita | 6,154,228 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 5 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,234,885 | 2001 | 1 | `` | [] |
| 6 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,234,243 | 2001 | 1 | `` | [] |
| 7 | expandir | 2000 | False | orcamento_enumeracao | 2,501,894 | 2001 | 1 | `` | [] |
| 8 | semLinha1 | 2000 | False | orcamento_enumeracao | 2,581,989 | 2001 | 1 | `` | [] |
| 9 | vizPretos | 2000 | True | aceita | 6,543,678 | 1614 | 2 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 10 | semLinha1 | 2000 | False | orcamento_enumeracao | 2,671,688 | 2001 | 2 | `` | [] |
| 11 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,279,432 | 2001 | 2 | `` | [] |
| 12 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,278,502 | 2001 | 2 | `` | [] |
| 13 | expandir | 2000 | False | orcamento_enumeracao | 2,588,704 | 2001 | 2 | `` | [] |
| 14 | semLinha1 | 4000 | True | aceita | 6,089,959 | 2905 | 3 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 15 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,331,196 | 2001 | 3 | `` | [] |
| 16 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,330,279 | 2001 | 3 | `` | [] |
| 17 | expandir | 2000 | False | orcamento_enumeracao | 2,144,737 | 2001 | 3 | `` | [] |
| 18 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 7,232,200 | 4001 | 3 | `` | [] |
| 19 | ParAdjacente | 4000 | False | orcamento_enumeracao | 7,304,597 | 4001 | 3 | `` | [] |
| 20 | expandir | 4000 | True | aceita | 6,021,053 | 3059 | 4 | `λx0 x1. juntar (mapear@P>LP (abs2 x0) x1)` | ['abs2'] |
| 21 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 8,848,094 | 4001 | 4 | `` | [] |
| 22 | ParAdjacente | 4000 | True | aceita | 3,895,906 | 2026 | 5 | `λx0. nao (vazia?@P (abs4 x0 (pretas x0)))` | ['abs4'] |
| 23 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 10,274,313 | 4001 | 5 | `` | [] |
| 24 | NenhumaIsolada | 8000 | False | orcamento_enumeracao | 26,249,092 | 8001 | 5 | `` | [] |
| 25 | NenhumaIsolada | 16000 | False | orcamento_enumeracao | 65,308,465 | 16001 | 5 | `` | [] |
| 26 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 83,663,219 | 20001 | 5 | `` | [] |

## autodirigido/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,526,184 | 2001 | 0 | `` | [] |
| 2 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,525,830 | 2001 | 0 | `` | [] |
| 3 | expandir | 2000 | False | orcamento_enumeracao | 1,505,228 | 2001 | 0 | `` | [] |
| 4 | pretasColuna1 | 2000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 5 | semLinha1 | 2000 | False | orcamento_enumeracao | 1,552,226 | 2001 | 0 | `` | [] |
| 6 | vizPretos | 2000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 7 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 8,514,106 | 4001 | 0 | `` | [] |
| 8 | ParAdjacente | 4000 | False | orcamento_enumeracao | 8,511,863 | 4001 | 0 | `` | [] |
| 9 | expandir | 4000 | False | orcamento_enumeracao | 6,457,736 | 4001 | 0 | `` | [] |
| 10 | semLinha1 | 4000 | True | aceita | 4,545,309 | 2366 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 11 | NenhumaIsolada | 8000 | False | orcamento_enumeracao | 28,058,699 | 8001 | 0 | `` | [] |
| 12 | ParAdjacente | 8000 | False | orcamento_enumeracao | 28,054,613 | 8001 | 0 | `` | [] |
| 13 | expandir | 8000 | False | orcamento_enumeracao | 25,202,846 | 8001 | 0 | `` | [] |
| 14 | NenhumaIsolada | 16000 | False | orcamento_enumeracao | 84,967,931 | 16001 | 0 | `` | [] |
| 15 | ParAdjacente | 16000 | False | orcamento_enumeracao | 73,028,525 | 16001 | 0 | `` | [] |
| 16 | expandir | 16000 | False | orcamento_enumeracao | 39,772,803 | 16001 | 0 | `` | [] |
| 17 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 18 | ParAdjacente | 20000 | False | orcamento_enumeracao | 91,826,937 | 20001 | 0 | `` | [] |
| 19 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |

## Medições
- autodirigido/L-lib+f: parede 204 s, CPU 152 s, memória 513632 KiB
- autodirigido/L-fix: parede 443 s, CPU 385 s, memória 698220 KiB
