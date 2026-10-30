# Piloto — medições reais (NÃO determinísticas)

Tempo de parede e memória de pico (ru_maxrss do processo, KiB). Não entram no livro-razão.

- fase 1: parede 18.6 s; CPU (processo + filhos) 72.0 s
- fase 2: parede 0.4 s; CPU (processo + filhos) 0.4 s
- fase 3: parede 1395.2 s; CPU (processo + filhos) 3255.9 s
- fase 4: parede 15.8 s; CPU (processo + filhos) 31.7 s
- fase 5: parede 3.4 s; CPU (processo + filhos) 3.3 s
- fase 6: parede 795.3 s; CPU (processo + filhos) 1929.9 s
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
| ParAdjacente | 3 | 0.095 | 708.240 | 1.412 |
| ParAdjacente | 4 | 0.063 | 1597.815 | 0.626 |
| ParAdjacente | 5 | 0.806 | 124.141 | 8.055 |
| ParAdjacente | 6 | 1.694 | 59.022 | 16.943 |
| NenhumaIsolada | 3 | 0.356 | 120.872 | 8.273 |
| NenhumaIsolada | 4 | 0.180 | 554.605 | 1.803 |
| NenhumaIsolada | 5 | 0.053 | 1877.095 | 0.533 |
| NenhumaIsolada | 6 | 0.059 | 1699.002 | 0.589 |
| UmComponente | 3 | 0.261 | 126.420 | 7.910 |
| UmComponente | 4 | 0.170 | 586.979 | 1.704 |
| UmComponente | 5 | 0.042 | 2394.553 | 0.418 |
| UmComponente | 6 | 0.046 | 2166.361 | 0.462 |
| Igual_linha1_linhaN | 3 | 0.028 | 1127.730 | 0.887 |
| Igual_linha1_linhaN | 4 | 0.120 | 831.201 | 1.203 |
| Igual_linha1_linhaN | 5 | 0.027 | 3638.471 | 0.275 |
| Igual_linha1_linhaN | 6 | 0.038 | 2626.869 | 0.381 |
| LinhasIguais | 3 | 0.009 | 793.202 | 1.261 |
| LinhasIguais | 4 | 0.113 | 883.711 | 1.132 |
| LinhasIguais | 5 | 0.067 | 1491.217 | 0.671 |
| LinhasIguais | 6 | 0.062 | 1617.833 | 0.618 |
| TodosMesmoTamanho | 3 | 0.321 | 102.876 | 9.720 |
| TodosMesmoTamanho | 4 | 0.112 | 895.254 | 1.117 |
| TodosMesmoTamanho | 5 | 0.065 | 1547.694 | 0.646 |
| TodosMesmoTamanho | 6 | 0.064 | 1573.207 | 0.636 |
| DoisSeparados | 3 | 0.633 | 44.229 | 22.609 |
| DoisSeparados | 4 | 0.083 | 1203.159 | 0.831 |
| DoisSeparados | 5 | 0.038 | 2623.671 | 0.381 |
| DoisSeparados | 6 | 0.052 | 1907.934 | 0.524 |

## Execução autônoma

| braço | parede (s) | CPU (s) | memória pico (KiB) |
|---|---|---|---|
| L-fix@E0 | 307.728 | 304.473 | 579324 |
| L-lib@E0 | 310.596 | 307.208 | 578448 |
| L-lib+f@E0 | 292.483 | 289.637 | 572148 |
| L-fix@E0mais | 536.820 | 530.092 | 626460 |
| L-lib@E0mais | 502.680 | 498.158 | 635136 |
