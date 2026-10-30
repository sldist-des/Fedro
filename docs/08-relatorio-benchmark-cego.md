# 08 — Relatório do benchmark cego

**Versão 0.1** — 2026-10-30 (em construção durante a execução dos blocos; a leitura final está em §7). Protocolo pré-registado: `benchmark/protocolo-avaliacao.md`. Contrato enviado ao autor: `benchmark/contrato-publico.md`. Registo de envio e receção: `benchmark/recebidos/REGISTO.md`.

Rótulos: **[E]** evidência dos registros, **[C]** procedimento, **[R]** requisito, **[A]** aberto, **[F]** falha.

---

## 1. Versões recebidas e integridade **[E]**

| versão | hash do pacote | congelado (autor) | recebido | validação | erros de integridade | tarefas inválidas no ambiente |
|---|---|---|---|---|---|---|
| grades-e0-independente v1 | `9e600a4155844bc44f5c815d451a209954b5b6194bf8e4b21ecf66dd658729f8` | 2026-10-30 17:29:27 UTC | 17:38 UTC, pela mensagem final da sessão `session_01Cs7W3uj1L2HYX9rKqMuDc4` (Claude Opus 5.5, sem repositório); os cinco ficheiros coincidem byte a byte com os SHA-256 do manifesto do autor | 0 erros, 3 avisos | nenhum comunicado | 0 (todas as 28 instanciáveis: exemplos iniciais formados em todos os braços) |

Uma única versão. Nenhum ficheiro do autor foi alterado. O código de referência importa só o módulo da grade. As notas seladas do autor (`notas-do-autor.md`) foram abertas na receção, depois da validação; contêm expectativas do autor que não alteraram o protocolo. Os avisos: `pretasEmDomino` tem positivos raros em grades naturais de n = 6 (o autor dá um gerador `POSITIVOS`); as testemunhas com `fix` usam `->`, que o validador do kit não reconhece como símbolo de E0 (falso positivo; §6).

O contentor desta sessão foi reciclado às 17:47 UTC, antes de qualquer tarefa do bloco A terminar; os blocos foram relançados do zero às 17:48 UTC e nenhum resultado parcial foi aproveitado (registo).

## 2. O conjunto do autor **[E]**

28 tarefas, os oito tipos aceites, na ordem de listagem do autor (a ordem da execução primária). O "nível" e o tamanho da testemunha são do autor (contagem dele, com dois ligadores por λ de dois parâmetros); os tamanhos pela nossa contagem estão em §6.

| # | tarefa | tipo | natureza | comparação | nível (autor) | tamanho da testemunha (autor) | descrição |
|---|---|---|---|---|---|---|---|
| 1 | ultimaLinha | `Grade -> L Pos` | funcao | exata | nivel1 | 5 | As posições da última linha (linha n), da esquerda para a direita. |
| 2 | contidoEm | `L Pos -> L Pos -> Bool` | funcao | exata | nivel1 | 6 | Verdadeiro se todo elemento de A ocorre em B (inclusão de conjuntos A ⊆ B). |
| 3 | vizinhosPretos | `Grade -> Pos -> L Pos` | funcao | conjunto | nivel1 | 8 | O conjunto dos vizinhos ortogonais de p (dentro da grade) que são pretos. |
| 4 | todaLinhaTemPreta | `Grade -> Bool` | predicado | exata | nivel1 | 7 | Verdadeiro se cada uma das n linhas contém pelo menos uma célula preta. |
| 5 | complementoDe | `Grade -> L Pos -> L Pos` | funcao | exata | nivel1 | 6 | Todas as posições da grade que não ocorrem em S, linha a linha. |
| 6 | pretasPorColunas | `Grade -> L Pos` | funcao | exata | nivel1 | 7 | As posições pretas por ordem de colunas: coluna 1 de cima para baixo, depois coluna 2, etc. |
| 7 | intersecaoOrdenada | `L Pos -> L Pos -> L Pos` | funcao | exata | nivel1 | 7 | Os elementos de A que também ocorrem em B, pela ordem (e com as repetições) de A. |
| 8 | contemTodasPretas | `Grade -> L Pos -> Bool` | funcao | exata | nivel1 | 7 | Verdadeiro se toda célula preta da grade ocorre em S. |
| 9 | colunaVazia | `Grade -> Bool` | predicado | exata | nivel1 | 8 | Verdadeiro se existe pelo menos uma coluna sem nenhuma célula preta. |
| 10 | naBorda | `Grade -> Pos -> Bool` | funcao | exata | nivel2 | 9 | Verdadeiro se p está na primeira ou última linha ou na primeira ou última coluna (equivalentemente: p tem menos de 4 vizinhos dentro da grade). |
| 11 | linhaDaPosicao | `Grade -> Pos -> L Pos` | funcao | exata | nivel1 | 8 | A linha que contém p: as posições (i, 1), …, (i, n) da esquerda para a direita, com i a linha de p. |
| 12 | juntarSemRepetir | `L Pos -> L Pos -> L Pos` | funcao | exata | nivel1 | 7 | B seguida dos elementos de A que não ocorrem em B, pela ordem de A (nota: difere da constante uniao, que põe os de B primeiro mas A no fim). |
| 13 | brancasDaLista | `Grade -> L Pos -> L Pos` | funcao | exata | nivel1 | 6 | Os elementos de S que são células brancas, pela ordem de S. |
| 14 | diferencaSimetrica | `L Pos -> L Pos -> L Pos` | funcao | conjunto | nivel2 | 9 | O conjunto das posições que ocorrem em exatamente uma das listas A e B. |
| 15 | pretasOrdemInversa | `Grade -> L Pos` | funcao | exata | nivel2 | 10 | As posições pretas por ordem inversa da leitura linha a linha (a última preta primeiro). |
| 16 | algumaLinhaCheia | `Grade -> Bool` | predicado | exata | nivel2 | 9 | Verdadeiro se existe uma linha com todas as células pretas. |
| 17 | linhaTemPretaEm | `Grade -> Pos -> Bool` | funcao | exata | nivel2 | 11 | Verdadeiro se a linha de p contém pelo menos uma célula preta (p pode ser branca). |
| 18 | semPretaIsolada | `Grade -> Bool` | predicado | exata | nivel2 | 11 | Verdadeiro se toda célula preta tem pelo menos um vizinho ortogonal preto (a grade toda branca é positiva). |
| 19 | colunasBrancas | `Grade -> L Pos` | funcao | exata | nivel2 | 11 | A concatenação, da esquerda para a direita, das colunas sem nenhuma preta, cada uma de cima para baixo. |
| 20 | mesmoConjunto | `L Pos -> L Pos -> Bool` | funcao | exata | nivel2 | 11 | Verdadeiro se A e B têm os mesmos elementos (igualdade de conjuntos, ignorando ordem e repetições). |
| 21 | tocaPreta | `Grade -> L Pos -> Bool` | funcao | exata | nivel2 | 11 | Verdadeiro se algum elemento de S tem um vizinho ortogonal preto (o próprio elemento pode ser de qualquer cor). |
| 22 | bordaPreta | `Grade -> L Pos` | funcao | exata | nivel2 | 12 | As células pretas que têm pelo menos um vizinho branco dentro da grade, linha a linha (os limites da grade não contam como branco). |
| 23 | vizinhancaExterna | `Grade -> L Pos -> L Pos` | funcao | conjunto | nivel2 | 12 | O conjunto das células pretas que não estão em S mas são vizinhas ortogonais de algum elemento de S. |
| 24 | semPretasAdjacentes | `Grade -> Bool` | predicado | exata | nivel2 | 12 | Verdadeiro se não há duas células pretas ortogonalmente vizinhas. |
| 25 | cruzDaPosicao | `Grade -> Pos -> L Pos` | funcao | conjunto | nivel3 | 15 | O conjunto das posições da linha de p e da coluna de p (a cruz centrada em p). |
| 26 | pretasEmDomino | `Grade -> Bool` | predicado | exata | nivel3 | 22 | Verdadeiro se toda célula preta tem exatamente um vizinho ortogonal preto, ou seja, as pretas formam dominós isolados (a grade toda branca é positiva). |
| 27 | pretasConexas | `Grade -> Bool` | predicado | exata | nivel4 | 37 | Verdadeiro se as células pretas formam um único componente 4-conexo (a grade toda branca é positiva). |
| 28 | componenteDe | `Grade -> Pos -> L Pos` | funcao | conjunto | nivel4 | 37 | O conjunto das células do componente 4-conexo de pretas que contém p; vazio se p é branca. |

Características declaradas pelo autor nas notas seladas (abertas na receção): ordem aproximadamente crescente em dificuldade; `grupo` = nível pelo tamanho da testemunha; cadeias de subtermos que o autor espera reaparecerem (linhaDaPosicao → linhaTemPretaEm → cruzDaPosicao; vizinhosPretos → semPretaIsolada → semPretasAdjacentes → pretasEmDomino; vizinhancaExterna → componenteDe); cinco tarefas com "armadilha de ordem" (comparação exata em listas); duas tarefas que exigem recursão (`fix`). Uma coincidência a assinalar: `vizinhosPretos` é a mesma operação que a primeira tarefa do currículo do documento 05, escolhida pelo autor sem acesso a ela; e `semPretaIsolada`/`semPretasAdjacentes` são variantes próximas de tarefas nossas. Isto é informação sobre a **naturalidade** destas operações no ambiente, não sobre independência (que está garantida pelo procedimento), e é tratada em §7.

## 3. Bloco A — modo zero, semente 10007, ordem do autor **[E]**

Oito braços (L-fix, L-lib, L-lib+f, L-lib+f/lesão × políticas tamanho e unigrama), biblioteca vazia no início, custo = só o benchmark. Lesão aplicada antes da tarefa de índice 14 (`pretasOrdemInversa`). Tabelas geradas por `analysis/relatorio_bx.py` a partir do registro:

<!-- TABELAS:A -->
### Registro `bx-grades-e0-independente-v1-A-s10007`

Pacote grades-e0-independente v1, hash `9e600a4155844bc4…`; semente 10007; B = 20000; modos ['zero']; k_reservatorio = 40; parede total 1998 s.

| braço | aceitas | custo prévio | custo benchmark | custo cumulativo | custo por aceita | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha | inválidas |
|---|---|---|---|---|---|---|---|---|---|
| zero/tamanho/L-fix | 15/28 | 0.0 M | 1882.3 M | 1882.3 M | 125.5 M | 0 | 0 (0) | True | 0 |
| zero/tamanho/L-lib | 16/28 | 0.0 M | 1674.8 M | 1674.8 M | 104.7 M | 2 | 3 (2) | True | 0 |
| zero/tamanho/L-lib+f | 15/28 | 0.0 M | 1540.8 M | 1540.8 M | 102.7 M | 5 | 19 (6) | True | 0 |
| zero/tamanho/L-lib+f/lesao | 15/28 | 0.0 M | 1859.8 M | 1859.8 M | 124.0 M | 3 | 1 (1) | True | 0 |
| zero/unigrama/L-fix | 17/28 | 0.0 M | 1865.5 M | 1865.5 M | 109.7 M | 0 | 0 (0) | True | 0 |
| zero/unigrama/L-lib | 18/28 | 0.0 M | 1529.5 M | 1529.5 M | 85.0 M | 3 | 7 (3) | True | 0 |
| zero/unigrama/L-lib+f | 17/28 | 0.0 M | 2514.5 M | 2514.5 M | 147.9 M | 6 | 21 (7) | True | 0 |
| zero/unigrama/L-lib+f/lesao | 17/28 | 0.0 M | 2609.3 M | 2609.3 M | 153.5 M | 3 | 3 (1) | True | 0 |

| comparação | positivas | negativas | neutras | inconclusivas | com reuso |
|---|---|---|---|---|---|
| zero/tamanho/L-lib+f vs zero/tamanho/L-fix | 4 | 13 | 0 | 11 | 5 |
| zero/unigrama/L-lib+f vs zero/unigrama/L-fix | 4 | 14 | 0 | 10 | 6 |

| lesão | tarefas após a lesão | aceitas L-lib+f | aceitas lesão | custo L-lib+f | custo lesão | entradas removidas | sensível |
|---|---|---|---|---|---|---|---|
| zero/tamanho/L-lib+f vs zero/tamanho/L-lib+f/lesao | 14 | 3 | 3 | 1277.8 M | 1596.7 M | 13 | True |
| zero/unigrama/L-lib+f vs zero/unigrama/L-lib+f/lesao | 14 | 4 | 4 | 2048.6 M | 2143.3 M | 14 | True |

Tarefas aceitas a custo cumulativo igual (para cada aceitação de L-lib+f ao custo C, aceitas de L-lib+f vs de L-fix com custo ≤ C):
- zero/tamanho/L-lib+f vs zero/tamanho/L-fix: ultimaLinha C=0.1 M → 1 vs 1; contidoEm C=0.9 M → 2 vs 2; vizinhosPretos C=8.2 M → 3 vs 3; todaLinhaTemPreta C=10.9 M → 4 vs 5; complementoDe C=11.0 M → 5 vs 5; pretasPorColunas C=13.2 M → 6 vs 7; intersecaoOrdenada C=15.0 M → 7 vs 7; contemTodasPretas C=15.1 M → 8 vs 7; naBorda C=107.8 M → 9 vs 13; linhaDaPosicao C=117.4 M → 10 vs 13; juntarSemRepetir C=132.4 M → 11 vs 13; brancasDaLista C=137.1 M → 12 vs 13; linhaTemPretaEm C=403.6 M → 13 vs 14; tocaPreta C=727.4 M → 14 vs 14; semPretasAdjacentes C=970.3 M → 15 vs 14
- zero/unigrama/L-lib+f vs zero/unigrama/L-fix: ultimaLinha C=0.1 M → 1 vs 1; contidoEm C=2.6 M → 2 vs 2; vizinhosPretos C=35.9 M → 3 vs 5; todaLinhaTemPreta C=44.8 M → 4 vs 6; complementoDe C=44.9 M → 5 vs 6; pretasPorColunas C=58.3 M → 6 vs 8; intersecaoOrdenada C=60.1 M → 7 vs 8; contemTodasPretas C=60.2 M → 8 vs 8; colunaVazia C=132.4 M → 9 vs 9; naBorda C=296.0 M → 10 vs 13; linhaDaPosicao C=307.8 M → 11 vs 14; juntarSemRepetir C=342.4 M → 12 vs 14; brancasDaLista C=347.1 M → 13 vs 14; linhaTemPretaEm C=656.4 M → 14 vs 15; mesmoConjunto C=977.2 M → 15 vs 15; tocaPreta C=1057.5 M → 16 vs 17; semPretasAdjacentes C=1452.2 M → 17 vs 17

Tarefa a tarefa (✔ aceita / ✘ não; custo em passos; tamanho da hipótese entre parênteses; classe de transferência com razão exata ×, ou limite inferior ≥× quando L-fix não aceita):

| tarefa | tamanho: L-lib+f | L-fix | classe | unigrama: L-lib+f | L-fix | classe |
|---|---|---|---|---|---|---|
| ultimaLinha | ✔ 0.1 M (5) | ✔ 0.1 M (5) | negativa ×1.00 | ✔ 0.1 M (5) | ✔ 0.1 M (5) | negativa ×1.00 |
| contidoEm | ✔ 0.9 M (6) | ✔ 0.9 M (6) | negativa ×1.00 | ✔ 2.5 M (6) | ✔ 2.5 M (6) | negativa ×1.00 |
| vizinhosPretos | ✔ 7.2 M (8) | ✔ 6.3 M (8) | negativa ×0.88 | ✔ 33.3 M (8) | ✔ 25.2 M (8) | negativa ×0.76 |
| todaLinhaTemPreta | ✔ 2.8 M (7) | ✔ 2.1 M (7) | negativa ×0.76 | ✔ 8.9 M (7) | ✔ 7.2 M (7) | negativa ×0.80 |
| complementoDe | ✔ 0.0 M (4) | ✔ 0.0 M (4) | negativa ×0.92 | ✔ 0.1 M (4) | ✔ 0.0 M (4) | negativa ×0.92 |
| pretasPorColunas | ✔ 2.2 M (7) | ✔ 1.9 M (7) | negativa ×0.86 | ✔ 13.4 M (7) | ✔ 9.5 M (7) | negativa ×0.71 |
| intersecaoOrdenada | ✔ 1.9 M (6) | ✔ 1.6 M (6) | negativa ×0.85 | ✔ 1.9 M (6) | ✔ 1.7 M (6) | negativa ×0.88 |
| contemTodasPretas | ✔ 0.1 M (4) reuso abs2 | ✔ 3.6 M (7) | positiva ×66.71 | ✔ 0.0 M (4) reuso abs2,abs5 | ✔ 5.2 M (7) | positiva ×305.34 |
| colunaVazia | ✘ 49.4 M | ✔ 24.0 M (8) | negativa | ✔ 72.3 M (8) | ✔ 21.6 M (8) | negativa ×0.30 |
| naBorda | ✔ 43.3 M (9) | ✔ 31.9 M (9) | negativa ×0.74 | ✔ 163.6 M (9) | ✔ 108.0 M (9) | negativa ×0.66 |
| linhaDaPosicao | ✔ 9.6 M (8) | ✔ 6.3 M (8) | negativa ×0.66 | ✔ 11.8 M (8) | ✔ 5.8 M (8) | negativa ×0.49 |
| juntarSemRepetir | ✔ 15.0 M (7) | ✔ 7.0 M (7) | negativa ×0.47 | ✔ 34.6 M (7) | ✔ 14.6 M (7) | negativa ×0.42 |
| brancasDaLista | ✔ 4.8 M (6) reuso abs4,abs7 | ✔ 0.8 M (6) | negativa ×0.16 | ✔ 4.7 M (6) reuso abs4,abs5,abs7 | ✔ 0.4 M (6) | negativa ×0.09 |
| diferencaSimetrica | ✘ 125.9 M | ✘ 89.6 M | inconclusiva | ✘ 118.8 M | ✔ 97.2 M (9) | negativa |
| pretasOrdemInversa | ✘ 57.3 M | ✘ 81.7 M | inconclusiva | ✘ 103.1 M | ✘ 128.1 M | inconclusiva |
| algumaLinhaCheia | ✘ 69.8 M | ✔ 71.5 M (9) | negativa | ✘ 83.5 M | ✘ 118.0 M | inconclusiva |
| linhaTemPretaEm | ✔ 13.4 M (8) reuso abs10 | ✘ 165.3 M | positiva ≥×12.3 | ✔ 3.9 M (8) reuso abs11 | ✔ 58.6 M (11) | positiva ×14.85 |
| semPretaIsolada | ✘ 94.2 M | ✘ 138.8 M | inconclusiva | ✘ 105.7 M | ✘ 133.0 M | inconclusiva |
| colunasBrancas | ✘ 71.9 M | ✘ 80.1 M | inconclusiva | ✘ 120.8 M | ✘ 122.6 M | inconclusiva |
| mesmoConjunto | ✘ 100.8 M | ✘ 199.4 M | inconclusiva | ✔ 94.2 M (9) reuso abs2,abs7 | ✔ 135.9 M (10) | positiva ×1.44 |
| tocaPreta | ✔ 56.9 M (8) reuso abs15 | ✔ 88.7 M (9) | positiva ×1.56 | ✔ 80.3 M (8) reuso abs3 | ✔ 34.2 M (9) | negativa ×0.43 |
| bordaPreta | ✘ 76.4 M | ✘ 81.7 M | inconclusiva | ✘ 144.1 M | ✘ 128.1 M | inconclusiva |
| vizinhancaExterna | ✘ 163.3 M | ✘ 111.3 M | inconclusiva | ✘ 246.1 M | ✘ 73.1 M | inconclusiva |
| semPretasAdjacentes | ✔ 3.3 M (6) reuso abs18 | ✘ 138.8 M | positiva ≥×41.7 | ✔ 4.5 M (6) reuso abs20,abs5 | ✘ 132.9 M | positiva ≥×29.3 |
| cruzDaPosicao | ✘ 186.7 M | ✘ 138.0 M | inconclusiva | ✘ 366.3 M | ✘ 120.1 M | inconclusiva |
| pretasEmDomino | ✘ 100.2 M | ✘ 138.8 M | inconclusiva | ✘ 167.3 M | ✘ 132.9 M | inconclusiva |
| pretasConexas | ✘ 97.0 M | ✘ 134.0 M | inconclusiva | ✘ 162.8 M | ✘ 128.8 M | inconclusiva |
| componenteDe | ✘ 186.5 M | ✘ 138.1 M | inconclusiva | ✘ 366.0 M | ✘ 120.2 M | inconclusiva |

Verificação pós-execução:

(verificação ainda não executada)
<!-- /TABELAS:A -->

### 3.1 Desempenho absoluto

| política | L-fix | L-lib | L-lib+f | L-lib+f/lesão |
|---|---|---|---|---|
| tamanho: tarefas aceitas (de 28) | 15 | **16** | 15 | 15 |
| tamanho: custo cumulativo | 1 882 M | 1 675 M | **1 541 M** | 1 860 M |
| unigrama: tarefas aceitas | 17 | **18** | 17 | 17 |
| unigrama: custo cumulativo | 1 866 M | **1 529 M** | 2 515 M | 2 609 M |

Em ambas as políticas, **nenhum braço passa de 18 tarefas**; as dez tarefas que nenhum braço resolve são as de nível 2 alto, 3 e 4 do autor (bordaPreta, colunasBrancas, pretasOrdemInversa, cruzDaPosicao, pretasEmDomino, pretasConexas, componenteDe, vizinhancaExterna, e, conforme a política, diferencaSimetrica, mesmoConjunto ou semPretaIsolada). As aceitas são as de testemunha ≤ 9 folhas pela contagem do autor e algumas de 10–12 (linhaTemPretaEm, semPretaIsolada, mesmoConjunto, tocaPreta, semPretasAdjacentes), exatamente a fronteira de alcance anunciada no contrato.

### 3.2 Vantagem relativa de L-lib+f sobre L-fix

| política | positivas | negativas | inconclusivas | com reutilização verificável | custo cumulativo L-lib+f / L-fix |
|---|---|---|---|---|---|
| tamanho | 4 | 13 | 11 | 5 | 0,82 |
| unigrama | 4 | 14 | 10 | 6 | 1,35 |

As quatro transferências positivas por política são as mesmas em espírito: `contemTodasPretas` (reutiliza `abs2 = λl₁ l₂. vazia?@P (diferenca l₁ l₂)`, promovida de `contidoEm`; razão exata ×66,7 e ×305), `linhaTemPretaEm` (reutiliza a promoção de `linhaDaPosicao`; L-fix falha na política de tamanho — razão mínima ≥ ×12 — e aceita com um programa de 11 folhas na unigrama, ×14,9), `semPretasAdjacentes` (reutiliza a promoção de `vizinhosPretos` através de uma entrada intermédia; L-fix falha nas duas políticas, razão mínima ≥ ×42 e ≥ ×29) e `tocaPreta` (×1,56 na política de tamanho) ou `mesmoConjunto` (×1,44, unigrama). Em todas elas a hipótese aceita usa uma entrada com certificado de descoberta criada **dentro** do benchmark, a partir de tarefas do autor: é reutilização verificável de operações adquiridas em tarefas que não preparámos.

As transferências negativas dominam em número. Lidas com uma tolerância de 5 % na razão de custo (critério **post hoc**, declarado aqui porque o pré-registro classifica como negativa qualquer razão < 1, e duas tarefas diferem em menos de 0,1 %), as "negativas" são: 2 equivalentes (ultimaLinha, contidoEm), 9 (tamanho) e 11 (unigrama) mais lentas com a mesma hipótese (razões 0,09–0,92; mediana 0,86 e 0,78 sobre as tarefas aceitas por ambos), e **2 tarefas perdidas** na política de tamanho (`algumaLinhaCheia`, `colunaVazia`: L-fix aceita, L-lib+f esgota o orçamento) e **1** na unigrama (`diferencaSimetrica`). A causa está nas bibliotecas: L-lib+f acumula 19 (tamanho) e 21 (unigrama) entradas, das quais só 6 e 7 são alguma vez reutilizadas; o resto são promoções de soluções que nunca mais servem e **cinco fragmentos triviais criados pela compressão por recorrência** (`λf g. f g`, `λf g p. f g p`), que são aplicações genéricas sem conteúdo e que a compressão aceitou porque ocorrem em ≥ 2 soluções. Cada entrada inútil alarga a gramática e empurra programas de 8–9 folhas para fora do orçamento. Este defeito do mecanismo de compressão (o critério de ocorrências não exclui fragmentos cuja única função é aplicar um argumento a outro) é um achado deste benchmark e fica registado como [F] para correção **depois** desta avaliação, nunca durante.

### 3.3 L-lib: a compressão por recorrência, sozinha, é o melhor braço

L-lib (sem promoção) aceita mais tarefas do que L-lib+f e L-fix nas duas políticas (16 e 18) com o menor custo na unigrama (1 529 M). As suas entradas são poucas (3 e 7) e duas delas são reutilizadas em tarefas que mais ninguém resolve no modo zero: `semPretaIsolada` (via `abs3 = λg f. todos@LP (algum@P (celula g)) (f g)`, fragmento comum a `todaLinhaTemPreta` e `colunaVazia`) e `mesmoConjunto` (via `abs2 = λl₁ l₂. vazia?@P (diferenca l₁ l₂)`, duas ocorrências). É a primeira vez em todo o programa que a compressão por recorrência produz uma entrada reutilizada (nos documentos 05 e 06 nunca disparou): o conjunto do autor, com 28 tarefas e vários pares que partilham subtermos, dá-lhe a estatística de que o nosso currículo de quatro degraus não dispunha. Isto responde parcialmente, e antes do tempo, à hipótese H-I1 do documento 07, e é discutido em §7.

### 3.4 Lesão

A lesão (13 e 14 entradas removidas antes da tarefa 15) não muda o número de tarefas aceitas nas 14 tarefas seguintes (3 e 4 em ambos os braços) mas muda **quais**: na política de tamanho, L-lib+f aceita `linhaTemPretaEm` e `semPretasAdjacentes` por reutilização e falha `algumaLinhaCheia`; o braço lesionado, com a gramática limpa, aceita `algumaLinhaCheia` e `semPretasAdjacentes` (reconstruindo a operação de vizinhança numa entrada nova) e falha `linhaTemPretaEm`. O custo nas tarefas pós-lesão é 25 % maior com lesão (tamanho) e 5 % maior (unigrama). A sensibilidade existe, mas é pequena e ambígua: a biblioteca removida continha tanto operações úteis como lastro.

## 4. Bloco B — modo prévio (cadeia do documento 05 incluída no custo) **[E]**

Seis braços (L-fix, L-lib+f, L-lib+f/lesão × duas políticas). Todos passam primeiro pelas três tarefas do documento 05 (vizPretos, expandir, ParAdjacente), que entram no custo cumulativo; L-lib+f chega ao benchmark com `abs1` (vizinhas pretas de uma posição) e `abs2` (vizinhas pretas de um conjunto); a lesão remove exatamente essas duas entradas antes da primeira tarefa do autor.

<!-- TABELAS:B -->
### Registro `bx-grades-e0-independente-v1-B-s10007`

Pacote grades-e0-independente v1, hash `9e600a4155844bc4…`; semente 10007; B = 20000; modos ['previo']; k_reservatorio = 40; parede total 1639 s.

| braço | aceitas | custo prévio | custo benchmark | custo cumulativo | custo por aceita | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha | inválidas |
|---|---|---|---|---|---|---|---|---|---|
| previo/tamanho/L-fix | 15/28 | 256.1 M | 1882.3 M | 2138.4 M | 142.6 M | 0 | 0 (0) | True | 0 |
| previo/tamanho/L-lib+f | 17/28 | 14.2 M | 1646.1 M | 1660.3 M | 97.7 M | 8 | 23 (9) | True | 0 |
| previo/tamanho/L-lib+f/lesao | 15/28 | 14.2 M | 1540.8 M | 1555.0 M | 103.7 M | 5 | 19 (6) | True | 0 |
| previo/unigrama/L-fix | 18/28 | 267.4 M | 2286.3 M | 2553.7 M | 141.9 M | 0 | 0 (0) | True | 0 |
| previo/unigrama/L-lib+f | 19/28 | 27.9 M | 1959.0 M | 1986.9 M | 104.6 M | 10 | 25 (10) | True | 0 |
| previo/unigrama/L-lib+f/lesao | 18/28 | 27.9 M | 1885.5 M | 1913.4 M | 106.3 M | 7 | 21 (8) | True | 0 |

| comparação | positivas | negativas | neutras | inconclusivas | com reuso |
|---|---|---|---|---|---|
| previo/tamanho/L-lib+f vs previo/tamanho/L-fix | 7 | 12 | 0 | 9 | 8 |
| previo/unigrama/L-lib+f vs previo/unigrama/L-fix | 9 | 11 | 0 | 8 | 10 |

| lesão | tarefas após a lesão | aceitas L-lib+f | aceitas lesão | custo L-lib+f | custo lesão | entradas removidas | sensível |
|---|---|---|---|---|---|---|---|
| previo/tamanho/L-lib+f vs previo/tamanho/L-lib+f/lesao | 28 | 17 | 15 | 1646.1 M | 1540.8 M | 2 | True |
| previo/unigrama/L-lib+f vs previo/unigrama/L-lib+f/lesao | 28 | 19 | 18 | 1959.0 M | 1885.5 M | 2 | True |

Tarefas aceitas a custo cumulativo igual (para cada aceitação de L-lib+f ao custo C, aceitas de L-lib+f vs de L-fix com custo ≤ C):
- previo/tamanho/L-lib+f vs previo/tamanho/L-fix: ultimaLinha C=14.3 M → 1 vs 0; contidoEm C=15.2 M → 2 vs 0; vizinhosPretos C=15.2 M → 3 vs 0; todaLinhaTemPreta C=19.3 M → 4 vs 0; complementoDe C=19.9 M → 5 vs 0; pretasPorColunas C=23.7 M → 6 vs 0; intersecaoOrdenada C=25.7 M → 7 vs 0; contemTodasPretas C=25.8 M → 8 vs 0; naBorda C=128.2 M → 9 vs 0; linhaDaPosicao C=138.8 M → 10 vs 0; juntarSemRepetir C=154.5 M → 11 vs 0; brancasDaLista C=161.4 M → 12 vs 0; linhaTemPretaEm C=443.9 M → 13 vs 13; semPretaIsolada C=457.5 M → 14 vs 13; tocaPreta C=655.2 M → 15 vs 14; vizinhancaExterna C=786.9 M → 16 vs 14; semPretasAdjacentes C=786.9 M → 17 vs 14
- previo/unigrama/L-lib+f vs previo/unigrama/L-fix: ultimaLinha C=32.4 M → 1 vs 0; contidoEm C=35.1 M → 2 vs 0; vizinhosPretos C=35.1 M → 3 vs 0; todaLinhaTemPreta C=40.6 M → 4 vs 0; complementoDe C=42.5 M → 5 vs 0; pretasPorColunas C=48.9 M → 6 vs 0; intersecaoOrdenada C=50.9 M → 7 vs 0; contemTodasPretas C=50.9 M → 8 vs 0; colunaVazia C=70.8 M → 9 vs 0; linhaDaPosicao C=179.7 M → 10 vs 0; juntarSemRepetir C=203.9 M → 11 vs 0; brancasDaLista C=209.5 M → 12 vs 0; diferencaSimetrica C=324.5 M → 13 vs 9; linhaTemPretaEm C=520.0 M → 14 vs 13; semPretaIsolada C=527.5 M → 15 vs 14; mesmoConjunto C=656.6 M → 16 vs 14; tocaPreta C=673.5 M → 17 vs 14; vizinhancaExterna C=857.1 M → 18 vs 15; semPretasAdjacentes C=857.1 M → 19 vs 15

Tarefa a tarefa (✔ aceita / ✘ não; custo em passos; tamanho da hipótese entre parênteses; classe de transferência com razão exata ×, ou limite inferior ≥× quando L-fix não aceita):

| tarefa | tamanho: L-lib+f | L-fix | classe | unigrama: L-lib+f | L-fix | classe |
|---|---|---|---|---|---|---|
| ultimaLinha | ✔ 0.1 M (5) | ✔ 0.1 M (5) | negativa ×0.76 | ✔ 4.5 M (5) | ✔ 2.3 M (5) | negativa ×0.52 |
| contidoEm | ✔ 0.9 M (6) | ✔ 0.9 M (6) | negativa ×1.00 | ✔ 2.6 M (6) | ✔ 2.6 M (6) | negativa ×1.00 |
| vizinhosPretos | ✔ 0.0 M (1) reuso abs1 | ✔ 6.3 M (8) | positiva ×17878.59 | ✔ 0.0 M (1) reuso abs1 | ✔ 1.1 M (8) | positiva ×2981.81 |
| todaLinhaTemPreta | ✔ 4.2 M (7) | ✔ 2.1 M (7) | negativa ×0.51 | ✔ 5.6 M (7) | ✔ 3.1 M (7) | negativa ×0.55 |
| complementoDe | ✔ 0.6 M (4) | ✔ 0.0 M (4) | negativa ×0.06 | ✔ 1.9 M (5) | ✔ 0.1 M (5) | negativa ×0.03 |
| pretasPorColunas | ✔ 3.8 M (7) | ✔ 1.9 M (7) | negativa ×0.49 | ✔ 6.4 M (7) | ✔ 3.2 M (7) | negativa ×0.49 |
| intersecaoOrdenada | ✔ 2.0 M (6) | ✔ 1.6 M (6) | negativa ×0.79 | ✔ 2.0 M (6) | ✔ 1.7 M (6) | negativa ×0.82 |
| contemTodasPretas | ✔ 0.1 M (4) reuso abs4 | ✔ 3.6 M (7) | positiva ×66.41 | ✔ 0.0 M (4) reuso abs4 | ✔ 1.5 M (7) | positiva ×43.67 |
| colunaVazia | ✘ 54.5 M | ✔ 24.0 M (8) | negativa | ✔ 19.9 M (7) reuso abs5 | ✔ 20.7 M (8) | positiva ×1.04 |
| naBorda | ✔ 47.9 M (9) | ✔ 31.9 M (9) | negativa ×0.67 | ✘ 97.2 M | ✔ 101.3 M (9) | negativa |
| linhaDaPosicao | ✔ 10.6 M (8) | ✔ 6.3 M (8) | negativa ×0.60 | ✔ 11.7 M (8) | ✔ 6.2 M (8) | negativa ×0.53 |
| juntarSemRepetir | ✔ 15.7 M (7) | ✔ 7.0 M (7) | negativa ×0.45 | ✔ 24.2 M (7) | ✔ 14.6 M (7) | negativa ×0.60 |
| brancasDaLista | ✔ 7.0 M (6) reuso abs5,abs8 | ✔ 0.8 M (6) | negativa ×0.11 | ✔ 5.5 M (6) reuso abs6,abs9 | ✔ 0.4 M (6) | negativa ×0.07 |
| diferencaSimetrica | ✘ 127.4 M | ✘ 89.6 M | inconclusiva | ✔ 115.1 M (9) | ✔ 97.3 M (9) | negativa ×0.85 |
| pretasOrdemInversa | ✘ 64.3 M | ✘ 81.7 M | inconclusiva | ✘ 98.5 M | ✘ 118.3 M | inconclusiva |
| algumaLinhaCheia | ✘ 75.4 M | ✔ 71.5 M (9) | negativa | ✘ 95.6 M | ✘ 132.6 M | inconclusiva |
| linhaTemPretaEm | ✔ 15.3 M (8) reuso abs11 | ✘ 165.3 M | positiva ≥×10.8 | ✔ 1.3 M (7) reuso abs12,abs5 | ✔ 54.5 M (11) | positiva ×42.33 |
| semPretaIsolada | ✔ 13.6 M (7) reuso abs2,abs9 | ✘ 138.8 M | positiva ≥×10.2 | ✔ 7.5 M (7) reuso abs10,abs2 | ✔ 57.6 M (10) | positiva ×7.65 |
| colunasBrancas | ✘ 75.0 M | ✘ 80.1 M | inconclusiva | ✘ 127.0 M | ✘ 113.7 M | inconclusiva |
| mesmoConjunto | ✘ 99.7 M | ✘ 199.4 M | inconclusiva | ✔ 2.1 M (6) reuso abs17 | ✔ 135.9 M (10) | positiva ×65.08 |
| tocaPreta | ✔ 22.9 M (7) reuso abs16,abs2 | ✔ 88.7 M (9) | positiva ×3.87 | ✔ 16.9 M (7) reuso abs2,abs5 | ✔ 30.3 M (9) | positiva ×1.80 |
| bordaPreta | ✘ 76.7 M | ✘ 81.7 M | inconclusiva | ✘ 146.3 M | ✘ 118.3 M | inconclusiva |
| vizinhancaExterna | ✔ 55.0 M (7) reuso abs2 | ✘ 111.3 M | positiva ≥×2.0 | ✔ 37.3 M (7) reuso abs2 | ✘ 158.1 M | positiva ≥×4.2 |
| semPretasAdjacentes | ✔ 0.1 M (4) reuso abs19 | ✘ 138.8 M | positiva ≥×2243.0 | ✔ 0.0 M (3) reuso abs20 | ✘ 170.2 M | positiva ≥×7378.5 |
| cruzDaPosicao | ✘ 325.9 M | ✘ 138.0 M | inconclusiva | ✘ 387.3 M | ✘ 316.6 M | inconclusiva |
| pretasEmDomino | ✘ 118.1 M | ✘ 138.8 M | inconclusiva | ✘ 175.6 M | ✘ 142.0 M | inconclusiva |
| pretasConexas | ✘ 108.6 M | ✘ 134.0 M | inconclusiva | ✘ 181.5 M | ✘ 165.2 M | inconclusiva |
| componenteDe | ✘ 321.0 M | ✘ 138.1 M | inconclusiva | ✘ 385.4 M | ✘ 316.7 M | inconclusiva |

Verificação pós-execução:

(verificação ainda não executada)
<!-- /TABELAS:B -->

### 4.1 Desempenho absoluto e relativo

| política | L-fix | L-lib+f | L-lib+f/lesão | positivas / negativas / inconclusivas (L-lib+f vs L-fix) | com reutilização |
|---|---|---|---|---|---|
| tamanho: aceitas; custo cumulativo (com a cadeia) | 15; 2 138 M | **17**; 1 660 M | 15; 1 555 M | 7 / 12 / 9 | 8 |
| unigrama: aceitas; custo cumulativo | 18; 2 554 M | **19**; 1 987 M | 18; 1 913 M | 9 / 11 / 8 | 10 |

Com as operações prévias, L-lib+f resolve 2 (tamanho) e 1 (unigrama) tarefas a mais do que L-fix e do que o seu próprio braço lesionado, a custo cumulativo menor (0,78 e 0,78 do de L-fix), apesar de a cadeia prévia custar 14–28 M a L-lib+f e 256–267 M a L-fix.

### 4.2 Transferência das nossas operações para tarefas do autor (pergunta de 06, §6.3.1)

Reutilização **direta** de `abs1`/`abs2` em hipóteses aceitas, nas duas políticas: `vizinhosPretos` (a hipótese aceita é a própria `abs1`: a tarefa do autor é a nossa operação), `semPretaIsolada` (abs2 composta com uma entrada do benchmark; L-fix falha na política de tamanho, razão mínima ≥ ×10,2; aceita com 10 folhas na unigrama, ×7,65), `tocaPreta` (×3,87 e ×1,80) e `vizinhancaExterna` (só L-lib+f aceita: `λg S. abs2 g S` menos S, razão mínima ≥ ×2,0 e ≥ ×4,2). Reutilização **indireta** (entrada do benchmark cujo corpo usa abs1/abs2): `semPretasAdjacentes` (só L-lib+f aceita; ≥ ×2 243 e ≥ ×7 379, porque a hipótese tem 3–4 folhas). As restantes reutilizações (contemTodasPretas, brancasDaLista, linhaTemPretaEm, colunaVazia, mesmoConjunto) usam só entradas criadas dentro do benchmark, como no bloco A.

O critério pré-registado §7.4 (transferência positiva das nossas operações para ≥ 2 tarefas do autor com reutilização verificável) é **satisfeito** nas duas políticas, com 4 tarefas de reutilização direta e 1 indireta, 3 das quais L-fix não resolve no orçamento. A leitura honesta inclui a coincidência de §2: o autor escolheu, por conta própria, a operação "vizinhos pretos de uma posição" como tarefa e como peça de outras três; a transferência observada é, em parte, a de uma operação que dois autores independentes consideram natural neste ambiente.

### 4.3 Lesão e transferência negativa

A lesão das duas entradas prévias custa 2 (tamanho) e 1 (unigrama) tarefas e torna o braço lesionado idêntico, em aceitações, a L-fix: a vantagem de L-lib+f sobre L-fix neste bloco é inteiramente atribuível a `abs1`/`abs2` e ao que delas deriva. A transferência negativa mantém o padrão do bloco A: 9 tarefas mais lentas por política (razões 0,03–0,85; as piores, `complementoDe` e `brancasDaLista`, são tarefas de 4–6 folhas em que a gramática alargada custa 10–30× mais), 1 tarefa perdida na política de tamanho (`colunaVazia`; recuperada na unigrama por reutilização, ×1,04) e 1 na unigrama (`naBorda`). O custo das entradas inúteis é o mesmo mecanismo de §3.2.

## 5. Blocos C, D e E — robustez e ordens **[E]**

### 5.1 Bloco C — sementes 10008 e 10009 (modo zero; L-fix e L-lib+f; duas políticas)

<!-- TABELAS:C8 -->
### Registro `bx-grades-e0-independente-v1-C-s10008`

Pacote grades-e0-independente v1, hash `9e600a4155844bc4…`; semente 10008; B = 20000; modos ['zero']; k_reservatorio = 40; parede total 1420 s.

| braço | aceitas | custo prévio | custo benchmark | custo cumulativo | custo por aceita | tarefas com reuso | entradas descobertas (reutilizadas) | livro fecha | inválidas |
|---|---|---|---|---|---|---|---|---|---|
| zero/tamanho/L-fix | 15/28 | 0.0 M | 1877.1 M | 1877.1 M | 125.1 M | 0 | 0 (0) | True | 0 |
| zero/tamanho/L-lib+f | 15/28 | 0.0 M | 1549.6 M | 1549.6 M | 103.3 M | 5 | 19 (6) | True | 0 |
| zero/unigrama/L-fix | 17/28 | 0.0 M | 1873.1 M | 1873.1 M | 110.2 M | 0 | 0 (0) | True | 0 |
| zero/unigrama/L-lib+f | 17/28 | 0.0 M | 2517.6 M | 2517.6 M | 148.1 M | 6 | 21 (7) | True | 0 |

| comparação | positivas | negativas | neutras | inconclusivas | com reuso |
|---|---|---|---|---|---|
| zero/tamanho/L-lib+f vs zero/tamanho/L-fix | 4 | 13 | 0 | 11 | 5 |
| zero/unigrama/L-lib+f vs zero/unigrama/L-fix | 4 | 14 | 0 | 10 | 6 |

| lesão | tarefas após a lesão | aceitas L-lib+f | aceitas lesão | custo L-lib+f | custo lesão | entradas removidas | sensível |
|---|---|---|---|---|---|---|---|

Tarefas aceitas a custo cumulativo igual (para cada aceitação de L-lib+f ao custo C, aceitas de L-lib+f vs de L-fix com custo ≤ C):
- zero/tamanho/L-lib+f vs zero/tamanho/L-fix: ultimaLinha C=0.1 M → 1 vs 1; contidoEm C=0.9 M → 2 vs 2; vizinhosPretos C=7.8 M → 3 vs 3; todaLinhaTemPreta C=10.9 M → 4 vs 5; complementoDe C=10.9 M → 5 vs 5; pretasPorColunas C=13.0 M → 6 vs 7; intersecaoOrdenada C=14.9 M → 7 vs 7; contemTodasPretas C=15.0 M → 8 vs 7; naBorda C=111.9 M → 9 vs 13; linhaDaPosicao C=121.4 M → 10 vs 13; juntarSemRepetir C=136.4 M → 11 vs 13; brancasDaLista C=141.4 M → 12 vs 13; linhaTemPretaEm C=403.5 M → 13 vs 14; tocaPreta C=727.4 M → 14 vs 14; semPretasAdjacentes C=964.7 M → 15 vs 14
- zero/unigrama/L-lib+f vs zero/unigrama/L-fix: ultimaLinha C=0.1 M → 1 vs 1; contidoEm C=2.6 M → 2 vs 2; vizinhosPretos C=34.9 M → 3 vs 5; todaLinhaTemPreta C=44.2 M → 4 vs 6; complementoDe C=44.2 M → 5 vs 6; pretasPorColunas C=57.7 M → 6 vs 8; intersecaoOrdenada C=59.5 M → 7 vs 8; contemTodasPretas C=59.6 M → 8 vs 8; colunaVazia C=107.3 M → 9 vs 9; naBorda C=271.6 M → 10 vs 13; linhaDaPosicao C=283.3 M → 11 vs 13; juntarSemRepetir C=317.9 M → 12 vs 14; brancasDaLista C=322.2 M → 13 vs 14; linhaTemPretaEm C=633.0 M → 14 vs 15; mesmoConjunto C=946.8 M → 15 vs 15; tocaPreta C=1026.1 M → 16 vs 16; semPretasAdjacentes C=1406.8 M → 17 vs 17

Tarefa a tarefa (✔ aceita / ✘ não; custo em passos; tamanho da hipótese entre parênteses; classe de transferência com razão exata ×, ou limite inferior ≥× quando L-fix não aceita):

| tarefa | tamanho: L-lib+f | L-fix | classe | unigrama: L-lib+f | L-fix | classe |
|---|---|---|---|---|---|---|
| ultimaLinha | ✔ 0.1 M (5) | ✔ 0.1 M (5) | negativa ×1.00 | ✔ 0.1 M (5) | ✔ 0.1 M (5) | negativa ×1.00 |
| contidoEm | ✔ 0.9 M (6) | ✔ 0.9 M (6) | negativa ×1.00 | ✔ 2.5 M (6) | ✔ 2.5 M (6) | negativa ×1.00 |
| vizinhosPretos | ✔ 6.9 M (8) | ✔ 6.2 M (8) | negativa ×0.89 | ✔ 32.3 M (8) | ✔ 24.5 M (8) | negativa ×0.76 |
| todaLinhaTemPreta | ✔ 3.0 M (7) | ✔ 2.1 M (7) | negativa ×0.71 | ✔ 9.2 M (7) | ✔ 7.2 M (7) | negativa ×0.78 |
| complementoDe | ✔ 0.0 M (4) | ✔ 0.0 M (4) | negativa ×0.92 | ✔ 0.1 M (4) | ✔ 0.0 M (4) | negativa ×0.92 |
| pretasPorColunas | ✔ 2.1 M (7) | ✔ 1.8 M (7) | negativa ×0.86 | ✔ 13.4 M (7) | ✔ 9.3 M (7) | negativa ×0.69 |
| intersecaoOrdenada | ✔ 1.9 M (6) | ✔ 1.6 M (6) | negativa ×0.85 | ✔ 1.9 M (6) | ✔ 1.7 M (6) | negativa ×0.88 |
| contemTodasPretas | ✔ 0.1 M (4) reuso abs2 | ✔ 3.7 M (7) | positiva ×48.32 | ✔ 0.0 M (4) reuso abs2,abs5 | ✔ 5.3 M (7) | positiva ×137.76 |
| colunaVazia | ✘ 53.5 M | ✔ 10.7 M (8) | negativa | ✔ 47.7 M (8) | ✔ 21.8 M (8) | negativa ×0.46 |
| naBorda | ✔ 43.4 M (9) | ✔ 32.1 M (9) | negativa ×0.74 | ✔ 164.3 M (9) | ✔ 108.2 M (9) | negativa ×0.66 |
| linhaDaPosicao | ✔ 9.5 M (8) | ✔ 6.0 M (8) | negativa ×0.63 | ✔ 11.7 M (8) | ✔ 5.5 M (8) | negativa ×0.47 |
| juntarSemRepetir | ✔ 15.0 M (7) | ✔ 7.0 M (7) | negativa ×0.47 | ✔ 34.6 M (7) | ✔ 14.6 M (7) | negativa ×0.42 |
| brancasDaLista | ✔ 4.9 M (6) reuso abs4,abs7 | ✔ 0.8 M (6) | negativa ×0.17 | ✔ 4.2 M (6) reuso abs4,abs5,abs7 | ✔ 0.4 M (6) | negativa ×0.10 |
| diferencaSimetrica | ✘ 125.4 M | ✘ 89.1 M | inconclusiva | ✘ 118.7 M | ✔ 97.2 M (9) | negativa |
| pretasOrdemInversa | ✘ 57.3 M | ✘ 82.0 M | inconclusiva | ✘ 104.6 M | ✘ 129.2 M | inconclusiva |
| algumaLinhaCheia | ✘ 66.3 M | ✔ 72.2 M (9) | negativa | ✘ 83.7 M | ✘ 119.0 M | inconclusiva |
| linhaTemPretaEm | ✔ 13.2 M (8) reuso abs10 | ✘ 161.6 M | positiva ≥×12.2 | ✔ 3.9 M (8) reuso abs11 | ✔ 57.3 M (11) | positiva ×14.55 |
| semPretaIsolada | ✘ 93.3 M | ✘ 139.9 M | inconclusiva | ✘ 103.9 M | ✘ 134.7 M | inconclusiva |
| colunasBrancas | ✘ 70.2 M | ✘ 78.7 M | inconclusiva | ✘ 115.6 M | ✘ 120.9 M | inconclusiva |
| mesmoConjunto | ✘ 100.9 M | ✘ 199.4 M | inconclusiva | ✔ 94.2 M (9) reuso abs2,abs7 | ✔ 136.6 M (10) | positiva ×1.45 |
| tocaPreta | ✔ 59.5 M (8) reuso abs15 | ✔ 90.5 M (9) | positiva ×1.52 | ✔ 79.3 M (8) reuso abs3 | ✔ 34.0 M (9) | negativa ×0.43 |
| bordaPreta | ✘ 72.6 M | ✘ 77.3 M | inconclusiva | ✘ 123.4 M | ✘ 122.1 M | inconclusiva |
| vizinhancaExterna | ✘ 162.6 M | ✘ 113.7 M | inconclusiva | ✘ 253.5 M | ✘ 75.4 M | inconclusiva |
| semPretasAdjacentes | ✔ 2.2 M (6) reuso abs18 | ✘ 139.9 M | positiva ≥×62.9 | ✔ 3.8 M (6) reuso abs20,abs5 | ✘ 134.7 M | positiva ≥×35.3 |
| cruzDaPosicao | ✘ 189.4 M | ✘ 138.4 M | inconclusiva | ✘ 375.5 M | ✘ 119.3 M | inconclusiva |
| pretasEmDomino | ✘ 101.4 M | ✘ 139.9 M | inconclusiva | ✘ 176.8 M | ✘ 134.7 M | inconclusiva |
| pretasConexas | ✘ 101.0 M | ✘ 139.8 M | inconclusiva | ✘ 176.2 M | ✘ 134.6 M | inconclusiva |
| componenteDe | ✘ 193.0 M | ✘ 141.9 M | inconclusiva | ✘ 382.2 M | ✘ 122.2 M | inconclusiva |

Verificação pós-execução:

(verificação ainda não executada)
<!-- /TABELAS:C8 -->

<!-- TABELAS:C9 -->

<!-- LEITURA:C -->

### 5.2 Bloco D — reservatório do oráculo com 20 grades (semente 10007; política de tamanho)

<!-- TABELAS:D -->

<!-- LEITURA:D -->

### 5.3 Bloco E — ordens do autor, aleatórias e autodirigida (política de tamanho; L-lib+f e L-fix)

<!-- TABELAS:E -->

<!-- LEITURA:E -->

## 6. Verificação pós-execução **[E]**

(preenchido por `verificacao.json` de cada registro)

## 7. Leitura segundo os critérios pré-registados **[R]**

Protocolo §7, bloco A (modo zero, semente 10007), por política: V = 28 tarefas válidas.

| grandeza | tamanho | unigrama | exigido pelo critério 1 |
|---|---|---|---|
| a_lib ≥ a_fix | 15 ≥ 15 ✔ | 17 ≥ 17 ✔ | ✔ |
| r (aceitas com reutilização verificável) ≥ 2 | 5 ✔ | 6 ✔ | ✔ |
| p⁺ ≥ 2 | 4 ✔ | 4 ✔ | ✔ |
| p⁺ > p⁻ | 4 > 13 ✘ | 4 > 14 ✘ | ✘ |
| hipóteses aceitas sem erro de previsão | ver §6 | ver §6 | — |
| lesão sensível | ✔ (custo) | ✔ (custo) | ✔ |

- **Critério 1 (mecanismo robusto ao autor): não satisfeito**, por uma única condição: as transferências negativas excedem as positivas nas duas políticas (13 e 14 contra 4 e 4).
- **Critério 2 (mecanismo inerte): não satisfeito**: há reutilização verificável em 5 e 6 tarefas e 4 transferências positivas por política, 3 delas em tarefas que L-fix não resolve no orçamento.
- **Resultado: misto (critério 3)**, reportado tarefa a tarefa em §3. A leitura que os dados sustentam é precisa: **o mecanismo adquire e reutiliza operações em tarefas que não preparámos** (contemTodasPretas, linhaTemPretaEm, semPretasAdjacentes, tocaPreta/mesmoConjunto, todas com entradas criadas dentro do conjunto do autor e certificadas), **mas o custo da biblioteca que acumula anula o ganho no agregado**: na política unigrama L-lib+f gasta 35 % mais do que L-fix para o mesmo número de tarefas; na política de tamanho gasta 18 % menos mas perde duas tarefas que L-fix resolve. A compressão por recorrência sozinha (L-lib), com 3–7 entradas, é o braço que mais tarefas resolve.
- **Critério 4 (transferência das nossas operações, bloco B): satisfeito** nas duas políticas (§4.2), com a ressalva da coincidência de §2.
- **Critérios 5–6 (robustez; erros de previsão)**: §5 e §6.
- **Critério 7**: nada aqui é evidência de H-B1, de formação de conceitos ou de inteligência geral. O que se decide é a robustez do mecanismo atual a tarefas não preparadas: **parcial**. A aquisição e a reutilização sobrevivem ao autor independente; a economia não.

**Decisão de programa (protocolo §7, caso 3)**: tarefa a tarefa, com o padrão de reutilização e de transferência negativa como guia. O padrão é claro e aponta uma correção concreta e barata antes de qualquer sofisticação: a biblioteca precisa de um critério de **utilidade** (poda das entradas nunca reutilizadas ao fim de k tarefas; exclusão dos fragmentos triviais de aplicação da compressão) — exatamente o que o documento 07 (§3, H-I3) já previa como condição para a promoção de subtermos, e que este benchmark mostra ser necessário até para a promoção de soluções. A investigação do documento 07 passa a incluir essa poda como variável, e a sua tríade de controlo C⁻ (tarefa em que a operação é inútil) torna-se a medida principal. A transição para o Experimento 2 (06, §5.2) não depende deste resultado e continua a exigir o que lá está escrito.

## 8. Limitações

1. Uma semente de dados nos blocos A, B e E (10007); a replicação do documento 06 mostrou variabilidade pequena entre sementes porque a busca é determinística, e o bloco C confere isso aqui com duas sementes.
2. A bateria finita de argumentos (contrato §2.3) define o que "correto" significa para as tarefas de função; as referências do autor são totais em listas arbitrárias, mas a avaliação só vê a bateria.
3. O alcance da busca (≈ 8–9 folhas a B = 20 000) foi declarado no contrato e o autor calibrou os níveis por ele; dez tarefas ficaram fora do alcance de todos os braços e são inconclusivas por construção, não por evidência.
4. O autor é um modelo da mesma família que o pesquisador principal; a independência é procedimental (sessão sem repositório, contrato auditado), não uma garantia de ausência de vieses partilhados sobre o que é "natural" numa grade — a coincidência de `vizinhosPretos` ilustra isso.
5. A classificação pré-registada de transferência não tem tolerância; a leitura com tolerância de 5 % em §3.2 é post hoc e está identificada como tal.
6. A contagem de tamanho do autor difere da nossa em tarefas de dois parâmetros (ele conta um ligador por parâmetro; nós contamos um por λ sintático); os tamanhos "do autor" em §2 são dele, os de §6 são os nossos.

## 9. Desvios do pré-registro

1. O contentor foi reciclado às 17:47 UTC durante o primeiro lançamento dos blocos A e B; ambos foram relançados do zero às 17:48 UTC. Nenhum resultado parcial existia nem foi usado. Registado em `benchmark/recebidos/REGISTO.md`.
2. Os blocos C, D e E, condicionais no protocolo, foram executados (§5) porque o bloco A demorou 33 min de parede.
3. Nenhuma alteração ao código, à DSL, à biblioteca ou às tarefas entre a receção e o fim da avaliação. O defeito da compressão (§3.2) foi identificado e **não** corrigido durante a avaliação.
