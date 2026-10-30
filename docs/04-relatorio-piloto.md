# Relatório do piloto — Experimento 1

## Documento 04 — Execução exploratória `piloto-s10001-exploratorio-v2`

**Status:** v0.2 (2026-10-30). A v0.1 foi corrigida por uma revisão crítica adversarial; os achados estão na seção 6.4. Relatório de uma execução exploratória em escala reduzida do piloto descrito em `docs/03-plano-piloto.md`. Não contém alegação científica (documento 03, seção 0, regra 1).

**Fontes.** Todo número deste documento vem de um destes arquivos:

- `runs/piloto-s10001-exploratorio-v2/` — `config.json`, `deterministico.json`, `medicoes.json`, `razao.json`, `abstracoes.json`, `hashes.json`, `relatorio.md`, `medicoes.md`, `comandos.txt`;
- `runs/piloto-s10001-exploratorio-v2-pm15/pm15.json` — comparação de determinismo (PM15);
- a saída da suíte de testes (seção 1.2), executada sobre o mesmo código.

Exceções: os números das seções 2.2 e 6.3 sem **[nota]** são declarações dos módulos e não estão em nenhum arquivo de registro. O tempo da suíte de testes (seção 1.2) vem de uma saída que não foi arquivada em `runs/`. As reconstruções da revisão crítica (seção 6.4) dão o comando que as reproduz.

Os números da seção 2.2 são **declarações dos módulos de implementação** (relatórios de retorno de cada módulo), não medições desta execução. Quando contradizem os registros de `runs/piloto-s10001-exploratorio-v2`, valem os registros, e a contradição é anotada.

**Código.** SHA-256 das fontes de `fedro_piloto/` = `9d0e41dedebb9e59edcb6111a306d170434ad06cea5d74c1ad98502810edd7a4` (Python 3.13.17), em `config.json → fontes`. Conferi os 17 hashes por arquivo contra os arquivos atuais e todos coincidem. Os registros antigos `runs/piloto-s10001-exploratorio`, `-parcial-1` e `-parcial-2` não foram alterados e não são usados aqui.

**Comandos** (`comandos.txt`):

```
python3 -m fedro_piloto.piloto --id piloto-s10001-exploratorio-v2 --semente 10001 --processos 4
python3 -m fedro_piloto.piloto --id piloto-s10001-exploratorio-v2-pm15 --semente 10001 --processos 4 \
    --fases 1,2,4,5,6,7 --reaproveitar runs/piloto-s10001-exploratorio-v2 --comparar-com runs/piloto-s10001-exploratorio-v2
python3 -m unittest discover -s fedro_piloto/tests -v
```

Na primeira execução as fases 1 a 7 foram todas calculadas, sem reaproveitamento (`deterministico.json → reaproveitamento` = ausente). Na execução PM15 a fase 3 foi reaproveitada, com verificação do hash das fontes.

**Rótulos epistêmicos** (documento 03): [P] prova formal; [E] evidência empírica (medição física: tempo, memória); [C] resultado computacional determinístico; [F] interpretação; [H] hipótese ou extrapolação; [R] condição de refutação ou interrupção; [A] questão aberta.

---

## 0. Resumo factual

- Execução com semente 10001, escala `exploratoria-reduzida`, 4 processos, iniciada em 2026-10-29T23:00:07. Tempo de parede somado das fases: 2 944,7 s. CPU somada (processo + filhos): 8 249,7 s. [E]
- PM1: 0 discordâncias entre `ref_a` e `ref_b` em 35 conceitos (2 312 310 avaliações exaustivas em n de 1 a 4; 52 500 amostras em n de 5 a 9). [C]
- PM2 a PM5: 28 células (conceito, n) não degeneradas, todas com aceitação 1,000, PM4 = 1,000 e M10 = 0,500. ExistePreta é degenerado nas 4 células medidas. [C]
- PM6: 256 comparações com a auditoria, 0 fora de 3 DP. [C]
- PM8: s_reach(10⁴) entre 6 e 11, conforme base e contexto. s_reach(10⁵) = 9 em E0 e E0+ `{g} → Bool` e 10 em E0' `{g} → Bool`. s_reach(10⁶) não foi medido. [C]
- PM9: vazão do enumerador entre 56 e 2 899 candidatos/s, mediana 423. 83 das 84 medições ficam abaixo de 2 000/s, e 21 ficam abaixo de 200/s (I6). [E]
- PM10, em E0: 6 de 14 degraus alcançáveis a B = 10⁴; em E0+, 6 de 14. Cada degrau é avaliado com os degraus anteriores (manuais) como constantes. Três dos 6 de E0 (`componenteDe`, `noMaximo`, `mesmoNumero`) dependem de degraus inalcançáveis (`fecho`, `descartar`). Contando só cadeias de degraus alcançáveis, ficam 3 de 14 em E0 e 3 de 14 em E0+ (seção 3.4). [C]
- PM11: 1 de 3 alvos extraído pela compressão gulosa (`passo`), em modo `mecanismo-teste`, sobre programas manuais. As 2 ocorrências de `passo` vêm de um único programa manual (`fecho`, com `passo` expandido), não de tarefas distintas. Os registros marcam I4 como disparada sem a revisão do compressor que o documento 03, §9, exige antes (seção 7, item 7). [C]
- PM12 = 50/50. PM13: latência máxima de 0,360 s. PM14 = 0. PM15: idêntico nas fases 1, 2, 4, 5, 6 e 7. [C]/[E]
- PM16: 7 399 h de CPU projetadas, contra um limiar de 2 000 h. [E]/[H]
- Execução autônoma: 5 braços. Cada um aceitou 3 das 14 tarefas (ExistePreta, vizPretos, pretasDe), todas com acurácia de teste 1,000. Para ExistePreta essa acurácia não informa nada: o conjunto de teste tem 29 positivos e nenhum negativo, e o predicado constante `verdadeiro` também acertaria 29/29 (seção 6.4, item 1). As outras 11 terminaram por `orcamento_enumeracao`. Houve 1 abstração com proveniência `descoberta` em L-lib@E0 e em L-lib@E0+, e 2 promovidas na variante L-lib+f@E0. Todas são cópias (α/η) de soluções já aceitas, e nenhuma foi reutilizada. [C]
- Decisão: **NO-GO a B = 10⁴**. A regra usada é a do documento 03, §10, com B = 10⁴ no lugar de B_max = 10⁶ (que não foi medido), mais uma exigência autônoma que não está no §10. Só pela tabela PM10 a 10⁴ o resultado já é NO-GO. A decisão conservadora e a decisão com a variante L-lib+f também dão NO-GO. A regra literal, a 10⁶, não foi aplicada (seção 7). O piloto também não atinge os critérios de aceitação do §10. [C]/[H]
- Suíte de testes: 215 testes executados em 481,6 s; 215 passam, 0 falham, 0 erros, 0 pulados (seção 1.2). A saída não foi arquivada em `runs/`. A contagem de 215 métodos `test_` confere por inspeção do código.

---

## 1. O que foi implementado

### 1.1 Módulos

Contagem de linhas por `wc -l`, sobre o código com hash `9d0e41de…` (o mesmo da execução).

| módulo | linhas | responsabilidade (documento 03, seção 3) |
|---|---|---|
| `grade.py` | 139 | Grade, Pos, serialização, hash, vizinhança, transformações, partição por balde |
| `referencias.py` | 252 | `ref_a` (busca em largura) e `ref_b` (união-busca) para os 35 conceitos do REGISTRO |
| `geradores.py` | 1 149 | amostragem natural, geradores construtivos, negativos emparelhados, quase-acerto, M10, degeneração |
| `dsl.py` | 1 002 | tipos, termos, tabelas E0, E0', E0+ e E0'+ (curadas e sistemáticas), tamanho, impressão, proveniência |
| `avaliador.py` | 375 | Sem_n com contagem de passos, combustível, truncamento e valores padrão |
| `tradutores.py` | 353 | τ e τ', inline, β segura |
| `enumerador.py` | 1 273 | enumeração por tamanho e tipo, poda OE, contagem N(s, τ), s_reach |
| `biblioteca.py` | 857 | fragmentos, anti-unificação, pontuação, compressão gulosa, modos `mecanismo-teste` e `autonomo` |
| `oraculo.py` | 487 | rótulo, contraexemplo mínimo, reservatório, busca local, registro de consultas |
| `aprendizes.py` | 920 | L-fix e L-lib (L-mem não foi implementado), laço dialético |
| `razao.py` | 323 | livro-razão com diário, fechamento e conciliação |
| `certificados.py` | 111 | certificado de proveniência das soluções do laço do aprendiz |
| `medidas.py` | 77 | medições reais (tempo de parede, CPU, memória), separadas dos contadores |
| `programas_referencia.py` | 162 | programas manuais da escada (`manual-teste`) e `DISCREPANCIAS_DOC` |
| `adaptadores.py` | 356 | portadores sequência e grafo (U18) |
| `piloto.py` | 1 906 | orquestração das fases 1 a 7, relatórios, PM15, separação do confirmatório |
| `__init__.py` | 1 | — |
| **total sem testes** | **9 743** | documento 03: indicativo de 2 500 a 3 500 |
| `tests/` (15 arquivos) | 3 418 | U1 a U27 e testes de achados de revisão (`test_achados.py`) |

### 1.2 Testes

Comando: `cd /home/user/Fedro && python3 -m unittest discover -s fedro_piloto/tests -v`

Execução em 2026-10-30, sobre o código com hash `9d0e41de…`. Resumo da saída real (últimas linhas, sem cortes):

```
----------------------------------------------------------------------
Ran 215 tests in 481.552s

OK
```

| arquivo | testes | arquivo | testes |
|---|---|---|---|
| test_achados.py | 17 | test_geradores.py | 24 |
| test_adaptadores.py | 13 | test_grade.py | 9 |
| test_aprendizes.py | 15 | test_oraculo.py | 16 |
| test_avaliador.py | 14 | test_piloto.py | 9 |
| test_biblioteca.py | 19 | test_programas_referencia.py | 7 |
| test_dsl.py | 21 | test_razao.py | 7 |
| test_enumerador.py | 24 | test_referencias.py | 10 |
| | | test_tradutores.py | 10 |

**Passam: 215. Falham: 0. Erros: 0. Pulados: 0.** [C]

Os testes cobrem U1 a U27 com as reduções de escala listadas na seção 2.2 (itens 1 e 2). U3 usa 10⁴ amostras por n, não 10⁵. U26 é coberto pelo teste de determinismo de `test_piloto.py` e, na execução real, por PM15. O teste `test_desvio_tau_inv_dobra_ingenua` documenta D1 (seção 2.2, item 15).

---

## 2. Desvios em relação aos documentos 02 e 03

### 2.1 Desvios registrados pela própria execução (`deterministico.json → desvios`)

1. **Escala reduzida.** PM1 com 300 amostras por n de 5 a 9 (documento: 10⁵). PM2 a PM5 com até 100 pares (documento: ≥ 1 000). PM6 com Monte Carlo de 1 000 amostras em n = 5 e 6. s_reach medido até B = 10⁵ só nos 4 pares de `config.json → alcance_completos` (documento: até 10⁶); os demais, até 10⁴. Execução autônoma com B_tarefa = 10⁴ (documento: B_max = 10⁶), sem L-mem e sem controles.
2. **B único.** O B_max da regra de decisão (10⁶) foi substituído por um B único = 10⁴ (`alcance_B_unico`), medido em todos os contextos, tabelas e profundidades da tabela PM10. A decisão é tomada a 10⁴. Um NO-GO por alcance a 10⁴ não implica NO-GO a 10⁶.
3. **Memória.** Cada trabalhador roda com RLIMIT_AS = 4 GB (`memoria_trabalhador_gb`), num processo novo por job. Um `MemoryError` deixa o resultado inconclusivo e é registrado em `medicoes.json` (bloco `dependente_de_recurso`). Nesta execução isso ocorreu uma vez: E0 `{g, S: L Pos} → L Pos` a 10⁵ parou após 52 726 candidatos.
4. **Curadoria da tabela de primitivas.** As instâncias monomórficas de `dsl.INSTANCIAS` foram escolhidas a partir dos programas da escada. O documento 02, 2.3.2, define primitivas polimórficas. A curadoria foi mantida nos braços da fase 6. O seu efeito foi medido com `dsl.BASES_SISTEMATICAS` (critério fixado sem olhar a escada) em E0 e E0+ (colunas "sistemática" da seção 3.4).
5. **Profundidade λ.** Com D = 2, os programas de E0' e E0'+ (profundidade de 3 a 6) ficam fora da gramática. A tabela PM10 mede s_reach com D = max(2, profundidade do programa). Os aprendizes continuam com D = 2.
6. **PM10 com s_reach da tabela base é otimista.** A coluna "c/ ant. na tabela" mede s_reach com os degraus anteriores (manuais, em modo auditoria) acrescentados à tabela. A decisão principal segue a regra literal; a decisão "conservadora" usa o menor s_reach medido.
7. E0'+ só tem s_reach a 10⁴.
8. **Livro-razão.** `busca_candidatos` conta só candidatos no sentido do protocolo (documento 03, 2.3). Os candidatos internos do enumerador vão para `enumeracao_candidatos` e `enumeracao_passos`. B_tarefa limita os dois separadamente. A comparação a custo igual usa `total_aprendiz`.
9. **Poda OE.** Os mundos da busca são a amostra fixa mais as grades dos exemplos e contraexemplos recebidos (refinamento com re-enumeração). A incompletude residual é medida pela auditoria OE (seção 3.3).
10. **Oráculos.** Uma hipótese indefinida (orçamento de passos esgotado) numa entrada conta como discordância.

### 2.2 Desvios declarados pelos módulos

Itens transcritos dos relatórios de implementação de cada módulo. Os números destes itens vêm de testes e medições dos módulos, não desta execução, salvo indicação. Uma **[nota]** marca onde os registros v2 os corrigem ou atualizam.

**Referências e geradores**

1. U3 usa 10⁴ amostras naturais por n de 5 a 9, em vez das 10⁵ do documento 03, mais um complemento construtivo (positivos e negativos emparelhados de cada conceito) para cobrir conceitos raros. O motivo é a suíte rodar em minutos. U2 continua exaustivo para n de 1 a 4 em todos os 35 conceitos do REGISTRO, sem nenhuma discordância entre `ref_a` e `ref_b`.
2. Reduções de U7 a U10 e de PM3, conforme o campo testes. U6 manteve as 10⁵ amostras. O valor exato é 1810/65536 = 0,02762, conferido também pela contagem exaustiva de 1 810 positivos em n = 4.
3. Correção mínima em `referencias.py`, só de desempenho e sem efeito sobre os rótulos: `componentes_a` e `componentes_b` ganharam `lru_cache` por grade, cada um com o seu próprio cache. `ref_a` continua a depender só da busca em largura, e `ref_b` só da união-busca. As duas passaram a devolver tuplas, e não listas, para que o valor em cache seja imutável. Com isso a avaliação exaustiva de n = 4 caiu de cerca de 50 s para cerca de 18 s, e a de n = 9 de 3,3 ms para 1 ms por grade.
4. **[P] Matematicamente impossível no protocolo.** O emparelhamento em densidade (02, 2.2.3) e o limiar M10 ≤ 0,55 (03, PQ2/PM5) não valem para ExistePreta em nenhum n. O único negativo é a grade vazia, que tem 0 pretas, e nenhum positivo tem 0 pretas. Logo não existe negativo emparelhado, e qualquer conjunto com os dois rótulos tem M10 = 1. O código detecta isso: `degenerado()` devolve `negativos_emparelhados_possiveis=False` e `conjunto_de_desenho` levanta `ConceitoDegenerado`. Correção proposta: ExistePreta fica fora de PQ2/PM5 como degrau do currículo, com M10 = 1 reportado e declarado, ou o pré-registro define outro desenho de negativos para ele. **[nota]** Confirmado na v2: as 4 células de ExistePreta (n de 3 a 6) estão marcadas como degeneradas.
5. **[P] Limitação lógica de M10.** Quando os pares são perfeitamente emparelhados (PM4 = 1), as densidades de positivos e negativos formam o mesmo multiconjunto, e M10 = 0,5 exatamente, por construção. M10 ≤ 0,55 só informa alguma coisa quando o emparelhamento falha, ou em conjuntos não emparelhados. O teste `test_m10_detecta_confundidor` confirma que um conjunto balanceado por rejeição natural (UmComponente, n = 6) dá M10 > 0,55. O critério que de fato prende é PM4 = 1,0. **[nota]** Na v2, as 28 células não degeneradas têm M10 = 0,500 e PM4 = 1,000.
6. "Metade dos negativos por permutação e metade por troca" (02, 2.2.3) nem sempre é atingível. Para conceitos cujos negativos são raros na densidade do positivo, uma permutação aleatória quase nunca dá negativo: em PeloMenosDois com n = 9, 1 em 100. O código alterna os dois métodos, recorre ao outro quando um falha e registra a contagem real em `metadados['metodos']` (`deterministico.json → fases.1.pm2_pm5[*].metodos` e `relatorio.md`, fase 1; a tabela da seção 3.1 não tem essa coluna).
7. Partição por instância (correção 2) aplicada por `PARTICOES` sobre `Grade.balde(100)`. Consequência que precisa de decisão: para n ≤ 4, o contraexemplo "mínimo" passa a ser o mínimo dentro da partição (`oraculo_treino`), não no domínio inteiro. O quase-acerto exato de n ≤ 4 (U9) e a força bruta usam essa definição.
8. Os documentos (2.7.1) fazem as regiões de F3 serem disjuntas. Isso só vale para n ≥ 2: em n = 1, linha1 = linhaN e col1 = colN, e as duas metades são vazias. Os 11 conceitos de F3 são constantemente verdadeiros em n = 1, o que `degenerado()` detecta. Não há gerador construtivo para regiões sobrepostas; em n = 1 usa-se rejeição natural verificada.
9. U9: para n ≤ 4, a busca de quase-acerto é exata e mais forte que a pedida (trocas simples e depois duplas aleatórias). Ela escolhe o alvo de menor distância em trocas (Hamming/2) dentro da partição, usando a tabela exaustiva de rótulos, e ordena as trocas de modo que a penúltima grade mantenha o rótulo original. Para n ≥ 5 vale o esquema pedido: nível 1 com todas as trocas simples em ordem aleatória; nível 2 com trocas duplas, exaustivas se forem poucas e amostradas (L tentativas) caso contrário; nível 3 com busca local. Só os níveis 1 e 2 garantem o mínimo.
10. Heurística acrescentada em `conjunto_de_desenho` para n ≥ 5: um número de pretas k que falhou pelo menos 2 vezes, com taxa de sucesso abaixo de 20 %, deixa de ser tentado. Isso restringe os positivos às densidades em que existem negativos emparelhados alcançáveis e enviesa a distribuição de densidade dos positivos. O efeito fica registrado em `metadados['pretas_puladas']`. Para n ≤ 4, a restrição é exata (`capacidade_particao`). **[nota]** Na v2 houve pretas puladas em ParAdjacente n = 5 (k de 8 a 19) e n = 6 (k de 13 a 29), UmComponente n = 5 e 6 (k = 1) e TodosMesmoTamanho n = 5 (k = 1 e 2) (`deterministico.json → fases.1.pm2_pm5[*].pretas_puladas`).
11. Geradores construtivos com modos "perto da fronteira", além do esquema básico de 02, 2.2.3, porque sem eles o emparelhamento era inviável em n = 9: ExisteCompReto dava só 14 pares em 4 000 tentativas. Os modos acrescentados são: ParAdjacente esparso (conjunto independente mais um par adjacente); NumComp com sementes à distância 2; ExisteComp tocaBorda/contemCanto com ruído fora da borda ou dos cantos; ExisteComp reto/min3 com componentes de fundo que violam P mais um único componente pequeno que satisfaz P; MaiorCompPeloMenosLinha1 com o maior componente exatamente igual à contagem da linha 1; e PeloMenosDois concentrado em m = 2. Todos são verificados por `ref_a` e `ref_b` e publicados no código.
12. PM2 (taxa de aceitação) é interpretada como aceitas pelas referências sobre construídas dentro da partição. As rejeições por balde fora da partição são contadas à parte, em `rejeitadas_particao` e `taxa_particao`. **[nota]** Na v2, `taxa_particao` varia de 0,123 a 0,570 nas 28 células não degeneradas (o relatório do módulo dizia cerca de 80 % de rejeição).
13. U5: os valores de borda não estavam definidos no pré-registro e foram fixados no teste a partir do código existente. TodosComp*, TodosMesmoTamanho e MaiorTocaBorda exigem pelo menos um componente. NoMaximoDois, NumCompIgual*, MaiorCompPeloMenosLinha1 e as comparações de cardinalidade são verdadeiros na grade vazia. ColunaDoisVazia é falso em n = 1.
14. Assinaturas: `degenerado` e `conjunto_de_desenho` recebem o objeto `Conceito`, não o nome. `negativo_emparelhado` recebe a partição como 4º argumento obrigatório, `(g, conceito, rng, particao, metodo='auto', ...)`, e devolve `(grade, num_trocas, metodo)` ou `None`. `conjunto_de_desenho` devolve `ConjuntoDesenho`, iterável sobre `(grade, rotulo)`, em vez de uma lista simples.

**Linguagem, avaliador e tradutores**

15. **D1 [P] — erro matemático no documento 02, 2.3.4.** Com `fix f = f^{F(n)}(padrao)`, a tradução óbvia de `dobraR` (`λf z L. fix (λrec l. se (vazia? l) z (f (cabeca l) (rec (cauda l)))) L`) usa m + 1 níveis de fix para uma lista de comprimento m. Quando |L| = F(n) (por exemplo `posicoes` em n = 1, ou listas construídas com `cons`/`concatenar`), ela devolve `padrao(b)` em vez de z. Logo, a afirmação de que as duas definições coincidem em todo o domínio, inclusive nos casos de truncamento, é falsa para essa tradução. Correção: τ'(`dobraR`) verifica se a cauda é vazia antes de recursar (`se (vazia? (cauda l)) z (rec (cauda l))`), e assim uma lista de comprimento m usa só m níveis, o que é exato para m ≤ F(n). Um teste mostra a versão ingênua falhando e a corrigida passando. Custo: |τ'(`dobraR`)| = 20, não 15.
16. **D2 — constantes.** c = 22, calculado a partir de `diferenca` (`linhas`/`colunas` valem 15, não cerca de 35), e c' = 20, a partir de τ'(`dobraR`) (o documento dá 15). Vale com `linhaDe`/`colunaDe : Grade → Pos → L Pos`, isto é, recebendo o argumento grade, como `vizinhos`.
17. **D3 — tamanho (documento 02, 2.8.1).** `mesmoNumero = λA B. e (noMaximo A B) (noMaximo B A)` tem tamanho 9 (7 folhas + 2 abstrações), não 7. O programa não foi alterado. Fica registrado em `programas_referencia.DISCREPANCIAS_DOC` e é verificado por teste. **[nota]** PM10 da v2 usa 9.
18. **D4 — tamanhos brutos.** ParAdjacente e NenhumaIsolada têm 13 brutos com β (17 só com substituição), não 15. O `passo` bruto = 14 coincide com o documento. Tamanhos brutos aproximados do documento, recalculados por inline com β segura: `fecho` 34 (documento: cerca de 38), `componenteDe` 38 (cerca de 44), UmComponente 50 (cerca de 60), `noMaximo` 18 (cerca de 18), `mesmoNumero` 35 (cerca de 35), PrimeiraUltimaIguais 49 (cerca de 45), LinhasIguais 51 (cerca de 45). Todos os tamanhos com biblioteca, exceto `mesmoNumero`, coincidem com o documento: 5, 8, 10, 10, 9, 16, 7, 17, 6, 13, 6, 13, 14.
19. **D5 — semântica.** O programa NenhumaIsolada do documento (`todos … (pretas g)`) devolve verdadeiro na grade sem pretas. `referencias.NenhumaIsolada` exige pelo menos um componente e devolve falso ali. Os dois discordam exatamente nas grades sem pretas, em todo n testado. O programa do documento foi mantido, e uma variante corrigida (tamanho 15 com a biblioteca) é fornecida como `NENHUMA_ISOLADA_CORRIGIDA`, que concorda em todo o domínio. O pré-registro deve escolher uma das duas. **[nota]** Na v2, a verificação dos programas manuais registra 1 discordância documentada em E0 e em E0+ e 3 em E0'+; a variante corrigida tem 0 em todas as bases.
20. **D6 — E0'.** O documento diz que `fecho` em E0' fica em torno de 16. Mas `diferenca` não é primitiva de E0', e por isso beta_segura(τ(`fecho`)) = 33. Uma versão E0' escrita à mão, que detecta "nada novo" comparando comprimentos via `dobraR`, tem tamanho 20. Os demais degraus de E0' (beta_segura(τ(E0))) são limites superiores, longe de E0: `vizPretos` 17, ParAdjacente/NenhumaIsolada 14, `passo` 39, UmComponente 28, `pretasDe` 15, PrimeiraUltimaIguais 46, LinhasIguais 42. `descartar` fica em 9, como no documento; em E0+/E0'+, `fecho` 4 e `descartar` 9, como no documento.
21. **D7 — documento 02, 2.0 ("custo de avaliação não muda" sob inlining).** Com este modelo de passos (nós mais aplicações saturadas), o inlining muda a contagem. Substituição pura difere em O(k) passos; a β-redução segura corta até cerca de 20 % (UmComponente numa grade 4×4: 8 639 passos contra 7 752). A denotação é preservada, a contagem exata não.
22. **D8 — decisões operacionais**, documentadas no código, porque os documentos as deixam em aberto: chamada por valor; `se` com 3 argumentos avalia só o ramo tomado (denotação igual, contagem de passos diferente); `algum`/`todos` em curto-circuito; `uniao A B` definida exatamente como `dobraR (λx acc. se (pertence x acc) acc (cons x acc)) A B`, que põe os elementos novos primeiro e remove duplicatas de B; padrao(Grade) = grade vazia de lado n; `ateFixo` para quando f(x) = x ou após F(n) aplicações e devolve o último x; fix em tipo funcional é preguiçoso (nível k = x ↦ (f nível_{k−1}) x, a forma η-expandida de f^{F(n)}(padrao)); `se`/`se@*` são nomes reservados para a avaliação preguiçosa.
23. **D9 — polimorfismo.** Instâncias monomórficas: o mínimo exigido pela escada e pelo fechamento de τ/τ' sobre ela. E0 tem 37 instâncias mais fix; E0', 31 mais fix; E0+, 44; E0'+, 32. As contagens genéricas são 29/20/31/21, como no documento, e um teste as verifica. Escolher instâncias conhecendo a escada é decisão do experimentador e precisa ser reportada. **[nota]** Ver o item 4 da seção 2.1: a v2 mede o efeito com a tabela sistemática.

**Enumerador**

24. **Desvio 1 [P] — o item (a), como pedido, é matematicamente impossível.** Nenhuma grade de `oraculo_treino` com n ≤ 4 tem uma única preta em (1,1), nem o complemento disso. Por isso os termos `algum@P (celula g) (cauda@P (posicoes g))` (tamanho 6) e `nao (vazia?@P (pretas g))` (tamanho 4) coincidem em todas as amostras admissíveis e só diferem numa grade da partição reservada. Nenhum enumerador com amostra só de `oraculo_treino` pode igualar o sem-poda sobre as 512 grades de n = 3. Correção: a validação foi dividida em dois testes. V1 testa o mecanismo em modo auditoria, com os 512 mundos como amostra; isso só é aceito com `auditoria=True` e `permitir_fora_particao=True`, e a busca do aprendiz nunca usa esse modo. V2 usa a amostra de produção e verifica que nenhuma classe da amostra se perde. O teste `test_limitacao_particao` registra o contraexemplo.
25. **Desvio 2 — gramática.** Redexes β `((λx.c) a)` ficam excluídos por omissão (`redexes_beta=False`). Quando x ocorre no máximo uma vez, c[a/x] é menor e nada se perde; quando ocorre duas ou mais vezes (um "let"), o tamanho mínimo de uma classe pode aumentar. A gramática literal continua disponível com `redexes_beta=True`, e as contagens são publicadas nos dois modos. Exemplo em `{g} ⊢ Bool` com s = 8: 106 384 termos sem redexes contra 663 325 com eles. A decisão é necessária para a viabilidade: com redexes, a busca precisa de contextos (L Pos, L Pos) com milhares de mundos. **[nota]** PM7 da v2 dá N(8) = 106 384 em E0 `{g} → Bool`.
26. **Desvio 3 — fix.** Só aparece em tipos funcionais, na forma η-longa `fix (λrec. λx1..xk. corpo)`. Regras: rec ocorre pelo menos uma vez; os seus argumentos não contêm rec; rec pode ser aplicado parcialmente e chamado várias vezes; fix aninhado é permitido em subtermos sem rec. Fix em tipo de primeira ordem, que o documento 02 permite, não é enumerado. Os corpos que contêm rec são montados a partir dos representantes da poda para os subtermos sem rec, e só o fix completo é deduplicado. Limitação: na recursão, os x recebem valores fora das amostras.
27. **Desvio 4 — universo de tipos.** T é `dsl.UNIVERSO_TIPOS` mais os subtipos da tabela, do tipo-alvo e do contexto, o mesmo para E0, E0' e E0+. Uma aplicação f a exige que α e α → τ estejam em T. A profundidade de λ é D = 2 por omissão; ela conta os x de fix, mas não conta rec nem as variáveis do contexto. Alguns programas brutos precisam de D = 3 (por exemplo UmComponente com `fecho` inline).
28. **Desvio 5 — s_reach.** A definição de s_reach (documento 03, 2.4) é ambígua quanto a quais candidatos contam. O valor principal conta todos os candidatos avaliados pela poda, em todos os contextos e tipos auxiliares (leitura conservadora). `s_reach_so_alvo` conta só os candidatos do tipo-alvo, mas dentro da mesma execução limitada pelo orçamento total.
29. **Desvio 6 — a poda é aproximada em pontos documentados.** Há níveis de amostragem: binders Pos, listas e funções criam contextos com os mundos de só K1 = 8 e K2 = 3 mundos-raiz (hiperparâmetro `mundos_funcao`); dentro de cada contexto a comparação é congruente, e a aproximação fica na fronteira entre níveis. As amostras de lista são 11 no nível 0 e 6 nos níveis aninhados. A amostra de Grade é só a própria grade: `Grade.vazia(n)` ficou de fora porque, para n = 2 e n = 4, ela está na partição confirmatória. Os tipos funcionais usam deduplicação exata em dois estágios (chave rápida em 4 mundos).
30. **Desvio 7 — limite de passos.** O limite é por mundo avaliado (`orcamento_passos_mundo`, 10 000 por omissão), não por candidato. Candidatos que o excedem são descartados e contados em `descartados_orcamento_passos`, uma fonte declarada de incompletude: 1 332 em 10⁵ candidatos em `{g} ⊢ Bool`.
31. **Desvio 8 — `buscar`** devolve o menor representante consistente, na ordem do enumerador. A amostra da poda é fixa e independente dos exemplos, o que mantém válida a continuação incremental. Em compensação, se os exemplos tiverem grades fora da amostra, um termo podado pode ser consistente onde o representante não é. O orçamento de `buscar` conta candidatos do tipo da tarefa (documento 03, 2.3); o custo interno da poda vai para os campos `enumeracao_*`. **[nota]** Na v2 os mundos OE incluem também as grades dos exemplos e contraexemplos (item 9 da seção 2.1).
32. **Desvio 9** — o parâmetro `n` de `Enumerador` foi mantido na interface, mas não é usado: o lado de cada mundo é o da sua grade.
33. **Desvio 10 — desempenho.** PM9 (≥ 2 000 candidatos/s) não é atingido. O módulo mediu 1 044/s e 528/s com 10⁴ e de 206 a 278/s com 10⁵, perto do limite de interrupção I6 (200/s). Cerca de 80 % do tempo vai para 1,3 % dos candidatos: fix divergentes lineares (por exemplo `fix (λrec x1. rec x1)`), que o avaliador desdobra preguiçosamente por F(n) níveis (256 em n = 4). Memória: pico de 1,7 GB com 10⁵, contra a estimativa do documento 03, §8, de menos de 4 GB com 10⁶. **[nota]** PM9 da v2: mínimo 56, mediana 423, máximo 2 899/s (seção 3.3).

**Biblioteca**

34. **impl das entradas de biblioteca.** A tarefa pedia uma `Primitiva` "com impl obtida avaliando o termo fechado". Só que `dsl.Primitiva` exige que uma entrada de biblioteca tenha corpo e `impl=None`, e levanta `ErroProveniencia` caso contrário. Para manter esse invariante, a entrada guarda só o corpo. O avaliador calcula a denotação a partir do corpo quando ela é necessária (`Contexto.constante`), e `Biblioteca.denotacao(nome, n)` a expõe. O comportamento é o mesmo; nada é guardado como impl.
35. **Pontuação.** `pontuacao = (ocorrencias − 1) × (tamanho − 1)`, com tamanho = |termo fechado|, como no documento 03. Esse é o ganho MDL exato só para subtermos fechados: ignora os parâmetros em cada uso, e o ganho real é k·(|corpo| − 1 − p) − |termo fechado|. Para garantir que a compressão gulosa termine, foi acrescentado um filtro que não está nos documentos: |corpo| > 1 + número de parâmetros, de modo que toda reescrita encolhe estritamente o corpus. Também são filtrados os fragmentos η-redutíveis e os feitos só de parâmetros.
36. **Buracos.** A tarefa fixa no máximo 1 buraco, e o documento 03 diz "até dois". Foi implementado um parâmetro `max_buracos`, com padrão 1. Variáveis livres emparelhadas entre as duas ocorrências viram parâmetros, mas não contam como buracos. Um par (a, b) que aparece mais de uma vez reutiliza o mesmo buraco. A anti-unificação pode pôr um buraco na cabeça de uma aplicação quando as duas constantes têm o mesmo tipo (por exemplo `algum`/`todos`, `linhas`/`colunas`).
37. **Contagem de ocorrências.** As ocorrências são contadas módulo renomeação, por casamento de padrões sobre todas as soluções e sem sobreposição, exatamente pela regra que a reescrita usa (a mais externa primeiro, depois dentro dos argumentos). Registram-se o total de ocorrências e as soluções de origem (`origem_ids`). A tarefa não dizia se a contagem é por solução ou total.
38. **Modo `mecanismo-teste`.** Toda entrada é forçada a `manual-teste`, mesmo quando as soluções de entrada são declaradas `descoberta`. Motivo: uma tabela de referência só com entradas `descoberta` passaria por `Tabela.para_aprendiz()`, o que seria um vazamento. No modo autônomo as regras são: só objetos `Solucao`, cada um marcado `descoberta`; as origens do fragmento têm de ser exatamente {`descoberta`}; e a `Tabela` de uso `descoberta` recusa `manual-teste`. São duas barreiras independentes.

**Livro-razão**

39. **Nomes de campo.** O documento 03, 2.3, diz `compressao_passos`; a tarefa diz `compressao_subtermos`. Foi usado `compressao_subtermos`, cuja unidade são nós de termo examinados (enumeração + anti-unificação + casamento/reescrita; `ContadorCompressao.subtermos_examinados`).
40. **total() do livro.** Os campos têm unidades diferentes (candidatos, passos, nós, consultas, grades). `total()` é a soma simples que o protocolo define. São reportados também `total_aprendiz` (busca, compressão, consultas), `total_ambiente` (`oraculo_custo_ambiente`, `geracao_grades`) e `total_avaliacao`. O documento 02, 2.5, diz que o custo do ambiente é reportado à parte. Na execução seca (U25), o termo do ambiente era cerca de 95 % do total. **[nota]** Na v2, `total_aprendiz` inclui também `enumeracao_*`. Em L-fix@E0, os campos do ambiente (`geracao_grades`, `geracao_rotulos`, `oraculo_custo_ambiente`, `oraculo_passos_hipotese`) somam 612 518 de 598 278 269, cerca de 0,1 %.
41. **`verificar_fechamento`.** Somar os campos para obter o total tornaria a verificação trivialmente verdadeira. Em vez disso, toda escrita vai para um diário de lançamentos, e a verificação reconstrói cada entrada a partir do diário: entrada = diário, campo a campo; total = soma dos campos = soma do diário. Uma escrita direta numa entrada é detectada.
42. `memoria_pico_kb` = `ru_maxrss` do processo inteiro (que não pode ser reiniciado), não o pico do bloco medido, como em `medidas.py` e `geradores.py`. **[nota]** Em `medicoes.json` da v2, a memória por job é o pico do trecho (VmHWM reiniciado, num processo novo por job, escopo `trecho`). Em `razao.json → medicoes`, ela continua a ser o pico do processo desde o início.
43. A execução seca U25 não tem módulo enumerador nem oráculo (eles não estavam disponíveis quando foi escrita). Usa uma lista fixa de candidatos por tarefa, traduzida para E0' por beta_segura∘τ, e uma busca exaustiva de contraexemplo em n ≤ 3 dentro do teste. Para NenhumaIsolada usa `NENHUMA_ISOLADA_CORRIGIDA`, porque o programa do documento discorda da referência na grade vazia (já registrado em `DISCREPANCIAS_DOC`).

**Oráculo**

44. **[P] "Pular tamanhos degenerados" (instrução da tarefa) é matematicamente incorreto para o oráculo, se "pular" significar descartar.** Exemplo: ExistePreta é degenerado em todo n ≤ 4 na partição `oraculo_treino`, pelo critério `geradores.degenerado` (o único negativo, a grade vazia, não tem par), e o reservatório de n = 5 e 6 não tem negativos. Descartar esses tamanhos faria o oráculo devolver `None` para h = falso, ou seja, declarar correta uma hipótese errada. Correção adotada: os tamanhos degenerados são pulados na ordem normal e examinados só no fim da busca. `criterio_degenerado='sem_par'` é o padrão e usa `geradores.degenerado(...)['degenerado']`; também existem `'rotulo_constante'` e `'nenhum'` (ordem pura). A ordem efetiva fica em `Oraculo.ordem_busca`, e a minimalidade vale nessa ordem. Com o padrão, a ordem típica é n = 3, 4, depois 5 e 6 (reservatório e busca local) e, por fim, n = 1 e 2. A força bruta de U23 recebe a mesma ordem de tamanhos (parâmetro `ns`); o teste U23 também passa com `'nenhum'` na ordem natural de 1 a 4.
45. Para n ≥ 5, o diagnóstico de degeneração usa a composição do reservatório (falta de positivos ou de negativos) em vez de chamar `geradores.degenerado`. Para n ≥ 5, essa função gasta o rng e só faz tentativas, e o domínio de fato buscado é o reservatório.
46. "Busca local por trocas que maximiza a discordância" (documento 02, 2.2.3) não tem sentido literal: a discordância numa única grade é binária, e h é uma caixa-preta. Interpretação implementada: vizinhança de UMA troca preta↔branca a partir das grades do reservatório (preservando o número de pretas de cada semente), dentro da partição e fora do reservatório. São gerados até `max_busca_local` = 500 candidatos, ordenados pela chave de minimalidade, e devolve-se a primeira discordância. O resultado é mínimo só dentro do conjunto examinado (`minimo_garantido=False`).
47. Hiperparâmetros provisórios do piloto, ainda não calibrados: `K_RESERVATORIO` = 40 positivos construtivos por n (cada um com o seu negativo emparelhado e o seu quase-acerto) e `MAX_BUSCA_LOCAL` = 500. **[nota]** `config.json`: `k_reservatorio` = 40.
48. Por padrão, `Oraculo.rotulo(g)` recusa grades fora da partição do oráculo (`PermissionError`), para evitar vazamento de rótulos de teste. O protocolo não especifica isso.
49. **Custo do ambiente no livro-razão.** Cada consulta lança `oraculo_consultas` = 1 e `oraculo_custo_ambiente` = número de grades em que h foi avaliada nessa consulta (1 para `rotulo`). A construção lança `geracao_grades` = soma de `grades_geradas` dos reservatórios. O documento 03, 2.3, não fixa a unidade do "custo do ambiente".

**Adaptadores**

50. O documento 02, 2.11.1, não define F(n) para portadores que não são grades. Adotei n_semantica = ⌈√m⌉, de modo que F = n⁴ ≥ m² (para m = n², coincide com as grades). Posições de sequência e de grafo são codificadas como o par opaco (1, i): Pos é opaco em E0, e assim o padrão (1,1) de Sem_n é o primeiro elemento na ordem fixa, o que mantém totais `cabeca` de lista vazia e fix em Pos. Em sequências, `linhaDe(i)` = todos os índices e `colunaDe(i)` = (i,), por coerência com `linhas`/`colunas` (E0' não está na tabela 2.11.1). Os vizinhos de um grafo saem em ordem crescente de nó.
51. A tabela adaptada inclui SEMPRE as 8 primitivas de portador, mesmo as de outra base, para que o avaliador nunca recorra a `REGISTRO_BASE`, isto é, à implementação de grades, com um portador que não é grade.
52. "Nenhum arquivo de outro módulo foi editado" (declaração do módulo de adaptadores). **[nota]** O item 3 desta seção registra uma correção em `referencias.py` feita pelo módulo de geradores. `git status` mostra `fedro_piloto/referencias.py` como modificado.

**Orquestração e execução**

53. **Escala reduzida**, para caber em cerca de 2 h de CPU (o documento 03, seção 8, previa até cerca de 100 h). PM1 usa 300 amostras por n de 5 a 9 (documento: 10⁵). PM2 a PM5 usam até 100 pares (documento: ≥ 1 000). PM6 usa Monte Carlo de 1 000 só para n de 5 e 6. s_reach foi medido até B = 10⁵ (documento: 10⁶), e só nos pares E0 {g}→Bool, E0 {g,S}→LP, E0' {g}→Bool e E0+ {g}→Bool; os demais pares e os 5 tipos fechados de tarefa foram medidos até 10⁴. A execução autônoma usou B_tarefa = 10⁴ (a sugestão era 2×10⁴) e não incluiu L-mem nem controles. O B_max da regra de decisão passou a ser o maior B medido. E0'+ não tem s_reach medido. **[nota]** Na v2, o B da regra de decisão é um B único = 10⁴ (item 2 da seção 2.1), e E0'+ tem s_reach a 10⁴ (seção 3.3).
54. **CPU real gasta**: cerca de 88 min na execução completa, cerca de 32 min na recomputação das fases 1, 6 e 7, mais cerca de 1 h numa primeira tentativa abortada. Total acima das cerca de 2 h previstas. **[nota]** Esses números são das execuções anteriores. A v2 gastou 8 249,7 s de CPU (cerca de 137 min) e 2 944,7 s de parede (seção 5.2). A execução PM15 não está somada aqui.
55. **Memória.** A primeira tentativa foi abortada porque um trabalhador que media o alcance em E0+ a 10⁵ passou de 8 GB. O limite do cgroup é de 14,3 GB para todos os processos; o OOM matou o trabalhador e travou o Pool. Agora cada trabalhador roda com RLIMIT_AS = 4 GB, e um `MemoryError` fica registrado (`limitado_por_memoria`) em vez de travar. Na execução final, E0 {g,S}→LP a 10⁵ parou por memória após 52 628 candidatos; s_reach(10⁵) ficou nulo e s_reach(10⁴) = 6 continua válido. O documento 03, seção 8, estimava menos de 4 GB a 10⁶. **[nota]** Na v2 a parada foi após 52 726 candidatos (`medicoes.md`), com s_reach(10⁴) = 6.
56. **Correção de PM6** (erro do módulo, encontrado e refeito). Restringir a amostragem aos baldes não confirmatórios enviesa domínios pequenos: CantoSupEsq com n = 3 e p = 0,2 dava 0,110 contra 0,2. Para n ≤ 4 a frequência passou a ser exata sobre o domínio inteiro (auditoria, como o PM1 exaustivo; nenhuma grade vira dado). Para n ≥ 5 continua o MC fora dos baldes confirmatórios. A tolerância cobre o arredondamento de 3 casas da auditoria. As fases 1, 6 e 7 foram recalculadas com `--reaproveitar`, registrado em `deterministico.json → reaproveitamento` e em `comandos.txt`. **[nota]** Isso vale para a execução anterior. A v2 calculou as 7 fases sem reaproveitar, e o seu PM6 já usa "exata (domínio inteiro)" em n = 3 e 4 e "mc (baldes não confirmatórios)" em n = 5 e 6.
57. Os exemplos iniciais vêm da partição `oraculo_treino`, como pedido (o protocolo, 2.9, diz D_treino). ExistePreta não admite negativo emparelhado em densidade: o único negativo é a grade vazia, e entre n = 3 e 4 só a de n = 3 está em `oraculo_treino`. Por isso a tarefa usou 2 positivos e 1 negativo natural, com o método registrado. **[nota]** v2: exemplos `4:1101001111111011` (verdadeiro), `3:000000000` (falso), `4:0000110001100000` (verdadeiro); métodos `positivo-construtivo:n=4` ×2, `negativo-natural-sem-par:n=3`.
58. **Tarefas de função** (o protocolo não especifica estes detalhes). (a) As entradas vêm de baterias fixas do ambiente derivadas da grade: todas as posições; listas (vazia, 1ª/última preta, pretas, posições, linhas, colunas); pares de listas de pretas por região. (b) O oráculo de função varre exaustivamente as grades da partição para n de 1 a 3, mais um reservatório de 40 grades de n = 4, na ordem (n, pretas, lexicográfica, índice da bateria); só a parte exaustiva garante o mínimo. (c) `passo`, `fecho` e `componenteDe` comparam por igualdade de conjunto, porque a ordem não é especificada. (d) As tarefas sem argumento Grade (`descartar`, `noMaximo`, `mesmoNumero`) são avaliadas em Sem_3.
59. **Contabilidade da busca.** `busca_candidatos` soma os candidatos testados nos exemplos (nota `exemplos`) e os avaliados internamente pelo enumerador na poda OE, em todos os contextos (nota `enumeracao-oe`); o mesmo vale para `busca_passos`. B_tarefa limita a contagem do enumerador e, separadamente, a dos testes nos exemplos. **[nota]** Na v2 os candidatos internos estão em campos próprios, `enumeracao_candidatos` e `enumeracao_passos` (item 8 da seção 2.1).
60. Uma hipótese que excede 10⁵ passos numa grade fica "indefinida" ali e é pulada pelo oráculo (convenção do `oraculo.py`), com o caso contado. **[nota]** Na v2 uma indefinição conta como discordância (item 10 da seção 2.1). `config.json → orcamento_passos` = 100 000.
61. **Variante declarada L-lib+f** (não é o braço do protocolo; fica fora da decisão principal). A solução aceita de cada tarefa de FUNÇÃO também vira entrada de biblioteca (método `promocao-solucao`, proveniência `descoberta`). Motivo: a regra de compressão (ocorrências ≥ 2, pontuação (o − 1)(t − 1)) nunca transforma a solução isolada de um degrau em abstração, mas a tabela 2.8.1 mede cada degrau "com os degraus anteriores". Como está escrito, o protocolo é inconsistente nesse ponto.
62. Limiar de compressão fixado a priori em 3, que é a pontuação de um fragmento de tamanho 4 com 2 ocorrências, com `max_pares` = 20 000. **[nota]** `config.json`: `limiar` = 3; `limiar_mecanismo` = 5 na fase 5.
63. PM10: s_reach por contexto com desconto de binders (Grade → Bool: tamanho − 1 em {g} → Bool; λg S.: tamanho − 2 em {g,S} → LP) ou pelo tipo fechado a 10⁴. A coluna de profundidade λ mostra que o enumerador (D = 2) não representa `descartar` via `dobraR` em E0+ e E0' (que exige profundidade 4): em E0+, só a versão com fix (tamanho 13) está na gramática.
64. PM11 conta igualdade comportamental a menos da ordem dos argumentos: `passo` foi extraído como λS g. … (permutação [1, 0]).
65. A avaliação em teste (M4 simplificada) usa 30 grades de `teste_int` com n de 4 a 6, e só para hipóteses aceitas. A verificação a custo igual, se fosse necessária, usaria candidatos como unidade e teto de 60 000. Ela não chegou a ser acionada, porque nenhuma reutilização ocorreu. **[nota]** `config.json`: `num_teste` = 30, `custo_igual_max` = 60 000; `fases.6.custo_igual` = [].

### 2.3 Desvios do plano visíveis nos registros e não listados acima

- PM7 foi reportado até s = 10 (`contagem_s_max` = 10); o documento pede até s = 12.
- PM8 sem B = 10⁶; ver item 2 da seção 2.1.
- PQ11 (execução seca com distribuição de K e curvas de custo) foi feita como execução autônoma de 5 braços. As curvas estão em `deterministico.json → fases.6.bracos.*.curva` como tabelas, não como gráficos.
- PQ12 / PM16 usa o K médio observado (1,40) e o custo por candidato observado; o modelo é o da seção 8.
- Nenhum braço E0' na fase 6, e por isso a exigência autônoma em E0' não foi verificada (`exigencia_autonoma_E0p`).
- Fases numeradas de 1 a 7 no código, contra 0 a 6 no documento 03, §7. A fase 7 do código é a decisão.
- A regra de decisão aplicada (`piloto.decidir`) acrescenta uma exigência autônoma por base que não está no documento 03, §10. O acréscimo é mais restritivo que a regra (seção 7).
- As condições de interrupção I4 e I6 só disparam, pelo §9, "após revisão" e "após otimização". Nenhuma das duas foi feita, mas os registros marcam as duas como disparadas (seção 7, item 7). I2 não é avaliada pelo código.

---

## 3. Resultados por fase

### 3.0 Tabela PM1–PM16

| métrica | limiar (doc. 03, §4) | valor nesta execução | situação | fonte |
|---|---|---|---|---|
| PM1 concordância de referências | 0 | 0 discordâncias (35 conceitos; exaustivo n de 1 a 4; 300 amostras por n de 5 a 9) | atingido, em escala reduzida [C] | `deterministico.json → fases.1.pm1_total_discordancias` |
| PM2 taxa de aceitação | ≥ 0,5 | 1,000 nas 28 células não degeneradas; 4 células degeneradas (ExistePreta) | atingido onde definido [C] | `fases.1.pm2_pm5` |
| PM3 vazão dos geradores | ≥ 1 000 pares em ≤ 60 s | projeção a partir de ≤ 100 pares: de 0,34 s a 18,8 s por 1 000 pares; 1 000 pares não foram gerados | não medido no limiar; projeção dentro de 60 s [E]/[H] | `medicoes.md`, PM3 |
| PM4 emparelhamento de densidade | 1,0 | 1,000 nas 28 células não degeneradas; impossível em ExistePreta (seção 2.2, item 4) | atingido onde definido [C] | `fases.1.pm2_pm5` |
| PM5 M10 | ≤ 0,55 | 0,500 nas 28 células (por construção; seção 2.2, item 5); em ExistePreta M10 = 1 por prova | atingido nas 28 células, pouco informativo; não atingível em ExistePreta [C]/[P] | `fases.1.pm2_pm5` |
| PM6 frequências naturais | dentro de 3 DP | 256 comparações, 0 fora de 3 DP | atingido [C] | `fases.1.pm6`, `pm6_fora_de_3dp` |
| PM7 contagem N(s, τ) | até s = 12 | até s = 10, 12 pares (base, contexto) | parcial [C] | `fases.2.pm7` |
| PM8 s_reach(B, τ) | B ∈ {10⁴, 10⁵, 10⁶} | 10⁴ em todos os pares; 10⁵ em 4 pares, um deles nulo por memória; 10⁶ não medido | parcial [C] | `fases.3.pm8` |
| PM9 vazão do enumerador | ≥ 2 000/s em s ≤ 8 | mín. 56, mediana 423, máx. 2 899; 83/84 abaixo | falha [E] | `medicoes.json → decisao_custo.PM9` |
| PM10 degraus alcançáveis | tabela | E0: 6/14; E0': 4/14; E0+: 6/14; E0'+: 5/14 (B = 10⁴, anteriores manuais como constantes); em cadeia: E0 3/14, E0+ 3/14, E0' 1/14, E0'+ 1/14 | ver seções 3.4 e 7 [C] | `fases.4.pm10` |
| PM11 extração de abstrações | 100 % | 1/3 (`passo`, de um único programa manual); alvo presente no ranking: 3/3 | falha; condição de I4 observada, sem a revisão exigida [C]/[R] | `fases.5` |
| PM12 minimalidade do oráculo | 50/50 | 50/50 (50 com contraexemplo) | atingido [C] | `fases.6.pm12` |
| PM13 latência do oráculo | ≤ 2 s | máx. 0,360 s na fase 6; máx. 0,0015 s nos 50 pares de PM12 | atingido [E] | `medicoes.json → decisao_custo.PM13`, `fases_detalhe.6.pm12` |
| PM14 fechamento do livro-razão | 0 | fechamento: diferença 0; conciliação com contadores independentes: diferença 0, 0 divergências | atingido [C] | `fases.6.fechamento`, `fases.6.pm14_conciliacao` |
| PM15 determinismo | idêntico | idêntico nas fases 1, 2, 4, 5, 6 e 7; livro-razão sem diferenças; mesmo código | atingido nas fases comparadas. A fase 3 (s_reach, PM9) não foi comparada; as fases 4 e 7 da PM15 usam o s_reach reaproveitado [C] | `runs/…-v2-pm15/pm15.json` |
| PM16 custo projetado | ≤ 2 000 h | 7 399 h | falha [E]/[H] | `medicoes.json → decisao_custo.PM16` |

PM14: os campos `oraculo_passos_hipotese`, `geracao_rotulos` e `avaliacao_passos` não têm contador independente (`pm14_conciliacao.campos_sem_contador_independente`), e por isso a conciliação não os cobre.

### 3.1 Fase 1 — referências e geradores (PM1 a PM6)

**PM1.** 35 conceitos. Exaustivo em n = 1, 2, 3 e 4 (2, 16, 512 e 65 536 grades por conceito; 2 312 310 avaliações no total) e 300 amostras por n de 5 a 9 (52 500 no total). Discordâncias: 0. Tempo de parede da fase 1: 32,5 s. [C]

**PM2 a PM5** (partição `oraculo_treino`; até 100 pares solicitados):

| conceito | n=3 pares | n=4 | n=5 | n=6 | PM2 | PM4 | PM5 (M10) |
|---|---|---|---|---|---|---|---|
| ExistePreta | degenerado | degenerado | degenerado | degenerado | — | — | — |
| ParAdjacente | 67 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |
| NenhumaIsolada | 43 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |
| UmComponente | 33 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |
| Igual_linha1_linhaN | 32 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |
| LinhasIguais | 7 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |
| TodosMesmoTamanho | 33 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |
| DoisSeparados | 28 | 100 | 100 | 100 | 1,000 | 1,000 | 0,500 |

- Em n = 3 as 7 células estão marcadas `limitado_por_capacidade` (a partição não tem mais pares).
- Motivos da degeneração de ExistePreta: n = 3, "nenhum positivo tem negativo com o mesmo número de pretas"; n = 4, "sem negativos"; n = 5 e 6, "nenhum par formado (200 tentativas, 200 positivos sem par)".
- `rotulos_confirmados` = verdadeiro nas 28 células. `taxa_particao` (fração das grades construídas que cai na partição) vai de 0,123 a 0,570.
- Métodos de negativos e hashes por célula: `relatorio.md`, fase 1, e `hashes.json`.
- **Negativos repetidos** (`negativos_repetidos`, omitido na v0.1). Os conjuntos de n = 3 reaproveitam muitas vezes os mesmos negativos: ParAdjacente 60 em 67 pares; NenhumaIsolada 14/43; TodosMesmoTamanho 13/33; UmComponente 9/33; DoisSeparados 6/28; Igual_linha1_linhaN 2/32; LinhasIguais 0/7. Em n = 4: ParAdjacente 17/100, DoisSeparados 9/100, LinhasIguais 4/100. O número de grades distintas é, portanto, menor que 2 × pares, e PM4 = 1 e M10 = 0,5 valem sobre conjuntos com negativos repetidos. [C]

**PM3** (`medicoes.md`): pares/s entre 53,1 (DoisSeparados, n = 3) e 2 905,8 (LinhasIguais, n = 6). A projeção para 1 000 pares vai de 0,344 s a 18,818 s. Ela é extrapolada de ≤ 100 pares e, em n = 3, de células limitadas por capacidade, onde 1 000 pares não existem na partição. ExistePreta não tem PM3. [E]/[H]

**PM6.** 16 conceitos × n ∈ {3, 4, 5, 6} × p ∈ {0,2; 0,35; 0,5; 0,65} = 256 comparações com `analysis/audit_frequencias_saida.md`. Em n = 3 e 4 o cálculo é exato (domínio inteiro); em n = 5 e 6, MC com 1 000 amostras fora dos baldes confirmatórios. Fora de 3 DP: 0. [C]

**Degeneração em `oraculo_treino`** (n de 1 a 6; 16 células degeneradas): ExistePreta em n de 1 a 6; ParAdjacente, NenhumaIsolada, UmComponente, Igual_linha1_linhaN e LinhasIguais em n = 1 e 2. Para n = 5 e 6 a degeneração é heurística: "por 200 tentativas; ausência não provada". [C]

### 3.2 Fase 2 — contagem N(s, τ) (PM7)

Contagem exata por programação dinâmica, gramática sem redexes β (seção 2.2, item 25). [C]

| base | contexto | N(8) | N(9) | N(10) | N(10)/N(9) |
|---|---|---|---|---|---|
| E0 | {g} → Bool | 106 384 | 645 367 | 3 984 141 | 6,17 |
| E0 | {g} → L Pos | 65 433 | 385 825 | 2 318 750 | 6,01 |
| E0 | {g, S: L Pos} → L Pos | 193 252 | 1 275 100 | 8 563 892 | 6,72 |
| E0' | {g} → Bool | 43 549 | 237 091 | 1 316 298 | 5,55 |
| E0' | {g} → L Pos | 5 644 | 26 810 | 130 000 | 4,85 |
| E0' | {g, S: L Pos} → L Pos | 15 781 | 81 147 | 422 450 | 5,21 |
| E0+ | {g} → Bool | 125 234 | 794 685 | 5 138 098 | 6,47 |
| E0+ | {g} → L Pos | 121 174 | 782 720 | 5 141 682 | 6,57 |
| E0+ | {g, S: L Pos} → L Pos | 362 006 | 2 616 664 | 19 236 606 | 7,35 |
| E0'+ | {g} → Bool | 45 817 | 251 248 | 1 403 823 | 5,59 |
| E0'+ | {g} → L Pos | 10 401 | 51 287 | 257 204 | 5,01 |
| E0'+ | {g, S: L Pos} → L Pos | 28 939 | 155 157 | 843 344 | 5,44 |

As contagens de s = 1 a 10 estão em `relatorio.md`, fase 2. A razão de crescimento por unidade de tamanho, entre s = 9 e s = 10, fica entre 4,85 e 7,35. PH5 fala em "base entre 6 e 12 por folha"; o tamanho conta folhas e abstrações, então as duas grandezas não são idênticas. [C]

### 3.3 Fase 3 — alcance (PM8), vazão (PM9) e auditoria da poda OE

**PM8, tabela curada, D = 2** (s_reach principal; entre parênteses, s_reach só do alvo quando difere):

| base | {g}→Bool | {g}→L Pos | {g,S}→L Pos | Grade→Bool | Grade→Pos→L Pos | Grade→L Pos→L Pos | L Pos→L Pos→L Pos | L Pos→L Pos→Bool |
|---|---|---|---|---|---|---|---|---|
| E0, 10⁴ | 7 (9) | 7 | 6 (7) | 8 | 9 | 8 | 7 | 9 |
| E0, 10⁵ | 9 | — | nulo (memória) | — | — | — | — | — |
| E0', 10⁴ | 8 (10) | 8 | 7 | 10 | 11 | 10 | 8 | 10 |
| E0', 10⁵ | 10 | — | — | — | — | — | — | — |
| E0+, 10⁴ | 7 (9) | 7 | 6 | 8 | 9 | 8 | 7 | 8 |
| E0+, 10⁵ | 9 | — | — | — | — | — | — | — |
| E0'+, 10⁴ | 8 | 8 | 7 | 10 | 11 | 9 | 8 | 10 |

- **Tabela sistemática, 10⁴.** E0: 7, 6, 6, 8, 9, 7, 7, 8. E0+: 6, 6, 6, 8, 9, 7, 7, 8 (mesma ordem de colunas). A curadoria aumenta s_reach em até 1 nas células em que eles diferem. [C]
- **D = 4** (contextos que os programas de E0'/E0'+ exigem), 10⁴: E0' Grade→Pos→L Pos 9, {g,S}→L Pos 7, Grade→L Pos→L Pos 8, {g}→Bool 7, L Pos→L Pos→L Pos 7; E0+ L Pos→L Pos→L Pos 7; E0'+ Grade→Pos→L Pos 9, {g,S}→L Pos 7, {g}→Bool 7, L Pos→L Pos→L Pos 7. [C]
- **I5** (s_reach(10⁶, `Grade → Bool`) < 8): o fechado Grade → Bool tem s_reach(10⁴) = 8 em E0. Como s_reach não decresce com B, s_reach(10⁶) ≥ 8, e I5 não dispara. [C]

**PM9** (`medicoes.md`): 84 jobs de medição; candidatos/s mín. 56, mediana 423, máx. 2 899. Abaixo de 2 000/s: 83/84. Abaixo de 200/s: 21/84. O maior pico de memória de um job foi 4 026 792 KiB (E0 {g,S}→L Pos, curada, limitado a 4 GB); E0 {g}→Bool, a 10⁵, teve pico de 1 699 748 KiB. [E]

**Auditoria da poda OE** (E0, D = 2, contra uma amostra independente de `teste_int`; classes de tamanho mínimo s sem representante OE com essa denotação):

| tipo | s_max | classes | perdidas | atrasadas | perdas por s |
|---|---|---|---|---|---|
| Grade → Bool | 8 | 56 | 2 | 0 | s = 8: 2/38 |
| Grade → Pos → L Pos | 8 | 214 | 2 | 0 | s = 8: 2/143 |
| Grade → L Pos → L Pos | 8 | 875 | 12 | 0 | s = 7: 1/189; s = 8: 11/579 |
| L Pos → L Pos → L Pos | 7 | 225 | 0 | 0 | — |
| L Pos → L Pos → Bool | 8 | 163 | 8 | 2 | s = 7: 1/43; s = 8: 7/93 |

Nenhuma classe foi perdida em s ≤ 6. As perdas aparecem em s = 7 e 8. [C]

### 3.4 Fase 4 — viabilidade da escada (PM10)

Os programas da escada são **manuais** (`manual-teste`), e por isso os tamanhos são limites superiores. B único = 10⁴. "Comparado" = tamanho com anteriores − desconto de binders do contexto. NenhumaIsolada usa a variante corrigida.

| degrau | contexto | E0: comparado / s_reach | E0 | E0+: comparado / s_reach | E0+ | E0' | E0'+ |
|---|---|---|---|---|---|---|---|
| ExistePreta | {g}→Bool | 4 / 7 | sim | 4 / 7 | sim | sim | sim |
| vizPretos | Grade→Pos→L Pos | 8 / 9 | sim | 8 / 9 | sim | não (17 / 9) | não (17 / 9) |
| ParAdjacente | {g}→Bool | 9 / 7 | não | 9 / 7 | não | não | não |
| NenhumaIsolada | {g}→Bool | 14 / 7 | não | 14 / 7 | não | não | não |
| passo | {g,S}→L Pos | 7 / 6 | não | 7 / 6 | não | não | não |
| fecho | Grade→L Pos→L Pos | 16 / 8 | não | 4 / 8 | sim | não | sim |
| componenteDe | Grade→Pos→L Pos | 7 / 9 | sim | 7 / 9 | sim | sim | sim |
| UmComponente | {g}→Bool | 16 / 7 | não | 16 / 7 | não | não | não |
| pretasDe | {g,S}→L Pos | 4 / 6 | sim | 4 / 6 | sim | não | não |
| descartar | L Pos→L Pos→L Pos | 13 / 7 | não | 9 / 7 | não | não | não |
| noMaximo | L Pos→L Pos→Bool | 6 / 9 | sim | 6 / 8 | sim | sim | sim |
| mesmoNumero | L Pos→L Pos→Bool | 9 / 9 | sim (conservador: não) | 9 / 8 | não | sim | sim |
| PrimeiraUltimaIguais | {g}→Bool | 12 / 7 | não | 12 / 7 | não | não | não |
| LinhasIguais | {g}→Bool | 13 / 7 | não | 13 / 7 | não | não | não |
| **alcançáveis** | | | **6/14** | | **6/14** | **4/14** | **5/14** |

Os tamanhos brutos (sem biblioteca), as colunas sistemática e "c/ ant. na tabela" e a profundidade λ estão em `relatorio.md`, fase 4. Em E0, `mesmoNumero` passa com s_reach = 9 da tabela curada e falha com o s_reach = 8 da tabela sistemática ou da tabela com os anteriores; é a única diferença entre a decisão principal e a conservadora em E0. [C]

**Dependência entre degraus** (omitida na v0.1). A coluna "comparado" supõe que os degraus anteriores, que são os programas manuais, já estão na biblioteca como constantes. Ela não exige que esses degraus sejam eles próprios alcançáveis. Em E0, `componenteDe` (7) usa `fecho`, que é inalcançável (16 > 8). `noMaximo` (6) usa `descartar`, também inalcançável (13 > 7), e `mesmoNumero` usa `noMaximo`. Sem esses degraus, os tamanhos brutos são 38, 18 e 35 em E0 e 19, 10 e 19 em E0+, todos acima de s_reach a 10⁴ (`fases.4.pm10[*].tamanho_bruto`). Em E0+, `fecho` (4) usa `passo`, que é inalcançável (7 > 6). Contando só degraus cujos anteriores também são alcançáveis, ficam 3 de 14 em E0 e em E0+: ExistePreta, `vizPretos` e `pretasDe`. Em E0' e E0'+ fica 1 de 14 (ExistePreta). São exatamente as 3 tarefas aceitas na fase 6. [C]

**Verificação dos programas manuais** contra as referências: 0 discordâncias não documentadas em todas as bases. As discordâncias documentadas são as do programa NenhumaIsolada do documento na grade sem pretas: 1 em E0, 1 em E0+ e 3 em E0'+. [C]

### 3.5 Fase 5 — mecanismo de compressão (PM11; modo `mecanismo-teste`, soluções manuais)

| alvo | fontes manuais | extraído (gulosa) | posição no ranking | fragmento igual ao alvo | primeiro fragmento (pontuação) |
|---|---|---|---|---|---|
| vizPretos | ParAdjacente, NenhumaIsolada | não | 4 | `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` (pontuação 7) | `λf1 g2. f1 (λp3. nao (vazia?@P (filtrar@P (celula g2) (vizinhos g2 p3)))) (pretas g2)` (13) |
| passo | fecho | sim, com permutação [1, 0] | 1 | `λl1 g2. uniao l1 (juntar (mapear@P>LP (λp3. filtrar@P (celula g2) (vizinhos g2 p3)) l1))` (13) | o mesmo |
| pretasDe | PrimeiraUltimaIguais, LinhasIguais | não | 11 | `λg1. filtrar@P (celula g1)` (12) | `λl1 l2. vazia?@P ((fix (λf3 l4 l5. se@LP (vazia?@P l4) l5 (f3 (cauda@P l4) (cauda@P l5)))) l1 l2)` (51) |

PM11 = 1/3 = 0,33. A fração de alvos presentes no ranking é 1,00. I4 está marcada como disparada nos registros, sem a revisão do compressor que o §9 exige antes. O único alvo extraído, `passo`, tem `origem_ids` = [`fecho`]: as 2 ocorrências estão dentro de um único programa manual, com `passo` expandido. É repetição dentro de uma solução escrita à mão que já contém o alvo, não compressão entre tarefas. Não mostra que o compressor extrairia `passo` de soluções do aprendiz. A comparação comportamental usou 144 grades (`pm11:grades`, hash `11e13c0b1dcf1da7`). Tempo de parede da fase 5: 2,8 s. [C]/[R]

### 3.6 Fase 6 — execução autônoma (PM12, PM13, PM14; biblioteca vazia, modo `autonomo`)

Cinco braços: L-fix@E0, L-lib@E0, L-lib+f@E0 (variante, fora da decisão), L-fix@E0+, L-lib@E0+. B_tarefa = 10⁴; K = 12; 14 tarefas na ordem da escada.

| braço | aceitas | tarefas aceitas | rodadas por tarefa (contagem) | consultas | candidatos do protocolo | candidatos da enumeração | total_aprendiz |
|---|---|---|---|---|---|---|---|
| L-fix@E0 | 3/14 | ExistePreta, vizPretos, pretasDe | 0:5, 1:6, 2:2, 3:1 | 13 | 4 706 | 111 607 | 597 662 643 |
| L-lib@E0 | 3/14 | idem | 0:5, 1:6, 2:2, 3:1 | 13 | 4 726 | 111 607 | 598 577 530 |
| L-lib+f@E0 | 3/14 | idem | 0:5, 1:6, 2:1, 3:2 | 14 | 5 007 | 111 607 | 571 500 296 |
| L-fix@E0+ | 3/14 | idem | 0:4, 1:7, 2:3 | 13 | 5 196 | 111 916 | 750 572 294 |
| L-lib@E0+ | 3/14 | idem | 0:4, 1:7, 2:3 | 13 | 5 216 | 111 916 | 744 228 913 |

- Hipóteses aceitas, iguais nos 5 braços: ExistePreta `λx0. nao (vazia?@P (pretas x0))` (tamanho 5); vizPretos `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)` (8); pretasDe `λx0. filtrar@P (celula x0)` (4). Acurácia em teste: 1,000 (30 grades de `teste_int`, que dão 90 entradas nas tarefas de função; 29 grades para ExistePreta). As 29 grades de teste de ExistePreta são todas positivas (seção 6.4, item 1), e nessa tarefa a acurácia 1,000 não distingue a hipótese da constante `verdadeiro`. [C]
- As 11 tarefas restantes terminam por `orcamento_enumeracao` em todos os braços. Isso inclui `componenteDe`, `noMaximo` e `mesmoNumero`, que PM10 classifica como alcançáveis em E0. [C] Os registros contradizem a explicação da v0.1, segundo a qual o orçamento seria consumido por re-enumerações do refinamento OE: `refinamentos_oe` = 0 nessas três tarefas, em todos os braços (só ParAdjacente teve 1 ou 2). O que os registros mostram é outro fato. Os tamanhos de PM10 dessas três tarefas supõem `fecho` e `descartar` como constantes de biblioteca, e nenhum aprendiz os tinha. Os tamanhos brutos (38, 18 e 35 em E0; 19, 10 e 19 em E0+) ficam acima de s_reach a 10⁴, e cada uma das tarefas esgotou os 10 001 candidatos de enumeração (seção 3.4, "Dependência entre degraus"). [C]/[F]
- K médio observado: 1,40 (`PM16.K_medio_observado`).
- PM12: 50/50 pares iguais à força bruta, todos com contraexemplo. [C]
- PM13: latência máxima por consulta 0,360 s (L-lib@E0+, ExistePreta). A latência média por braço vai de 0,026 s a 0,032 s. [E]
- PM14: fechamento aritmético, diferença 0; conciliação, diferença 0. Hash do diário: `16c362ee2b3e67ed`. [C]
- Comparação a custo total igual: nenhuma solução aceita reutilizou abstração, e a lista `custo_igual` está vazia. [C]

### 3.7 PM15 — determinismo

`pm15.json`: `identico` = verdadeiro; `fases_identicas` = verdadeiro para 1, 2, 4, 5, 6 e 7; `diferencas_livro_razao` = []; `mesmo_codigo` = verdadeiro. A fase 3 foi reaproveitada e não foi comparada. [C]

### 3.8 PM16 — custo projetado

Modelo do documento 03, §8: tarefas × B × K × s/candidato × sementes × bases × braços, com 60 tarefas, B = 10⁶, K = 1,40 (observado), 3,161 ms/candidato (CPU da fase 6, 1 844,6 s, dividida por 583 504 candidatos, contando os do protocolo e os internos do enumerador), 5 sementes, 2 bases e 10 braços. Resultado: 7 399 h, contra o limiar de 2 000 h. [E]/[H]

### 3.9 Separação do confirmatório (U27)

Semente 10001 no intervalo do piloto: verdadeiro. Partições disjuntas: verdadeiro. Grades no confirmatório: 0. Hashes de todos os conjuntos (desenho, tarefas, reservatórios, contraexemplos, amostras OE, PM11): `hashes.json` e `relatorio.md`, seção "Separação do confirmatório". [C]

---

## 4. Abstrações

### 4.1 Tabela de classificação

| fornecida explicitamente | manual usada como referência ou teste | descoberta pelo aprendiz | descoberta e reutilizada |
|---|---|---|---|
| Primitivas da tabela E0 curada usadas nas hipóteses aceitas: `nao`, `vazia?@P`, `pretas`, `filtrar@P`, `celula`, `vizinhos`. Em E0+ também `ateFixo` e `dobraR` (documento 02, 2.8.3), nenhuma delas usada em hipótese aceita. A construção `fix` é da linguagem. L-teto: tabela não construída. | Os 14 programas da escada de `programas_referencia` (PM10 e verificação), mais `NENHUMA_ISOLADA_CORRIGIDA`. As entradas da compressão gulosa da fase 5, todas `manual-teste`: `λf1 g2. f1 (λp3. nao (vazia?@P (filtrar@P (celula g2) (vizinhos g2 p3)))) (pretas g2)`; `λl1 g2. uniao l1 (juntar (mapear@P>LP (λp3. filtrar@P (celula g2) (vizinhos g2 p3)) l1))`; `λl1 l2. vazia?@P ((fix (λf3 l4 l5. se@LP (vazia?@P l4) l5 (f3 (cauda@P l4) (cauda@P l5)))) l1 l2)`; `λg1 l2. filtrar@P (celula g1) (cabeca@LP l2)`; `λl1 l2. e (abs1 l2 l1) (abs1 l1 l2)`. | Proveniência `descoberta`, mas todas são cópias (α/η) de soluções já aceitas, sem reutilização. L-lib@E0 `abs1`, L-lib@E0+ `abs1`: `λg1. filtrar@P (celula g1)` (fechamento; ocorre nas soluções de `vizPretos` e `pretasDe` e é igual à solução de `pretasDe`). Variante L-lib+f@E0: `abs1` = `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` e `abs2` = `λg1. filtrar@P (celula g1)` (promoção de solução). | **Nenhuma.** |

### 4.2 Abstrações com proveniência `descoberta` (fase 6)

| braço | nome | termo impresso | tipo | método | tarefas de origem | ocorrências / pontuação | cópia de solução | tarefas de reuso | L-fix resolveu a mesma tarefa ao mesmo custo? |
|---|---|---|---|---|---|---|---|---|---|
| L-lib@E0 | abs1 | `λg1. filtrar@P (celula g1)` | Grade → L Pos → L Pos | fechamento | vizPretos, pretasDe | 2 / 3 | sim (= solução de pretasDe) | nenhuma | Origem pretasDe: L-fix@E0 resolveu, custo do aprendiz 39 018 contra 39 391 em L-lib@E0. Reuso: não se aplica. |
| L-lib@E0+ | abs1 | `λg1. filtrar@P (celula g1)` | Grade → L Pos → L Pos | fechamento | vizPretos, pretasDe | 2 / 3 | sim (= solução de pretasDe) | nenhuma | Origem pretasDe: L-fix@E0+ resolveu, 94 449 contra 94 822. Reuso: não se aplica. |
| L-lib+f@E0 (variante) | abs1 | `λg1 p2. filtrar@P (celula g1) (vizinhos g1 p2)` | Grade → Pos → L Pos | promoção de solução | vizPretos | 1 / 0 | sim (= solução de vizPretos) | nenhuma | Origem vizPretos: L-fix@E0 resolveu, 6 308 437 contra 6 308 610. Reuso: não se aplica. ParAdjacente, a tarefa seguinte, não foi resolvida em nenhum dos braços. |
| L-lib+f@E0 (variante) | abs2 | `λg1. filtrar@P (celula g1)` | Grade → L Pos → L Pos | promoção de solução | pretasDe | 1 / 0 | sim (= solução de pretasDe) | nenhuma | Origem pretasDe: L-fix@E0 resolveu, 39 018 contra 39 176. Reuso: não se aplica. |

`descobertas_nao_copia_de_solucao` = [] em todos os braços. `reutilizacoes_em_solucoes_aceitas` = []. A abstração de L-lib foi inserida após a aceitação de pretasDe (9ª tarefa); as 5 tarefas seguintes não foram resolvidas. [C]

---

## 5. Custos

### 5.1 Contadores determinísticos (livro-razão; `deterministico.json → fases.6.livro_total_por_aprendiz`, `razao.json`)

| campo | L-fix@E0 | L-lib@E0 | L-lib+f@E0 | L-fix@E0+ | L-lib@E0+ |
|---|---|---|---|---|---|
| busca_candidatos | 4 706 | 4 726 | 5 007 | 5 196 | 5 216 |
| busca_passos | 135 392 | 136 072 | 154 142 | 326 102 | 326 782 |
| enumeracao_candidatos | 111 607 | 111 607 | 111 607 | 111 916 | 111 916 |
| enumeracao_passos | 597 410 925 | 598 324 544 | 571 229 147 | 750 129 067 | 743 784 418 |
| compressao_subtermos | 0 | 568 | 379 | 0 | 568 |
| oraculo_consultas | 13 | 13 | 14 | 13 | 13 |
| oraculo_custo_ambiente | 17 626 | 17 626 | 17 638 | 17 623 | 17 623 |
| oraculo_passos_hipotese | 204 337 | 204 337 | 204 763 | 204 304 | 204 304 |
| geracao_grades | 8 313 | 8 313 | 8 313 | 8 313 | 8 313 |
| geracao_rotulos | 382 242 | 382 242 | 382 244 | 382 244 | 382 244 |
| avaliacao_passos | 3 108 | 3 108 | 3 108 | 3 108 | 3 108 |
| **total** | 598 278 269 | 599 193 156 | 572 116 362 | 751 187 886 | 744 844 505 |
| total_aprendiz (cumulativo da escada) | 597 662 643 | 598 577 530 | 571 500 296 | 750 572 294 | 744 228 913 |

Livro-razão inteiro (`razao.json`): 782 lançamentos; total 3 265 620 178; hash do diário `16c362ee2b3e67ed`. `enumeracao_passos` é 99,85 % do total (3 260 878 101). [C]

**Diferenças de custo entre braços não são vantagem.** `total_aprendiz` de L-lib@E0+ é menor que o de L-fix@E0+ (744 228 913 contra 750 572 294; −0,8 %), e o de L-lib+f@E0 é menor que o de L-fix@E0 (571 500 296 contra 597 662 643; −4,4 %). Toda a diferença vem de tarefas não resolvidas, que esgotaram o mesmo orçamento de 10 001 candidatos de enumeração com contagens de passos diferentes. Nas 3 tarefas aceitas, L-lib custou mais que L-fix (+48, +147 e +373 em L-lib@E0 e em L-lib@E0+). As soluções aceitas e as acurácias são idênticas. Não há vantagem de L-lib nestes dados. Mesmo que houvesse, seria só uma observação de viabilidade com dados expostos (documento 03, §0, regra 1). [C]/[F]

Outros contadores determinísticos: N(s, τ) (seção 3.2); candidatos por s_reach (`deterministico.json → fases.3.pm8`); contadores dos geradores (`fases.1.pm2_pm5[*].contadores`: aceitas, rejeitadas por partição, permutações e trocas avaliadas, consultas à tabela exaustiva).

### 5.2 Medições reais (`medicoes.json`, `medicoes.md`; fora do livro-razão)

**Por fase:**

| fase | parede (s) | CPU, processo + filhos (s) | pico do processo principal (KiB) |
|---|---|---|---|
| 1 | 32,5 | 123,7 | 23 508 |
| 2 | 0,3 | 0,3 | 25 996 |
| 3 | 2 116,7 | 6 238,6 | 44 844 |
| 4 | 13,9 | 27,6 | 45 100 |
| 5 | 2,8 | 2,8 | 51 244 |
| 6 | 778,4 | 1 856,6 | 51 244 |
| 7 | 0,0 | 0,0 | 51 244 |
| **soma** | **2 944,7** | **8 249,7** | — |

Somas calculadas sobre os valores não arredondados de `medicoes.json → fases` (parede: 2 944,689 s; a v0.1 somava os valores arredondados e dava 2 944,6). O pico do processo principal não inclui os trabalhadores do Pool. [E]

**Por braço da fase 6** (memória de pico do trecho, num processo novo por job):

| braço | parede (s) | CPU (s) | memória de pico (KiB) | latência máx. do oráculo (s) | latência média (s) |
|---|---|---|---|---|---|
| L-fix@E0 | 289,1 | 284,5 | 582 148 | 0,286 | 0,026 |
| L-lib@E0 | 285,4 | 282,8 | 581 368 | 0,276 | 0,028 |
| L-lib+f@E0 | 269,3 | 266,3 | 572 836 | 0,284 | 0,026 |
| L-fix@E0+ | 510,7 | 505,9 | 662 860 | 0,279 | 0,026 |
| L-lib@E0+ | 509,0 | 505,0 | 662 788 | 0,360 | 0,032 |

**Fase 3:** 84 jobs de enumeração; a vazão e a memória por job estão em `medicoes.md` (PM9). Auditoria OE: de 19,1 s a 123,4 s por tipo. Um job limitado por memória (E0 {g,S}→L Pos, 10⁵, 4 GB, 52 726 candidatos ao parar). [E]

**Fase 1:** PM1 com 4 jobs de 9,4 s a 11,2 s de parede; PM3 em `medicoes.md`. [E]

---

## 6. Falhas e limitações

### 6.1 Falhas medidas nesta execução

- **PM9** falha (83/84 abaixo de 2 000/s), e **I6** disparou (21/84 abaixo de 200/s). Nenhuma otimização foi tentada, e o documento 03 exige isso antes de interromper. [E]/[R]
- **PM16** falha: 7 399 h projetadas contra 2 000 h. [E]/[H]
- **PM11** = 1/3, e **I4** disparou. [C]/[R]
- **PM10**: 8 dos 14 degraus inalcançáveis em E0 e em E0+ a 10⁴. [C]
- Fase 6: 11 das 14 tarefas não foram resolvidas em nenhum braço; nenhuma reutilização. [C]
- PM8: s_reach(10⁵) de E0 {g,S}→L Pos é nulo por limite de memória. [E]

### 6.2 Achados de revisão não corrigidos

1. **4/10 (parte).** Não foram revistos a pontuação nem o limiar do compressor para que `vizPretos` saia de ParAdjacente + NenhumaIsolada. Fazer isso seria ajustar o mecanismo ao alvo conhecido, a mesma forma de vazamento do achado 1. I4 fica registrada como disparada. A revisão do compressor (por exemplo, restringir buracos de tipo funcional) é um problema aberto que precisa ser fixado antes de olhar o alvo. [A]
2. **1 (parte).** A tabela sistemática foi medida só em E0 e E0+, que são as bases dos aprendizes. E0' e E0'+ sistemáticas não foram medidas, e os braços da fase 6 continuam com a tabela curada (desvio declarado). [A]
3. **13/14 (parte).** A poda OE continua inexata em contextos aninhados de nível ≥ 1 (só os primeiros mundos-raiz) e nas tarefas sem Grade. A auditoria mede o efeito (até 12 classes perdidas em 875, em s ≤ 8), mas não o elimina. [C]/[A]
4. **18 (parte).** O s_reach a B_max = 10⁶ não foi medido. I6 está disparada, e nenhuma otimização foi tentada, embora o plano exija isso antes de interromper. [A]

### 6.3 Problemas abertos

Itens transcritos dos relatórios dos módulos, traduzidos quando necessário. Os números são dos módulos, salvo **[nota]**.

**Partições e dados**

1. Capacidade das partições em grades pequenas: em n = 1 as duas grades caem em `reservado_confirmatorio`, e as partições do piloto ficam vazias. Em n = 2, os tamanhos são `oraculo_treino` = 3, validação = 1, `teste_int` = 2, `teste_ext` = 1 e reservado = 9. Em n = 3: 111/58/49/48/246. Em n = 4: 12 988/6 419/6 565/6 543/33 021. O oráculo exaustivo de n de 1 a 4 e o protocolo 2.9 ficam muito limitados para n ≤ 2. [A]
2. ExistePreta sob partição por instância: o único negativo de cada n (a grade vazia) cai numa única partição. Em `oraculo_treino` estão as vazias de n = 3 e n = 7; em `teste_ext`, a de n = 5; em validação, a de n = 6; em `teste_int`, nenhuma de n de 1 a 9. Logo, ExistePreta não tem nenhum negativo em `teste_int`, e em `oraculo_treino` só os tem nos tamanhos 3 e 7. O primeiro degrau da escada precisa de decisão de protocolo. [A] **[nota]** Na v2, o conjunto de teste de ExistePreta tem 29 grades, contra 30 das outras tarefas.
3. `PARTICOES` junta P_oraculo e D_treino em `oraculo_treino` e não tem baldes para D_teste_remap, D_teste_port e D_teste_nat (02, 2.7.1). Falta decidir: de que partição sai D_teste_nat; se uma grade transformada (remap) que cai em outro balde pode ser usada; e se treino e oráculo devem ser separados. [A]
4. PM3 (1 000 pares em ≤ 60 s) não foi verificado para todos os pares (conceito, n), só para 3 conceitos em n = 6. As extrapolações para n = 9 indicam risco para ExisteCompTocaBorda, ExisteCompMin3, ExisteCompReto, PeloMenosDois, MaiorTocaBorda e MaiorCompPeloMenosLinha1 (cerca de 8 a 16 s por 100 pares). Use `tabela_geradores` para a tabela completa de PM2 a PM5. [A] **[nota]** Na v2, PM3 foi projetado para 8 conceitos em n de 3 a 6 (seção 3.1).
5. Em n ≤ 4, a capacidade limita o tamanho dos conjuntos de desenho em várias partições: LinhasIguais em n = 3 dá só 7 pares em `oraculo_treino`, e ExisteCompTocaBorda em n = 4 dá 26 pares. Também em n ≤ 4, ExisteCompTocaBorda é degenerado para emparelhamento em n = 3, e TresComponentes não tem positivos em n = 2. **[nota]** Na v2, LinhasIguais n = 3: 7 pares.
6. Para n ≥ 5, `degenerado()` é heurístico: "não encontrado em k tentativas" não prova impossibilidade, e o campo `motivo` diz isso.
7. PQ3 (frequências naturais contra `analysis/audit_frequencias_saida.md`, PM6) não foi implementado no módulo de geradores; só U6 compara a frequência exata com Monte Carlo. **[nota]** Na v2, PM6 foi implementado em `piloto.py` (fase 1; 256 comparações).
8. `memoria_pico_kb` é o `ru_maxrss` do processo inteiro (o pico desde o início), não o pico do trecho medido. Medir por trecho exigiria um subprocesso ou tracemalloc. **[nota]** `medicoes.json` da v2 mede por trecho em processo novo; `razao.json → medicoes` não.
9. Os geradores ainda não aplicam por si a regra "semente confirmatória ≥ 20 000": `rng_piloto` e `rng_confirmatorio` verificam os intervalos, mas as funções recebem um `random.Random` já criado. A partição confirmatória exige `permitir_confirmatorio=True` em todas as funções.
10. Degeneração em partições pequenas: `oraculo_treino` tem 0 grades em n = 1, 3 em n = 2 e 111 em n = 3. Para ExistePreta não existe nenhum negativo na partição em n ≤ 6 (a grade vazia fica fora dos baldes, ou sem par), e portanto o oráculo nunca pode mostrar um negativo de ExistePreta. Isso é propriedade da partição por hash, não do oráculo, e deve ser reportado. **[nota]** O exemplo inicial da v2 usa a grade vazia de n = 3, de `oraculo_treino`, como negativo natural sem par. A frase "nenhum negativo na partição" vale para conjuntos emparelhados, não para negativos naturais.

**Linguagem, avaliador e tradutores**

11. Os programas da escada em E0' são limites superiores, não mínimos (`passo` 39, PrimeiraUltimaIguais 46, LinhasIguais 42). A regra GO do documento 03, seção 10, exige E0 e E0'. Antes de medir PQ7 em E0', alguém precisa minimizar à mão a escada E0', ou a diferença de tamanho tem de ser aceita como resultado. [A]
12. Custo de avaliação: o mesmo conceito custa cerca de 30 vezes mais passos em E0' do que em E0 (UmComponente numa grade 6×6: 248 mil contra 8,5 mil passos), porque `pertence`/`uniao`/`diferenca` viram dobras. Isso afeta `avaliacao_passos` e a vazão do enumerador em E0' (PM9, I6).
13. Não está definido como o livro-razão conta passos de avaliação quando há constantes de biblioteca (ver D7). Opções: contar na forma com inline e sem β, ou aceitar a diferença e reportá-la. [A]
14. PM7 (contagem N(s, τ)) e o enumerador não estavam implementados no módulo de linguagem. `UNIVERSO_TIPOS` inclui os tipos das tarefas da escada (`TIPOS_TAREFA`), não só os tipos das assinaturas, porque Grade → Bool não é subtipo de nenhuma assinatura. **[nota]** Na v2, PM7 e o enumerador estão implementados (seções 3.2 e 3.3).
15. `Lteto` foi acrescentado aos valores de proveniência permitidos (conceito fornecido) para uso futuro. A tabela L-teto em si (`componentes`, `mesmoNumero` como primitivas) não foi construída.
16. U16/U17 usam uma amostra determinística de combinações de argumentos: 12 por grade para primitivas com argumento Grade, em todas as 530 grades com n ≤ 3, e até 400 por grade em 50 grades fixas para primitivas sem argumento Grade. Faltam a verificação exaustiva até n = 4 (02, 2.3.4) e as provas por primitiva. [A]
17. O avaliador roda a cerca de 0,36 µs por passo em Python puro. Compila termos em fechamentos e usa ambientes em dicionário (`lru_cache` de 8 192 em `compilar`). Se 2 000 candidatos/s são atingíveis depende do enumerador.
18. Recursão: `sys.setrecursionlimit(200000)`. Foi testada até recursão sobre uma lista de comprimento F(4) = 256 e nos casos 6×6. Em n = 9, com listas de comprimento 6 561 recursando por fix, a pilha C pode exigir uma thread com pilha maior; não testado.
19. `referencias.py` aparece como modificado no `git status`, mas a modificação não foi feita pelo módulo de linguagem, e sim por outro agente (ver seção 2.2, item 3). O módulo de linguagem não editou `grade.py`, `referencias.py` nem `geradores.py`.

**Enumerador**

20. Acelerar o fix funcional em `avaliador.py` (detecção de ciclo, ou memo por nível quando rec é chamado com o mesmo argumento) eliminaria cerca de 80 % do tempo do enumerador. Isso exige mexer em outro módulo e não foi feito.
21. Reduzir a memória: guardar só um hash das assinaturas de tipos funcionais e verificar por recomputação quando houver colisão; recalcular os fechos sob demanda; reaproveitar valores repetidos (em s = 8 há 255 mil valores base e só 8 275 distintos). Pela projeção linear, 10⁶ candidatos precisariam de cerca de 15 GB. Além disso, `grades_amostra_oe` aciona o cache `_dominio(4)` de geradores (65 536 grades, cerca de 30 MB). [H]
22. Otimização ainda não implementada: reaproveitar nos contextos-filho os termos que não mencionam a variável nova, em vez de reavaliá-los.
23. s_reach(10⁶) não foi medido. Extrapolação: o custo cumulativo cresce cerca de 3 vezes por tamanho, o que daria s_reach(10⁶) ≈ 11 em `{g} ⊢ Bool` e ≈ 12 em `Grade → Bool` fechado. Com a vazão atual, isso levaria de 1 a 2 h por contexto. [H]
24. A validação V2 só cobre até s ≤ 7 (Bool) e s ≤ 6 (L Pos). A não-congruência na fronteira entre níveis e a poda dentro de corpos de fix podem perder classes em tamanhos maiores. **[nota]** A auditoria OE da v2 mostra perdas em s = 7 e 8 (seção 3.3).
25. Hiperparâmetros a congelar no piloto: amostra de 36 mundos (3 de n = 2, 23 de n = 3 estratificados por contagem de pretas, 10 de n = 4), `mundos_funcao=(8,3)`, `M_RAPIDA=4`, limites de amostras de lista (11/6) e de função (3), `orcamento_passos_mundo=10_000` e D = 2. Reduzir os mundos de n = 4 de 10 para 4 perdeu 8 de 178 classes em s ≤ 8. **[nota]** v2: `oe:grades_amostra_oe` = 36 grades, hash `bd3ff55fee8ae23f`.
26. A limitação da partição também afeta os aprendizes: algumas classes não são separáveis por nenhuma amostra admissível de `oraculo_treino` com n ≤ 4.
27. Cabe ao `razao.py` decidir se o custo interno da poda (`enumeracao_*`) entra no custo da tarefa, e se as tabelas do enumerador são compartilhadas e amortizadas entre tarefas. Hoje cada `EstadoBusca` tem o seu próprio `Enumerador`. **[nota]** Na v2, `enumeracao_*` entra em `total_aprendiz` e no total.
28. Fix de primeira ordem foi excluído, como a tarefa pede. Ele poderia encurtar programas iterativos, por exemplo um `componenteDe` via `fix (λS. uniao (cons p vazio) (passo g S))`. A inclusão é uma decisão a tomar antes do pré-registro. [A]
29. Programas brutos com três binders aninhados (λg, λq e o fix de `fecho`) exigem `profundidade_lambda=3`, com custo maior, ou o uso da biblioteca.

**Biblioteca**

30. **PH8 / PM11 (afeta o critério de interrupção I4).** `vizPretos` é extraído como fragmento (U21 passa), mas não é o de maior pontuação. Em ParAdjacente + NenhumaIsolada, o fragmento do topo é o quantificador de ordem superior `λf g. f (λp. nao (vazia? (filtrar (celula g) (vizinhos g p)))) (pretas g)`, com pontuação 13, contra 7 de `vizPretos`. A compressão gulosa acrescenta esse primeiro, e depois disso `vizPretos` não se repete mais. Sobre a escada manual inteira, a compressão gulosa (limiar 6) produz: `noMaximo` (argumentos trocados), `passo` (argumentos trocados, (S, g)), `fecho`, `pretasDe` (forma η), `mesmoNumero`, `componenteDe`. Não produz `vizPretos` como entrada separada. O documento 03 diz "extrai `vizPretos`". É preciso decidir antes do congelamento: basta que `vizPretos` apareça entre os fragmentos, ou ele tem de entrar na biblioteca? Disso depende se a pontuação ou a política gulosa precisam mudar. [A] **[nota]** Confirmado na v2: posição 4 no ranking, pontuação 7 contra 13 (seção 3.5).
31. A ordem de parâmetros "por ordem de ocorrência" produz entradas com argumentos permutados em relação aos programas manuais: `passo` sai como λS g em vez de λg S, e `noMaximo` sai invertido. A comparação PH8/PM11 tem de aceitar igualdade a menos de permutação de argumentos. Esse critério foi usado no teste da escada inteira e deve constar do pré-registro.
32. U22, `noMaximo` a partir de só duas tarefas: a generalização menos geral (lgg) de NoMax_linha1_linhaN e NoMax_col1_colN é mais específica que `noMaximo`. É a tarefa inteira com um buraco em `linhas`/`colunas`, pontuação 28. Por isso, nesse teste, `noMaximo` não sai nem com 1 buraco nem com 2. Sai quando `noMaximo`, `mesmoNumero`, PrimeiraUltimaIguais e LinhasIguais são comprimidos juntos. U22 é satisfeito por `descartar` (fechado e exato).
33. A proveniência `descoberta` de uma `Solucao` é declarativa: o código ainda pode embrulhar um termo manual como `Solucao(..., 'descoberta')`. Os módulos enumerador e aprendizes deveriam ser os únicos lugares que constroem objetos `Solucao('descoberta')`, de preferência com um token de execução. O caminho positivo do modo autônomo (acrescentar entradas, contar reutilizações) não foi testado com soluções reais no módulo: não havia enumerador, e rotular programas manuais como `descoberta` num teste quebraria a regra. **[nota]** Na v2 o caminho positivo foi exercido na fase 6 com certificados (`certificados.py`). Inserção: sim. Reutilização: não ocorreu.
34. Custo da extração: a anti-unificação é quadrática nos subtermos que compartilham uma assinatura de raiz. Na escada manual inteira (347 nós), leva cerca de 0,03 s. Para corpora grandes em L-lib existe `max_pares` (corte determinístico, com contagem dos pares omitidos). O seu valor tem de ser fixado no piloto.
35. O limiar de `comprimir()` é um hiperparâmetro a congelar no piloto. O teste usou 7 e 6; não há valor padrão. **[nota]** v2: `limiar` = 3 (fase 6), `limiar_mecanismo` = 5 (fase 5).

**Oráculo**

36. PM13/I3: a latência é dominada pela avaliação de h, não pelo oráculo (de 0,13 a 0,18 s de sobrecarga numa varredura completa de cerca de 14 300 grades de n ≤ 4 na partição `oraculo_treino`). Com h da DSL baseada em `fecho` (UmComponente via fix e tabela de referência), uma rodada sem contraexemplo levou 20,7 s, acima do limiar de interrupção de 10 s. NenhumaIsolada levou 2,5 s, perto do limite PM13 de 2 s. É preciso decidir antes da fase 5: avaliador mais rápido, cache de avaliação, varredura de n = 4 limitada, ou aceitar que o custo do ambiente cresce com o custo de h. [A] **[nota]** Na v2 nenhuma hipótese desse tamanho chegou ao oráculo; latência máxima de 0,360 s.
37. Hipótese que não termina dentro do orçamento: a grade é pulada e registrada (`RegistroConsulta.indefinidas`, `ContadorOraculo.h_indefinido`). Se h estiver indefinida em todas as grades que discordam, o oráculo devolve `None`. O laço dialético (`aprendizes.py`) deve tratar uma h com indefinições como não aceita, ou exigir zero indefinições para aceitar. **[nota]** A v2 trata a indefinição como discordância (seção 2.1, item 10).
38. A minimalidade com o critério padrão vale na ordem com os degenerados adiados, não na ordem pura (n, pretas, lexicográfica) do documento 02. É preciso escolher entre `'sem_par'` (padrão, segue a instrução da tarefa) e `'nenhum'` (literal ao documento 02), e registrar a escolha no pré-registro. [A]
39. A busca local é de uma única troca, com orçamento fixo; não há passeio de várias trocas. Os reservatórios não incluem as grades extremas (vazia, cheia), a não ser que o gerador as produza.
40. O teste U23 depende de `enumerador.enumerar_sem_poda`, de outro módulo. Mudanças de assinatura ou da ordem de enumeração alteram a amostra de h (o resultado continua verificável).

**Adaptadores**

41. `padrao(Grade, n)` do avaliador continua a ser uma grade vazia. Um termo com fix ou `cabeca` do tipo Grade, avaliado num portador, receberia uma Grade, e as primitivas do adaptador levantariam `TypeError` (caso não exercitado pela escada). O critério (ii) de não-vazamento de 2.11.1 (complexidade de definição não maior que nas grades) está documentado, mas não é verificado mecanicamente.

**Execução e decisão**

42. Decisão NO-GO nesta escala, em todos os braços: nenhuma abstração descoberta foi reutilizada em solução aceita posterior. [C]
43. Inconsistência do protocolo: a escada (2.8.1) supõe que as soluções de tarefas de função viram constantes, mas a compressão por recorrência não faz isso. Com a regra literal, L-lib só extrai fragmentos repetidos entre soluções, e nesta execução extraiu apenas `λg. filtrar@P (celula g)`. Falta decidir se a promoção de soluções entra no protocolo. [A]
44. Mesmo na variante L-lib+f, ParAdjacente com `vizPretos` tem tamanho 10. Isso fica fora do s_reach fechado de Grade → Bool a 10⁴ (que é 8) e dentro do s_reach em contexto a 10⁵ (9 + 1 = 10). Um teste dirigido com B ≈ 10⁵ em L-lib+f e L-fix nas 4 primeiras tarefas da F2 é o próximo passo natural (cerca de 25 min de CPU, memória de 2 a 4 GB). Não foi rodado por causa do orçamento. [H]
45. Vazão do enumerador: de 77 a 1 006 candidatos/s, abaixo do limiar de 2 000/s do PM9. Alguns contextos (E0' e E0+ em listas) ficam abaixo de 200/s, na faixa da interrupção I6. Na prática, 10⁶ candidatos por contexto é inviável em Python puro: horas e mais de 8 GB em E0+. **[nota]** v2: de 56 a 2 899/s (seção 3.3).
46. A memória do enumerador a 10⁵ já chega a 4–8 GB, contra a estimativa de menos de 4 GB a 10⁶ (documento 03, seção 8). **[nota]** v2: pico de 4 026 792 KiB no job limitado a 4 GB.
47. E0'+ sem s_reach medido; a condição "vale em E0+ e E0'+" não foi verificada. **[nota]** Na v2, E0'+ tem s_reach a 10⁴, e a condição foi avaliada a esse B (falha: seção 7).
48. Os tamanhos manuais em E0' são grandes (`vizPretos` 17, `passo` 39, PrimeiraUltimaIguais 46), porque as versões E0' são β-segura∘τ, só limites superiores. PM10 em E0' fica pessimista até haver programas mínimos em E0'. [A]
49. NenhumaIsolada: o programa do documento discorda da referência na grade vazia (discrepância já documentada em `programas_referencia`).
50. PM3 (≥ 1 000 pares em ≤ 60 s) foi só projetado a partir de 100 pares. A capacidade de n = 3 em `oraculo_treino` limita os pares (LinhasIguais tem só 7).
51. A medição de memória por trabalhador (`ru_maxrss`) acumula jobs anteriores do mesmo trabalhador do Pool e não isola o pico por medição. **[nota]** Na v2, cada job roda num processo novo (`maxtasksperchild=1`) com VmHWM reiniciado (escopo `trecho`).

### 6.4 Achados da revisão crítica deste relatório (não corrigidos no código)

1. **O teste de ExistePreta não tem negativos.** As 29 grades de `teste_int` (n de 4 a 6, amostragem natural) são todas positivas, e o predicado constante `verdadeiro` teria acurácia 1,000. Reconstrução: `aprendizes.Ambiente(10001, k_reservatorio=40, ns_reservatorio=(5, 6), num_teste=30).preparar(TAREFAS_POR_ID['ExistePreta']).teste` dá 29 rótulos verdadeiros. Isso é coerente com o item 2 da seção 6.3 (`teste_int` não contém nenhuma grade vazia). O oráculo também nunca mostrou contraexemplo nessa tarefa (aceita na rodada 1). O protocolo precisa decidir: teste com negativos, ou ExistePreta fora da avaliação por acurácia. [C]/[A]
2. **Negativos repetidos nos conjuntos de desenho** de n = 3 e 4 (seção 3.1). PM4 e M10 não detectam a repetição. [C]/[A]
3. **Dependência entre degraus em PM10** (seção 3.4). A regra do §10 avalia cada degrau com os anteriores manuais e não exige que os anteriores sejam alcançáveis. Lida em cadeia, a escada alcançável a 10⁴ fica em 3 de 14 degraus em E0 e em E0+. [C]/[A]
4. **I2 não avaliada.** PM5 é impossível para ExistePreta [P], e PM3 não foi medido no limiar. Pela letra de I2, depois de revisão ExistePreta teria de ser retirado ou redefinido. [A]
5. **I4 e I6 sem a pré-condição.** O §9 exige revisão (I4) e otimização (I6) antes da interrupção. Nenhuma das duas foi feita, mas os registros marcam I4 como disparada sem ressalva, e I6 como disparada com nota. As duas condições foram observadas; a interrupção formal está pendente. [R]/[A]
6. **I5 não está nos registros.** A conclusão "não disparada" é inferência: s_reach(10⁴, `Grade → Bool`) = 8 e s_reach não decresce com B. [F]
7. **PM15 não cobre a fase 3.** A segunda execução reaproveitou o s_reach; as fases 4 e 7 comparadas dependem desse valor. O determinismo de s_reach e da vazão (PM9) não foi testado. [C]
8. **Verificação dos programas manuais.** As 3 discordâncias documentadas de E0'+ são a mesma grade vazia de n = 3, sorteada 3 vezes. A amostra de E0' (47 grades) não contém grade sem pretas, e por isso a discrepância de NenhumaIsolada não foi exercida em E0'. Reconstrução: `piloto._grades_verificacao(ConfigPiloto(), base)`. [C]
9. **Saída da suíte de testes não arquivada** em `runs/`. O tempo de 481,6 s não pode ser conferido pelos registros. [A]
10. **Contradição na v0.1.** A v0.1 explicava as falhas de `componenteDe`, `noMaximo` e `mesmoNumero` por re-enumerações OE; os registros mostram `refinamentos_oe` = 0 nessas tarefas (seção 3.6). A v0.1 também dizia que a condição autônoma "não depende de B", mas as 11 falhas são por orçamento (seção 7). [C]

---

## 7. Decisão GO / E0+ / NO-GO

**Regra aplicada** (documento 03, §10, com B único = 10⁴ no lugar de B_max = 10⁶, mais a exigência autônoma por base; `piloto.decidir`):

- **GO com E0:** todo degrau alcançável (PM10) em E0 **e** em E0', **e**, em L-lib@E0, ≥ 1 tarefa aceita com reutilização de uma abstração descoberta que L-fix@E0 não resolve a custo total igual.
- **GO com E0+:** falha em E0 só em `fecho` e/ou `descartar`; todo degrau alcançável em E0+ **e** em E0'+; **e** a mesma exigência autônoma em L-lib@E0+ contra L-fix@E0+.
- **NO-GO:** nos demais casos.

A exigência autônoma é acréscimo da implementação; o §10 decide só pela tabela PM10, a B_max = 10⁶.

**Aplicação, número a número** (seção 3.4; `deterministico.json → fases.7`):

1. **E0, alcance:** falha. 8 degraus têm tamanho comparado acima de s_reach: ParAdjacente 9 > 7; NenhumaIsolada 14 > 7; `passo` 7 > 6; `fecho` 16 > 8; UmComponente 16 > 7; `descartar` 13 > 7; PrimeiraUltimaIguais 12 > 7; LinhasIguais 13 > 7. [C]
2. **E0', alcance:** falha em 10 degraus (`vizPretos`, ParAdjacente, NenhumaIsolada, `passo`, `fecho`, UmComponente, `pretasDe`, `descartar`, PrimeiraUltimaIguais, LinhasIguais). Os tamanhos de E0' são limites superiores (seção 2.2, item 20). [C]
3. **Condição "só laços falham em E0":** falsa. As falhas de E0 incluem 6 degraus além de `fecho` e `descartar`. [C]
4. **E0+, alcance:** falha em 8 degraus: ParAdjacente 9 > 7; NenhumaIsolada 14 > 7; `passo` 7 > 6; UmComponente 16 > 7; `descartar` 9 > 7; `mesmoNumero` 9 > 8; PrimeiraUltimaIguais 12 > 7; LinhasIguais 13 > 7. `fecho` passa (4 ≤ 8). [C]
5. **E0'+, alcance:** falha em 9 degraus (`vizPretos`, ParAdjacente, NenhumaIsolada, `passo`, UmComponente, `pretasDe`, `descartar`, PrimeiraUltimaIguais, LinhasIguais). [C]
6. **Exigência autônoma:** E0, falsa; E0+, falsa. Há 0 tarefas aceitas com reutilização em qualquer braço (`reutilizacoes_em_solucoes_aceitas` = []). As abstrações descobertas são cópias (α/η) de soluções de degraus (`descobertas_nao_copia_de_solucao` vazio em todos os braços). E0': não verificada (sem braço). [C]
7. **Interrupções:** Condição de I4 observada (PM11 = 1/3), mas sem a revisão do compressor que o §9 exige ("após revisão"; seção 6.2, item 1). Os registros marcam I4 como disparada. Condição de I6 observada (21/84 < 200/s), mas sem a otimização exigida ("após otimização"). I1 (referências, livro-razão) não disparada. I7 não disparada (0 grades no confirmatório). I3 não disparada (0,360 s < 10 s). I5 não disparada por inferência: não há campo nos registros, e s_reach(10⁴, Grade → Bool) = 8. I2 não avaliada: PM5 é impossível para ExistePreta [P], e PM3 não foi medido no limiar. [C]/[E]/[R]
8. **Custo:** PM16 = 7 399 h > 2 000 h. [E]/[H]

**Decisão: NO-GO a B = 10⁴.** Decisão conservadora (menor s_reach medido): NO-GO; em E0, `mesmoNumero` passa a falhar também (9 > 8). Decisão se a variante L-lib+f contasse: NO-GO. Só pela tabela PM10, sem a exigência autônoma, também dá NO-GO a 10⁴, porque o alcance falha em E0 e em E0+. [C]

A B_max = 10⁶ a regra literal não pode ser aplicada, porque s_reach(10⁶) não foi medido. A extrapolação do item 23 da seção 6.3 (s_reach(10⁶) ≈ 11 em {g} ⊢ Bool) ainda deixaria NenhumaIsolada (14), UmComponente (16), LinhasIguais (13) e PrimeiraUltimaIguais (12) acima do alcance, em E0 e em E0+. [H]

**Alcance da decisão.** Ela foi tomada a B = 10⁴, com escala reduzida, D = 2 nos aprendizes, tabela curada nos braços e programas manuais como limites superiores de tamanho. Um NO-GO por alcance a 10⁴ não implica NO-GO a 10⁶ (seção 2.1, item 2). A condição autônoma também depende do orçamento. As 11 tarefas não resolvidas terminaram por `orcamento_enumeracao` com B_tarefa = 10⁴, e nenhuma abstração que não fosse cópia de solução foi descoberta ou reutilizada. Não se sabe o que aconteceria com B maior. [F]

**Aceitação do piloto** (documento 03, §10): não atingida. Faltam: PM11 = 100 %; PM3 medido no limiar; PM2 a PM5 com ≥ 1 000 pares; PM5 em ExistePreta (impossível, [P]); PM1 e U3 com 10⁵ amostras por n de 5 a 9; PM15 sobre todas as fases. Pelo §9, as condições de I4 e I6 também exigem revisão documentada antes de retomar. [C]

Pela regra de NO-GO, o experimento 1 é redesenhado (busca guiada, tarefas de função mais finas, outra decomposição) e volta ao piloto. Os itens [A] das seções 6.2 e 6.3 são decisões a tomar antes disso. [A]

---

## 8. O que este piloto NÃO mostra

- **Nenhuma evidência para H-B1**, nem a favor nem contra. Os dados e os hiperparâmetros estão expostos, as instâncias de conceito foram usadas em ajuste, e não houve reutilização de abstração. A frase do documento 03, §11 ("o mecanismo funciona nos dados do piloto") não se aplica: L-lib não superou L-fix, e os dois aceitaram as mesmas 3 tarefas com as mesmas hipóteses. [F]
- **Sucesso sintático não é sucesso científico.** As 3 tarefas aceitas têm hipóteses iguais aos programas manuais (`pretasDe` a menos de η), de tamanho 4 a 8. A busca usou a tabela curada, cujas instâncias foram escolhidas a partir desses mesmos programas (seção 2.1, item 4). A acurácia de teste é 1,000, mas o teste de ExistePreta não tem negativos (seção 6.4, item 1). Isso só mostra que o laço enumerador–oráculo termina e aceita em tarefas cujo programa cabe no alcance a 10⁴. Não mostra aprendizagem de conceitos, generalização fora da partição nem composicionalidade. [F]
- A abstração "descoberta" em L-lib (`λg1. filtrar@P (celula g1)`) ocorre nas soluções de `vizPretos` e `pretasDe`, mas é igual (α/η) à solução inteira de `pretasDe`. Não abstrai nada além de uma solução já aceita, e não foi reutilizada. Não é evidência de descoberta de abstração. [C]/[F]
- A fase 5 usa soluções **manuais** (`manual-teste`): mostra propriedades do compressor, não descoberta. O único sucesso de PM11 (`passo`) vem de repetição dentro de um único programa manual. [F]
- PM10 e o alcance sintático usam programas manuais como limites superiores. "Alcançável" é uma afirmação sobre o tamanho de um programa escrito à mão, não sobre o que o aprendiz encontra. A fase 6 mostra a distância: foram resolvidos os 3 degraus alcançáveis em cadeia, e não foram resolvidos os 3 que só são alcançáveis com anteriores inalcançáveis. [F]
- As diferenças de `total_aprendiz` entre L-lib e L-fix vêm só de tarefas não resolvidas (seção 5.1), e não são vantagem de L-lib. [C]/[F]
- O NO-GO não mostra que a escada seja inalcançável a 10⁶, nem em outra linguagem de implementação, nem com outra política de compressão. [H]
- Nada sobre transferência (adaptadores só testados unitariamente), controles neurais (não implementados), L-mem (não implementado), L2 ou inteligência geral (documento 03, §11).
- As medições de tempo e memória valem para esta máquina e esta implementação em Python puro. PM16 é uma projeção linear sobre K e custo por candidato medidos a B = 10⁴. [E]/[H]
