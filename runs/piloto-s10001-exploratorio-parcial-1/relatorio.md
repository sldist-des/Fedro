# Piloto exploratório — registros determinísticos (semente 10001, escala exploratoria-reduzida)

Nenhuma alegação científica: dados e hiperparâmetros expostos (documento 03, seção 0). Medições reais (tempo, memória) ficam em `medicoes.md`.

## Fase 1 — referências e geradores

PM1: discordâncias ref_a ≠ ref_b no total = **0** (35 conceitos; exaustivo n ∈ [1, 2, 3, 4], 300 amostras por n ∈ [5, 6, 7, 8, 9]).

| conceito | n | k pares | PM2 aceitação | PM4 mesmo nº pretas | PM5 M10 | métodos | hash |
|---|---|---|---|---|---|---|---|
| ExistePreta | 3 | degenerado | nenhum positivo tem negativo com o mesmo número de pretas |  |  |  |  |
| ExistePreta | 4 | degenerado | sem negativos |  |  |  |  |
| ExistePreta | 5 | degenerado | nenhum par formado (200 tentativas, 200 positivos sem par) |  |  |  |  |
| ExistePreta | 6 | degenerado | nenhum par formado (200 tentativas, 200 positivos sem par) |  |  |  |  |
| ParAdjacente | 3 | 67 | 1.000 | 1.000 | 0.500 | {'exato': 50, 'permutacao': 17} | 804c9725daaf |
| ParAdjacente | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 76, 'permutacao': 24} | 3791acc4d03c |
| ParAdjacente | 5 | 100 | 1.000 | 1.000 | 0.500 | {'busca-local': 4, 'permutacao': 30, 'troca1': 55, 'troca2-amostral': 11} | 1ac8ded753bd |
| ParAdjacente | 6 | 100 | 1.000 | 1.000 | 0.500 | {'busca-local': 3, 'permutacao': 23, 'troca1': 70, 'troca2-amostral': 4} | 31de86a8a412 |
| NenhumaIsolada | 3 | 43 | 1.000 | 1.000 | 0.500 | {'exato': 21, 'permutacao': 22} | 5aab312c3ff1 |
| NenhumaIsolada | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 51, 'permutacao': 49} | 6f1d7cbf46bf |
| NenhumaIsolada | 5 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 49, 'troca2-amostral': 1} | ae4f85085da2 |
| NenhumaIsolada | 6 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 0ca057faadc2 |
| UmComponente | 3 | 33 | 1.000 | 1.000 | 0.500 | {'exato': 16, 'permutacao': 17} | 3cd561720ffd |
| UmComponente | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 50, 'permutacao': 50} | f6e6d45e9c2a |
| UmComponente | 5 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | ad29874aab68 |
| UmComponente | 6 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 4e6368cacbf3 |
| Igual_linha1_linhaN | 3 | 32 | 1.000 | 1.000 | 0.500 | {'exato': 16, 'permutacao': 16} | ca8cf71a5286 |
| Igual_linha1_linhaN | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 50, 'permutacao': 50} | 944595ce96c1 |
| Igual_linha1_linhaN | 5 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 65eda473021f |
| Igual_linha1_linhaN | 6 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | af68545e0918 |
| LinhasIguais | 3 | 7 | 1.000 | 1.000 | 0.500 | {'exato': 3, 'permutacao': 4} | 63701ab75e94 |
| LinhasIguais | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 50, 'permutacao': 50} | 33e302512c29 |
| LinhasIguais | 5 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 1aca6946dbee |
| LinhasIguais | 6 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 7d64738bf8ed |
| TodosMesmoTamanho | 3 | 33 | 1.000 | 1.000 | 0.500 | {'exato': 16, 'permutacao': 17} | d5fd99b772ce |
| TodosMesmoTamanho | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 50, 'permutacao': 50} | 9fe253fd140f |
| TodosMesmoTamanho | 5 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 008328280790 |
| TodosMesmoTamanho | 6 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | c5cb4a3d8fcc |
| DoisSeparados | 3 | 28 | 1.000 | 1.000 | 0.500 | {'exato': 14, 'permutacao': 14} | 3039417d6b01 |
| DoisSeparados | 4 | 100 | 1.000 | 1.000 | 0.500 | {'exato': 50, 'permutacao': 50} | b8361eec7efd |
| DoisSeparados | 5 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 49, 'troca1': 51} | 66525d01d631 |
| DoisSeparados | 6 | 100 | 1.000 | 1.000 | 0.500 | {'permutacao': 50, 'troca1': 50} | 3a4207b8ef48 |

PM6: 256 comparações com a auditoria; fora de 3 DP: 17.

| conceito | n | p | piloto | auditoria | DP |
|---|---|---|---|---|---|
| TopoCheio | 3 | 0.65 | 0.324 | 0.275 | 0.015 |
| LinhasIguais | 3 | 0.2 | 0.235 | 0.192 | 0.013 |
| LinhasIguais | 4 | 0.2 | 0.027 | 0.057 | 0.005 |
| Igual_metadeEsq_metadeDir | 3 | 0.2 | 0.472 | 0.419 | 0.016 |
| Igual_metadeEsq_metadeDir | 3 | 0.65 | 0.379 | 0.331 | 0.015 |
| Igual_linha1_linhaN | 3 | 0.35 | 0.384 | 0.331 | 0.015 |
| CantoSupEsq | 3 | 0.2 | 0.110 | 0.2 | 0.010 |
| Diagonal | 3 | 0.65 | 0.340 | 0.275 | 0.015 |
| DoisSeparados | 3 | 0.2 | 0.237 | 0.323 | 0.014 |
| DoisSeparados | 3 | 0.35 | 0.377 | 0.437 | 0.016 |
| MaiorTocaBorda | 3 | 0.2 | 0.726 | 0.834 | 0.014 |
| MaiorTocaBorda | 3 | 0.35 | 0.940 | 0.97 | 0.008 |
| PeloMenosDois | 3 | 0.2 | 0.291 | 0.393 | 0.015 |
| TodosMesmoTamanho | 4 | 0.2 | 0.630 | 0.562 | 0.016 |
| UmComponente | 3 | 0.35 | 0.445 | 0.388 | 0.016 |
| NumCompIgualLinha1 | 3 | 0.2 | 0.391 | 0.329 | 0.016 |
| NumCompIgualLinha1 | 4 | 0.2 | 0.100 | 0.131 | 0.010 |

Degeneração em oraculo_treino (só os degenerados):

| conceito | n | exaustivo | motivo |
|---|---|---|---|
| ExistePreta | 1 | True | sem positivos; sem negativos |
| ExistePreta | 2 | True | sem negativos |
| ExistePreta | 3 | True | nenhum positivo tem negativo com o mesmo número de pretas |
| ExistePreta | 4 | True | sem negativos |
| ExistePreta | 5 | False | sem negativos; (por 200 tentativas; ausência não provada) |
| ExistePreta | 6 | False | sem negativos; (por 200 tentativas; ausência não provada) |
| ParAdjacente | 1 | True | sem positivos; sem negativos |
| ParAdjacente | 2 | True | sem negativos |
| NenhumaIsolada | 1 | True | sem positivos; sem negativos |
| NenhumaIsolada | 2 | True | sem negativos |
| UmComponente | 1 | True | sem positivos; sem negativos |
| UmComponente | 2 | True | sem negativos |
| Igual_linha1_linhaN | 1 | True | sem positivos; sem negativos |
| Igual_linha1_linhaN | 2 | True | nenhum positivo tem negativo com o mesmo número de pretas |
| LinhasIguais | 1 | True | sem positivos; sem negativos |
| LinhasIguais | 2 | True | nenhum positivo tem negativo com o mesmo número de pretas |

## Fase 2 — contagem N(s, τ) (PM7)

- E0 {g} → Bool: 1:2, 2:4, 3:22, 4:102, 5:556, 6:3101, 7:17907, 8:106384, 9:645367, 10:3984141
- E0 {g} → L Pos: 1:1, 2:5, 3:16, 4:73, 5:381, 6:2035, 7:11354, 8:65433, 9:385825, 10:2318750
- E0 {g, S: L Pos} → L Pos: 1:2, 2:6, 3:26, 4:140, 5:790, 6:4778, 7:29954, 8:193252, 9:1275100, 10:8563892
- E0p {g} → Bool: 1:2, 2:4, 3:17, 4:65, 5:314, 6:1587, 7:8190, 8:43549, 9:237091, 10:1316298
- E0p {g} → L Pos: 1:1, 2:4, 3:5, 4:14, 5:77, 6:323, 7:1273, 8:5644, 9:26810, 10:130000
- E0p {g, S: L Pos} → L Pos: 1:2, 2:5, 3:6, 4:31, 5:171, 6:699, 7:3119, 8:15781, 9:81147, 10:422450
- E0mais {g} → Bool: 1:2, 2:4, 3:22, 4:103, 5:578, 6:3359, 7:20196, 8:125234, 9:794685, 10:5138098
- E0mais {g} → L Pos: 1:1, 2:5, 3:17, 4:89, 5:528, 6:3120, 7:19129, 8:121174, 9:782720, 10:5141682
- E0mais {g, S: L Pos} → L Pos: 1:2, 2:6, 3:28, 4:178, 5:1112, 6:7400, 7:51170, 8:362006, 9:2616664, 10:19236606
- E0pmais {g} → Bool: 1:2, 2:4, 3:17, 4:66, 5:323, 6:1644, 7:8550, 8:45817, 9:251248, 10:1403823
- E0pmais {g} → L Pos: 1:1, 2:4, 3:6, 4:22, 5:115, 6:504, 7:2194, 8:10401, 9:51287, 10:257204
- E0pmais {g, S: L Pos} → L Pos: 1:2, 2:5, 3:8, 4:46, 5:250, 6:1112, 7:5429, 8:28939, 9:155157, 10:843344

## Fase 3 — alcance s_reach (PM8)

| classe | base | contexto/tipo | s_reach(B) | s_reach só alvo | s_completo | esgotado | limitado por memória |
|---|---|---|---|---|---|---|---|
| contexto | E0 | {g} → Bool | {'10000': 7, '100000': 9} | {'10000': 9, '100000': 9} | 9 | True | False |
| contexto | E0 | {g} → L Pos | {'10000': 7} | {'10000': 7} | 7 | True | False |
| contexto | E0 | {g, S: L Pos} → L Pos | {'10000': 6, '100000': None} | {'10000': 7, '100000': None} | 7 | False | True |
| fechado | E0 | fechado Grade → Bool | {'10000': 8} | {'10000': 8} | 8 | True | False |
| fechado | E0 | fechado Grade → Pos → L Pos | {'10000': 9} | {'10000': 9} | 9 | True | False |
| fechado | E0 | fechado Grade → L Pos → L Pos | {'10000': 8} | {'10000': 8} | 8 | True | False |
| fechado | E0 | fechado L Pos → L Pos → L Pos | {'10000': 7} | {'10000': 7} | 7 | True | False |
| fechado | E0 | fechado L Pos → L Pos → Bool | {'10000': 9} | {'10000': 9} | 9 | True | False |
| contexto | E0p | {g} → Bool | {'10000': 8, '100000': 10} | {'10000': 10, '100000': 10} | 10 | True | False |
| contexto | E0p | {g} → L Pos | {'10000': 8} | {'10000': 8} | 8 | True | False |
| contexto | E0p | {g, S: L Pos} → L Pos | {'10000': 7} | {'10000': 7} | 7 | True | False |
| fechado | E0p | fechado Grade → Bool | {'10000': 10} | {'10000': 10} | 10 | True | False |
| fechado | E0p | fechado Grade → Pos → L Pos | {'10000': 11} | {'10000': 11} | 11 | True | False |
| fechado | E0p | fechado Grade → L Pos → L Pos | {'10000': 10} | {'10000': 10} | 10 | True | False |
| fechado | E0p | fechado L Pos → L Pos → L Pos | {'10000': 8} | {'10000': 8} | 8 | True | False |
| fechado | E0p | fechado L Pos → L Pos → Bool | {'10000': 10} | {'10000': 10} | 10 | True | False |
| contexto | E0mais | {g} → Bool | {'10000': 7, '100000': 9} | {'10000': 9, '100000': 9} | 9 | True | False |
| contexto | E0mais | {g} → L Pos | {'10000': 7} | {'10000': 7} | 7 | True | False |
| contexto | E0mais | {g, S: L Pos} → L Pos | {'10000': 6} | {'10000': 6} | 6 | True | False |
| fechado | E0mais | fechado Grade → Bool | {'10000': 8} | {'10000': 8} | 8 | True | False |
| fechado | E0mais | fechado Grade → Pos → L Pos | {'10000': 9} | {'10000': 9} | 9 | True | False |
| fechado | E0mais | fechado Grade → L Pos → L Pos | {'10000': 8} | {'10000': 8} | 8 | True | False |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | {'10000': 7} | {'10000': 7} | 7 | True | False |
| fechado | E0mais | fechado L Pos → L Pos → Bool | {'10000': 8} | {'10000': 8} | 8 | True | False |

## Fase 4 — viabilidade da escada (PM10)

Programas da escada são MANUAIS (manual-teste): só limites superiores de tamanho.

| degrau | base | tam. c/ anteriores | bruto | prof. λ (c/ ant. / bruto) | fonte s_reach | B | s_reach | alcançável c/ ant. | alcançável bruto |
|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | E0 | 5 | 5 | 1 / 1 | {g} → Bool | 100000 | 9 | True | True |
| vizPretos | E0 | 8 | 8 | 2 / 2 | fechado Grade → Pos → L Pos | 10000 | 9 | True | True |
| ParAdjacente | E0 | 10 | 13 | 2 / 2 | {g} → Bool | 100000 | 9 | True | False |
| NenhumaIsolada | E0 | 10 | 13 | 2 / 2 | {g} → Bool | 100000 | 9 | True | False |
| passo | E0 | 9 | 14 | 2 / 3 | {g, S: L Pos} → L Pos | 10000 | 6 | False | False |
| fecho | E0 | 16 | 34 | 2 / 3 | fechado Grade → L Pos → L Pos | 10000 | 8 | False | False |
| componenteDe | E0 | 7 | 38 | 2 / 4 | fechado Grade → Pos → L Pos | 10000 | 9 | True | False |
| UmComponente | E0 | 17 | 50 | 2 / 4 | {g} → Bool | 100000 | 9 | False | False |
| pretasDe | E0 | 6 | 6 | 2 / 2 | {g, S: L Pos} → L Pos | 10000 | 6 | True | True |
| descartar | E0 | 13 | 13 | 2 / 2 | fechado L Pos → L Pos → L Pos | 10000 | 7 | False | False |
| noMaximo | E0 | 6 | 18 | 2 / 4 | fechado L Pos → L Pos → Bool | 10000 | 9 | True | False |
| mesmoNumero | E0 | 9 | 35 | 2 / 4 | fechado L Pos → L Pos → Bool | 10000 | 9 | True | False |
| PrimeiraUltimaIguais | E0 | 13 | 49 | 1 / 5 | {g} → Bool | 100000 | 9 | False | False |
| LinhasIguais | E0 | 14 | 51 | 2 / 5 | {g} → Bool | 100000 | 9 | False | False |
| ExistePreta | E0p | 5 | 5 | 1 / 1 | {g} → Bool | 100000 | 10 | True | True |
| vizPretos | E0p | 17 | 17 | 4 / 4 | fechado Grade → Pos → L Pos | 10000 | 11 | False | False |
| ParAdjacente | E0p | 14 | 26 | 3 / 5 | {g} → Bool | 100000 | 10 | False | False |
| NenhumaIsolada | E0p | 14 | 26 | 3 / 5 | {g} → Bool | 100000 | 10 | False | False |
| passo | E0p | 39 | 51 | 6 / 6 | {g, S: L Pos} → L Pos | 10000 | 7 | False | False |
| fecho | E0p | 20 | 112 | 4 / 6 | fechado Grade → L Pos → L Pos | 10000 | 10 | False | False |
| componenteDe | E0p | 7 | 116 | 2 / 7 | fechado Grade → Pos → L Pos | 10000 | 11 | True | False |
| UmComponente | E0p | 28 | 139 | 5 / 8 | {g} → Bool | 100000 | 10 | False | False |
| pretasDe | E0p | 15 | 15 | 4 / 4 | {g, S: L Pos} → L Pos | 10000 | 7 | False | False |
| descartar | E0p | 9 | 9 | 4 / 4 | fechado L Pos → L Pos → L Pos | 10000 | 8 | False | False |
| noMaximo | E0p | 6 | 10 | 2 / 4 | fechado L Pos → L Pos → Bool | 10000 | 10 | True | False |
| mesmoNumero | E0p | 9 | 19 | 2 / 4 | fechado L Pos → L Pos → Bool | 10000 | 10 | True | False |
| PrimeiraUltimaIguais | E0p | 46 | 84 | 3 / 5 | {g} → Bool | 100000 | 10 | False | False |
| LinhasIguais | E0p | 42 | 90 | 5 / 6 | {g} → Bool | 100000 | 10 | False | False |
| ExistePreta | E0mais | 5 | 5 | 1 / 1 | {g} → Bool | 100000 | 9 | True | True |
| vizPretos | E0mais | 8 | 8 | 2 / 2 | fechado Grade → Pos → L Pos | 10000 | 9 | True | True |
| ParAdjacente | E0mais | 10 | 13 | 2 / 2 | {g} → Bool | 100000 | 9 | True | False |
| NenhumaIsolada | E0mais | 10 | 13 | 2 / 2 | {g} → Bool | 100000 | 9 | True | False |
| passo | E0mais | 9 | 14 | 2 / 3 | {g, S: L Pos} → L Pos | 10000 | 6 | False | False |
| fecho | E0mais | 4 | 15 | 1 / 3 | fechado Grade → L Pos → L Pos | 10000 | 8 | True | False |
| componenteDe | E0mais | 7 | 19 | 2 / 4 | fechado Grade → Pos → L Pos | 10000 | 9 | True | False |
| UmComponente | E0mais | 17 | 31 | 2 / 4 | {g} → Bool | 100000 | 9 | False | False |
| pretasDe | E0mais | 6 | 6 | 2 / 2 | {g, S: L Pos} → L Pos | 10000 | 6 | True | True |
| descartar | E0mais | 9 | 9 | 4 / 4 | fechado L Pos → L Pos → L Pos | 10000 | 7 | False | False |
| noMaximo | E0mais | 6 | 10 | 2 / 4 | fechado L Pos → L Pos → Bool | 10000 | 8 | True | False |
| mesmoNumero | E0mais | 9 | 19 | 2 / 4 | fechado L Pos → L Pos → Bool | 10000 | 8 | False | False |
| PrimeiraUltimaIguais | E0mais | 13 | 33 | 1 / 5 | {g} → Bool | 100000 | 9 | False | False |
| LinhasIguais | E0mais | 14 | 35 | 2 / 5 | {g} → Bool | 100000 | 9 | False | False |
| ExistePreta | E0pmais | 5 | 5 | 1 / 1 | {g} → Bool |  |  |  |  |
| vizPretos | E0pmais | 17 | 17 | 4 / 4 | fechado Grade → Pos → L Pos |  |  |  |  |
| ParAdjacente | E0pmais | 14 | 26 | 3 / 5 | {g} → Bool |  |  |  |  |
| NenhumaIsolada | E0pmais | 14 | 26 | 3 / 5 | {g} → Bool |  |  |  |  |
| passo | E0pmais | 39 | 51 | 6 / 6 | {g, S: L Pos} → L Pos |  |  |  |  |
| fecho | E0pmais | 4 | 52 | 1 / 6 | fechado Grade → L Pos → L Pos |  |  |  |  |
| componenteDe | E0pmais | 7 | 56 | 2 / 7 | fechado Grade → Pos → L Pos |  |  |  |  |
| UmComponente | E0pmais | 28 | 79 | 5 / 8 | {g} → Bool |  |  |  |  |
| pretasDe | E0pmais | 15 | 15 | 4 / 4 | {g, S: L Pos} → L Pos |  |  |  |  |
| descartar | E0pmais | 9 | 9 | 4 / 4 | fechado L Pos → L Pos → L Pos |  |  |  |  |
| noMaximo | E0pmais | 6 | 10 | 2 / 4 | fechado L Pos → L Pos → Bool |  |  |  |  |
| mesmoNumero | E0pmais | 9 | 19 | 2 / 4 | fechado L Pos → L Pos → Bool |  |  |  |  |
| PrimeiraUltimaIguais | E0pmais | 46 | 84 | 3 / 5 | {g} → Bool |  |  |  |  |
| LinhasIguais | E0pmais | 42 | 90 | 5 / 6 | {g} → Bool |  |  |  |  |

Verificação dos programas manuais contra as referências do ambiente:

| programa | base | entradas verificadas | discordâncias | documentadas | nota |
|---|---|---|---|---|---|
| ExistePreta | E0 | 303 | 0 | 0 |  |
| vizPretos | E0 | 3192 | 0 | 0 |  |
| ParAdjacente | E0 | 303 | 0 | 0 |  |
| NenhumaIsolada | E0 | 303 | 0 | 1 | grade sem pretas: programa do documento dá verdadeiro, referência falso (DISCREPANCIAS_DOC) |
| passo | E0 | 3411 | 0 | 0 |  |
| fecho | E0 | 3411 | 0 | 0 |  |
| componenteDe | E0 | 3192 | 0 | 0 |  |
| UmComponente | E0 | 303 | 0 | 0 |  |
| pretasDe | E0 | 3411 | 0 | 0 |  |
| descartar | E0 | 16891 | 0 | 0 |  |
| noMaximo | E0 | 16891 | 0 | 0 |  |
| mesmoNumero | E0 | 16891 | 0 | 0 |  |
| PrimeiraUltimaIguais | E0 | 303 | 0 | 0 |  |
| LinhasIguais | E0 | 303 | 0 | 0 |  |
| ExistePreta | E0p | 47 | 0 | 0 |  |
| vizPretos | E0p | 888 | 0 | 0 |  |
| ParAdjacente | E0p | 47 | 0 | 0 |  |
| NenhumaIsolada | E0p | 47 | 0 | 0 |  |
| passo | E0p | 610 | 0 | 0 |  |
| fecho | E0p | 610 | 0 | 0 |  |
| componenteDe | E0p | 888 | 0 | 0 |  |
| UmComponente | E0p | 47 | 0 | 0 |  |
| pretasDe | E0p | 610 | 0 | 0 |  |
| descartar | E0p | 4002 | 0 | 0 |  |
| noMaximo | E0p | 4002 | 0 | 0 |  |
| mesmoNumero | E0p | 4002 | 0 | 0 |  |
| PrimeiraUltimaIguais | E0p | 47 | 0 | 0 |  |
| LinhasIguais | E0p | 47 | 0 | 0 |  |
| ExistePreta | E0mais | 303 | 0 | 0 |  |
| vizPretos | E0mais | 3192 | 0 | 0 |  |
| ParAdjacente | E0mais | 303 | 0 | 0 |  |
| NenhumaIsolada | E0mais | 303 | 0 | 1 | grade sem pretas: programa do documento dá verdadeiro, referência falso (DISCREPANCIAS_DOC) |
| passo | E0mais | 3411 | 0 | 0 |  |
| fecho | E0mais | 3411 | 0 | 0 |  |
| componenteDe | E0mais | 3192 | 0 | 0 |  |
| UmComponente | E0mais | 303 | 0 | 0 |  |
| pretasDe | E0mais | 3411 | 0 | 0 |  |
| descartar | E0mais | 16946 | 0 | 0 |  |
| noMaximo | E0mais | 16946 | 0 | 0 |  |
| mesmoNumero | E0mais | 16946 | 0 | 0 |  |
| PrimeiraUltimaIguais | E0mais | 303 | 0 | 0 |  |
| LinhasIguais | E0mais | 303 | 0 | 0 |  |
| ExistePreta | E0pmais | 47 | 0 | 0 |  |
| vizPretos | E0pmais | 888 | 0 | 0 |  |
| ParAdjacente | E0pmais | 47 | 0 | 0 |  |
| NenhumaIsolada | E0pmais | 47 | 0 | 3 | grade sem pretas: programa do documento dá verdadeiro, referência falso (DISCREPANCIAS_DOC) |
| passo | E0pmais | 605 | 0 | 0 |  |
| fecho | E0pmais | 605 | 0 | 0 |  |
| componenteDe | E0pmais | 888 | 0 | 0 |  |
| UmComponente | E0pmais | 47 | 0 | 0 |  |
| pretasDe | E0pmais | 605 | 0 | 0 |  |
| descartar | E0pmais | 3970 | 0 | 0 |  |
| noMaximo | E0pmais | 3970 | 0 | 0 |  |
| mesmoNumero | E0pmais | 3970 | 0 | 0 |  |
| PrimeiraUltimaIguais | E0pmais | 47 | 0 | 0 |  |
| LinhasIguais | E0pmais | 47 | 0 | 0 |  |

## Fase 5 — MECANISMO (modo mecanismo-teste; soluções MANUAIS; não é descoberta) — PM11

| alvo | fontes manuais | extraído | ordem dos args (perm.) | posição | fragmento igual | entradas gulosas (manual-teste) |
|---|---|---|---|---|---|---|
| vizPretos | ParAdjacente, NenhumaIsolada | True | [0, 1] | 4 | λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2) | λf1 g2. f1 (λp3. nao (vazia?@P (filtrar@P (celula g2) (vizinhos g2 p3)))) (pretas g2) |
| passo | fecho | True | [1, 0] | 1 | λl1 g2. uniao l1 (juntar (mapear@P>LP (λp3. filtrar@P (celula g2) (vizinhos g2 p3)) l1)) | λl1 g2. uniao l1 (juntar (mapear@P>LP (λp3. filtrar@P (celula g2) (vizinhos g2 p3)) l1)) |
| pretasDe | PrimeiraUltimaIguais, LinhasIguais | True | [0, 1] | 11 | λg1. filtrar@P (celula g1) | λl1 l2. vazia?@P ((fix (λf3 l4 l5. se@LP (vazia?@P l4) l5 (f3 (cauda@P l4) (cauda@P l5)))) l1 l2); λg1 l2. filtrar@P (celula g1) (cabeca@LP l2); λl1 l2. e (abs1 l2 l1) (abs1 l1 l2) |

PM11 = 1.00

## Fase 6 — EXECUÇÃO AUTÔNOMA (biblioteca vazia, modo autonomo)

Fechamento do livro-razão: True (diferença 0); hash do diário f9da95bef7188961.

### L-fix@E0

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 61278 | 61278 | 229 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 5669995 | 5731273 | 1658 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 0 |  |  | 37200372 | 42931645 | 11728 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 37200699 | 80132344 | 21798 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 33021819 | 113154163 | 32796 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 33033858 | 146188021 | 43795 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 30066996 | 176255017 | 54474 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 37200528 | 213455545 | 64545 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 34845 | 213490390 | 64641 | 1.000 |  |  |  |
| descartar | False | orcamento_enumeracao | 0 |  |  | 18735104 | 232225494 | 74962 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 3 |  |  | 130323429 | 362548923 | 85566 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 130325829 | 492874752 | 96169 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 37200550 | 530075302 | 106240 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 37200577 | 567275879 | 116310 |  |  |  |  |

### L-lib@E0

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 61326 | 61326 | 229 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 5670142 | 5731468 | 1658 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 0 |  |  | 37200372 | 42931840 | 11728 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 37200699 | 80132539 | 21798 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 33021819 | 113154358 | 32796 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 33033858 | 146188216 | 43795 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 30066996 | 176255212 | 54474 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 37200528 | 213455740 | 64545 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 35218 | 213490958 | 64641 | 1.000 |  |  | abs1 = λg1. filtrar@P (celula g1) (fechamento) |
| descartar | False | orcamento_enumeracao | 0 |  |  | 18792356 | 232283314 | 74962 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 3 |  |  | 130356628 | 362639942 | 85566 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 130359028 | 492998970 | 96169 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 37520249 | 530519219 | 106251 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 37520276 | 568039495 | 116332 |  |  |  |  |

Abstrações (todas proveniência 'descoberta'):

| nome | categoria | tipo | corpo | método | origem | reutilizações |
|---|---|---|---|---|---|---|
| abs1 | descoberta | Grade → L Pos → L Pos | λg1. filtrar@P (celula g1) | fechamento | vizPretos, pretasDe |  |

### L-lib+f@E0

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 61326 | 61326 | 229 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 5670168 | 5731494 | 1658 | 1.000 |  |  | abs1 = λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2) (promocao-solucao) |
| ParAdjacente | False | orcamento_enumeracao | 0 |  |  | 38450326 | 44181820 | 11737 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 38450660 | 82632480 | 21816 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 34334708 | 116967188 | 32879 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 34349474 | 151316662 | 43943 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 26889287 | 178205949 | 54741 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 38450467 | 216656416 | 64821 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 35003 | 216691419 | 64917 | 1.000 |  |  | abs2 = λg1. filtrar@P (celula g1) (promocao-solucao) |
| descartar | False | orcamento_enumeracao | 0 |  |  | 18809842 | 235501261 | 75238 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 3 |  |  | 130393127 | 365894388 | 85842 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 130395527 | 496289915 | 96445 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 28479196 | 524769111 | 106535 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 28479274 | 553248385 | 116624 |  |  |  |  |

Abstrações (todas proveniência 'descoberta'):

| nome | categoria | tipo | corpo | método | origem | reutilizações |
|---|---|---|---|---|---|---|
| abs1 | descoberta | Grade → Pos → L Pos | λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2) | promocao-solucao | vizPretos |  |
| abs2 | descoberta | Grade → L Pos → L Pos | λg1. filtrar@P (celula g1) | promocao-solucao | pretasDe |  |

### L-fix@E0mais

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 82731 | 82731 | 233 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 8563534 | 8646265 | 1974 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 0 |  |  | 41052591 | 49698856 | 12053 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 41052930 | 90751786 | 22132 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 97282917 | 188034703 | 33558 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 97524734 | 285559437 | 44985 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 59632592 | 345192029 | 55779 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 41052747 | 386244776 | 65859 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 83461 | 386328237 | 65963 | 1.000 |  |  |  |
| descartar | False | orcamento_enumeracao | 0 |  |  | 74585577 | 460913814 | 76453 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 4 |  |  | 80629491 | 541543305 | 86704 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 1 |  |  | 80628746 | 622172051 | 96952 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 41052853 | 663224904 | 107032 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 41052868 | 704277772 | 117111 |  |  |  |  |

### L-lib@E0mais

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 82779 | 82779 | 233 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 8563681 | 8646460 | 1974 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 0 |  |  | 41052591 | 49699051 | 12053 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 41052930 | 90751981 | 22132 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 97282917 | 188034898 | 33558 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 97524734 | 285559632 | 44985 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 59632592 | 345192224 | 55779 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 41052747 | 386244971 | 65859 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 83834 | 386328805 | 65963 | 1.000 |  |  | abs1 = λg1. filtrar@P (celula g1) (fechamento) |
| descartar | False | orcamento_enumeracao | 0 |  |  | 74556151 | 460884956 | 76453 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 4 |  |  | 80658081 | 541543037 | 86704 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 1 |  |  | 80657336 | 622200373 | 96952 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 38281804 | 660482177 | 107043 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 38281819 | 698763996 | 117133 |  |  |  |  |

Abstrações (todas proveniência 'descoberta'):

| nome | categoria | tipo | corpo | método | origem | reutilizações |
|---|---|---|---|---|---|---|
| abs1 | descoberta | Grade → L Pos → L Pos | λg1. filtrar@P (celula g1) | fechamento | vizPretos, pretasDe |  |

### Comparação a custo cumulativo igual (reutilizações)

Nenhuma solução aceita reutilizou abstração descoberta; nada a comparar.

## Fase 7 — decisão

**Decisão (braços do protocolo): NO-GO**

Decisão se a variante L-lib+f contasse: NO-GO

- alcance sintático falha em E0 para ['passo', 'fecho', 'UmComponente', 'descartar', 'PrimeiraUltimaIguais', 'LinhasIguais']
- condição E0+ não satisfeita (só laços falham em E0: False; E0+: False; E0'+: None — None = não medido)
- abstrações foram descobertas, mas NENHUMA foi reutilizada numa solução aceita posterior

Decisão de viabilidade do piloto exploratório (documento 03, seção 10 + exigência de descoberta e reutilização autônomas); não é resultado científico.

## Separação do confirmatório (U27)

Semente 10001 no intervalo do piloto: True; partições disjuntas: True; grades no confirmatório: **0**.

| conjunto | grades | hash |
|---|---|---|
| contraexemplos:L-fix@E0 | 3 | e8428d6dc65abaa7 |
| contraexemplos:L-fix@E0mais | 3 | e8428d6dc65abaa7 |
| contraexemplos:L-lib+f@E0 | 3 | e8428d6dc65abaa7 |
| contraexemplos:L-lib@E0 | 3 | e8428d6dc65abaa7 |
| contraexemplos:L-lib@E0mais | 3 | e8428d6dc65abaa7 |
| desenho:DoisSeparados:n=3 | 56 | 3039417d6b013834 |
| desenho:DoisSeparados:n=4 | 200 | b8361eec7efdcf2d |
| desenho:DoisSeparados:n=5 | 200 | 66525d01d6317cc3 |
| desenho:DoisSeparados:n=6 | 200 | 3a4207b8ef48a9ff |
| desenho:Igual_linha1_linhaN:n=3 | 64 | ca8cf71a52869b1b |
| desenho:Igual_linha1_linhaN:n=4 | 200 | 944595ce96c13881 |
| desenho:Igual_linha1_linhaN:n=5 | 200 | 65eda473021f752c |
| desenho:Igual_linha1_linhaN:n=6 | 200 | af68545e0918ecbc |
| desenho:LinhasIguais:n=3 | 14 | 63701ab75e948a63 |
| desenho:LinhasIguais:n=4 | 200 | 33e302512c298770 |
| desenho:LinhasIguais:n=5 | 200 | 1aca6946dbee5169 |
| desenho:LinhasIguais:n=6 | 200 | 7d64738bf8edcf60 |
| desenho:NenhumaIsolada:n=3 | 86 | 5aab312c3ff18394 |
| desenho:NenhumaIsolada:n=4 | 200 | 6f1d7cbf46bfbafb |
| desenho:NenhumaIsolada:n=5 | 200 | ae4f85085da29774 |
| desenho:NenhumaIsolada:n=6 | 200 | 0ca057faadc2f614 |
| desenho:ParAdjacente:n=3 | 134 | 804c9725daaff770 |
| desenho:ParAdjacente:n=4 | 200 | 3791acc4d03c407f |
| desenho:ParAdjacente:n=5 | 200 | 1ac8ded753bdab98 |
| desenho:ParAdjacente:n=6 | 200 | 31de86a8a412102a |
| desenho:TodosMesmoTamanho:n=3 | 66 | d5fd99b772ceb205 |
| desenho:TodosMesmoTamanho:n=4 | 200 | 9fe253fd140f51a3 |
| desenho:TodosMesmoTamanho:n=5 | 200 | 0083282807906593 |
| desenho:TodosMesmoTamanho:n=6 | 200 | c5cb4a3d8fcc78a2 |
| desenho:UmComponente:n=3 | 66 | 3cd561720ffdc42a |
| desenho:UmComponente:n=4 | 200 | f6e6d45e9c2ac51a |
| desenho:UmComponente:n=5 | 200 | ad29874aab68e77f |
| desenho:UmComponente:n=6 | 200 | 4e6368cacbf38f80 |
| oe:grades_amostra_oe | 36 | b70b6d624e498365 |
| pm11:grades | 144 | 11e13c0b1dcf1da7 |
| tarefa:ExistePreta:exemplos | 3 | 98c16ae5c5a8eb2c |
| tarefa:ExistePreta:reservatorio_oraculo | 80 | 483f4730deb5acaf |
| tarefa:ExistePreta:teste | 30 | fff8ff71e87862f4 |
| tarefa:LinhasIguais:exemplos | 4 | 0b5a36ad807932eb |
| tarefa:LinhasIguais:reservatorio_oraculo | 193 | 4c1c9d263b61f180 |
| tarefa:LinhasIguais:teste | 30 | de8983ccf7445ada |
| tarefa:NenhumaIsolada:exemplos | 4 | 507d3c6123639f8c |
| tarefa:NenhumaIsolada:reservatorio_oraculo | 240 | 4b8dc326166e2c43 |
| tarefa:NenhumaIsolada:teste | 30 | 2af3839722a2151a |
| tarefa:ParAdjacente:exemplos | 4 | 07d04eea1364ab08 |
| tarefa:ParAdjacente:reservatorio_oraculo | 141 | 3642c3cb5d94b5b0 |
| tarefa:ParAdjacente:teste | 29 | c7534ef38f36e626 |
| tarefa:PrimeiraUltimaIguais:exemplos | 4 | 595a28e761560cfc |
| tarefa:PrimeiraUltimaIguais:reservatorio_oraculo | 240 | 475e4e7ff3f7cda5 |
| tarefa:PrimeiraUltimaIguais:teste | 30 | 3785ab33ae7e92ec |
| tarefa:UmComponente:exemplos | 4 | ea64784231cb3c15 |
| tarefa:UmComponente:reservatorio_oraculo | 223 | 33c72de26cd87b0f |
| tarefa:UmComponente:teste | 30 | d4855c2c9d1a87b8 |
| tarefa:componenteDe:exemplos | 4 | 50ab31c086f451b2 |
| tarefa:componenteDe:reservatorio_oraculo | 40 | 0900644b9abb9819 |
| tarefa:componenteDe:teste | 30 | a557fc7373088419 |
| tarefa:descartar:exemplos | 0 | e3b0c44298fc1c14 |
| tarefa:descartar:reservatorio_oraculo | 40 | f39e11c4949cf54f |
| tarefa:descartar:teste | 0 | e3b0c44298fc1c14 |
| tarefa:fecho:exemplos | 4 | 490c04d8da40e91f |
| tarefa:fecho:reservatorio_oraculo | 40 | ada70f5498285c24 |
| tarefa:fecho:teste | 30 | 1cd2d62291ff82e3 |
| tarefa:mesmoNumero:exemplos | 0 | e3b0c44298fc1c14 |
| tarefa:mesmoNumero:reservatorio_oraculo | 40 | 826e6bdbaca6e1b3 |
| tarefa:mesmoNumero:teste | 0 | e3b0c44298fc1c14 |
| tarefa:noMaximo:exemplos | 0 | e3b0c44298fc1c14 |
| tarefa:noMaximo:reservatorio_oraculo | 40 | 6dd91ea7464543a8 |
| tarefa:noMaximo:teste | 0 | e3b0c44298fc1c14 |
| tarefa:passo:exemplos | 4 | 0adbf0938aea80df |
| tarefa:passo:reservatorio_oraculo | 40 | b42e04de13b8073c |
| tarefa:passo:teste | 30 | e03ff654a2123c30 |
| tarefa:pretasDe:exemplos | 4 | 9264f9ba63a9ef0f |
| tarefa:pretasDe:reservatorio_oraculo | 40 | 3568659f13e5f78e |
| tarefa:pretasDe:teste | 30 | 760ee2c694fead9d |
| tarefa:vizPretos:exemplos | 4 | 84ab9da7ca49cc11 |
| tarefa:vizPretos:reservatorio_oraculo | 40 | ecf5927a32836bd0 |
| tarefa:vizPretos:teste | 30 | de01ad928fa43e3d |

## Desvios declarados

- Piloto exploratório com orçamentos reduzidos para caber em ~2 h de CPU (documento 03, seção 8 previa até ~100 h): PM1 com amostras por n de 5 a 9 reduzidas (documento: 10^5); PM2-PM5 com k pares reduzido (documento: >= 1000 pares); PM6 com Monte Carlo reduzido; s_reach medido até B = 10^5 (documento: 10^6) e só para os pares (base, contexto) listados em alcance_completos, os demais até 10^4; s_reach dos tipos fechados das tarefas só até alcance_fechado_B; execução autônoma com B_tarefa por tarefa (documento: B_max = 10^6) e sem L-mem nem controles.
- Memória: a primeira execução completa foi abortada porque um trabalhador da medição de alcance em E0+ a B = 10^5 passou de 8 GB e foi morto pelo OOM do cgroup (limite de 14,3 GB para todos os processos). Na execução registrada, cada trabalhador tem RLIMIT_AS = memoria_trabalhador_gb; um MemoryError encerra a medição e fica registrado (limitado_por_memoria), e só os pares de alcance_completos vão a 10^5.
- B_max da regra de decisão (documento 03, seção 10: 10^6) substituído pelo maior orçamento medido; E0'+ não tem s_reach medido nesta escala, logo a condição 'vale em E0+ e E0'+' não pode ser confirmada e é reportada como não verificada.
