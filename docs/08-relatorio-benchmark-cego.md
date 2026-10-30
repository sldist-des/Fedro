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

(preenchido pelos registros `runs/bx-grades-e0-independente-v1-A-s10007`)

## 4. Bloco B — modo prévio (cadeia do documento 05 incluída no custo) **[E]**

(preenchido por `runs/bx-grades-e0-independente-v1-B-s10007`)

## 5. Blocos C, D e E — robustez e ordens **[E]**

(preenchido se executados)

## 6. Verificação pós-execução **[E]**

(preenchido por `verificacao.json` de cada registro)

## 7. Leitura segundo os critérios pré-registados **[R]**

## 8. Limitações

## 9. Desvios do pré-registro
