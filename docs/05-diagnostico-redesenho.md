# Diagnóstico e redesenho após o primeiro NO-GO

## Documento 05 — Causas do fracasso do piloto, experimento mínimo de aquisição e transferência, integridade e estratégia de busca

**Status:** v0.1 (2026-10-30). Depende do documento 04 (`runs/piloto-s10001-exploratorio-v2`) e dos registros novos em `runs/em-*`. Rótulos: [P] prova; [E] medição física; [C] resultado computacional determinístico; [F] interpretação; [H] hipótese; [A] aberto.

**Regra deste documento.** Um programa fora do alcance da busca não demonstra incapacidade de aprendizagem; demonstra que a busca, nesta configuração, não o alcança. Só se considera o mecanismo de reutilização funcionalmente demonstrado quando uma abstração encontrada pelo próprio aprendiz, a partir de exemplos e contraexemplos, é usada numa tarefa posterior inédita, com certificado de proveniência, e com custo menor que o do mesmo aprendiz sem biblioteca a orçamento equivalente. Nada aqui é evidência para H-B1: dados e hiperparâmetros estão expostos (documento 03, §0 e §11).

### Sumário

1. Missão 1 — Diagnóstico causal, com evidências
2. Missão 2 — Experimento mínimo de aquisição e transferência
3. Missão 3 — Correções de integridade
4. Missão 4 — Estratégia de busca
5. Veredito pelo critério central e próxima intervenção
6. Comandos executados e testes
7. Desvios e limitações

---

## 1. Missão 1 — Diagnóstico causal

Fonte: `runs/piloto-s10001-exploratorio-v2/deterministico.json` (fases 3, 4, 6) e o código em `fedro_piloto/`. Cada causa recebe um veredito: **comprovada** (há evidência direta nos registros ou no código), **contribuinte** (evidência de efeito menor) ou **hipótese** (sem evidência direta).

### 1.1 Explosão combinatória do enumerador — comprovada, causa dominante a B = 10⁴

Candidatos acumulados do enumerador (poda OE incluída) por tamanho máximo enumerado, contexto `{g: Grade} ⊢ Bool`, base E0 (`fases.3.pm8[*].por_tamanho`) [C]:

| tamanho s | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|
| candidatos acumulados | 217 | 833 | 2 309 | 7 018 | 18 758 | 53 697 |
| classes OE do tipo-alvo no tamanho | 3 | 5 | 13 | 45 | 112 | 263 |

O fator de crescimento é de 2,7 a 3,0 por tamanho. Com B = 10⁴ o enumerador completa o tamanho 7; com 10⁵, o 9; por extrapolação [H], 10⁶ daria 11 e os degraus de 13 a 16 da escada exigiriam entre 10⁸ e 10⁹ candidatos, o que, à vazão medida (mediana 423 candidatos/s, documento 04, §3.3), seriam meses de CPU. Nos outros contextos o quadro é igual: `{g, S} ⊢ L Pos` completa o 6 com 3 854 candidatos; `Grade → L Pos → L Pos` fechado completa o 8 com 6 954.

Consequência direta nos registros da fase 6: das 14 tarefas, 11 terminaram por `orcamento_enumeracao`, e 8 delas com `rodadas = 0`, isto é, o orçamento de 10⁴ candidatos internos esgotou-se **antes de qualquer hipótese do tamanho necessário chegar aos exemplos** (`fases.6.bracos.L-fix@E0.relatorio.resultados[*].motivo_fim`). Os tamanhos necessários (documento 04, §3.4) vão de 9 (ParAdjacente com `vizPretos`) a 16.

**O que isto não mostra.** Que os conceitos sejam inaprendíveis. Mostra que, por enumeração ascendente pura em Python, a 10⁴ candidatos, o alcance é 7 a 9 e os degraus estão acima disso.

### 1.2 Ausência de promoção de funções intermediárias — comprovada como lacuna de mecanismo; efeito insuficiente sozinho

O protocolo (documento 02, 2.8.1) mediu a escada "com os degraus anteriores como constantes", mas o braço L-lib do protocolo só adiciona à biblioteca fragmentos que se **repetem** entre soluções (`Biblioteca.comprimir`, `min_ocorrencias = 2`). A solução de uma tarefa de função resolvida uma só vez nunca vira constante. No piloto, L-lib descobriu apenas `λg. filtrar (celula g)` (duas ocorrências: `vizPretos` e `pretasDe`), que é cópia da solução de `pretasDe`.

A variante L-lib+f promove a solução de cada tarefa de função a entrada da biblioteca. No piloto ela promoveu `vizPretos` (tamanho 8) e, mesmo assim, ParAdjacente escrito com `vizPretos` tem tamanho 10 (`λg. algum (λp. nao (vazia? (vizPretos g p))) (pretas g)`) contra um alcance de 7 a 8 a 10⁴ no contexto `{g} ⊢ Bool` (`E0+anteriores-a-ParAdjacente`: 7 344 candidatos para completar o 7). Ou seja: a promoção é necessária (sem ela a escada do documento 02 é inconsistente, documento 04, §6.3, item 43), mas o degrau seguinte do currículo do piloto continuava 2 a 3 unidades acima do alcance. Veredito: lacuna real do mecanismo, insuficiente para explicar sozinha o fracasso.

### 1.3 Política de compressão por recorrência — comprovada como inadequada para este currículo

Três evidências [C]: (i) sobre as soluções manuais (modo mecanismo-teste), o fragmento de maior pontuação em ParAdjacente + NenhumaIsolada é o quantificador de ordem superior `λf g. f (λp. nao (vazia? (filtrar (celula g) (vizinhos g p)))) (pretas g)`, pontuação 13, e não `vizPretos` (pontuação 7); a compressão gulosa insere o primeiro e `vizPretos` deixa de se repetir (documento 04, §3.5); (ii) PM11 real = 1/3, e o único acerto (`passo`) vem de repetição dentro de um único programa; (iii) na execução autônoma, a única entrada foi uma cópia (α/η) de uma solução. A pontuação (ocorrências − 1) × (tamanho − 1) favorece fragmentos grandes com buracos funcionais e não distingue "abstração reutilizável" de "parte repetida de uma solução". Não foi reajustada ao alvo, de propósito (documento 04, §6.2, item 1).

### 1.4 Perda de classes pela poda observacional — contribuinte menor, não causa

Auditoria OE do documento 04 (§3.3): 0 classes perdidas em s ≤ 6 em todos os tipos; 2 de 38 em `Grade → Bool` em s = 8; 12 de 875 em `Grade → L Pos → L Pos` em s = 7 e 8; 8 de 163 em `L Pos → L Pos → Bool`. Como as buscas da fase 6 não chegaram aos tamanhos 7 e 8 na maioria dos contextos, a poda não foi o que impediu as soluções. Fica como contribuinte potencial a partir de s = 7, e o experimento mínimo verifica diretamente se a classe de denotação de cada alvo está presente entre os representantes (seção 2.5).

### 1.5 Falta de degraus acessíveis no currículo — comprovada

Tabela do documento 04, §3.4, em E0: contando só cadeias de degraus alcançáveis, 3 de 14; os degraus ParAdjacente (9 com `vizPretos`), `passo` (7 no contexto, alcance 6), `fecho` (16), `descartar` (13) ficam acima do alcance a 10⁴. A escada supunha saltos de "≤ 8 nós" (documento 02, 2.8.2) e os saltos reais, medidos com a convenção de tamanho e o D = 2 do aprendiz, são de 9 a 16. O currículo não tinha degraus do tamanho que a busca alcança. Esta é a causa que o experimento mínimo corrige diretamente: tarefas cujas soluções com a abstração anterior têm 7 nós.

### 1.6 Semântica, tipos e parâmetros da DSL — contribuintes; um deles comprovado

- **Codificação por λ dos quantificadores** (comprovado): `algum (λp. …) (pretas g)` custa 2 nós (λ e variável) além do corpo e sobe a profundidade D; ParAdjacente sem λ, via `expandir`, cai de 10 para 7. A DSL permite a forma sem λ (`expandir g (pretas g)`), mas a escada do documento 02 não a usava.
- **Fix de ordem superior** (comprovado como custo): `fecho` e `descartar` exigem `fix` com 2 a 3 binders (13 a 16 nós) e a avaliação de `fix` domina o tempo do enumerador (documento 04, §6.3, item 20). O experimento mínimo evita `fix` de propósito, para isolar o mecanismo de reutilização.
- **Instâncias monomórficas curadas** (contribuinte, medido): a tabela curada aumenta o alcance em até 1 em relação à sistemática (documento 04, §3.3); o efeito é pequeno e vai nos dois sentidos.
- **D = 2 nos aprendizes** (contribuinte): programas de E0' precisam de D de 3 a 6 (documento 04, §2.1, item 5). Não afeta E0 nas tarefas do experimento mínimo.
- **Avaliador em Python puro** (comprovado como custo, não como causa lógica): 56 a 2 899 candidatos/s. Afeta o quanto cabe em tempo de parede, não o que é alcançável por candidato.

### 1.7 Síntese

| causa | veredito | evidência |
|---|---|---|
| 1 explosão combinatória | comprovada, dominante a 10⁴ | crescimento ×2,7–3,0 por tamanho; 11/14 tarefas por `orcamento_enumeracao`, 8 com 0 rodadas |
| 2 sem promoção | comprovada como lacuna; insuficiente sozinha | L-lib só compressão por recorrência; L-lib+f promove mas o degrau seguinte fica 2–3 acima |
| 3 compressão por recorrência | comprovada como inadequada | PM11 = 1/3; fragmento de topo é quantificador de ordem superior; entrada autônoma = cópia |
| 4 poda OE | contribuinte menor | 0 perdas em s ≤ 6; perdas só em s = 7–8, onde a busca não chegou |
| 5 currículo sem degraus | comprovada | saltos reais de 9 a 16 contra alcance 6 a 9 |
| 6 DSL | contribuinte; λ nos quantificadores comprovado | ParAdjacente 10 → 7 sem λ; fix 13–16 |

Conclusão operacional: a intervenção mais informativa não é mais orçamento, e sim (a) um currículo cujos degraus com a abstração anterior caibam no alcance medido, (b) promoção das soluções de função como mecanismo declarado de consolidação, (c) controles que separem reutilização de "qualquer treino ajuda", e (d) uma política de busca igual para todos os aprendizes. É o que a seção 2 faz.

---

## 2. Missão 2 — Experimento mínimo de aquisição e transferência

Módulo `fedro_piloto/experimento_minimo.py`. Registros: `runs/em-s10002-tamanho/` (política por tamanho) e `runs/em-s10002-unigrama/` (política unigrama, seção 4.2); cada um com `deterministico.json`, `medicoes.json`, `hashes.json`, `relatorio.md`, e `verificacao_exaustiva.json`. Semente 10 002 (intervalo do piloto; a semente 10 001 foi a do documento 04). Hash das fontes em `deterministico.json → fontes`.

### 2.1 Desenho

**Currículo principal**, todas as tarefas definidas pelo ambiente (referências Python independentes da DSL; o aprendiz só recebe exemplos, contraexemplos e um conjunto de teste disjunto por instância):

| ordem | tarefa | tipo | natureza | menor programa conhecido em E0 (nós) | com a abstração anterior |
|---|---|---|---|---|---|
| T1 | `vizPretos`: vizinhas pretas de p | Grade → Pos → L Pos | função | 8 | — |
| T2 | `expandir`: vizinhas pretas de um conjunto, sem o conjunto | Grade → L Pos → L Pos | função (conjunto) | 12 | 7 (`juntar (mapear (vizPretos g) S)`) |
| T3 | `ParAdjacente`: existe par de pretas adjacentes | Grade → Bool | predicado | 15 (via λ) ou 10 (sem λ) | 7 (`nao (vazia? (expandir g (pretas g)))`) |
| T4 | `NenhumaIsolada`: toda preta tem vizinha preta | Grade → Bool | predicado | ≥ 14 | 9 (`vazia? (diferenca (pretas g) (expandir g (pretas g)))`) |

Os tamanhos "com a abstração anterior" foram escolhidos para caber no alcance medido (6 a 9 a 10⁴ no documento 04): é desenho de currículo pelo experimentador, declarado; o aprendiz nunca vê programas. T4 foi incluída como degrau fora do alcance esperado a B = 2 × 10⁴.

**Currículo não relacionado (controle):** U1 `pretasColuna1` (pretas da primeira coluna; Grade → Pos → L Pos, ignora p), U2 `semLinha1` (S sem as células da primeira linha; Grade → L Pos → L Pos), depois T3 e T4. Mesmo número de tarefas de função, mesmos tipos, sem vizinhança.

**Braços**, todos com B = 2 × 10⁴ candidatos de enumeração por tarefa, K = 12 rodadas, mesma semente (logo os mesmos exemplos, contraexemplos e testes por tarefa), mesma política de busca, base E0:

| braço | biblioteca | currículo |
|---|---|---|
| L-fix | nenhuma | T1 T2 T3 T4 |
| L-lib | compressão por recorrência (≥ 2 ocorrências) | T1 T2 T3 T4 |
| L-lib+f | recorrência + promoção da solução de cada tarefa de função | T1 T2 T3 T4 |
| L-lib+f/lesao | como L-lib+f; **lesão** (remoção de todas as entradas descobertas e do corpus) antes de T3 | T1 T2 · T3 T4 |
| L-lib+f/controle | como L-lib+f | U1 U2 T3 T4 |
| L-fix/custo-igual | nenhuma; só T3, com B + (custo cumulativo de enumeração de L-lib+f antes de T3 − o de L-fix), se positivo | T3 |
| L-fix/10x | nenhuma; só T3 com 10·B | T3 |

Sem adaptadores de portador. Nenhuma solução manual em nenhuma tabela de aprendiz (certificados de proveniência; `Biblioteca` em modo autônomo).

### 2.2 Resultados, política por tamanho (`runs/em-s10002-tamanho`)

| braço | tarefa | aceita | rodadas | hipótese aceita (tamanho) | entradas usadas | custo da tarefa | cumulativo | enum. cumul. |
|---|---|---|---|---|---|---|---|---|
| L-fix | vizPretos | sim | 1 | `λg p. filtrar (celula g) (vizinhos g p)` (8) | — | 6 307 717 | 6 307 717 | 1 281 |
| L-fix | expandir | não | 0 | orçamento de enumeração | — | 109 655 765 | 115 963 482 | 21 282 |
| L-fix | ParAdjacente | não | 3 | orçamento de enumeração | — | 91 826 937 | 207 790 419 | 41 283 |
| L-fix | NenhumaIsolada | não | 1 | orçamento de enumeração | — | 138 795 451 | 346 585 870 | 61 284 |
| L-lib | (idêntico a L-fix nas 4 tarefas; nenhum fragmento com ≥ 2 ocorrências; 0 entradas) | | | | | | 346 585 963 | 61 284 |
| **L-lib+f** | vizPretos | sim | 1 | `λg p. filtrar (celula g) (vizinhos g p)` (8) → **abs1** | — | 6 307 825 | 6 307 825 | 1 281 |
| **L-lib+f** | expandir | sim | 1 | `λg S. juntar (mapear (abs1 g) S)` (7) → **abs2** | abs1 | 4 550 621 | 10 858 446 | 3 729 |
| **L-lib+f** | ParAdjacente | sim | 1 | `λg. nao (vazia? (abs2 g (pretas g)))` (7) | abs2 (e abs1 por abs2) | 3 762 043 | 14 620 489 | 5 465 |
| L-lib+f | NenhumaIsolada | não | 1 | orçamento de enumeração | — | 100 061 162 | 114 681 651 | 25 466 |
| L-lib+f/lesao | vizPretos, expandir | sim, sim | 1, 1 | como L-lib+f | abs1 | | 10 858 446 | 3 729 |
| L-lib+f/lesao | **lesão**: abs1 e abs2 removidas; corpus esquecido | | | | | | | |
| L-lib+f/lesao | ParAdjacente | **não** | 3 | orçamento de enumeração | — | 91 826 937 | 102 685 383 | 23 730 |
| L-lib+f/lesao | NenhumaIsolada | não | 1 | orçamento de enumeração | — | 138 795 451 | 241 480 834 | 43 731 |
| L-lib+f/controle | pretasColuna1 | sim | 1 | `λg p. filtrar (celula g) (cabeca (colunas g))` (8) → abs1 = `λg. filtrar (celula g) (cabeca (colunas g))` | — | 6 154 228 | 6 154 228 | 1 281 |
| L-lib+f/controle | semLinha1 | sim | 1 | `λg S. diferenca S (cabeca (linhas g))` (7) → abs2 | — | 5 873 897 | 12 028 125 | 4 094 |
| L-lib+f/controle | ParAdjacente | **não** | 3 | orçamento de enumeração | — | 78 632 505 | 90 660 630 | 24 095 |
| L-lib+f/controle | NenhumaIsolada | não | 1 | orçamento de enumeração | — | 91 793 613 | 182 454 243 | 44 096 |
| L-fix/custo-igual | ParAdjacente (B = 2 × 10⁴; delta = −17 553, L-fix já gastara mais) | não | 3 | orçamento de enumeração | — | 91 826 937 | 91 826 937 | 20 001 |
| **L-fix/10x** | ParAdjacente (B = 2 × 10⁵) | **sim** | 4 | `λg. algum (celula g) (juntar (mapear (vizinhos g) (pretas g)))` (10) | — | 350 840 773 | 350 840 773 | 43 498 |

Unidade de "custo": `total_aprendiz` do livro-razão (candidatos de enumeração + candidatos do protocolo + passos de avaliação dos dois + subtermos da compressão + consultas ao oráculo). "enum. cumul." = candidatos de enumeração acumulados. Todas as hipóteses aceitas foram **verificadas exaustivamente** contra as referências do ambiente em todas as grades de n = 1 a 4 (`verificacao_exaustiva.json`): 0 erros em 66 066 grades para os predicados e em 264 258 entradas para as funções. [C]

**Abstrações, com proveniência** (`deterministico.json → bracos.*.abstracoes`):

| braço | nome | corpo | tipo | método | tarefa de origem | reutilizada em (direta) | indireta | certificado |
|---|---|---|---|---|---|---|---|---|
| L-lib+f | abs1 | `λg p. filtrar (celula g) (vizinhos g p)` | Grade → Pos → L Pos | promoção da solução | vizPretos | **expandir** (1) | **ParAdjacente** (1, via abs2) | busca → descoberta → entrada |
| L-lib+f | abs2 | `λg S. juntar (mapear (abs1 g) S)` | Grade → L Pos → L Pos | promoção da solução | expandir | **ParAdjacente** (1) | — | idem |
| L-lib+f/controle | abs1 | `λg. filtrar (celula g) (cabeca (colunas g))` | Grade → L Pos | promoção (parâmetro p não usado, retirado) | pretasColuna1 | nenhuma | — | idem |
| L-lib+f/controle | abs2 | `λg S. diferenca S (cabeca (linhas g))` | Grade → L Pos → L Pos | promoção | semLinha1 | nenhuma | — | idem |
| L-lib | — | nenhuma entrada | | | | | | |

Classificação (documento 04, §4): **fornecidas**: as 29 primitivas de E0; **manuais de referência ou teste**: nenhuma em nenhum braço (os programas de `programas_referencia` não foram usados neste experimento, nem na auditoria OE, que compara com as referências Python do ambiente); **descobertas**: abs1 e abs2 de L-lib+f, abs1 e abs2 do controle; **descobertas e reutilizadas**: abs1 e abs2 de L-lib+f. As entradas promovidas são, por definição do método, iguais à solução da tarefa de origem; a novidade não está na entrada, está no seu uso numa tarefa posterior.

**Medições** (`medicoes.json`, por braço, processo próprio): L-fix 217 s de parede, 171 s de CPU, 531 MiB de pico; L-lib 219 s; L-lib+f 80 s, 59 s de CPU, 541 MiB; lesão 166 s; controle 116 s; L-fix/10x 152 s, 517 MiB; total 396 s de parede com 4 processos. [E]

### 2.3 Leitura pelo critério central

1. **Encontrou autonomamente a operação intermediária:** sim. `vizPretos` e `expandir` saíram da enumeração a partir de 4 pares de exemplo cada (grades naturais de n = 3 e 4 da partição `oraculo_treino`), sem contraexemplo (1 rodada); as hipóteses coincidem com as referências em todo o domínio até n = 4.
2. **Consolidou-a na biblioteca:** sim, por promoção da solução certificada (abs1, abs2), com certificado de busca, de descoberta e de entrada (`certificados.py`); a tabela de aprendiz recusa entradas manuais por construção.
3. **Reutilizou numa tarefa posterior inédita:** sim, duas vezes em cadeia. `expandir` não é tarefa de origem de abs1 e a usa; `ParAdjacente` (predicado, tipo diferente, oráculo de contraexemplos) não é tarefa de origem de abs2 e a usa, e usa abs1 indiretamente. As reutilizações estão em `reutilizacoes` e `reutilizacoes_indiretas` das entradas e em `constantes_biblioteca_usadas` dos resultados.
4. **Economia de recursos a informação de treino igual:** a custo por tarefa igual (B = 2 × 10⁴), L-fix não resolve T2 nem T3; L-lib+f resolve as duas e chega a T3 com custo cumulativo 14,6 milhões contra 207,8 milhões de L-fix (que não resolveu). Com 10 × B só em T3, L-fix resolve T3 por outro programa (tamanho 10), ao custo de 350,8 milhões nessa tarefa, 24 vezes o custo cumulativo de L-lib+f em T1 + T2 + T3 e 8 vezes mais candidatos de enumeração (43 498 contra 5 465 acumulados). A sonda "custo igual" não teve o que igualar: L-fix já gastara 5,7 vezes mais candidatos de enumeração antes de T3.
5. **Ablação:** removidas abs1 e abs2 (e o corpus) antes de T3, o mesmo aprendiz falha T3 com o mesmo orçamento e exatamente o custo de L-fix. O que resolveu T3 foi a biblioteca, não outro estado do aprendiz.
6. **Controle de currículo não relacionado:** duas tarefas de função de mesmo tipo e tamanho, resolvidas e promovidas, não ajudam em T3. "Qualquer treino" não explica o resultado.
7. **L-lib (recorrência apenas):** idêntico a L-fix. Confirma a causa 3 do diagnóstico: sem promoção, nenhuma entrada é formada a partir de soluções únicas.

**Veredito do critério central, nesta configuração:** o mecanismo de aquisição, consolidação e reutilização está **funcionalmente demonstrado** para a cadeia T1 → T2 → T3, com proveniência verificável e economia medida. [C]

### 2.4 O que isto não mostra

- Não é evidência para H-B1 (documento 01): semente única, dados e hiperparâmetros expostos, currículo desenhado pelo experimentador para caber no alcance. É a demonstração de que o mecanismo funciona quando os degraus cabem; a questão científica é se degraus assim existem e são encontráveis sem desenho, o que fica para o experimento confirmatório e para um currículo autogerado.
- A abstração consolidada é a solução inteira do degrau (promoção), não uma abstração extraída por compressão entre tarefas. A compressão por recorrência não produziu nada neste currículo.
- T4 (NenhumaIsolada, 9 nós com abs2) ficou fora do alcance a 2 × 10⁴ em todos os braços: a fronteira de alcance continua a 1 ou 2 nós dos degraus seguintes.
- O conjunto de teste de ParAdjacente tem 27 positivos e 3 negativos (distribuição natural de `teste_int`): não é degenerado, mas a acurácia balanceada assenta em 3 negativos; por isso a verificação exaustiva em n ≤ 4 foi acrescentada.
- L-fix/10x mostra que ParAdjacente é alcançável sem biblioteca a 10 × B por um programa de tamanho 10 sem λ: a vantagem da biblioteca é de custo (24 ×), não de possibilidade.

### 2.5 Integridade dos dados deste experimento

- Partição por instância: todos os exemplos e contraexemplos vêm de `oraculo_treino`; os testes, de `teste_int`; 0 grades dos baldes reservados ao confirmatório (`hashes.json`).
- Exemplos iniciais: 4 por tarefa, instâncias distintas; teste: 30 grades distintas por predicado (90 entradas distintas por função).
- Auditoria OE na tabela base (48 grades independentes de `teste_int`): a classe de `vizPretos` está presente ao custo 8; as de `expandir` e `ParAdjacente` não estão até o custo 8 (esperado: tamanhos brutos 12 e 15). Isto confirma que as soluções de T2 e T3 só entraram no alcance através das abstrações, não por uma classe perdida ou ganha na poda.
- Medições de tempo e memória em bloco separado; contadores determinísticos; 0 falhas internas nos braços (`falha = null`).

## 3. Missão 3 — Correções de integridade

Todas implementadas em código, com testes em `fedro_piloto/tests/test_redesenho.py` (seção 6).

| problema (documento 04) | correção | onde |
|---|---|---|
| Acurácia 1,000 num conjunto de teste sem negativos apresentada como se informasse (ExistePreta: 29 positivos, 0 negativos) | Todo resultado de teste traz agora `teste_resumo`: contagem por classe (predicados) ou de saídas distintas (funções), acurácia **balanceada** e a marca `degenerado` quando há uma só classe; nesse caso a acurácia balanceada é `None` e o aviso é gravado no registro. O relatório do experimento mostra sempre acc / balanceada / degenerado lado a lado | `aprendizes.AprendizBase._avaliar_teste_resumo`; `ResultadoTarefa.teste_resumo` |
| Duplicações: negativos repetidos nos conjuntos de desenho em n pequeno (ParAdjacente 60/67 em n = 3) e entradas de teste repetidas | No experimento mínimo os exemplos iniciais exigem instâncias distintas (`exemplos_iniciais_*`, já existente) e o conjunto de teste é amostrado sem reposição por valor; cada preparo grava `teste_entradas_distintas` e `num_teste`, e a seção 2 reporta a razão | `aprendizes.conjunto_teste`, `PreparoTarefa.como_dict` |
| Perdas pela poda OE (classes perdidas em s = 7 e 8) | Isoladas, não eliminadas: (i) o refinamento OE por contraexemplo continua ligado e o número de reconstruções é gravado por tarefa (`refinamentos_oe`); (ii) **auditoria do alvo**: para cada alvo do experimento, verifica-se se a classe de denotação da referência do ambiente está entre os representantes OE até o custo c, comparando numa amostra independente de 48 grades de `teste_int` (com 6 grades um termo espúrio coincidiu com ParAdjacente no teste de fumaça, e isso ficou registrado) | `experimento_minimo.classe_alvo_presente`; teste `TestAuditoriaOE` |
| Custos misturados | Registro independente, por tarefa e braço, de: candidatos da enumeração (poda OE), candidatos do protocolo (testados nos exemplos), passos de avaliação dos dois, subtermos examinados na compressão, consultas e custo do oráculo; e, em bloco separado, tempo de parede, CPU e memória de pico por braço (processo próprio, VmHWM reiniciado) | `razao.LivroRazao`, `experimento_minimo.job_braco` |
| "Candidatos" apresentados como custo | O custo cumulativo usado nas curvas e na sonda de custo igual é `total_aprendiz` (todas as parcelas do aprendiz); os candidatos de enumeração e do protocolo aparecem como colunas separadas | `experimento_minimo._curva`, `_cum_antes` |

Observação nova sobre custos (dos registros do piloto, `fases.6.*.contador_busca`): os passos gastos dentro do enumerador para calcular assinaturas OE superam em 3 a 4 ordens de grandeza os passos gastos a testar candidatos nos exemplos (ParAdjacente, L-fix@E0: 32,7 milhões contra 3 925), e o número de candidatos do protocolo testados por tarefa ficou entre 5 e 1 062. O custo está na poda, não no teste de hipóteses. [C]

## 4. Missão 4 — Estratégia de busca

### 4.1 Alternativas avaliadas

| alternativa | o que é | custo de implementação | o que isola | decisão |
|---|---|---|---|---|
| Enumeração por tamanho com poda OE (atual) | ascendente, completa, dedupe por denotação em 36 mundos | — | referência | mantida como linha de base |
| **Custo de folha ponderado (unigrama)** | cada constante tem custo inteiro ≥ 1; a enumeração é por custo total; completa (todo termo de tamanho s tem custo ≤ 2s). Política: custo 1 para constantes já usadas em soluções aceitas **deste** aprendiz e para entradas da sua biblioteca cujo corpo só usa constantes baratas; 2 para as demais. É a forma mais simples de "proposta probabilística": um unigrama de dois níveis aprendido só das próprias soluções | pequeno: `Gramatica.custos_folha`, camada de folhas por custo em `Enumerador._construir`, `AprendizBase.custos_folha_correntes` | a MESMA política para L-fix e L-lib, logo a diferença entre eles continua a ser só a biblioteca | **implementada e medida** (seção 4.2) |
| Busca guiada por modelo (reconhecimento à DreamCoder) | rede que prediz uma distribuição sobre primitivas por tarefa | grande; precisa de dados de treino (tarefas resolvidas) que ainda não existem em número | não isola: o modelo é mais um lugar onde o alvo pode vazar | adiada; condição: ≥ dezenas de tarefas resolvidas |
| Reutilização de cálculos entre tarefas | partilhar as tabelas OE (por tabela de primitivas, contexto e tipo) entre tarefas do mesmo tipo; evitar reconstruções | médio; hoje cada `EstadoBusca` tem o seu `Enumerador` e cada refinamento reconstrói | reduz custo igualmente nos dois aprendizes | **medida a oportunidade** (abaixo); implementação adiada |
| Reutilização de cálculos dentro da avaliação | memoizar o `fix` funcional (80 % do tempo do enumerador no piloto) | médio | não muda o que é alcançável por candidato; muda a vazão | adiada; irrelevante no experimento mínimo (sem `fix`) |
| Propostas probabilísticas por amostragem (PCFG amostrada em vez de enumerada) | sortear programas segundo um prior | médio | perde completude e determinismo por ordem; dificulta o custo igual | não adotada nesta fase |

**Oportunidade de reutilização de cálculos, medida nos registros do piloto.** Nas 14 tarefas de L-fix@E0, as reconstruções do enumerador por refinamento OE foram raras (1 em ParAdjacente; 0 nas demais; 2 em L-lib+f). O custo não está nas reconstruções; está nas assinaturas OE dos subtermos de todos os tipos (`enumeracao_passos`). As tabelas OE de um contexto dependem só da tabela de primitivas e dos mundos; tarefas do mesmo tipo e tabela (no experimento mínimo: `vizPretos` e `pretasColuna1`; `ParAdjacente` e `NenhumaIsolada`) poderiam partilhá-las, o que pouparia até metade da enumeração nesses pares. Para L-lib a tabela muda a cada entrada nova, logo a partilha vale só entre tarefas sem mudança de biblioteca. Fica registrada como próxima intervenção de custo (seção 5), não de alcance.

### 4.2 Resultado medido: política por tamanho contra política unigrama

Mesmo experimento, mesma semente, mesmos exemplos e testes; só muda a ordem de enumeração (`runs/em-s10002-unigrama`). Todas as hipóteses aceitas verificadas exaustivamente em n ≤ 4: 15 hipóteses, 0 erros (`verificacao_exaustiva.json`). [C]

| braço | tarefa | tamanho: aceita / custo | unigrama: aceita / custo | hipótese sob unigrama |
|---|---|---|---|---|
| L-fix | expandir | não / 109,7 M | **sim** / 173,3 M | `λg S. filtrar (celula g) (juntar (mapear (vizinhos g) S))` (10) |
| L-fix | ParAdjacente | não / 91,8 M | **sim** / 84,4 M | `λg. algum (celula g) (juntar (mapear (vizinhos g) (pretas g)))` (10) |
| L-fix | cumulativo até T3 | 207,8 M (1 de 3) | 264,0 M (3 de 3) | |
| L-lib | expandir, ParAdjacente | não, não | sim, sim (como L-fix) | extrai depois `λg. filtrar (celula g)` e `λg S. juntar (mapear (vizinhos g) S)`, nenhuma reutilizada |
| L-lib+f | expandir | sim / 4,6 M (7) | sim / 8,3 M (7, abs1) | `λg S. juntar (mapear (abs1 g) S)` |
| L-lib+f | ParAdjacente | sim / 3,8 M (7) | sim / 13,7 M (8, abs2) | `λg. algum (celula g) (abs2 g (pretas g))` |
| L-lib+f | cumulativo até T3 | 14,6 M (3 de 3) | 28,3 M (3 de 3) | |
| L-lib+f/lesao | ParAdjacente | não | **sim** / 84,4 M (10, sem biblioteca) | o mesmo programa de L-fix |
| L-lib+f/controle | ParAdjacente | não | **não** / 259,6 M | — |
| todos | NenhumaIsolada | não | não | — |

Leituras [C]:

1. **A política unigrama amplia o alcance de L-fix** o bastante para resolver T2 e T3 a 2 × 10⁴: depois de T1, `filtrar`, `celula` e `vizinhos` custam 1 e os programas de tamanho 10 feitos só delas e de `juntar`, `mapear`, `algum` (custo 2) entram no orçamento. Com a mesma política, a biblioteca continua a dar economia, agora só de custo: 264,0 M contra 28,3 M (9,3 vezes) até T3, 13 431 contra 4 109 candidatos de enumeração. A diferença entre "possível" e "impossível" a este B é da política de busca; a diferença de custo é da biblioteca.
2. **A lesão deixa de bloquear T3** sob unigrama, porque o aprendiz lesionado conserva as constantes usadas (custo 1) e encontra o programa de tamanho 10 de L-fix, ao custo de L-fix (84,4 M contra 13,7 M com abs2). A ablação continua a mostrar o que a biblioteca vale: 6 vezes em custo nessa tarefa.
3. **Transferência negativa do prior de busca no controle:** o aprendiz treinado em `pretasColuna1` e `semLinha1` fica com `cabeca`, `colunas`, `diferenca`, `linhas` baratas e `vizinhos`, `juntar`, `mapear`, `algum` caras; o programa de tamanho 10 de ParAdjacente fica fora do alcance e o controle falha T3, com custo maior que o de L-fix por tamanho. A política unigrama transfere um viés, e um viés errado bloqueia. É um resultado negativo informativo: a reutilização de "o que já usei" não é neutra.
4. **A compressão por recorrência passa a ter material** sob unigrama (duas soluções com `filtrar (celula g)` e duas com `juntar (mapear (vizinhos g) ·)`), mas as entradas surgem depois das tarefas em que ocorrem e não são reutilizadas, porque o currículo acaba. Com um currículo mais longo, poderiam ser; não há evidência disso aqui.
5. **Custo da política para L-lib+f:** sob unigrama, `nao` e `vazia?` custam 2 (nunca usadas) e a solução de 7 nós de ParAdjacente fica atrás da de 8 nós com `algum`; L-lib+f gasta 1,9 vezes mais que por tamanho. O prior ajuda o aprendiz sem biblioteca e atrapalha o com biblioteca, nesta cadeia.

**Decisão sobre a política.** Nenhuma das duas domina. Para o confirmatório, a política é um fator a cruzar com a biblioteca (2 × 2), nunca uma escolha prévia: é o único desenho que isola o efeito da biblioteca do efeito do prior, como os dois registros mostram.

## 5. Veredito pelo critério central e próxima intervenção

**Veredito.** Pelo critério central deste documento, o mecanismo de reutilização está funcionalmente demonstrado na configuração do experimento mínimo: uma abstração encontrada pelo próprio aprendiz a partir de exemplos (`vizPretos`, depois `expandir`) foi consolidada com certificado de proveniência e utilizada em tarefas posteriores inéditas (`expandir`, depois `ParAdjacente`), com a lesão e o currículo não relacionado falhando na mesma tarefa, e com L-fix a precisar de 10 vezes o orçamento e 24 vezes o custo para resolvê-la por outro caminho. [C]

**O que o veredito não é.** Não é a decisão GO do documento 03, que exige a escada inteira (14 degraus, incluindo `fecho` e `descartar`) e o confirmatório com instâncias não expostas; aqui são 3 degraus desenhados para caber no alcance, uma semente, e T4 fora do alcance. Não é evidência de H-B1. É a prova de que o bloqueio do piloto era de mecanismo e de currículo, não de impossibilidade, e de que a próxima pergunta tem objeto.

**Sob a política unigrama** (seção 4.2), L-fix também resolve T2 e T3 a 2 × 10⁴ por programas de tamanho 10; a biblioteca passa a valer 9,3 vezes em custo cumulativo e a lesão custa 6 vezes em T3. O critério central continua satisfeito (abs1 reutilizada em `expandir`, abs2 em `ParAdjacente`, 15 hipóteses verificadas sem erro), e a afirmação correta é: a biblioteca converte custo, não possibilidade, quando a busca tem um prior adequado; e o prior aprendido de tarefas não relacionadas é prejudicial (controle falha T3 nas duas políticas).

**Bloqueio exato que resta.** A fronteira de alcance a 2 × 10⁴ está em 7 a 8 nós com a biblioteca; o degrau seguinte (NenhumaIsolada com `expandir`, 9 nós) e os laços de recursão (`fecho` 16, `descartar` 13) continuam fora. Cada degrau novo exige ou uma abstração anterior que o traga para ≤ 8, ou mais alcance.

**Próxima intervenção mais informativa**, em ordem:

1. **Currículo autogerado sob o mesmo mecanismo** (resposta à objeção de desenho pelo experimentador): o ambiente oferece um conjunto de tarefas de função sem ordem; o aprendiz escolhe a próxima pela estimativa de custo (menor tamanho esperado com a biblioteca corrente) ou por progresso; mede-se se a cadeia T1 → T2 → T3 emerge sem a ordem dada. Custo: pequeno (um seletor de tarefas); risco: o conjunto oferecido ainda é desenhado.
2. **Compressão que produza abstrações menores que a solução**: a promoção consolida soluções inteiras; para `NenhumaIsolada` (9 com `expandir`) e para os laços, a abstração útil é um sub-termo. Alterar a pontuação para privilegiar fragmentos de primeira ordem (sem buracos funcionais) e medir PM11 de novo, sem olhar os alvos ao fixar a regra.
3. **Partilha das tabelas OE entre tarefas do mesmo tipo** e memoização do `fix` (seção 4.1): reduz o custo, não o alcance; necessária antes de qualquer tentativa com os laços de recursão.
4. Só depois: T4 e os laços, com B maior **medido**, nunca "indiscriminado": o custo de cada nó a mais é conhecido (×2,7 a 3,0).

## 6. Comandos executados e testes

```
# diagnóstico (leitura dos registros do piloto)
python3 - < (consultas a runs/piloto-s10001-exploratorio-v2/deterministico.json; números citados na seção 1)

# experimento mínimo, política por tamanho e política unigrama (em sequência, 4 processos)
python3 -m fedro_piloto.experimento_minimo --id em-s10002-tamanho  --B 20000 --politica tamanho  --processos 4
python3 -m fedro_piloto.experimento_minimo --id em-s10002-unigrama --B 20000 --politica unigrama --processos 4

# verificação exaustiva das hipóteses aceitas (n = 1..4) -> runs/em-*/verificacao_exaustiva.json
PYTHONPATH=. python3 - < (script registrado na sessão; reproduzível a partir de deterministico.json)

# testes
python3 -m unittest discover -s fedro_piloto/tests -v
```

Suíte completa após as alterações: **229 testes, 0 falhas, 0 erros** (458 s). Os 14 testes novos estão em `fedro_piloto/tests/test_redesenho.py`: referências das tarefas novas (`expandir` sem o conjunto de entrada; composição `nao (vazia? (expandir g (pretas g)))` = ParAdjacente em todas as grades 3 × 3); custo ponderado (custo 1 coincide com tamanho; completude: denotações até o tamanho s ⊆ denotações até o custo 2s; custo inválido rejeitado); política unigrama (custos após uma solução; política inválida rejeitada); lesão (remove descobertas, mantém fornecidas, tabela continua de uso "descoberta"); resumo de teste (conjunto degenerado marcado, acurácia balanceada 0,5 para o predicado constante); aritmética da sonda de custo igual; auditoria OE do alvo (ExistePreta presente até o custo 5, 48 grades independentes); promoção de solução com parâmetro não usado.

**Falha encontrada e corrigida durante a execução:** a primeira execução completa abortou no braço de controle, porque a solução de `pretasColuna1` ignora o argumento p e a promoção com dois parâmetros não casava com o corpus (`ErroProveniencia: fragmento não ocorre nas soluções certificadas`). Correção: a promoção retira parâmetros que não ocorrem no corpo e recusa soluções constantes (registrado); uma exceção num braço passou a ficar registrada no próprio braço em vez de abortar os outros.

## 7. Desvios e limitações

1. **Currículo desenhado**: a ordem e as tarefas T1 a T4 foram escolhidas sabendo os tamanhos das soluções com a abstração anterior. O aprendiz não vê programas, e o controle não relacionado e a lesão separam o efeito da biblioteca do efeito de "treinar". Mas a existência de degraus deste tamanho no currículo é obra do experimentador (seção 5, intervenção 1).
2. **Promoção como consolidação**: a entrada de biblioteca é a solução inteira da tarefa de função. É o mecanismo que o documento 02, 2.8.1, pressupunha sem o dizer; fica declarado como mecanismo de L-lib+f, distinto da compressão por recorrência de L-lib.
3. **Semente única e escala exploratória**: B = 2 × 10⁴, uma semente (10 002), base E0 só. Nada é estatística; os registros permitem repetir com outras sementes.
4. **T4 e os laços de recursão** não foram alcançados; o experimento não toca `fix`.
5. **Teste de ParAdjacente com 3 negativos** (distribuição natural): suprido pela verificação exaustiva em n ≤ 4, que é uma verificação do ambiente, não uma medida de generalização fora de n ≤ 4.
6. **Política unigrama**: custos em {1, 2} aprendidos das próprias soluções; é a forma mais simples de proposta probabilística, escolhida pela facilidade de verificação (completude), não por ser a melhor.
7. **Alcance medido só nesta máquina e em Python puro**: 56 a 2 899 candidatos/s (documento 04); a fronteira de 7 a 9 nós por 10⁴ a 10⁵ candidatos é uma propriedade do enumerador, não do problema.
8. Sob unigrama, o aprendiz lesionado e L-fix encontram ParAdjacente por um programa diferente do de L-lib+f: a economia da biblioteca não é "resolver ou não", é custo. A frase "L-fix não resolve T3" vale só para a política por tamanho a 2 × 10⁴.
9. O registro do primeiro lançamento abortado não foi guardado (o `runs/em-s10002-tamanho` presente é o relançamento com a correção, com o mesmo código salvo pela correção, cujo hash está em `fontes`).
