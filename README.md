# Fedro

Programa independente de pesquisa sobre as condições que tornam possível o surgimento da inteligência, com o objetivo de longo prazo de investigar a construção de uma inteligência artificial geral a partir de mecanismos fundamentais, e não de modelos existentes.

## Documentos

- `docs/01-investigacao-fundamentos.md` (v0.2, com nota v0.3) — Análise crítica: hipótese reformulada em camadas de novidade (L0–L3), objeções, estado da arte, direções. O histórico de mudanças conceituais está no início do documento; os blocos **Revisão v0.2** e **Nota v0.3** preservam o texto anterior onde ele foi corrigido.
- `docs/02-protocolo-experimental.md` (v0.2) — Protocolo pré-registrável dos dois experimentos: grades com dialética de contraexemplos (fundamentos formais corrigidos, auditoria de frequências, geradores, famílias por esquema, escada de currículo, auditoria de transferência, F4 com oráculo oculto) e agente sensório-motor (separação anomalia / regularidade / objeto / causa, controles de intervenção, desenho fatorial viés × dados). Comparação e ordem de execução.
- `docs/03-plano-piloto.md` (v0.1) — Especificação do piloto do experimento 1: perguntas de viabilidade, arquitetura mínima, métricas, testes unitários, dados próprios, estimativa de recursos, condições de interrupção, critérios de aceitação e decisão GO / E0+ / NO-GO.

## Análises reproduzíveis

- `analysis/audit_frequencias.py` — Frequência de positivos por conceito, tamanho de grade e parâmetro de Bernoulli (fórmulas exatas e Monte Carlo), e potência do teste de sinal pareado. Saída em `analysis/audit_frequencias_saida.md`. Executar com `python3 -I analysis/audit_frequencias.py 20000`.

O experimento em si ainda não foi implementado; a próxima etapa é o piloto conforme o documento 03.

## Convenções

Cada afirmação relevante leva um rótulo epistêmico: **[P]** prova formal, **[E]** evidência empírica, **[C]** resultado computacional, **[F]** interpretação filosófica, **[H]** hipótese, **[R]** condição de refutação, **[A]** questão aberta. Nenhuma referência é incluída sem verificação; as que não puderam ser verificadas estão marcadas no texto.

Regras fundamentais: a primeira definição mensurável de aprendizagem adotada pelo programa não é uma definição da natureza da inteligência; nenhum resultado positivo isolado demonstra a hipótese; resultados sobre máquinas universais não justificam conclusões sobre as linguagens limitadas dos experimentos.
