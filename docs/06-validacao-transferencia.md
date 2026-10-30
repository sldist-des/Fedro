# 06 — Validação independente e aprendizagem autodirigida

**Versão 0.1** — 2026-10-30. Código, testes (243) e registros em `fedro_piloto/` e `runs/`; comandos em §7.

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

### 2.1 Desenho **[C]**

`fedro_piloto/replicacao.py` executa o experimento mínimo completo (cinco braços: L-fix, L-lib, L-lib+f, L-lib+f/lesão, L-lib+f/controlo; sem sondas e sem auditoria OE) para cada par (semente, política), com B = 20 000 e K = 12, e agrega os resultados (`runs/rep-1/resumo.json`, `resumo.md`). Sementes 10003, 10004, 10005 e 10006: nunca usadas antes (10001 no piloto, 10002 no documento 05) e dentro do intervalo exploratório; `verificar_sementes` recusa sementes já usadas ou fora de 10000–19999 (teste `test_guarda_de_sementes`). Nenhum dado das partições reservadas foi tocado: as 8 execuções usam `oraculo_treino` para exemplos e `teste_int` para o teste; os buckets 50–99 continuam intactos.

### 2.2 Resultados **[E]**

Oito execuções (4 sementes × 2 políticas), 40 braços, 0 falhas de braço, 3 934 s de parede no total (4 processos):

| semente | política | L-lib+f: cumul. até T3 | L-fix: tarefas / cumul. até T3 | lesão em ParAdjacente | controlo em ParAdjacente | tarefas a custo cumul. igual (L-lib+f vs L-fix) | livro fecha | veredito | parede |
|---|---|---|---|---|---|---|---|---|---|
| 10003 | tamanho | 14.7 M | 1 / 258.7 M | falha a 139.6 M | falha a 90.9 M | 3 vs 1 | sim | **verdadeiro** | 228 s |
| 10003 | unigrama | 28.4 M | 3 / 271.0 M | aceita a 85.8 M | falha a 324.1 M | 3 vs 1 | sim | **verdadeiro** | 548 s |
| 10004 | tamanho | 14.3 M | 1 / 260.2 M | falha a 139.3 M | falha a 90.1 M | 3 vs 1 | sim | **verdadeiro** | 320 s |
| 10004 | unigrama | 27.6 M | 3 / 272.2 M | aceita a 84.4 M | falha a 320.9 M | 3 vs 1 | sim | **verdadeiro** | 825 s |
| 10005 | tamanho | 14.6 M | 1 / 261.3 M | falha a 139.5 M | falha a 91.2 M | 3 vs 1 | sim | **verdadeiro** | 230 s |
| 10005 | unigrama | 27.5 M | 3 / 272.9 M | aceita a 84.4 M | falha a 323.4 M | 3 vs 1 | sim | **verdadeiro** | 790 s |
| 10006 | tamanho | 14.5 M | 1 / 211.5 M | falha a 92.9 M | falha a 78.9 M | 3 vs 1 | sim | **verdadeiro** | 295 s |
| 10006 | unigrama | 27.7 M | 3 / 268.4 M | aceita a 84.4 M | falha a 258.2 M | 3 vs 1 | sim | **verdadeiro** | 698 s |

Agregado por política e braço (mín / mediana / máx sobre as 4 sementes):

| política | braço | tarefas aceitas | aceitas por tarefa (T1, T2, T3, T4) | custo cumul. até T3 | com reutilização |
|---|---|---|---|---|---|
| tamanho | L-fix | 1 / 1 / 1 | 4, 0, 0, 0 | 211,5 M / 259,5 M / 261,3 M | 0 |
| tamanho | L-lib | 1 / 1 / 1 | 4, 0, 0, 0 | 211,5 M / 259,5 M / 261,3 M | 0 |
| tamanho | L-lib+f | 3 / 3 / 3 | 4, 4, 4, 0 | 14,3 M / 14,5 M / 14,7 M | 4 de 4 |
| tamanho | L-lib+f/lesão | 2 / 2 / 2 | 4, 4, 0, 0 | 103,8 M / 150,3 M / 150,6 M | 0 |
| tamanho | L-lib+f/controlo | 2 / 2 / 2 | (U1, U2 aceitas; T3, T4 não) | 90,8 M / 101,6 M / 102,3 M | 0 |
| unigrama | L-fix | 3 / 3 / 3 | 4, 4, 4, 0 | 268,4 M / 271,6 M / 272,9 M | 0 |
| unigrama | L-lib | 3 / 3 / 3 | 4, 4, 4, 0 | 268,8 M / 271,7 M / 273,3 M | 0 |
| unigrama | L-lib+f | 3 / 3 / 3 | 4, 4, 4, 0 | 27,5 M / 27,6 M / 28,4 M | 4 de 4 |
| unigrama | L-lib+f/lesão | 3 / 3 / 3 | 4, 4, 4, 0 | 99,2 M / 99,3 M / 101,0 M | 0 |
| unigrama | L-lib+f/controlo | 2 / 2 / 2 | (U1, U2 aceitas; T3, T4 não) | 275,7 M / 338,7 M / 341,6 M | 0 |

Observações:

1. **O veredito de cinco condições é verdadeiro nas 8 execuções** (4 sementes × 2 políticas), com as mesmas hipóteses aceitas em todas as sementes (uma hipótese distinta por tarefa e braço; as hipóteses de L-lib+f são sempre `λg p. filtrar@P (celula g) (vizinhos g p)` → abs1, `λg S. juntar (mapear@P>LP (abs1 g) S)` → abs2, e ParAdjacente por `nao (vazia?@P (abs2 g (pretas g)))` (tamanho) ou `algum@P (celula g) (abs2 g (pretas g))` (unigrama)).
2. **A variabilidade entre sementes é pequena** (custo cumulativo até T3 de L-lib+f: 14,3–14,7 M na política de tamanho, 27,5–28,4 M na unigrama; L-fix: 211–261 M e 268–273 M). A razão é estrutural, não um sinal de robustez forte: a busca é uma enumeração determinística por tamanho; a semente altera só as 36 grades da amostra OE, os exemplos iniciais e os contraexemplos. A replicação exclui, portanto, que o resultado do documento 05 dependesse de uma amostra OE ou de uma sequência de contraexemplos particular; **não** diz nada sobre a dependência do currículo, da DSL ou do orçamento, que são os mesmos nas 8 execuções.
3. T4 NenhumaIsolada **nunca** é resolvida (0 de 40 braços), como no documento 05: continua a ser o degrau fora do alcance.
4. A lesão tem efeito diferente por política, de forma consistente: na política de tamanho, sem biblioteca ParAdjacente fica fora do alcance (4/4 falhas); na unigrama, as constantes baratas sobrevivem à lesão (são do aprendiz, não da biblioteca) e ParAdjacente é resolvida a ~99 M, 3,5× o custo de L-lib+f, com o programa bruto de 10 folhas. O controlo de currículo não relacionado falha em ParAdjacente nas 8 execuções.

As hipóteses aceitas nas 8 execuções coincidem sintaticamente com as já verificadas em §1.1 (mesmas cadeias de caracteres), pelo que a verificação exaustiva e amostral de §1.1 se aplica a elas.

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

### 3.2 Resultados **[E]**

`runs/ca-s10002-tamanho` (política de tamanho; 1 122 s de parede, 2 processos; seletor autodirigido na versão 1, cuja escada parava em 16 000 — ver §3.4 para a versão corrigida). Dez braços: 3 seletores × 2 aprendizes, com 3 sementes para o aleatório. Cada braço parou quando o seletor não tinha mais nada a tentar (nenhum esgotou G = 240 000).

| seletor / aprendiz | tarefas aceitas | ordem de aceitação | tentativas (falhas) | repetições após mudança de biblioteca | gasto global (candidatos) | custo total (passos) | custo das falhas | cadeia de reutilização |
|---|---|---|---|---|---|---|---|---|
| autodirigido (v1) / L-lib+f | 5 | pretasColuna1 → vizPretos → semLinha1 → expandir → ParAdjacente | 25 (20) | 19 | 78 905 | **186,7 M** | 158,0 M | expandir←abs2 (=vizPretos), ParAdjacente←abs4 (=expandir) |
| manual / L-lib+f | 5 | vizPretos → expandir → ParAdjacente → pretasColuna1 → semLinha1 | 8 (3) | 2 | 70 162 | 306,2 M | 274,7 M | expandir←abs1, ParAdjacente←abs2 |
| aleatório#1 / L-lib+f | 5 | vizPretos → pretasColuna1 → expandir → semLinha1 → ParAdjacente | 8 (3) | 2 | 70 756 | 289,9 M | 258,3 M | expandir←abs1, ParAdjacente←abs3 |
| aleatório#2 / L-lib+f | 5 | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 12 (7) | 6 | 150 899 | 596,0 M | 567,1 M | expandir←abs3, ParAdjacente←abs4 |
| aleatório#3 / L-lib+f | 5 | vizPretos → expandir → semLinha1 → ParAdjacente → pretasColuna1 | 10 (5) | 4 | 109 823 | 598,5 M | 567,8 M | expandir←abs1, ParAdjacente←abs2 |
| autodirigido (v1) / L-fix | 3 | pretasColuna1 → vizPretos → semLinha1 | 16 (13) | 10 | 96 941 | 327,7 M | 310,7 M | — |
| manual / L-fix | 3 | vizPretos → pretasColuna1 → semLinha1 | 6 (3) | 0 | 64 931 | 357,3 M | 340,3 M | — |
| aleatório#1–3 / L-fix | 3 | (três ordens) | 6 (3) | 0 | 64 931 | 357,3 M | 340,3 M | — |

(Os nomes abs*n* são atribuídos pela ordem de promoção em cada braço; "=vizPretos" indica a solução promovida. NenhumaIsolada não é aceita por nenhum braço.)

Leitura:

1. **A cadeia vizPretos → expandir → ParAdjacente aparece sem ser prescrita** em todos os cinco braços L-lib+f, incluindo o autodirigido e as três ordens aleatórias, sempre com reutilização verificável (abs da solução de vizPretos em expandir; abs da solução de expandir em ParAdjacente). O mecanismo que a faz emergir é a regra de **progresso**: uma tarefa falhada volta a ser elegível quando a biblioteca muda. No aleatório#2, ParAdjacente e expandir falham antes de vizPretos (passos 2–3), expandir é aceita só na repetição após a promoção de vizPretos (passo 9) e ParAdjacente na repetição seguinte (passo 11). Sem a regra de progresso (uma só passagem), as ordens aleatórias #2 e #3 não teriam completado a cadeia. A ordem em si, portanto, não precisa de ser prescrita; o que precisa de existir é a reavaliação das tarefas falhadas depois de uma aquisição, que usa apenas informação interna (versão da biblioteca).
2. **O seletor autodirigido é o mais barato em passos** (186,7 M contra 289,9–598,5 M para os aleatórios e 306,2 M para o manual, com L-lib+f), apesar de fazer o maior número de tentativas (25). A economia vem do aprofundamento iterativo: as tarefas fora do alcance (NenhumaIsolada; e ParAdjacente/expandir antes das aquisições) são sondadas a 2 000–4 000 candidatos (2–9 M por tentativa) em vez de 20 000 (80–140 M). O custo cresce mais do que linearmente com o orçamento (16 000 candidatos custam 65 M; 20 000 custam 84–139 M), por isso várias sondas pequenas custam menos do que uma grande. O manual, com a ordem "certa", gasta 274,7 M só em NenhumaIsolada (três tentativas a 20 000: a inicial e duas repetições após as promoções de pretasColuna1 e semLinha1) — a regra de progresso, que faz emergir a cadeia, também encarece as tarefas sem solução; o aprofundamento iterativo limita esse preço.
3. **A ordem escolhida pelo autodirigido não é "inteligente"**: com todas as tarefas ao mesmo orçamento efetivo, o desempate é por id e o que determina a ordem de aceitação é o custo real (pretasColuna1 e vizPretos cabem em 2 000 candidatos; semLinha1 precisa de 4 000; expandir só cabe em 4 000 com abs2; ParAdjacente só cabe em 4 000 com abs4). O seletor não prevê custos: descobre-os. Um seletor que previsse custo (por exemplo, pelo maior tamanho carregado em tentativas anteriores) é a extensão natural; não foi testado.
4. **Com L-fix nenhum seletor passa de 3 tarefas** (vizPretos, pretasColuna1, semLinha1: as de ≤ 8 folhas): a seleção autodirigida não substitui o mecanismo de aquisição; só muda quanto se gasta a descobrir que uma tarefa está fora do alcance (autodirigido 327,7 M, com 13 falhas baratas, contra 357,3 M com 3 falhas caras).
5. As hipóteses aceitas nos 10 braços foram verificadas com `verificacao.py` (regimes de §1.1): ver `runs/ca-s10002-tamanho/verificacao.json` (resumo em §7).

Política unigrama: `runs/ca-s10002-unigrama` (mesma configuração) — resultados em §3.3.

### 3.3 Política unigrama **[E]**

`runs/ca-s10002-unigrama` (2 927 s de parede, 2 processos; mesma configuração de §3.2, seletor autodirigido na versão 1, ver §3.4).

| seletor / aprendiz | tarefas aceitas | ordem de aceitação | tentativas (falhas) | gasto global | custo total (passos) | cadeia de reutilização |
|---|---|---|---|---|---|---|
| autodirigido (v1) / L-lib+f | 5 | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 23 (18) | 74 013 | **493,5 M** | expandir←abs3 (=vizPretos), ParAdjacente←abs4 (=expandir) |
| manual / L-lib+f | 5 | vizPretos → expandir → ParAdjacente → pretasColuna1 → semLinha1 | 8 (3) | 67 881 | 923,8 M | expandir←abs1, ParAdjacente←abs2 |
| aleatório#1 / L-lib+f | 5 | vizPretos → pretasColuna1 → expandir → semLinha1 → ParAdjacente | 8 (3) | 69 345 | 730,5 M | expandir←abs1, ParAdjacente←abs3 |
| aleatório#2 / L-lib+f | 5 | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 12 (7) | 150 002 | 2 053,2 M | expandir←abs3, ParAdjacente←abs4 |
| aleatório#3 / L-lib+f | 5 | vizPretos → expandir → semLinha1 → ParAdjacente → pretasColuna1 | 10 (5) | 108 611 | 1 546,3 M | expandir←abs1, ParAdjacente←abs2 |
| autodirigido (v1) / L-fix | **3** | pretasColuna1 → semLinha1 → vizPretos | 15 (12) | 92 985 | 1 296,9 M | — |
| manual / L-fix | **5** | vizPretos → expandir → ParAdjacente → pretasColuna1 → semLinha1 | 6 (1) | 35 808 | 730,5 M | — |
| aleatório#1 / L-fix | **5** | vizPretos → pretasColuna1 → expandir → semLinha1 → ParAdjacente | 6 (1) | 42 657 | 840,8 M | — |
| aleatório#2 / L-fix | **3** | pretasColuna1 → semLinha1 → vizPretos | 6 (3) | 62 976 | 1 326,9 M | — |
| aleatório#3 / L-fix | **4** | vizPretos → ParAdjacente → pretasColuna1 → semLinha1 | 6 (2) | 58 354 | 770,4 M | — |

Leitura:

1. Com L-lib+f, o resultado de §3.2 repete-se: a cadeia emerge em todas as cinco ordens, com reutilização verificável; o autodirigido é o mais barato (493,5 M contra 730–2 053 M). Os custos são 2–4× os da política de tamanho porque, na unigrama, as tarefas fora do alcance custam mais por candidato (a busca por custo ponderado carrega termos maiores a orçamento igual).
2. **Com L-fix, a política unigrama torna o resultado dependente da ordem**: o prior de constantes é construído a partir das soluções já aceitas pelo próprio aprendiz, logo é uma aquisição *path-dependent*. Se vizPretos é resolvida primeiro, `filtrar`, `celula` e `vizinhos` ficam baratas e expandir (10 folhas brutas) e ParAdjacente (10) entram no alcance a 20 000 (manual, aleatório#1: 5 tarefas; aleatório#3: 4). Se pretasColuna1 e semLinha1 são resolvidas primeiro, as constantes baratas são `cabeca`, `colunas`, `linhas`, `diferenca` e `vizinhos` continua cara: expandir fica fora do alcance (aleatório#2: 3 tarefas). Isto é o mesmo fenómeno de transferência negativa do prior visto no controlo de currículo não relacionado (documento 05, §4.2), agora como função da ordem. L-lib+f é insensível a isto porque a biblioteca encurta os programas independentemente do prior.
3. **O seletor autodirigido na versão 1 ficou limitado por um erro de desenho**: a escada de orçamentos 2 000 → 4 000 → 8 000 → 16 000 nunca chegava a B_max = 20 000 (o degrau seguinte, 32 000, excedia o limite e a tarefa era abandonada). Na política de tamanho isso não alterou nenhuma aceitação (nenhuma tarefa é resolvida entre 16 000 e 20 000 candidatos), mas na unigrama com L-fix custou 2 tarefas: expandir e ParAdjacente são resolvidas por L-fix a 20 000 (manual) e não a 16 000. O seletor foi corrigido (último degrau exatamente B_max) e só os braços autodirigidos foram reexecutados, nas duas políticas: §3.4. Os braços manual e aleatório não dependem da escada e não foram repetidos.

### 3.4 Seletor autodirigido, versão 2 (escada até B_max) **[E]**

`runs/ca2-s10002-tamanho` (443 s) e `runs/ca2-s10002-unigrama` (1 447 s): só os braços autodirigidos, com a escada 2 000 → 4 000 → 8 000 → 16 000 → **20 000**. Os braços manual e aleatório de §3.2–3.3 são a comparação (não dependem da escada).

| política | aprendiz | tarefas aceitas | ordem de aceitação | tentativas (falhas) | gasto global | custo total (passos) | v1 (§3.2–3.3) | manual | aleatório (3) |
|---|---|---|---|---|---|---|---|---|---|
| tamanho | L-lib+f | 5 | pretasColuna1 → vizPretos → semLinha1 → expandir → ParAdjacente | 26 (21) | 98 906 | **270,3 M** | 186,7 M | 306,2 M | 289,9 / 596,0 / 598,5 M |
| tamanho | L-fix | 3 | pretasColuna1 → vizPretos → semLinha1 | 19 (16) | 156 944 | 668,0 M | 327,7 M | 357,3 M | 357,3 M (×3) |
| unigrama | L-lib+f | 5 | pretasColuna1 → semLinha1 → vizPretos → expandir → ParAdjacente | 24 (19) | 94 014 | **693,9 M** | 493,5 M | 923,8 M | 730,5 / 2 053,2 / 1 546,3 M |
| unigrama | L-fix | **3** | pretasColuna1 → semLinha1 → vizPretos | 18 (15) | 152 988 | 2 495,6 M | 1 296,9 M | 730,5 M (5 tarefas) | 840,8 (5) / 1 326,9 (3) / 770,4 M (4) |

Leitura:

1. **Com L-lib+f a conclusão de §3.2 mantém-se com a escada completa**: a cadeia emerge (mesmas hipóteses e reutilizações) e o autodirigido continua o mais barato nas duas políticas, por uma margem menor (270,3 M contra 289,9–598,5 M; 693,9 M contra 730,5–2 053,2 M). O custo adicional em relação à v1 é inteiramente a última tentativa de NenhumaIsolada a 20 000 (83,7 M e 200,4 M), que falha como em todos os outros braços.
2. **Com L-fix o aprofundamento iterativo é o seletor mais caro** (668,0 M contra 357,3 M; 2 495,6 M contra 730–1 327 M): para uma tarefa sem solução ao alcance, a escada paga 2 000 + 4 000 + 8 000 + 16 000 + 20 000 candidatos em vez de 20 000. A vantagem do autodirigido depende, portanto, de haver aquisições que tornem baratas as tarefas sondadas; sem mecanismo de aquisição, sondar é desperdício.
3. **Na política unigrama, L-fix autodirigido continua a não resolver expandir nem ParAdjacente a 20 000** (372,4 M e 346,8 M gastos em vão), enquanto o manual as resolve à primeira. A diferença é a **seletividade do prior**: no manual, quando expandir é tentada, só as constantes de vizPretos (`filtrar`, `celula`, `vizinhos`) estão baratas; no autodirigido, pretasColuna1 e semLinha1 foram resolvidas antes (cabem em 2 000 candidatos) e `cabeca`, `colunas`, `linhas`, `diferenca` também estão baratas, o que multiplica os candidatos por custo e empurra o programa de 10 folhas para fora do alcance. O prior unigrama é uma aquisição dependente do caminho e **pode piorar com mais aprendizagem**; a biblioteca (L-lib+f) não tem este problema porque atua no tamanho dos programas, não na ordenação dos candidatos. Este é o resultado mais claro deste documento sobre a diferença entre os dois mecanismos.
4. Todas as hipóteses aceitas nos quatro braços foram verificadas (§7.1).


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

### 4.3 Resultados **[E]**

`runs/tr-s10002` (1 198 s de parede, 2 processos). As 29 hipóteses aceitas (18 de L-lib+f, 11 de L-fix) foram verificadas com `verificacao.py`: 14 171 770 entradas exaustivas em n ≤ 4, 14 200 entradas amostrais em n = 5..9 (`teste_ext`) e 1 484 de desenho, **0 erros** (`runs/tr-s10002/verificacao.json`).

Cadeia T1–T3 antes da fotografia: L-lib+f 14,6 M (tamanho) e 28,3 M (unigrama), com abs1 e abs2 como no documento 05; L-fix 207,8 M e 264,0 M (na política de tamanho L-fix não resolve T2 nem T3; na unigrama resolve ambas com programas brutos).

| tarefa | família | tam. ref. E0 / abs | tamanho: L-lib+f | L-fix | razão | unigrama: L-lib+f | L-fix | razão |
|---|---|---|---|---|---|---|---|---|
| expandir2 | F-comp | 21 / 7 | aceita (7, abs2) 7,7 M | falha 115,1 M | 0,07 | aceita (7, abs2) 3,7 M | falha 320,1 M | 0,01 |
| fronteira | F-comp | 14 / 7 | aceita (7, abs2) 7,5 M | falha 112,4 M | 0,07 | aceita (7, abs2) 6,4 M | falha 311,2 M | 0,02 |
| isoladaP | F-comp | 13 / 10 | aceita (10, abs1) 144,0 M | falha 161,5 M | 0,89 | aceita (10, abs1) 53,1 M | aceita (13) 620,8 M | 0,09 |
| duasVizinhas | F-comp | 11 / 8 | aceita (8, abs1) 9,7 M | falha 165,4 M | 0,06 | aceita (9, abs1) 13,0 M | aceita (12) 104,8 M | 0,12 |
| pretasComVizinha | F-comp | 11 / 5 | aceita (5, abs2) 0,09 M | falha 78,4 M | 0,001 | aceita (5, abs2) 0,04 M | aceita (10) 17,4 M | 0,002 |
| TopoCheio | F-neg | 7 / 7 | aceita (7) 3,8 M | aceita (7) 2,1 M | 1,77 | aceita (7) 17,5 M | aceita (7) 13,1 M | 1,33 |
| LinhaOcupada | F-neg | 9 / 9 | aceita (7) 3,8 M | aceita (7) 2,1 M | 1,77 | aceita (7) 8,5 M | aceita (7) 5,7 M | 1,50 |
| pretasUltimaColuna | F-neg | 8 / 8 | aceita (8) 13,8 M | aceita (8) 9,7 M | 1,42 | aceita (8) 95,4 M | aceita (8) 64,0 M | 1,49 |
| semColuna1 | F-neg | 7 / 7 | aceita (7) 7,7 M | aceita (7) 4,5 M | 1,69 | aceita (7) 46,8 M | aceita (7) 33,3 M | 1,40 |

(Entre parênteses: tamanho da hipótese aceita e entrada da biblioteca reutilizada. "Razão" = custo L-lib+f / custo L-fix. Custos em passos do livro-razão, M = 10⁶.)

Hipóteses de L-lib+f em F-comp (idênticas nas duas políticas, exceto duasVizinhas na unigrama, que usa `nao (vazia?@P (cauda@P (abs1 g p)))` com uma folha a mais):

- expandir2: `λg S. abs2 g (abs2 g S)` — composição de abs2 consigo mesma;
- fronteira: `λg S. diferenca (abs2 g S) S`;
- isoladaP: `λg p. e (celula g p) (vazia?@P (abs1 g p))`;
- duasVizinhas: `λg p. nao (vazia?@P (cauda@P (abs1 g p)))`;
- pretasComVizinha: `λg. abs2 g (pretas g)`.

Leitura:

1. **Transferência positiva em todas as 5 tarefas de F-comp, nas duas políticas, sempre com reutilização de abs1 ou abs2**, em composições que não existiam no currículo (abs2∘abs2, abs2 com `diferenca`, abs1 com `cauda`, abs1 com `celula`/`e`). Na política de tamanho L-fix não resolve nenhuma das 5 (todas ≥ 11 folhas em E0, fora do alcance a B = 20 000); na unigrama resolve 3 (as de 10–13 folhas), a custos 8–500× maiores. As hipóteses de L-lib+f coincidem, folha a folha, com os programas de referência "abs" congelados antes da execução (exceto duasVizinhas/unigrama, com uma folha a mais), o que mostra que a busca encontra o **menor** programa com as abstrações e não um programa acidental.
2. **Transferência negativa em todas as 4 tarefas de F-neg, nas duas políticas**: ambos os aprendizes aceitam os mesmos programas (mesmos tamanhos), mas L-lib+f paga 1,42–1,77× (tamanho) e 1,33–1,50× (unigrama). O custo vem da gramática maior (abs1 e abs2 como folhas e, por isso, mais candidatos por tamanho e mais assinaturas OE) e, na unigrama, do prior de constantes: as folhas da cadeia (`filtrar`, `celula`, `vizinhos`, `juntar`, `mapear`, `pretas`, `nao`, `vazia?`) custam 1 e as necessárias (`cabeca`, `colunas`, `linhas`, `reverter`, `diferenca`, `todos`) custam 2. A transferência negativa é moderada (nunca impede a solução) e previsível em magnitude pelo tamanho da gramática; é o preço da biblioteca, e deve ser contabilizado em qualquer afirmação de ganho.
3. isoladaP (10 folhas com abs1) é o caso-limite: na política de tamanho L-lib+f aceita a 144 M, quase o custo de uma falha (razão 0,89), porque o tamanho 10 está no limite do alcance a B = 20 000. A vantagem das abstrações depende do quanto elas encurtam o programa: 21→7 e 14→7 são ganhos de duas ordens de grandeza; 13→10 quase não é ganho.
4. Nada aqui foi ajustado depois de ver os resultados: a família, o hash, a DSL e a biblioteca são os de antes da execução (§4.1).


## 5. Objetivo científico preservado

### 5.1 O que a promoção de funções é, e o que não é **[R]**

A promoção de soluções (L-lib+f) toma a solução aceita de uma tarefa de função, abstrai os argumentos que ela usa e acrescenta o termo resultante à tabela como constante nova. O que o aprendiz adquire é uma **operação** (um programa fechado, reutilizável como folha da gramática) e o que os registros demonstram é **aprendizagem e reutilização de operações**: a operação reduz o tamanho das soluções posteriores (expandir de 12 para 7 folhas; ParAdjacente de 15 para 7) e por isso as traz para dentro do alcance da busca. Nada disto é formação espontânea de conceitos no sentido das camadas L2/L3 do documento 02:

- a **decomposição** do problema em degraus (vizPretos antes de expandir antes de ParAdjacente) foi feita pelo pesquisador; o currículo autodirigido (§3) testa apenas se a **ordem** pode ser escolhida pelo aprendiz, não se os degraus podem ser inventados;
- a operação promovida é exatamente a solução de uma tarefa definida pelo ambiente, com as entradas/saídas escolhidas pelo ambiente; o aprendiz não escolheu *o que* abstrair, só *se* a solução aceita se torna constante (sempre que tem argumentos usados);
- não há mudança de representação: a nova constante é um termo da mesma DSL, com o mesmo tipo-base; a expressividade teórica (L0) não muda (lema de inlining do documento 02) e o que muda é a expressividade efetiva (L1);
- nenhuma das abstrações satisfaz os critérios de L2 do documento 02 (uso fora do domínio de treino com reorganização de inferências, incomensurabilidade com a tabela base): são macros com procedência.

A frase correta para os registros é: *o mecanismo de aquisição e reutilização de operações foi demonstrado funcionalmente em um currículo de quatro degraus com uma semente de dados, e replicado em sementes independentes (§2)*. Qualquer afirmação sobre H-B1 (bootstrapping conceitual), sobre inteligência geral ou sobre o experimento confirmatório continua indevida.

### 5.2 Transição para o experimento sensório-motor **[R]** **[A]**

O documento 02 (§4) e o documento 03 (§D) definiram o experimento sensório-motor como o segundo teste da hipótese, independente da síntese de programas. A síntese de programas não é a arquitetura final: é o primeiro ambiente em que o critério de aquisição-e-reutilização pôde ser tornado mensurável com procedência. O que transita, o que muda e o que fica em aberto:

| transita (invariantes do critério) | muda | em aberto |
|---|---|---|
| critério central: uma estrutura adquirida pelo próprio sistema numa tarefa anterior é usada numa tarefa posterior inédita, com procedência verificável e custo total conciliado | não há DSL nem enumeração por tamanho: a "estrutura adquirida" tem de ser identificada no próprio sistema (por exemplo, um sub-controlador ou um preditor reutilizado), não lida de uma tabela de constantes | como certificar procedência sem termos sintáticos; candidatos: registos de ativação/uso com hash por episódio, lesão da estrutura candidata (como `lesionar()` aqui) |
| controlos obrigatórios: lesão da estrutura adquirida, currículo não relacionado, comparação a custo cumulativo igual com um sistema sem o mecanismo | o custo deixa de ser passos de Sem_n: passa a ser interações com o ambiente (episódios/passos) e computação, registadas separadamente | o equivalente da separação AD/RL/OR/CA (documento 03, §D) tem de ser mantido: aquisição, reutilização, oráculo e controlo em contadores distintos |
| verificação em regimes separados: exaustivo (onde finito) e amostral em condições novas, com partição por instância e sem dados reservados | o "exaustivo" raramente existe; substituir por testes de generalização a distribuições novas de dinâmica/observação, com os mesmos cuidados de degeneração e emparelhamento | definir "tarefa inédita" num mundo contínuo sem a prescrever pela mesma família de geradores |
| seleção autodirigida de tarefas por sinais internos (histórico, custo, progresso) e nunca por informação do oráculo | os sinais de progresso passam a ser erro de predição/recompensa; a legalidade continua a exigir que o seletor não veja as soluções | se a seleção autodirigida acrescenta algo além de aprofundamento iterativo (§3 responde no caso simbólico) |
| transferência estrutural para famílias **congeladas por hash antes dos resultados**, com famílias negativas | as famílias passam a ser tarefas motoras/perceptivas novas definidas por composição de dinâmicas; o hash cobre a definição do ambiente | medir transferência negativa quando não há "tamanho de programa" como proxy de dificuldade |

Pré-requisito para avançar (documento 03, §D, mantido): o experimento sensório-motor só deve ser iniciado com o desenho fatorial viés × dados e os quatro contadores separados já especificados, e com um critério de reutilização que não dependa de inspeção sintática. Este documento não o inicia.

## 6. Demonstrado, falhado, inconclusivo, próximo

### 6.1 Demonstrado **[E]**

1. As 155 hipóteses aceitas em todos os registros deste documento e do documento 05 (25 do experimento mínimo, 29 da transferência, 101 do currículo autodirigido) são corretas em todas as grades com n ≤ 4 (na bateria de argumentos do ambiente) e em todas as grades amostradas em n = 5..9 de uma partição nunca vista: 0 erros em 116,2 milhões de entradas exaustivas, 101,8 mil amostrais e 4,9 mil de desenho (§7.1).
2. O veredito do critério central, agora com cinco condições (reutilização em tarefa inédita, procedência certificada, livro-razão fechado, controlos piores na tarefa posterior à intervenção, mais tarefas que L-fix a custo cumulativo igual), é verdadeiro nas 2 execuções do documento 05 e nas 8 execuções de replicação (4 sementes novas × 2 políticas), com as mesmas hipóteses e variação de custo abaixo de 3 % entre sementes.
3. As operações adquiridas (abs1 ≡ vizinhas pretas de uma posição; abs2 ≡ vizinhas pretas de um conjunto) transferem para **5 tarefas de uma família congelada por hash antes da execução**, em composições inéditas (abs2∘abs2, abs2 com `diferenca`, abs1 com `cauda`, abs1 com `e`/`celula`, abs2 com `pretas`), em ambas as políticas, sempre com reutilização; L-fix não resolve nenhuma (tamanho) ou resolve 3 a custo 8–500× maior (unigrama).
4. A transferência tem um preço mensurável: nas 4 tarefas onde as operações são inúteis, L-lib+f paga 1,33–1,77× o custo de L-fix, sem perder nenhuma solução.
5. A cadeia de aquisições emerge **sem ordem prescrita** quando o ambiente oferece as seis tarefas sem ordem: em todas as cinco ordens testadas (autodirigida, manual e três aleatórias) com L-lib+f, nas duas políticas, usando apenas o histórico de tentativas e a versão da biblioteca; o seletor autodirigido por aprofundamento iterativo (versão 2, escada até B_max) completa-a com o menor custo (270,3 M contra 290–599 M na política de tamanho; 693,9 M contra 730–2 053 M na unigrama).

### 6.2 Falhou **[F]**

1. T4 NenhumaIsolada não é resolvida por nenhum braço em nenhuma execução (0 de 50 tentativas de braço nos registros deste documento, mais as 9 tentativas escalonadas do seletor autodirigido): a composição ∀p ¬isoladaP, com 9 folhas usando abs2 segundo o documento 05, não é encontrada a B = 20 000, nem com o orçamento escalonado até 16 000 candidatos. O documento 05 previa 9 folhas com abs2; isoladaP (10 folhas com abs1) só foi encontrada na transferência a um custo próximo do de uma falha. O alcance efetivo da busca com biblioteca continua a ser ≈ 8–9 folhas a este orçamento.
2. A seleção autodirigida não produz uma ordem informada: o seletor só descobre custos tentando; a sua vantagem é inteiramente devida ao aprofundamento iterativo (sondas baratas), não a uma previsão, e inverte-se sem mecanismo de aquisição (com L-fix é o seletor mais caro: 668 M contra 357 M). A primeira versão da escada não chegava a B_max e foi corrigida e reexecutada (§3.4, §7.3).
3. Na política unigrama, o prior de constantes de L-fix é dependente do caminho e piora com aquisições não relacionadas: L-fix resolve expandir e ParAdjacente na ordem manual e falha-as, a orçamento igual, depois de resolver pretasColuna1 e semLinha1 primeiro (§3.3–3.4).
4. A replicação não mede robustez a mudanças do currículo, da DSL ou do orçamento: a variabilidade entre sementes é pequena porque a busca é determinística; o teste sensível (famílias congeladas) só foi feito com uma semente.

### 6.3 Inconclusivo **[A]**

1. Se a transferência positiva sobrevive a famílias definidas por **outro** autor: as famílias F-comp foram escritas pelo mesmo investigador que desenhou o currículo, com a DSL em mente (composições curtas das operações adquiridas). O congelamento por hash impede ajustes posteriores, mas não a escolha prévia de tarefas favoráveis. Uma família escrita sem conhecer abs1/abs2 seria um teste mais forte.
2. Quanto da transferência negativa é da gramática maior e quanto é do prior unigrama: as duas políticas mostram razões semelhantes (1,4–1,8 e 1,3–1,5), o que sugere que a gramática domina, mas não foi feita a ablação (biblioteca presente, prior desligado).
3. Se um seletor com previsão de custo (pelo maior tamanho carregado ou pelo número de contraexemplos) escolheria uma ordem melhor do que o aprofundamento iterativo cego, e a que custo de sondagem.
4. Se a aquisição funciona quando as tarefas de função do currículo não são **exatamente** as sub-operações necessárias (aqui, vizPretos e expandir são as peças de ParAdjacente por construção): o teste com peças "aproximadas" (por exemplo, uma tarefa cuja solução contém a operação útil como subtermo, sem ser ela) não foi feito.
5. A verificação de funções continua limitada à bateria finita de argumentos do ambiente (listas derivadas da grade).

### 6.4 Próximo experimento mais informativo **[R]**

O ponto mais fraco da evidência é o item 1 de §6.3: as famílias de transferência foram desenhadas por quem conhecia as abstrações. O experimento mais informativo, e pequeno, é uma **família cega**: tarefas definidas a partir de uma descrição em linguagem natural das operações disponíveis na DSL base (sem mencionar vizPretos, expandir ou ParAdjacente), escritas antes de ler os documentos 05 e 06, congeladas por hash e avaliadas com o mesmo protocolo de §4.2 (fotografia após a cadeia; L-lib+f vs L-fix; duas políticas; uma semente nova do intervalo exploratório). Se metade ou mais das tarefas cegas que envolvem vizinhança mostrarem reutilização de abs1/abs2 com razão de custo < 0,5, a transferência estrutural deixa de depender da escolha do investigador; se nenhuma mostrar, o resultado de §4 é um artefacto de desenho. Custo estimado: ≈ 20 min de CPU por semente a B = 20 000. Em paralelo, e ainda mais barato (≈ 5 min), a ablação de §6.3.2 (biblioteca com prior desligado) separa as duas fontes de transferência negativa. Só depois destes dois resultados faz sentido o desenho do experimento sensório-motor (§5.2) e, mais tarde, o confirmatório — que continua por executar.

## 7. Comandos, registros e desvios

### 7.1 Registros produzidos neste documento

| registro | conteúdo | parede |
|---|---|---|
| `runs/em-s10002-{tamanho,unigrama}/verificacao.json` | verificação exaustiva e amostral das 25 hipóteses do documento 05 (§1.1); `analise_v2` em `deterministico.json` com o veredito de cinco condições (§1.2) | — |
| `runs/rep-1/` | replicação: 8 subpastas `s<semente>-<política>` com os registros completos do experimento mínimo; `resumo.json`, `resumo.md` (§2) | 3 934 s |
| `runs/tr-s10002/` | transferência estrutural: cadeia + 9 tarefas × 2 aprendizes × 2 políticas; `verificacao.json` (§4) | 1 198 s |
| `runs/ca-s10002-tamanho/` | currículo autodirigido, política de tamanho: 10 braços; `verificacao.json` (§3.2) | 1 122 s |
| `runs/ca-s10002-unigrama/` | currículo autodirigido, política unigrama: 10 braços; `verificacao.json` (§3.3) | 2 927 s |
| `runs/ca2-s10002-{tamanho,unigrama}/` | seletor autodirigido versão 2 (escada até B_max), 2 braços cada; `verificacao.json` (§3.4) | 443 s, 1 447 s |

Verificação das hipóteses dos registros novos (regimes de §1.1):

| registro | hipóteses aceitas | entradas exaustivas | erros | amostrais (natural) | erros | desenho | erros |
|---|---|---|---|---|---|---|---|
| `tr-s10002` | 29 | 14 171 770 | 0 | 14 200 | 0 | 1 484 | 0 |
| `ca-s10002-tamanho` | 40 | 34 260 230 | 0 | 29 000 | 0 | 775 | 0 |
| `ca-s10002-unigrama` | 45 | 36 173 748 | 0 | 31 200 | 0 | 1 240 | 0 |
| `ca2-s10002-tamanho` | 8 | 6 852 046 | 0 | 5 800 | 0 | 155 | 0 |
| `ca2-s10002-unigrama` | 8 | 6 852 046 | 0 | 5 800 | 0 | 155 | 0 |
| **total (com §1.1)** | **155** | **116 166 082** | **0** | **101 800** | **0** | **4 894** | **0** |

Todos os registros têm `hashes.json`/`fontes` com o hash das fontes do pacote no momento da execução, contadores determinísticos separados das medições de tempo e memória, e os certificados de procedência das entradas de biblioteca. Semente de dados única nos registros de transferência e currículo: 10002 (a do documento 05, para comparação direta); sementes da replicação: 10003–10006. Sementes exploratórias usadas até agora: 10001–10006. Buckets 50–99: intocados.

### 7.2 Comandos

```bash
python3 -m unittest discover -s fedro_piloto/tests -v        # 243 testes, ≈ 8 min
python3 -m fedro_piloto.verificacao --run runs/<id>            # verificacao.json (regimes de §1.1)
python3 -m fedro_piloto.replicacao --id rep-1 --sementes 10003,10004,10005,10006 --politicas tamanho,unigrama --B 20000 --processos 4
python3 -m fedro_piloto.curriculo_autodirigido --id ca-s10002-tamanho --semente 10002 --G 240000 --B-max 20000 --politica tamanho --seletores autodirigido,aleatorio,manual --aprendizes L-lib+f,L-fix --sementes-aleatorio 1,2,3 --processos 2
python3 -m fedro_piloto.transferencia --id tr-s10002 --semente 10002 --B 20000 --politicas tamanho,unigrama --processos 2
python3 -m fedro_piloto.familias_transferencia                 # hash da especificação, tamanhos, verificação das referências DSL
```

Re-análise dos registros do documento 05 com o veredito novo (gravada como `analise_v2`):

```bash
python3 -c "import json,io; from fedro_piloto import experimento_minimo as EM
for r in ('em-s10002-tamanho','em-s10002-unigrama'):
    d=json.load(io.open(f'runs/{r}/deterministico.json',encoding='utf-8'))
    print(r, EM.analisar({k:{'deterministico':v} for k,v in d['bracos'].items()}, EM.ConfigEM())['criterio_central']['veredito'])"
```

### 7.3 Desvios e incidentes

1. O programa de referência na DSL para LinhaOcupada foi corrigido **antes** do congelamento da família (§4.1); o hash anterior (`f0085ade…`) nunca foi usado numa execução de avaliação.
2. A primeira execução do currículo autodirigido abortou porque a semente do seletor aleatório passava pela guarda de sementes de dados (`rng_derivado` exige o intervalo do piloto). A semente do seletor passou a ser própria (`random.Random("curriculo|<seletor>|<semente>")`), separada das sementes de dados; a execução foi relançada do zero e a falha de um braço passou a ser registada em vez de derrubar o Pool. Nenhum resultado da execução abortada foi usado.
3. A condição 4 do veredito foi corrigida depois de se ter observado que a sua primeira versão avaliava tarefas anteriores à intervenção de controlo (§1.2). A correção é de aplicabilidade, não de limiar, e está registada aqui para que não seja confundida com um ajuste a posteriori do critério: a versão anterior dava veredito falso por artefacto; a atual exige os mesmos controlos, na tarefa certa.
4. As execuções de replicação, currículo e transferência correram em paralelo na mesma máquina (4 núcleos); os tempos de parede não são comparáveis entre registros, e só os contadores determinísticos devem ser usados em comparações.
5. A política unigrama do currículo autodirigido (§3.3) foi executada por completude; o seu custo (≈ 50 min de parede) é o maior gasto adicional deste documento. Nenhum orçamento por tarefa foi aumentado além do B = 20 000 do documento 05.
6. A primeira versão da escada do seletor autodirigido (2 000 → 16 000) não chegava a B_max; ao ler os resultados da política unigrama (§3.3) ficou claro que isso o fazia tentar menos do que os outros seletores. A escada foi corrigida (último degrau = B_max) e só os braços autodirigidos foram reexecutados em registros novos (`ca2-*`, §3.4); os registros `ca-*` ficam como estão, com a versão 1 identificada. A correção foi feita depois de ver resultados, e por isso está declarada aqui: ela não altera nenhuma conclusão a favor do seletor (torna-o mais caro) e corrige uma desvantagem injusta.
