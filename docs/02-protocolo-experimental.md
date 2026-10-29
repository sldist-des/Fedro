# Protocolo experimental

## Documento 02 — Dois experimentos, comparação e ordem de execução

**Status:** **v0.2** (2026-10-29). Pré-registro em rascunho. Sem código do experimento. Sem arquitetura definitiva. Depende do documento 01 (v0.2, com a nota v0.3 em 1.2-bis). A v0.1 deste documento está no histórico do repositório (commit `48d616d`).

**Rótulos epistêmicos:** [P] prova formal; [E] evidência empírica; [C] resultado computacional; [F] interpretação filosófica; [H] hipótese; [R] condição de refutação; [A] questão aberta.

### Histórico de revisões

**v0.1 → v0.2 (segunda auditoria independente).**

| # | Seção | A v0.1 dizia | A v0.2 corrige para |
|---|---|---|---|
| 1 | 0.5, 2.6 | "Pelo teorema da invariância, nenhuma afirmação assintótica é admissível" | O teorema da invariância vale para máquinas universais; E0 não é universal, tem combustível e domínio finito. O argumento é substituído pelo **lema de inlining** para linguagens tipadas finitas e pela observação de que não há parâmetro assintótico num domínio finito. A regra "finito, nunca assintótico" permanece, com outra justificativa (seção 2.0) |
| 2 | 2.3 | Equivalência de E0 e E0' "demonstrada" por compilações mais testes amostrais, rotulada [P] | Equivalência delimitada formalmente: traduções composicionais com lemas por primitiva, provados por indução estrutural sobre uma semântica finita truncada e comum. Testes amostrais são testes da implementação dos tradutores, nunca prova (seção 2.3) |
| 3 | 2.2 | Mistura de Bernoulli com rejeição até balancear | Auditoria numérica das frequências (seção 2.2.2, `analysis/`): `LinhasIguais` em 9×9 tem frequência da ordem de 2 × 10⁻⁵; `ComponentesVsVazias` é degenerado (2 × 10⁻⁴) e foi retirado; vários conceitos têm positivos concentrados em um único valor de p, o que cria um **confundidor de densidade**. Geradores construtivos, negativos emparelhados em densidade e avaliação natural separada (seção 2.2.3) |
| 4 | 2.2 | Três conceitos por família | Potência do teste de sinal com três conceitos é zero. Famílias geradas por **esquemas** com pelo menos 20 conceitos-alvo no desfecho primário, análise pareada por conceito (seção 2.2.4) |
| 5 | 2.8 | Currículo F1 → F2 → F3 | **Bloqueio de bootstrapping** identificado: os primeiros programas de componente conexo e de comparação de cardinalidade têm degraus de 13 a 16 nós (folhas mais abstrações) sem subtarefa natural abaixo deles. Currículo refeito com escada de tarefas-degrau, incluindo tarefas de função por exemplos de entrada e saída; regra de decisão pré-registrada para a variante E0+ (seção 2.8) |
| 6 | 2.11 | Transferência entre grades, sequências e grafos para todos os conceitos | Auditoria por conceito e portador: a família de componentes transfere para sequências e grafos; a de comparação de cardinalidade transfere parcialmente para sequências e não para grafos; `MaiorTocaBorda`, `LinhasIguais` e `PrimeiraUltimaIguais` degeneram em sequências. Critério de não-vazamento do adaptador e controle "só adaptador" (seção 2.11) |
| 7 | 2.7 | F4 adversarial "escrita por terceiro após congelamento" | F4 com dificuldade comparável por faixas de tamanho medidas no piloto, classes de abstração exigidas, geradores auditados, e **oráculo oculto** que responde rótulos e contraexemplos sem revelar definições (seção 2.7.2) |
| 8 | 3.4, 3.5 | Violação de expectativa como medida de objeto; "capacidade que some com a ablação do viés estava no viés" | Separação operacional entre detecção de anomalia, aprendizagem de regularidade, representação de objeto e causalidade (seção 3.4); controles de intervenção fortalecidos e sondas contrafactuais (seção 3.4, E-6); desenho fatorial viés × dados com quatro leituras, substituindo a inferência "dependente de viés = programado" (seção 3.5); critérios funcionais sem pressupor representação simbólica (seção 3.0) |
| 9 | 2.13 | Matriz de resultados | Acrescentadas saídas F-h (bloqueio de currículo) e F-i (confundidor de densidade), e a regra de que nenhum resultado positivo isolado demonstra a hipótese |

### Sumário

0. Regras do protocolo
1. O que cada experimento pode e não pode testar
2. Experimento 1 — Abstração sob dialética em micro-mundo de grades
   - 2.0 Fundamentos formais corrigidos
   - 2.1 Pergunta e hipóteses
   - 2.2 Ambiente, conceitos, auditoria de frequências, geradores, famílias e potência
   - 2.3 E0, E0' e a equivalência delimitada
   - 2.4 Aprendizes
   - 2.5 Contabilização integral de custo
   - 2.6 Finito versus assintótico
   - 2.7 Protocolo de dados sem vazamento e F4 com oráculo oculto
   - 2.8 Currículo, escada de tarefas e bloqueio de bootstrapping
   - 2.9 Protocolo dialético
   - 2.10 Medidas
   - 2.11 Auditoria de transferência
   - 2.12 Controles
   - 2.13 Hipóteses neutras para controles neurais
   - 2.14 Matriz de resultados e critérios de decisão
   - 2.15 Limitações
3. Experimento 2 — Agente sensório-motor em micro-mundo sem definições
4. Comparação dos dois experimentos
5. Ordem de execução
6. Status epistêmico das afirmações deste protocolo
7. Questões abertas preservadas
8. Referências

---

## 0. Regras do protocolo

1. **Regra fundamental.** A definição mensurável de aprendizagem usada aqui (transições de eficiência em recursos finitos, camada L1, mais testes de política de generalização, camada L3) é a primeira operacionalização do programa. Não é uma definição da natureza da inteligência. Nenhum resultado será descrito como evidência de inteligência geral.
2. **Nenhum resultado positivo isolado demonstra a hipótese.** H-B1 só é considerada apoiada por um conjunto de desfechos pré-registrados (2.14) sobre famílias de conceitos, com controles, em duas bases, e com replicação por sementes. Um conceito aceito, um controle favorável, ou uma execução são observações, não demonstrações.
3. **Pré-registro integral.** Antes de qualquer execução confirmatória ficam publicados com hash: E0 e E0' com as traduções e os lemas; definições formais, implementações de referência e geradores de todos os conceitos; distribuições; partições; orçamentos; tolerâncias; a matriz de resultados; a escada de currículo. Qualquer mudança posterior é uma nova versão, não uma correção.
4. **Nenhum critério de sucesso depende de leitura humana de programas ou de pesos.** Toda medida é comportamental, de custo ou de invariância.
5. **Finito, nunca assintótico.** O domínio é finito (grades de 1 a 9) e as linguagens não são universais; não existe parâmetro assintótico. Reportam-se razões finitas de custo a orçamentos declarados (2.0, 2.6).
6. **Custo integral.** Toda comparação é a custo cumulativo total igual, incluindo aprendizagem anterior, construção de biblioteca, consultas ao oráculo e avaliação, e incluindo o aumento do fator de ramificação que uma biblioteca maior impõe à busca.
7. **Hipóteses neutras.** Para cada controle, as saídas possíveis têm leitura pré-registrada. Nenhum controle é desenhado para falhar.
8. **Piloto e confirmatório separados.** O piloto (documento 03) usa sementes, grades e instâncias de conceito próprias. Nada que o piloto tenha exposto entra no desfecho primário confirmatório.

---

## 1. O que cada experimento pode e não pode testar

| Alvo | Experimento 1 (grades) | Experimento 2 (agente) |
|---|---|---|
| L0 expressividade teórica | Não se aplica: E0 não é universal | Não se aplica |
| L1 expressividade efetiva (H-B1) | **Sim**, alvo principal | Sim, para espaço, si/mundo, objeto, identidade, quantidade e causa |
| L2 mudança qualitativa (H-B2) | **Não, por construção**: toda abstração é uma definição | Candidato apenas; sem critério validado [A] |
| L3 capacidades de generalização (H-B3) | Parcial: política de generalização entre famílias | Parcial: transferência de corpo e de mundo |
| Fundamentação (R1–R6 contínuos) | Não | **Sim**, alvo principal |
| Regime de experiência | Dialético, com oráculo | Ativo, sem oráculo |
| H-C revisão de método | Não | Não |
| Inteligência geral | Não | Não |

---

## 2. Experimento 1 — Abstração sob dialética em micro-mundo de grades

### 2.0 Fundamentos formais corrigidos

**O que a v0.1 fez de errado.** Usou o teorema da invariância da complexidade de Kolmogorov, que diz que para máquinas universais U e V existe uma constante dependente apenas do par tal que o comprimento mínimo de descrição de qualquer objeto difere entre U e V por no máximo essa constante, para concluir que "toda vantagem de re-representação é fator constante" e que afirmações assintóticas são vazias. O teorema é verdadeiro **[P]**, mas não se aplica aos aprendizes deste experimento, por três razões: (i) E0 não é universal: tem combustível de recursão, listas truncadas e domínio finito; (ii) a quantidade relevante para um enumerador não é o comprimento de descrição mínimo, e sim o número de candidatos avaliados até encontrar uma solução, que depende da fatoração da linguagem de modo que o teorema não governa; (iii) num domínio finito não há parâmetro que cresça, logo "assintótico" não designa nada. A regra "finito, nunca assintótico" sobrevive por (iii), não por invariância.

**Quatro quantidades que não podem ser confundidas.**

| Quantidade | Definição neste experimento | O que uma biblioteca aprendida muda |
|---|---|---|
| Comprimento de descrição, s_L(f) | Menor tamanho (folhas mais abstrações, seção 2.3) de um termo de L que denota f | Diminui ou mantém (lema de inlining, abaixo) |
| Custo de avaliação, t(p, x) | Passos da semântica operacional de p sobre a entrada x, limitados por combustível | **Não muda**: inlining preserva passos; só memoização mudaria |
| Custo de busca, C_L(f, B) | Soma, sobre os candidatos enumerados até a solução dentro do orçamento B, de (custo de avaliação sobre os exemplos) | Pode diminuir muito, pode aumentar: menos profundidade, mas mais ramificação |
| Recursos limitados | Orçamento B de candidatos avaliados por tarefa; combustível F(n) por recursão; truncamento de listas em F(n) | Não muda; é o que torna a diferença entre s_L e s_{L+ℓ} decisiva |

**Lema de inlining (versão finita do que a v0.1 queria dizer).** Seja L uma linguagem tipada com termos fechados e tamanho |t| = número de folhas mais número de abstrações. Seja ℓ um termo fechado de L e L+ℓ a linguagem que acrescenta a constante c_ℓ com [[c_ℓ]] = [[ℓ]] e |c_ℓ| = 1. Então, para todo f denotável: (a) s_{L+ℓ}(f) ≤ s_L(f), porque todo termo de L é termo de L+ℓ; (b) s_L(f) ≤ s_{L+ℓ}(f) + k·(|ℓ| − 1), em que k é o número de ocorrências de c_ℓ num termo mínimo de L+ℓ, porque substituir cada ocorrência pelo corpo de ℓ dá um termo de L com a mesma denotação (por beta-redução, com a mesma semântica de combustível, já que inlining não altera a contagem de passos de `fix`); logo (c) s_L(f) ≤ |ℓ|·s_{L+ℓ}(f). Para uma biblioteca de m entradas, aplica-se o lema m vezes **[P, trivial e exato para esta classe de linguagens]**.

**O que o lema implica e o que não implica.** Implica que uma biblioteca encurta descrições por um fator limitado por |ℓ| por ocorrência, isto é, uma quantidade finita e específica ao alvo. Não implica nada sobre custo de busca, que depende de (i) quantos candidatos de tamanho até s existem em cada linguagem, uma função que cresce exponencialmente em s com base que **aumenta** quando a biblioteca cresce, e (ii) da poda por tipos e por equivalência observacional. A razão C_L(f, B)/C_{L+ℓ}(f, B) é portanto uma quantidade empírica, finita, que pode ser maior ou menor que 1. **É exatamente isso que o experimento mede.** Nenhuma afirmação de "fator constante" ou "mais que constante" é feita: afirma-se uma razão medida a orçamentos declarados.

**Complexidade de Levin e busca universal.** Também são noções sobre máquinas universais; o análogo finito aqui é o livro-razão de custo da seção 2.5. A nota v0.3 do documento 01 registra a correção.

### 2.1 Pergunta e hipóteses

**Pergunta.** Em um micro-mundo com dotação inicial declarada e pequena, a construção de abstrações a partir das próprias soluções, sob um protocolo de contraexemplos e um currículo com degraus, produz, a custo cumulativo total igual, (i) vantagem de custo em recursos finitos sobre o mesmo aprendiz sem construção, (ii) que persiste sob mudança de fatoração da base, (iii) que exibe estrutura de pré-requisitos e (iv) que transfere apenas a estrutura análoga e a portadores em que a transferência é legítima?

**Hipóteses testadas.** H-B1 integralmente; H-B3 pelo teste de política de generalização (2.10, M9). H-B2 não é testada.

### 2.2 Ambiente, conceitos, auditoria de frequências, geradores, famílias e potência

#### 2.2.1 Instâncias e definições auxiliares

Uma grade de tamanho n é uma função g de {1..n}² em {0, 1}; 1 é "preto". Tamanhos de treino: 3 a 6. Extrapolação: 7 a 9. Vizinhança de 4. Componente: conjunto maximal de células pretas conexo por vizinhança. Borda: alguma coordenada igual a 1 ou a n. Metades: colunas 1 a piso(n/2) e n − piso(n/2) + 1 a n; a coluna central, se n é ímpar, não pertence a nenhuma. Toda definição de conceito é um predicado sobre grades de qualquer tamanho; as definições formais e as duas implementações de referência independentes (busca em largura explícita; formulação declarativa) ficam no pré-registro, com concordância exaustiva para n até 4 e por 10⁵ amostras por tamanho de 5 a 9. Discordância bloqueia o pré-registro.

#### 2.2.2 Auditoria de frequências sob a distribuição natural

Distribuição natural: Bernoulli(p) independente por célula, p uniforme em {0,20; 0,35; 0,50; 0,65}. Fórmulas exatas onde existem; Monte Carlo com 20 000 amostras por célula para conceitos de componentes. O script e a saída completa estão em `analysis/audit_frequencias.py` e `analysis/audit_frequencias_saida.md` **[C]**. Resumo (frequência de positivos sob a mistura):

| Conceito | n = 3 | n = 6 | n = 9 | Diagnóstico |
|---|---|---|---|---|
| TopoCheio | 0,113 | 0,023 | 0,006 | Positivos em 9×9 vêm quase só de p = 0,65 |
| ParDireita | 0,59 | 0,91 | 0,98 | Negativos raros em n ≥ 6, só com p = 0,20 |
| LinhaOcupada | 0,51 | 0,67 | 0,77 | Negativos concentrados em p = 0,20 |
| UmComponente | 0,47 | 0,061 | 0,018 | Em 9×9, 99% dos positivos vêm de p = 0,65 |
| DoisSeparados | 0,36 | 0,105 | 0,039 | Idem, dominado por p = 0,65 |
| MaiorTocaBorda | 0,95 | 0,92 | 0,85 | Negativos raros e esparsos |
| LinhasIguais | 0,136 | 0,002 | **1,7 × 10⁻⁵** | Um positivo a cada ~60 000 grades em 9×9; 4,2 × 10⁻⁵ com p = 0,20 e 6,8 × 10⁻⁶ com p = 0,50 |
| MetadesIguais | 0,35 | 0,14 | 0,10 | Aceitável |
| ComponentesVsVazias (v0.1) | 0,11 | 0,018 | **2,1 × 10⁻⁴** | Degenerado; retirado |
| LinhaIgualColuna (candidato) | 0,21 | 0,003 | 2,5 × 10⁻⁵ | Só com gerador construtivo |
| PrimeiraUltimaIguais (novo) | 0,35 | 0,25 | 0,20 | Bom |
| TodosMesmoTamanho (novo, F2×F3) | 0,65 | 0,106 | 0,022 | Bimodal em p (0,20 e 0,65) |
| NenhumaIsolada (novo) | 0,42 | 0,165 | 0,070 | Dominado por p = 0,65 em n grande |
| TresComponentes (novo) | 0,115 | 0,151 | 0,053 | Dominado por p = 0,65 em n grande |
| ExisteComponenteReto (novo) | 0,25 | 0,55 | 0,74 | Negativos concentrados em p = 0,65 |
| ComponentesIgualLinha1 (novo) | 0,28 | 0,086 | 0,043 | Aceitável |

**Duas consequências.** Primeira: rejeição simples é inviável ou enviesada para vários conceitos; `LinhasIguais` exige da ordem de 6 × 10⁴ sorteios por positivo em 9×9 e os positivos obtidos são extremos. Segunda, e mais grave: para a maioria dos conceitos, os positivos e os negativos sob a mistura diferem sistematicamente em **densidade** (fração de células pretas). Um classificador por limiar de densidade obteria acurácia balanceada alta em conjuntos "balanceados por rejeição", sem representar o conceito. A v0.1 não controlava isto. É a saída F-i da matriz 2.14.

#### 2.2.3 Geradores: distribuição de desenho e distribuição natural

Dois regimes de avaliação, sempre reportados separadamente.

**Distribuição de desenho (treino, oráculo, teste principal).** Para cada conceito c e tamanho n:

- **Positivos construtivos.** Um gerador específico por esquema (abaixo), que produz um positivo diretamente, seguido de verificação pelas duas implementações de referência; rejeição apenas se a verificação falhar (por exemplo, fusão acidental de componentes). Os geradores são publicados e auditados: para cada (c, n) reporta-se a taxa de aceitação e a distribuição de densidade dos positivos.
- **Negativos emparelhados em densidade.** Para cada positivo, um negativo com **o mesmo número de células pretas**, obtido por: (a) permutação aleatória das células, verificada negativa; ou (b) **quase-acerto por troca**: aplicação do menor número de trocas (uma célula preta e uma branca trocam de lugar) que inverte o rótulo, encontrado por busca local com reinícios. Metade dos negativos de cada tipo. Trocas, não inversões, para preservar densidade.
- **Verificação do confundidor.** Em cada conjunto de desenho, a acurácia balanceada de um classificador por limiar de densidade, ajustado no próprio conjunto, deve ser ≤ 0,55. Caso contrário o conjunto é rejeitado e o gerador revisto.

**Esquemas de geradores construtivos.**

| Esquema | Geração de positivos |
|---|---|
| Cardinalidade de A igual à de B (regiões disjuntas) | Sortear k; escolher k células de A e k de B uniformemente; preencher o resto por Bernoulli(p) com p sorteado |
| Para toda linha, cardinalidade igual à da linha 1 | Sortear k; cada linha recebe um k-subconjunto uniforme de colunas |
| Cardinalidade de A no máximo a de B | Sortear k_A ≤ k_B; preencher como acima |
| Número de componentes igual a m | Semear m passeios aleatórios de comprimento sorteado, com faixa de separação de uma célula; verificar contagem; rejeitar fusões |
| Todos os componentes com propriedade P | Semear componentes gerados sob P (retos, de tamanho fixo, tocando a borda); verificar |
| Existe componente com P | Um componente sob P mais ruído esparso verificado |
| Conceitos rasos F1 e F1' | Construção direta mais preenchimento por Bernoulli |

**Distribuição natural (avaliação independente, obrigatória).** Conjuntos de teste sorteados da mistura de Bernoulli sem balanceamento, 10⁵ grades por tamanho, com hash publicado. Reportam-se taxa-base, precisão, revocação, coeficiente de correlação de Matthews, e o desempenho do classificador trivial de maioria. Para conceitos com taxa-base abaixo de 10⁻³ num tamanho, a avaliação natural mede apenas especificidade, e isso é dito. A avaliação natural é a resposta à pergunta "o programa aprendido funciona no mundo de onde os exemplos não vieram".

**Contraexemplos difíceis para o oráculo.** Dado uma hipótese h e o conceito c, o oráculo procura a menor grade em que h e c discordam, com ordem de minimalidade (n, número de pretas, ordem lexicográfica linha a linha): exaustivamente para n de 1 a 4; para n de 5 a 6, num reservatório fixo por semente de positivos construtivos, negativos emparelhados e quase-acertos, seguido de busca local por trocas que maximiza a discordância mantendo o número de pretas mínimo. O caso difícil, c raro e h "sempre falso", é coberto pelos positivos construtivos.

#### 2.2.4 Famílias por esquema, tarefas independentes e potência

**Por que três conceitos não bastam.** O desfecho primário é pareado por conceito (L-lib contra L-fix a custo igual). Com k conceitos, o teste de sinal unilateral a α = 0,05 tem potência (auditoria em `analysis/`, [C]):

| k conceitos | π = 0,7 | π = 0,8 | π = 0,9 |
|---|---|---|---|
| 3 | 0,00 | 0,00 | 0,00 |
| 10 | 0,15 | 0,38 | 0,74 |
| 20 | 0,42 | 0,80 | 0,99 |
| 30 | 0,73 | 0,97 | 1,00 |

em que π é a probabilidade de vantagem por conceito. Sementes não são unidades independentes para uma afirmação sobre famílias; agregam-se por maioria dentro de cada conceito. **Exigência: pelo menos 20 conceitos-alvo no desfecho primário**, idealmente 30.

**Famílias geradas por esquemas.** Os esquemas vivem no ambiente; o aprendiz só recebe exemplos e contraexemplos.

- **F2 (componentes):** número de componentes em S, para S em {= 1, = 2, = 3, ≥ 2, ≤ 2}; existe componente com P, para P em {toca a borda, contém um canto, é reto, tem pelo menos 3 células}; todos os componentes têm P, para P em {reto, pelo menos 2 células, toca a borda}. Doze conceitos.
- **F3 (comparação de cardinalidades):** cardinalidade de A igual à de B, para pares de regiões em {linha 1, linha n, coluna 1, coluna n, metade esquerda, metade direita}, excluindo pares que se sobrepõem; cardinalidade de A no máximo a de B para os mesmos pares; para toda linha, cardinalidade igual à da linha 1; para toda coluna, idem. Cerca de vinte conceitos, dos quais os de metades são mais difíceis (2.8).
- **F2×F3:** todos os componentes têm o mesmo tamanho; número de componentes igual à cardinalidade da linha 1; idem coluna 1; o maior componente tem pelo menos tantas células quanto a linha 1. Quatro conceitos.
- **F1 e F1':** como na v0.1, com `ParDireita` substituído por `ParAdjacente` (existe célula preta com vizinha preta), por razão de tamanho de programa (2.8).
- **F4:** adversarial (2.7.2).

**Tarefas independentes sem conhecimento do alvo.** Além dos conceitos-alvo, o currículo inclui **tarefas de função** especificadas por pares entrada-saída, do tipo `Grade → Lista Pos` ou `Lista Pos → Lista Pos → Bool`, como "as vizinhas pretas de p", "as células pretas da linha r", "o conjunto alcançável a partir de p". Elas são degraus (2.8) e são dadas a **todos** os aprendizes, inclusive L-fix. O que o aprendiz recebe de uma tarefa de função são exemplos e contraexemplos, nunca programas. O que o ambiente sabe, e o aprendiz não, é que as soluções dessas tarefas são subtermos das soluções dos alvos.

**Análise pré-registrada.** Desfecho primário: diferença pareada de aceitação a custo igual sobre os conceitos de F2 ∪ F3 ∪ F2×F3 não expostos no piloto, teste de sinal unilateral, α = 0,05. Secundário: diferença pareada do logaritmo do custo até aceitação, teste de Wilcoxon. Tamanhos de efeito e intervalos por conceito, todos reportados.

### 2.3 E0, E0' e a equivalência delimitada

#### 2.3.1 Núcleo comum

Cálculo lambda simplesmente tipado com constantes. Tipos: Bool, Pos, Grade, Lista a, e setas. Termos: variáveis, abstrações, aplicações, constantes, e `fix`. **Tamanho** |t| = número de folhas (constantes e variáveis) mais número de abstrações. **Semântica finita truncada Sem_n**, comum às duas linguagens: para cada n de 1 a 9, Pos = {1..n}², Grade = funções de Pos em Bool, listas têm comprimento no máximo F(n) = n⁴ (operações que produziriam listas maiores truncam), e `fix f` denota f aplicada F(n) vezes ao valor padrão do tipo (falso, vazio, (1,1)). Toda função é total. Nenhuma das duas linguagens é universal, e nenhuma afirmação sobre máquinas universais é usada.

#### 2.3.2 Primitivas de E0 (29)

- Grade: `celula`, `posicoes` (ordem linha a linha), `pretas` (células pretas em ordem), `linhas` (lista de listas de posições), `colunas`, `vizinhos` (vizinhas de 4 dentro da grade, ordem fixa).
- Bool: `verdadeiro`, `falso`, `e`, `ou`, `nao`, `se`.
- Pos: `igualP`.
- Lista: `vazio`, `cons`, `vazia?`, `cabeca`, `cauda`, `mapear`, `filtrar`, `algum`, `todos`, `concatenar`, `juntar`, `reverter`, `pertence`, `uniao`, `diferenca`.
- Recursão: `fix`.

Não há aritmética, contagem, comparação de comprimentos, componente conexo, simetria, nem coordenadas acessíveis. `pertence`, `uniao` e `diferenca` são utilidades de conjunto sobre listas de posições; `pretas` é uma conveniência igual a `filtrar (celula g) (posicoes g)`. Ambas as escolhas são declaradas e estão nas duas bases, logo não afetam o controle C3.

#### 2.3.3 Primitivas de E0' (20)

- Grade: `celula`, `posicoes`, `pretas`, `linhaDe` (posições da linha que contém p), `colunaDe`, `vizinhos`.
- Bool: as seis de E0. Pos: `igualP`.
- Lista: `vazio`, `cons`, `vazia?`, `cabeca`, `cauda`, `dobraR` (dobra à direita).
- Recursão: `fix`.

Em E0', `mapear`, `filtrar`, `algum`, `todos`, `concatenar`, `juntar`, `reverter`, `pertence`, `uniao`, `diferenca`, `linhas` e `colunas` são termos derivados.

#### 2.3.4 O que é provado, como, e o que não é

**Afirmação delimitada.** Existem traduções composicionais τ: E0 → E0' e τ': E0' → E0, que são homomorfismos sobre a estrutura dos termos (comutam com abstração e aplicação, fixam variáveis e `fix`, e levam cada constante a um termo fechado), tais que para todo termo fechado t e todo n de 1 a 9, Sem_n[[τ(t)]] = Sem_n[[t]] e Sem_n[[τ'(t)]] = Sem_n[[t]]; e |τ(t)| ≤ c·|t|, |τ'(t)| ≤ c'·|t|, com c = máximo de |τ(p)| sobre as primitivas p de E0 e c' análogo.

**Prova.** Por indução estrutural sobre t, dado que as traduções são homomorfismos e que a semântica é composicional, basta provar um lema por primitiva: Sem_n[[τ(p)]] = Sem_n[[p]]. Os lemas das primitivas de lista são identidades de dobra (por exemplo, `mapear f` é igual a `dobraR (λx acc. cons (f x) acc) vazio`), provadas por indução sobre listas de comprimento no máximo F(n); como `dobraR` em E0' é definida com o mesmo combustível F(n) que `fix` em E0, e as listas estão truncadas em F(n), as duas definições coincidem em todo o domínio, inclusive nos casos de truncamento. Os lemas das primitivas de grade (`linhas` em termos de `linhaDe` e vice-versa) são verificações diretas das definições sobre Pos finito. As provas são feitas à mão no pré-registro e, se possível, mecanizadas; **[P, condicional à publicação das provas por primitiva]**.

**Constantes estimadas** (a serem publicadas exatamente): c ≈ 35, dominada por `linhas` e `colunas`; c' = 15, dominada por `dobraR` traduzida por `fix`. A assimetria importa: em E0' a recursão simultânea sobre duas listas custa 9 folhas e abstrações; em E0, 15. A equivalência de expressividade não iguala custos, e é por isso que C3 é um controle e não uma redundância.

**O que os testes amostrais são.** Os tradutores são implementados; a implementação é testada contra a semântica por enumeração exaustiva para n até 4 e por amostragem para n de 5 a 9. Isso testa a implementação. Não é a prova, e não substitui a prova.

**O que não é afirmado.** Não se afirma que E0 ou E0' sejam universais, nem que toda função sobre grades seja denotável, nem nada sobre complexidade de Kolmogorov. Afirma-se apenas: mesmo conjunto de funções denotáveis sob Sem_n, com distorção de tamanho limitada por c e c'.

### 2.4 Aprendizes

Procedimento de busca comum: enumeração tipada por tamanho crescente, com poda por tipo e por equivalência observacional calculada **apenas sobre grades do reservatório de treino e do oráculo**, sob orçamento B em candidatos avaliados.

- **L-mem**: tabela com vizinho mais próximo por distância de Hamming; rejeita tamanhos novos.
- **L-fix**: busca em E0 fixa; recebe o mesmo currículo, inclusive as tarefas de função.
- **L-lib**: L-fix mais compressão após cada tarefa aceita: subtermos recorrentes das soluções viram constantes nomeadas (anti-unificação de fragmentos, no espírito de Ellis et al. 2021 e Bowers et al. 2023), com um hiperparâmetro de compressão fixado no piloto.
- **L-nn-conv**, **L-nn-seq**, **L-mdl**: como na v0.1, com vieses declarados; duas condições, sem e com aumento de dados pelas invariâncias declaradas.
- **L-teto**: E0 mais `componentes` e `mesmoNumero` como primitivas.
- **L-adapt** (só em transferência, 2.11): E0 mais o adaptador de portador, sem biblioteca.

### 2.5 Contabilização integral de custo

Unidade nativa simbólica: candidatos avaliados mais passos de avaliação (passos da semântica operacional somados sobre exemplos). Unidade neural: operações de ponto flutuante. Tempo de parede em hardware fixo reportado ao lado. Livro-razão por aprendiz e execução: busca por tarefa; compressão por passo; consultas ao oráculo (contadas) e custo da busca por contraexemplo (custo do ambiente, reportado à parte); avaliação em teste. **O custo de busca sob biblioteca maior inclui o aumento de ramificação**: um candidato avaliado conta um, qualquer que seja a linguagem. Comparação a custo cumulativo total igual em cada ponto do currículo; curvas de aceitação por custo cumulativo; ponto de cruzamento como resultado primário. Custo de aprendizagem anterior nunca é afundado.

### 2.6 Finito versus assintótico

Orçamentos por tarefa B, 3B, 10B e 30B, com B fixado no piloto de modo que L-fix resolva toda a família F1 em B. Para cada orçamento, reporta-se a razão de custo e a diferença de aceitação. A forma da curva é o resultado. Nenhuma separação assintótica é afirmada (2.0).

### 2.7 Protocolo de dados sem vazamento e F4 com oráculo oculto

#### 2.7.1 Partições

Reservatórios P_oráculo (n de 1 a 6, por semente), D_treino (3 a 6), D_val (3 a 6, só família F1 e tarefas de função para fixar hiperparâmetros), D_teste_int (3 a 6), D_teste_ext (7 a 9), D_teste_remap, D_teste_port (portadores), D_teste_nat (distribuição natural). Disjunção por hash de grade serializada, verificada antes de cada execução; hashes dos conjuntos publicados. Sementes confirmatórias a partir de 20 000; as do piloto, de 10 000 a 19 999 (documento 03). Instâncias de conceito usadas no piloto são marcadas "expostas" e excluídas do desfecho primário.

#### 2.7.2 Família adversarial F4 com oráculo oculto

- **Autor independente**, após o congelamento de E0 e do pré-registro. Recebe: a especificação de E0 e E0'; o vocabulário dos esquemas (componentes, cardinalidades, linhas, colunas, bordas); as **faixas de tamanho mínimo** medidas no piloto para F2 e F3 (por exemplo, "entre 10 e 16 folhas com as abstrações da escada"), sem os programas; e o script de auditoria de frequências.
- **Conteúdo:** seis conceitos, dois por classe de abstração exigida (fecho; comparação de cardinalidade; ambas), um dos quais fora do alcance das abstrações da escada por desenho, para medir transferência negativa e sobreajuste da biblioteca. Cada conceito vem com definição formal, duas implementações de referência, gerador construtivo auditado e verificação do confundidor de densidade.
- **Oráculo oculto:** os aprendizes interagem com F4 só por um serviço que responde rótulo(grade) e contraexemplo(h), executando h contra as referências seladas; os experimentadores não veem as definições até o fim das execuções. O serviço registra todas as consultas.
- **Dificuldade comparável, verificada depois:** após a revelação, os tamanhos mínimos de F4 são medidos pelo mesmo procedimento do piloto. Conceitos fora das faixas de F2 e F3 são reportados mas excluídos da comparação primária.

### 2.8 Currículo, escada de tarefas e bloqueio de bootstrapping

#### 2.8.1 O bloqueio

Programas de referência em E0, escritos à mão como limites superiores de tamanho (folhas mais abstrações), verificados contra as implementações de referência no piloto:

| Degrau | Programa (esboço) | Tamanho com os degraus anteriores | Tamanho bruto |
|---|---|---|---|
| ExistePreta (F1) | `λg. nao (vazia? (pretas g))` | 5 | 5 |
| vizPretos (função) | `λg p. filtrar (celula g) (vizinhos g p)` | 8 | 8 |
| ParAdjacente (F1) | `λg. algum (λp. nao (vazia? (vizPretos g p))) (pretas g)` | 10 | 15 |
| NenhumaIsolada (F2) | `λg. todos (λp. nao (vazia? (vizPretos g p))) (pretas g)` | 10 | 15 |
| passo (função) | `λg S. uniao S (juntar (mapear (vizPretos g) S))` | 9 | 14 |
| **fecho** (função) | `λg. fix (λrec S. se (vazia? (diferenca (passo g S) S)) S (rec (passo g S)))` | **16** | ≈ 38 |
| componenteDe (função) | `λg p. fecho g (cons p vazio)` | 7 | ≈ 44 |
| UmComponente (F2) | `λg. e (nao (vazia? (pretas g))) (todos (λq. pertence q (componenteDe g (cabeca (pretas g)))) (pretas g))` | 17 | ≈ 60 |
| pretasDe (função) | `λg r. filtrar (celula g) r` | 6 | 6 |
| **descartar** (função) | `fix (λrec A B. se (vazia? A) B (rec (cauda A) (cauda B)))` | **13** | 13 |
| noMaximo (função) | `λA B. vazia? (descartar B A)` | 6 | ≈ 18 |
| mesmoNumero (função) | `λA B. e (noMaximo A B) (noMaximo B A)` | 7 | ≈ 35 |
| PrimeiraUltimaIguais (F3) | `λg. mesmoNumero (pretasDe g (cabeca (linhas g))) (pretasDe g (cabeca (reverter (linhas g))))` | 13 | ≈ 45 |
| LinhasIguais (F3) | `λg. todos (λr. mesmoNumero (pretasDe g r) (pretasDe g (cabeca (linhas g)))) (linhas g)` | 14 | ≈ 45 |

Em E0', `descartar` é `λA B. dobraR (λx acc. cauda acc) B A`, com 9 (contra 13 em E0); `fecho` continua a exigir `fix` e fica em torno de 16 nas duas bases.

**Diagnóstico.** O currículo F1 → F2 → F3 da v0.1 tinha, entre F1 e o primeiro conceito de F2, um salto de cerca de 60 folhas brutas, e nenhuma solução de F1 contém subtermos de `fecho`. Isso é um bloqueio de bootstrapping: não há degrau. Mesmo com a escada acima, restam dois degraus de 13 a 16 (`descartar` e `fecho`), que são os laços de recursão, e que não têm subtarefa natural abaixo deles. Enumeradores puros, mesmo com poda por tipo e equivalência observacional, costumam alcançar tamanhos de 8 a 12 em contextos de tipo estreitos; 16 é incerto **[H, a medir no piloto]**.

#### 2.8.2 O currículo corrigido

- **Escada F2:** ExistePreta → vizPretos → ParAdjacente, NenhumaIsolada → passo → fecho → componenteDe → conceitos de F2 por esquema.
- **Escada F3:** pretasDe → descartar → noMaximo → família "no máximo" por esquema → mesmoNumero → família "igual" por esquema → LinhasIguais, ColunasIguais.
- **F2×F3** após as duas escadas.
- **Currículo distrator (C6):** mesmo número de tarefas de função e de predicados, com tamanhos de programa emparelhados, mas sem subtermos de `fecho` nem de `descartar` (por exemplo, "as células da primeira coluna", "a lista das linhas invertida", "existe célula preta no canto").
- **Ordem embaralhada (C2):** mesmas tarefas em ordem aleatória, e em ordem inversa, para medir pré-requisitos e sensibilidade de custo.

A escolha dos degraus usa conhecimento do experimentador sobre as soluções. Isso é legítimo porque (i) o aprendiz recebe só exemplos e contraexemplos; (ii) todos os aprendizes recebem o mesmo currículo; (iii) o distrator controla "qualquer escada ajuda". O que não é legítimo, e não é feito, é dar as abstrações como primitivas.

#### 2.8.3 Regra de decisão pré-registrada sobre E0+

Se o piloto mostrar que os degraus de 13 a 16 não são alcançáveis em E0 sob o orçamento máximo B_max, a execução confirmatória usa **E0+**, igual a E0 mais dois combinadores genéricos e não específicos de grade: `ateFixo : (Lista a → Lista a) → Lista a → Lista a` (itera até não mudar, com combustível F(n)) e `dobraR`. Com E0+, `fecho` cai para 4 e `descartar` para 9. A consequência para a alegação é declarada: parte do que seria "construir fecho" passa a ser "aplicar iteração genérica à vizinhança preta", e o custo C0 de cada conceito-alvo em E0+ é publicado. E0'+ recebe os mesmos dois combinadores para manter a equivalência.

### 2.9 Protocolo dialético

Para cada tarefa (predicado ou função), na ordem do currículo: 2 positivos e 2 negativos (para funções, 4 pares entrada-saída) de D_treino; hipótese dentro do orçamento; contraexemplo mínimo conforme 2.2.3; revisão; até K = 12 rodadas; todas as hipóteses registradas; avaliação em todos os conjuntos de teste.

### 2.10 Medidas

M1 aceitação por orçamento; M2 rodadas; M3 custo cumulativo (2.5); M4 acurácia em D_teste_int, _ext, _remap, _port; **M4n** métricas na distribuição natural (2.2.3); M5 falsos positivos em quase-acertos por troca; M6 localidade da revisão; M7 regressão; M8 identidade comportamental das abstrações contra os predicados auxiliares de referência; M9 política de generalização (H-B3), como na v0.1; **M10** confundidor de densidade: acurácia balanceada do classificador por densidade em cada conjunto, reportada ao lado de M4.

### 2.11 Auditoria de transferência

#### 2.11.1 Adaptadores de portador

Um adaptador substitui apenas as primitivas de portador (`celula`, `posicoes`, `pretas`, `linhas`, `colunas`, `vizinhos`; em E0', `linhaDe`, `colunaDe`) por equivalentes publicados; a biblioteca aprendida em grades é mantida sem alteração; o programa aprendido é avaliado sem modificação.

| Primitiva | Sequências binárias de comprimento m | Grafos rotulados (nó preto ou branco) |
|---|---|---|
| `posicoes` | índices 1..m | nós em ordem fixa |
| `celula` | valor no índice | rótulo do nó |
| `pretas` | índices com valor 1 | nós pretos |
| `vizinhos` | {i−1, i+1} dentro dos limites | adjacência |
| `linhas` | lista com uma única lista: todos os índices | **não definida** |
| `colunas` | lista de singletons | **não definida** |

**Critério de não-vazamento.** Um adaptador é legítimo se cada primitiva é definida por uma relação do portador que (i) não menciona nenhum predicado-alvo nem nenhuma abstração da escada e (ii) tem complexidade de definição não maior que a versão em grades. Adjacência em grafos é legítima: componente é o fecho da adjacência, e o fecho é o que o aprendiz teve de construir. Uma "partição em metades" para grafos **não** é legítima: introduziria estrutura que o conceito pressupõe. **Controle "só adaptador" (L-adapt):** E0 mais adaptador, sem biblioteca, no portador novo; se resolve o conceito dentro do orçamento, o adaptador vazou ou o conceito é trivial no portador, e a transferência desse conceito é anulada.

#### 2.11.2 Veredito por conceito

| Conceito ou família | Sequências | Grafos | Razão |
|---|---|---|---|
| ExistePreta, ParAdjacente, NenhumaIsolada | Legítima | Legítima | Só `pretas` e `vizinhos` |
| Número de componentes em S | Legítima (corridas de uns) | Legítima | Fecho da adjacência |
| TodosMesmoTamanho, todos os componentes com pelo menos 2 células | Legítima | Legítima | Idem |
| Existe componente reto | Degenera (toda corrida é reta) | Não definida (sem linhas) | Usa `linhas`/`colunas` |
| MaiorTocaBorda | **Degenera**: borda em grades é "no máximo 3 vizinhas", em sequências é sempre verdadeira | **Não transferível**: sem borda | A noção de borda é derivada do grau de vizinhança |
| PrimeiraUltimaIguais, LinhasIguais, ColunasIguais | **Degenera**: uma única linha | Não transferível | `linhas` |
| Cardinalidade de A igual à de B com A, B metades | Legítima (metades da sequência via `colunas`) | Não transferível | Partição não definível sem vazamento |
| Cardinalidade de coluna 1 igual à de coluna n | Degenera (singletons) | Não transferível | — |
| ComponentesIgualLinha1 | Legítima mas pouco natural (corridas igual a uns) | Não transferível | `linhas` |

**Consequência.** A transferência legítima é o teste T2 só para a família de componentes (sequências e grafos) e para os conceitos de metades (sequências). Para o resto, T2 não se aplica e isso é dito; nenhum resultado de transferência é computado para conceitos degenerados.

#### 2.11.3 Demais testes

T1 invariância por conceito; T3 transferência negativa sob o distrator; T4 reuso de abstrações (uso único é indício de heurística); T5 identidade comportamental com limiares pré-registrados (99% para n até 6; 95% para 7 a 9).

### 2.12 Controles

C1 orçamento a custo igual e múltiplos; C2 ordem; C3 base E0'; C4 oráculo com exemplos aleatórios; C5 lesão da biblioteca; C6 distrator com escada emparelhada; C7 superfície remapeada; C8 biblioteca de programas aleatórios; **C9** só adaptador (2.11); **C10** classificador por densidade em todo conjunto (M10).

### 2.13 Hipóteses neutras para controles neurais

Como na v0.1, com uma adição: cada controle neural é avaliado também em D_teste_nat e em M10, de modo que uma rede que aprenda densidade seja identificada como tal, e isso seja reportado como "aprendeu o confundidor", não como fracasso nem como sucesso.

### 2.14 Matriz de resultados e critérios de decisão

Os resultados referem-se a famílias com k ≥ 20 conceitos, sementes múltiplas, e a análise pré-registrada de 2.2.4.

**Se H-B1 vale neste regime:**

- S1 L-lib aceita significativamente mais conceitos de F2 ∪ F3 ∪ F2×F3 que L-fix a custo cumulativo igual, em B e em 3B.
- S2 S1 persiste em E0'.
- S3 O custo após a escada é menor que após o distrator (C6); a lesão (C5) elimina o ganho; C8 não o produz.
- S4 T1, T3, T4, T5 satisfeitos; T2 satisfeito nos conceitos em que a transferência é legítima, com L-adapt falhando.
- S5 Em C2, há conceitos não aceitos antes dos degraus de recursão (13 a 16) em nenhuma ordem, e o custo total depende da ordem.
- S6 Em M9, a política de generalização desloca-se após família relacionada e não após o distrator.
- S7 M10 ≤ 0,55 em todos os conjuntos de desenho, e M4n coerente com M4.

**Saídas que enfraquecem ou refutam, e a decisão que cada uma dispara:**

- F-a L-fix a custo igual, ou a 3B, iguala L-lib. Decisão: H-B1 não apoiada neste regime; reportar e passar ao experimento 2.
- F-b A vantagem some em E0'. Decisão: artefato de fatoração; E0 suspeita; repetir com uma terceira fatoração antes de qualquer alegação.
- F-c C4 iguala a dialética. Decisão: reportar que contraexemplos mínimos não importam neste regime.
- F-d Abstrações aceitas sem identidade comportamental (T5). Decisão: separar compressão de conceito no relato; é a saída mais informativa.
- F-e S1 e S2 com S3 ou T2 falhando. Decisão: ganho de busca genérico; H-B1 sem transferência.
- F-f F4 não aceita enquanto F2 e F3 são. Decisão: E0 ou escada ajustadas às famílias planejadas; resultado principal desvalorizado.
- **F-h** Nenhum aprendiz alcança os degraus de recursão em E0 nem em E0+. Decisão: bloqueio de currículo; o experimento não testa H-B1 e é redesenhado (busca guiada, ou tarefas de função mais finas); nada é alegado.
- **F-i** M10 > 0,55 em algum conjunto, ou um aprendiz atinge M4 alto com M4n incoerente. Decisão: confundidor; o conjunto e os resultados nele são invalidados e regenerados.
- F-g S1 a S7 valem. Decisão: H-B1 e parte de H-B3 apoiadas em micro-mundo simbólico, **nesta E0, nesta escada, nestas famílias**. Nada sobre H-B2, fundamentação, revisão de método ou inteligência geral. Nenhuma alegação é feita antes da replicação em E0' (S2) e da família F4.

### 2.15 Limitações

Não testa L2 (toda abstração é definição), fundamentação, instanciações contínuas, H-C, abertura, inteligência geral. A escada é desenhada pelo experimentador, o que limita a alegação a "dado um currículo com degraus, a construção de biblioteca produz as transições"; a versão com currículo autogerado é um experimento posterior. A busca é enumerativa pura; resultados com busca guiada por rede podem diferir. As famílias são geradas por esquemas que o experimentador conhece; F4 é a única defesa contra o ajuste inadvertido de E0 às famílias.

---

## 3. Experimento 2 — Agente sensório-motor em micro-mundo sem definições

### 3.0 Vocabulário e compromissos (v0.2)

"Conceito emergente", neste experimento, designa um **aglomerado de capacidades funcionais** medidas comportamentalmente (persistência, ligação de propriedades, contagem, uso de intervenção), **não** um símbolo, um slot, nem uma variável discreta no estado interno. Representações contínuas, distribuídas ou atratoras contam, desde que passem os testes. Análises do estado interno (decodificação linear, dimensionalidade do manifold de estados) são descritivas e nunca critério.

### 3.1 Pergunta

Como na v0.1, com a adição: as capacidades adquiridas são distinguíveis de detecção de anomalia e de aprendizagem de regularidades temporais?

### 3.2 Capacidades iniciais e instanciação

Como na v0.1 (R1–R6 contínuos; comparador de segunda ordem não dado; vieses opcionais ablacionáveis: lentidão, gargalo, bônus de exploração).

### 3.3 Representação de observações e ações

Como na v0.1, com uma adição: o ambiente mantém um **programador de intervenções forçadas** que, em um braço, move o agente e executa um empurrão em instantes aleatórios independentes da política, para produzir dados interventivos aleatorizados (3.4, E-6).

### 3.4 Quatro coisas que a surpresa não distingue, e como separá-las

| Nível | O que é | Como um sistema sem o nível seguinte passaria | Controle que o separa do nível seguinte |
|---|---|---|---|
| **AD** Detecção de anomalia | Surpresa proporcional à novidade estatística da entrada | Um preditor de estatísticas de pixel sem memória é surpreendido por qualquer evento raro | **Aparência nova:** objetos nunca vistos (forma, cor) em eventos possíveis não devem produzir surpresa de nível "impossível"; e a diferença impossível − possível deve persistir para aparências novas |
| **RL** Aprendizagem de regularidade | Surpresa quando uma regularidade temporal aprendida é violada (por exemplo, reaparição após k passos) | Um modelo que memoriza "atrás do oclusor, k passos, reaparece à direita" passa no teste padrão de permanência | **Variação paramétrica:** velocidade do objeto e largura do oclusor variam no teste; a predição de tempo e lugar de reaparição deve escalar fisicamente; um aprendiz de regularidade treinado numa velocidade falha nas outras |
| **OR** Representação de objeto | Entidade persistente, contável, à qual propriedades estão ligadas | — | **Ligação:** evento "entra vermelho, sai azul" produz surpresa; **contagem:** E-5 com área e densidade emparelhadas; **identidade:** E-4 com dinâmicas distintas |
| **CA** Causalidade | Distinção entre ver e fazer; predição interventiva e contrafactual | Um modelo associativo prediz co-movimento por correlação | **Intervenção** (E-6) e **sonda contrafactual** (abaixo) |

A hierarquia é cumulativa: OR só é alegada se os controles de AD e RL são passados; CA só se os de OR são.

**E-6 fortalecido (causalidade).**

- Treino passivo com causa comum (vento move A e B juntos). Teste: o agente empurra A; mede-se a predição ou a surpresa sobre B. Predição causal: B fica. Predição associativa: B se move.
- **Três estruturas**, cada uma com predição interventiva distinta: causa comum (A e B movidos pelo vento), cadeia (vento move A, A empurra B), causa direta (A empurra B sem vento). Um sistema causal distingue as três sob intervenção; um associativo não.
- **Intervenções aleatorizadas** pelo programador forçado, para que os dados interventivos não dependam da política do agente; braço "acorrentado" com a mesma sequência sensorial sem ação; braço curioso; braço aleatório.
- **Sonda contrafactual**, aplicável a agentes com modelo preditivo utilizável como simulador: a partir do mesmo estado e histórico, o modelo é executado sob "empurrar A" e sob "não empurrar"; a diferença predita na trajetória de B deve ser próxima de zero na causa comum e positiva na causa direta. É uso generativo do modelo, não inspeção do estado. Para agentes sem modelo, a sonda não se aplica, e isso é declarado.

### 3.5 Viés, dados e a leitura correta de uma ablação

A v0.1 escreveu que "uma capacidade que desaparece com a remoção de um viés estava no viés". Isso confunde condição necessária com conteúdo. Um prior de lentidão não contém permanência de objeto; pode ser o que torna a aquisição possível, como qualquer viés indutivo (documento 01, Objeção 1). A leitura correta é fatorial:

| | Dados com objetos | Dados sem objetos (A-4) |
|---|---|---|
| **Com o viés** | Capacidade presente: **adquirida sob viés habilitador** | Capacidade presente: **estava no viés** (regularidade programada) |
| **Sem o viés** | Capacidade presente: **adquirida sem esse viés** | Capacidade presente: artefato de medida |

Para cada capacidade e cada viés declarado reporta-se a célula em que ela aparece, e a curva de quantidade de dados necessária com e sem o viés. "Regularidade programada" é o rótulo apenas da célula superior direita. A célula superior esquerda é o caso normal de qualquer aprendiz, inclusive biológico, e é o que o experimento espera encontrar.

### 3.6 Resultados que refutariam a hipótese neste regime

Como na v0.1, com as substituições: a assinatura de OR reproduzida por um preditor de pixel (AD) ou por um aprendiz de regularidade sem escalonamento físico (RL); E-6 falhando nas três estruturas inclusive com intervenções aleatorizadas; capacidades presentes na célula "viés sem dados".

### 3.7 Riscos, custo e limitações

Como na v0.1. Acrescenta-se: a bateria de eventos emparelhados é o maior custo humano; a sonda contrafactual restringe a classe de agentes.

---

## 4. Comparação dos dois experimentos

Como na v0.1, com duas linhas alteradas: **Força dos controles** do experimento 1 passa a "alta, condicionada ao piloto (reach dos degraus de recursão)"; **Risco de autoengano** do experimento 1 passa a "baixo a médio, com dois confundidores identificados e controlados: densidade (C10) e ajuste de E0 às famílias (F4)".

---

## 5. Ordem de execução

1. **Piloto do experimento 1** (documento 03): viabilidade e calibração; sem alegações.
2. **Decisão GO / E0+ / NO-GO** pela regra de 2.8.3 e pelos critérios de aceitação do piloto.
3. **Experimento 1 confirmatório**, pré-registrado, com dados e instâncias de conceito não expostos no piloto.
4. **Experimento 2**, em qualquer caso, com os ajustes de desenho que o resultado do experimento 1 dispara (seção 5 da v0.1).
5. A replicação de Philipona, O'Regan e Nadal (2003) pode correr em paralelo como validação de infraestrutura.

---

## 6. Status epistêmico das afirmações deste protocolo

| Afirmação | Status |
|---|---|
| Teorema da invariância para máquinas universais | [P], **não aplicável** a E0 |
| Lema de inlining para linguagens tipadas finitas | [P], trivial |
| Equivalência de E0 e E0' sob Sem_n | [P], condicional à publicação das provas por primitiva; testes amostrais testam a implementação |
| Frequências de positivos (fórmulas exatas) | [P] para as fórmulas; [C] para os valores calculados |
| Frequências de positivos (Monte Carlo) | [C], 20 000 amostras por célula, semente publicada |
| Potência do teste de sinal | [P] para a fórmula binomial; [C] para a tabela |
| Confundidor de densidade existe nos conjuntos balanceados por rejeição | [C], inferido das frequências por valor de p; medido diretamente por M10 |
| Degraus de 13 a 16 são o bloqueio | [C] para os tamanhos dos programas de referência (limites superiores); [H] sobre alcançabilidade, a medir no piloto |
| Aprendizagem de biblioteca reduz custo em domínios estreitos | [C] (Ellis et al. 2021; Bowers et al. 2023) |
| Efeitos de ordem de currículo em humanos | [E/C] (Zhao, Lucas e Bramley 2024) |
| Dimensionalidade do espaço inferível de contingências sensório-motoras | [C] (Philipona et al. 2003) |
| Crianças aprendem estrutura causal por intervenção | [E] (Gopnik et al. 2004) |
| Violação de expectativa mede objeto | [F]; tratada como hipótese operacional com os controles AD e RL |
| Capacidade dependente de viés foi programada | **Rejeitada** como inferência; substituída pelo desenho fatorial |
| Sucesso em qualquer experimento é evidência de inteligência geral | Negado por regra |

---

## 7. Questões abertas preservadas

As seis da v0.1, mais: (7) se um enumerador puro alcança degraus de 13 a 16 folhas em contextos de tipo estreitos, ou se a construção de abstrações depende de busca guiada; (8) se um currículo autogerado por progresso de aprendizagem produz a escada sem desenho do experimentador; (9) se a separação AD/RL/OR/CA é exaustiva, ou se há níveis intermediários que os controles não capturam.

---

## 8. Referências

As da v0.1 permanecem. Acrescentadas: `analysis/audit_frequencias.py` e `analysis/audit_frequencias_saida.md` (este repositório), que são a fonte das tabelas de 2.2.2 e 2.2.4.
