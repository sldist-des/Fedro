# Investigação fundamental sobre a origem da inteligência

## Documento 01 — Análise crítica inicial: hipótese, objeções, estado da arte, direções e primeiro experimento

**Status:** rascunho de fundação, **v0.2**, com a **nota v0.3** em 1.2-bis (2026-10-29). A v0.1 é do mesmo dia (commit `9b194df`); a v0.2, do commit `48d616d`. Sem código do experimento. Sem arquitetura definitiva.

A v0.2 resulta de uma auditoria epistemológica independente. As mudanças conceituais estão registradas na seção "Histórico de revisões" e, no corpo do texto, em blocos marcados **Revisão v0.2**. O texto da v0.1 foi preservado onde foi corrigido, para que a trajetória das conclusões seja auditável. Regra fundamental adotada na v0.2: **a primeira definição mensurável de aprendizagem deste programa (transições de eficiência) não é uma definição da natureza da inteligência nem da novidade conceitual.**

**Sobre as referências:** nenhuma referência foi inventada. As referências de 2024–2026 foram verificadas online na data deste documento. As referências clássicas são citadas com os dados bibliográficos usuais e devem ser conferidas uma a uma antes de qualquer publicação. Onde um dado não pôde ser verificado, isso está dito no texto.

### Histórico de revisões

**v0.1 → v0.2 (auditoria epistemológica, 2026-10-29).** Tabela das mudanças conceituais. Cada linha aponta a seção em que o texto da v0.1 foi preservado e o bloco **Revisão v0.2** que o corrige.

| # | Seção | A v0.1 afirmava | A v0.2 corrige para | Base da correção |
|---|---|---|---|---|
| 1 | 1.2 | Novidade conceitual = transição de eficiência (tratabilidade) | Quatro camadas distintas: L0 expressividade teórica; L1 expressividade efetiva sob recursos; L2 mudança qualitativa do sistema conceitual; L3 capacidades de generalização. Eficiência operacionaliza apenas L1 | Carey 2009, 2011, 2014, 2015; Rips et al. 2006, 2008, 2013; Beck 2017; Rey 2014; Pantsar 2021; Rule e Piantadosi 2025; Karmiloff-Smith 1992 |
| 2 | 1.2, 1.3 | "Mais do que um fator constante" como critério de H-B | O teorema da invariância torna vazia qualquer afirmação assintótica sobre re-representação; o conteúdo de H-B está na magnitude das constantes em recursos finitos, na sua amortização sobre uma distribuição de tarefas e na sua seleção a partir de dados | Li e Vitányi 2008 [P]; Levin 1973 [P] |
| 3 | 1.3 | H-B-fraca e H-B-forte | H-B1 (eficiência, L1), H-B2 (reorganização qualitativa, L2), H-B3 (capacidades de generalização, L3). H-B-fraca ≈ H-B1; H-B-forte foi dividida entre H-B1 (transferência) e H-B3 | Idem |
| 4 | 2, Objeção 2 | "A distinção definição/primitiva não tem significado computacional além do custo" | Retirada como conclusão. É a posição de um lado do debate (Rule e Piantadosi); o outro (Carey, Beck) sustenta descontinuidade por papel inferencial. Marcada [A] | Idem |
| 5 | 4.2 | Igualdade, detector de inconsistência e linguagem com ordenação de simplicidade são **primitivas inevitáveis** | Inevitáveis são **requisitos funcionais** (discriminabilidade, sinal de discrepância, plasticidade, ordenação de preferência, persistência), não operadores simbólicos; implementações contínuas e probabilísticas satisfazem os requisitos e podem adquirir resolução. Aberto: se o comparador de segunda ordem pode ser adquirido | Damper e Harnad 2000; Valle-Pérez, Camargo e Louis 2019; Rao e Ballard 1999; Yu e Dayan 2005; Xie et al. 2022; von Oswald et al. 2023; Akyürek et al. 2023 |
| 6 | 4.4 | Critério 3: currículos diferentes devem produzir abstrações diferentes | Substituído por estrutura de pré-requisitos e sensibilidade de custo à ordem; invariância do ponto final não conta contra aquisição | Zhao, Lucas e Bramley 2024 |
| 7 | 4.4 | Quatro critérios para "adquirido" | Os quatro valem para L1; acrescentados critérios candidatos para L2 e L3, com a ressalva de que L2 não tem operacionalização aceita [A] | — |
| 8 | 8 | Protocolo do experimento de grades | Oito problemas identificados pela revisão; protocolo corrigido migrado para `docs/02-protocolo-experimental.md`; predições sobre o controle neural tornadas neutras; sucesso explicitamente não é prova de inteligência geral | Revisão independente |
| 9 | 9 | Demarcação como primeira questão | Mantida, agora em três camadas (L1, L2, L3), com a regra de não confundir a primeira operacionalização com a definição | — |
| 10 | Legenda | [C] cobria teoremas e sistemas | [P] para provas formais; [A] para questões abertas | — |
| 11 (v0.3) | 1.2-bis | O teorema da invariância justifica que "toda vantagem de re-representação é fator constante" e que afirmações assintóticas são vazias | O teorema vale para máquinas universais e **não se aplica** às linguagens finitas, com combustível, dos experimentos; substituído pelo lema de inlining e pela observação de que um domínio finito não tem parâmetro assintótico (documento 02, 2.0). A regra "finito, nunca assintótico" permanece por essa outra razão | Terceira auditoria independente |

**Afirmações da v0.1 reclassificadas como [P] na v0.2:** a tese de Church–Turing enquanto resultado sobre máquinas universais (a tese em si permanece [F]); Mitchell 1980 (um aprendiz sem viés não generaliza, no sentido formal do espaço de versões); Wolpert 1996 (ausência de almoço grátis); o teorema de Locatello et al. 2019 (os experimentos do mesmo artigo ficam [C]); Pearl 2009 (não identificabilidade da estrutura causal a partir de distribuições observacionais, em geral); Solomonoff 1964 (incomputabilidade do prior universal); Gold 1967; Valiant 1984; Angluin 1987; o teorema da invariância da complexidade de Kolmogorov; a otimalidade da busca de Levin até fator constante.

**O que a v0.2 não muda:** as cinco objeções continuam de pé; a Objeção 1 e a Objeção 3 saem reforçadas (a v0.2 mostra que vieses implícitos e laços externos dados reaparecem nas instanciações contínuas); a prioridade da questão de demarcação; a rejeição do vocabulário de consciência.

### Como ler este documento

Cada afirmação relevante leva um rótulo epistêmico, conforme pedido:

- **[P]** prova formal: teorema, válido sob as hipóteses do teorema (acrescentado na v0.2)
- **[E]** fato empírico com evidência publicada
- **[F]** interpretação filosófica
- **[C]** resultado computacional: existe sistema ou experimento reproduzível; não é prova
- **[H]** hipótese (nossa ou da literatura)
- **[R]** condição de refutação
- **[A]** questão aberta: a literatura não permite conclusão (acrescentado na v0.2)

Na v0.1, o rótulo [C] cobria teoremas e sistemas. Na v0.2, os teoremas passam a [P]; a lista das afirmações reclassificadas está no histórico de revisões. Rótulos do texto da v0.1 que não foram tocados devem ser lidos com essa ressalva.

### Sumário

Histórico de revisões (v0.2)
0. Resumo executivo
1. Reformulação científica da hipótese
2. As cinco objeções mais fortes
3. Questão A — O que estamos tentando reproduzir
4. Questão B — O problema dos princípios anteriores à experiência
5. Questão C — O que a ciência já investigou
6. Questão D — Reproduzir o processo, não programar o resultado
7. Direções de investigação distintas
8. Questão E — O primeiro experimento decisivo
9. Qual questão resolver primeiro e por quê
10. Referências

---

## 0. Resumo executivo

A hipótese inicial, tomada literalmente, mistura quatro afirmações de natureza diferente: uma tese metafísica (independência de substrato), uma tese empírica parcialmente falsa (o humano "não começa sabendo"), uma tese construtivista testável (um sistema pode construir e revisar suas próprias representações) e uma dicotomia mal posta ("desenvolver" versus "receber regras programadas").

A reformulação central deste documento é a seguinte. Para qualquer sistema computacionalmente universal, **tudo o que é aprendível já é expressável** na linguagem inicial do sistema. Portanto a hipótese não pode ser sobre expressividade. Ela só tem conteúdo científico se for sobre **tratabilidade**: um conceito é "novo" para um sistema quando não era alcançável dentro de seu orçamento de recursos e passa a ser alcançável em função de uma mudança que o próprio sistema produziu em si mesmo. A hipótese vira, assim, uma afirmação sobre **transições de eficiência** na aprendizagem, mensuráveis como descontinuidades no custo de aprender em função do que foi aprendido antes. Essa reformulação também dissolve, em termos computacionais, o paradoxo do Mênon: não se procura o que não se pode representar; procura-se uma descrição mais curta do que já se pode representar, e o ganho é real, porém limitado.

As cinco objeções mais fortes são: (1) não existe aprendizagem sem viés, logo "sem princípios programados" é ininteligível; (2) nada é genuinamente novo em um sistema universal, logo "transformar os próprios princípios" precisa ser redefinido ou abandonado; (3) toda auto-revisão exige um critério de valor que não é revisado, logo a hierarquia tem um topo fixo; (4) o caso humano talvez não instancie a hipótese, porque depende de um prior evolutivo enorme e de tecnologias culturais transmitidas; (5) escala estatística talvez baste, e sem definições operacionais cada resultado pode ser lido dos dois modos, como aconteceu historicamente com o programa AM.

A questão a resolver primeiro não é "qual arquitetura", e sim **o critério de demarcação entre capacidade adquirida e capacidade implícita no desenho**. Sem esse critério, nenhum experimento posterior é interpretável. O primeiro experimento proposto (seção 8) serve exatamente para calibrar esse critério em um micro-mundo de grades, com um aprendiz que constrói sua própria biblioteca de abstrações sob um protocolo de contraexemplos, comparado a controles de memorização, de regras fixas, de orçamento ampliado e de mudança de base.

**Atualização v0.2.** A auditoria independente levou a três correções de fundo. Primeira: a redução de "novidade conceitual" a transições de eficiência era a adoção tácita de um lado do debate entre Piantadosi e Carey; a v0.2 distingue quatro camadas de novidade (expressividade teórica, expressividade efetiva, mudança qualitativa, capacidades de generalização), reconhece que o critério de eficiência operacionaliza só a segunda, e deixa a terceira como questão aberta. Segunda: o que é inevitável num aprendiz são requisitos funcionais, não operadores simbólicos; sistemas contínuos os satisfazem e podem adquirir resolução. Terceira: o critério de dependência de currículo foi corrigido, e o protocolo experimental foi refeito em documento próprio (`docs/02-protocolo-experimental.md`), com contabilização integral de custo, demonstração de equivalência de bases, definições formais dos conceitos, protocolo sem vazamento, testes de transferência real e hipóteses neutras sobre os controles neurais. Regra fundamental da v0.2: a primeira definição mensurável de aprendizagem não é uma definição da natureza da inteligência.

---

## 1. Reformulação científica da hipótese

### 1.1 O que a hipótese original afirma, desmontada em partes

Seu texto contém pelo menos quatro afirmações distintas, que precisam ser separadas porque têm status epistêmicos diferentes:

- **P1 (independência de substrato):** a inteligência depende de princípios abstratos reproduzíveis em outros substratos.
- **P2 (insuficiência do inato):** o humano não nasce sabendo matemática, linguagem ou leis da natureza; desenvolve capacidades progressivamente.
- **P3 (construtivismo):** um sistema pode desenvolver, revisar e transformar seus próprios princípios de representação e raciocínio.
- **P4 (anti-programação):** isso deve ocorrer "em vez de receber esses princípios como regras programadas".

**Sobre P1.** Esta é a tese da realizabilidade múltipla, formulada por Putnam (1967) e base do funcionalismo em filosofia da mente **[F]**. Ela não está empiricamente estabelecida. O apoio mais forte é indireto: (a) a tese de Church-Turing garante que qualquer função efetivamente computável é implementável em qualquer substrato universal **[C]**, mas não diz se a inteligência é "uma função computável" nem sob quais limites de recursos; (b) há evidência de que redes de arquiteturas diferentes, treinadas em modalidades diferentes, convergem para representações com geometria semelhante, a chamada "Platonic Representation Hypothesis" de Huh, Cheung, Wang e Isola (2024) **[E, interpretativa e contestada]**; (c) redes profundas reproduzem muitas assinaturas comportamentais da percepção e da linguagem humanas **[E]**. O que refutaria P1 **[R]**: uma demonstração de que alguma função cognitiva necessária depende de uma propriedade física não reproduzível em outro substrato. Não existe tal demonstração. P1 é, por ora, um pressuposto de trabalho, não um resultado.

**Sobre P2.** Esta afirmação é empiricamente meio falsa, e o meio falso importa. Bebês de poucos meses já exibem expectativas estruturadas sobre objetos (coesão, continuidade, contato: Spelke 1990; Baillargeon, Spelke e Wasserman 1985), sobre quantidade pequena (Wynn 1992; Feigenson, Dehaene e Spelke 2004), sobre agentes e sobre espaço, sistematizadas como "conhecimento nuclear" (Spelke e Kinzler 2007; Spelke 2022) **[E]**. O humano não começa com matemática, mas começa com muito. A quantidade relevante foi estimada por Zador (2019): o genoma não tem capacidade de especificar o conectoma, portanto especifica regras de aprendizagem e priors de conexão altamente comprimidos, o "gargalo genômico" **[E/F]**. A formulação honesta é: a dotação inicial humana é **altamente comprimida, mas não mínima, e não é genérica**; ela é específica a domínios (objetos, número, agentes, espaço).

**Sobre P3 e P4.** Aqui está uma falsa dicotomia, e ela é o ponto mais importante a corrigir. Qualquer aprendiz que generaliza possui, necessariamente, (i) uma linguagem de hipóteses, (ii) uma ordenação de preferência sobre hipóteses (o viés indutivo) e (iii) um critério de sucesso. Esses três elementos são sempre "recebidos" (Mitchell 1980; Wolpert 1996) **[C]**. A variável real não é "programado versus desenvolvido", e sim **qual nível fica fixo, quais níveis mudam sob experiência, e quanto da competência final é atribuível a essas mudanças**.

**Sobre as inspirações filosóficas.** Há uma tensão que vale registrar desde já. A teoria da reminiscência do Mênon (80d–86c) e do Fédon (72e–77a) é uma forma de **inatismo**: o conhecimento preexiste e aprender é recuperá-lo. Isso é o oposto de P3. O paradoxo do Mênon ("não se pode procurar nem o que se sabe nem o que não se sabe") é o **problema** certo; a reminiscência é a **solução** errada para um construtivista. A epagogé aristotélica (Segundos Analíticos II.19, 99b–100b: percepção, memória, experiência, universal) está muito mais próxima de P3, mas o nous aristotélico, que "apreende" os primeiros princípios, é o nome de um mecanismo, não um mecanismo **[F]**.

### 1.2 O erro de categoria central: expressividade versus tratabilidade

O argumento é curto e decisivo para todo o programa.

Seja E0 a dotação inicial do sistema (primitivas, regras de composição, procedimento de aprendizagem, critério). Se E0 é computacionalmente universal, então todo conceito que o sistema possa vir a usar já é expressável em E0. Logo, "desenvolver princípios que não foram dados" não pode significar "expressar o inexpressável".

Fodor (1975; 1980) transformou isso no "paradoxo da aprendizagem": testar uma hipótese pressupõe representá-la; logo, as primitivas de representação não podem ser aprendidas, apenas as composições delas. A conclusão de Fodor, o nativismo radical de conceitos, é amplamente rejeitada (Laurence e Margolis 2002; Carey 2009) **[F]**, mas o núcleo válido permanece: **a novidade só pode ser definida relativamente a recursos**.

A resolução que propomos: um conceito é **novo para um sistema** se (a) não era alcançável sob o orçamento de recursos do sistema antes de certa experiência, e (b) passa a ser alcançável depois, em função de uma mudança que o próprio sistema produziu na sua organização interna (uma nova abstração, uma nova sub-rotina, um novo invariante). Com isso, a hipótese passa a ser uma afirmação sobre **transições de eficiência**: descontinuidades no custo de aprendizagem (amostras, passos de busca, comprimento de descrição) em função do que foi aprendido antes. Isso é mensurável.

Esta reformulação também dissolve computacionalmente o paradoxo do Mênon: não se procura o que não se pode representar; procura-se uma descrição mais curta ou mais barata do que já se pode representar. O ganho de compressão é real, converte intratável em tratável, e é limitado pela universalidade de E0. A reminiscência platônica seria o caso-limite em que o custo é zero, o que é empiricamente falso para humanos, que levam anos.

### 1.2-bis Revisão v0.2 — Quatro camadas de novidade e o desafio de Carey

**O que a auditoria encontrou.** A seção 1.2 reduziu "novidade conceitual" a tratabilidade. Isso coincide, sem o dizer, com a posição de um dos lados de um debate em curso: o de Piantadosi e colaboradores, contra Carey e Beck, e, por razões diferentes, contra Rips e Rey. A v0.2 não decide o debate. Separa quatro camadas que a v0.1 misturou e diz qual delas cada experimento pode tocar.

**L0 — Expressividade teórica.** O que uma linguagem universal pode expressar com recursos ilimitados. Para E0 universal, tudo o que é computável **[P]**. Rule e Piantadosi (2025) chegam ao mesmo ponto: para uma mente idealizada com primitivas universais e recursos ilimitados, não há conceitos novos a adquirir. Nesta camada, a tese de Fodor é trivialmente verdadeira e sem interesse.

**L1 — Expressividade efetiva.** Os recursos representacionais efetivamente disponíveis ao aprendiz: o que ele pode construir, armazenar e **usar de modo confiável** sob limites de tempo e memória. Rule e Piantadosi (2025) formalizam a posse de um conceito como um grau contínuo, T(c) − R(c), em que T(c) é o comprimento de descrição do conceito e R(c) a informação que o aprendiz ainda precisa extrair do ambiente para selecioná-lo; na formulação deles, qualquer mudança que diminua a informação necessária para representar um conceito é parte da aquisição, e chunking, abstração e aprendizagem de biblioteca aumentam a expressividade de uma mente com recursos limitados **[F/C]**. Uma medida formal nesta camada é a complexidade de Levin, Kt(x) = min sobre programas p de |p| + log t(p), que penaliza tempo além de comprimento (Levin 1973) **[P]**. Era aqui que a v0.1 estava. O critério de transição de eficiência é a operacionalização de L1, e só dela.

**L2 — Mudança conceitual qualitativa.** A tese de Carey (2009): um sistema conceitual CS2 tem mais poder expressivo que CS1 quando conceitos de CS2 não são definíveis nos termos de CS1; os casos são o número natural a partir dos sistemas nucleares, o número racional, e matéria, peso e densidade na física intuitiva. O mecanismo proposto, o bootstrapping quineano, tem duas fases: uma estrutura de marcadores vazios é aprendida como estrutura (a lista de contagem recitada sem significado) e depois "processos de modelagem", analogia, inferência indutiva, abdução e experimento mental, dão conteúdo aos marcadores pelas relações entre eles. O conteúdo vem do **papel inferencial**, não de uma definição. A evidência empírica é aceita por todos os lados: os níveis de conhecedor de número (Le Corre e Carey 2007; Sarnecka e Carey 2008) **[E]**. A interpretação é disputada **[A]**.

**L3 — Capacidades de generalização.** Mudanças em *como* o sistema generaliza, não em *o que* representa: os "learning sets" de Harlow (1949), o viés de forma treinável (Smith et al. 2002), as sobre-hipóteses (Kemp, Perfors e Tenenbaum 2007) e a redescrição representacional de Karmiloff-Smith (1992), em que conhecimento procedimental implícito é redescrito em formatos explícitos que permitem novas generalizações **[E/F]**. Não são conceitos; são disposições indutivas de segunda ordem.

**Em que sentido exato Carey desafia a formulação da v0.1.** Três sentidos, de força diferente.

1. **Nível de descrição.** O "poder expressivo" de Carey é relativo ao sistema conceitual disponível, definido por papéis inferenciais, e não à linguagem de hipóteses do substrato. Traduzido para os nossos termos: "não definível em CS1" não é "não expressável em E0". A tradução caridosa é: CS1 é o conjunto de representações que o aprendiz consegue instanciar e usar em inferência no instante t, uma noção de L1; "CS2 não definível em CS1" vira "conceitos de CS2 não são composições de conceitos de CS1", o que é compatível com serem expressáveis em E0 se E0 tem combinadores (recursão, ponto fixo) que CS1 não usa. Nessa leitura, o desafio de Carey à v0.1 é **parcial**: ela acrescenta uma condição estrutural que o custo não captura. Um conceito constituído por papel não é uma definição sobre conceitos antigos; dois sistemas podem ter custos idênticos e diferir em se o conceito novo é definido ou constituído por relações. Consequência direta para o programa: **um aprendiz por síntese de programas, em que toda abstração é uma definição, só pode produzir novidade de L1, por construção**. O experimento de grades não pode testar L2. Isso é uma limitação de desenho, não um resultado.

2. **Circularidade e interpretação desviante.** Rips, Asmuth e Bloomfield (2006; 2008) argumentam que o bootstrap não consegue selecionar a sequência dos números naturais entre sequências não equivalentes compatíveis com a evidência, e que propostas de indução empírica pressupõem os conceitos matemáticos que deveriam explicar. Piantadosi, Tenenbaum e Goodman (2012) mostraram uma rota não circular, em que a hipótese do conhecedor de cardinalidade é selecionada por inferência bayesiana sobre uma linguagem de primitivas; Rips, Asmuth e Bloomfield (2013) respondem que o modelo recombina primitivas escolhidas à mão e não exibe a descontinuidade que o bootstrapping exige. Beck (2017) distingue aprendizagem modesta, em que o conceito novo é expressável nos antigos (por composição não óbvia ou por seleção de conceitos "à espera"), de aprendizagem radical, em que não é, e argumenta que o desafio da interpretação desviante atinge toda aprendizagem indutiva, não só o bootstrap. Pantsar (2021) contesta essa generalização e propõe enculturação como solução. Rey (2014) sustenta que evidência sobre a manifestação de conceitos em crianças não decide questões lógico-semânticas de poder expressivo, e que analogia e bootstrapping pressupõem o poder expressivo que pretendem explicar; Carey respondeu (2014; 2015). Rule e Piantadosi (2025) dissolvem a dicotomia inato/aprendido em posse graduada sob recursos limitados. Este conjunto é um debate vivo **[A]**. O que é consenso: os fatos desenvolvimentais. O que é disputado: se "descontinuidade" nomeia algo além de L1.

3. **Consequência metodológica.** A seção 2, Objeção 2, escreveu que "a distinção entre definição e primitiva não tem significado computacional além do custo". Isso é a tese de Rule e Piantadosi, não um fato. A v0.2 retira a frase como conclusão e a reclassifica como uma das posições em disputa. O programa mantém L1 como primeira camada mensurável, declara que o experimento 1 só a testa, e registra em 4.4-bis os critérios candidatos para L2, com a ressalva de que nenhum sistema computacional conhecido os satisfaz de modo demonstrado **[A]**.

**O teorema da invariância e a frase "mais do que um fator constante".** Para máquinas universais U e V existe uma constante c, dependente apenas do par de máquinas, tal que o comprimento de descrição de qualquer objeto x difere entre U e V por no máximo c (Li e Vitányi 2008) **[P]**. Logo qualquer re-representação fixa, uma biblioteca aprendida inclusive, altera o comprimento de descrição de todo alvo por no máximo uma constante aditiva; sob busca enumerativa, uma constante aditiva no comprimento é um fator multiplicativo exponencial nessa constante no tempo. Assintoticamente, portanto, **toda** vantagem de re-representação é "fator constante", e a frase da v0.1 era mal posta. O conteúdo científico de H-B1 está em outro lugar: (a) na magnitude da constante em relação ao orçamento finito, que pode ser a diferença entre tratável e intratável; (b) na amortização da constante sobre uma distribuição de tarefas, que é o que torna uma biblioteca útil e não um truque para uma tarefa; (c) em que o aprendiz **encontre** a partir dos dados a biblioteca cuja constante é pequena para a distribuição **futura**, o que é uma afirmação estatística, não de complexidade. A otimalidade da busca de Levin até fator constante (Levin 1973) **[P]** mostra o mesmo ponto do lado do procedimento. Consequência para o protocolo: o experimento reporta tamanhos de efeito em recursos finitos e nunca afirma separação assintótica.

**Nota v0.3 (terceira auditoria).** O parágrafo acima aplica um teorema sobre máquinas universais a aprendizes que não são universais: as linguagens dos experimentos têm combustível de recursão, listas truncadas e domínio finito. Nelas, (i) o comprimento mínimo de descrição de um alvo muda com uma biblioteca por um fator limitado por ocorrência (lema de inlining, documento 02, 2.0) **[P]**; (ii) o custo de busca de um enumerador não é governado pelo teorema da invariância e pode subir ou descer com a biblioteca; (iii) não há parâmetro assintótico. A conclusão operacional (reportar razões de custo finitas a orçamentos declarados, nunca separação assintótica) permanece, mas por essa razão, não pela invariância. A menção à complexidade de Levin fica como noção da camada L1 em geral; o análogo finito nos experimentos é o livro-razão de custo. Lição metodológica registrada: resultados sobre máquinas universais não justificam conclusões sobre linguagens limitadas.

**Revisão da "dissolução" do Mênon.** A v0.1 disse que o paradoxo se dissolve em termos computacionais. A v0.2 mantém isso para L0 e L1, e registra que, para L2, o paradoxo é exatamente o que está em disputa entre Carey e seus críticos: se há aquisição que não é seleção em um espaço prévio, o Mênon não está dissolvido, está reaberto **[A]**.

### 1.3 A hipótese reformulada em três partes testáveis

**H-A (realizabilidade):** a organização funcional suficiente para inteligência geral é implementável em substrato não biológico. Status: **[F]**, pressuposto de trabalho. **[R]:** demonstração de dependência de propriedade física não reproduzível. Não é objeto de experimento neste programa; é assumida.

**H-B-fraca (construtivismo representacional, forma mensurável):** existe uma dotação inicial E0, de descrição curta e fixada antes de qualquer experiência, e um regime de experiência X, tais que um sistema que parte de E0 e interage sob X constrói representações intermediárias que reduzem o custo de aprendizagem de tarefas novas em **mais do que um fator constante**, relativamente ao mesmo sistema sem o mecanismo de construção, ou com uma E0 expressivamente equivalente mas estruturada de outro modo. Status: **[C]** em domínios estreitos: DreamCoder (Ellis et al. 2021), bootstrapping numérico (Piantadosi, Tenenbaum e Goodman 2012), sistematicidade meta-aprendida (Lake e Baroni 2023). **[R]:** em experimentos bem controlados, toda vantagem é explicável por um fator constante de computação, ou desaparece quando se muda a fatoração da base.

**H-B-forte (conceitualidade):** além disso, as representações construídas são conceituais no sentido de serem invariantes a mudanças de superfície e transferíveis a domínios estruturalmente análogos, e sua aquisição depende da história de experiência (efeitos de ordem e de currículo). Status: **[H]**. **[R]:** as abstrações construídas não transferem, ou transferem igualmente a partir de qualquer currículo.

**H-C (construtivismo de método, ou meta-nível):** o próprio procedimento de aprendizagem (estratégia de busca, representação do erro, critério de parada) é revisado em função de falhas, com ganho de eficiência em famílias de tarefas novas que não se explica por transferência de representações. Status: **[H]**, com demonstrações parciais que mantêm um laço externo fixo: meta-aprendizagem (Schmidhuber 1987; Hochreiter, Younger e Conwell 2001; Finn, Abbeel e Levine 2017), aprendizagem de regras de atualização (Metz et al. 2019; Kirsch e Schmidhuber 2021) e evolução de algoritmos de aprendizagem a partir de operações elementares (Real et al. 2020). A forma ilimitada ("revisar todos os níveis") é incoerente por regressão; o caso-limite teórico é a máquina de Gödel de Schmidhuber (2003), que exige provas formais de melhoria e nunca foi instanciada de modo útil. Só formas **limitadas** de H-C são testáveis.

### 1.3-bis Revisão v0.2 — H-B em três partes

A seção 1.3 tinha H-B-fraca e H-B-forte. A v0.2 as substitui por três hipóteses alinhadas às camadas, mantendo H-A e H-C. O texto da v0.1 fica acima como registro.

**H-B1 (eficiência, camada L1).** Existe E0 de descrição curta e um regime de experiência X tais que o sistema constrói representações intermediárias que reduzem o custo de aprendizagem de tarefas novas da mesma distribuição, em recursos finitos, por um fator grande em relação ao orçamento e amortizado sobre a família de tarefas; a vantagem persiste sob mudança de fatoração de E0 e transfere a famílias estruturalmente análogas, não a distratoras. Corresponde à H-B-fraca mais a parte de transferência da H-B-forte, com a frase "mais do que um fator constante" substituída conforme 1.2-bis. Status: **[C]** em domínios estreitos (Ellis et al. 2021; Piantadosi et al. 2012; Lake e Baroni 2023) e **[E]** em humanos (Zhao, Lucas e Bramley 2024). **[R]:** vantagem igualada por orçamento ampliado dentro do mesmo regime finito, ou desaparece sob mudança de base, ou é indiscriminada entre famílias.

**H-B2 (reorganização qualitativa, camada L2).** Além de H-B1, o sistema passa a usar representações cujo conteúdo é constituído por papel inferencial e não por definição sobre representações anteriores, com mudança do conjunto de inferências licenciadas e perda em qualquer tradução para o sistema anterior. Status: **[H]** e sem operacionalização aceita **[A]**; a evidência humana é disputada (1.2-bis). **[R]:** por enquanto, só a formulação negativa é segura: se toda representação construída por um sistema é uma definição substituível sem alterar as inferências a jusante, o sistema não exibe H-B2.

**H-B3 (capacidades de generalização, camada L3).** A experiência em uma família de tarefas muda a política de generalização do sistema em famílias novas: a distribuição de primeiras hipóteses em tarefas ambíguas de uma só amostra desloca-se de modo previsível pela estrutura compartilhada. Status: **[E]** em humanos e animais (Harlow 1949; Smith et al. 2002); **[C]** em modelos hierárquicos (Kemp et al. 2007) e meta-aprendizes (Lake e Baroni 2023). **[R]:** a política de generalização não muda, ou muda igualmente após qualquer família.

Relação com a definição de trabalho (Chollet 2019): eficiência de aquisição é uma medida de L1 e L3 combinadas. A v0.2 acrescenta a regra: **esta é a primeira definição mensurável de aprendizagem do programa, não uma definição da natureza da inteligência.** O programa deve manter aberta a possibilidade de que a inteligência envolva L2 e de que L2 não seja redutível a L1 e L3.

### 1.4 As variáveis que a hipótese original deixa indefinidas

- **"Experiência"** precisa ser um regime definido: fluxo passivo de observações; interação ativa com consequências; ou diálogo com um oráculo que fornece contraexemplos. Os três têm poderes diferentes. Em particular, observação passiva não identifica estrutura causal em geral (Pearl 2009) **[C]**; a intervenção é necessária ou precisam-se assunções fortes (Schölkopf et al. 2021).
- **"Mínimo"** precisa ser quantificado: comprimento de descrição de E0, e ausência verificável dos conceitos-alvo como primitivas (ver critério de custo, seção 4.4).
- **"Comparável à inteligência humana em capacidades gerais"** não é um alvo bem definido. A definição que mais se ajusta a H-B é a de Chollet (2019): inteligência como **eficiência de aquisição de competências** sobre um escopo de tarefas, controlando priors e experiência. Alternativas: Legg e Hutter (2007), que depende da máquina de referência e é incomputável; Hernández-Orallo (2017), que discute extensamente por que testes de inteligência para máquinas são difíceis. Adotamos a definição de Chollet como definição de trabalho, com a ressalva de que ela converte "inteligência" em uma medida relativa a um escopo, não em uma propriedade absoluta.

### 1.5 O cenário em que a sua intuição está fundamentalmente errada

Ele precisa ser dito explicitamente para que possamos reconhecê-lo se aparecer. Nesse cenário:

1. A inteligência humana é, no essencial, um prior evolutivo enorme e específico a domínios (Spelke; Zador), mais aprendizagem estatística em larga escala, mais tecnologias culturais transmitidas (lógica, contagem, escrita) que nenhum indivíduo constrói (Heyes 2018; Tomasello 1999; Frank et al. 2008).
2. "Transformar os próprios princípios" não acontece em indivíduos; a sensação de construir princípios é narrativa retrospectiva sobre um processo de ajuste estatístico e de absorção cultural.
3. Sistemas estatísticos em escala, sem nenhum mecanismo desenvolvimental, atingem generalização conceitual suficiente (a "lição amarga" de Sutton 2019).

Como saberíamos que estamos nesse cenário **[R]**: (i) em todos os experimentos bem controlados, os efeitos de construção de representações são fatores constantes; (ii) a evidência desenvolvimental mostra que as mudanças conceituais em crianças são maturação ou absorção cultural, não reorganização dirigida por contradições; (iii) sistemas de escala passam em testes contrafactuais (seção 5, linha 6) sem qualquer mecanismo construtivo. O programa deve tratar (iii) como **controle obrigatório**, não como adversário.

---

## 2. As cinco objeções mais fortes

### Objeção 1 — Não existe aprendizagem sem viés (objeção lógica)

Hume formulou o problema da indução; Goodman (1955) mostrou com o predicado "grue" que nenhum conjunto finito de dados distingue entre infinitas hipóteses igualmente compatíveis, logo a escolha de quais predicados são "projetáveis" é anterior aos dados **[F]**. Mitchell (1980) mostrou que um aprendiz sem viés não generaliza, apenas memoriza **[C]**. Wolpert (1996) provou que, sem assunções sobre o problema, nenhum algoritmo de aprendizagem supera outro na média **[C]**. Locatello et al. (2019) provaram que a aprendizagem não supervisionada de representações "desemaranhadas" é impossível sem vieses indutivos, e confirmaram em larga escala que os ganhos reportados dependiam de escolhas de modelo e de hiperparâmetros **[C]**. Mesmo o prior universal de Solomonoff (1964) é um prior, e incomputável.

**Consequência para a hipótese:** P4 é ininteligível como formulada. O que sobra, e vale investigar, é se o nível fixo pode ser **pequeno e genérico** (sem conceitos de domínio) e se os conceitos de domínio vêm da experiência. Isso é contestado empiricamente, porque o conhecimento nuclear humano é específico a domínios **[E]**. A hipótese tem de conceder a objeção e sobreviver na forma H-B.

### Objeção 2 — Nada é genuinamente novo (objeção representacional)

Esta é a objeção de Fodor (1975; 1980), desenvolvida na seção 1.2. Sua versão mais incômoda: mesmo "transições de eficiência" podem ser descritas como mero *caching*. Uma abstração aprendida é uma **definição** sobre primitivas, não uma nova primitiva; chamá-la de "novo princípio de raciocínio" seria retórica.

**Resposta parcial:** a distinção entre "definição" e "primitiva" não tem significado computacional além do custo, e o custo é exatamente o que separa o que um sistema finito pode e não pode fazer. Mas a objeção obriga a hipótese a **abandonar a linguagem romântica** ("transformar os próprios princípios") e a manter apenas a linguagem mensurável (descontinuidades de custo, invariância de base, transferência). Se, depois disso, você sentir que a hipótese perdeu o que a tornava interessante, é um sinal de que o interesse estava na retórica.

**Revisão v0.2 da Objeção 2.** A "resposta parcial" acima adota a tese de Rule e Piantadosi (2025) como se fosse um fato. Não é. A v0.2 reclassifica: a questão de se "definição" e "constituição por papel inferencial" diferem além do custo é **aberta [A]**, e a seção 1.2-bis descreve os dois lados. O que permanece da objeção: um aprendiz cujas abstrações são, por construção, definições não pode alegar H-B2, e deve limitar suas alegações a H-B1 e H-B3. O que permanece da resposta: a linguagem romântica continua inadmissível, porque não há hoje critério operacional de L2 que não colapse em L1.

### Objeção 3 — Regressão normativa: toda auto-revisão exige um critério não revisado

Um sistema que revisa seus métodos precisa decidir o que conta como "melhor". Os candidatos na literatura são: erro de predição, compressão (Schmidhuber 2010; Chater e Vitányi 2003), recompensa (Silver et al. 2021, "reward is enough", tese contestada), sobrevivência. Qualquer um deles é anterior à experiência e **molda** quais "princípios" emergirão. Um sistema que revisasse o critério precisaria de um meta-critério, e assim por diante. Aristóteles já observou que o princípio de não-contradição não pode ser demonstrado porque toda demonstração o pressupõe (Metafísica Γ.3–4) **[F]**; computacionalmente, um aprendiz precisa de um detector de inconsistência que ele não pode aprender, porque é com ele que aprende.

**Consequência:** a hierarquia tem um topo fixo. H-C só é coerente em forma limitada. Além disso, sem ancoragem externa do critério (tarefa, sobrevivência, oráculo), compressão pura pode produzir "conceitos" degenerados: compressões de ruído, ou de idiossincrasias do oráculo. O experimento da seção 8 tem um controle para isso.

### Objeção 4 — O caso humano talvez não instancie a hipótese (objeção biológico-cultural)

(a) O prior evolutivo é enorme e específico (Zador 2019; Spelke 2022) **[E]**. (b) Boa parte dos "princípios de raciocínio" que associamos à inteligência humana adulta são **tecnologias culturais**: número exato depende de sistemas de contagem linguísticos (Gordon 2004; Frank, Everett, Fedorenko e Gibson 2008) **[E, com debate sobre interpretação]**; Heyes (2018) argumenta que mecanismos tidos como inatos, como leitura de mente e imitação, são "gadgets cognitivos" aprendidos culturalmente **[F/E]**; Tomasello (1999) e Henrich (2016) localizam a especificidade humana na transmissão cumulativa. (c) Cadeias de transmissão produzem estrutura (composicionalidade) que nenhum indivíduo inventa, demonstrado em laboratório por Kirby, Cornish e Smith (2008) **[E/C]**. (d) Parte do desenvolvimento é maturação, não experiência.

**Consequência:** "reproduzir o processo" pode exigir reproduzir evolução e cultura, não um aprendiz individual. Isso não refuta H-B, mas **realoca** a unidade de análise: talvez uma população com transmissão, e um regime de experiência que inclui entrada social. É uma alternativa séria de desenho, não um detalhe.

### Objeção 5 — Escala talvez baste, e os termos não estão operacionalizados (objeção metodológica)

(a) Modelos de linguagem exibem generalização com aparência conceitual sem qualquer mecanismo desenvolvimental. No ARC-AGI-2 (Chollet et al. 2025), concebido como teste de abstração resistente a memorização, páginas de resultados da ARC Prize Foundation consultadas em outubro de 2026 reportam sistemas de fronteira acima de 90% com orçamentos de computação em tempo de teste muito altos; não consegui verificar o placar oficial completo, e a trilha com computação limitada (Kaggle) ficou em torno de 24% em 2025. Ao mesmo tempo, testes contrafactuais mostram fragilidade quando a estrutura da tarefa é alterada (Wu et al. 2024; Lewis e Mitchell 2024) **[E]**. O status honesto é: **aberto**, e a tendência é que o gap se feche por computação, o que é compatível com a leitura de "eficiência" da seção 1.2, mas não com a leitura de que um mecanismo desenvolvimental é necessário.

(b) Sem definições operacionais, todo resultado pode ser lido das duas maneiras. O caso histórico é o programa AM de Lenat (1976), que "descobria" conceitos matemáticos (números primos, conjectura de Goldbach) a partir de heurísticas; a análise crítica de Ritchie e Hanna (1984) e a resposta dos próprios autores (Lenat e Brown 1984) convergiram em que boa parte da descoberta estava **implícita na representação LISP** escolhida: mutações sintáticas de expressões curtas em LISP tendem a produzir conceitos matemáticos interessantes. O sucessor EURISKO não reverteu o diagnóstico. Esta é a forma exata do problema "capacidade adquirida versus implícita no desenho".

**Consequência:** esta é a objeção mais forte na prática. Ela determina qual questão resolver primeiro (seção 9).

---

## 3. Questão A — O que estamos tentando reproduzir

### 3.1 Taxonomia operacional das capacidades

As distinções pedidas só têm valor se cada uma vier com um teste que a separe das vizinhas. Abaixo, cada capacidade é definida por **o que a quebra**.

| Capacidade | Definição operacional | O que a distingue da anterior | Teste que a quebra |
|---|---|---|---|
| Memorização | Mapeamento armazenado instância → resposta | — | Qualquer instância fora do conjunto armazenado; desempenho cai com perturbação mínima |
| Generalização estatística | Desempenho em instâncias novas da **mesma distribuição** | Responde a instâncias não vistas | Deslocamento de distribuição; extrapolação de tamanho ou comprimento (Lake e Baroni 2018) |
| Inferência | Derivação de conclusões por aplicação de operações a representações (dedutiva, indutiva, abdutiva) | Combina operações conhecidas em **combinações novas** | Sistematicidade: itens que exigem composição nunca vista de partes vistas (Fodor e Pylyshyn 1988) |
| Abstração | Representação invariante sob uma classe de transformações, reutilizável entre domínios | O conteúdo é a estrutura, não a superfície | Transferência distante: mesma estrutura, superfície inteiramente nova; mapeamento analógico (Gentner 1983; Mitchell 2021) |
| Compreensão operacional | Posse de um modelo que suporta predição contrafactual, planejamento por intervenção e explicação de falhas | Responde a "e se eu fizesse X" em condições nunca vistas (degraus 2 e 3 de Pearl) | Detecção de eventos impossíveis em configurações novas (Riochet et al. 2022; Piloto et al. 2022) |
| Aprendizagem de novas formas de representação | Mudança no espaço de hipóteses ou nas primitivas efetivas, de modo que problemas antes intratáveis ficam tratáveis | Muda **o que pode ser aprendido**, não só o que foi aprendido | Descontinuidade de custo + invariância de base + transferência (seção 4.4) |
| Revisão de métodos (meta) | Mudança no procedimento de aprendizagem em função de falhas | Muda **como** se aprende | Curvas de aprendizagem em famílias novas melhoram além do explicável por transferência de representações |

Duas observações. Primeira: as linhas 4 a 7 são as que importam para o programa, e as linhas 1 a 3 são os controles. Segunda: "compreensão" é usada aqui apenas no sentido operacional (linha 5); não fazemos nenhuma afirmação sobre consciência ou experiência subjetiva, e o programa deve evitar o vocabulário.

### 3.2 O núcleo mínimo: o que um sistema precisa ter para desenvolver conceitos

Independentemente de arquitetura, um sistema que vai formar conceitos a partir da experiência precisa de, no mínimo:

1. **Individuação:** alguma forma de segmentar o fluxo em entidades ou eventos (o problema do "binding"; Greff, van Steenkiste e Schmidhuber 2020).
2. **Comparação:** um operador de igualdade ou similaridade sobre o que foi individuado.
3. **Composição:** um modo de combinar representações em representações mais complexas.
4. **Critério de avaliação de hipóteses:** erro de predição, compressão, consistência, ou alguma combinação.
5. **Memória entre episódios.**
6. **Procedimento de busca e revisão.**
7. **Acesso a dados informativos:** ação sobre o ambiente, ou pelo menos um fluxo com estrutura explorável.

Estes sete itens constituem a E0 inevitável. A seção 4 argumenta que nenhum deles é dispensável e que a disputa científica é sobre **quanto mais** do que isso precisa estar em E0.

### 3.3 O alvo não é "inteligência humana", é eficiência de aquisição sob priors controlados

Pelo exposto em 1.4, o alvo operacional do programa é: dado E0 de descrição curta e um regime de experiência X, medir a eficiência com que o sistema adquire competências em um escopo de tarefas **que não estavam em E0**, comparando com controles que têm as competências como primitivas (teto) e que não têm mecanismo de construção (piso).

---

## 4. Questão B — O problema dos princípios anteriores à experiência

### 4.1 O paradoxo do Mênon, reformulado

A versão platônica: "não se pode procurar o que se sabe (não há o que procurar) nem o que não se sabe (não se reconheceria ao encontrar)". A versão de Fodor: não se pode testar uma hipótese que não se pode representar. A versão de aprendizagem de máquina: não se pode generalizar sem um viés que já contém, implicitamente, a classe das hipóteses projetáveis (Mitchell 1980; Goodman 1955).

As soluções possíveis, e seus correspondentes computacionais:

| Solução | Correspondente computacional | Status |
|---|---|---|
| Inatismo (reminiscência; Fodor) | Os conceitos estão no espaço de hipóteses; aprender é seleção | **[C]** trivialmente verdadeiro em expressividade; **[E]** falso como descrição do custo humano |
| Composição (Fodor concede) | Conceitos novos são composições de primitivas fixas | **[C]** modelos de linguagem do pensamento (Goodman et al. 2008; Piantadosi, Tenenbaum e Goodman 2016) |
| Bootstrapping (Carey 2009) | Um sistema simbólico vazio ("placeholder") é preenchido por mapeamento com estruturas existentes, e depois excede o que as estruturas-fonte expressavam | **[E]** evidência desenvolvimental (contagem); **[C]** Piantadosi, Tenenbaum e Goodman (2012) |
| Re-representação por compressão | Abstrações aprendidas viram primitivas efetivas, mudando o custo da busca subsequente | **[C]** DreamCoder (Ellis et al. 2021); Stitch (Bowers et al. 2023); invenção de predicados em ILP (Muggleton, Lin e Tamaddoni-Nezhad 2015; Cropper e Morel 2021) |
| Meta-aprendizagem | O procedimento de busca é ajustado por experiência em famílias de tarefas | **[C]** com laço externo fixo (seção 5, linha 5) |

A conclusão desta tabela: o Mênon tem resposta computacional, e ela é a terceira e a quarta linhas. Mas nenhuma delas é "aprender sem pressupostos". Todas pressupõem E0.

### 4.2 O que é inevitável, e por que

Para cada item, o argumento de inevitabilidade:

- **Um operador de igualdade sobre os valores sensoriais primitivos.** Sem ele, nenhuma regularidade é detectável, porque regularidade é repetição. Goodman mostrou que *similaridade* é carregada de teoria **[F]**, mas igualdade sobre primitivas não é: é a condição de qualquer processamento.
- **Uma linguagem de hipóteses com ordenação de simplicidade.** Solomonoff (1964) e Chater e Vitányi (2003) mostram que simplicidade (comprimento de descrição) é o viés mais geral que ainda permite aprender **[C/F]**, e que a escolha da linguagem de descrição é o prior. Não há escolha neutra; há escolhas mais e menos comprometidas com domínios.
- **Um detector de inconsistência.** Um sistema que não registra que a hipótese h previa x e observou não-x não pode revisar nada. Esta é a correspondência computacional do princípio de não-contradição aristotélico: não demonstrável, pressuposto por toda demonstração **[F→C]**.
- **Um critério de valor.** Seção 2, Objeção 3.
- **Memória e ordem temporal.** Sem elas, não há "experiência", apenas estímulo.
- **Ação, se o alvo incluir causalidade.** Pearl (2009) mostra que distribuições observacionais em geral não identificam a estrutura causal **[C]**. O agente que aprende causalidade ou intervém, ou herda assunções (mecanismos independentes, mudanças esparsas: Schölkopf et al. 2021). A própria ação do agente é um operador "do" natural, o que Gopnik et al. (2004) exploraram para crianças **[E]**.

### 4.2-bis Revisão v0.2 — Requisitos funcionais, não primitivas

A lista de 4.2 confundiu dois níveis: o **requisito funcional** que qualquer aprendiz deve satisfazer e a **implementação particular** que a v0.1 nomeou (um operador de igualdade, um detector de inconsistência, uma linguagem com ordenação de simplicidade). Só o primeiro nível é inevitável. Reescrita:

| Requisito funcional | Implementação simbólica | Implementação contínua ou probabilística | O que é dado e o que pode ser adquirido |
|---|---|---|---|
| **R1 Discriminabilidade**: entradas distintas podem levar a estados distintos | Operador de igualdade sobre primitivas | Métrica do espaço de estados mais uma não linearidade; capacidade de canal finita sob ruído | Dada pela física do substrato: alguma topologia. Adquirida: a resolução e quais diferenças importam (aprendizagem perceptual, E. Gibson 1969 [E]; a percepção categórica emerge em redes genéricas, Damper e Harnad 2000 [C]; Liberman et al. 1957 [E]) |
| **R2 Sinal de discrepância**: comparação entre expectativa e resultado | Contradição lógica: h implica x e observa-se não-x | Erro de predição (Rao e Ballard 1999); surpresa como log-probabilidade negativa | Dado: algum comparador de primeira ordem. Adquirido ou não: o comparador de **segunda ordem** que distingue erro de parâmetro de erro de classe de modelo (incerteza inesperada, Yu e Dayan 2005; detecção de pontos de mudança; comparação bayesiana de modelos). Se um sistema contínuo pode adquirir o de segunda ordem sem um laço externo desenhado para isso: **[A]** |
| **R3 Plasticidade dirigida pelo sinal** | Revisão de hipótese | Atualização de parâmetros | Dada como regra; a forma da regra pode ser meta-aprendida (seção 5, linha 5) |
| **R4 Ordenação de preferência** (viés) | Prior de simplicidade explícito (MDL) | Viés implícito do mapa parâmetro-função (Valle-Pérez, Camargo e Louis 2019 [C]), que pode ser prejudicial (Shah et al. 2020 [C]) | Inevitável como **viés** (Objeção 1 intacta), não como operador |
| **R5 Persistência** | Memória explícita | Mudança de pesos; estados recorrentes | Toda plasticidade é memória; o formato é implementação |
| **R6 Ação** (condicional) | Operador de intervenção | Comandos motores com consequências | Necessária se o alvo inclui causalidade no sentido de Pearl [P] |

**Evidência de que sistemas contínuos implementam revisão sem operadores explícitos [C]:** a aprendizagem em contexto de transformadores implementa atualização de tipo bayesiano (Xie et al. 2022) e até descida de gradiente dentro da passagem direta (von Oswald et al. 2023; Akyürek et al. 2023); estruturas de tipo simbólico emergem em dinâmicas contínuas de redes recorrentes (Tani 2016) e em comunicação emergente entre agentes (Lazaridou e Baroni 2020). A hipótese dinamicista (van Gelder 1998; Spivey 2007) vai além e nega operadores em qualquer nível **[F]**. O princípio da energia livre de Friston (2010) pretende unificar R2 a R4 em um único funcional; sua base formal é contestada (Bruineberg et al. 2022) **[F]**.

**Duas ressalvas que a evidência não remove.** Primeira: em todos os casos citados há um laço externo (descida de gradiente, evolução) que foi dado, e a regressão da Objeção 3 reaparece nele. Segunda: vieses implícitos continuam sendo vieses; a Objeção 1 não é tocada. O que muda em relação à v0.1 é isto: **o programa não deve colocar operadores simbólicos em E0 por omissão**. Instanciações simbólicas e contínuas de R1 a R6 são candidatas legítimas, e o experimento 2 do protocolo é onde as contínuas são testadas. A frase da v0.1 "um aprendiz precisa de um detector de inconsistência que ele não pode aprender" fica restrita ao comparador de primeira ordem; para o de segunda ordem, a questão está aberta.

### 4.3 O que pode ser derivado, segundo a evidência disponível

- **Espaço.** Philipona, O'Regan e Nadal (2003) mostraram que um agente com sensores e motores **não interpretados** pode inferir a dimensionalidade do espaço externo a partir da estrutura algébrica das contingências sensório-motoras **[C]**. Pierce e Kuipers (1997) mostraram aprendizagem de mapas a partir de sensores não interpretados **[C]**. Isso é a demonstração mais limpa de que uma categoria kantiana (espaço) pode ser derivada em vez de programada, com a ressalva de que o agente precisa de ação e de um operador de comparação.
- **Objetos e identidade ao longo do tempo.** Modayil e Kuipers (2008) mostraram um robô que individua objetos a partir de dados brutos de laser por continuidade de movimento **[C]**; modelos de atenção por "slots" (Locatello et al. 2020) individuam objetos sem supervisão em cenas simples **[C]**, com forte dependência de vieses arquiteturais. Em humanos, a individuação de objetos é muito precoce, o que sugere que, no caso biológico, é largamente nuclear **[E]**. Ou seja: derivável, mas o humano não parece derivá-la.
- **Causalidade.** Crianças pequenas aprendem estrutura causal por intervenção e observação de modo compatível com inferência bayesiana sobre redes causais (Gopnik et al. 2004) **[E]**; modelos de revisão causal online existem (Bramley et al. 2017) **[C]**. A aprendizagem de **variáveis** causais a partir de dados brutos ("causal representation learning") permanece aberta (Schölkopf et al. 2021).
- **Quantidade.** Piantadosi, Tenenbaum e Goodman (2012) mostraram que o conhecimento de cardinalidade pode ser aprendido como um programa sobre primitivas de conjuntos, mais uma lista de contagem memorizada, reproduzindo os estágios observados em crianças **[C]**. Carey (2009) argumenta que a cardinalidade exata excede os sistemas nucleares e é construída por bootstrapping **[E/F]**. A dependência de número exato em relação a sistemas culturais de contagem (Frank et al. 2008) sugere que a derivação, em humanos, é culturalmente escorada **[E]**.
- **Identidade e diferença em sentido abstrato.** Provavelmente não deriváveis: igualdade sobre primitivas é E0. O que é derivável é a **identidade de entidades** ao longo do tempo (continuidade), e a identidade de **tipos** (categorias), que é a formação de conceitos propriamente dita.

### 4.4 Como distinguir capacidade adquirida de capacidade implícita no desenho

Esta é a questão metodológica central do programa. Propomos quatro critérios conjuntos, todos operacionais:

1. **Critério de custo.** A competência-alvo tem custo de obtenção C0 a partir de E0 sem experiência (medido em passos de busca, amostras ou comprimento de descrição). Se C0 é pequeno, a competência estava implícita. "Adquirida" exige C0 grande e custo pequeno **depois** da experiência.
2. **Critério de invariância de base.** O resultado deve se manter quando E0 é substituída por E0', expressivamente equivalente mas fatorada de outro modo (outras primitivas, outra estrutura de tipos). Se a vantagem desaparece, era artefato da fatoração, o diagnóstico exato do caso AM.
3. **Critério de dependência da história.** A competência adquirida deve depender de qual experiência ocorreu e em que ordem; currículos diferentes devem produzir abstrações diferentes ou custos diferentes. O que não depende da história estava no desenho.
4. **Critério de transferência estrutural.** A competência deve reduzir o custo em tarefas estruturalmente análogas com superfície nova, e **não** reduzir em tarefas não análogas (controle de distrator). Ganho indiscriminado indica melhoria genérica de busca, não conceito.

Acrescentamos o aviso histórico: além do caso AM, o caso "Clever Hans" e a contaminação de benchmarks em modelos de linguagem mostram que o pesquisador é a fonte mais provável de erro. O experimento da seção 8 é desenhado para forçar esses quatro critérios.

### 4.4-bis Revisão v0.2 — Critérios por camada

**Para L1 (eficiência), os critérios 1, 2 e 4 da seção 4.4 permanecem. O critério 3 é substituído.** A v0.1 exigia que "currículos diferentes produzam abstrações diferentes". Isso é errado em dois sentidos: um aprendiz forte pode convergir ao mesmo ponto final a partir de qualquer ordem, e isso é robustez, não indício de que a capacidade estava no desenho; e dependência de ponto final pode ser produzida por compressão gulosa trivial, que não é conceitual. O critério 3' passa a ser **estrutura de pré-requisitos e sensibilidade de custo à ordem**: há conceitos inalcançáveis dentro do orçamento antes que outros sejam adquiridos, com um grafo de pré-requisitos previsto pela estrutura composicional dos conceitos e não pela superfície; e o custo, não necessariamente o ponto final, depende da ordem. A evidência humana apoia esta forma: Zhao, Lucas e Bramley (2024), em quatro experimentos com 570 participantes, encontram efeitos de ordem de currículo e de "caminho de jardim" na aprendizagem de conceitos causais composicionais, explicados por um modelo com biblioteca de conceitos reutilizados, e não por modelos simbólicos ou subsimbólicos sem biblioteca **[E/C]**.

**Para L2 (reorganização qualitativa), critérios candidatos, nenhum validado [A]:**

- *Constituição por papel*: substituir o corpo de uma representação construída por outro extensionalmente equivalente, mas estruturalmente diferente, não altera as inferências a jusante, porque elas dependem das relações da representação e não do seu corpo. Em aprendizes por síntese de programas isso falha por construção; o critério só se aplica a sistemas em que o conteúdo é relacional (semântica de papel conceitual, como em Piantadosi 2021, ou representações distribuídas).
- *Mudança do conjunto de inferências licenciadas*: antes e depois, o sistema afirma implicações diferentes entre os mesmos itens, e a mudança não é explicável por acréscimo monotônico de regras.
- *Perda em tradução*: um sistema restrito ao estado anterior não reproduz os julgamentos do estado posterior nem com dados ilimitados no mesmo orçamento. Ressalva: isto colapsa em L1 a menos que o orçamento seja infinito, o que mostra o tamanho do problema.

**Para L3 (capacidades de generalização):** medir a política de generalização, não o desempenho. Em tarefas ambíguas de uma só amostra numa família nova, a distribuição de primeiras hipóteses do sistema antes e depois do treino numa família relacionada deve deslocar-se na direção prevista pela estrutura compartilhada e não se deslocar após uma família distratora. É o desenho de sobre-hipóteses de Kemp, Perfors e Tenenbaum (2007) convertido em teste.

### 4.5 Indução, fundamentação de símbolos e generalização sem pressupostos

- **Indução:** tratada em 2.1. Consequência prática: o programa deve declarar explicitamente a linguagem de hipóteses e a ordenação de preferência de todo sistema testado, e medir o quanto delas é consumido pelo resultado.
- **Fundamentação de símbolos** (Harnad 1990): símbolos manipulados por regras não adquirem significado por mais regras; precisam de ligação a projeções sensório-motoras. Searle (1980) é frequentemente invocado aqui, mas o argumento da Sala Chinesa é sobre semântica e consciência, não sobre capacidade; para este programa, a versão útil é a de Harnad. Evidência recente: uma rede genérica treinada em 61 horas de vídeo e áudio de uma única criança aprende mapeamentos palavra-referente e generaliza a referentes novos (Vong, Wang, Orhan e Lake 2024) **[E/C]**, mas falha em palavras como "mão", que a criança aprende pela própria experiência corporal. Isso sugere que fundamentação por correlação multimodal vai longe, e que a parte que falta é a interação.
- **Indeterminação da referência** (Quine 1960, "gavagai") e **seguir regras** (Wittgenstein 1953, §§185–242; Kripke 1982): nenhum conjunto finito de dados fixa uma regra ou uma referência **[F]**. O que as fixa é a disposição do sistema, isto é, E0. Isso não é um problema a resolver; é uma razão a mais para que E0 seja declarada, e para que a "generalização correta" seja definida por um critério externo (o oráculo ou o ambiente), nunca pelo pesquisador que lê os programas aprendidos.

---

## 5. Questão C — O que a ciência já investigou

Síntese por linha de pesquisa. Para cada uma: o que resolveu, o que continua aberto, referências-chave. A ordenação é por proximidade com a hipótese.

### Linha 1 — Desenvolvimento cognitivo e conhecimento nuclear

**Resolveu [E]:** a caracterização dos sistemas iniciais humanos (objetos, número aproximado e pequeno, agentes, espaço, forma geométrica): Spelke (1990); Baillargeon et al. (1985); Wynn (1992); Feigenson, Dehaene e Spelke (2004); Spelke e Kinzler (2007); Spelke (2022). A demonstração de aprendizagem estatística precoce (Saffran, Aslin e Newport 1996), de aprendizagem de regras abstratas aos sete meses (Marcus et al. 1999) e de inferência estatística intuitiva aos oito meses (Xu e Garcia 2008). A demonstração de que um viés indutivo pode ser **aprendido** e depois acelerar a aprendizagem: o viés de forma treinado em crianças (Smith et al. 2002) e sua formalização como "sobre-hipóteses" em modelos bayesianos hierárquicos (Kemp, Perfors e Tenenbaum 2007). A evidência de que crianças exploram mais quando a evidência é confundida (Schulz e Bonawitz 2007; Cook, Goodman e Schulz 2011; Gopnik 2012).

**Aberto:** o mecanismo pelo qual sistemas nucleares se combinam em conceitos novos (a disputa entre Carey 2009 e os críticos de bootstrapping); quanto da mudança conceitual é experiência e quanto é maturação; o papel da linguagem como escora (Carey; Frank et al. 2008). Os modelos construtivistas de Piaget (1936; 1937; 1975) continuam sendo a descrição mais completa do processo, mas sem mecanismo computacional explícito; Drescher (1991) foi a tentativa mais séria de dar-lhe um, e ficou restrita a micro-mundos.

### Linha 2 — Modelos probabilísticos de formação de conceitos e indução de programas

**Resolveu [C]:** aprendizagem de conceitos booleanos como programas em uma linguagem do pensamento, reproduzindo a dificuldade humana (Shepard, Hovland e Jenkins 1961; Feldman 2000; Goodman et al. 2008); descoberta de forma estrutural (árvore, anel, grade) a partir de dados (Kemp e Tenenbaum 2008); aprendizagem de conceitos a partir de um único exemplo via programas probabilísticos (Lake, Salakhutdinov e Tenenbaum 2015); bootstrapping numérico (Piantadosi et al. 2012); uma proposta de origem computacional das representações simbólicas, com implementação que aprende lógica, número e estruturas recursivas (Piantadosi 2021); a agenda "a criança como hacker" (Rule, Tenenbaum e Piantadosi 2020). Em síntese de programas: crescimento de biblioteca por compressão (DreamCoder: Ellis et al. 2021; Stitch: Bowers et al. 2023; LILO: Grand et al. 2024); invenção de predicados em programação lógica indutiva (Muggleton 1991; Muggleton, Lin e Tamaddoni-Nezhad 2015; Cropper e Morel 2021; revisão em Cropper e Dumančić 2022); indução diferenciável de regras (Evans e Grefenstette 2018); síntese guiada por contraexemplos (Solar-Lezama et al. 2006; Gulwani, Polozov e Singh 2017).

**Aberto:** escalar a busca combinatória para além de domínios pequenos; ligar os programas à percepção bruta; a questão teórica de se há algo além de "definições sobre primitivas" (seção 2, Objeção 2). O problema das Bongard, do próprio Bongard (1970), permanece um bom teste: Depeweg, Rothkopf e Jäkel (2024) resolvem 35 problemas com linguagem visual e inferência bayesiana, mas com vocabulário visual dado.

### Linha 3 — Aprendizagem causal

**Resolveu [C/E]:** semântica formal da intervenção e critérios de identificabilidade (Pearl 2009); evidência de que crianças aprendem redes causais por intervenção (Gopnik et al. 2004); algoritmos de revisão causal online que reproduzem assinaturas humanas (Bramley et al. 2017).

**Aberto:** aprendizagem de variáveis causais a partir de dados brutos (Schölkopf et al. 2021 é um programa, não um resultado); a relação entre causalidade intervencionista e as causas formal e final aristotélicas, para as quais não há formalização aceita.

### Linha 4 — Robótica desenvolvimental e IA construtivista

**Resolveu [C]:** aprendizagem de espaço e de mapas a partir de sensores não interpretados (Pierce e Kuipers 1997; Philipona, O'Regan e Nadal 2003; Olsson, Nehaniv e Polani 2006); individuação de objetos e ações de alto nível a partir de dados contínuos (Modayil e Kuipers 2008; Mugan e Kuipers 2012); motivação intrínseca que auto-organiza um currículo de complexidade crescente (Oudeyer, Kaplan e Hafner 2007; Baranes e Oudeyer 2013; Forestier et al. 2022; revisão em Colas et al. 2022); auto-modelagem corporal (Bongard, Zykov e Lipson 2006). Programa geral: Weng et al. (2001); Lungarella et al. (2003); Cangelosi e Schlesinger (2015); revisão crítica em Guerin (2011). Tentativas de "IA construtivista" explícita: Drescher (1991), Thórisson (2012), Nivel et al. (2013), estas últimas com pouca replicação independente.

**Aberto:** ninguém chegou de sensores não interpretados a conceitos abstratos (número, lógica); os resultados param em espaço, objetos e ações simples; baixa replicação; forte dependência de ambientes feitos à mão.

### Linha 5 — Meta-aprendizagem, aprendizagem de algoritmos e abertura (open-endedness)

**Resolveu [C]:** que procedimentos de aprendizagem podem ser aprendidos (Schmidhuber 1987; Hochreiter et al. 2001; Finn et al. 2017; Wang et al. 2016; Duan et al. 2016); que regras de atualização podem ser meta-aprendidas (Metz et al. 2019; Kirsch e Schmidhuber 2021); que algoritmos de aprendizagem podem ser **evoluídos** a partir de operações elementares, redescobrindo retropropagação e variantes (Real et al. 2020, AutoML-Zero); que algoritmos de curiosidade podem ser meta-aprendidos (Alet et al. 2020); que ambientes gerados co-evoluindo com agentes produzem competência geral dentro de um universo de tarefas (Wang et al. 2019, POET; Open-Ended Learning Team 2021). Programas: Clune (2019), "AI-generating algorithms"; Hughes et al. (2024), tese de que abertura é essencial.

**Aberto:** o laço externo é sempre fixo e caro; aprendizes meta-aprendidos generalizam mal fora da distribuição de meta-treino; a "inteligência" pode estar no laço externo (regressão da Objeção 3).

### Linha 6 — Composicionalidade, neuro-simbólico, abstração e os testes contrafactuais

**Resolveu [C/E]:** o diagnóstico de que redes sequenciais falham em generalização sistemática (Lake e Baroni 2018), e a demonstração de que uma rede **meta-treinada** para composicionalidade atinge sistematicidade semelhante à humana em gramáticas restritas (Lake e Baroni 2023), um resultado central para H-B porque mostra o viés sendo instalado por experiência; aprendizes de conceitos neuro-simbólicos (Mao et al. 2019); o debate clássico (Fodor e Pylyshyn 1988; Smolensky 1988; Marcus 2001); revisões (Garcez e Lamb 2023). Testes de abstração: ARC (Chollet 2019; Chollet et al. 2024; 2025), ConceptARC (Moskvichev, Odouard e Mitchell 2023); um resultado notável para este programa é o CompressARC de Liao e Gu (2025): um modelo de cerca de 76 mil parâmetros, sem pré-treino, resolve cerca de 20% do conjunto de avaliação do ARC-AGI-1 minimizando o comprimento de descrição de cada enigma em tempo de inferência (valor reportado pelos autores, sem replicação independente que eu tenha encontrado). Testes contrafactuais de modelos de linguagem (Wu et al. 2024; Lewis e Mitchell 2024) e o debate sobre analogia emergente (Webb, Holyoak e Lu 2023 versus Lewis e Mitchell 2024).

**Aberto:** se a abstração "genuína" é distinguível de busca massiva em tempo de teste; o estado do ARC-AGI-2 em 2026 sugere que a distinção, se existe, não é capturada por esse benchmark isoladamente.

### Linha 7 — Teoria formal da aprendizagem e medidas de inteligência

**Resolveu [C]:** definições formais (Solomonoff 1964; Hutter 2005; Legg e Hutter 2007); limites de aprendibilidade (Gold 1967; Valiant 1984); aprendizagem por consultas e contraexemplos (Angluin 1987; 1988); teoremas de ausência de almoço grátis (Wolpert 1996); medidas com priors e experiência controlados (Chollet 2019; Hernández-Orallo 2017).

**Aberto:** versões com recursos limitados das definições universais; a distância entre definições formais e testes operacionais.

### Linha 8 — Descoberta automática de invariantes e variáveis

**Resolveu [C]:** descoberta de leis de conservação por regressão simbólica a partir de dados de movimento (Schmidt e Lipson 2009); redescoberta de equações físicas (Udrescu e Tegmark 2020); extração de parâmetros físicos interpretáveis por redes com gargalo (Iten et al. 2020); estimativa do número de variáveis de estado de sistemas dinâmicos a partir de vídeo (Chen et al. 2022). Fundamentos: representações desemaranhadas definidas por simetrias (Higgins et al. 2018); vieses relacionais e geométricos como estrutura de grupos (Battaglia et al. 2018; Bronstein et al. 2021).

**Aberto:** os sistemas descobrem variáveis mas não as "nomeiam" nem as ligam a conceitos; a escolha do espaço de funções é um prior forte.

---

## 6. Questão D — Reproduzir o processo, não programar o resultado

### 6.1 Mecanismos candidatos para cada subprocesso

| Subprocesso | Mecanismo candidato | Status |
|---|---|---|
| Construir representações internas | Compressão / comprimento mínimo de descrição; crescimento de biblioteca por refatoração de soluções | **[C]** DreamCoder; CompressARC |
| Descobrir invariantes | Extração de simetrias e de contingências sensório-motoras; gargalos de informação | **[C]** Philipona 2003; Higgins 2018; Iten 2020 |
| Individuar entidades (identidade) | Atenção por slots; rastreamento por continuidade | **[C]** em cenas simples |
| Formular hipóteses | Busca em linguagem de programas com prior de simplicidade; abdução (Peirce) | **[C]** |
| Identificar contradições | Detector de inconsistência fixo + refinamento por contraexemplos (CEGIS; Angluin; Popper de Cropper) | **[C]** |
| Corrigir generalizações inadequadas | Revisão local (exceção) versus estrutural (nova abstração); equilibração piagetiana | **[H]** não há métrica aceita para distinguir as duas |
| Gerar a própria experiência | Motivação intrínseca; exploração dirigida a progresso de aprendizagem | **[C]** Oudeyer 2007; Schmidhuber 2010 |
| Revisar os próprios métodos | Meta-aprendizagem; evolução de algoritmos | **[C]** com laço externo fixo |

### 6.2 Correspondências filosóficas, com limites

| Fonte | Correspondência computacional | Limite da correspondência |
|---|---|---|
| Mênon: paradoxo da investigação | Impossibilidade de aprender sem viés; paradoxo de Fodor | O paradoxo é correto; a solução platônica (reminiscência) é inatismo, oposto à hipótese |
| Mênon: o escravo e a geometria | Busca guiada por contraexemplos sobre uma capacidade representacional pré-dada; Sócrates age como oráculo de Angluin | O episódio mostra ensino supervisionado, não descoberta; sem o oráculo, não há diálogo |
| Elenchus socrático | Aprendizagem por consultas e contraexemplos (Angluin 1987; 1988); CEGIS; "Proofs and Refutations" de Lakatos (1976) como modelo de revisão conceitual por monstros e exceções | Exige quem conheça o conceito; na natureza o ambiente fornece contraexemplos passivamente; o "auto-elenchus" é apenas verificação de consistência interna |
| Aristóteles: epagogé (Seg. An. II.19) | Memória de instâncias → regularidade estatística → regra comprimida; hierarquia instância-protótipo-categoria | O nous que "vê" o universal não é mecanismo; quais traços abstrair é exatamente o problema de Goodman |
| Aristóteles: categorias e identidade | Sistema de tipos da linguagem de hipóteses; individuação de objetos | As categorias **são** E0 em termos computacionais; não há evidência de que sejam deriváveis |
| Aristóteles: quatro causas | Apenas a causa eficiente tem formalização aceita (intervenção, Pearl); causa final corresponde parcialmente a modelos condicionados a objetivos | Causas formal e material não têm correspondente computacional claro |
| Aristóteles: demonstração e primeiros princípios | Dedução a partir de axiomas; a parada da regressão nos primeiros princípios é o "topo fixo" da Objeção 3 | Aristóteles e o meta-aprendizado têm o mesmo problema não resolvido |
| Aristóteles: não-contradição | Detector de inconsistência como pré-condição não aprendível | — |
| Piaget: assimilação / acomodação | Atualização de parâmetros / mudança da classe de modelos | A fronteira entre os dois é o que falta medir (seção 8, medida de localidade) |
| Piaget: abstração refletidora (1977) | Abstração sobre as próprias operações, não sobre os dados: biblioteca aprendida a partir dos **programas** de solução, não das instâncias | Correspondência promissora e pouco explorada; é o que DreamCoder faz, sem citar Piaget |

### 6.3 Explicações alternativas à hipótese

1. **Inatismo forte com maturação (Spelke; Fodor):** o "processo" é desencadeamento de estrutura pré-existente; experiência seleciona, não constrói. Prediz: pouca dependência de currículo; efeitos de custo constantes.
2. **Estatística em escala (Sutton; a tradição conexionista de Elman et al. 1996 e McClelland):** representações emergem de otimização sobre dados abundantes sem nenhum mecanismo construtivo discreto. Prediz: sistemas grandes sem mecanismo passam em testes contrafactuais; o gap fecha com computação.
3. **Cultura como locus (Tomasello; Heyes; Kirby):** os princípios são artefatos externos internalizados; a unidade de análise é a população. Prediz: aprendizes isolados estagnam em conceitos de baixo nível; cadeias de transmissão produzem estrutura.
4. **Dinamicismo sem representação (Brooks 1991; Thelen e Smith 1994):** "representações" e "princípios" são glosa do observador sobre acoplamento dinâmico. Prediz: nenhuma estrutura interna discreta identificável por critérios de invariância.

O programa deve manter as quatro como hipóteses rivais vivas, e cada experimento deve dizer qual delas prediz o quê.

---

## 7. Direções de investigação distintas

Três direções realmente diferentes, mais um programa de controle obrigatório. Elas diferem na **unidade de análise**, no **regime de experiência** e no **que é fixo**.

### Direção 1 — Construtivismo sensório-motor (de sensores não interpretados a espaço, objetos e causa)

- **Hipótese:** a estrutura dos conceitos elementares (espaço, objeto, identidade, causa própria versus alheia) é a estrutura dos invariantes do laço agente-mundo; pode ser derivada por um agente com sensores e motores não interpretados, dado apenas o núcleo mínimo de 3.2.
- **Herança:** Pierce e Kuipers (1997); Philipona et al. (2003); Drescher (1991); Modayil e Kuipers (2008); O'Regan e Noë (2001).
- **O que mostraria:** que categorias "kantianas" são deriváveis sob ação.
- **[R]:** se a estrutura derivada rastreia a fiação dos sensores e não o mundo (controle: permutar a fiação; mudar a dimensionalidade do mundo), ou se nada além de espaço e objetos simples é alcançado com orçamento razoável.
- **Risco:** é a direção em que a literatura estagnou; é fiel à intuição aristotélica, mas distante de abstração.
- **Custo:** baixo (simulação em NumPy).

### Direção 2 — Linguagem do pensamento com crescimento de biblioteca sob dialética de contraexemplos

- **Hipótese:** a re-representação (abstrações construídas a partir das próprias soluções, no sentido piagetiano de abstração refletidora) produz transições de eficiência, e um oráculo de contraexemplos (elenchus) acelera e disciplina a revisão.
- **Herança:** Goodman et al. (2008); Piantadosi et al. (2012); Ellis et al. (2021); Cropper e Morel (2021); Angluin (1987); Lakatos (1976).
- **O que mostraria:** H-B-fraca e, com os controles de 4.4, H-B-forte, em micro-mundos.
- **[R]:** vantagem explicável por fator constante; vantagem desaparece com mudança de base; abstrações construídas não transferem.
- **Risco:** "estava tudo na DSL" (o fantasma do AM); por isso os controles de base.
- **Custo:** baixo (CPU, Python). **É a direção do primeiro experimento.**

### Direção 3 — Aprendizes meta-aprendidos em ambientes abertos (o método como objeto)

- **Hipótese:** H-C limitada: um laço externo fixo pode produzir aprendizes cujo procedimento muda em função de falhas, e cujo ganho em famílias novas excede a transferência de representações.
- **Herança:** Clune (2019); Real et al. (2020); Kirsch e Schmidhuber (2021); Wang et al. (2019); Hughes et al. (2024).
- **O que mostraria:** até onde "revisar os próprios métodos" é mais do que um slogan.
- **[R]:** aprendizes meta-aprendidos não generalizam fora da distribuição de meta-treino; toda a competência fica no laço externo.
- **Risco:** computação alta; a regressão da Objeção 3 se manifesta como "quem é inteligente é o laço externo".
- **Custo:** alto. Não é a primeira direção.

### Programa de controle (obrigatório, não é uma direção)

Testar os sistemas estatísticos existentes, grandes e pequenos, exatamente nas tarefas e com os controles das direções 1 e 2, com tarefas contrafactuais (Wu et al. 2024; Lewis e Mitchell 2024). Este programa é o que decide se a Objeção 5 (a) vence. Sem ele, qualquer resultado positivo das direções 1–3 é incomparável.

---

## 8. Questão E — O primeiro experimento decisivo

**Revisão v0.2.** A revisão independente identificou oito problemas no protocolo abaixo. O texto da v0.1 fica preservado nesta seção como registro; o protocolo corrigido está em `docs/02-protocolo-experimental.md`, que também especifica um segundo experimento e a ordem de execução. Os oito problemas e o que mudou:

1. **Custo computacional contabilizado parcialmente.** A v0.1 comparava orçamentos por tarefa e ignorava o custo da compressão da biblioteca e da aprendizagem anterior. A v0.2 compara custo cumulativo total, incluindo busca em todas as tarefas, compressão, consultas ao oráculo e avaliação, com o aprendiz de base fixa recebendo o mesmo total.
2. **Finito versus assintótico.** Pelo teorema da invariância (1.2-bis), nenhuma afirmação assintótica é admissível; o protocolo reporta tamanhos de efeito a orçamentos declarados e a forma da curva de vantagem em função do orçamento.
3. **Dependência de currículo.** Critério substituído por pré-requisitos e sensibilidade de custo (4.4-bis).
4. **Equivalência expressiva de E0 e E0'.** A v0.1 afirmava a equivalência sem demonstrá-la. A v0.2 exige compilações mútuas explícitas com limites de tamanho, publicadas antes das execuções.
5. **Definição dos conceitos-alvo.** Cada conceito recebe definição formal, duas implementações de referência independentes e a distribuição de amostragem de grades.
6. **Vazamento.** Partições com hashes publicados, oráculo restrito a um reservatório disjunto do teste, hiperparâmetros fixados em validação, e uma família de conceitos adversarial escrita por terceiro após o congelamento de E0.
7. **Transferência real versus heurísticas do ambiente.** Testes de invariância a transformações, transferência entre portadores (grades, sequências, grafos), controle de transferência negativa e contagem de reuso.
8. **Hipóteses sobre o controle neural.** A v0.1 previa que a rede falharia em extrapolação. Isso não é neutro e a evidência é mista. A v0.2 formula as duas saídas como resultados informativos e acrescenta um controle neural por compressão em tempo de teste.

Regra: **sucesso no experimento 1 é evidência para H-B1 em um micro-mundo simbólico. Não é evidência de inteligência geral, nem de H-B2, nem de fundamentação de símbolos.**

### 8.1 Pergunta que o experimento responde

Em um micro-mundo com dotação inicial declarada e pequena, **a construção de abstrações a partir das próprias soluções, sob um protocolo de contraexemplos, produz transições de eficiência que (i) não são fator constante, (ii) sobrevivem à mudança de base, (iii) dependem do currículo e (iv) transferem apenas para estrutura análoga?**

Se sim, H-B-fraca está demonstrada no micro-mundo e o critério de demarcação de 4.4 fica calibrado. Se não, a forma mais barata da hipótese é falsa nesse regime, o que é informativo: diz que re-representação por compressão não basta e empurra o programa para outra direção.

### 8.2 Ambiente

- **Instâncias:** grades binárias n × n. Treino com n ∈ {3, 4, 5, 6}. Teste de extrapolação com n ∈ {7, 8, 9}.
- **Conceito:** um predicado sobre grades (verdadeiro/falso). O ambiente conhece a definição; o aprendiz nunca a vê.
- **Famílias de conceitos**, pré-registradas antes de qualquer execução:
  - **F1 (rasos):** expressáveis com profundidade pequena na base. Exemplos: "a linha superior está toda preenchida"; "existe célula preta com vizinho à direita preto"; "toda linha contém pelo menos uma célula preta".
  - **F2 (exigem noção de objeto):** "há exatamente um componente conexo"; "há dois componentes que não se tocam"; "o maior componente toca a borda".
  - **F3 (exigem noção de mesmo número):** "cada linha tem tantas células pretas quanto a primeira"; "a metade esquerda tem tantas pretas quanto a direita"; "o número de componentes é igual ao número de linhas vazias".
  - **F1' (distratores):** conceitos rasos sem relação estrutural com F2 e F3, usados no controle de transferência.
- **Codificação de superfície:** 0/1 no treino; no teste de invariância, remapeada (por exemplo, três cores, das quais só uma é relevante), para checar que as abstrações são sobre estrutura.

### 8.3 Dotação inicial (E0), o que é dado

Uma linguagem de programas tipada, pequena e pré-registrada, com, aproximadamente:

- acesso a células, linhas e colunas; relação de vizinhança;
- operadores booleanos e igualdade entre valores de célula;
- quantificadores sobre células, linhas e colunas;
- operações elementares sobre listas (primeiro, resto, vazio?, mapear, filtrar) e um operador de recursão (ponto fixo);
- **sem** aritmética, **sem** contagem, **sem** noção de objeto, **sem** componente conexo, **sem** simetria.

Com essa base, "comprimento de lista" e "mesmo comprimento" são deriváveis por recursão (profundidade média), e "componente conexo" é derivável por iteração até ponto fixo (profundidade alta). A escolha final de E0 deve ser fixada por escrito **antes** das execuções, com estimativa do custo C0 de cada conceito-alvo (critério 1 de 4.4), e o experimento só é válido se C0(F2) e C0(F3) forem grandes em relação ao orçamento B.

O procedimento de aprendizagem é busca enumerativa tipada com prior de simplicidade (programas mais curtos primeiro) e orçamento B de programas avaliados por conceito. Esse procedimento é fixo em todos os aprendizes: este experimento **não** testa H-C.

### 8.4 O que não é ensinado

- As definições dos conceitos.
- Que conceitos são reutilizáveis entre tarefas.
- A decomposição de conceitos profundos em intermediários.
- Qualquer rótulo além de "sim/não" e contraexemplos.
- A ordem "certa" de abstração.

### 8.5 Protocolo de experiência (a dialética)

Para cada conceito c, em ordem de currículo F1 → F2 → F3:

1. O oráculo fornece 2 exemplos positivos e 2 negativos.
2. O aprendiz produz uma hipótese h consistente com os dados, dentro do orçamento B.
3. O oráculo busca um **contraexemplo mínimo**: a menor grade (por tamanho, depois por ordem lexicográfica) em que h e c discordam, limitada a n ≤ 5. Se não há, o conceito é dado como aprendido provisoriamente.
4. O aprendiz revisa h. Repete até K rodadas.
5. Avaliação final em conjunto reservado, incluindo tamanhos 7–9 e codificação remapeada.

O passo 3 é a correspondência do elenchus: Sócrates é um oráculo de Angluin. O passo 5 é o que impede que uma resposta certa isolada conte como prova.

### 8.6 Aprendizes comparados

- **L-mem:** memorização (tabela; vizinho mais próximo por distância de Hamming). Controle de piso.
- **L-fix:** busca em E0 fixa, orçamento B. É a condição "aplicação de regras fornecidas".
- **L-lib:** igual a L-fix, mais um passo de compressão após cada conceito aprendido: as soluções são refatoradas e os fragmentos recorrentes viram novas primitivas (no espírito de DreamCoder e Stitch). É a condição "constrói seus próprios conceitos".
- **L-nn:** uma rede convolucional pequena treinada com o mesmo número de exemplos e contraexemplos. Controle de generalização estatística; mantém redes neurais no jogo, conforme pedido.
- **L-teto:** E0 acrescida de "componente conexo" e "mesmo número" como primitivas. Limite superior.

### 8.7 Controles e manipulações

- **C1 (orçamento):** L-fix com B, 10B e 100B. Se L-fix a 10B iguala L-lib a B, o efeito é fator constante.
- **C2 (currículo embaralhado):** L-lib com F2 antes de F1, ou com F3 primeiro. Testa dependência de história.
- **C3 (mudança de base):** repetir tudo com E0', expressivamente equivalente mas fatorada de outro modo (por exemplo, quantificadores definidos via dobra em vez de primitivos; listas trocadas por conjuntos com pertinência). Se a vantagem de L-lib desaparece, era artefato de base.
- **C4 (ablação do oráculo):** substituir contraexemplos mínimos por exemplos aleatórios em número igual. Mede a contribuição da dialética.
- **C5 (lesão da biblioteca):** remover as abstrações construídas antes de F3. Mede se o ganho em F3 vem delas.
- **C6 (distrator):** L-lib treinado em F1' em vez de F1 antes de F2 e F3. Se o ganho é igual, não há transferência estrutural, apenas "qualquer treino ajuda".
- **C7 (remapeamento de superfície):** avaliação com codificação alterada.

### 8.8 Medidas

Por conceito e por aprendiz: resolvido ou não dentro de B; número de rodadas de contraexemplo; número de programas avaliados até a solução; acurácia em tamanhos 7–9; taxa de falsos positivos em negativos estruturalmente novos; **localidade da revisão** (a nova hipótese adiciona uma exceção ou reutiliza ou cria uma abstração, medida por distância de edição entre programas e por reuso de biblioteca); **regressão** (conceitos anteriores continuam corretos?); e **identidade comportamental das abstrações** (a primitiva inventada concorda com "componente conexo" ou "mesmo comprimento" em grades aleatórias de todos os tamanhos, com concordância medida, não inspeção de código).

### 8.9 Predições pré-registradas e critérios de sucesso e fracasso

Se H-B-fraca é verdadeira neste regime:

- **S1:** L-lib resolve a maioria de F2 e F3 em B; L-fix não resolve em B nem em 10B.
- **S2:** a vantagem de L-lib persiste sob C3 (mudança de base), dentro de uma tolerância fixada antes.
- **S3:** o custo de F3 após F2 é menor do que após F1' (C6), e a lesão C5 elimina o ganho.
- **S4:** L-nn generaliza dentro da distribuição e falha na extrapolação de tamanho; L-mem falha em tudo que é novo.

Resultados que contam como **fracasso ou enfraquecimento**:

- **F-a:** L-fix a 10B iguala L-lib. Leitura: efeito de eficiência constante. H-B-fraca não confirmada; a hipótese perde sua forma mais barata.
- **F-b:** a vantagem some sob C3. Leitura: artefato de base, o caso AM. O critério 2 de 4.4 fica validado como necessário.
- **F-c:** C4 iguala a dialética. Leitura: contraexemplos não importam neste regime; a correspondência com o elenchus é fraca. Resultado negativo valioso.
- **F-d:** L-lib inventa abstrações que comprimem e resolvem F3 mas **não** concordam comportamentalmente com os conceitos-alvo. Leitura: compressão não é conceito. Esta é a saída mais interessante para a teoria, porque separa duas coisas que a literatura costuma identificar.
- **F-e:** S3 falha com S1 e S2 valendo. Leitura: ganho de busca genérico, sem transferência estrutural; H-B-forte enfraquecida.

Nenhum resultado isolado em um conceito conta. Os critérios são sobre as famílias, com sementes múltiplas e intervalos reportados.

### 8.10 O que este experimento não mostra

Não mostra fundamentação de símbolos (as grades são simbólicas), nem corporificação, nem revisão de método (o procedimento de busca é fixo), nem abertura, nem nada sobre consciência. Mostra, se funcionar, que re-representação sob dialética produz transições de eficiência não triviais e calibra o critério de demarcação. Em relação à literatura, é uma replicação em miniatura do efeito de biblioteca de DreamCoder; a contribuição está nos controles C3, C4, C6, na medida de localidade da revisão e no critério de identidade comportamental, que não aparecem combinados nos trabalhos citados.

### 8.11 Recursos e reprodutibilidade

CPU, Python, algumas horas de computação por configuração, código na ordem de uma a duas mil linhas. Tudo determinístico por semente. O oráculo, a E0, a E0', as famílias de conceitos, o orçamento B e as tolerâncias são publicados antes das execuções. Os programas aprendidos são publicados, mas o critério de sucesso nunca é leitura humana deles.

### 8.12 Experimento seguinte, já apontado

Se S1–S3 valerem, o passo seguinte é a Direção 1: substituir as grades simbólicas por um agente com sensores e motores não interpretados, e perguntar se "objeto" e "mesmo número" podem ser construídos a partir de contingências sensório-motoras com a mesma bateria de controles. Se F-a ou F-b ocorrerem, o passo seguinte é o programa de controle (seção 7) e a reconsideração da Alternativa 2 (estatística em escala).

---

## 9. Qual questão resolver primeiro e por quê

**A questão a resolver primeiro é a de demarcação: como distinguir, de modo operacional e à prova do próprio pesquisador, uma capacidade adquirida de uma capacidade implícita no desenho do sistema.**

Razões:

1. **Toda outra questão depende dela.** Sem o critério, "o sistema desenvolveu o conceito" e "o conceito estava na DSL" são a mesma observação com duas narrativas. A pergunta A (o que reproduzir) só ganha conteúdo quando se diz como medir aquisição; a pergunta D (reproduzir o processo) é ininterpretável sem ela.
2. **É onde o programa pode fracassar sem perceber.** AM e EURISKO, Clever Hans, e a contaminação de benchmarks mostram que a fonte mais provável de erro é a leitura do pesquisador. Um critério publicado antes dos resultados é a única proteção.
3. **Ela é a versão computacional do paradoxo do Mênon**, e respondê-la é responder, em termos mensuráveis, à sua pergunta central: o que significa um sistema "desenvolver" princípios em vez de "recebê-los". A resposta proposta, custo mais invariância de base mais dependência de história mais transferência estrutural, converte a pergunta filosófica em quatro medições.
4. **Ela é barata.** O experimento da seção 8 cabe em um computador comum e produz, em semanas, uma calibração do critério e um primeiro veredito sobre H-B-fraca.

A segunda questão, imediatamente a seguir, é a definição do regime de experiência (passivo, ativo, dialético), porque é a variável independente que a hipótese original deixa implícita e que mais muda o que é derivável (seção 4.2, item sobre ação).

Em ordem de prioridade: demarcação → regime de experiência → mecanismos de re-representação (Direção 2) → derivação sensório-motora (Direção 1) → revisão de método (Direção 3). O que fica explicitamente fora, por ora: arquitetura definitiva, escala, e qualquer afirmação sobre consciência.

**Revisão v0.2.** A prioridade não muda: demarcação primeiro. O que muda é que a demarcação tem agora três camadas. Para L1 há critérios e um experimento. Para L3 há um critério e um teste derivável do mesmo experimento. Para L2 há apenas candidatos, e a honestidade exige dizer que, se L2 for real e irredutível, o programa ainda não tem instrumento para detectá-lo **[A]**. A segunda questão permanece o regime de experiência, e a seção 4.2-bis acrescenta uma terceira: se os requisitos funcionais R1 a R6 podem ser instanciados de modo contínuo sem que o comparador de segunda ordem seja dado. Essa terceira questão é a que o experimento 2 do protocolo começa a tocar.

---

## 10. Referências

Organizadas por área. As de 2024–2026 foram verificadas online em 2026-10-29; as demais são citadas pelos dados bibliográficos usuais e devem ser conferidas antes de publicação.

### Filosofia

- Aristóteles. *Segundos Analíticos* II.19 (99b15–100b17); *Metafísica* A.1 (980a21–981b10) e Γ.3–4 (1005b–1006a); *Categorias*; *Física* II.3 (194b16–195a3); *De Anima* III.4–5.
- Platão. *Mênon* 80d–86c; *Fédon* 72e–77a.
- Kant, I. (1781/1787). *Crítica da Razão Pura*.
- Hume, D. (1748). *Investigação sobre o Entendimento Humano*.
- Goodman, N. (1955). *Fact, Fiction, and Forecast*. Harvard University Press.
- Quine, W. V. O. (1951). "Two dogmas of empiricism". *Philosophical Review* 60(1): 20–43. Quine, W. V. O. (1960). *Word and Object*. MIT Press.
- Wittgenstein, L. (1953). *Investigações Filosóficas*, §§185–242. Kripke, S. (1982). *Wittgenstein on Rules and Private Language*. Harvard University Press.
- Popper, K. (1959). *The Logic of Scientific Discovery*. Popper, K. (1963). *Conjectures and Refutations*.
- Lakatos, I. (1976). *Proofs and Refutations*. Cambridge University Press.
- Putnam, H. (1967). "Psychological predicates". In *Art, Mind, and Religion*. University of Pittsburgh Press.
- Fodor, J. A. (1975). *The Language of Thought*. Harvard University Press. Fodor, J. A. (1980). "Fixation of belief and concept acquisition". In Piattelli-Palmarini, M. (ed.), *Language and Learning: The Debate between Jean Piaget and Noam Chomsky*. Harvard University Press. Fodor, J. A. (1998). *Concepts: Where Cognitive Science Went Wrong*. Oxford University Press.
- Fodor, J. A. e Pylyshyn, Z. W. (1988). "Connectionism and cognitive architecture: a critical analysis". *Cognition* 28: 3–71.
- Laurence, S. e Margolis, E. (2002). "Radical concept nativism". *Cognition* 86: 25–55.
- Searle, J. (1980). "Minds, brains, and programs". *Behavioral and Brain Sciences* 3(3): 417–457.
- Harnad, S. (1990). "The symbol grounding problem". *Physica D* 42: 335–346.
- Dennett, D. (1995). *Darwin's Dangerous Idea*. Simon & Schuster.
- Heyes, C. (2018). *Cognitive Gadgets: The Cultural Evolution of Thinking*. Harvard University Press.

### Desenvolvimento cognitivo

- Piaget, J. (1936). *La naissance de l'intelligence chez l'enfant*. Piaget, J. (1937). *La construction du réel chez l'enfant*. Piaget, J. (1975). *L'équilibration des structures cognitives*. PUF. Piaget, J. (1977). *Recherches sur l'abstraction réfléchissante*. PUF.
- Spelke, E. S. (1990). "Principles of object perception". *Cognitive Science* 14: 29–56.
- Baillargeon, R., Spelke, E. S. e Wasserman, S. (1985). "Object permanence in five-month-old infants". *Cognition* 20: 191–208.
- Wynn, K. (1992). "Addition and subtraction by human infants". *Nature* 358: 749–750.
- Feigenson, L., Dehaene, S. e Spelke, E. (2004). "Core systems of number". *Trends in Cognitive Sciences* 8(7): 307–314.
- Spelke, E. S. e Kinzler, K. D. (2007). "Core knowledge". *Developmental Science* 10(1): 89–96.
- Spelke, E. S. (2022). *What Babies Know: Core Knowledge and Composition*, vol. 1. Oxford University Press.
- Carey, S. (2009). *The Origin of Concepts*. Oxford University Press.
- Saffran, J. R., Aslin, R. N. e Newport, E. L. (1996). "Statistical learning by 8-month-old infants". *Science* 274: 1926–1928.
- Marcus, G. F., Vijayan, S., Bandi Rao, S. e Vishton, P. M. (1999). "Rule learning by seven-month-old infants". *Science* 283: 77–80.
- Xu, F. e Garcia, V. (2008). "Intuitive statistics by 8-month-old infants". *PNAS* 105(13): 5012–5015.
- Smith, L. B., Jones, S. S., Landau, B., Gershkoff-Stowe, L. e Samuelson, L. (2002). "Object name learning provides on-the-job training for attention". *Psychological Science* 13(1): 13–19.
- Kemp, C., Perfors, A. e Tenenbaum, J. B. (2007). "Learning overhypotheses with hierarchical Bayesian models". *Developmental Science* 10(3): 307–321.
- Gopnik, A., Glymour, C., Sobel, D. M., Schulz, L. E., Kushnir, T. e Danks, D. (2004). "A theory of causal learning in children: causal maps and Bayes nets". *Psychological Review* 111(1): 3–32.
- Schulz, L. E. e Bonawitz, E. B. (2007). "Serious fun: preschoolers engage in more exploratory play when evidence is confounded". *Developmental Psychology* 43(4): 1045–1050.
- Cook, C., Goodman, N. D. e Schulz, L. E. (2011). "Where science starts: spontaneous experiments in preschoolers' exploratory play". *Cognition* 120(3): 341–349.
- Gopnik, A. (2012). "Scientific thinking in young children". *Science* 337: 1623–1627.
- Elman, J. L., Bates, E. A., Johnson, M. H., Karmiloff-Smith, A., Parisi, D. e Plunkett, K. (1996). *Rethinking Innateness*. MIT Press.
- Thelen, E. e Smith, L. B. (1994). *A Dynamic Systems Approach to the Development of Cognition and Action*. MIT Press.
- Gordon, P. (2004). "Numerical cognition without words: evidence from Amazonia". *Science* 306: 496–499.
- Frank, M. C., Everett, D. L., Fedorenko, E. e Gibson, E. (2008). "Number as a cognitive technology: evidence from Pirahã language and cognition". *Cognition* 108: 819–824.
- Tomasello, M. (1999). *The Cultural Origins of Human Cognition*. Harvard University Press.
- Henrich, J. (2016). *The Secret of Our Success*. Princeton University Press.
- Kirby, S., Cornish, H. e Smith, K. (2008). "Cumulative cultural evolution in the laboratory". *PNAS* 105(31): 10681–10686.
- Zador, A. M. (2019). "A critique of pure learning and what artificial neural networks can learn from animal brains". *Nature Communications* 10: 3770.
- Pylyshyn, Z. W. (2001). "Visual indexes, preconceptual objects, and situated vision". *Cognition* 80: 127–158.

### Formação de conceitos, linguagem do pensamento e indução de programas

- Shepard, R. N., Hovland, C. I. e Jenkins, H. M. (1961). "Learning and memorization of classifications". *Psychological Monographs* 75(13).
- Feldman, J. (2000). "Minimization of Boolean complexity in human concept learning". *Nature* 407: 630–633.
- Goodman, N. D., Tenenbaum, J. B., Feldman, J. e Griffiths, T. L. (2008). "A rational analysis of rule-based concept learning". *Cognitive Science* 32: 108–154.
- Kemp, C. e Tenenbaum, J. B. (2008). "The discovery of structural form". *PNAS* 105(31): 10687–10692.
- Tenenbaum, J. B., Kemp, C., Griffiths, T. L. e Goodman, N. D. (2011). "How to grow a mind: statistics, structure, and abstraction". *Science* 331: 1279–1285.
- Piantadosi, S. T., Tenenbaum, J. B. e Goodman, N. D. (2012). "Bootstrapping in a language of thought: a formal model of numerical concept learning". *Cognition* 123(2): 199–217.
- Piantadosi, S. T., Tenenbaum, J. B. e Goodman, N. D. (2016). "The logical primitives of thought: empirical foundations for compositional cognitive models". *Psychological Review* 123(4): 392–424.
- Lake, B. M., Salakhutdinov, R. e Tenenbaum, J. B. (2015). "Human-level concept learning through probabilistic program induction". *Science* 350(6266): 1332–1338.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. e Gershman, S. J. (2017). "Building machines that learn and think like people". *Behavioral and Brain Sciences* 40: e253.
- Rule, J. S., Tenenbaum, J. B. e Piantadosi, S. T. (2020). "The child as hacker". *Trends in Cognitive Sciences* 24(11): 900–915.
- Piantadosi, S. T. (2021). "The computational origin of representation". *Minds and Machines* 31: 1–58.
- Ullman, T. D. e Tenenbaum, J. B. (2020). "Bayesian models of conceptual development: learning as building models of the world". *Annual Review of Developmental Psychology* 2: 533–558.
- Ellis, K., Wong, C., Nye, M., Sablé-Meyer, M., Morales, L., Hewitt, L., Cary, L., Solar-Lezama, A. e Tenenbaum, J. B. (2021). "DreamCoder: bootstrapping inductive program synthesis with wake-sleep library learning". *PLDI 2021*: 835–850.
- Bowers, M., Olausson, T. X., Wong, L., Grand, G., Tenenbaum, J. B., Ellis, K. e Solar-Lezama, A. (2023). "Top-down synthesis for library learning". *Proceedings of the ACM on Programming Languages* 7 (POPL).
- Grand, G., Wong, L., Bowers, M., Olausson, T. X., Liu, M., Tenenbaum, J. B. e Andreas, J. (2024). "LILO: Learning interpretable libraries by compressing and documenting code". *ICLR 2024*.
- Muggleton, S. (1991). "Inductive logic programming". *New Generation Computing* 8: 295–318.
- Muggleton, S. H., Lin, D. e Tamaddoni-Nezhad, A. (2015). "Meta-interpretive learning of higher-order dyadic datalog: predicate invention revisited". *Machine Learning* 100: 49–73.
- Lin, D., Dechter, E., Ellis, K., Tenenbaum, J. B. e Muggleton, S. (2014). "Bias reformulation for one-shot function induction". *ECAI 2014*.
- Cropper, A. e Morel, R. (2021). "Learning programs by learning from failures". *Machine Learning* 110: 801–856.
- Cropper, A. e Dumančić, S. (2022). "Inductive logic programming at 30: a new introduction". *Journal of Artificial Intelligence Research* 74: 765–850.
- Evans, R. e Grefenstette, E. (2018). "Learning explanatory rules from noisy data". *Journal of Artificial Intelligence Research* 61: 1–64.
- Solar-Lezama, A., Tancau, L., Bodík, R., Seshia, S. e Saraswat, V. (2006). "Combinatorial sketching for finite programs". *ASPLOS 2006*.
- Gulwani, S., Polozov, O. e Singh, R. (2017). "Program synthesis". *Foundations and Trends in Programming Languages* 4(1–2).
- Lenat, D. B. (1976). *AM: An Artificial Intelligence Approach to Discovery in Mathematics as Heuristic Search*. Tese de doutorado, Stanford. Lenat, D. B. (1983). "EURISKO: a program that learns new heuristics and domain concepts". *Artificial Intelligence* 21: 61–98.
- Lenat, D. B. e Brown, J. S. (1984). "Why AM and EURISKO appear to work". *Artificial Intelligence* 23: 269–294.
- Ritchie, G. D. e Hanna, F. K. (1984). "AM: a case study in AI methodology". *Artificial Intelligence* 23: 249–268.
- Bongard, M. M. (1970). *Pattern Recognition*. Spartan Books.
- Depeweg, S., Rothkopf, C. A. e Jäkel, F. (2024). "Solving Bongard problems with a visual language and pragmatic constraints". *Cognitive Science* 48(5): e13432. (Pré-publicação arXiv:1804.04452, 2018.)
- Gentner, D. (1983). "Structure-mapping: a theoretical framework for analogy". *Cognitive Science* 7: 155–170.
- Mitchell, M. (1993). *Analogy-Making as Perception*. MIT Press. Hofstadter, D. R. (1995). *Fluid Concepts and Creative Analogies*. Basic Books.
- Mitchell, M. (2021). "Abstraction and analogy-making in artificial intelligence". *Annals of the New York Academy of Sciences* 1505: 79–101.

### Causalidade

- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference*, 2ª ed. Cambridge University Press. Pearl, J. e Mackenzie, D. (2018). *The Book of Why*. Basic Books.
- Schölkopf, B., Locatello, F., Bauer, S., Ke, N. R., Kalchbrenner, N., Goyal, A. e Bengio, Y. (2021). "Toward causal representation learning". *Proceedings of the IEEE* 109(5): 612–634.
- Bramley, N. R., Dayan, P., Griffiths, T. L. e Lagnado, D. A. (2017). "Formalizing Neurath's ship: approximate algorithms for online causal learning". *Psychological Review* 124(3): 301–338.

### Robótica desenvolvimental e IA construtivista

- Drescher, G. L. (1991). *Made-Up Minds: A Constructivist Approach to Artificial Intelligence*. MIT Press.
- Pierce, D. e Kuipers, B. (1997). "Map learning with uninterpreted sensors and effectors". *Artificial Intelligence* 92: 169–227.
- Philipona, D., O'Regan, J. K. e Nadal, J.-P. (2003). "Is there something out there? Inferring space from sensorimotor dependencies". *Neural Computation* 15(9): 2029–2049.
- O'Regan, J. K. e Noë, A. (2001). "A sensorimotor account of vision and visual consciousness". *Behavioral and Brain Sciences* 24(5): 939–1031.
- Olsson, L., Nehaniv, C. L. e Polani, D. (2006). "From unknown sensors and actuators to actions grounded in sensorimotor perceptions". *Connection Science* 18(2): 121–144.
- Modayil, J. e Kuipers, B. (2008). "The initial development of object knowledge by a learning robot". *Robotics and Autonomous Systems* 56(11): 879–890.
- Mugan, J. e Kuipers, B. (2012). "Autonomous learning of high-level states and actions in continuous environments". *IEEE Transactions on Autonomous Mental Development* 4(1): 70–86.
- Weng, J., McClelland, J., Pentland, A., Sporns, O., Stockman, I., Sur, M. e Thelen, E. (2001). "Autonomous mental development by robots and animals". *Science* 291: 599–600.
- Lungarella, M., Metta, G., Pfeifer, R. e Sandini, G. (2003). "Developmental robotics: a survey". *Connection Science* 15(4): 151–190.
- Cangelosi, A. e Schlesinger, M. (2015). *Developmental Robotics: From Babies to Robots*. MIT Press.
- Guerin, F. (2011). "Learning like a baby: a survey of artificial intelligence approaches". *Knowledge Engineering Review* 26(2): 209–236.
- Bongard, J., Zykov, V. e Lipson, H. (2006). "Resilient machines through continuous self-modeling". *Science* 314: 1118–1121.
- Oudeyer, P.-Y., Kaplan, F. e Hafner, V. V. (2007). "Intrinsic motivation systems for autonomous mental development". *IEEE Transactions on Evolutionary Computation* 11(2): 265–286.
- Schmidhuber, J. (2010). "Formal theory of creativity, fun, and intrinsic motivation (1990–2010)". *IEEE Transactions on Autonomous Mental Development* 2(3): 230–247.
- Baranes, A. e Oudeyer, P.-Y. (2013). "Active learning of inverse models with intrinsically motivated goal exploration in robots". *Robotics and Autonomous Systems* 61(1): 49–73.
- Forestier, S., Portelas, R., Mollard, Y. e Oudeyer, P.-Y. (2022). "Intrinsically motivated goal exploration processes with automatic curriculum learning". *Journal of Machine Learning Research* 23(152): 1–41.
- Colas, C., Karch, T., Sigaud, O. e Oudeyer, P.-Y. (2022). "Autotelic agents with intrinsically motivated goal-conditioned reinforcement learning: a short survey". *Journal of Artificial Intelligence Research* 74: 1159–1199.
- Pathak, D., Agrawal, P., Efros, A. A. e Darrell, T. (2017). "Curiosity-driven exploration by self-supervised prediction". *ICML 2017*.
- Thórisson, K. R. (2012). "A new constructivist AI: from manual methods to self-constructive systems". In Wang, P. e Goertzel, B. (eds.), *Theoretical Foundations of Artificial General Intelligence*, 145–171. Atlantis/Springer.
- Nivel, E., Thórisson, K. R. et al. (2013). "Bounded recursive self-improvement". arXiv:1312.6764.
- Brooks, R. A. (1991). "Intelligence without representation". *Artificial Intelligence* 47: 139–159.

### Meta-aprendizagem, aprendizagem de algoritmos e abertura

- Schmidhuber, J. (1987). *Evolutionary principles in self-referential learning*. Diplomarbeit, TU München. Schmidhuber, J. (2003). "Gödel machines: self-referential universal problem solvers making provably optimal self-improvements". arXiv:cs/0309048.
- Hochreiter, S., Younger, A. S. e Conwell, P. R. (2001). "Learning to learn using gradient descent". *ICANN 2001*.
- Finn, C., Abbeel, P. e Levine, S. (2017). "Model-agnostic meta-learning for fast adaptation of deep networks". *ICML 2017*.
- Wang, J. X. et al. (2016). "Learning to reinforcement learn". arXiv:1611.05763. Duan, Y. et al. (2016). "RL²: fast reinforcement learning via slow reinforcement learning". arXiv:1611.02779.
- Metz, L., Maheswaranathan, N., Cheung, B. e Sohl-Dickstein, J. (2019). "Meta-learning update rules for unsupervised representation learning". *ICLR 2019*.
- Real, E., Liang, C., So, D. R. e Le, Q. V. (2020). "AutoML-Zero: evolving machine learning algorithms from scratch". *ICML 2020*.
- Kirsch, L. e Schmidhuber, J. (2021). "Meta learning backpropagation and improving it". *NeurIPS 2021*.
- Alet, F., Schneider, M. F., Lozano-Pérez, T. e Kaelbling, L. P. (2020). "Meta-learning curiosity algorithms". *ICLR 2020*.
- Clune, J. (2019). "AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence". arXiv:1905.10985.
- Wang, R., Lehman, J., Clune, J. e Stanley, K. O. (2019). "Paired open-ended trailblazer (POET)". arXiv:1901.01753.
- Open-Ended Learning Team (2021). "Open-ended learning leads to generally capable agents". arXiv:2107.12808.
- Hughes, E. et al. (2024). "Open-endedness is essential for artificial superhuman intelligence". *ICML 2024* (arXiv:2406.04268).
- Stanley, K. O. e Lehman, J. (2015). *Why Greatness Cannot Be Planned*. Springer.
- Sutton, R. S. (2019). "The bitter lesson". Ensaio online.
- Silver, D., Singh, S., Precup, D. e Sutton, R. S. (2021). "Reward is enough". *Artificial Intelligence* 299: 103535.

### Composicionalidade, neuro-simbólico, abstração e testes

- Smolensky, P. (1988). "On the proper treatment of connectionism". *Behavioral and Brain Sciences* 11(1): 1–74.
- Marcus, G. F. (2001). *The Algebraic Mind*. MIT Press.
- Lake, B. M. e Baroni, M. (2018). "Generalization without systematicity: on the compositional skills of sequence-to-sequence recurrent networks". *ICML 2018*.
- Lake, B. M. e Baroni, M. (2023). "Human-like systematic generalization through a meta-learning neural network". *Nature* 623: 115–121.
- Mao, J., Gan, C., Kohli, P., Tenenbaum, J. B. e Wu, J. (2019). "The neuro-symbolic concept learner". *ICLR 2019*.
- Garcez, A. d'A. e Lamb, L. C. (2023). "Neurosymbolic AI: the 3rd wave". *Artificial Intelligence Review* 56: 12387–12406.
- Greff, K., van Steenkiste, S. e Schmidhuber, J. (2020). "On the binding problem in artificial neural networks". arXiv:2012.05208.
- Locatello, F., Weissenborn, D., Unterthiner, T., Mahendran, A., Heigold, G., Uszkoreit, J., Dosovitskiy, A. e Kipf, T. (2020). "Object-centric learning with slot attention". *NeurIPS 2020*.
- Locatello, F., Bauer, S., Lucic, M., Rätsch, G., Gelly, S., Schölkopf, B. e Bachem, O. (2019). "Challenging common assumptions in the unsupervised learning of disentangled representations". *ICML 2019*.
- Higgins, I., Amos, D., Pfau, D., Racanière, S., Matthey, L., Rezende, D. e Lerchner, A. (2018). "Towards a definition of disentangled representations". arXiv:1812.02230.
- Battaglia, P. W. et al. (2018). "Relational inductive biases, deep learning, and graph networks". arXiv:1806.01261.
- Bronstein, M. M., Bruna, J., Cohen, T. e Veličković, P. (2021). "Geometric deep learning: grids, groups, graphs, geodesics, and gauges". arXiv:2104.13478.
- Chollet, F. (2019). "On the measure of intelligence". arXiv:1911.01547.
- Chollet, F., Knoop, M., Kamradt, G. e Landers, B. (2024). "ARC Prize 2024: technical report". arXiv:2412.04604.
- Chollet, F., Knoop, M., Kamradt, G., Landers, B. e Pinkard, H. (2025). "ARC-AGI-2: a new challenge for frontier AI reasoning systems". arXiv:2505.11831.
- Moskvichev, A., Odouard, V. V. e Mitchell, M. (2023). "The ConceptARC benchmark: evaluating understanding and generalization in the ARC domain". *Transactions on Machine Learning Research*.
- Liao, I. e Gu, A. (2025). "ARC-AGI without pretraining". arXiv:2512.06104.
- Wu, Z. et al. (2024). "Reasoning or reciting? Exploring the capabilities and limitations of language models through counterfactual tasks". *NAACL 2024* (arXiv:2307.02477).
- Lewis, M. e Mitchell, M. (2024). "Using counterfactual tasks to evaluate the generality of analogical reasoning in large language models". arXiv:2402.08955.
- Webb, T., Holyoak, K. J. e Lu, H. (2023). "Emergent analogical reasoning in large language models". *Nature Human Behaviour* 7: 1526–1541.
- Huh, M., Cheung, B., Wang, T. e Isola, P. (2024). "The Platonic representation hypothesis". *ICML 2024* (arXiv:2405.07987).
- Vong, W. K., Wang, W., Orhan, A. E. e Lake, B. M. (2024). "Grounded language acquisition through the eyes and ears of a single child". *Science* 383: 504–511.
- Piloto, L. S., Weinstein, A., Battaglia, P. e Botvinick, M. (2022). "Intuitive physics learning in a deep-learning model inspired by developmental psychology". *Nature Human Behaviour* 6: 1257–1267.
- Riochet, R. et al. (2022). "IntPhys 2019: a benchmark for visual intuitive physics understanding". *IEEE Transactions on Pattern Analysis and Machine Intelligence* 44(9).

### Teoria formal da aprendizagem e medidas de inteligência

- Solomonoff, R. J. (1964). "A formal theory of inductive inference", partes I e II. *Information and Control* 7: 1–22, 224–254.
- Gold, E. M. (1967). "Language identification in the limit". *Information and Control* 10: 447–474.
- Valiant, L. G. (1984). "A theory of the learnable". *Communications of the ACM* 27(11): 1134–1142.
- Angluin, D. (1987). "Learning regular sets from queries and counterexamples". *Information and Computation* 75: 87–106. Angluin, D. (1988). "Queries and concept learning". *Machine Learning* 2: 319–342.
- Mitchell, T. M. (1980). "The need for biases in learning generalizations". Rutgers CBM-TR-117. Mitchell, T. M. (1982). "Generalization as search". *Artificial Intelligence* 18: 203–226.
- Wolpert, D. H. (1996). "The lack of a priori distinctions between learning algorithms". *Neural Computation* 8(7): 1341–1390.
- Chater, N. e Vitányi, P. (2003). "Simplicity: a unifying principle in cognitive science?". *Trends in Cognitive Sciences* 7(1): 19–22.
- Hutter, M. (2005). *Universal Artificial Intelligence*. Springer.
- Legg, S. e Hutter, M. (2007). "Universal intelligence: a definition of machine intelligence". *Minds and Machines* 17: 391–444.
- Hernández-Orallo, J. (2017). *The Measure of All Minds*. Cambridge University Press.
- Newell, A. e Simon, H. A. (1976). "Computer science as empirical inquiry: symbols and search". *Communications of the ACM* 19(3): 113–126.

### Descoberta de invariantes e variáveis

- Schmidt, M. e Lipson, H. (2009). "Distilling free-form natural laws from experimental data". *Science* 324: 81–85.
- Udrescu, S.-M. e Tegmark, M. (2020). "AI Feynman: a physics-inspired method for symbolic regression". *Science Advances* 6(16): eaay2631.
- Iten, R., Metger, T., Wilming, H., del Rio, L. e Renner, R. (2020). "Discovering physical concepts with neural networks". *Physical Review Letters* 124: 010508.
- Chen, B., Huang, K., Raghupathi, S., Chandratreya, I., Du, Q. e Lipson, H. (2022). "Automated discovery of fundamental variables hidden in experimental data". *Nature Computational Science* 2: 433–442.
- Cranmer, M. et al. (2020). "Discovering symbolic models from deep learning with inductive biases". *NeurIPS 2020*.


### Referências acrescentadas na v0.2

Verificadas online em 2026-10-29, salvo indicação.

**Debate sobre bootstrapping e nativismo de conceitos**

- Carey, S. (2011). "Précis of *The Origin of Concepts*" e "Concept innateness, concept continuity, and bootstrapping" (resposta aos comentários). *Behavioral and Brain Sciences* 34(3).
- Carey, S. (2014). "On learning new primitives in the language of thought: reply to Rey". *Mind & Language* 29(2). (Existência verificada online; paginação não verificada.)
- Carey, S. (2015). "Why theories of concepts should not ignore the problem of acquisition". *Disputatio* 7(41): 113–163. Também em Margolis, E. e Laurence, S. (eds.), *The Conceptual Mind*, MIT Press, 415–454.
- Rips, L. J., Asmuth, J. e Bloomfield, A. (2006). "Giving the boot to the bootstrap: how not to learn the natural numbers". *Cognition* 101: B51–B60.
- Rips, L. J., Bloomfield, A. e Asmuth, J. (2008). "From numerical concepts to concepts of number". *Behavioral and Brain Sciences* 31: 623–642 (com comentários até p. 687).
- Rips, L. J. e Hespos, S. J. (2011). "Rebooting the bootstrap argument: two puzzles for bootstrap theories of concept development". *Behavioral and Brain Sciences* 34(3).
- Rips, L. J., Asmuth, J. e Bloomfield, A. (2013). "Can statistical learning bootstrap the integers?". *Cognition* 128: 320–330.
- Margolis, E. e Laurence, S. (2008). "How to learn the natural numbers: inductive inference and the acquisition of number concepts". *Cognition* 106: 924–939. (Não verificada online nesta data.)
- Margolis, E. e Laurence, S. (2011). "Beyond the building blocks model". *Behavioral and Brain Sciences* 34(3).
- Shea, N. (2011). "Acquiring a new concept is not explicable-by-content". *Behavioral and Brain Sciences* 34(3).
- Beck, J. (2017). "Can bootstrapping explain concept learning?". *Cognition* 158: 110–121.
- Pantsar, M. (2021). "Bootstrapping of integer concepts: the stronger deviant-interpretation challenge (and how to solve it)". *Synthese* 199: 5791–5814.
- Rey, G. (2014). "Innate and learned: Carey, Mad Dog Nativism, and the poverty of stimuli and analogies (yet again)". *Mind & Language* 29(2): 109–132.
- Rule, J. S. e Piantadosi, S. T. (2025). "The end of radical concept nativism". arXiv:2505.18277.
- Fodor, J. A. (2008). *LOT 2: The Language of Thought Revisited*. Oxford University Press. (Não verificada online nesta data.)
- Le Corre, M. e Carey, S. (2007). "One, two, three, four, nothing more: an investigation of the conceptual sources of the verbal counting principles". *Cognition* 105: 395–438. (Não verificada online nesta data.)
- Sarnecka, B. W. e Carey, S. (2008). "How counting represents number: what children must learn and when they learn it". *Cognition* 108: 662–674. (Não verificada online nesta data.)
- Zhao, B., Lucas, C. G. e Bramley, N. R. (2024). "A model of conceptual bootstrapping in human cognition". *Nature Human Behaviour* 8: 125–136.

**Mudança conceitual e capacidades de generalização**

- Kuhn, T. S. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press.
- Chi, M. T. H. (1992). "Conceptual change within and across ontological categories: examples from learning and discovery in science". In Giere, R. (ed.), *Cognitive Models of Science*. University of Minnesota Press.
- Thagard, P. (1992). *Conceptual Revolutions*. Princeton University Press.
- Nersessian, N. J. (2008). *Creating Scientific Concepts*. MIT Press.
- Karmiloff-Smith, A. (1992). *Beyond Modularity: A Developmental Perspective on Cognitive Science*. MIT Press.
- Clark, A. e Karmiloff-Smith, A. (1993). "The cognizer's innards: a psychological and philosophical perspective on the development of thought". *Mind & Language* 8(4): 487–519.
- Harlow, H. F. (1949). "The formation of learning sets". *Psychological Review* 56: 51–65.

**Complexidade com recursos limitados**

- Levin, L. A. (1973). "Universal sequential search problems". *Problems of Information Transmission* 9(3): 265–266.
- Li, M. e Vitányi, P. (2008). *An Introduction to Kolmogorov Complexity and Its Applications*, 3ª ed. Springer.
- Grünwald, P. D. (2007). *The Minimum Description Length Principle*. MIT Press.
- Bennett, C. H. (1988). "Logical depth and physical complexity". In Herken, R. (ed.), *The Universal Turing Machine: A Half-Century Survey*. Oxford University Press.
- Schmidhuber, J. (2002). "The speed prior: a new simplicity measure yielding near-optimal computable predictions". *COLT 2002*.
- Lieder, F. e Griffiths, T. L. (2020). "Resource-rational analysis: understanding human cognition as the optimal use of limited computational resources". *Behavioral and Brain Sciences* 43: e1.
- Marr, D. (1982). *Vision*. W. H. Freeman.

**Implementações contínuas dos requisitos funcionais**

- Liberman, A. M., Harris, K. S., Hoffman, H. S. e Griffith, B. C. (1957). "The discrimination of speech sounds within and across phoneme boundaries". *Journal of Experimental Psychology* 54: 358–368.
- Gibson, E. J. (1969). *Principles of Perceptual Learning and Development*. Appleton-Century-Crofts.
- Damper, R. I. e Harnad, S. R. (2000). "Neural network models of categorical perception". *Perception & Psychophysics* 62(4): 843–867.
- Rao, R. P. N. e Ballard, D. H. (1999). "Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects". *Nature Neuroscience* 2: 79–87.
- Yu, A. J. e Dayan, P. (2005). "Uncertainty, neuromodulation, and attention". *Neuron* 46: 681–692.
- Valle-Pérez, G., Camargo, C. Q. e Louis, A. A. (2019). "Deep learning generalizes because the parameter-function map is biased towards simple functions". *ICLR 2019*.
- Shah, H., Tamuly, K., Raghunathan, A., Jain, P. e Netrapalli, P. (2020). "The pitfalls of simplicity bias in neural networks". *NeurIPS 2020*.
- Xie, S. M., Raghunathan, A., Liang, P. e Ma, T. (2022). "An explanation of in-context learning as implicit Bayesian inference". *ICLR 2022*.
- von Oswald, J. et al. (2023). "Transformers learn in-context by gradient descent". *ICML 2023*.
- Akyürek, E., Schuurmans, D., Andreas, J., Ma, T. e Zhou, D. (2023). "What learning algorithm is in-context learning? Investigations with linear models". *ICLR 2023*.
- Tani, J. (2016). *Exploring Robotic Minds: Actions, Symbols, and Consciousness as Self-Organizing Dynamic Phenomena*. Oxford University Press.
- Lazaridou, A. e Baroni, M. (2020). "Emergent multi-agent communication in the deep learning era". arXiv:2006.02419.
- van Gelder, T. (1998). "The dynamical hypothesis in cognitive science". *Behavioral and Brain Sciences* 21: 615–665.
- Spivey, M. (2007). *The Continuity of Mind*. Oxford University Press.
- Bruineberg, J., Dołęga, K., Dewhurst, J. e Baltieri, M. (2022). "The Emperor's new Markov blankets". *Behavioral and Brain Sciences* 45: e183.
- Wiskott, L. e Sejnowski, T. J. (2002). "Slow feature analysis: unsupervised learning of invariances". *Neural Computation* 14: 715–770.
- Xu, F. e Spelke, E. S. (2000). "Large number discrimination in 6-month-old infants". *Cognition* 74: B1–B11.
