# Piloto — medições reais (NÃO determinísticas)

Tempo de parede, CPU e memória de pico. Memória de um job = pico do TRECHO (VmHWM reiniciado no início do job, num processo novo por job) quando 'trecho'; 'processo-desde-o-inicio' = ru_maxrss monotônico. A linha de cada fase dá só o pico do processo PRINCIPAL desde o início (não a memória da fase). Nada aqui entra no livro-razão.

- fase 3: parede 2116.7 s; CPU (processo + filhos) 6238.6 s (reaproveitada)
- fase 1: parede 32.6 s; CPU (processo + filhos) 124.9 s
- fase 2: parede 0.3 s; CPU (processo + filhos) 0.3 s
- fase 4: parede 14.2 s; CPU (processo + filhos) 28.1 s
- fase 5: parede 2.9 s; CPU (processo + filhos) 2.9 s
- fase 6: parede 789.6 s; CPU (processo + filhos) 1867.8 s
- fase 7: parede 0.0 s; CPU (processo + filhos) 0.0 s

## Condições de custo (documento 03, seções 4, 8, 9)

- PM9 (vazão em tamanhos ≤ 8): mín 56, mediana 423, máx 2899 candidatos/s; 83/84 abaixo do limiar 2000/s → FALHA
- I6 (vazão < 200/s): 21/84 medições → DISPARADA (I6 exige vazão abaixo do limiar 'após otimização'; nenhuma otimização foi tentada)
- PM13 (latência do oráculo ≤ 2.0 s): máx 0.405 s → ok; I3 (> 10.0 s): não disparada
- PM16 (custo projetado): 3.179 ms/candidato, K médio 1.40 → 7440 h de CPU (limiar 2000 h) → EXCEDE; candidato = candidato do protocolo + candidato interno do enumerador (o custo de CPU inclui ambos); B aplicado como no piloto

## PM9 (vazão do enumerador por job)

| classe | base | contexto/tipo | tabela | D | tempo (s) | candidatos/s (total) | memória pico (KiB) | escopo |
|---|---|---|---|---|---|---|---|---|
| contexto | E0 | {g} → Bool | curada | 2 | 335.107 | 298.416 | 1699748 | trecho |
| contexto | E0 | {g} → L Pos | curada | 2 | 8.321 | 1201.955 | 224292 | trecho |
| contexto | E0 | {g, S: L Pos} → L Pos | curada | 2 | 272.747 | 193.315 | 4026792 | trecho |
| fechado | E0 | fechado Grade → Bool | curada | 2 | 18.461 | 541.726 | 130100 | trecho |
| fechado | E0 | fechado Grade → Pos → L Pos | curada | 2 | 13.991 | 714.824 | 217504 | trecho |
| fechado | E0 | fechado Grade → L Pos → L Pos | curada | 2 | 17.532 | 570.458 | 213156 | trecho |
| fechado | E0 | fechado L Pos → L Pos → L Pos | curada | 2 | 10.921 | 915.789 | 304364 | trecho |
| fechado | E0 | fechado L Pos → L Pos → Bool | curada | 2 | 51.800 | 193.070 | 233256 | trecho |
| contexto | E0p | {g} → Bool | curada | 2 | 984.788 | 101.546 | 1904556 | trecho |
| contexto | E0p | {g} → L Pos | curada | 2 | 29.599 | 337.888 | 276780 | trecho |
| contexto | E0p | {g, S: L Pos} → L Pos | curada | 2 | 88.187 | 113.407 | 645916 | trecho |
| fechado | E0p | fechado Grade → Bool | curada | 2 | 76.188 | 131.268 | 210932 | trecho |
| fechado | E0p | fechado Grade → Pos → L Pos | curada | 2 | 66.392 | 150.636 | 172452 | trecho |
| fechado | E0p | fechado Grade → L Pos → L Pos | curada | 2 | 62.247 | 160.667 | 240356 | trecho |
| fechado | E0p | fechado L Pos → L Pos → L Pos | curada | 2 | 28.518 | 350.694 | 224932 | trecho |
| fechado | E0p | fechado L Pos → L Pos → Bool | curada | 2 | 163.499 | 61.169 | 224724 | trecho |
| contexto | E0mais | {g} → Bool | curada | 2 | 335.303 | 298.241 | 2047492 | trecho |
| contexto | E0mais | {g} → L Pos | curada | 2 | 18.044 | 554.247 | 237196 | trecho |
| contexto | E0mais | {g, S: L Pos} → L Pos | curada | 2 | 123.392 | 81.051 | 699152 | trecho |
| fechado | E0mais | fechado Grade → Bool | curada | 2 | 24.114 | 414.732 | 201980 | trecho |
| fechado | E0mais | fechado Grade → Pos → L Pos | curada | 2 | 39.004 | 256.409 | 176980 | trecho |
| fechado | E0mais | fechado Grade → L Pos → L Pos | curada | 2 | 66.374 | 150.677 | 344148 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | curada | 2 | 57.982 | 172.485 | 323408 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → Bool | curada | 2 | 58.126 | 172.059 | 259024 | trecho |
| contexto | E0pmais | {g} → Bool | curada | 2 | 27.184 | 367.895 | 218896 | trecho |
| contexto | E0pmais | {g} → L Pos | curada | 2 | 39.723 | 251.770 | 300624 | trecho |
| contexto | E0pmais | {g, S: L Pos} → L Pos | curada | 2 | 212.346 | 47.098 | 697660 | trecho |
| fechado | E0pmais | fechado Grade → Bool | curada | 2 | 81.113 | 123.297 | 183428 | trecho |
| fechado | E0pmais | fechado Grade → Pos → L Pos | curada | 2 | 136.628 | 73.199 | 218716 | trecho |
| fechado | E0pmais | fechado Grade → L Pos → L Pos | curada | 2 | 97.254 | 102.834 | 322044 | trecho |
| fechado | E0pmais | fechado L Pos → L Pos → L Pos | curada | 2 | 66.812 | 149.688 | 278156 | trecho |
| fechado | E0pmais | fechado L Pos → L Pos → Bool | curada | 2 | 175.167 | 57.094 | 229584 | trecho |
| contexto | E0 | {g} → Bool | sistematica | 2 | 5.611 | 1782.498 | 142348 | trecho |
| contexto | E0 | {g} → L Pos | sistematica | 2 | 4.688 | 2133.375 | 182656 | trecho |
| contexto | E0 | {g, S: L Pos} → L Pos | sistematica | 2 | 19.034 | 525.426 | 681052 | trecho |
| fechado | E0 | fechado Grade → Bool | sistematica | 2 | 8.716 | 1147.489 | 155956 | trecho |
| fechado | E0 | fechado Grade → Pos → L Pos | sistematica | 2 | 17.714 | 564.566 | 233580 | trecho |
| fechado | E0 | fechado Grade → L Pos → L Pos | sistematica | 2 | 6.478 | 1543.814 | 205788 | trecho |
| fechado | E0 | fechado L Pos → L Pos → L Pos | sistematica | 2 | 8.704 | 1149.038 | 263328 | trecho |
| fechado | E0 | fechado L Pos → L Pos → Bool | sistematica | 2 | 21.667 | 461.587 | 305596 | trecho |
| contexto | E0mais | {g} → Bool | sistematica | 2 | 16.458 | 607.674 | 201060 | trecho |
| contexto | E0mais | {g} → L Pos | sistematica | 2 | 22.097 | 452.595 | 220612 | trecho |
| contexto | E0mais | {g, S: L Pos} → L Pos | sistematica | 2 | 158.195 | 63.219 | 1028812 | trecho |
| fechado | E0mais | fechado Grade → Bool | sistematica | 2 | 29.983 | 333.561 | 273104 | trecho |
| fechado | E0mais | fechado Grade → Pos → L Pos | sistematica | 2 | 48.986 | 204.162 | 290416 | trecho |
| fechado | E0mais | fechado Grade → L Pos → L Pos | sistematica | 2 | 44.186 | 226.340 | 279028 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | sistematica | 2 | 78.118 | 128.024 | 397508 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → Bool | sistematica | 2 | 78.612 | 127.220 | 338888 | trecho |
| fechado | E0p | fechado Grade → Pos → L Pos | curada | 4 | 28.121 | 355.646 | 391336 | trecho |
| contexto | E0p | {g, S: L Pos} → L Pos | curada | 4 | 78.557 | 127.309 | 504096 | trecho |
| fechado | E0p | fechado Grade → L Pos → L Pos | curada | 4 | 15.499 | 645.258 | 351408 | trecho |
| contexto | E0p | {g} → Bool | curada | 4 | 14.897 | 671.339 | 201264 | trecho |
| fechado | E0p | fechado L Pos → L Pos → L Pos | curada | 4 | 14.672 | 681.633 | 516852 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | curada | 4 | 55.270 | 180.947 | 558240 | trecho |
| fechado | E0pmais | fechado Grade → Pos → L Pos | curada | 4 | 53.778 | 185.968 | 393180 | trecho |
| contexto | E0pmais | {g, S: L Pos} → L Pos | curada | 4 | 196.557 | 50.881 | 612060 | trecho |
| contexto | E0pmais | {g} → Bool | curada | 4 | 17.049 | 586.614 | 224288 | trecho |
| fechado | E0pmais | fechado L Pos → L Pos → L Pos | curada | 4 | 24.935 | 401.083 | 517564 | trecho |
| fechado | E0 | fechado Grade → Pos → L Pos | anteriores:vizPretos | 2 | 13.487 | 741.539 | 217744 | trecho |
| contexto | E0 | {g} → Bool | anteriores:ParAdjacente | 2 | 8.129 | 1230.251 | 185328 | trecho |
| contexto | E0 | {g} → Bool | anteriores:NenhumaIsolada | 2 | 8.371 | 1194.716 | 186468 | trecho |
| contexto | E0 | {g, S: L Pos} → L Pos | anteriores:passo | 2 | 26.294 | 380.359 | 581884 | trecho |
| fechado | E0 | fechado Grade → L Pos → L Pos | anteriores:fecho | 2 | 18.308 | 546.265 | 228604 | trecho |
| fechado | E0 | fechado Grade → Pos → L Pos | anteriores:componenteDe | 2 | 18.883 | 529.628 | 178224 | trecho |
| contexto | E0 | {g} → Bool | anteriores:UmComponente | 2 | 12.600 | 793.702 | 158048 | trecho |
| contexto | E0 | {g, S: L Pos} → L Pos | anteriores:pretasDe | 2 | 51.686 | 193.494 | 612676 | trecho |
| fechado | E0 | fechado L Pos → L Pos → L Pos | anteriores:descartar | 2 | 15.527 | 644.099 | 266132 | trecho |
| fechado | E0 | fechado L Pos → L Pos → Bool | anteriores:noMaximo | 2 | 30.593 | 326.902 | 233920 | trecho |
| fechado | E0 | fechado L Pos → L Pos → Bool | anteriores:mesmoNumero | 2 | 66.425 | 150.561 | 271688 | trecho |
| contexto | E0 | {g} → Bool | anteriores:PrimeiraUltimaIguais | 2 | 30.120 | 332.040 | 144220 | trecho |
| contexto | E0 | {g} → Bool | anteriores:LinhasIguais | 2 | 32.661 | 306.202 | 144236 | trecho |
| fechado | E0mais | fechado Grade → Pos → L Pos | anteriores:vizPretos | 2 | 40.632 | 246.135 | 177160 | trecho |
| contexto | E0mais | {g} → Bool | anteriores:ParAdjacente | 2 | 12.185 | 820.732 | 235084 | trecho |
| contexto | E0mais | {g} → Bool | anteriores:NenhumaIsolada | 2 | 10.425 | 959.283 | 198064 | trecho |
| contexto | E0mais | {g, S: L Pos} → L Pos | anteriores:passo | 2 | 126.666 | 78.956 | 720152 | trecho |
| fechado | E0mais | fechado Grade → L Pos → L Pos | anteriores:fecho | 2 | 50.976 | 196.190 | 289100 | trecho |
| fechado | E0mais | fechado Grade → Pos → L Pos | anteriores:componenteDe | 2 | 41.964 | 238.325 | 224044 | trecho |
| contexto | E0mais | {g} → Bool | anteriores:UmComponente | 2 | 14.956 | 668.676 | 174028 | trecho |
| contexto | E0mais | {g, S: L Pos} → L Pos | anteriores:pretasDe | 2 | 158.276 | 63.187 | 772388 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | anteriores:descartar | 4 | 64.650 | 154.695 | 557864 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → Bool | anteriores:noMaximo | 2 | 69.179 | 144.566 | 296968 | trecho |
| fechado | E0mais | fechado L Pos → L Pos → Bool | anteriores:mesmoNumero | 2 | 100.744 | 99.272 | 290900 | trecho |
| contexto | E0mais | {g} → Bool | anteriores:PrimeiraUltimaIguais | 2 | 26.823 | 372.847 | 179172 | trecho |
| contexto | E0mais | {g} → Bool | anteriores:LinhasIguais | 2 | 27.147 | 368.407 | 176916 | trecho |

Medições limitadas por memória (dependente de recurso):

| base | contexto/tipo | tabela | D | limite (GB) | candidatos ao parar |
|---|---|---|---|---|---|
| E0 | {g, S: L Pos} → L Pos | curada | 2 | 4.0 | 52726 |

## PM3 (vazão dos geradores)

| conceito | n | tempo (s) | pares/s | projeção 1000 pares (s) |
|---|---|---|---|---|
| ExistePreta | 3 |  |  |  |
| ExistePreta | 4 |  |  |  |
| ExistePreta | 5 |  |  |  |
| ExistePreta | 6 |  |  |  |
| ParAdjacente | 3 | 0.106 | 630.531 | 1.586 |
| ParAdjacente | 4 | 0.066 | 1509.859 | 0.662 |
| ParAdjacente | 5 | 0.647 | 154.546 | 6.471 |
| ParAdjacente | 6 | 1.383 | 72.329 | 13.826 |
| NenhumaIsolada | 3 | 0.298 | 144.248 | 6.932 |
| NenhumaIsolada | 4 | 0.180 | 555.654 | 1.800 |
| NenhumaIsolada | 5 | 0.060 | 1674.013 | 0.597 |
| NenhumaIsolada | 6 | 0.069 | 1448.187 | 0.691 |
| UmComponente | 3 | 0.404 | 81.765 | 12.230 |
| UmComponente | 4 | 0.166 | 603.107 | 1.658 |
| UmComponente | 5 | 0.060 | 1655.347 | 0.604 |
| UmComponente | 6 | 0.059 | 1688.828 | 0.592 |
| Igual_linha1_linhaN | 3 | 0.028 | 1125.566 | 0.888 |
| Igual_linha1_linhaN | 4 | 0.116 | 861.784 | 1.160 |
| Igual_linha1_linhaN | 5 | 0.027 | 3691.905 | 0.271 |
| Igual_linha1_linhaN | 6 | 0.037 | 2709.658 | 0.369 |
| LinhasIguais | 3 | 0.009 | 804.806 | 1.243 |
| LinhasIguais | 4 | 0.140 | 713.421 | 1.402 |
| LinhasIguais | 5 | 0.041 | 2415.325 | 0.414 |
| LinhasIguais | 6 | 0.035 | 2872.061 | 0.348 |
| TodosMesmoTamanho | 3 | 0.310 | 106.551 | 9.385 |
| TodosMesmoTamanho | 4 | 0.110 | 912.238 | 1.096 |
| TodosMesmoTamanho | 5 | 0.069 | 1447.539 | 0.691 |
| TodosMesmoTamanho | 6 | 0.061 | 1635.348 | 0.611 |
| DoisSeparados | 3 | 0.517 | 54.184 | 18.456 |
| DoisSeparados | 4 | 0.089 | 1119.996 | 0.893 |
| DoisSeparados | 5 | 0.057 | 1761.557 | 0.568 |
| DoisSeparados | 6 | 0.052 | 1928.248 | 0.519 |

## Execução autônoma

| braço | parede (s) | CPU (s) | memória pico (KiB) | escopo | consultas ao oráculo | latência máx (s) | latência média (s) |
|---|---|---|---|---|---|---|---|
| L-fix@E0 | 286.671 | 283.720 | 584092 | trecho | 13 | 0.405 | 0.036 |
| L-lib@E0 | 286.127 | 283.628 | 582816 | trecho | 13 | 0.318 | 0.029 |
| L-lib+f@E0 | 269.908 | 266.034 | 574252 | trecho | 14 | 0.326 | 0.027 |
| L-fix@E0mais | 510.567 | 506.420 | 664936 | trecho | 13 | 0.342 | 0.032 |
| L-lib@E0mais | 519.462 | 515.110 | 667108 | trecho | 13 | 0.319 | 0.030 |
