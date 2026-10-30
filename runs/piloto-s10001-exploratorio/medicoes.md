# Piloto — medições reais (NÃO determinísticas)

Tempo de parede e memória de pico (ru_maxrss do processo, KiB). Não entram no livro-razão.

- fase 2: parede 0.4 s; CPU (processo + filhos) 0.4 s
- fase 3: parede 1395.2 s; CPU (processo + filhos) 3255.9 s
- fase 4: parede 15.8 s; CPU (processo + filhos) 31.7 s
- fase 5: parede 3.4 s; CPU (processo + filhos) 3.3 s
- fase 6: parede 822.4 s; CPU (processo + filhos) 1905.8 s
- fase 1: parede 18.7 s; CPU (processo + filhos) 73.0 s
- fase 7: parede 0.0 s; CPU (processo + filhos) 0.0 s

## PM9 (vazão do enumerador)

| classe | base | contexto/tipo | tempo (s) | candidatos/s | memória pico (KiB) |
|---|---|---|---|---|---|
| contexto | E0 | {g} → Bool | 368.365 | 271.473 | 1710888 |
| contexto | E0 | {g} → L Pos | 9.939 | 1006.286 | 1710888 |
| contexto | E0 | {g, S: L Pos} → L Pos | 284.487 | 184.993 | 4007632 |
| fechado | E0 | Grade → Bool | 21.059 | 474.898 | 1710888 |
| fechado | E0 | Grade → Pos → L Pos | 17.531 | 570.473 | 2062988 |
| fechado | E0 | Grade → L Pos → L Pos | 21.536 | 464.392 | 1710888 |
| fechado | E0 | L Pos → L Pos → L Pos | 11.864 | 843.000 | 2062988 |
| fechado | E0 | L Pos → L Pos → Bool | 58.814 | 170.045 | 1710888 |
| contexto | E0p | {g} → Bool | 1106.232 | 90.398 | 4007632 |
| contexto | E0p | {g} → L Pos | 33.816 | 295.745 | 2062988 |
| contexto | E0p | {g, S: L Pos} → L Pos | 102.716 | 97.365 | 2062988 |
| fechado | E0p | Grade → Bool | 92.144 | 108.537 | 1710888 |
| fechado | E0p | Grade → Pos → L Pos | 75.153 | 133.075 | 2062988 |
| fechado | E0p | Grade → L Pos → L Pos | 70.681 | 141.496 | 1710888 |
| fechado | E0p | L Pos → L Pos → L Pos | 33.798 | 295.903 | 2062988 |
| fechado | E0p | L Pos → L Pos → Bool | 185.818 | 53.821 | 1710888 |
| contexto | E0mais | {g} → Bool | 365.840 | 273.346 | 2062860 |
| contexto | E0mais | {g} → L Pos | 19.434 | 514.607 | 2062988 |
| contexto | E0mais | {g, S: L Pos} → L Pos | 129.465 | 77.249 | 1710888 |
| fechado | E0mais | Grade → Bool | 26.262 | 380.816 | 2062988 |
| fechado | E0mais | Grade → Pos → L Pos | 43.210 | 231.449 | 2062988 |
| fechado | E0mais | Grade → L Pos → L Pos | 71.715 | 139.455 | 2062988 |
| fechado | E0mais | L Pos → L Pos → L Pos | 63.482 | 157.541 | 1710888 |
| fechado | E0mais | L Pos → L Pos → Bool | 65.007 | 153.844 | 2062988 |

## PM3 (vazão dos geradores)

| conceito | n | tempo (s) | pares/s | projeção 1000 pares (s) |
|---|---|---|---|---|
| ExistePreta | 3 |  |  |  |
| ExistePreta | 4 |  |  |  |
| ExistePreta | 5 |  |  |  |
| ExistePreta | 6 |  |  |  |
| ParAdjacente | 3 | 0.127 | 527.237 | 1.897 |
| ParAdjacente | 4 | 0.056 | 1788.361 | 0.559 |
| ParAdjacente | 5 | 0.707 | 141.524 | 7.066 |
| ParAdjacente | 6 | 1.905 | 52.492 | 19.050 |
| NenhumaIsolada | 3 | 0.305 | 140.957 | 7.094 |
| NenhumaIsolada | 4 | 0.173 | 577.211 | 1.732 |
| NenhumaIsolada | 5 | 0.057 | 1751.707 | 0.571 |
| NenhumaIsolada | 6 | 0.067 | 1481.858 | 0.675 |
| UmComponente | 3 | 0.312 | 105.670 | 9.463 |
| UmComponente | 4 | 0.174 | 573.562 | 1.743 |
| UmComponente | 5 | 0.034 | 2928.372 | 0.341 |
| UmComponente | 6 | 0.051 | 1943.563 | 0.515 |
| Igual_linha1_linhaN | 3 | 0.028 | 1151.801 | 0.868 |
| Igual_linha1_linhaN | 4 | 0.114 | 879.549 | 1.137 |
| Igual_linha1_linhaN | 5 | 0.028 | 3607.163 | 0.277 |
| Igual_linha1_linhaN | 6 | 0.034 | 2902.177 | 0.345 |
| LinhasIguais | 3 | 0.010 | 717.914 | 1.393 |
| LinhasIguais | 4 | 0.153 | 653.705 | 1.530 |
| LinhasIguais | 5 | 0.062 | 1624.513 | 0.616 |
| LinhasIguais | 6 | 0.038 | 2606.381 | 0.384 |
| TodosMesmoTamanho | 3 | 0.312 | 105.863 | 9.446 |
| TodosMesmoTamanho | 4 | 0.097 | 1030.493 | 0.970 |
| TodosMesmoTamanho | 5 | 0.060 | 1668.215 | 0.599 |
| TodosMesmoTamanho | 6 | 0.067 | 1490.347 | 0.671 |
| DoisSeparados | 3 | 0.548 | 51.124 | 19.560 |
| DoisSeparados | 4 | 0.116 | 863.234 | 1.158 |
| DoisSeparados | 5 | 0.036 | 2779.854 | 0.360 |
| DoisSeparados | 6 | 0.046 | 2182.304 | 0.458 |

## Execução autônoma

| braço | parede (s) | CPU (s) | memória pico (KiB) |
|---|---|---|---|
| L-fix@E0 | 325.955 | 297.059 | 581836 |
| L-fix@E0mais | 552.392 | 520.982 | 622940 |
| L-lib+f@E0 | 316.693 | 286.366 | 573944 |
| L-lib@E0 | 327.562 | 300.282 | 580900 |
| L-lib@E0mais | 505.601 | 500.869 | 636556 |
