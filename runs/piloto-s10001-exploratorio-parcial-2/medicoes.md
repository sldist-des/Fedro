# Piloto — medições reais (NÃO determinísticas)

Tempo de parede e memória de pico (ru_maxrss do processo, KiB). Não entram no livro-razão.

- fase 2: parede 0.4 s; CPU (processo + filhos) 0.4 s
- fase 3: parede 1395.2 s; CPU (processo + filhos) 3255.9 s
- fase 4: parede 15.8 s; CPU (processo + filhos) 31.7 s
- fase 5: parede 3.4 s; CPU (processo + filhos) 3.3 s
- fase 1: parede 26.8 s; CPU (processo + filhos) 83.7 s
- fase 6: parede 822.4 s; CPU (processo + filhos) 1905.8 s
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
| ParAdjacente | 3 | 0.207 | 323.699 | 3.089 |
| ParAdjacente | 4 | 0.072 | 1382.666 | 0.723 |
| ParAdjacente | 5 | 1.427 | 70.099 | 14.265 |
| ParAdjacente | 6 | 2.407 | 41.538 | 24.074 |
| NenhumaIsolada | 3 | 0.499 | 86.120 | 11.612 |
| NenhumaIsolada | 4 | 0.154 | 648.562 | 1.542 |
| NenhumaIsolada | 5 | 0.109 | 920.154 | 1.087 |
| NenhumaIsolada | 6 | 0.145 | 689.580 | 1.450 |
| UmComponente | 3 | 0.338 | 97.543 | 10.252 |
| UmComponente | 4 | 0.294 | 340.170 | 2.940 |
| UmComponente | 5 | 0.075 | 1329.759 | 0.752 |
| UmComponente | 6 | 0.114 | 875.883 | 1.142 |
| Igual_linha1_linhaN | 3 | 0.066 | 484.310 | 2.065 |
| Igual_linha1_linhaN | 4 | 0.177 | 565.522 | 1.768 |
| Igual_linha1_linhaN | 5 | 0.057 | 1765.687 | 0.566 |
| Igual_linha1_linhaN | 6 | 0.109 | 914.701 | 1.093 |
| LinhasIguais | 3 | 0.029 | 239.281 | 4.179 |
| LinhasIguais | 4 | 0.227 | 440.588 | 2.270 |
| LinhasIguais | 5 | 0.137 | 731.849 | 1.366 |
| LinhasIguais | 6 | 0.066 | 1513.941 | 0.661 |
| TodosMesmoTamanho | 3 | 0.614 | 53.755 | 18.603 |
| TodosMesmoTamanho | 4 | 0.280 | 357.069 | 2.801 |
| TodosMesmoTamanho | 5 | 0.231 | 431.973 | 2.315 |
| TodosMesmoTamanho | 6 | 0.137 | 730.514 | 1.369 |
| DoisSeparados | 3 | 0.977 | 28.654 | 34.899 |
| DoisSeparados | 4 | 0.156 | 641.111 | 1.560 |
| DoisSeparados | 5 | 0.130 | 769.975 | 1.299 |
| DoisSeparados | 6 | 0.167 | 598.980 | 1.670 |

## Execução autônoma

| braço | parede (s) | CPU (s) | memória pico (KiB) |
|---|---|---|---|
| L-fix@E0 | 325.955 | 297.059 | 581836 |
| L-lib@E0 | 327.562 | 300.282 | 580900 |
| L-lib+f@E0 | 316.693 | 286.366 | 573944 |
| L-fix@E0mais | 552.392 | 520.982 | 622940 |
| L-lib@E0mais | 505.601 | 500.869 | 636556 |
