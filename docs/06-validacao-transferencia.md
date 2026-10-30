# 06 — Validação independente e aprendizagem autodirigida

**Versão 0.1** (rascunho em construção: as secções 2–4 são preenchidas pelos registros `runs/rep-1`, `runs/ca-*` e `runs/tr-*` à medida que terminam).

Pergunta decisiva deste documento: *Fedro consegue usar o que aprendeu para escolher o que aprender a seguir e transferir isso para problemas cuja estrutura não foi preparada pelo pesquisador?* A resposta é dada em quatro partes separadas (§6): o que foi demonstrado, o que falhou, o que permanece inconclusivo e qual a experiência mais informativa a seguir. O experimento confirmatório **não** foi executado; todas as sementes usadas estão no intervalo exploratório (10000–19999) e os buckets 50–99 continuam intocados.

Rótulos epistêmicos como nos documentos anteriores: **[P]** prova, **[E]** evidência empírica dos registros, **[C]** resultado computacional reproduzível, **[F]** falha, **[H]** hipótese, **[R]** requisito, **[A]** questão em aberto.

---

## 1. Correção das medições

### 1.1 Verificação exaustiva incorporada ao repositório **[C]**

O código que no documento 05 verificou as hipóteses à parte foi incorporado como `fedro_piloto/verificacao.py` e corre sobre qualquer registro (`python3 -m fedro_piloto.verificacao --run runs/<id>`), gravando `<run>/verificacao.json`. Dois regimes, **distinguidos explicitamente no rótulo do registro**:

| regime | predicados (Grade → Bool) | funções (Grade → Pos → ·, Grade → L Pos → ·, Grade → ·) |
|---|---|---|
| exaustivo | **todas** as grades com n ≤ 4 (2 + 16 + 512 + 65 536) | todas as grades com n ≤ 4 **× bateria finita de argumentos do ambiente** (`entradas_da_grade`: todas as posições; listas derivadas da grade). Rótulo: "exaustivo em grades (n ≤ 4), bateria finita de argumentos do ambiente" — **não** é exaustivo nos argumentos funcionais, cujo espaço é infinito |
| amostral | grades da mistura natural (k = 40 por n) **e** conjunto de desenho (positivos construtivos + negativos emparelhados por densidade) em n = 5..9 | grades da mistura natural em n = 5..9 × bateria de argumentos |

A partição usada no regime amostral é `teste_ext` (buckets 40–49): nunca foi vista pelos aprendizes (treino em `oraculo_treino`, buckets 0–19; teste em `teste_int`, 30–39). As dimensões 5–9 nunca foram vistas por nenhum aprendiz (reservatório do oráculo em n ∈ {5, 6}, mas só para contraexemplos de predicados; as grades de teste amostral vêm de outra partição).

Resultado sobre os dois registros do documento 05 **[E]**:

| registro | hipóteses aceitas | entradas exaustivas (n ≤ 4) | erros | entradas amostrais (n = 5..9, natural) | erros | entradas de desenho (predicados) | erros | indefinidas por orçamento |
|---|---|---|---|---|---|---|---|---|
| `em-s10002-tamanho` | 10 | 7 971 362 | 0 | 6 800 | 0 | 310 | 0 | 0 |
| `em-s10002-unigrama` | 15 | 9 884 880 | 0 | 9 000 | 0 | 775 | 0 | 0 |

Todas as 25 hipóteses aceitas (incluindo as dos braços de controlo e das sondas) são corretas em todas as grades com n ≤ 4 (na bateria do ambiente) e em todas as grades amostradas de n = 5 a 9. Isto corrige a limitação do documento 05, em que a verificação exaustiva fora feita por código não versionado e sem o regime amostral em dimensões novas. Limitação que permanece **[A]**: a bateria de argumentos funcionais é finita e fixa (listas derivadas da própria grade); programas corretos nessa bateria podem falhar em listas arbitrárias (por exemplo, listas com posições repetidas ou fora da grade), que o ambiente nunca apresenta.

### 1.2 Veredito automático com cinco condições **[C]**

`experimento_minimo.analisar` passou a emitir o veredito do critério central apenas quando **todas** as condições seguintes se verificam para o braço L-lib+f:

1. **Reutilização em tarefa inédita**: uma entrada da biblioteca, descoberta pelo próprio aprendiz numa tarefa anterior, ocorre na hipótese aceita de uma tarefa posterior que o aprendiz nunca tinha visto.
2. **Procedência**: a entrada tem certificado de descoberta (cadeia HMAC busca → descoberta → entrada); nenhuma entrada manual ou de referência está na tabela.
3. **Custo total verificável**: a soma das entradas do livro-razão do braço fecha com o custo cumulativo final da curva (`_fechamento_livro`); as sondas que não preservam o histórico não entram.
4. **Controlos piores nas tarefas de reutilização a que se aplicam**: lesão (biblioteca apagada antes de ParAdjacente) e currículo não relacionado têm de falhar, ou custar mais, **na tarefa posterior à intervenção**. Correção desta versão: a condição aplicava-se antes a *todas* as tarefas de reutilização, incluindo `expandir`, que no braço de lesão é resolvida **antes** da lesão (logo ao mesmo custo) e que não existe no currículo de controlo; o veredito era falso por um artefacto da análise e não por evidência contrária. Agora a aplicabilidade é lida dos eventos registados (`lesao` com `antes_de`) e do currículo do braço.
5. **Mais tarefas do que L-fix a custo cumulativo igual**: para cada tarefa aceita por L-lib+f ao custo cumulativo C, conta-se quantas tarefas L-fix tinha aceitado com custo cumulativo ≤ C na **sua própria** curva (`custo_cumulativo_igual`). Isto substitui a antiga sonda "custo igual", que não preservava o histórico de aprendizagem de nenhum dos dois sistemas; as sondas foram renomeadas `L-fix/orcamento-extra` e `L-fix/sonda-10x` e marcadas como não comparáveis.

Resultado nos dois registros (análise `analise_v2` gravada em `deterministico.json`) **[E]**:

| registro | 1 reuso | 2 proced. | 3 livro fecha | 4 controlos (ParAdjacente) | 5 custo cumul. igual | veredito |
|---|---|---|---|---|---|---|
| tamanho | expandir←abs1, ParAdjacente←abs2 | sim | 114 681 651 = 114 681 651 | lesão: falha a 91,8 M; controlo: falha a 78,6 M (L-lib+f aceita a 3,8 M) | a C = 14,6 M: L-lib+f 3 tarefas, L-fix 1 | **verdadeiro** |
| unigrama | expandir←abs1, ParAdjacente←abs2 | sim | 439 063 707 = 439 063 707 | lesão: aceita a 84,4 M; controlo: falha a 259,6 M (L-lib+f aceita a 13,7 M) | a C = 28,3 M: L-lib+f 3 tarefas, L-fix 1 | **verdadeiro** |

O que o veredito **não** afirma: nada sobre H-B1, nada sobre formação de conceitos (§5), nada sobre tarefas fora do currículo de quatro degraus. Ele afirma apenas que, nesta semente e neste orçamento, o mecanismo de promoção de soluções produziu uma operação reutilizada numa tarefa inédita, com procedência verificável, custo total conciliado e vantagem sobre os controlos e sobre L-fix a custo igual.

### 1.3 Sinal de busca exposto ao aprendiz **[C]**

`ContadorBusca.tamanho_max_carregado` regista o maior tamanho (custo) de termo carregado na busca de cada tarefa. É um sinal legítimo para a seleção de tarefas (§3): descreve a própria busca, não a solução.

---

## 2. Replicação independente

(preenchido a partir de `runs/rep-1/resumo.json`)

## 3. Currículo autodirigido

### 3.1 Desenho **[C]**

`fedro_piloto/curriculo_autodirigido.py`. O ambiente disponibiliza um **conjunto** de seis tarefas sem ordem (vizPretos, expandir, ParAdjacente, NenhumaIsolada, pretasColuna1, semLinha1: os quatro degraus do documento 05 e as duas tarefas do currículo não relacionado). Um seletor escolhe a tarefa seguinte e o orçamento de enumeração da tentativa. Três seletores, todos com o mesmo orçamento global G (candidatos de enumeração acumulados, 240 000) e o mesmo limite por tentativa B_max (20 000, o B do documento 05):

| seletor | regra | informação usada |
|---|---|---|
| manual | ordem prescrita do documento 05 (T1 T2 T3 T4 U1 U2), uma passagem com B_max; repete uma tarefa só se a biblioteca mudou desde a sua última tentativa | ordem fixa; histórico |
| aleatório | ordem uniforme ao acaso entre as elegíveis (três sementes próprias do seletor: 1, 2, 3), mesma regra de repetição | histórico |
| autodirigido | aprofundamento iterativo com progresso: cada tarefa pendente tem um orçamento próximo (2 000 na primeira tentativa; dobra após cada falha); se a biblioteca mudou desde a última tentativa da tarefa, oferece-se **uma** repetição com o mesmo orçamento (a tarefa pode ter ficado mais barata); escolhe-se a tarefa de menor orçamento efetivo (empate: repetição com biblioteca nova, depois menos tentativas, depois id) | histórico de tentativas (orçamento, resultado, custo), versão da biblioteca, maior tamanho carregado |

Legalidade **[R]**: o seletor recebe apenas objetos `HistoricoTarefa` (id, tipo, tentativas, aceita, custos, último orçamento, último motivo de paragem, maior tamanho carregado, versão da biblioteca na última tentativa, orçamento próximo, número de exemplos finais). Não recebe os objetos `Tarefa`, as referências do ambiente, os tamanhos mínimos conhecidos (tabela do documento 02) nem as definições dos conceitos. O teste `test_seletores_nao_consultam_referencias` confere, no código-fonte dos seletores (sem docstrings), a ausência de qualquer acesso a `REFERENCIAS_FUNCAO`, `REGISTRO`, `saida_referencia`, `programas_referencia`, `TAREFAS` e afins, e que os campos do histórico são exatamente os listados. O custo das sondas do seletor autodirigido conta no orçamento global e no livro-razão como qualquer tentativa.

Os seletores correm com dois aprendizes (L-lib+f e L-fix), semente de dados 10002 (a mesma do documento 05, para comparação direta com a ordem manual), política de tamanho. A pergunta é se a cadeia vizPretos → expandir → ParAdjacente **aparece sem ser prescrita** e a que custo, em comparação com a ordem manual e com ordens aleatórias.

### 3.2 Resultados

(preenchido a partir de `runs/ca-s10002-tamanho/deterministico.json`)

## 4. Transferência estrutural

### 4.1 Famílias congeladas **[C]**

`fedro_piloto/familias_transferencia.py` define nove tarefas novas, nenhuma presente no currículo do documento 05, em duas famílias. A especificação (ids, tipos, natureza, comparação, código-fonte Python das referências do ambiente, programas de referência na DSL e os seus tamanhos) tem o hash SHA-256

`3b6646466e4545926d2c0cd990c792d7a3775e7da294ea059a4eb1e2a1d74aca`

gravado em `HASH_CONGELADO` e conferido pelo teste `test_hash_congelado`; o executor `transferencia.executar` recusa-se a correr se o hash do módulo diferir. A família foi congelada às **13:04 UTC de 2026-10-30**, antes do lançamento da execução `runs/tr-s10002` (13:04:42 UTC), e não foi alterada depois. Uma única correção foi feita **antes** do congelamento e **antes** de qualquer execução de avaliação: o programa de referência na DSL para LinhaOcupada codificava "alguma linha toda preta"; a verificação exaustiva contra o REGISTRO (41 382 erros em n ≤ 4) mostrou que o conceito registado é "toda linha tem pelo menos uma preta", e o programa foi corrigido (hash anterior `f0085ade…`). A tarefa em si, definida pelo REGISTRO, não mudou. Nem a DSL nem a biblioteca foram ajustadas depois de observar resultados.

Os programas de referência na DSL (proveniência manual-teste; nunca entram numa biblioteca de aprendiz) foram verificados exaustivamente em n ≤ 4 contra as referências Python: 0 erros nas 18 versões (E0 puro e com as abstrações manuais absViz ≡ corpo de vizPretos e absExp ≡ corpo de expandir). Servem só para provar exprimibilidade e dar limites superiores de tamanho:

| tarefa | família | tipo | o que calcula | tamanho E0 | tamanho com absViz/absExp |
|---|---|---|---|---|---|
| expandir2 | F-comp | Grade → L Pos → L Pos | vizinhas pretas em dois passos (expandir ∘ expandir) | 21 | 7 |
| fronteira | F-comp | Grade → L Pos → L Pos | vizinhas pretas de S que não estão em S | 14 | 7 |
| isoladaP | F-comp | Grade → Pos → Bool | p é preta e sem vizinha preta (NenhumaIsolada ≡ ∀p ¬isoladaP, com pretas) | 13 | 10 |
| duasVizinhas | F-comp | Grade → Pos → Bool | p tem ≥ 2 vizinhas pretas | 11 | 8 |
| pretasComVizinha | F-comp | Grade → L Pos | pretas com alguma vizinha preta (= expandir g (pretas g)) | 11 | 5 |
| TopoCheio | F-neg | Grade → Bool | primeira linha toda preta (REGISTRO) | 7 | 7 |
| LinhaOcupada | F-neg | Grade → Bool | toda linha tem alguma preta (REGISTRO) | 9 | 9 |
| pretasUltimaColuna | F-neg | Grade → L Pos | pretas da última coluna | 8 | 8 |
| semColuna1 | F-neg | Grade → L Pos → L Pos | S sem as células da primeira coluna | 7 | 7 |

F-comp exige **composições inéditas** das operações adquiridas na cadeia (vizPretos, expandir): composição consigo mesma (expandir2), com `diferenca` (fronteira), com `pretas` (pretasComVizinha), com `cauda` (duasVizinhas) e com `celula`/`e` (isoladaP). F-neg são tarefas em que essas operações são inúteis (linhas, colunas, bordas): aqui a biblioteca só pode atrapalhar (gramática maior; na política unigrama, constantes da cadeia baratas e constantes necessárias caras). Alcance esperado com B = 20 000 (documento 05, §4): tamanhos 7–9 ao alcance de L-fix; 10–11 só com a política unigrama; ≥ 12 fora do alcance. Logo, **sem** abstrações, expandir2, fronteira e isoladaP estão fora do alcance, pretasComVizinha e duasVizinhas no limite; **com** abs1/abs2, todas as F-comp exceto isoladaP (10) ficam ao alcance.

### 4.2 Protocolo **[C]**

`fedro_piloto/transferencia.py`. Para cada política (tamanho, unigrama) e aprendiz (L-lib+f, L-fix), o aprendiz passa pela cadeia T1 vizPretos → T2 expandir → T3 ParAdjacente (a mesma exposição para ambos; só o mecanismo de biblioteca difere; para L-fix a cadeia só afeta a política unigrama, através das constantes das suas soluções) e é então **fotografado** (cópia profunda). Cada tarefa das famílias é tentada a partir da mesma fotografia, independentemente das outras: sem efeitos de ordem e sem que a biblioteca receba soluções das tarefas de avaliação. B = 20 000 por tarefa, K = 12 rodadas, semente 10002. Medidas: aceitação, custo (livro-razão), reutilização de entradas da biblioteca na hipótese aceita, tamanho; por família, razão de custo L-lib+f / L-fix e contagem de transferências positivas (L-lib+f aceita e L-fix não, ou ambos aceitam e L-lib+f é mais barato) e negativas (o inverso).

### 4.3 Resultados

(preenchido a partir de `runs/tr-s10002/deterministico.json`)

## 5. Objetivo científico preservado

## 6. Demonstrado, falhado, inconclusivo, próximo

## 7. Comandos, registros e desvios
