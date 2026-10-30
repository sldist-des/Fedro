# Currículo autodirigido — G = 240000, B_max = 20000, semente 10002, política unigrama

| braço | aceitas | ordem de aceitação | passos | custo total | gasto global (enum.) | cadeia de reuso |
|---|---|---|---|---|---|---|
| autodirigido/L-lib+f | 5: ParAdjacente, expandir, pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 24 | 693,884,358 | 94,014 | [('expandir', ['abs3']), ('ParAdjacente', ['abs4'])] |
| autodirigido/L-fix | 3: pretasColuna1, semLinha1, vizPretos | pretasColuna1 → semLinha1 → vizPretos | 18 | 2,495,569,743 | 152,988 | [] |

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
| 24 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 200,420,427 | 20001 | 5 | `` | [] |

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
| 16 | NenhumaIsolada | 20000 | False | orcamento_enumeracao | 479,422,586 | 20001 | 0 | `` | [] |
| 17 | ParAdjacente | 20000 | False | orcamento_enumeracao | 346,832,914 | 20001 | 0 | `` | [] |
| 18 | expandir | 20000 | False | orcamento_enumeracao | 372,438,922 | 20001 | 0 | `` | [] |

## Medições
- autodirigido/L-lib+f: parede 474 s, CPU 420 s, memória 547400 KiB
- autodirigido/L-fix: parede 1447 s, CPU 1381 s, memória 672952 KiB
