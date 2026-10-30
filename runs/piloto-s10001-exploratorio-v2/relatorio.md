# Piloto exploratório — registros determinísticos (semente 10001, escala exploratoria-reduzida)

Nenhuma alegação científica: dados e hiperparâmetros expostos (documento 03, seção 0). Medições reais (tempo, memória, vazão PM9, latência PM13, custo PM16, I3/I6) ficam em `medicoes.md`.

Código: SHA-256 das fontes de fedro_piloto/ = `9d0e41dedebb9e59` (Python 3.13.17; por arquivo em config.json/deterministico.json).

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

PM6: 256 comparações com a auditoria; fora de 3 DP: 0.

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

Tabela 'curada' = dsl.BASES (instâncias escolhidas a partir da escada: desvio declarado); 'sistematica' = dsl.BASES_SISTEMATICAS (critério fixado sem olhar a escada); 'anteriores:X' = base + degraus manuais anteriores a X (modo auditoria). D = profundidade λ máxima. s_reach None = não determinado (limite de memória; ver medicoes).

| classe | base | contexto/tipo | tabela | D | s_reach(B) | s_reach só alvo | s_completo | esgotado |
|---|---|---|---|---|---|---|---|---|
| contexto | E0 | {g} → Bool | curada | 2 | {'10000': 7, '100000': 9} | {'10000': 9, '100000': 9} | 9 | True |
| contexto | E0 | {g} → L Pos | curada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0 | {g, S: L Pos} → L Pos | curada | 2 | {'10000': 6, '100000': None} | {'10000': 7, '100000': None} |  |  |
| fechado | E0 | fechado Grade → Bool | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0 | fechado Grade → Pos → L Pos | curada | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| fechado | E0 | fechado Grade → L Pos → L Pos | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0 | fechado L Pos → L Pos → L Pos | curada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0 | fechado L Pos → L Pos → Bool | curada | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0p | {g} → Bool | curada | 2 | {'10000': 8, '100000': 10} | {'10000': 10, '100000': 10} | 10 | True |
| contexto | E0p | {g} → L Pos | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0p | {g, S: L Pos} → L Pos | curada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0p | fechado Grade → Bool | curada | 2 | {'10000': 10} | {'10000': 10} | 10 | True |
| fechado | E0p | fechado Grade → Pos → L Pos | curada | 2 | {'10000': 11} | {'10000': 11} | 11 | True |
| fechado | E0p | fechado Grade → L Pos → L Pos | curada | 2 | {'10000': 10} | {'10000': 10} | 10 | True |
| fechado | E0p | fechado L Pos → L Pos → L Pos | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0p | fechado L Pos → L Pos → Bool | curada | 2 | {'10000': 10} | {'10000': 10} | 10 | True |
| contexto | E0mais | {g} → Bool | curada | 2 | {'10000': 7, '100000': 9} | {'10000': 9, '100000': 9} | 9 | True |
| contexto | E0mais | {g} → L Pos | curada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0mais | {g, S: L Pos} → L Pos | curada | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0mais | fechado Grade → Bool | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0mais | fechado Grade → Pos → L Pos | curada | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| fechado | E0mais | fechado Grade → L Pos → L Pos | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | curada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0mais | fechado L Pos → L Pos → Bool | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0pmais | {g} → Bool | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0pmais | {g} → L Pos | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0pmais | {g, S: L Pos} → L Pos | curada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0pmais | fechado Grade → Bool | curada | 2 | {'10000': 10} | {'10000': 10} | 10 | True |
| fechado | E0pmais | fechado Grade → Pos → L Pos | curada | 2 | {'10000': 11} | {'10000': 11} | 11 | True |
| fechado | E0pmais | fechado Grade → L Pos → L Pos | curada | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| fechado | E0pmais | fechado L Pos → L Pos → L Pos | curada | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0pmais | fechado L Pos → L Pos → Bool | curada | 2 | {'10000': 10} | {'10000': 10} | 10 | True |
| contexto | E0 | {g} → Bool | sistematica | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0 | {g} → L Pos | sistematica | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| contexto | E0 | {g, S: L Pos} → L Pos | sistematica | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0 | fechado Grade → Bool | sistematica | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0 | fechado Grade → Pos → L Pos | sistematica | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| fechado | E0 | fechado Grade → L Pos → L Pos | sistematica | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0 | fechado L Pos → L Pos → L Pos | sistematica | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0 | fechado L Pos → L Pos → Bool | sistematica | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0mais | {g} → Bool | sistematica | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| contexto | E0mais | {g} → L Pos | sistematica | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| contexto | E0mais | {g, S: L Pos} → L Pos | sistematica | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0mais | fechado Grade → Bool | sistematica | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0mais | fechado Grade → Pos → L Pos | sistematica | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| fechado | E0mais | fechado Grade → L Pos → L Pos | sistematica | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | sistematica | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0mais | fechado L Pos → L Pos → Bool | sistematica | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0p | fechado Grade → Pos → L Pos | curada | 4 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0p | {g, S: L Pos} → L Pos | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0p | fechado Grade → L Pos → L Pos | curada | 4 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0p | {g} → Bool | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0p | fechado L Pos → L Pos → L Pos | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0pmais | fechado Grade → Pos → L Pos | curada | 4 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0pmais | {g, S: L Pos} → L Pos | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0pmais | {g} → Bool | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0pmais | fechado L Pos → L Pos → L Pos | curada | 4 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0 | fechado Grade → Pos → L Pos | anteriores:vizPretos | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0 | {g} → Bool | anteriores:ParAdjacente | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0 | {g} → Bool | anteriores:NenhumaIsolada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0 | {g, S: L Pos} → L Pos | anteriores:passo | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0 | fechado Grade → L Pos → L Pos | anteriores:fecho | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0 | fechado Grade → Pos → L Pos | anteriores:componenteDe | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0 | {g} → Bool | anteriores:UmComponente | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0 | {g, S: L Pos} → L Pos | anteriores:pretasDe | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0 | fechado L Pos → L Pos → L Pos | anteriores:descartar | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0 | fechado L Pos → L Pos → Bool | anteriores:noMaximo | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0 | fechado L Pos → L Pos → Bool | anteriores:mesmoNumero | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0 | {g} → Bool | anteriores:PrimeiraUltimaIguais | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| contexto | E0 | {g} → Bool | anteriores:LinhasIguais | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0mais | fechado Grade → Pos → L Pos | anteriores:vizPretos | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0mais | {g} → Bool | anteriores:ParAdjacente | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0mais | {g} → Bool | anteriores:NenhumaIsolada | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0mais | {g, S: L Pos} → L Pos | anteriores:passo | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0mais | fechado Grade → L Pos → L Pos | anteriores:fecho | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| fechado | E0mais | fechado Grade → Pos → L Pos | anteriores:componenteDe | 2 | {'10000': 9} | {'10000': 9} | 9 | True |
| contexto | E0mais | {g} → Bool | anteriores:UmComponente | 2 | {'10000': 7} | {'10000': 7} | 7 | True |
| contexto | E0mais | {g, S: L Pos} → L Pos | anteriores:pretasDe | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0mais | fechado L Pos → L Pos → L Pos | anteriores:descartar | 4 | {'10000': 6} | {'10000': 6} | 6 | True |
| fechado | E0mais | fechado L Pos → L Pos → Bool | anteriores:noMaximo | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| fechado | E0mais | fechado L Pos → L Pos → Bool | anteriores:mesmoNumero | 2 | {'10000': 8} | {'10000': 8} | 8 | True |
| contexto | E0mais | {g} → Bool | anteriores:PrimeiraUltimaIguais | 2 | {'10000': 6} | {'10000': 6} | 6 | True |
| contexto | E0mais | {g} → Bool | anteriores:LinhasIguais | 2 | {'10000': 6} | {'10000': 6} | 6 | True |

### Auditoria da poda OE contra amostra independente (teste_int, baterias do ambiente; E0, D = 2)

Classe = denotação nas entradas da amostra independente. 'perdidas' = classes de tamanho mínimo s sem representante OE com essa denotação até s_max; 'atrasadas' = representadas só por termo maior.

| tipo | s_max | entradas | termos sem poda | representantes | classes | perdidas | atrasadas | perdidas por s (perdidas/novas) |
|---|---|---|---|---|---|---|---|---|
| Grade → Bool | 8 | 113 | 21733 | 69 | 56 | 2 | 0 | 2:0/2, 5:0/2, 6:0/4, 7:0/10, 8:2/38 |
| Grade → Pos → L Pos | 8 | 120 | 2672 | 216 | 214 | 2 | 0 | 1:0/1, 3:0/1, 4:0/2, 5:0/6, 6:0/18, 7:0/43, 8:2/143 |
| Grade → L Pos → L Pos | 8 | 120 | 17267 | 997 | 875 | 12 | 0 | 2:0/1, 3:0/2, 4:0/9, 5:0/23, 6:0/72, 7:1/189, 8:11/579 |
| L Pos → L Pos → L Pos | 7 | 120 | 7148 | 320 | 225 | 0 | 0 | 1:0/3, 2:0/3, 3:0/1, 4:0/6, 5:0/18, 6:0/59, 7:0/135 |
| L Pos → L Pos → Bool | 8 | 120 | 7930 | 207 | 163 | 8 | 2 | 2:0/1, 3:0/2, 4:0/4, 5:0/7, 6:0/13, 7:1/43, 8:7/93 |

## Fase 4 — viabilidade da escada (PM10)

Programas da escada são MANUAIS (manual-teste): só limites superiores de tamanho. B único = 10000. NenhumaIsolada usa a variante corrigida (o programa do documento discorda da referência na grade vazia). 'alcançável' = tamanho − binders do contexto ≤ s_reach(D adequado, tabela curada); colunas à direita: s_reach a D = 2 (gramática do aprendiz), com a tabela sistemática e com os degraus anteriores na tabela; 'conservador' usa o menor s_reach medido.

| degrau | base | programa | tam. c/ ant. | bruto | prof. λ (contexto) | D | fonte s_reach | s_reach(D) | alcançável | motivo | s_reach D=2 | s_reach sist. | s_reach c/ ant. na tabela | conservador |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | E0 | ExistePreta | 5 | 5 | 0 | 2 | {g} → Bool | 7 | True | alcançável | 7 | 7 |  | True |
| vizPretos | E0 | vizPretos | 8 | 8 | 2 | 2 | fechado Grade → Pos → L Pos | 9 | True | alcançável | 9 | 9 | 9 | True |
| ParAdjacente | E0 | ParAdjacente | 10 | 13 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 7 | 7 | False |
| NenhumaIsolada | E0 | NenhumaIsoladaCorrigida | 15 | 18 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 7 | 7 | False |
| passo | E0 | passo | 9 | 14 | 0 | 2 | {g, S: L Pos} → L Pos | 6 | False | acima de s_reach | 6 | 6 | 6 | False |
| fecho | E0 | fecho | 16 | 34 | 2 | 2 | fechado Grade → L Pos → L Pos | 8 | False | acima de s_reach | 8 | 7 | 8 | False |
| componenteDe | E0 | componenteDe | 7 | 38 | 2 | 2 | fechado Grade → Pos → L Pos | 9 | True | alcançável | 9 | 9 | 9 | True |
| UmComponente | E0 | UmComponente | 17 | 50 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 7 | 7 | False |
| pretasDe | E0 | pretasDe | 6 | 6 | 0 | 2 | {g, S: L Pos} → L Pos | 6 | True | alcançável | 6 | 6 | 6 | True |
| descartar | E0 | descartar | 13 | 13 | 2 | 2 | fechado L Pos → L Pos → L Pos | 7 | False | acima de s_reach | 7 | 7 | 7 | False |
| noMaximo | E0 | noMaximo | 6 | 18 | 2 | 2 | fechado L Pos → L Pos → Bool | 9 | True | alcançável | 9 | 8 | 8 | True |
| mesmoNumero | E0 | mesmoNumero | 9 | 35 | 2 | 2 | fechado L Pos → L Pos → Bool | 9 | True | alcançável | 9 | 8 | 8 | False |
| PrimeiraUltimaIguais | E0 | PrimeiraUltimaIguais | 13 | 49 | 0 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 7 | 6 | False |
| LinhasIguais | E0 | LinhasIguais | 14 | 51 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 7 | 6 | False |
| ExistePreta | E0p | ExistePreta | 5 | 5 | 0 | 2 | {g} → Bool | 8 | True | alcançável | 8 |  |  | True |
| vizPretos | E0p | vizPretos | 17 | 17 | 4 | 4 | fechado Grade → Pos → L Pos | 9 | False | acima de s_reach | 11 |  |  | False |
| ParAdjacente | E0p | ParAdjacente | 14 | 26 | 2 | 2 | {g} → Bool | 8 | False | acima de s_reach | 8 |  |  | False |
| NenhumaIsolada | E0p | NenhumaIsoladaCorrigida | 19 | 31 | 2 | 2 | {g} → Bool | 8 | False | acima de s_reach | 8 |  |  | False |
| passo | E0p | passo | 39 | 51 | 4 | 4 | {g, S: L Pos} → L Pos | 7 | False | acima de s_reach | 7 |  |  | False |
| fecho | E0p | fecho | 20 | 112 | 4 | 4 | fechado Grade → L Pos → L Pos | 8 | False | acima de s_reach | 10 |  |  | False |
| componenteDe | E0p | componenteDe | 7 | 116 | 2 | 2 | fechado Grade → Pos → L Pos | 11 | True | alcançável | 11 |  |  | True |
| UmComponente | E0p | UmComponente | 28 | 139 | 4 | 4 | {g} → Bool | 7 | False | acima de s_reach | 8 |  |  | False |
| pretasDe | E0p | pretasDe | 15 | 15 | 2 | 2 | {g, S: L Pos} → L Pos | 7 | False | acima de s_reach | 7 |  |  | False |
| descartar | E0p | descartar | 9 | 9 | 4 | 4 | fechado L Pos → L Pos → L Pos | 7 | False | acima de s_reach | 8 |  |  | False |
| noMaximo | E0p | noMaximo | 6 | 10 | 2 | 2 | fechado L Pos → L Pos → Bool | 10 | True | alcançável | 10 |  |  | True |
| mesmoNumero | E0p | mesmoNumero | 9 | 19 | 2 | 2 | fechado L Pos → L Pos → Bool | 10 | True | alcançável | 10 |  |  | True |
| PrimeiraUltimaIguais | E0p | PrimeiraUltimaIguais | 46 | 84 | 2 | 2 | {g} → Bool | 8 | False | acima de s_reach | 8 |  |  | False |
| LinhasIguais | E0p | LinhasIguais | 42 | 90 | 4 | 4 | {g} → Bool | 7 | False | acima de s_reach | 8 |  |  | False |
| ExistePreta | E0mais | ExistePreta | 5 | 5 | 0 | 2 | {g} → Bool | 7 | True | alcançável | 7 | 6 |  | True |
| vizPretos | E0mais | vizPretos | 8 | 8 | 2 | 2 | fechado Grade → Pos → L Pos | 9 | True | alcançável | 9 | 9 | 9 | True |
| ParAdjacente | E0mais | ParAdjacente | 10 | 13 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 6 | 7 | False |
| NenhumaIsolada | E0mais | NenhumaIsoladaCorrigida | 15 | 18 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 6 | 7 | False |
| passo | E0mais | passo | 9 | 14 | 0 | 2 | {g, S: L Pos} → L Pos | 6 | False | acima de s_reach | 6 | 6 | 6 | False |
| fecho | E0mais | fecho | 4 | 15 | 1 | 2 | fechado Grade → L Pos → L Pos | 8 | True | alcançável | 8 | 7 | 7 | True |
| componenteDe | E0mais | componenteDe | 7 | 19 | 2 | 2 | fechado Grade → Pos → L Pos | 9 | True | alcançável | 9 | 9 | 9 | True |
| UmComponente | E0mais | UmComponente | 17 | 31 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 6 | 7 | False |
| pretasDe | E0mais | pretasDe | 6 | 6 | 0 | 2 | {g, S: L Pos} → L Pos | 6 | True | alcançável | 6 | 6 | 6 | True |
| descartar | E0mais | descartar | 9 | 9 | 4 | 4 | fechado L Pos → L Pos → L Pos | 7 | False | acima de s_reach | 7 | 7 | 6 | False |
| noMaximo | E0mais | noMaximo | 6 | 10 | 2 | 2 | fechado L Pos → L Pos → Bool | 8 | True | alcançável | 8 | 8 | 8 | True |
| mesmoNumero | E0mais | mesmoNumero | 9 | 19 | 2 | 2 | fechado L Pos → L Pos → Bool | 8 | False | acima de s_reach | 8 | 8 | 8 | False |
| PrimeiraUltimaIguais | E0mais | PrimeiraUltimaIguais | 13 | 33 | 0 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 6 | 6 | False |
| LinhasIguais | E0mais | LinhasIguais | 14 | 35 | 1 | 2 | {g} → Bool | 7 | False | acima de s_reach | 7 | 6 | 6 | False |
| ExistePreta | E0pmais | ExistePreta | 5 | 5 | 0 | 2 | {g} → Bool | 8 | True | alcançável | 8 |  |  | True |
| vizPretos | E0pmais | vizPretos | 17 | 17 | 4 | 4 | fechado Grade → Pos → L Pos | 9 | False | acima de s_reach | 11 |  |  | False |
| ParAdjacente | E0pmais | ParAdjacente | 14 | 26 | 2 | 2 | {g} → Bool | 8 | False | acima de s_reach | 8 |  |  | False |
| NenhumaIsolada | E0pmais | NenhumaIsoladaCorrigida | 19 | 31 | 2 | 2 | {g} → Bool | 8 | False | acima de s_reach | 8 |  |  | False |
| passo | E0pmais | passo | 39 | 51 | 4 | 4 | {g, S: L Pos} → L Pos | 7 | False | acima de s_reach | 7 |  |  | False |
| fecho | E0pmais | fecho | 4 | 52 | 1 | 2 | fechado Grade → L Pos → L Pos | 9 | True | alcançável | 9 |  |  | True |
| componenteDe | E0pmais | componenteDe | 7 | 56 | 2 | 2 | fechado Grade → Pos → L Pos | 11 | True | alcançável | 11 |  |  | True |
| UmComponente | E0pmais | UmComponente | 28 | 79 | 4 | 4 | {g} → Bool | 7 | False | acima de s_reach | 8 |  |  | False |
| pretasDe | E0pmais | pretasDe | 15 | 15 | 2 | 2 | {g, S: L Pos} → L Pos | 7 | False | acima de s_reach | 7 |  |  | False |
| descartar | E0pmais | descartar | 9 | 9 | 4 | 4 | fechado L Pos → L Pos → L Pos | 7 | False | acima de s_reach | 8 |  |  | False |
| noMaximo | E0pmais | noMaximo | 6 | 10 | 2 | 2 | fechado L Pos → L Pos → Bool | 10 | True | alcançável | 10 |  |  | True |
| mesmoNumero | E0pmais | mesmoNumero | 9 | 19 | 2 | 2 | fechado L Pos → L Pos → Bool | 10 | True | alcançável | 10 |  |  | True |
| PrimeiraUltimaIguais | E0pmais | PrimeiraUltimaIguais | 46 | 84 | 2 | 2 | {g} → Bool | 8 | False | acima de s_reach | 8 |  |  | False |
| LinhasIguais | E0pmais | LinhasIguais | 42 | 90 | 4 | 4 | {g} → Bool | 7 | False | acima de s_reach | 8 |  |  | False |

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
| NenhumaIsoladaCorrigida | E0 | 303 | 0 | 0 |  |
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
| NenhumaIsoladaCorrigida | E0p | 47 | 0 | 0 |  |
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
| NenhumaIsoladaCorrigida | E0mais | 303 | 0 | 0 |  |
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
| NenhumaIsoladaCorrigida | E0pmais | 47 | 0 | 0 |  |

## Fase 5 — MECANISMO (modo mecanismo-teste; soluções MANUAIS; não é descoberta) — PM11

PM11 = alvo inserido pela compressão GULOSA (mecanismo de L-lib). 'no ranking' é diagnóstico: o alvo aparece entre os fragmentos candidatos (escolhido com conhecimento do alvo).

| alvo | fontes manuais | extraído (gulosa) | no ranking | posição | fragmento igual (ranking) | entradas gulosas (manual-teste) |
|---|---|---|---|---|---|---|
| vizPretos | ParAdjacente, NenhumaIsolada | False | True | 4 | λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2) | λf1 g2. f1 (λp3. nao (vazia?@P (filtrar@P (celula g2) (vizinhos g2 p3)))) (pretas g2) |
| passo | fecho | True | True | 1 | λl1 g2. uniao l1 (juntar (mapear@P>LP (λp3. filtrar@P (celula g2) (vizinhos g2 p3)) l1)) | λl1 g2. uniao l1 (juntar (mapear@P>LP (λp3. filtrar@P (celula g2) (vizinhos g2 p3)) l1)) |
| pretasDe | PrimeiraUltimaIguais, LinhasIguais | False | True | 11 | λg1. filtrar@P (celula g1) | λl1 l2. vazia?@P ((fix (λf3 l4 l5. se@LP (vazia?@P l4) l5 (f3 (cauda@P l4) (cauda@P l5)))) l1 l2); λg1 l2. filtrar@P (celula g1) (cabeca@LP l2); λl1 l2. e (abs1 l2 l1) (abs1 l1 l2) |

PM11 = 0.33 (alvo presente no ranking: 1.00); I4 disparada: True

## Fase 6 — EXECUÇÃO AUTÔNOMA (biblioteca vazia, modo autonomo)

Fechamento aritmético do livro-razão: True (diferença 0); PM14 (conciliação com contadores independentes): diferença **0** (0 divergências); hash do diário 16c362ee2b3e67ed.

PM12 (minimalidade do oráculo contra força bruta, n ≤ 4): 50/50 (50 com contraexemplo).

### L-fix@E0

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos (protocolo) cum. | enumeração cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 66976 | 66976 | 5 | 224 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 6308437 | 6375413 | 153 | 1505 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 2 |  |  | 32725404 | 39100817 | 224 | 11506 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 43437018 | 82537835 | 293 | 21507 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 36353145 | 118890980 | 1290 | 31508 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 36357731 | 155248711 | 2288 | 41509 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 32677341 | 187926052 | 2965 | 51510 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 43408979 | 231335031 | 3035 | 61511 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 39018 | 231374049 | 3040 | 61602 | 1.000 |  |  |  |
| descartar | False | orcamento_enumeracao | 0 |  |  | 18737539 | 250111588 | 3360 | 71603 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 3 |  |  | 130342348 | 380453936 | 3964 | 81604 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 130332198 | 510786134 | 4567 | 91605 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 43439543 | 554225677 | 4637 | 101606 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 43436966 | 597662643 | 4706 | 111607 |  |  |  |  |

### L-lib@E0

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos (protocolo) cum. | enumeração cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 67024 | 67024 | 5 | 224 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 6308584 | 6375608 | 153 | 1505 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 2 |  |  | 32725404 | 39101012 | 224 | 11506 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 43437018 | 82538030 | 293 | 21507 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 36353145 | 118891175 | 1290 | 31508 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 36357731 | 155248906 | 2288 | 41509 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 32677341 | 187926247 | 2965 | 51510 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 43408979 | 231335226 | 3035 | 61511 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 39391 | 231374617 | 3040 | 61602 | 1.000 |  |  | abs1 = λg1. filtrar@P (celula g1) (fechamento; descoberta) |
| descartar | False | orcamento_enumeracao | 0 |  |  | 18794754 | 250169371 | 3360 | 71603 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 3 |  |  | 130375547 | 380544918 | 3964 | 81604 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 130365397 | 510910315 | 4567 | 91605 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 43829555 | 554739870 | 4647 | 101606 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 43837660 | 598577530 | 4726 | 111607 |  |  |  |  |

Abstrações (proveniência 'descoberta', com certificado do laço do aprendiz):

| nome | categoria | tipo | corpo | método | origem | coincide com solução de | reutilizações |
|---|---|---|---|---|---|---|---|
| abs1 | descoberta | Grade → L Pos → L Pos | λg1. filtrar@P (celula g1) | fechamento | vizPretos, pretasDe | pretasDe |  |

### L-lib+f@E0

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos (protocolo) cum. | enumeração cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 67024 | 67024 | 5 | 224 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 6308610 | 6375634 | 153 | 1505 | 1.000 |  |  | abs1 = λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2) (promocao-solucao; descoberta) |
| ParAdjacente | False | orcamento_enumeracao | 3 |  |  | 23513277 | 29888911 | 224 | 11506 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 44804557 | 74693468 | 302 | 21507 |  |  |  |  |
| passo | False | orcamento_enumeracao | 0 |  |  | 37942244 | 112635712 | 1363 | 31508 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 37942477 | 150578189 | 2425 | 41509 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 29121753 | 179699942 | 3221 | 51510 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 44783450 | 224483392 | 3300 | 61511 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 39176 | 224522568 | 3305 | 61602 | 1.000 |  |  | abs2 = λg1. filtrar@P (celula g1) (promocao-solucao; descoberta) |
| descartar | False | orcamento_enumeracao | 0 |  |  | 18812225 | 243334793 | 3625 | 71603 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 3 |  |  | 130412047 | 373746840 | 4229 | 81604 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 130401897 | 504148737 | 4832 | 91605 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 33671455 | 537820192 | 4920 | 101606 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 33680104 | 571500296 | 5007 | 111607 |  |  |  |  |

Abstrações (proveniência 'descoberta', com certificado do laço do aprendiz):

| nome | categoria | tipo | corpo | método | origem | coincide com solução de | reutilizações |
|---|---|---|---|---|---|---|---|
| abs1 | promocao-solucao | Grade → Pos → L Pos | λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2) | promocao-solucao | vizPretos | vizPretos |  |
| abs2 | promocao-solucao | Grade → L Pos → L Pos | λg1. filtrar@P (celula g1) | promocao-solucao | pretasDe | pretasDe |  |

### L-fix@E0mais

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos (protocolo) cum. | enumeração cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 90778 | 90778 | 5 | 228 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 9283936 | 9374714 | 168 | 1806 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 2 |  |  | 41315384 | 50690098 | 248 | 11807 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 47952092 | 98642190 | 326 | 21808 |  |  |  |  |
| passo | False | orcamento_enumeracao | 1 |  |  | 104944726 | 203586916 | 1752 | 31809 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 105031218 | 308618134 | 3178 | 41810 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 62097299 | 370715433 | 3970 | 51811 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 47909296 | 418624729 | 4049 | 61812 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 94449 | 418719178 | 4054 | 61911 | 1.000 |  |  |  |
| descartar | False | orcamento_enumeracao | 0 |  |  | 74572094 | 493291272 | 4543 | 71912 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 2 |  |  | 80704511 | 573995783 | 4791 | 81913 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 80698457 | 654694240 | 5039 | 91914 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 47919766 | 702614006 | 5118 | 101915 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 47958288 | 750572294 | 5196 | 111916 |  |  |  |  |

### L-lib@E0mais

| tarefa | aceita | fim | rodadas | hipótese | tam. | custo aprendiz | cumulativo | candidatos (protocolo) cum. | enumeração cum. | acurácia teste | usa biblioteca | reutilizações | novas abstrações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ExistePreta | True | aceita | 1 | λx0. nao (vazia?@P (pretas x0)) | 5 | 90826 | 90826 | 5 | 228 | 1.000 |  |  |  |
| vizPretos | True | aceita | 1 | λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1) | 8 | 9284083 | 9374909 | 168 | 1806 | 1.000 |  |  |  |
| ParAdjacente | False | orcamento_enumeracao | 2 |  |  | 41315384 | 50690293 | 248 | 11807 |  |  |  |  |
| NenhumaIsolada | False | orcamento_enumeracao | 0 |  |  | 47952092 | 98642385 | 326 | 21808 |  |  |  |  |
| passo | False | orcamento_enumeracao | 1 |  |  | 104944726 | 203587111 | 1752 | 31809 |  |  |  |  |
| fecho | False | orcamento_enumeracao | 1 |  |  | 105031218 | 308618329 | 3178 | 41810 |  |  |  |  |
| componenteDe | False | orcamento_enumeracao | 0 |  |  | 62097299 | 370715628 | 3970 | 51811 |  |  |  |  |
| UmComponente | False | orcamento_enumeracao | 1 |  |  | 47909296 | 418624924 | 4049 | 61812 |  |  |  |  |
| pretasDe | True | aceita | 1 | λx0. filtrar@P (celula x0) | 4 | 94822 | 418719746 | 4054 | 61911 | 1.000 |  |  | abs1 = λg1. filtrar@P (celula g1) (fechamento; descoberta) |
| descartar | False | orcamento_enumeracao | 0 |  |  | 74542460 | 493262206 | 4543 | 71912 |  |  |  |  |
| noMaximo | False | orcamento_enumeracao | 2 |  |  | 80733123 | 573995329 | 4791 | 81913 |  |  |  |  |
| mesmoNumero | False | orcamento_enumeracao | 2 |  |  | 80727069 | 654722398 | 5039 | 91914 |  |  |  |  |
| PrimeiraUltimaIguais | False | orcamento_enumeracao | 1 |  |  | 44736717 | 699459115 | 5128 | 101915 |  |  |  |  |
| LinhasIguais | False | orcamento_enumeracao | 0 |  |  | 44769798 | 744228913 | 5216 | 111916 |  |  |  |  |

Abstrações (proveniência 'descoberta', com certificado do laço do aprendiz):

| nome | categoria | tipo | corpo | método | origem | coincide com solução de | reutilizações |
|---|---|---|---|---|---|---|---|
| abs1 | descoberta | Grade → L Pos → L Pos | λg1. filtrar@P (celula g1) | fechamento | vizPretos, pretasDe | pretasDe |  |

### Comparação a custo cumulativo TOTAL igual (reutilizações)

Nenhuma solução aceita reutilizou abstração descoberta; nada a comparar.

## Fase 7 — decisão

**Decisão (braços do protocolo, regra do documento 03): NO-GO**

Decisão conservadora (menor s_reach medido): NO-GO

Decisão se a variante L-lib+f contasse: NO-GO

Exigência autônoma por base (mín. 1 tarefa(s)): {'E0': False, 'E0mais': False}; E0': não verificada (sem braço E0' nesta escala)

- alcance sintático (D adequado, B único) falha em E0 para ['ParAdjacente', 'NenhumaIsolada', 'passo', 'fecho', 'UmComponente', 'descartar', 'PrimeiraUltimaIguais', 'LinhasIguais']
- E0': False (falhas: ['vizPretos', 'ParAdjacente', 'NenhumaIsolada', 'passo', 'fecho', 'UmComponente', 'pretasDe', 'descartar', 'PrimeiraUltimaIguais', 'LinhasIguais']; None = não medido ou limite inválido)
- condição E0+ não satisfeita (só laços falham em E0: False; E0+: False; E0'+: False — falhas E0+: ['ParAdjacente', 'NenhumaIsolada', 'passo', 'UmComponente', 'descartar', 'mesmoNumero', 'PrimeiraUltimaIguais', 'LinhasIguais'], E0'+: ['vizPretos', 'ParAdjacente', 'NenhumaIsolada', 'passo', 'UmComponente', 'pretasDe', 'descartar', 'PrimeiraUltimaIguais', 'LinhasIguais'])
- as abstrações 'descobertas' são todas cópias (α/η) de soluções de degraus; nenhuma compressão entre tarefas distintas
- abstrações foram descobertas, mas NENHUMA foi reutilizada numa solução aceita posterior
- exigência autônoma em E0: < 1 tarefa(s) com reutilização em L-lib@E0 e L-fix@E0 falhando a custo total igual
- exigência autônoma em E0+: < 1 tarefa(s) com reutilização em L-lib@E0mais e L-fix@E0mais falhando a custo total igual
- I4 (compressor) disparada: vizPretos não é extraído pela compressão gulosa

- Interrupção I4: {'disparada': True, 'motivo': 'compressão gulosa não extrai vizPretos de ParAdjacente + NenhumaIsolada (PM11 pela compressão efetiva)'}
- Interrupção I1_referencias: {'disparada': False, 'motivo': 'PM1 > 0 (discordância entre referências)'}
- Interrupção I1_livro: {'disparada': False, 'motivo': 'livro-razão não fecha ou não concilia com contadores independentes'}
- Interrupção I7_vazamento: {'disparada': False, 'motivo': 'grade do confirmatório usada pelo piloto (U27)'}

Decisão de viabilidade do piloto exploratório (documento 03, seção 10 + exigência de descoberta e reutilização autônomas por base); não é resultado científico. Condições de custo (I3, I6, PM16) em medicoes.json/medicoes.md.

## Separação do confirmatório (U27)

Semente 10001 no intervalo do piloto: True; partições disjuntas: True; grades no confirmatório: **0**.

| conjunto | grades | hash |
|---|---|---|
| auditoria_oe:Grade → Bool | 120 | faf2cacc4a7c38f7 |
| auditoria_oe:Grade → L Pos → L Pos | 24 | 7fceb54250450dbf |
| auditoria_oe:Grade → Pos → L Pos | 24 | 57b179c9684ba73c |
| auditoria_oe:L Pos → L Pos → Bool | 24 | 49966e3c3363e8e1 |
| auditoria_oe:L Pos → L Pos → L Pos | 24 | bb8ae7ff3b7b1a30 |
| contraexemplos:L-fix@E0 | 5 | 3c9b9f4d21568e00 |
| contraexemplos:L-fix@E0mais | 6 | bb921b294085d67c |
| contraexemplos:L-lib+f@E0 | 6 | e8fee0ea5bcbfb2e |
| contraexemplos:L-lib@E0 | 5 | 3c9b9f4d21568e00 |
| contraexemplos:L-lib@E0mais | 6 | bb921b294085d67c |
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
| oe:grades_amostra_oe | 36 | bd3ff55fee8ae23f |
| pm11:grades | 144 | 11e13c0b1dcf1da7 |
| tarefa:ExistePreta:exemplos | 3 | 60f2efe29f6e57c5 |
| tarefa:ExistePreta:exemplos_fonte | 0 | e3b0c44298fc1c14 |
| tarefa:ExistePreta:reservatorio_oraculo | 80 | fc17666eb5a8f364 |
| tarefa:ExistePreta:teste | 29 | b3e06bb6e149ecdf |
| tarefa:ExistePreta:teste_fonte | 29 | b3e06bb6e149ecdf |
| tarefa:LinhasIguais:exemplos | 4 | e4b8b5407a642372 |
| tarefa:LinhasIguais:exemplos_fonte | 0 | e3b0c44298fc1c14 |
| tarefa:LinhasIguais:reservatorio_oraculo | 196 | 9f9c14711b6d57ee |
| tarefa:LinhasIguais:teste | 29 | aed4fd4bfd258151 |
| tarefa:LinhasIguais:teste_fonte | 29 | aed4fd4bfd258151 |
| tarefa:NenhumaIsolada:exemplos | 4 | d09f0665dbc22ad5 |
| tarefa:NenhumaIsolada:exemplos_fonte | 0 | e3b0c44298fc1c14 |
| tarefa:NenhumaIsolada:reservatorio_oraculo | 240 | 6ee3f95262902cec |
| tarefa:NenhumaIsolada:teste | 30 | ca0316831b56c7a6 |
| tarefa:NenhumaIsolada:teste_fonte | 30 | ca0316831b56c7a6 |
| tarefa:ParAdjacente:exemplos | 4 | 71118402afa62839 |
| tarefa:ParAdjacente:exemplos_fonte | 0 | e3b0c44298fc1c14 |
| tarefa:ParAdjacente:reservatorio_oraculo | 149 | 229d01d7dde86ace |
| tarefa:ParAdjacente:teste | 30 | 58b5d31c5fd1c36c |
| tarefa:ParAdjacente:teste_fonte | 30 | 58b5d31c5fd1c36c |
| tarefa:PrimeiraUltimaIguais:exemplos | 4 | 224c8c56da42714a |
| tarefa:PrimeiraUltimaIguais:exemplos_fonte | 0 | e3b0c44298fc1c14 |
| tarefa:PrimeiraUltimaIguais:reservatorio_oraculo | 240 | 7fc1b5f1a8377da5 |
| tarefa:PrimeiraUltimaIguais:teste | 30 | 40f9e198c784f220 |
| tarefa:PrimeiraUltimaIguais:teste_fonte | 30 | 40f9e198c784f220 |
| tarefa:UmComponente:exemplos | 4 | 149bab05a73305b9 |
| tarefa:UmComponente:exemplos_fonte | 0 | e3b0c44298fc1c14 |
| tarefa:UmComponente:reservatorio_oraculo | 229 | df9fb753493815fa |
| tarefa:UmComponente:teste | 30 | 3ddd85cd786fba9d |
| tarefa:UmComponente:teste_fonte | 30 | 3ddd85cd786fba9d |
| tarefa:componenteDe:exemplos | 4 | d4b4fc8d12e38ddd |
| tarefa:componenteDe:exemplos_fonte | 4 | d4b4fc8d12e38ddd |
| tarefa:componenteDe:reservatorio_oraculo | 40 | 52c553c3cb66283f |
| tarefa:componenteDe:teste | 30 | a47e577d3c209517 |
| tarefa:componenteDe:teste_fonte | 30 | a47e577d3c209517 |
| tarefa:descartar:exemplos | 0 | e3b0c44298fc1c14 |
| tarefa:descartar:exemplos_fonte | 4 | b187347588f74528 |
| tarefa:descartar:reservatorio_oraculo | 40 | 792545e2598a702b |
| tarefa:descartar:teste | 0 | e3b0c44298fc1c14 |
| tarefa:descartar:teste_fonte | 30 | 687ad9cea673d1ff |
| tarefa:fecho:exemplos | 4 | 1c9aeee4d86de5e3 |
| tarefa:fecho:exemplos_fonte | 4 | 1c9aeee4d86de5e3 |
| tarefa:fecho:reservatorio_oraculo | 40 | d50a33eae8f43e4e |
| tarefa:fecho:teste | 30 | 4a993b50eb3cca40 |
| tarefa:fecho:teste_fonte | 30 | 4a993b50eb3cca40 |
| tarefa:mesmoNumero:exemplos | 0 | e3b0c44298fc1c14 |
| tarefa:mesmoNumero:exemplos_fonte | 4 | ac55da9b86dbc54e |
| tarefa:mesmoNumero:reservatorio_oraculo | 40 | f38851ba102b1dcd |
| tarefa:mesmoNumero:teste | 0 | e3b0c44298fc1c14 |
| tarefa:mesmoNumero:teste_fonte | 30 | a9755800eff52afb |
| tarefa:noMaximo:exemplos | 0 | e3b0c44298fc1c14 |
| tarefa:noMaximo:exemplos_fonte | 4 | befdc88f2d96d650 |
| tarefa:noMaximo:reservatorio_oraculo | 40 | 8d48e54fe3e8bc67 |
| tarefa:noMaximo:teste | 0 | e3b0c44298fc1c14 |
| tarefa:noMaximo:teste_fonte | 30 | 066193db63243899 |
| tarefa:passo:exemplos | 4 | b160b1bd6e8af919 |
| tarefa:passo:exemplos_fonte | 4 | b160b1bd6e8af919 |
| tarefa:passo:reservatorio_oraculo | 40 | ab250c06ab109919 |
| tarefa:passo:teste | 30 | 95ff58d8724bc022 |
| tarefa:passo:teste_fonte | 30 | 95ff58d8724bc022 |
| tarefa:pretasDe:exemplos | 4 | 145f661dafb22c77 |
| tarefa:pretasDe:exemplos_fonte | 4 | 145f661dafb22c77 |
| tarefa:pretasDe:reservatorio_oraculo | 40 | f9b13631a13a3481 |
| tarefa:pretasDe:teste | 30 | e860f840d591a203 |
| tarefa:pretasDe:teste_fonte | 30 | e860f840d591a203 |
| tarefa:vizPretos:exemplos | 4 | 3454bac3ad93b7a6 |
| tarefa:vizPretos:exemplos_fonte | 4 | 3454bac3ad93b7a6 |
| tarefa:vizPretos:reservatorio_oraculo | 40 | b7a6a14756af5751 |
| tarefa:vizPretos:teste | 30 | cb4c12f4d51996e9 |
| tarefa:vizPretos:teste_fonte | 30 | cb4c12f4d51996e9 |

## Desvios declarados

- Piloto exploratório com orçamentos reduzidos para caber em poucas horas de CPU (documento 03, seção 8 previa até ~100 h): PM1 com amostras por n de 5 a 9 reduzidas (documento: 10^5); PM2-PM5 com k pares reduzido (documento: >= 1000 pares); PM6 com Monte Carlo reduzido; s_reach medido até B = 10^5 (documento: 10^6) só para os pares (base, contexto) listados em alcance_completos, os demais até 10^4; execução autônoma com B_tarefa por tarefa (documento: B_max = 10^6) e sem L-mem nem controles.
- B_max da regra de decisão (documento 03, seção 10: 10^6) substituído por UM ÚNICO B = alcance_B_unico (10^4), medido em todos os contextos, tabelas e profundidades da tabela PM10 (antes: o maior B medido em cada contexto, misturando 10^5 e 10^4 entre degraus). A decisão é tomada a B = 10^4, não a 10^6: um NO-GO por alcance a 10^4 não implica NO-GO a 10^6.
- Memória: a primeira execução completa foi abortada porque um trabalhador da medição de alcance em E0+ a B = 10^5 passou de 8 GB e foi morto pelo OOM do cgroup. Cada trabalhador tem RLIMIT_AS = memoria_trabalhador_gb (agora parte da configuração) e roda num processo novo por job (maxtasksperchild=1). Um MemoryError torna o resultado INCONCLUSIVO: o ponto de parada e os contadores ao parar vão para medicoes.json (bloco dependente_de_recurso); no determinístico ficam só os s_reach(B) já determinados e o prefixo do histórico até o maior desses B.
- CURADORIA DA TABELA DE PRIMITIVAS (achado de revisão): as instâncias monomórficas de dsl.INSTANCIAS foram escolhidas com base nos programas da escada ("o MÍNIMO exigido"), o que recorta o espaço de busca com conhecimento das soluções manuais e não vale para F4 nem para o distrator C6. O documento 02, 2.3.2, define primitivas polimórficas. A curadoria é mantida nos braços da fase 6 e nas medições principais, e o seu efeito é medido: s_reach e PM10 também com dsl.BASES_SISTEMATICAS (critério fixado sem olhar a escada: elementos em {Pos, L Pos}, valores em {Bool, Pos, L Pos, L (L Pos)}), em alcance_sistematica_bases, a B único; a diferença está nas colunas 'sistemática' da tabela PM10.
- Profundidade λ (achado de revisão): com D = 2 os programas de E0' e E0'+ (profundidade 3 a 6) ficam fora da gramática para QUALQUER s_reach, o que tornava 'GO com E0' e 'GO com E0+' impossíveis por construção. A tabela PM10 passa a medir s_reach com D = max(2, profundidade do programa) (alcance_D_adequado_bases) e separa 'fora da gramática a D = 2' de 'acima de s_reach'. Os aprendizes da fase 6 continuam com D = 2 (E0, E0+: programas com anteriores têm profundidade ≤ 2, salvo descartar via dobraR em E0+, profundidade 4).
- PM10 com s_reach da tabela BASE é otimista (acrescentar constantes aumenta a ramificação): a coluna 'com anteriores' mede s_reach com os degraus anteriores (manuais, modo auditoria, nunca aprendiz) na tabela, em alcance_com_anteriores_bases; a decisão principal segue a regra literal do documento 03 (s_reach da base) e a decisão 'conservadora' usa o menor s_reach medido.
- E0'+ só tem s_reach a B único (10^4); 'vale em E0+ e E0'+' é avaliado a esse B.
- Livro-razão: busca_candidatos conta só candidatos NO SENTIDO DO PROTOCOLO (documento 03, 2.3); os candidatos internos do enumerador (poda OE) vão para o campo novo enumeracao_candidatos (e enumeracao_passos). B_tarefa limita SEPARADAMENTE cada um dos dois (candidatos do protocolo; candidatos da enumeração, cumulativos na tarefa, inclusive refinamentos OE). A comparação a custo igual usa o custo TOTAL do aprendiz (total_aprendiz: busca, enumeração, passos, compressão, consultas). Campos novos do ambiente: oraculo_passos_hipotese, geracao_rotulos.
- Poda OE (achado de revisão): os mundos OE da busca são a amostra fixa MAIS as grades dos exemplos e contraexemplos recebidos (enumerador.EstadoBusca, refinamento com re-enumeração). Contextos aninhados seguem com os primeiros mundos-raiz e tarefas L Pos → L Pos → · não têm grades: incompletude residual medida pela auditoria OE da fase 3 (classes perdidas por tamanho).
- Oráculos: hipótese indefinida (orçamento de passos esgotado) numa entrada conta como discordância (sem aceitação vácua).
