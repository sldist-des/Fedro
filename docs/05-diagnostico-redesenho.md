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

(preenchido a partir de `runs/em-*`; ver seções 2.1 a 2.7)

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

(preenchido a partir de `runs/em-s10002-tamanho` e `runs/em-s10002-unigrama`)

## 5. Veredito pelo critério central e próxima intervenção

(ver seção 5)

## 6. Comandos executados e testes

(ver seção 6)

## 7. Desvios e limitações

(ver seção 7)
