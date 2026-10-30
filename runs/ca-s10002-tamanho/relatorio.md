# Currículo autodirigido — G = 240000, B_max = 20000, semente 10002, política tamanho

| braço | aceitas | ordem de aceitação | passos | custo total | gasto global (enum.) | cadeia de reuso |
|---|---|---|---|---|---|---|
| autodirigido/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | pretasColuna1 → vizPretos → semLinha1 → expandir → ParAdjacente | 25 | 186,656,376 | 78,905 | [('expandir', ['abs2']), ('ParAdjacente', ['abs4'])] |
| autodirigido/L-fix | 3: pretasColuna1, semLinha1, vizPretos | pretasColuna1 → vizPretos → semLinha1 | 16 | 327,685,728 | 96,941 | [] |
| aleatorio#1/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → pretasColuna1 → expandir → semLinha1 → ParAdjacente | 8 | 289,904,726 | 70,756 | [('expandir', ['abs1']), ('ParAdjacente', ['abs3'])] |
| aleatorio#2/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 12 | 596,045,137 | 150,899 | [('expandir', ['abs3']), ('ParAdjacente', ['abs4'])] |
| aleatorio#3/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → expandir → semLinha1 → ParAdjacente → pretasColuna1 | 10 | 598,503,907 | 109,823 | [('expandir', ['abs1']), ('ParAdjacente', ['abs2'])] |
| aleatorio#1/L-fix | 3: pretasColuna1, semLinha1, vizPretos | vizPretos → pretasColuna1 → semLinha1 | 6 | 357,285,291 | 64,931 | [] |
| aleatorio#2/L-fix | 3: pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos | 6 | 357,285,291 | 64,931 | [] |
| aleatorio#3/L-fix | 3: pretasColuna1, semLinha1, vizPretos | vizPretos → pretasColuna1 → semLinha1 | 6 | 357,285,291 | 64,931 | [] |
| manual/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → expandir → ParAdjacente → pretasColuna1 → semLinha1 | 8 | 306,247,785 | 70,162 | [('expandir', ['abs1']), ('ParAdjacente', ['abs2'])] |
| manual/L-fix | 3: pretasColuna1, semLinha1, vizPretos | vizPretos → pretasColuna1 → semLinha1 | 6 | 357,285,291 | 64,931 | [] |

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

## aleatorio#1/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,825 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | pretasColuna1 | 20000 | True | aceita | 6,338,105 | 1417 | 2 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 3 | expandir | 20000 | True | aceita | 5,846,211 | 2905 | 3 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | ['abs1'] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 93,706,551 | 20001 | 3 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 9,242,042 | 3124 | 4 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 80,905,046 | 20001 | 4 | `` | [] |
| 7 | ParAdjacente | 20000 | True | aceita | 3,895,799 | 2026 | 5 | `λx0. nao (vazia?@P (abs3 x0 (pretas x0)))` | ['abs3'] |
| 8 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 83,663,147 | 20001 | 5 | `` | [] |

## aleatorio#2/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | pretasColuna1 | 20000 | True | aceita | 6,154,228 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 2 | ParAdjacente | 20000 | False | orcamento_enumeracao | 83,906,490 | 20001 | 1 | `` | [] |
| 3 | expandir | 20000 | False | orcamento_enumeracao | 49,089,208 | 20001 | 1 | `` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 94,323,976 | 20001 | 1 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 5,873,897 | 2813 | 2 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | vizPretos | 20000 | True | aceita | 7,016,792 | 1713 | 3 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 7 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 95,750,278 | 20001 | 3 | `` | [] |
| 8 | ParAdjacente | 20000 | False | orcamento_enumeracao | 79,444,972 | 20001 | 3 | `` | [] |
| 9 | expandir | 20000 | True | aceita | 6,021,053 | 3059 | 4 | `λx0 x1. juntar (mapear@P>LP (abs3 x0) x1)` | ['abs3'] |
| 10 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 80,905,118 | 20001 | 4 | `` | [] |
| 11 | ParAdjacente | 20000 | True | aceita | 3,895,906 | 2026 | 5 | `λx0. nao (vazia?@P (abs4 x0 (pretas x0)))` | ['abs4'] |
| 12 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 83,663,219 | 20001 | 5 | `` | [] |

## aleatorio#3/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 2 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 3 | vizPretos | 20000 | True | aceita | 6,307,825 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 135,659,617 | 20001 | 1 | `` | [] |
| 5 | expandir | 20000 | True | aceita | 4,550,621 | 2448 | 2 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | ['abs1'] |
| 6 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 100,061,162 | 20001 | 2 | `` | [] |
| 7 | semLinha1 | 20000 | True | aceita | 7,662,068 | 2632 | 3 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 8 | ParAdjacente | 20000 | True | aceita | 3,815,965 | 1783 | 4 | `λx0. nao (vazia?@P (abs2 x0 (pretas x0)))` | ['abs2'] |
| 9 | pretasColuna1 | 20000 | True | aceita | 8,332,286 | 1674 | 5 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 10 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 83,663,147 | 20001 | 5 | `` | [] |

## aleatorio#1/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | pretasColuna1 | 20000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 3 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 4,545,309 | 2366 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | ParAdjacente | 20000 | False | orcamento_enumeracao | 91,826,937 | 20001 | 0 | `` | [] |

## aleatorio#2/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | pretasColuna1 | 20000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 2 | ParAdjacente | 20000 | False | orcamento_enumeracao | 91,826,937 | 20001 | 0 | `` | [] |
| 3 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 4,545,309 | 2366 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |

## aleatorio#3/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 2 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 3 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 4 | ParAdjacente | 20000 | False | orcamento_enumeracao | 91,826,937 | 20001 | 0 | `` | [] |
| 5 | pretasColuna1 | 20000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 6 | semLinha1 | 20000 | True | aceita | 4,545,309 | 2366 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |

## manual/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,825 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | expandir | 20000 | True | aceita | 4,550,621 | 2448 | 2 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | ['abs1'] |
| 3 | ParAdjacente | 20000 | True | aceita | 3,762,043 | 1736 | 2 | `λx0. nao (vazia?@P (abs2 x0 (pretas x0)))` | ['abs2'] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 100,061,162 | 20001 | 2 | `` | [] |
| 5 | pretasColuna1 | 20000 | True | aceita | 7,712,358 | 1570 | 3 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 6 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 93,706,551 | 20001 | 3 | `` | [] |
| 7 | semLinha1 | 20000 | True | aceita | 9,242,179 | 3124 | 4 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 8 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 80,905,046 | 20001 | 4 | `` | [] |

## manual/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 3 | ParAdjacente | 20000 | False | orcamento_enumeracao | 91,826,937 | 20001 | 0 | `` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 5 | pretasColuna1 | 20000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 6 | semLinha1 | 20000 | True | aceita | 4,545,309 | 2366 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |

## Medições
- autodirigido/L-lib+f: parede 144 s, CPU 103 s, memória 466384 KiB
- autodirigido/L-fix: parede 246 s, CPU 182 s, memória 620848 KiB
- aleatorio#1/L-lib+f: parede 185 s, CPU 137 s, memória 515084 KiB
- aleatorio#2/L-lib+f: parede 324 s, CPU 284 s, memória 595996 KiB
- aleatorio#3/L-lib+f: parede 309 s, CPU 281 s, memória 631968 KiB
- aleatorio#1/L-fix: parede 190 s, CPU 178 s, memória 481840 KiB
- aleatorio#2/L-fix: parede 187 s, CPU 178 s, memória 588728 KiB
- aleatorio#3/L-fix: parede 181 s, CPU 173 s, memória 632248 KiB
- manual/L-lib+f: parede 142 s, CPU 138 s, memória 554296 KiB
- manual/L-fix: parede 181 s, CPU 178 s, memória 531220 KiB
