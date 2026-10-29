# Plano do piloto — Experimento 1

## Documento 03 — Implementação mínima e exploratória, critérios de aceitação e condições de interrupção

**Status:** v0.1 (2026-10-29). Especificação do piloto. O piloto ainda não foi implementado nem executado. Depende de `docs/02-protocolo-experimental.md` v0.2.

**Rótulos epistêmicos:** [P] prova formal; [E] evidência empírica; [C] resultado computacional; [F] interpretação filosófica; [H] hipótese; [R] condição de refutação; [A] questão aberta.

### Sumário

0. Finalidade e regras do piloto
1. Perguntas do piloto e hipóteses de viabilidade
2. Definições
3. Arquitetura mínima
4. Métricas do piloto e limiares
5. Testes unitários
6. Dados do piloto e separação do confirmatório
7. Procedimento por fases
8. Estimativa de recursos
9. Condições de interrupção
10. Critérios de aceitação e decisão
11. O que o piloto não pode concluir
12. Entregáveis

---

## 0. Finalidade e regras do piloto

**Finalidade.** O piloto existe para responder perguntas de **viabilidade e calibração** do experimento 1 (documento 02, seção 2): se os geradores produzem o que o protocolo exige; se o enumerador alcança os tamanhos de programa que a escada de currículo precisa; se o mecanismo de compressão extrai as abstrações pretendidas quando as soluções estão disponíveis; se o oráculo encontra contraexemplos mínimos em tempo útil; quanto custa cada parte. Ele produz os números que o pré-registro confirmatório precisa (orçamento B, rodadas K, hiperparâmetro de compressão, faixas de tamanho para a família F4, custo projetado) e uma decisão GO / E0+ / NO-GO.

**Regras.**

1. **Nenhuma alegação científica sai do piloto.** Um aprendiz com biblioteca que vença um aprendiz sem biblioteca no piloto é uma observação sobre viabilidade com dados e hiperparâmetros expostos. Não é evidência para H-B1 e não será descrito como tal. Um resultado positivo isolado, no piloto ou no confirmatório, não demonstra a hipótese.
2. **Dados próprios.** O piloto usa sementes, grades e instâncias de conceito separadas das reservadas ao confirmatório (seção 6). Tudo o que o piloto expõe é marcado e excluído do desfecho primário confirmatório.
3. **O que pode passar do piloto ao confirmatório:** hiperparâmetros congelados; a escolha E0 ou E0+; a escada de currículo validada; faixas de tamanho para F4; o modelo de custo; o código testado. **O que não pode passar:** grades, sementes, instâncias de conceito usadas em ajuste, e qualquer leitura de desempenho como resultado.
4. **Sem implementar o experimento completo.** O piloto não executa a bateria de controles nem as famílias por esquema inteiras. Executa o mínimo que responde às perguntas da seção 1.
5. **Reprodutibilidade.** Tudo determinístico por semente; todo número reportado vem de um comando registrado.

---

## 1. Perguntas do piloto e hipóteses de viabilidade

Cada pergunta tem uma hipótese de viabilidade (PH), um limiar, e a decisão que o resultado dispara. Nenhuma PH é hipótese científica.

| # | Pergunta | Hipótese de viabilidade | Limiar de aceitação | Se falha |
|---|---|---|---|---|
| PQ1 | As duas implementações de referência de cada conceito concordam? | PH1: concordam | Exaustivo para n de 1 a 4; 10⁵ amostras por n de 5 a 9; zero discordâncias | Interrupção I1 |
| PQ2 | Os geradores produzem conjuntos de desenho válidos? | PH2: produzem | Por (conceito, n): ≥ 1 000 pares positivo/negativo em ≤ 60 s; 100% dos rótulos confirmados pelas duas referências; negativos com o mesmo número de pretas; M10 ≤ 0,55 | Revisão do gerador; se persistir, interrupção I2 |
| PQ3 | As frequências naturais calculadas coincidem com as do script de auditoria? | PH3: coincidem | Dentro de 3 desvios-padrão de Monte Carlo | Interrupção I1 (erro de referência ou de gerador) |
| PQ4 | O avaliador implementa Sem_n (combustível, truncamento) e os tradutores E0 ↔ E0' preservam a semântica? | PH4: sim | Testes U9, U13 passam; para cada primitiva, igualdade em todas as grades de n até 3 e numa bateria fixa de argumentos funcionais | Interrupção I1 |
| PQ5 | Quantos termos bem tipados existem por tamanho e tipo? | PH5: crescimento exponencial com base entre 6 e 12 por folha | Contagem exata por programação dinâmica até tamanho 12 para cinco contextos de tipo | Nenhuma falha possível; alimenta o modelo de custo |
| PQ6 | Que tamanho o enumerador alcança por contexto de tipo e orçamento? | PH6: s_reach(10⁶) entre 9 e 12 em `Grade → Bool`; menor em contextos com dois argumentos de lista **[H]** | Medido, não aceito ou rejeitado | Alimenta PQ7 |
| PQ7 | Os degraus da escada são alcançáveis? | PH7: os degraus de 13 (`descartar`) e 16 (`fecho`) **não** são alcançáveis em E0 por enumeração pura a 10⁶; são em E0+ **[H]** | Para cada degrau: tamanho com as abstrações anteriores ≤ s_reach(B_max) no contexto de tipo do degrau | Regra de decisão da seção 10 |
| PQ8 | O compressor extrai as abstrações pretendidas a partir de soluções conhecidas? | PH8: extrai `vizPretos`, `passo`, `pretasDe` | Fragmento extraído comportamentalmente igual à abstração pretendida em todas as grades do piloto de n até 6 | Revisão do compressor; se persistir, interrupção I4 |
| PQ9 | O oráculo encontra contraexemplos mínimos em tempo útil? | PH9: sim para n até 4 exaustivo; reservatório para 5 e 6 | Minimalidade igual à força bruta em 50 pares (h, c) com n até 4; latência ≤ 2 s por rodada | Otimização; se persistir, interrupção I3 |
| PQ10 | O livro-razão fecha e é independente da linguagem? | PH10: sim | Soma das partes igual ao total; um candidato avaliado conta um em qualquer base; duas execuções com a mesma semente dão livros idênticos | Interrupção I1 |
| PQ11 | Uma execução seca de L-fix e L-lib na escada termina e produz curvas de custo legíveis? | PH11: sim | Termina em ≤ 12 h de CPU; distribuição de rodadas K observada; curvas de aceitação por custo cumulativo geradas | Ajuste de B e K |
| PQ12 | O custo projetado do confirmatório cabe no orçamento? | PH12: ≤ 2 000 horas de CPU | Projeção pelo modelo de custo (seção 8) | Redução de famílias ou de sementes, decidida antes do pré-registro |

---

## 2. Definições

### 2.1 Dados

- **Grade** de tamanho n: tupla de n² bits em ordem linha a linha; serialização canônica `n:bits`; hash SHA-256 da serialização.
- **Pos**: par (i, j) com 1 ≤ i, j ≤ n.
- **Conceito**: identificador, definição formal em texto, duas implementações de referência (`ref_a`, `ref_b`), gerador construtivo, lista de invariâncias declaradas, esquema de origem, marca "exposto no piloto".
- **Tarefa**: predicado (`Grade → Bool`) ou função (tipos da escada), com conjuntos de exemplos e um ponteiro para o oráculo.

### 2.2 Linguagem e semântica

Como no documento 02, 2.3: cálculo lambda simplesmente tipado com constantes; tamanho = folhas mais abstrações; Sem_n com F(n) = n⁴, listas truncadas em F(n), `fix f = f^{F(n)}(padrão)`. E0 com 29 primitivas; E0' com 20; E0+ e E0'+ com `ateFixo` e `dobraR` acrescentados (documento 02, 2.8.3). As tabelas de tipos das primitivas são parte do pré-registro e do código.

### 2.3 Custo

- **Candidato avaliado**: um termo fechado do tipo da tarefa submetido à avaliação sobre os exemplos correntes. Conta um, em qualquer base.
- **Passos de avaliação**: passos da semântica operacional somados sobre os exemplos.
- **Livro-razão**: por tarefa e por aprendiz, campos `busca_candidatos`, `busca_passos`, `compressao_passos`, `oraculo_consultas`, `oraculo_custo_ambiente`, `avaliacao_passos`, `total`.

### 2.4 Alcance do enumerador

s_reach(B, τ) = maior tamanho s tal que o enumerador, com poda por tipo e por equivalência observacional, enumera todas as classes de equivalência observacional de termos de tipo τ e tamanho ≤ s dentro de B candidatos avaliados. Medido por contexto de tipo τ.

---

## 3. Arquitetura mínima

Python 3.11 ou superior, sem dependências obrigatórias (`numpy` opcional para acelerar geração). Um pacote `fedro_piloto/` com os módulos abaixo. A estimativa de linhas é indicativa.

| Módulo | Responsabilidade | Linhas |
|---|---|---|
| `grade.py` | Tipos Grade e Pos; serialização; hash; vizinhança; transformações (rotações, reflexões, transposição, remapeamento de cores) | 150 |
| `referencias.py` | `ref_a` (busca em largura explícita) e `ref_b` (formulação declarativa independente, por exemplo união-busca ou verificação por fecho de conjuntos) para cada conceito e predicado auxiliar (componentes, cardinalidades) | 300 |
| `geradores.py` | Amostragem natural; geradores construtivos por esquema; negativos emparelhados por permutação e por trocas; busca local de quase-acerto; classificador por densidade (M10) | 350 |
| `dsl.py` | Tipos, termos, tabelas de primitivas de E0, E0', E0+, E0'+; tamanho; impressão canônica | 250 |
| `avaliador.py` | Sem_n: avaliação com contagem de passos, combustível e truncamento; valores padrão por tipo | 250 |
| `tradutores.py` | τ: E0 → E0' e τ': E0' → E0 como homomorfismos; `inline` de entradas de biblioteca; verificação do lema de inlining (tamanho e semântica) | 200 |
| `enumerador.py` | Enumeração ascendente por tamanho e tipo; poda por equivalência observacional sobre uma amostra fixa de entradas; contagem exata de termos por tamanho e tipo (programação dinâmica, sem avaliar) | 350 |
| `biblioteca.py` | Extração de fragmentos: contagem de subtermos fechados recorrentes de tamanho ≥ 3 nas soluções aceitas; anti-unificação com até dois buracos; pontuação (ocorrências − 1) × (tamanho − 1); inserção como constante nomeada; registro de custo | 300 |
| `oraculo.py` | Rótulo; contraexemplo mínimo (exaustivo n ≤ 4; reservatório n = 5, 6; busca local por trocas); ordem (n, pretas, lexicográfica); registro de consultas | 200 |
| `aprendizes.py` | L-mem, L-fix, L-lib; laço dialético com K rodadas; integração com o livro-razão | 250 |
| `razao.py` | Livro-razão; verificação de fechamento; serialização | 100 |
| `adaptadores.py` | Portadores sequência e grafo para as primitivas de carrier (só para os testes U18; a transferência em si não é executada no piloto) | 120 |
| `piloto.py` | Orquestração das fases; relatório em Markdown com tabelas; hashes dos conjuntos | 250 |
| `tests/` | Testes unitários da seção 5 | 600 |

Total indicativo: 2 500 a 3 500 linhas. Os aprendizes neurais **não** fazem parte do piloto.

---

## 4. Métricas do piloto e limiares

| Métrica | Definição | Limiar ou uso |
|---|---|---|
| PM1 concordância de referências | Discordâncias entre `ref_a` e `ref_b` | 0 |
| PM2 taxa de aceitação dos geradores | Positivos construtivos aceitos pelas referências / gerados | ≥ 0,5 por (conceito, n); reportada sempre |
| PM3 vazão | Pares válidos por segundo por (conceito, n) | ≥ 1 000 pares em ≤ 60 s |
| PM4 emparelhamento de densidade | Fração de pares com o mesmo número de pretas | 1,0 |
| PM5 M10 | Acurácia balanceada do classificador por limiar de densidade, ajustado no próprio conjunto | ≤ 0,55 |
| PM6 frequências naturais | Comparação com `analysis/audit_frequencias_saida.md` | Dentro de 3 desvios-padrão |
| PM7 contagem de termos N(s, τ) | Programação dinâmica exata | Reportada até s = 12 |
| PM8 s_reach(B, τ) | Seção 2.4 | Reportado para B em {10⁴, 10⁵, 10⁶} e cinco contextos de tipo |
| PM9 vazão do enumerador | Candidatos avaliados por segundo | ≥ 2 000/s em tamanhos ≤ 8; reportada |
| PM10 degraus alcançáveis | Para cada degrau da escada: tamanho com abstrações anteriores ≤ s_reach(B_max, τ)? | Tabela; alimenta a decisão |
| PM11 extração de abstrações | Igualdade comportamental entre fragmento extraído e abstração pretendida | 100% nas grades do piloto, n ≤ 6 |
| PM12 minimalidade do oráculo | Igualdade com força bruta em n ≤ 4 | 50/50 pares |
| PM13 latência do oráculo | Segundos por rodada | ≤ 2 |
| PM14 fechamento do livro-razão | Total − soma das partes | 0 |
| PM15 determinismo | Igualdade de livros entre execuções com a mesma semente | Idêntico |
| PM16 custo projetado | Modelo da seção 8 | ≤ 2 000 horas de CPU |

---

## 5. Testes unitários

Cada teste tem entrada concreta e resultado esperado; todos devem passar antes de qualquer execução do piloto.

| # | Módulo | Teste | Esperado |
|---|---|---|---|
| U1 | referencias | Grade 3×3 com pretas em (1,1), (1,2), (3,3) | 2 componentes; `UmComponente` falso; `DoisSeparados` verdadeiro; `MaiorTocaBorda` verdadeiro |
| U2 | referencias | Todas as grades de n = 1 a 4, todos os conceitos | `ref_a` = `ref_b` |
| U3 | referencias | 10⁵ grades por n de 5 a 9, todos os conceitos | `ref_a` = `ref_b` |
| U4 | referencias | Invariâncias declaradas, 1 000 grades por conceito e transformação | Rótulo preservado |
| U5 | referencias | Grade vazia; grade toda preta; n = 1 | Casos de borda com os valores definidos no pré-registro |
| U6 | geradores | Frequência exata de `LinhasIguais` em n = 4, p = 0,5 (0,028) contra Monte Carlo com 10⁵ amostras | Dentro de 3 desvios-padrão |
| U7 | geradores | 1 000 positivos construtivos por (conceito, n ≤ 6) | 100% positivos pelas duas referências |
| U8 | geradores | Negativos emparelhados | Mesmo número de pretas; 100% negativos |
| U9 | geradores | Quase-acerto por trocas | Grade antes da última troca é positiva; depois, negativa; número de trocas mínimo verificado por força bruta em n ≤ 4 |
| U10 | geradores | M10 em cada conjunto gerado | ≤ 0,55 |
| U11 | avaliador | `fix (λx. x)` em tipo Bool com n = 3 | `falso` após F(3) = 81 passos, sem laço |
| U12 | avaliador | `concatenar` de duas listas de comprimento F(n) | Comprimento F(n), truncado |
| U13 | avaliador | Contagem de passos de `algum (celula g) (posicoes g)` numa grade 3×3 toda branca | Valor fixado no pré-registro, estável entre execuções |
| U14 | dsl | Tamanho de `λg. nao (vazia? (pretas g))` | 5 |
| U15 | dsl | Tamanho de `fix (λrec A B. se (vazia? A) B (rec (cauda A) (cauda B)))` | 13 |
| U16 | tradutores | Para cada primitiva p de E0 e de E0': `[[τ(p)]] = [[p]]` em todas as grades de n ≤ 3 e numa bateria fixa de argumentos funcionais | Igualdade |
| U17 | tradutores | `inline(t)` para t com biblioteca | Mesma denotação; tamanho ≤ bound do lema de inlining |
| U18 | adaptadores | Sequência `1101110` | Componentes = corridas {1,2}, {4,5,6}; grafo com 4 nós e arestas 1–2, 3–4, rótulos pretos 1, 2, 3 → componentes {1,2}, {3} |
| U19 | enumerador | Todos os termos fechados bem tipados de tamanho ≤ 4 em `Grade → Bool` | Conjunto igual ao gerado por força bruta; cardinalidade igual à contagem por programação dinâmica |
| U20 | enumerador | Poda por equivalência observacional em tamanho ≤ 5 | Pelo menos um representante por classe, comparado ao enumerador sem poda |
| U21 | biblioteca | Soluções manuais de `ParAdjacente` e `NenhumaIsolada` | Fragmento extraído comportamentalmente igual a `vizPretos` |
| U22 | biblioteca | Soluções manuais de duas tarefas "no máximo" | Fragmento igual a `descartar` ou a `noMaximo` |
| U23 | oraculo | 50 pares (h, c) com h aleatório de tamanho ≤ 6 e c em F1 ∪ F2, n ≤ 4 | Contraexemplo igual ao mínimo por força bruta |
| U24 | oraculo | c = `LinhasIguais`, h = `λg. falso`, n = 5 | Contraexemplo é um positivo construtivo com número mínimo de pretas no reservatório |
| U25 | razao | Execução seca com três tarefas | Total = soma; igual entre E0 e E0' em candidatos |
| U26 | piloto | Duas execuções com semente 10 001 | Relatórios idênticos byte a byte |
| U27 | piloto | Intervalos de sementes e hashes de conjuntos do piloto contra os reservados ao confirmatório | Disjuntos |

---

## 6. Dados do piloto e separação do confirmatório

- **Sementes:** piloto de 10 000 a 19 999; confirmatório de 20 000 em diante. Nenhum gerador do confirmatório aceita semente abaixo de 20 000 (verificado por asserção).
- **Grades:** todos os conjuntos do piloto (treino, oráculo, validação, teste interno, extrapolação) são gerados com sementes do piloto; os hashes dos conjuntos são publicados no relatório do piloto, e o pré-registro confirmatório verifica disjunção por hash (U27).
- **Instâncias de conceito expostas no piloto:** F1 completa; F1' completa; F2: `UmComponente`, `DoisSeparados`, `NenhumaIsolada`; F3: `PrimeiraUltimaIguais`, "linha 1 no máximo linha n", `LinhasIguais`; F2×F3: `TodosMesmoTamanho`; todas as tarefas de função das duas escadas; o currículo distrator. Todas ficam marcadas "exposto" e **fora do desfecho primário** confirmatório, que usa as demais instâncias dos esquemas (documento 02, 2.2.4) e F4.
- **F4:** não existe no piloto. As faixas de tamanho que o autor independente recebe vêm do piloto, sem os programas.
- **Hiperparâmetros fixados no piloto:** B, K, limiar de pontuação do compressor, tamanho da amostra de equivalência observacional, tamanho do reservatório do oráculo. Congelados no pré-registro.

---

## 7. Procedimento por fases

| Fase | Conteúdo | Saída | Duração indicativa |
|---|---|---|---|
| 0 | `grade`, `referencias`, testes U1–U5 | Referências validadas | 4 dias |
| 1 | `geradores`, testes U6–U10; reprodução das frequências; tabelas PM2–PM6 | Geradores validados; conjuntos do piloto com hashes | 3 dias |
| 2 | `dsl`, `avaliador`, `tradutores`, testes U11–U17; contagem N(s, τ) | PM7; verificação da implementação dos tradutores | 5 dias |
| 3 | `enumerador`, testes U19–U20; medição de s_reach por contexto de tipo e orçamento, em E0, E0', E0+ | PM8, PM9 | 3 dias de trabalho, até 40 horas de CPU |
| 4 | Verificação dos programas de referência da escada contra as referências; tabela de degraus; `biblioteca`, testes U21–U22; PM10, PM11 | Tabela de viabilidade da escada | 3 dias |
| 5 | `oraculo`, `aprendizes`, `razao`, testes U23–U26; execução seca de L-fix e L-lib na escada com dados do piloto; PM12–PM15 | Curvas de custo; distribuição de K; livro-razão | 4 dias, até 24 horas de CPU |
| 6 | Modelo de custo; projeção PM16; relatório; decisão | Relatório do piloto; decisão GO / E0+ / NO-GO; hiperparâmetros congelados | 2 dias |

Total indicativo: quatro a cinco semanas de uma pessoa.

---

## 8. Estimativa de recursos

- **Implementação:** 2 500 a 3 500 linhas de Python; sem dependências obrigatórias.
- **Memória:** o enumerador com poda guarda uma tabela por (tamanho, tipo) de representantes; com 10⁶ candidatos e assinaturas de equivalência de 64 entradas, abaixo de 4 GB.
- **CPU:** geração e auditorias, minutos; contagem N(s, τ), segundos; enumeração a 10⁶ candidatos por contexto, com 2 000 candidatos por segundo e 5 contextos em 3 bases, cerca de 2 horas por combinação, até 40 horas no total; execução seca, até 24 horas. Total do piloto abaixo de 100 horas de CPU num computador comum.
- **Modelo de custo para o confirmatório:** custo = (número de tarefas no currículo) × (orçamento B por tarefa) × (rodadas médias K) × (custo médio por candidato) × (sementes) × (bases) × (braços de controle). Com 60 tarefas, B = 10⁶, K médio 4, 0,5 ms por candidato, 5 sementes, 2 bases e 10 braços: 60 × 10⁶ × 4 × 0,0005 s × 5 × 2 × 10 ≈ 1,2 × 10⁷ s ≈ 3 300 horas. Isso excede o limiar PM16; o piloto mede o custo real por candidato e a necessidade de B, e a seção 10 prevê a redução de braços ou de sementes antes do pré-registro. **[H, a medir]**

---

## 9. Condições de interrupção

Qualquer uma interrompe o piloto e exige revisão documentada antes de retomar.

- **I1 Integridade:** discordância entre referências (PM1 > 0); falha em U11–U17; livro-razão não fecha; não determinismo.
- **I2 Geradores:** após revisão, algum (conceito, n) não atinge PM3 ou PM5; conceito é retirado ou redefinido, com registro.
- **I3 Oráculo:** minimalidade falha em n ≤ 4, ou latência acima de 10 s por rodada após otimização.
- **I4 Compressor:** não extrai `vizPretos` a partir de soluções conhecidas após revisão.
- **I5 Alcance mínimo:** s_reach(10⁶, `Grade → Bool`) < 8. Nem F1 é alcançável; E0 ou o enumerador precisam de redesenho antes de qualquer outra fase.
- **I6 Custo:** vazão do enumerador abaixo de 200 candidatos por segundo após otimização; o piloto não termina em prazo útil em Python puro e a implementação migra de linguagem antes de continuar.
- **I7 Vazamento:** qualquer uso de semente ou grade do intervalo confirmatório, detectado por U27 ou por inspeção.

---

## 10. Critérios de aceitação e decisão

**Aceitação do piloto (todas as condições):** U1–U27 passam; PM1 = 0; PM2–PM6 nos limiares; PM11 = 100%; PM12 = 50/50; PM14 = 0; PM15 idêntico; relatório com hashes publicado.

**Decisão sobre a base, pela tabela PM10, com B_max = 10⁶ candidatos por tarefa:**

- **GO com E0:** todo degrau da escada tem tamanho (com as abstrações anteriores) ≤ s_reach(B_max, τ) no seu contexto de tipo, em E0 **e** em E0'.
- **GO com E0+:** a condição falha em E0 para `fecho` ou `descartar`, mas vale em E0+ e E0'+. A alegação confirmatória é redigida com a restrição do documento 02, 2.8.3, e os custos C0 dos conceitos-alvo em E0+ são publicados.
- **NO-GO:** a condição falha também em E0+. O experimento 1 é redesenhado (busca guiada, tarefas de função mais finas, ou outra decomposição) e volta ao piloto. Nada é alegado.

**Decisão sobre custo:** se PM16 excede 2 000 horas, reduzir, nesta ordem e antes do pré-registro: braços de controle neurais com aumento de dados; sementes de 5 para 3; orçamento 30B. Nunca reduzir o número de conceitos abaixo de 20 no desfecho primário.

---

## 11. O que o piloto não pode concluir

- Nada sobre H-B1, H-B3, nem sobre nenhuma hipótese científica: dados e hiperparâmetros estão expostos, e as instâncias de conceito foram usadas em ajuste.
- Nada sobre transferência (os adaptadores só são testados unitariamente).
- Nada sobre controles neurais (não implementados).
- Nada sobre L2 (documento 01, 1.2-bis), por construção do experimento.
- Nada sobre inteligência geral.

Se o piloto mostrar que L-lib supera L-fix na execução seca, a frase correta é: "o mecanismo funciona nos dados do piloto; a hipótese será testada no confirmatório com dados e instâncias não expostos".

---

## 12. Entregáveis

1. Código do pacote `fedro_piloto/` com testes passando.
2. Relatório do piloto em `docs/04-relatorio-piloto.md` com: tabelas PM1–PM16; tabela de viabilidade da escada por base; curvas de custo da execução seca; hashes de todos os conjuntos; intervalos de sementes; lista de instâncias expostas.
3. Hiperparâmetros congelados e a escolha de base, em arquivo de configuração versionado.
4. Faixas de tamanho para a família F4, sem programas.
5. A decisão GO / E0+ / NO-GO com a justificativa pela seção 10.
6. Lista de desvios em relação a este plano, se houver.
