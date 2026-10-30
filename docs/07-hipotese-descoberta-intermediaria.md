# 07 — Hipótese separada: descoberta de operações intermediárias não apresentadas como tarefa

**Versão 0.1** — 2026-10-30. Desenho pré-registado de uma investigação **distinta** do benchmark cego (`benchmark/protocolo-avaliacao.md`). Nada aqui altera o benchmark externo, o contrato público ou o executor; nada aqui é executado antes de o benchmark cego estar avaliado. Rótulos: **[H]** hipótese, **[R]** requisito, **[C]** procedimento, **[A]** aberto, **[E]** evidência já existente.

---

## 1. Pergunta

Nos documentos 05 e 06, toda operação adquirida pelo aprendiz foi a **solução de uma tarefa que o ambiente apresentou**: a promoção transforma a solução aceita de uma tarefa de função em constante; a compressão por recorrência (L-lib) nunca disparou, porque as tarefas do currículo não partilhavam fragmentos repetidos em soluções aceitas. A decomposição do problema em degraus foi feita pelo pesquisador (06, §5.1).

A pergunta desta investigação é:

> **Pode um aprendiz identificar e consolidar uma operação intermediária útil sem que essa operação lhe seja apresentada como tarefa?**

"Operação intermediária" = um termo fechado da DSL, de tamanho ≥ 3, que (i) não é a solução de nenhuma tarefa apresentada, (ii) ocorre como subtermo das soluções de tarefas apresentadas, ou é aproximado por elas, e (iii) encurta a solução de uma tarefa posterior o suficiente para a trazer para dentro do alcance da busca.

## 2. Por que os mecanismos atuais não respondem **[E]**

| mecanismo | o que precisa para criar uma entrada | por que não descobre uma intermediária |
|---|---|---|
| promoção (L-lib+f) | uma tarefa de função aceita | a entrada **é** a tarefa; não há descoberta |
| compressão por recorrência (L-lib, limiar 3, ≥ 2 ocorrências) | o mesmo fragmento em ≥ 2 soluções aceitas | em princípio descobre sem tarefa; nunca disparou nos registros porque os currículos não tinham dois degraus **alcançáveis** com fragmento comum (05, §1; 06, §2: L-lib ≡ L-fix em 10 de 10 execuções) |

Logo a compressão é o candidato natural, mas nunca foi testada na condição em que poderia funcionar. É isso que esta investigação faz, antes de propor mecanismos novos.

## 3. Hipóteses **[H]**

- **H-I1 (recorrência basta).** Se duas tarefas apresentadas, ambas ao alcance de L-fix, têm soluções mínimas que partilham um subtermo fechado u de tamanho ≥ 3, a compressão por recorrência cria a entrada u, e uma terceira tarefa cuja solução mínima com u tem ≤ 8 folhas, mas ≥ 11 folhas sem u, passa a ser resolvida por L-lib e não por L-fix.
- **H-I2 (a recorrência é frágil à variação sintática).** Se as duas soluções mínimas contêm **variantes** de u (α-equivalentes mas com argumentos trocados, ou η-expandidas), a anti-unificação da compressão (biblioteca.py) ou as capta, ou não; prevê-se que capte variantes por renomeação e não capte variantes que exijam um parâmetro extra. Isto delimita o que "recorrência" quer dizer.
- **H-I3 (promoção de subtermos).** Um mecanismo que promove **todos** os subtermos fechados de tamanho ≥ 3 de cada solução aceita (candidatos a operação) resolve a terceira tarefa sem precisar de duas ocorrências, mas paga transferência negativa crescente com o número de entradas (gramática maior; 06, §4.3: 1,3–1,8× por duas entradas). Prevê-se que sem um critério de **utilidade** (poda das entradas nunca usadas ao fim de k tarefas) o custo nas tarefas sem relação cresça mais do que linearmente com o número de entradas.

A hipótese forte, que **não** se espera confirmar nesta fase, é: **H-I4** o aprendiz identifica uma operação intermediária que não é subtermo de nenhuma solução aceita (por exemplo, uma generalização de duas soluções por anti-unificação com um buraco). Fica registada como [A].

## 4. Desenho **[C]**

### 4.1 Tríades

Cada unidade experimental é uma **tríade** (A, B, C) de tarefas definidas no ambiente de grades, com a DSL E0 e os orçamentos do documento 05 (B = 20 000, K = 12):

- A e B: tarefas de função ao alcance de L-fix (solução mínima em E0 com ≤ 8 folhas), cujas soluções mínimas partilham um subtermo fechado u (tamanho ≥ 3), **sem** que u seja a solução de A nem de B;
- C: tarefa cuja solução mínima em E0 tem ≥ 11 folhas e cuja solução com u como constante tem ≤ 8 folhas;
- u **nunca** é apresentado como tarefa.

Controlos por tríade:

- (A', B', C): A' e B' ao alcance, sem subtermo comum relevante para C (mesmos tipos, tamanhos semelhantes) — a compressão não deve ajudar;
- (A, B, C⁻): C⁻ com a mesma dificuldade em E0 mas em que u é inútil — mede a transferência negativa da entrada criada;
- lesão: remover a entrada u antes de C.

### 4.2 Regra de construção das tríades **[R]**

Para não repetir o problema do documento 06 (famílias desenhadas por quem conhece as abstrações), as tríades são **geradas por um procedimento, não escolhidas à mão**: enumeram-se, com o próprio enumerador em modo de auditoria (tabela de referência, sem aprendiz), os termos fechados u de tipo Grade → Pos → L Pos, Grade → L Pos → L Pos ou Grade → L Pos com 3 ≤ |u| ≤ 5; para cada u, procuram-se, na enumeração de programas de ≤ 8 folhas, pares (A, B) de denotações distintas que contêm u, e programas C de ≤ 8 folhas com u cuja forma expandida tem ≥ 11 folhas e cuja denotação não é degenerada na partição de treino. As tríades são então **amostradas ao acaso** (semente registada) de entre as candidatas, sem olhar para o seu conteúdo, e congeladas por hash antes de qualquer execução. As referências Python de A, B, C são as denotações dos programas (o ambiente avalia a referência pela semântica da DSL, como já faz para as tarefas de função internas), com a mesma bateria de argumentos.

Isto elimina a escolha humana do conteúdo das tríades, mas **não** elimina o viés de que a DSL define o que conta como "intermediário": a tríade é, por construção, uma decomposição possível em E0. A pergunta respondida é se o aprendiz **encontra** essa decomposição sem que lha mostrem, não se a inventa.

### 4.3 Braços

| braço | mecanismo | prevê-se que resolva C? |
|---|---|---|
| L-fix | nenhum | não (≥ 11 folhas) |
| L-lib (limiar 3, ≥ 2 ocorrências) | compressão por recorrência | sim se H-I1 |
| L-lib+f | promoção | não (A e B são promovidas, mas u não é A nem B; só se a solução de A ou B coincidir com u — excluído por construção) |
| L-sub (novo; variante declarada) | promoção de todos os subtermos fechados com |u| ≥ 3 das soluções aceitas, com poda das entradas não usadas após k = 4 tarefas | sim se H-I3; custo medido em C⁻ |
| L-lib/lesão | compressão, entrada removida antes de C | não |

Políticas: tamanho (primária) e unigrama. Sementes: três do intervalo exploratório ainda não usadas (a fixar no pré-registro final, ≥ 10010). Tríades: 20 (potência: com 20 tríades independentes, um efeito em ≥ 15 é distinguível de acaso ao nível habitual do teste de sinal; o cálculo exato fica para o pré-registro final).

### 4.4 Medidas

As do documento 06 (aceitação, custo cumulativo, reutilização verificável com procedência, transferência positiva/negativa sem razões exatas quando um braço falha, verificação exaustiva e amostral), mais: (i) **se a entrada criada é u** (igualdade α-η com o u da construção) ou outra coisa; (ii) em L-sub, o número de entradas criadas e podadas e o custo em C⁻ em função desse número; (iii) para H-I2, a fração de tríades em que a compressão capta variantes de u.

## 5. Critérios pré-registados **[R]**

- H-I1 corroborada se L-lib resolve C em ≥ 15 das 20 tríades, com a entrada criada α-η-igual a u, e em ≤ 3 das 20 tríades de controlo (A', B', C); lesão reverte.
- H-I3 corroborada se L-sub resolve C em ≥ 15 das 20 tríades **e** o custo em C⁻ fica abaixo de 2× o de L-fix; refutada na parte de custo se a razão em C⁻ crescer acima de 2× com ≥ 4 entradas.
- Qualquer resultado é reportado por tríade, com as tríades falhadas e o motivo.

## 6. O que isto não é

Não é formação de conceitos (06, §5.1): u é um termo da mesma DSL; o que se testa é se a **estatística das soluções** (recorrência) ou a **estrutura das soluções** (subtermos) chega para consolidar uma operação não ensinada. Também não é o Experimento 2: continua no regime simbólico. É o passo intermediário que decide se vale a pena sofisticar o mecanismo simbólico (sucesso de H-I1/H-I3) ou se o problema da descoberta de intermediários exige outro tipo de sinal (fracasso).

## 7. Separação do benchmark cego **[R]**

1. Nenhuma tríade é derivada das tarefas do autor externo, e o autor externo não recebe este documento.
2. Esta investigação não começa antes de o relatório do benchmark cego (protocolo, §8) estar escrito; se o benchmark mostrar o mecanismo inerte (protocolo, §7.2), esta investigação passa à frente da sofisticação do mecanismo, como já está decidido no protocolo.
3. O código necessário (gerador de tríades, braço L-sub) fica em módulos próprios (`fedro_piloto/triades.py`, variante `LSub` em `aprendizes.py` marcada como declarada) e só é escrito depois do relatório do benchmark, para que nada do benchmark seja executado com código alterado.
