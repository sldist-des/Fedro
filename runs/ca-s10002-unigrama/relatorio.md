# Currículo autodirigido — G = 240000, B_max = 20000, semente 10002, política unigrama

| braço | aceitas | ordem de aceitação | passos | custo total | gasto global (enum.) | cadeia de reuso |
|---|---|---|---|---|---|---|
| autodirigido/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 23 | 493,463,931 | 74,013 | [('expandir', ['abs3']), ('ParAdjacente', ['abs4'])] |
| autodirigido/L-fix | 3: pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos | 15 | 1,296,875,321 | 92,985 | [] |
| aleatorio#1/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → pretasColuna1 → expandir → semLinha1 → ParAdjacente | 8 | 730,452,633 | 69,345 | [('expandir', ['abs1']), ('ParAdjacente', ['abs3'])] |
| aleatorio#2/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 12 | 2,053,239,318 | 150,002 | [('expandir', ['abs3']), ('ParAdjacente', ['abs4'])] |
| aleatorio#3/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → expandir → semLinha1 → ParAdjacente → pretasColuna1 | 10 | 1,546,300,494 | 108,611 | [('expandir', ['abs1']), ('ParAdjacente', ['abs2'])] |
| aleatorio#1/L-fix | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → pretasColuna1 → expandir → semLinha1 → ParAdjacente | 6 | 840,788,152 | 42,657 | [] |
| aleatorio#2/L-fix | 3: pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos | 6 | 1,326,863,779 | 62,976 | [] |
| aleatorio#3/L-fix | 4: ParAdjacente, pretasColuna1, semLinha1, vizPretos | vizPretos → ParAdjacente → pretasColuna1 → semLinha1 | 6 | 770,372,152 | 58,354 | [] |
| manual/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → expandir → ParAdjacente → pretasColuna1 → semLinha1 | 8 | 923,802,790 | 67,881 | [('expandir', ['abs1']), ('ParAdjacente', ['abs2'])] |
| manual/L-fix | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | vizPretos → expandir → ParAdjacente → pretasColuna1 → semLinha1 | 6 | 730,504,678 | 35,808 | [] |

## autodirigido/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,526,184 | 2001 | 0 | `` | [] |
| 2 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,525,830 | 2001 | 0 | `` | [] |
| 3 | expandir | 2000 | False | orcamento_enumeracao | 1,505,228 | 2001 | 0 | `` | [] |
| 4 | pretasColuna1 | 2000 | True | aceita | 6,154,228 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 5 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 13,777,266 | 2001 | 1 | `` | [] |
| 6 | ParAdjacente | 2000 | False | orcamento_enumeracao | 13,774,236 | 2001 | 1 | `` | [] |
| 7 | expandir | 2000 | False | orcamento_enumeracao | 12,409,544 | 2001 | 1 | `` | [] |
| 8 | semLinha1 | 2000 | True | aceita | 11,467,804 | 1689 | 2 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 9 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 11,335,083 | 2001 | 2 | `` | [] |
| 10 | ParAdjacente | 2000 | False | orcamento_enumeracao | 11,332,732 | 2001 | 2 | `` | [] |
| 11 | expandir | 2000 | False | orcamento_enumeracao | 7,272,665 | 2001 | 2 | `` | [] |
| 12 | vizPretos | 2000 | True | aceita | 4,027,041 | 532 | 3 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 13 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 11,753,845 | 2001 | 3 | `` | [] |
| 14 | ParAdjacente | 2000 | False | orcamento_enumeracao | 11,750,366 | 2001 | 3 | `` | [] |
| 15 | expandir | 2000 | False | orcamento_enumeracao | 7,407,662 | 2001 | 3 | `` | [] |
| 16 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 28,190,474 | 4001 | 3 | `` | [] |
| 17 | ParAdjacente | 4000 | False | orcamento_enumeracao | 28,248,412 | 4001 | 3 | `` | [] |
| 18 | expandir | 4000 | True | aceita | 16,880,580 | 3112 | 4 | `λx0 x1. juntar (mapear@P>LP (abs3 x0) x1)` | ['abs3'] |
| 19 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 25,842,443 | 4001 | 4 | `` | [] |
| 20 | ParAdjacente | 4000 | True | aceita | 20,831,648 | 3381 | 5 | `λx0. algum@P (celula x0) (abs4 x0 (pretas x0))` | ['abs4'] |
| 21 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 28,157,129 | 4001 | 5 | `` | [] |
| 22 | NenhumaIsolada | 8000 | False | orcamento_enumeracao | 67,007,273 | 8001 | 5 | `` | [] |
| 23 | NenhumaIsolada | 16000 | False | orcamento_enumeracao | 149,286,258 | 16001 | 5 | `` | [] |

## autodirigido/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 2000 | False | orcamento_enumeracao | 2,526,184 | 2001 | 0 | `` | [] |
| 2 | ParAdjacente | 2000 | False | orcamento_enumeracao | 2,525,830 | 2001 | 0 | `` | [] |
| 3 | expandir | 2000 | False | orcamento_enumeracao | 1,505,228 | 2001 | 0 | `` | [] |
| 4 | pretasColuna1 | 2000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 5 | semLinha1 | 2000 | True | aceita | 10,260,523 | 1343 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | vizPretos | 2000 | True | aceita | 3,022,531 | 349 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 7 | NenhumaIsolada | 4000 | False | orcamento_enumeracao | 57,499,356 | 4001 | 0 | `` | [] |
| 8 | ParAdjacente | 4000 | False | orcamento_enumeracao | 57,498,129 | 4001 | 0 | `` | [] |
| 9 | expandir | 4000 | False | orcamento_enumeracao | 35,392,791 | 4001 | 0 | `` | [] |
| 10 | NenhumaIsolada | 8000 | False | orcamento_enumeracao | 139,376,135 | 8001 | 0 | `` | [] |
| 11 | ParAdjacente | 8000 | False | orcamento_enumeracao | 123,120,121 | 8001 | 0 | `` | [] |
| 12 | expandir | 8000 | False | orcamento_enumeracao | 66,906,178 | 8001 | 0 | `` | [] |
| 13 | NenhumaIsolada | 16000 | False | orcamento_enumeracao | 338,855,676 | 16001 | 0 | `` | [] |
| 14 | ParAdjacente | 16000 | False | orcamento_enumeracao | 263,012,019 | 16001 | 0 | `` | [] |
| 15 | expandir | 16000 | False | orcamento_enumeracao | 189,220,508 | 16001 | 0 | `` | [] |

## aleatorio#1/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,825 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | pretasColuna1 | 20000 | True | aceita | 7,319,933 | 507 | 2 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 3 | expandir | 20000 | True | aceita | 11,135,016 | 1798 | 3 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | ['abs1'] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 270,995,218 | 20001 | 3 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 17,387,633 | 2375 | 4 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 196,055,009 | 20001 | 4 | `` | [] |
| 7 | ParAdjacente | 20000 | True | aceita | 20,831,648 | 3381 | 5 | `λx0. algum@P (celula x0) (abs3 x0 (pretas x0))` | ['abs3'] |
| 8 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 200,420,351 | 20001 | 5 | `` | [] |

## aleatorio#2/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | pretasColuna1 | 20000 | True | aceita | 6,154,228 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 2 | ParAdjacente | 20000 | False | orcamento_enumeracao | 361,761,413 | 20001 | 1 | `` | [] |
| 3 | expandir | 20000 | False | orcamento_enumeracao | 283,512,118 | 20001 | 1 | `` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 443,745,298 | 20001 | 1 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 11,467,804 | 1689 | 2 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | vizPretos | 20000 | True | aceita | 4,027,041 | 532 | 3 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 7 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 263,983,460 | 20001 | 3 | `` | [] |
| 8 | ParAdjacente | 20000 | False | orcamento_enumeracao | 244,400,721 | 20001 | 3 | `` | [] |
| 9 | expandir | 20000 | True | aceita | 16,880,580 | 3112 | 4 | `λx0 x1. juntar (mapear@P>LP (abs3 x0) x1)` | ['abs3'] |
| 10 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 196,054,580 | 20001 | 4 | `` | [] |
| 11 | ParAdjacente | 20000 | True | aceita | 20,831,648 | 3381 | 5 | `λx0. algum@P (celula x0) (abs4 x0 (pretas x0))` | ['abs4'] |
| 12 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 200,420,427 | 20001 | 5 | `` | [] |

## aleatorio#3/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 2 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 3 | vizPretos | 20000 | True | aceita | 6,307,825 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 591,804,485 | 20001 | 1 | `` | [] |
| 5 | expandir | 20000 | True | aceita | 8,328,388 | 1055 | 2 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | ['abs1'] |
| 6 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 429,243,328 | 20001 | 2 | `` | [] |
| 7 | semLinha1 | 20000 | True | aceita | 37,490,998 | 3163 | 3 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 8 | ParAdjacente | 20000 | True | aceita | 16,962,479 | 2356 | 4 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | ['abs2'] |
| 9 | pretasColuna1 | 20000 | True | aceita | 7,291,424 | 751 | 5 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 10 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 200,420,351 | 20001 | 5 | `` | [] |

## aleatorio#1/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | pretasColuna1 | 20000 | True | aceita | 7,110,506 | 403 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 3 | expandir | 20000 | True | aceita | 228,344,978 | 10821 | 0 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 461,076,443 | 20001 | 0 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 10,738,696 | 1491 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | ParAdjacente | 20000 | True | aceita | 127,209,812 | 8660 | 0 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` | [] |

## aleatorio#2/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | pretasColuna1 | 20000 | True | aceita | 6,154,112 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 2 | ParAdjacente | 20000 | False | orcamento_enumeracao | 478,971,372 | 20001 | 0 | `` | [] |
| 3 | expandir | 20000 | False | orcamento_enumeracao | 272,326,917 | 20001 | 0 | `` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 556,128,324 | 20001 | 0 | `` | [] |
| 5 | semLinha1 | 20000 | True | aceita | 10,260,523 | 1343 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 6 | vizPretos | 20000 | True | aceita | 3,022,531 | 349 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |

## aleatorio#3/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 138,795,451 | 20001 | 0 | `` | [] |
| 2 | expandir | 20000 | False | orcamento_enumeracao | 109,655,765 | 20001 | 0 | `` | [] |
| 3 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 4 | ParAdjacente | 20000 | True | aceita | 493,591,744 | 14695 | 0 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` | [] |
| 5 | pretasColuna1 | 20000 | True | aceita | 10,412,487 | 601 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 6 | semLinha1 | 20000 | True | aceita | 11,608,988 | 1775 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |

## manual/L-lib+f
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,825 | 1281 | 1 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | expandir | 20000 | True | aceita | 8,328,388 | 1055 | 2 | `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)` | ['abs1'] |
| 3 | ParAdjacente | 20000 | True | aceita | 13,690,434 | 1773 | 2 | `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))` | ['abs2'] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 410,737,060 | 20001 | 2 | `` | [] |
| 5 | pretasColuna1 | 20000 | True | aceita | 15,323,007 | 953 | 3 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 6 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 252,671,253 | 20001 | 3 | `` | [] |
| 7 | semLinha1 | 20000 | True | aceita | 19,220,815 | 2816 | 4 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |
| 8 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 197,524,008 | 20001 | 4 | `` | [] |

## manual/L-fix
| passo | tarefa | B | aceita | motivo | custo | enum. | versão bib. | hipótese | biblioteca usada |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vizPretos | 20000 | True | aceita | 6,307,717 | 1281 | 0 | `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` | [] |
| 2 | expandir | 20000 | True | aceita | 173,271,908 | 7380 | 0 | `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))` | [] |
| 3 | ParAdjacente | 20000 | True | aceita | 84,396,376 | 4770 | 0 | `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))` | [] |
| 4 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 444,507,202 | 20001 | 0 | `` | [] |
| 5 | pretasColuna1 | 20000 | True | aceita | 10,412,487 | 601 | 0 | `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))` | [] |
| 6 | semLinha1 | 20000 | True | aceita | 11,608,988 | 1775 | 0 | `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))` | [] |

## Medições
- autodirigido/L-lib+f: parede 363 s, CPU 297 s, memória 526916 KiB
- autodirigido/L-fix: parede 806 s, CPU 731 s, memória 610328 KiB
- aleatorio#1/L-lib+f: parede 383 s, CPU 376 s, memória 548172 KiB
- aleatorio#2/L-lib+f: parede 1080 s, CPU 1063 s, memória 567988 KiB
- aleatorio#3/L-lib+f: parede 738 s, CPU 728 s, memória 633352 KiB
- aleatorio#1/L-fix: parede 459 s, CPU 454 s, memória 547304 KiB
- aleatorio#2/L-fix: parede 706 s, CPU 697 s, memória 606024 KiB
- aleatorio#3/L-fix: parede 388 s, CPU 383 s, memória 632264 KiB
- manual/L-lib+f: parede 473 s, CPU 468 s, memória 690624 KiB
- manual/L-fix: parede 395 s, CPU 391 s, memória 590244 KiB
