# Protocolo experimental

## Documento 02 — Dois experimentos, comparação e ordem de execução

**Status:** v0.1 (2026-10-29). Pré-registro em rascunho. Sem código. Sem arquitetura definitiva. Depende do documento 01 na versão v0.2, em particular das camadas L0–L3 (1.2-bis), das hipóteses H-B1, H-B2, H-B3 (1.3-bis), dos requisitos funcionais R1–R6 (4.2-bis) e dos critérios por camada (4.4-bis).

**Rótulos epistêmicos:** [P] prova formal; [E] evidência empírica; [C] resultado computacional; [F] interpretação filosófica; [H] hipótese; [R] condição de refutação; [A] questão aberta.

### Sumário

0. Regras do protocolo
1. O que cada experimento pode e não pode testar
2. Experimento 1 — Abstração sob dialética em micro-mundo de grades (versão corrigida)
3. Experimento 2 — Agente sensório-motor em micro-mundo sem definições (desenho preliminar)
4. Comparação dos dois experimentos
5. Ordem de execução e justificativa
6. Status epistêmico das afirmações deste protocolo
7. Questões abertas preservadas
8. Referências

---

## 0. Regras do protocolo

1. **Regra fundamental.** A definição mensurável de aprendizagem usada aqui (transições de eficiência em recursos finitos, camada L1, mais testes de política de generalização, camada L3) é a primeira operacionalização do programa. Não é uma definição da natureza da inteligência. Nenhum resultado deste protocolo será descrito como evidência de inteligência geral.
2. **Pré-registro integral.** Antes de qualquer execução, ficam publicados com hash: a dotação inicial E0 e sua variante E0' com a demonstração de equivalência; as definições formais e as implementações de referência de todos os conceitos; as distribuições de amostragem; as partições de dados; os orçamentos; as tolerâncias; a matriz de resultados. Qualquer mudança posterior é uma nova versão do protocolo, não uma correção.
3. **Nenhum critério de sucesso depende de leitura humana de programas ou de pesos.** Toda medida é comportamental, de custo ou de invariância.
4. **Resultados negativos são resultados.** A matriz de resultados (2.13 e 3.6) diz o que cada saída significa antes de ela ocorrer.
5. **Finito, nunca assintótico.** Pelo teorema da invariância (documento 01, 1.2-bis) [P], nenhuma afirmação de separação assintótica é admissível. Reportam-se tamanhos de efeito a orçamentos declarados e a forma da curva de vantagem em função do orçamento.
6. **Custo integral.** Toda comparação entre aprendizes é feita a custo cumulativo total igual, incluindo aprendizagem anterior, construção de biblioteca, consultas ao oráculo e avaliação.
7. **Hipóteses neutras.** Para cada controle, as duas saídas possíveis têm leitura pré-registrada. Nenhum controle é desenhado para falhar.

---

## 1. O que cada experimento pode e não pode testar

| Alvo | Experimento 1 (grades) | Experimento 2 (agente) |
|---|---|---|
| L0 expressividade teórica | Trivial, não testada | Trivial, não testada |
| L1 expressividade efetiva (H-B1) | **Sim**, alvo principal | Sim, para espaço, objeto, identidade, quantidade e causa |
| L2 mudança qualitativa (H-B2) | **Não, por construção**: toda abstração é uma definição | Candidato apenas: só se a instanciação for relacional ou contínua; sem critério validado [A] |
| L3 capacidades de generalização (H-B3) | Parcial: teste de política de generalização entre famílias | Parcial: transferência de corpo e de mundo |
| Fundamentação (R1–R6 contínuos) | Não: símbolos dados | **Sim**, alvo principal |
| Regime de experiência | Dialético (oráculo de contraexemplos) | Ativo (ação com consequências), sem oráculo |
| H-C revisão de método | Não: procedimento de busca fixo | Não: regra de plasticidade fixa |
| Inteligência geral | Não | Não |

---

## 2. Experimento 1 — Abstração sob dialética em micro-mundo de grades (versão corrigida)

### 2.1 Pergunta e hipóteses

**Pergunta.** Em um micro-mundo com dotação inicial declarada e pequena, a construção de abstrações a partir das próprias soluções, sob um protocolo de contraexemplos, produz, a custo cumulativo total igual, (i) vantagem de eficiência em recursos finitos sobre o mesmo aprendiz sem construção, (ii) que sobrevive à mudança de fatoração da base, (iii) que exibe estrutura de pré-requisitos e (iv) que transfere apenas a estrutura análoga e a portadores novos?

**Hipóteses testadas.** H-B1 integralmente; H-B3 pelo teste de política de generalização (2.9, medida M9). H-B2 não é testada (seção 1).

### 2.2 Ambiente e definições formais dos conceitos

**Instâncias.** Uma grade de tamanho n é uma função g de {1..n} × {1..n} em {0, 1}; o valor 1 é "preto". Tamanhos de treino: n em {3, 4, 5, 6}. Tamanhos de extrapolação: n em {7, 8, 9}.

**Definições auxiliares (só para o ambiente e o oráculo; o aprendiz não as recebe).** Duas células são vizinhas se diferem em exatamente uma coordenada por exatamente uma unidade (vizinhança de 4). Um componente é um conjunto maximal de células pretas conexo por vizinhança. Uma célula toca a borda se alguma coordenada é 1 ou n. A metade esquerda são as colunas 1 até piso(n/2); a direita, as colunas n − piso(n/2) + 1 até n; a coluna central, se n é ímpar, não pertence a nenhuma.

**Conceitos-alvo, com definição formal.** Cada conceito é um predicado sobre grades de qualquer tamanho.

| Família | Nome | Definição formal | Invariâncias declaradas |
|---|---|---|---|
| F1 | TopoCheio | Para todo j, g(1, j) = 1 | Reflexão horizontal |
| F1 | ParDireita | Existe (i, j) com j < n, g(i, j) = 1 e g(i, j+1) = 1 | Reflexão horizontal, reflexão vertical |
| F1 | LinhaOcupada | Para todo i existe j com g(i, j) = 1 | Reflexão horizontal, reflexão vertical |
| F2 | UmComponente | O número de componentes é exatamente 1 | Rotações, reflexões, transposição |
| F2 | DoisSeparados | O número de componentes é exatamente 2 | Rotações, reflexões, transposição |
| F2 | MaiorTocaBorda | Existe um componente de cardinalidade máxima que contém uma célula de borda | Rotações, reflexões, transposição |
| F3 | LinhasIguais | Para todo i, a cardinalidade de {j : g(i, j) = 1} é igual à de {j : g(1, j) = 1} | Reflexão horizontal |
| F3 | MetadesIguais | A cardinalidade das células pretas na metade esquerda é igual à da metade direita | Reflexão horizontal |
| F3 | ComponentesVsVazias | O número de componentes é igual ao número de linhas i sem célula preta | Reflexão horizontal |
| F1' | CantoSupEsq | g(1, 1) = 1 | Nenhuma |
| F1' | Diagonal | Para todo i, g(i, i) = 1 | Transposição |
| F1' | ColunaDoisVazia | Para todo i, g(i, 2) = 0 | Reflexão vertical |
| F4 | (adversarial) | Três conceitos escritos por um revisor independente após o congelamento de E0, com definições formais seladas; revelados só após as execuções principais | Declaradas pelo revisor |

A família F1' é o distrator: conceitos rasos sem componente conexo e sem comparação de cardinalidades. Os conceitos de F2 exigem a noção de componente; os de F3, a de igualdade de cardinalidades, sem contagem dada; ComponentesVsVazias exige ambas.

**Implementações de referência.** Cada conceito recebe duas implementações independentes: uma por busca em largura explícita sobre a grade, outra por uma formulação declarativa (por exemplo, uma consulta em lógica de primeira ordem finita ou em uma biblioteca de grafos). As duas devem concordar em todas as grades de n até 4 (enumeração exaustiva) e em 10^5 grades aleatórias por tamanho de 5 a 9. Qualquer discordância bloqueia o pré-registro. Testes de propriedade verificam as invariâncias declaradas.

**Distribuição de amostragem.** Para cada conceito e tamanho, as grades são geradas por uma mistura de distribuições de Bernoulli independentes por célula com parâmetro p em {0,20; 0,35; 0,50; 0,65}, com rejeição até obter classes balanceadas. Metade dos negativos são "quase-acertos": obtidos de um positivo pela inversão de uma única célula que muda o rótulo, quando tal célula existe. A geração é determinística por semente. A razão: sob Bernoulli puro com p = 0,5, grades 6 × 6 quase sempre têm um único componente grande, e o conceito UmComponente seria trivialmente desequilibrado.

### 2.3 Dotação inicial E0 e variante E0'

**E0.** Uma linguagem funcional tipada, com tipos Bool, Pos, Grade, Lista(a), e as primitivas:

- sobre grades: `celula : Grade → Pos → Bool`; `posicoes : Grade → Lista(Pos)`; `linhas : Grade → Lista(Lista(Bool))`; `colunas : Grade → Lista(Lista(Bool))`; `vizinhos : Grade → Pos → Lista(Pos)`;
- booleanas: `e`, `ou`, `nao`, `igualB : Bool → Bool → Bool`; `igualP : Pos → Pos → Bool`;
- sobre listas: `vazia?`, `cabeca`, `cauda`, `mapear`, `filtrar`, `algum`, `todos`, `concatenar`;
- recursão: `fix` com combustível igual a n² passos, que devolve `falso` ao esgotar.

Não há: aritmética, contagem, comparação de comprimentos, componente conexo, simetria, coordenadas numéricas acessíveis ao programa. Com esta base, "mesmo comprimento" de duas listas é derivável por recursão simultânea (uma dezena de nós) e "componente conexo" por iteração até ponto fixo sobre vizinhos (algumas dezenas de nós). O combustível torna toda função total sobre o domínio finito, o que restringe a expressividade a uma classe primitiva-recursiva limitada e declarada.

**E0'.** Expressivamente equivalente, fatorada de outro modo: `linhas`, `colunas` e `posicoes` são substituídas por uma única `dobra : (Pos → a → a) → a → Grade → a` sobre as posições em ordem fixa, mais `sucessorLinha` e `sucessorColuna` parciais; `algum` e `todos` não são primitivas; listas são substituídas por conjuntos com `membro?`, `inserir`, `escolher` e `vazio?`.

**Demonstração de equivalência (exigida pela revisão).** A equivalência é demonstrada por exibição, antes das execuções, de duas tabelas de compilação:

- para cada primitiva de E0, um termo de E0' com o mesmo comportamento sobre todas as grades de n até 9, com seu tamanho em nós, e o maior tamanho é a constante c(E0 → E0');
- o inverso, com a constante c(E0' → E0).

A verificação é por teste exaustivo para n até 4 e por amostragem para n de 5 a 9. Com as duas compilações, toda função definível em uma linguagem é definível na outra com acréscimo de tamanho no máximo linear no número de ocorrências de primitivas, o que é a equivalência relevante [P, dado o domínio finito e as compilações exibidas]. As constantes c são publicadas, e também a menor descrição conhecida de cada conceito-alvo em cada linguagem, obtida por busca com orçamento grande, declarada como limite superior.

O que esta demonstração garante: qualquer diferença de desempenho entre E0 e E0' é efeito de fatoração, não de expressividade. O que não garante: que os custos de busca sejam iguais, porque o ponto do controle C3 é justamente que não são.

### 2.4 Aprendizes

Todos usam o mesmo procedimento de busca quando aplicável: enumeração tipada por tamanho crescente, ordenada por comprimento de descrição, com poda por tipo, sob orçamento medido em nós avaliados.

- **L-mem**: tabela de instâncias vistas, com vizinho mais próximo por distância de Hamming para instâncias novas e rejeição para tamanhos novos.
- **L-fix**: busca em E0 fixa.
- **L-lib**: busca em E0 mais um passo de compressão após cada conceito aceito: os programas das soluções são refatorados e os fragmentos recorrentes viram primitivas nomeadas, no espírito de DreamCoder (Ellis et al. 2021) e Stitch (Bowers et al. 2023), com um único hiperparâmetro de compressão fixado em validação.
- **L-nn-conv**: rede convolucional pequena com agregação global, treinada com os mesmos exemplos e contraexemplos. Viés declarado: equivariância a translação.
- **L-nn-seq**: rede sequencial sem convolução, sobre a grade linearizada. Viés declarado: nenhum espacial.
- **L-mdl**: um modelo neural pequeno ajustado por minimização de comprimento de descrição em tempo de teste, por tarefa, no espírito de Liao e Gu (2025). Viés declarado: o da arquitetura.
- **L-teto**: E0 acrescida de `componentes` e `mesmoComprimento` como primitivas. Limite superior.

Para os aprendizes neurais, são reportadas duas condições: sem aumento de dados, e com aumento de dados pelas invariâncias declaradas de cada conceito. O aumento é uma adição explícita a E0 e é tratado como tal.

### 2.5 Contabilização integral de custo

**Unidade de custo.** Para aprendizes simbólicos, número de nós de programa avaliados sobre grades, mais o número de avaliações de grades. Para aprendizes neurais, número de operações de ponto flutuante. Para comparação entre os dois, tempo de parede em hardware fixo com semente fixa, reportado ao lado da unidade nativa. As duas escalas são reportadas; não se afirma comparabilidade exata entre elas.

**Livro-razão.** Para cada aprendiz e cada execução, registram-se separadamente: custo de busca por conceito; custo de compressão de biblioteca por passo; número de consultas ao oráculo e custo de cada busca por contraexemplo (que é custo do ambiente, não do aprendiz, mas é reportado); custo de avaliação em teste. O custo cumulativo total é a soma, e é o que se compara.

**Comparação a custo igual.** L-fix recebe, em cada ponto do currículo, orçamento tal que seu custo cumulativo total iguale o de L-lib até aquele ponto, incluindo a compressão de L-lib. O mesmo para L-teto e para os neurais, na escala nativa.

**Curvas de amortização.** Para cada aprendiz: conceitos aceitos em função do custo cumulativo. O ponto de cruzamento entre L-lib e L-fix, se existir, é um resultado primário. Custo de aprendizagem anterior nunca é tratado como afundado: ele entra no eixo.

### 2.6 Finito versus assintótico

Orçamentos por conceito de B, 3B, 10B e 30B, com B fixado em validação de modo que L-fix resolva toda a família F1 em B. Para cada orçamento, reporta-se a vantagem de L-lib sobre L-fix em conceitos aceitos e em custo. A forma esperada, se H-B1 vale neste regime, é uma vantagem que diminui com o orçamento, porque L-fix eventualmente alcança os conceitos profundos. A forma da curva é o resultado; nenhuma afirmação de separação assintótica é feita, por 1.2-bis do documento 01 [P].

### 2.7 Protocolo de dados sem vazamento

- **Reservatórios.** P_oráculo: grades de n de 1 a 5, de onde o oráculo retira contraexemplos. D_val: grades de n de 3 a 6, usadas só para fixar hiperparâmetros com a família F1. D_teste_int: grades de n de 3 a 6. D_teste_ext: grades de n de 7 a 9. D_teste_remap: grades de D_teste_int e D_teste_ext com codificação de superfície alterada (três cores, das quais só uma conta como "preta"). D_teste_port: instâncias de outros portadores (2.11).
- **Disjunção.** Toda grade é serializada e seu hash registrado; os reservatórios são disjuntos por construção e a disjunção é verificada antes da execução.
- **Publicação.** O hash de cada reservatório serializado é publicado no pré-registro; as grades só são reveladas após as execuções.
- **Hiperparâmetros.** Orçamento B, número máximo de rodadas K, parâmetro de compressão de L-lib, taxa de aprendizagem e número de épocas dos neurais: fixados em D_val com a família F1 e nunca mais tocados. As famílias F2, F3, F1' e F4 não são usadas em nenhuma etapa de ajuste.
- **Família adversarial F4.** Escrita por um revisor independente depois do congelamento de E0 e do pré-registro, com hash selado publicado antes das execuções e definições reveladas depois. Seu papel é controlar o risco de que E0 tenha sido desenhada, mesmo sem intenção, para as famílias F2 e F3. É a defesa contra o caso AM.

### 2.8 Protocolo dialético

Para cada conceito c, em ordem de currículo F1, depois F2, depois F3, com F1' e F4 em braços próprios:

1. O oráculo fornece 2 positivos e 2 negativos de D_treino (n de 3 a 6).
2. O aprendiz produz uma hipótese h consistente com os dados, dentro do orçamento.
3. O oráculo busca um contraexemplo mínimo em P_oráculo: exaustivamente para n de 1 a 4, em ordem de tamanho e depois de ordem lexicográfica do vetor linha a linha; para n = 5, em um reservatório fixo de 10^5 grades por semente. Se não há contraexemplo, o conceito é aceito provisoriamente.
4. O aprendiz revisa h. Repete até K = 12 rodadas. Todas as hipóteses são registradas.
5. Avaliação em D_teste_int, D_teste_ext, D_teste_remap e D_teste_port.

### 2.9 Medidas

- **M1** Conceito aceito dentro do orçamento (sim/não), por orçamento.
- **M2** Número de rodadas dialéticas até aceitação.
- **M3** Custo cumulativo total até aceitação (2.5).
- **M4** Acurácia em D_teste_int, D_teste_ext, D_teste_remap, D_teste_port.
- **M5** Taxa de falsos positivos em negativos quase-acertos.
- **M6** Localidade da revisão: distância de edição entre hipóteses sucessivas, e se a nova hipótese reutiliza ou cria uma abstração.
- **M7** Regressão: acurácia nos conceitos anteriores após cada novo conceito.
- **M8** Identidade comportamental das abstrações construídas: concordância entre cada primitiva inventada por L-lib e os predicados auxiliares de referência (componentes, mesmo comprimento) em grades aleatórias uniformes de todos os tamanhos.
- **M9** Política de generalização (H-B3): para cada família nova, após 1 positivo e 1 negativo, a distribuição das cinco primeiras hipóteses do aprendiz, antes e depois do treino numa família relacionada e, separadamente, numa família distratora; reporta-se a divergência de Jensen–Shannon entre as distribuições e a fração de massa em hipóteses que usam abstrações estruturais.

### 2.10 Controles

- **C1 Orçamento.** L-fix a custo cumulativo igual ao de L-lib (2.5) e aos múltiplos de 2.6.
- **C2 Ordem.** L-lib com F2 antes de F1; com F3 primeiro; com ordem aleatória. Mede pré-requisitos e sensibilidade de custo (critério 3' do documento 01, 4.4-bis), não diferença de ponto final.
- **C3 Base.** Tudo repetido em E0' (2.3). A vantagem de L-lib deve existir nas duas bases; sua magnitude é reportada ao lado das constantes de compilação.
- **C4 Oráculo.** Contraexemplos mínimos substituídos por exemplos aleatórios em número igual.
- **C5 Lesão.** Abstrações de L-lib removidas antes de F3.
- **C6 Distrator.** L-lib treinado em F1' em vez de F1 antes de F2 e F3.
- **C7 Superfície.** Avaliação em D_teste_remap.
- **C8 Biblioteca de programas aleatórios.** L-lib cuja biblioteca é construída por compressão de programas aleatórios de tamanho comparável, sem tarefas. Testa se o conteúdo da biblioteca importa, e não apenas o fato de haver uma.

### 2.11 Transferência real versus heurísticas do ambiente

Uma abstração construída pode ser um atalho específico das grades (por exemplo, "n = 3 e canto preto") em vez de estrutura. Os testes:

- **T1 Invariância.** Para cada conceito, acurácia sob as transformações declaradas em 2.2 deve ser igual à acurácia sem transformação, dentro da tolerância.
- **T2 Portadores.** Os mesmos conceitos abstratos em portadores novos: sequências binárias, onde "componente" é uma corrida de uns e "metades" são as duas metades da sequência; e grafos explícitos dados por listas de adjacência, onde "componente" é componente conexo. A mudança de portador é feita trocando apenas as primitivas de portador (`posicoes`, `vizinhos`, `linhas`, `colunas`) por equivalentes publicados; a biblioteca construída em grades é mantida. Mede-se M3 e M4 no portador novo contra L-fix no portador novo.
- **T3 Transferência negativa.** Após F1', nenhuma redução de custo em F2 e F3 além da variância entre sementes.
- **T4 Reuso.** Cada abstração é anotada com o número de conceitos distintos em que aparece. Abstrações de uso único são reportadas separadamente e contam como indício de heurística, não de conceito.
- **T5 Identidade comportamental.** M8 com limiares pré-registrados: concordância de pelo menos 99% para n até 6 e de pelo menos 95% para n de 7 a 9.

### 2.12 Hipóteses neutras para os controles neurais

A v0.1 previa que a rede convolucional falharia em extrapolação. Isso não é neutro e a evidência é mista: há arquiteturas com viés adequado que extrapolam em tamanho para alguns predicados, e resultados como o de Liao e Gu (2025) mostram generalização sem pré-treino por compressão. As saídas e suas leituras:

| Saída | Leitura pré-registrada |
|---|---|
| L-nn-conv generaliza em D_teste_int e falha em D_teste_ext | Generalização estatística com viés de translação, sem extrapolação de tamanho neste regime de dados |
| L-nn-conv generaliza em ambos | O viés convolucional mais o regime de dados bastam para estes conceitos; a comparação relevante passa a ser de custo e de M9, e a Alternativa 2 do documento 01 ganha apoio neste domínio |
| L-nn-conv falha mesmo em D_teste_int | Lacuna de eficiência de amostra neste regime; não diz nada sobre capacidade com mais dados |
| L-nn-seq se comporta como L-nn-conv | O viés espacial não é o fator decisivo |
| L-mdl generaliza em ambos | Compressão em tempo de teste basta neste domínio; apoio ao princípio de compressão sem biblioteca explícita |
| L-mdl falha onde L-lib acerta | A biblioteca, não só a compressão, é o fator |

Nenhuma dessas saídas é "fracasso" do programa; cada uma muda o desenho do experimento 2.

### 2.13 Matriz de resultados pré-registrados

Os resultados referem-se a famílias, com múltiplas sementes e intervalos reportados. Nenhum conceito isolado conta.

**Se H-B1 vale neste regime:**

- **S1** A custo cumulativo igual, L-lib aceita a maioria de F2 e F3; L-fix não, em B nem em 3B.
- **S2** S1 persiste em E0' (C3).
- **S3** O custo de F3 após F2 é menor do que após F1' (C6); a lesão C5 elimina o ganho; C8 não o produz.
- **S4** T1 a T5 satisfeitos; em T2, a biblioteca reduz custo também no portador novo.
- **S5** Em C2, há conceitos de F3 não aceitos antes de F2 em nenhuma ordem, e o custo total depende da ordem.
- **S6** Em M9, a política de generalização desloca-se após família relacionada e não após distratora.

**Saídas que enfraquecem ou refutam:**

- **F-a** L-fix a custo igual, ou a 3B, iguala L-lib. Leitura: a vantagem é pequena em relação ao orçamento; H-B1 não confirmada neste regime.
- **F-b** A vantagem desaparece em E0'. Leitura: artefato de fatoração; o critério 2 de demarcação fica validado como necessário; a E0 original é suspeita.
- **F-c** C4 iguala a dialética. Leitura: contraexemplos mínimos não importam neste regime; a correspondência com o elenchus é fraca aqui.
- **F-d** L-lib aceita F3 com abstrações que não passam em T5. Leitura: compressão sem identidade conceitual; é a saída mais informativa para a teoria, porque separa L1 de qualquer noção de conceito.
- **F-e** S1 e S2 valem, S3 ou T2 falham. Leitura: ganho de busca genérico, sem transferência estrutural.
- **F-f** F4 (adversarial) não é aceita por L-lib enquanto F2 e F3 são. Leitura: E0 estava ajustada, mesmo sem intenção, às famílias planejadas; o resultado principal é desvalorizado.
- **F-g** S1 a S6 valem. Leitura: H-B1 e parte de H-B3 demonstradas em micro-mundo simbólico. Nada sobre H-B2, fundamentação, revisão de método ou inteligência geral.

### 2.14 O que o experimento 1 não mostra

Não mostra L2 (toda abstração é uma definição), fundamentação de símbolos (as grades são simbólicas), instanciações contínuas dos requisitos R1–R6, revisão de método (H-C), abertura, nem inteligência geral. Mostra, no melhor caso, H-B1 e um sinal de H-B3 em um domínio onde a verdade de base é exata.

### 2.15 Recursos

CPU, Python, horas de computação por configuração, código na ordem de uma a duas mil linhas, tudo determinístico por semente. O custo humano principal é o pré-registro: definições formais, implementações duplas, compilações E0/E0' e a família F4 por terceiro.

---

## 3. Experimento 2 — Agente sensório-motor em micro-mundo sem definições (desenho preliminar)

### 3.1 Pergunta

Um agente com sensores e motores não interpretados, dotado apenas de instanciações contínuas dos requisitos funcionais R1–R6, adquire capacidades da camada L1 para espaço, distinção entre si e mundo, objeto persistente, identidade ao longo do tempo, quantidade e causa própria, sem que nenhuma dessas noções seja dada? E as capacidades adquiridas são sobre o mundo, e não sobre a fiação dos sensores ou sobre os vieses declarados?

Este experimento é onde as alternativas construtivista-contínua (documento 01, 4.2-bis) e "a arquitetura fez tudo" se enfrentam diretamente.

### 3.2 Capacidades iniciais inevitáveis e sua instanciação

| Requisito | Instanciação neste experimento | Declarado como dado |
|---|---|---|
| R1 Discriminabilidade | Vetor sensorial contínuo s_t com k canais; topologia dada pela métrica euclidiana do espaço de ativações | Sim |
| R2 Sinal de discrepância | Erro de predição de s_{t+1} a partir de (s_t, a_t) e estado interno; só o comparador de **primeira ordem** é dado | Sim, primeira ordem; segunda ordem **não** é dada |
| R3 Plasticidade | Regra de atualização de parâmetros por gradiente do erro de predição; regra fixa | Sim |
| R4 Ordenação de preferência | Implícita na arquitetura e na regra; mais um bônus de exploração por progresso de aprendizagem (Oudeyer, Kaplan e Hafner 2007) | Sim, declarado e ablacionável |
| R5 Persistência | Estado recorrente de dimensão fixa | Sim |
| R6 Ação | Vetor motor a_t com m canais, efeitos desconhecidos | Sim |
| Vieses adicionais, opcionais e ablacionáveis | Prior de lentidão (Wiskott e Sejnowski 2002); gargalo de baixa dimensão | Sim, cada um em braço próprio |
| **Não dados** | Segmentação, coordenadas, identificadores de objeto, slots, contagem, operador de intervenção, detector de mudança de classe de modelo | — |

A ausência do comparador de segunda ordem é deliberada: a questão aberta de 4.2-bis é se ele emerge. Se não emergir e o agente mesmo assim adquirir as capacidades, aprendemos que ele não é necessário para L1 neste regime; se o agente estagnar em um ponto previsível pela ausência desse comparador, aprendemos onde ele é necessário.

### 3.3 Representação de observações e ações

- **Mundo.** Arena bidimensional limitada, tempo discreto, com objetos: discos persistentes, alguns empurráveis por contato, alguns fixos; oclusores opacos; em algumas condições, um "vento" exógeno que desloca objetos. Física determinística com uma pequena componente estocástica declarada.
- **Sensores.** Uma janela local em torno do agente é projetada por uma matriz fixa aleatória em k canais (por exemplo, k = 64), com permutação e sinal aleatórios por semente. O agente nunca recebe a geometria da janela, a permutação ou a matriz. Nada é rotulado.
- **Motores.** m canais (por exemplo, m = 4) mapeados por uma matriz fixa aleatória em deslocamento (dx, dy), com dois canais nulos. O agente não recebe a matriz. A existência de canais nulos é um teste: a dimensionalidade motora efetiva (2) deve ser recuperada, não a nominal (4).
- **Ações.** Escolhidas pelo agente: inicialmente balbucio motor aleatório; depois, exploração dirigida por progresso de aprendizagem. Um braço de controle usa política aleatória durante todo o treino.
- **Observações.** Apenas s_t. Nenhum canal de recompensa externa.

### 3.4 Como detectar a emergência de conceitos elementares

Todos os testes são comportamentais ou preditivos; nenhum inspeciona o estado interno. Os limiares são pré-registrados.

- **Espaço (E-1).** Replicação de Philipona, O'Regan e Nadal (2003): a dimensionalidade do conjunto de comandos motores compensáveis por mudanças sensoriais, estimada a partir do modelo aprendido, deve ser 2 na arena bidimensional e 1 em um corredor unidimensional, independentemente de k, de m e da permutação sensorial.
- **Si e mundo (E-2).** Reaferência: com vento exógeno presente, o erro de predição sob ação própria deve decompor-se em uma parte explicada pela ação e outra não; a surpresa do agente quando as consequências da própria ação são perturbadas deve diferir, em magnitude e em curso temporal, da surpresa quando um objeto externo se move. Critério: separação das duas distribuições de surpresa com área sob a curva pré-registrada.
- **Objeto e permanência (E-3).** Protocolo de violação de expectativa, no formato de Riochet et al. (2022): surpresa em eventos impossíveis (um objeto entra atrás do oclusor e não sai; atravessa uma parede) contra eventos possíveis emparelhados em estatística de baixo nível. Critério: área sob a curva de um classificador de surpresa acima do limiar, e **não** alcançada por um preditor de estatísticas de pixel sem memória (piso).
- **Identidade (E-4).** Dois objetos de dinâmica diferente (velocidades distintas) entram atrás de um oclusor e saem; eventos impossíveis: saída em tempo ou lugar incompatível com continuidade; o número de objetos que saem difere do número que entrou. Critério como em E-3.
- **Quantidade (E-5).** Análogo de desabituação (Xu e Spelke 2000): após exposição a cenas com dois objetos variando em tamanho, espaçamento e posição, surpresa para cenas com três objetos contra cenas novas com dois, com área total e densidade emparelhadas. Critério: surpresa à mudança de número maior que à mudança não numérica emparelhada, com curva de sensibilidade a razão (2 contra 3, 2 contra 4).
- **Causalidade (E-6, teste decisivo).** Fase de treino passiva em que os objetos A e B se movem juntos por causa comum (vento). Teste: o agente empurra A. Um modelo causal prevê que B fica; um modelo associativo prevê que B se move. Mede-se a predição do agente, ou sua surpresa quando B fica contra quando B se move. Braço adicional: agentes que puderam agir durante o treino contra agentes "acorrentados" que receberam a mesma sequência sensorial passivamente, no espírito de Gopnik et al. (2004). Isto testa diretamente o papel de R6.

### 3.5 Como distinguir abstração genuína de regularidades programadas

- **A-1 Permutação sensorial.** Dois agentes com permutações e matrizes sensoriais diferentes, no mesmo mundo, devem produzir as mesmas medidas E-1 a E-6, dentro da tolerância. Se as medidas rastreiam a fiação, não há conceito.
- **A-2 Transferência de corpo.** Após o treino, a matriz motora é trocada. O tempo de recuperação de E-1 e E-2 deve ser muito menor que o tempo de aprendizagem inicial, e E-3 a E-6 devem permanecer. Isso indica que o modelo separa mundo e corpo. Se tudo precisa ser reaprendido, a representação era do laço, não do mundo.
- **A-3 Mudança de mundo.** Corredor unidimensional; física de oclusão diferente. As medidas devem seguir o mundo.
- **A-4 Mundo sem objetos.** Um agente treinado numa arena sem objetos persistentes não deve exibir as assinaturas E-3 a E-5. Se exibir, a assinatura vem da arquitetura, não dos dados.
- **A-5 Ablação dos vieses declarados.** Cada viés opcional (lentidão, gargalo, bônus de exploração) é removido em um braço. Para cada capacidade, reporta-se de quais vieses depende. Uma capacidade que desaparece com a remoção de um viés estava no viés; isto é a forma do caso AM neste experimento, e é reportada como tal, não escondida.
- **A-6 Teto e piso arquiteturais.** Teto: modelo com slots de objeto explícitos. Piso: preditor autorregressivo de pixels sem estado recorrente. Os resultados do agente são posicionados entre os dois.
- **A-7 Política.** Agente curioso contra agente de política aleatória, com o mesmo número de passos. Mede se o currículo autogerado importa.

### 3.6 Resultados que refutariam a hipótese neste regime

- Nada além de E-1 emerge, em qualquer braço: o construtivismo sensório-motor contínuo não passa de espaço neste regime, como na literatura anterior.
- E-3 a E-5 só aparecem no teto com slots: "objeto" é arquitetura.
- As assinaturas de E-3 a E-5 são reproduzidas pelo piso de estatísticas de pixel: a violação de expectativa não mede objeto.
- E-6 falha em todos os braços, inclusive nos agentes ativos: o agente não usa a própria ação como intervenção; a causalidade no sentido de Pearl não é adquirida por este caminho.
- A-1 ou A-2 falham: a representação é da fiação ou do laço, não do mundo.
- A-5 mostra correspondência um a um entre capacidades e vieses declarados: regularidades programadas.

E o resultado positivo mais forte possível: E-1 a E-6 satisfeitos, A-1 a A-5 satisfeitos, com o agente entre piso e teto e sem o comparador de segunda ordem. Leitura pré-registrada: H-B1 para conceitos elementares fundamentados, com instanciação contínua de R1–R6, neste micro-mundo. Nada sobre H-B2, H-C ou inteligência geral.

### 3.7 Riscos e custo

Mais parâmetros livres que o experimento 1, resultados anteriores da literatura estagnados em espaço e objetos simples (documento 01, seção 5, linha 4), risco maior de que a arquitetura explique o resultado, e verdade de base menos exata para E-3 a E-5. Custo computacional baixo a moderado: horas de CPU ou GPU por braço. Custo humano maior no desenho dos eventos emparelhados.

### 3.8 O que o experimento 2 não mostra

Não mostra L2 com critério validado, nem H-C, nem abstração simbólica (número exato, lógica), nem inteligência geral. É o primeiro passo da Direção 1 do documento 01, e o único dos dois experimentos que toca fundamentação e instanciações contínuas.

---

## 4. Comparação dos dois experimentos

| Dimensão | Experimento 1 (grades) | Experimento 2 (agente) |
|---|---|---|
| Pergunta | Re-representação sob dialética produz eficiência não trivial? | Requisitos funcionais contínuos mais ação produzem conceitos elementares fundamentados? |
| Camadas | L1 integral; L3 parcial | L1 para conceitos elementares; L3 parcial; L2 candidato sem critério |
| Hipóteses | H-B1, H-B3 | H-B1 (fundamentada), H-B3; toca a questão aberta de 4.2-bis |
| E0 declarada | Linguagem tipada pequena, simbólica | R1–R6 contínuos mais vieses opcionais ablacionáveis |
| Regime de experiência | Dialético, com oráculo | Ativo, sem oráculo |
| Verdade de base | Exata | Exata para E-1, E-6; aproximada para E-3 a E-5 |
| Força dos controles | Alta: equivalência de bases demonstrável, custo exato, F4 adversarial | Média: permutação, transferência de corpo e ablações; verdade de base parcial |
| Risco de autoengano | Baixo a médio (caso AM mitigado por C3 e F4) | Médio a alto ("a arquitetura fez") |
| Custo | Baixo | Baixo a moderado |
| Reprodutibilidade | Determinística | Determinística por semente, mais sensível a hiperparâmetros |
| O que o sucesso significa | H-B1 em micro-mundo simbólico | H-B1 fundamentada, com instanciação contínua |
| O que o fracasso significa | Diagnosticável pela matriz 2.13 | Menos diagnosticável; depende das ablações |
| Dependência | Nenhuma | Beneficia-se da calibração dos critérios de demarcação pelo experimento 1 |

---

## 5. Ordem de execução e justificativa

**Executar primeiro o experimento 1.** Razões:

1. **Calibração do instrumento.** A questão prioritária do programa é a demarcação entre adquirido e implícito (documento 01, seção 9). O experimento 1 calibra os quatro critérios de L1 num caso em que a verdade de base é exata, o custo é contável sem ambiguidade e a equivalência de bases é demonstrável. Os mesmos critérios são depois aplicados ao experimento 2, onde cada um deles é mais difícil: a permutação sensorial é o análogo da mudança de base, a ablação de vieses é o análogo do critério de custo, a transferência de corpo é o análogo da transferência estrutural.
2. **Diagnosticabilidade.** A matriz 2.13 dá leitura para cada saída. O experimento 2 tem mais caminhos para um resultado ambíguo.
3. **Custo e tempo.** Semanas de trabalho humano, horas de computação.
4. **Independência das conclusões.** Os dois experimentos testam coisas diferentes; o experimento 2 é executado **em qualquer caso** após o experimento 1. O resultado do primeiro muda o desenho do segundo em pontos específicos: se F-b (artefato de base), as ablações A-5 do experimento 2 ganham peso e um braço adicional com vieses alternativos é acrescentado; se F-d (compressão sem identidade), a medida M8 é transposta para o experimento 2 como critério de identidade comportamental dos estados internos; se S1 a S6, a aprendizagem de biblioteca entra como variante simbólica do modelo do agente para comparação com a variante contínua.

**Preparação paralela permitida.** A replicação de Philipona, O'Regan e Nadal (2003) (E-1 isolada) pode ser executada em paralelo como validação de infraestrutura, porque é replicação de resultado publicado e não produz alegação nova.

**O que não deve acontecer.** O programa não deve parar no experimento 1, qualquer que seja o resultado, porque ele não toca fundamentação, instanciações contínuas, nem L2.

---

## 6. Status epistêmico das afirmações deste protocolo

| Afirmação | Status |
|---|---|
| Para E0 universal, toda função computável é expressável | [P] |
| Qualquer re-representação fixa altera o comprimento de descrição por no máximo uma constante aditiva (teorema da invariância) | [P] |
| A busca de Levin é ótima até fator constante | [P] |
| Com as compilações exibidas, E0 e E0' definem as mesmas funções sobre o domínio finito | [P], condicional à exibição e à verificação |
| Distribuições observacionais não identificam, em geral, a estrutura causal | [P] |
| Aprendizagem de biblioteca reduz custo de busca em domínios estreitos | [C] (Ellis et al. 2021; Bowers et al. 2023) |
| Compressão por tarefa em tempo de teste resolve parte do ARC-AGI-1 sem pré-treino | [C] (Liao e Gu 2025; valor reportado pelos autores) |
| Humanos exibem efeitos de ordem de currículo e caminho de jardim explicados por biblioteca de conceitos | [E/C] (Zhao, Lucas e Bramley 2024) |
| Bebês de 6 meses discriminam numerosidades grandes por razão | [E] (Xu e Spelke 2000) |
| A dimensionalidade do espaço é inferível de contingências sensório-motoras com sensores não interpretados | [C] (Philipona, O'Regan e Nadal 2003) |
| Crianças aprendem estrutura causal por intervenção | [E] (Gopnik et al. 2004) |
| A percepção categórica emerge em redes genéricas | [C] (Damper e Harnad 2000) |
| O mapa parâmetro-função de redes profundas tem viés de simplicidade | [C] (Valle-Pérez, Camargo e Louis 2019) |
| Violação de expectativa mede representação de objeto | [F], interpretação da literatura desenvolvimental; o protocolo trata como hipótese operacional com piso de controle |
| A vantagem de L-lib, se existir, diminuirá com o orçamento | [H] |
| O comparador de segunda ordem pode emergir sem ser dado | [A] |
| L2 tem critério operacional distinto de L1 | [A] |
| Sucesso em qualquer dos experimentos é evidência de inteligência geral | Negado por regra do protocolo |

---

## 7. Questões abertas preservadas

1. Se existe critério operacional para L2 que não colapse em L1 (documento 01, 4.4-bis). Nenhum dos dois experimentos o fornece.
2. Se o comparador de segunda ordem (erro de classe de modelo) pode ser adquirido por um sistema contínuo sem laço externo desenhado para isso. O experimento 2 observa, não decide.
3. Se a vantagem de re-representação em recursos finitos é grande o bastante para importar fora de micro-mundos. O experimento 1 mede em um micro-mundo.
4. Se sistemas estatísticos em escala exibem H-B3 sem mecanismo construtivo. O programa de controle do documento 01 (seção 7) permanece obrigatório e não está coberto por este protocolo.
5. Se a unidade de análise correta é o indivíduo ou uma população com transmissão (Objeção 4). Nenhum dos experimentos toca isso.
6. Se o regime dialético com oráculo tem análogo natural sem professor. O experimento 2 é o primeiro passo, com ambiente e sem oráculo.

---

## 8. Referências

As referências gerais estão no documento 01 (seções 10 e "Referências acrescentadas na v0.2"). Específicas deste protocolo:

- Bowers, M., Olausson, T. X., Wong, L., Grand, G., Tenenbaum, J. B., Ellis, K. e Solar-Lezama, A. (2023). "Top-down synthesis for library learning". *Proceedings of the ACM on Programming Languages* 7 (POPL).
- Ellis, K. et al. (2021). "DreamCoder: bootstrapping inductive program synthesis with wake-sleep library learning". *PLDI 2021*.
- Gopnik, A. et al. (2004). "A theory of causal learning in children: causal maps and Bayes nets". *Psychological Review* 111(1): 3–32.
- Liao, I. e Gu, A. (2025). "ARC-AGI without pretraining". arXiv:2512.06104.
- Oudeyer, P.-Y., Kaplan, F. e Hafner, V. V. (2007). "Intrinsic motivation systems for autonomous mental development". *IEEE Transactions on Evolutionary Computation* 11(2): 265–286.
- Philipona, D., O'Regan, J. K. e Nadal, J.-P. (2003). "Is there something out there? Inferring space from sensorimotor dependencies". *Neural Computation* 15(9): 2029–2049.
- Riochet, R. et al. (2022). "IntPhys 2019: a benchmark for visual intuitive physics understanding". *IEEE Transactions on Pattern Analysis and Machine Intelligence* 44(9).
- Wiskott, L. e Sejnowski, T. J. (2002). "Slow feature analysis: unsupervised learning of invariances". *Neural Computation* 14: 715–770.
- Xu, F. e Spelke, E. S. (2000). "Large number discrimination in 6-month-old infants". *Cognition* 74: B1–B11.
- Zhao, B., Lucas, C. G. e Bramley, N. R. (2024). "A model of conceptual bootstrapping in human cognition". *Nature Human Behaviour* 8: 125–136.
- Li, M. e Vitányi, P. (2008). *An Introduction to Kolmogorov Complexity and Its Applications*, 3ª ed. Springer.
- Levin, L. A. (1973). "Universal sequential search problems". *Problems of Information Transmission* 9(3): 265–266.
- Damper, R. I. e Harnad, S. R. (2000). "Neural network models of categorical perception". *Perception & Psychophysics* 62(4): 843–867.
- Valle-Pérez, G., Camargo, C. Q. e Louis, A. A. (2019). "Deep learning generalizes because the parameter-function map is biased towards simple functions". *ICLR 2019*.
