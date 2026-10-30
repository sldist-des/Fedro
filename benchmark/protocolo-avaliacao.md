# Protocolo de avaliação com benchmark cego

**Versão 0.1** — 2026-10-30. Pré-registro do procedimento de avaliação externa do mecanismo de aquisição e reutilização de operações (documentos 05 e 06), com um conjunto de tarefas construído por um autor independente a partir do contrato público (`benchmark/contrato-publico.md`). Este documento fica no repositório e **não** é enviado ao autor. Tudo o que está aqui é fixado antes de o pacote do autor ser recebido; o que for alterado depois é registado em §9 com data e motivo.

Rótulos como nos documentos anteriores: **[R]** requisito, **[C]** procedimento computacional, **[H]** hipótese, **[A]** aberto.

---

## 1. Papéis e fronteira de informação **[R]**

| papel | quem | tem acesso a | não tem acesso a |
|---|---|---|---|
| pesquisador e desenvolvedor principal | Claude Fable 5.1 (esta sessão) | todo o repositório | o pacote do autor até ao congelamento; nunca o altera |
| autor externo do benchmark | Claude Opus 5.5, sessão separada | só `benchmark/contrato-publico.md` e `benchmark/kit-autor/` | o repositório, os documentos 01–06, as soluções, a biblioteca aprendida, os currículos, as famílias anteriores, os resultados, as nossas expectativas |
| revisor humano | Gabriel Lopes | tudo | — |

A auditoria de vazamento (`benchmark/auditoria_vazamento.py`, relatório em `benchmark/auditoria-vazamento.md`) confere automaticamente que os ficheiros enviados não contêm identificadores das nossas tarefas, conceitos e entradas de biblioteca, nem termos de mecanismo e de resultado; a lista de conferência manual está no relatório. O contrato é revisto pelo revisor humano antes do envio.

O pesquisador principal **não cria tarefas** para o benchmark. O pacote de exemplo do kit (três tarefas triviais que só ilustram o formato) não entra na avaliação.

## 2. Receção e congelamento **[R]** **[C]**

1. O autor entrega a pasta do pacote já congelada com `validar_pacote.py --congelar` (MANIFESTO.json com os hashes). A pasta é copiada para `benchmark/recebidos/<nome>-v<versão>/` sem qualquer alteração e o hash do pacote é registado em `benchmark/recebidos/REGISTO.md` com a data.
2. O executor (`python3 -m fedro_piloto.benchmark_externo validar <pasta>`) repete a validação autónoma do kit e confere o hash. Qualquer ficheiro alterado depois do congelamento faz o executor recusar a execução (`ErroIntegridade`).
3. As tarefas são registadas no ambiente com ids internos prefixados (`bx:`), para nunca colidirem com tarefas internas. Os ficheiros selados (`testes_ocultos.json`, `testemunhas.json`) só são lidos depois da execução, pela verificação (§6).
4. **Erros de integridade** (validação falha; referência não total, não determinística ou degenerada no ambiente; discordância entre as duas implementações; tipo errado) são registados em `benchmark/recebidos/REGISTO.md` e comunicados ao autor, que produz uma **nova versão** com novo hash. Nenhum ficheiro do autor é corrigido por nós; nenhuma tarefa é removida por nós. Uma tarefa que se revele degenerada só durante a execução (o ambiente não consegue formar os exemplos iniciais na partição de treino) é registada como `invalida_no_ambiente` nos resultados de todos os braços, excluída das contagens de tarefas válidas e comunicada ao autor; o resto do pacote é avaliado.
5. Resultados de uma versão nunca são substituídos: cada versão tem os seus registros em `runs/bx-<nome>-v<versão>-*`. O relatório final diz que versões existiram e porquê.

## 3. O que é fixado antes de ver o pacote **[R]**

- A DSL (E0, tabela `BASES["E0"]`), o enumerador, as políticas de busca, os aprendizes e o ambiente são os do commit registado no relatório (`fontes` em cada registro). **Não são alterados depois de ver as tarefas nem depois de ver resultados.** Se um defeito de implementação for descoberto durante a avaliação, é corrigido, registado em §9, e **toda** a avaliação é repetida com o pacote inalterado; os registros antigos ficam.
- Orçamentos: B = 20 000 candidatos por tarefa e por tentativa, K = 12 rodadas de contraexemplos, 100 000 passos por avaliação de hipótese, tamanho máximo 30, os mesmos do documento 05. Não são aumentados para melhorar resultados.
- Sementes de dados (todas no intervalo exploratório, nunca usadas antes): **10007** (primária), **10008** e **10009** (robustez). Sementes do seletor aleatório: 1, 2, 3. Os buckets 50–99 continuam intocados.
- Ordem primária das tarefas: a ordem de listagem do autor.

## 4. Desenho experimental pré-registado **[C]**

Braços (cada um é um aprendiz que percorre as tarefas em sequência, com o mesmo ambiente):

| braço | mecanismo |
|---|---|
| L-fix | tabela fixa E0, sem estado entre tarefas (na política unigrama, o prior de constantes das próprias soluções é o único estado) |
| L-lib | L-fix + compressão por recorrência (fragmentos com ≥ 2 ocorrências nas soluções aceitas) |
| L-lib+f | L-lib + promoção da solução aceita de cada tarefa de função como entrada da biblioteca |
| L-lib+f/lesão | L-lib+f com remoção de todas as entradas descobertas num ponto fixado (abaixo) |

Políticas de busca: tamanho e unigrama (ambas, para todos os braços). Modos:

| modo | estado inicial | o que mede | custo contabilizado |
|---|---|---|---|
| **zero** (primário) | biblioteca vazia | se o mecanismo adquire e reutiliza operações **dentro** do conjunto do autor, sem nada preparado por nós | só o benchmark |
| **prévio** (secundário) | depois da cadeia de três tarefas do documento 05 (as mesmas para todos os braços; só o mecanismo difere) | se as operações adquiridas no nosso currículo transferem para tarefas que não desenhámos (a pergunta deixada aberta em 06, §6.3.1) | cadeia **+** benchmark; a cadeia entra no custo cumulativo de todos os braços |

Lesão: no modo zero, antes da tarefa de índice ⌊N/2⌋ da ordem do autor (N = número de tarefas); no modo prévio, imediatamente depois da cadeia. Mede a sensibilidade à remoção: tarefas aceitas e custo nas tarefas posteriores à lesão, em comparação com L-lib+f.

Execuções:

| bloco | braços | políticas | modo | sementes | ordem | registro |
|---|---|---|---|---|---|---|
| A (primário) | 4 | 2 | zero | 10007 | autor | `runs/bx-<nome>-v<v>-A-s10007` |
| B (transferência das nossas operações) | L-fix, L-lib+f, L-lib+f/lesão | 2 | prévio | 10007 | autor | `…-B-s10007` |
| C (robustez a sementes) | L-fix, L-lib+f | 2 | zero | 10008, 10009 | autor | `…-C-s1000{8,9}` |
| D (variação do ambiente) | L-fix, L-lib+f | tamanho | zero | 10007 | autor | `…-D-k20`: reservatório do oráculo com 20 grades em vez de 40 |
| E (ordens; só se N ≥ 6) | L-lib+f, L-fix | tamanho | zero | 10007 (dados); 1, 2, 3 (seletor) | autor, aleatória ×3, autodirigida (versão 2) | `…-E` |

Os blocos A e B são obrigatórios; C, D e E são executados se o custo de A e B o permitir (estimativa: 2–4 h de CPU por bloco com 12–20 tarefas). Nenhum bloco é acrescentado depois de ver resultados, salvo registo em §9.

## 5. Métricas pré-registadas **[C]**

Todas as métricas são calculadas por `benchmark_externo.metricas` e `verificar_benchmark` sobre **todas** as tarefas válidas do pacote; nenhuma tarefa é excluída depois de ver resultados.

| métrica | definição | por |
|---|---|---|
| tarefas resolvidas | número de tarefas aceitas (hipótese sem contraexemplo no domínio do oráculo); lista de ids | braço |
| custo computacional acumulado | soma dos passos do livro-razão do aprendiz em todas as tarefas (modo prévio: inclui a cadeia); o livro tem de fechar com a curva | braço |
| eficiência de aquisição | custo cumulativo / tarefas aceitas; tarefas aceitas por 10⁸ passos; tarefas aceitas a custo cumulativo igual (para cada aceitação de L-lib+f ao custo C, quantas L-fix tinha aceitado com custo ≤ C na sua própria curva) | braço; par L-lib+f/L-fix |
| reutilização verificável | tarefas cuja hipótese aceita usa ≥ 1 entrada da biblioteca com proveniência "descoberta" (certificado de descoberta → entrada); entradas descobertas e entradas reutilizadas | braço |
| transferência positiva / negativa | por tarefa, L-lib+f vs L-fix (mesma política e modo): ambos aceitam → razão exata custo L-fix / custo L-lib+f (> 1 positiva, < 1 negativa, = 1 neutra); só L-lib+f aceita → **positiva com razão mínima** custo gasto por L-fix / custo L-lib+f (limite inferior, nunca razão exata); só L-fix aceita → negativa com limite; nenhum aceita → inconclusiva | par |
| generalização a tamanhos inéditos | hipóteses aceitas verificadas em todas as grades n ≤ 4 (bateria do ambiente), em grades da partição `teste_ext` com n = 5..9 e nos testes ocultos do autor; acurácia e acurácia balanceada; conjuntos degenerados assinalados | hipótese |
| erros de previsão | discordâncias de hipóteses **aceitas** com a referência nesses regimes (uma aceitação com erro é uma aceitação indevida do oráculo, reportada como tal); erro de previsão do seletor autodirigido (bloco E): tentativas cujo orçamento era insuficiente | hipótese; seletor |
| sensibilidade à remoção | tarefas posteriores à lesão: aceitas e custo em L-lib+f/lesão vs L-lib+f; `sensível` se a lesão reduz aceitações ou aumenta o custo | par |
| robustez | min / mediana / máx de tarefas aceitas, custo cumulativo e tarefas com reutilização sobre as sementes (bloco C); tarefas aceitas em todas as sementes; diferença entre k = 40 e k = 20 (bloco D) | braço |

Desempenho **absoluto** (quantas tarefas do autor cada braço resolve, a que custo, com que erros) e **vantagem relativa** sobre os controlos (L-fix, lesão, L-lib) são reportados em tabelas separadas. A razão de velocidade só é exata quando ambos aceitam; quando L-fix esgota o orçamento sem aceitar, reporta-se "L-fix falha a C_f" e o limite inferior C_f / C, identificado como limite.

## 6. Verificação pós-execução **[C]**

`python3 -m fedro_piloto.benchmark_externo verificar runs/<registro>`: regimes exaustivo (n ≤ 4) e amostral (n = 5..9, `teste_ext`) de `verificacao.py` para todas as hipóteses aceitas; testes ocultos do autor; testemunhas do autor (parse, tipo, verificação em n ≤ 3, tamanho em E0 — dá o limite superior de tamanho de cada tarefa, usado só para **descrever** a dificuldade, nunca para escolher tarefas). Os ficheiros selados são abertos só nesta etapa.

## 7. Critérios de interpretação pré-registados **[H]** **[R]**

Sejam, no bloco A (modo zero, semente 10007), por política: V o número de tarefas válidas; a_fix, a_lib as tarefas aceitas por L-fix e L-lib+f; r o número de tarefas aceitas por L-lib+f com reutilização verificável; p⁺ e p⁻ as transferências positivas e negativas.

1. **Mecanismo robusto ao autor** (o resultado do documento 06 não é artefacto de desenho): em ambas as políticas, a_lib ≥ a_fix, r ≥ 2, p⁺ ≥ 2 e p⁺ > p⁻, com todas as hipóteses aceitas sem erro de previsão nos três regimes, e a lesão sensível.
2. **Mecanismo inerte no conjunto do autor**: r = 0 em ambas as políticas (nada é reutilizado), ou a_lib = a_fix com custo de L-lib+f ≥ L-fix em todas as tarefas aceitas (só transferência negativa). Interpretação: o mecanismo só funciona em tarefas preparadas como decomposição explícita; a evidência do documento 06 fica restrita a esse caso.
3. **Resultado misto**: qualquer outro padrão; reportado tarefa a tarefa, sem veredito agregado.
4. O bloco B responde separadamente à pergunta de 06, §6.3.1: transferência positiva das nossas operações para ≥ 2 tarefas do autor com reutilização verificável, ou nenhuma. Não altera a leitura de 1–3.
5. Robustez (C, D): o padrão de 1–3 mantém-se nas sementes 10008 e 10009 e com k = 20; se não se mantiver, o resultado primário é reportado como frágil.
6. Erros de previsão em hipóteses aceitas são reportados como **falha do oráculo** (aceitação indevida), separada das métricas de desempenho, e contam contra qualquer leitura positiva.
7. Em nenhum caso o resultado é interpretado como evidência de H-B1, de formação de conceitos ou de inteligência geral (documento 06, §5.1). O que se decide com ele é só a **robustez do mecanismo atual** a tarefas que não preparámos.

Decisão de programa (a tomar pelo revisor com estes critérios): (1) → aprofundar a arquitetura simbólica tem suporte empírico, e a transição para o Experimento 2 (documento 06, §5.2) pode usar o mecanismo como linha de base; (2) → a arquitetura simbólica atual não é a base para o Experimento 2 e a investigação de descoberta de operações intermediárias (`docs/07-hipotese-descoberta-intermediaria.md`) passa à frente; (3) → decidir tarefa a tarefa, com o padrão de reutilização e de transferência negativa como guia.

## 8. Relatório **[R]**

`docs/08-...` (a numerar) conterá: versões do pacote recebidas e erros de integridade; tabela de todas as tarefas válidas com tipo, tamanho da testemunha (se dada), e aceitação/custo/reutilização por braço e política; comparações por par; verificação; blocos C–E se executados; a leitura segundo §7, separando absoluto e relativo; limitações (uma só semente nos blocos A/B/E; a bateria finita de argumentos; o alcance da busca).

## 9. Alterações posteriores ao pré-registro

(nenhuma)
