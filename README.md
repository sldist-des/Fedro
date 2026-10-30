# Fedro

Programa independente de pesquisa sobre as condições que tornam possível o surgimento da inteligência, com o objetivo de longo prazo de investigar a construção de uma inteligência artificial geral a partir de mecanismos fundamentais, e não de modelos existentes.

## Documentos

- `docs/01-investigacao-fundamentos.md` (v0.2, com nota v0.3) — Análise crítica: hipótese reformulada em camadas de novidade (L0–L3), objeções, estado da arte, direções. O histórico de mudanças conceituais está no início do documento; os blocos **Revisão v0.2** e **Nota v0.3** preservam o texto anterior onde ele foi corrigido.
- `docs/02-protocolo-experimental.md` (v0.2) — Protocolo pré-registrável dos dois experimentos: grades com dialética de contraexemplos (fundamentos formais corrigidos, auditoria de frequências, geradores, famílias por esquema, escada de currículo, auditoria de transferência, F4 com oráculo oculto) e agente sensório-motor (separação anomalia / regularidade / objeto / causa, controles de intervenção, desenho fatorial viés × dados). Comparação e ordem de execução.
- `docs/03-plano-piloto.md` (v0.1) — Especificação do piloto do experimento 1: perguntas de viabilidade, arquitetura mínima, métricas, testes unitários, dados próprios, estimativa de recursos, condições de interrupção, critérios de aceitação e decisão GO / E0+ / NO-GO.

- `docs/04-relatorio-piloto.md` (v0.2) — Relatório da execução exploratória do piloto (semente 10001, escala reduzida): módulos, 215 testes, desvios, métricas PM1–PM16, classificação das abstrações (fornecida / manual de referência / descoberta / descoberta e reutilizada), custos e a decisão **NO-GO a B = 10⁴**. Nenhuma abstração foi reutilizada; nenhuma evidência para H-B1.

- `docs/05-diagnostico-redesenho.md` (v0.1) — Diagnóstico causal do NO-GO com evidências dos registros, experimento mínimo de aquisição e transferência (`fedro_piloto/experimento_minimo.py`, registros em `runs/em-*`), correções de integridade, avaliação da estratégia de busca e veredito pelo critério central (abstração descoberta pelo aprendiz e reutilizada em tarefa inédita, com proveniência verificável).

## Código do piloto

- `fedro_piloto/` — implementação exploratória do Experimento 1 (grades, referências independentes, geradores com partição por instância e detecção de degeneração, DSL com Sem_n, avaliador, tradutores E0↔E0', enumerador com poda por equivalência observacional validada contra enumeração exaustiva, biblioteca com certificados de proveniência, oráculo de contraexemplos mínimos, aprendizes L-fix e L-lib, livro-razão com contadores determinísticos separados das medições de tempo e memória). Testes: `python3 -m unittest discover -s fedro_piloto/tests -v` (cerca de 8 minutos). Execução do piloto: `python3 -m fedro_piloto.piloto --id <id> --semente <s> --processos 4`. Experimento mínimo: `python3 -m fedro_piloto.experimento_minimo --id <id> --B 20000 --politica tamanho|unigrama --processos 4`.
- `runs/` — registros reproduzíveis das execuções (configuração com hash das fontes, contadores determinísticos, medições, hashes dos conjuntos, abstrações).

## Análises reproduzíveis

- `analysis/audit_frequencias.py` — Frequência de positivos por conceito, tamanho de grade e parâmetro de Bernoulli (fórmulas exatas e Monte Carlo), e potência do teste de sinal pareado. Saída em `analysis/audit_frequencias_saida.md`. Executar com `python3 -I analysis/audit_frequencias.py 20000`.

O experimento confirmatório não foi executado. O piloto exploratório foi executado e resultou em NO-GO a B = 10⁴ (documento 04); a próxima etapa é o redesenho previsto no documento 03, seção 10.

## Convenções

Cada afirmação relevante leva um rótulo epistêmico: **[P]** prova formal, **[E]** evidência empírica, **[C]** resultado computacional, **[F]** interpretação filosófica, **[H]** hipótese, **[R]** condição de refutação, **[A]** questão aberta. Nenhuma referência é incluída sem verificação; as que não puderam ser verificadas estão marcadas no texto.

Regras fundamentais: a primeira definição mensurável de aprendizagem adotada pelo programa não é uma definição da natureza da inteligência; nenhum resultado positivo isolado demonstra a hipótese; resultados sobre máquinas universais não justificam conclusões sobre as linguagens limitadas dos experimentos.
