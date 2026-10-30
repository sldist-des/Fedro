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

(preenchido se executados)

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
