# Contrato público — ambiente de grades e interface de tarefas

**Versão 1.0** — 2026-10-30. Especificação técnica para a construção de um conjunto independente de tarefas (um *benchmark*) sobre um ambiente de grades binárias e uma linguagem de programas chamada E0. Este documento e a pasta `kit-autor/` são **tudo** o que o autor do benchmark recebe. O autor não deve consultar nenhum outro material do projeto.

Sumário: 1. Ambiente de grades · 2. Tipos, formatos e partição de instâncias · 3. A linguagem E0 e a semântica das operações · 4. Restrições computacionais · 5. Interface para definir tarefas (formato do pacote) · 6. Requisitos de integridade e congelamento · 7. Comunicação entre o benchmark e o aprendiz · 8. Lista de entrega.

---

## 0. Finalidade e regras de independência

O sistema avaliado é um **aprendiz de síntese de programas** em E0: recebe tarefas uma a uma, cada uma com alguns exemplos, propõe programas e recebe contraexemplos de um oráculo até que um programa fique sem contraexemplo (aceito) ou o orçamento se esgote. O aprendiz pode manter estado interno entre tarefas; o conteúdo desse estado não é especificado neste documento nem é relevante para definir tarefas.

O autor do benchmark deve produzir um conjunto de tarefas **sem** conhecer os experimentos anteriores do projeto, as tarefas já usadas, os programas já encontrados ou os resultados obtidos. O conjunto é dele: escolhe o conteúdo, a quantidade, a dificuldade e a organização. Este documento diz apenas **o que o ambiente é, o que uma tarefa pode ser e como ela é avaliada**. Nada aqui indica quais problemas o sistema deveria resolver.

Recomenda-se variedade: tarefas de vários tipos aceites (§2.2) e de dificuldades diversas (programas curtos e longos em E0, §3.4). A organização interna do conjunto fica inteiramente ao critério do autor. O autor pode, se quiser, registar num ficheiro selado (§5.6) observações suas sobre o conjunto; isso só é lido depois da avaliação.

## 1. Ambiente de grades

### 1.1 Grades

Uma **grade** é um quadrado de lado n (1 ≤ n ≤ 9) de células binárias: preta (1) ou branca (0). As **posições** são pares `(i, j)` de inteiros com 1 ≤ i, j ≤ n, onde i é a linha (de cima para baixo) e j a coluna (da esquerda para a direita). A posição `(1, 1)` é o canto superior esquerdo.

Serialização textual: `"n:bits"`, com os n² bits linha a linha (ex.: `"3:110010000"`), ou a forma visual com `#` (preta) e `.` (branca) e linhas separadas por `/` (ex.: `"##./.#./..."`). Ambas descrevem a mesma grade 3×3 com pretas em (1,1), (1,2) e (2,2).

### 1.2 Vizinhança

Duas posições são **vizinhas** se diferem em exatamente uma unidade numa só coordenada (4-vizinhança ortogonal; diagonais não são vizinhas). A lista de vizinhos de p dentro da grade é dada na ordem **cima, baixo, esquerda, direita**, omitindo as posições fora da grade.

### 1.3 API da grade (`kit-autor/grade.py`)

As referências do autor (§5.2) são funções Python que recebem objetos `Grade` com esta interface (e só devem usar esta interface):

| membro | significado |
|---|---|
| `g.n` | lado da grade |
| `g.celula(p)` | 1 se a célula p é preta, 0 se branca (p = `(i, j)`) |
| `g.posicoes()` | lista de todas as posições, linha a linha |
| `g.pretas()` | lista das posições pretas, linha a linha |
| `g.linhas()` | lista de linhas; cada linha é a lista das suas posições, da esquerda para a direita |
| `g.colunas()` | lista de colunas; cada coluna é a lista das suas posições, de cima para baixo |
| `g.vizinhos(p)` | vizinhos ortogonais de p dentro da grade, na ordem cima, baixo, esquerda, direita |
| `g.dentro(p)` | se p está dentro da grade |
| `g.contagem_pretas()`, `g.densidade()` | número e fração de células pretas |
| `g.bits` | tupla dos n² bits, linha a linha |
| `Grade.de_texto(s)`, `g.serializar()`, `g.texto()` | conversões com os formatos de §1.1 |
| `g.transposta()`, `g.reflexao_h()`, `g.reflexao_v()`, `g.rotacao90()`, `g.inverter(p)`, `g.trocar(p, q)` | transformações que devolvem grades novas |
| `g.balde(100)` | índice da partição de instâncias (§2.4) |

### 1.4 Distribuição natural de grades

Quando o ambiente precisa de uma grade "ao acaso" (exemplos de tarefas de função, testes), sorteia p uniformemente em {0,20; 0,35; 0,50; 0,65} e põe cada célula preta com probabilidade p, independentemente. Chama-se a isto a **mistura natural**. Para predicados, o ambiente também constrói positivos e negativos de forma dirigida (§7.2).

## 2. Tipos, formatos e partição de instâncias

### 2.1 Tipos de dados

| tipo | valores |
|---|---|
| `Bool` | verdadeiro / falso |
| `Pos` | posição `(i, j)` da grade corrente |
| `Grade` | grade de lado n |
| `L Pos` | lista (sequência finita, ordenada, com repetições possíveis) de posições |
| `L (L Pos)` | lista de listas de posições |
| `A -> B` | função |

Não há inteiros, caracteres nem outros tipos. Em particular **não há literais de posição nem numerais** em E0: toda posição que um programa manipula vem da grade (§3.2).

### 2.2 Assinaturas de tarefa aceites

Uma tarefa tem um **tipo**, uma **natureza** e uma **comparação**:

| tipo (texto em `tarefas.json`) | natureza | a referência recebe | devolve |
|---|---|---|---|
| `Grade -> Bool` | predicado | `g` | `bool` |
| `Grade -> Pos -> Bool` | funcao | `g, p` | `bool` |
| `Grade -> Pos -> L Pos` | funcao | `g, p` | coleção de posições |
| `Grade -> L Pos -> Bool` | funcao | `g, S` (tupla de posições) | `bool` |
| `Grade -> L Pos -> L Pos` | funcao | `g, S` | coleção de posições |
| `Grade -> L Pos` | funcao | `g` | coleção de posições |
| `L Pos -> L Pos -> Bool` | funcao | `A, B` (tuplas de posições) | `bool` |
| `L Pos -> L Pos -> L Pos` | funcao | `A, B` | coleção de posições |

"Predicado" é exclusivamente o tipo `Grade -> Bool`; tudo o resto é "funcao". Para um resultado `L Pos`, a comparação é `"exata"` (a saída do programa tem de ser a mesma **sequência**: ordem e repetições contam; a referência deve devolver uma lista ou tupla ordenada) ou `"conjunto"` (igualdade de **conjuntos**; a referência pode devolver qualquer coleção, inclusive `set`/`frozenset`). Para `Bool` e `Pos` a comparação é sempre exata.

### 2.3 Argumentos que o ambiente fornece (bateria de entradas)

Nas tarefas de função o ambiente nunca inventa argumentos arbitrários: deriva-os da grade corrente g, sempre pela mesma regra (a **bateria de entradas**), tanto nos exemplos como no oráculo e nos testes:

- `Grade -> Pos -> ·`: todas as posições de g;
- `Grade -> L Pos -> ·`: as listas `()`, a primeira preta (lista de um elemento), a última preta, todas as pretas, todas as posições, cada linha e cada coluna de g (sem repetições);
- `L Pos -> L Pos -> ·`: todos os pares (A, B) com A e B tiradas de {`()`, pretas de cada linha, pretas de cada coluna, todas as pretas} de g (sem repetições);
- `Grade -> ·`: apenas g.

As referências devem ser totais nestes argumentos (e, por prudência, em qualquer lista de posições válidas da grade).

### 2.4 Partição de instâncias

Cada grade tem um **balde** determinístico: os 16 primeiros dígitos hexadecimais do SHA-256 da sua serialização, módulo 100 (`g.balde(100)`). O ambiente usa os baldes para separar os dados sem sobreposição:

| baldes | uso |
|---|---|
| 0–19 | treino: exemplos iniciais e domínio do oráculo de contraexemplos |
| 30–39 | teste interno do ambiente |
| 40–49 | testes ocultos do avaliador em tamanhos n = 5..9 |
| 20–29, 50–99 | não usados nesta avaliação |

Consequência para o autor: os exemplos e contraexemplos que o aprendiz vê vêm só de grades dos baldes 0–19, em tamanhos n ≤ 4 (exaustivamente) e n = 5, 6 (amostras). Um predicado tem de ter **pelo menos 2 grades positivas e 2 negativas** nos baldes 0–19 com n = 3 ou n = 4 (o validador confere); caso contrário o ambiente não consegue formar os exemplos iniciais e a tarefa é inválida.

## 3. A linguagem E0 e a semântica das operações

### 3.1 Programas

Um programa é um termo do cálculo λ simplesmente tipado com as constantes abaixo, escrito em s-expressões:

```
(\ (g Grade) (p Pos) corpo)      função anónima (λ) com dois parâmetros tipados
(f a b)                          aplicação (currificada: (f a b) = ((f a) b))
nome                             constante da tabela E0 ou variável ligada
```

Tipos nos binders: `Grade`, `Pos`, `Bool`, `LP` (= `L Pos`), `LLP` (= `L (L Pos)`), ou as formas `(L Pos)` e `(-> A B)`. Variáveis são identificadores minúsculos. Exemplo de programa do tipo `Grade -> Bool`, que decide se a grade não tem células pretas: `(\ (g Grade) (vazia?@P (pretas g)))`.

**Tamanho** de um programa = número de folhas (ocorrências de constantes e de variáveis) + número de ligadores λ (+ 1 por cada `fix`). O exemplo acima tem tamanho 4. As aplicações não contam.

### 3.2 Tabela de constantes de E0 (36) e semântica exata

Um programa é avaliado numa grade de lado n. As listas têm comprimento máximo F(n) = n⁴: toda operação que constrói listas (cons, concatenar, juntar, uniao) trunca o resultado aos F(n) primeiros elementos. Os **valores por omissão** de cada tipo são: `Bool` falso; `Pos` (1,1); listas vazias; `Grade` a grade toda branca de lado n.

| constante | tipo | semântica |
|---|---|---|
| `celula` | `Grade -> Pos -> Bool` | verdadeiro se a célula p de g é preta |
| `posicoes` | `Grade -> L Pos` | todas as posições, linha a linha: (1,1), (1,2), …, (n,n) |
| `pretas` | `Grade -> L Pos` | as posições pretas, linha a linha |
| `linhas` | `Grade -> L (L Pos)` | as n linhas, de cima para baixo; cada uma é a lista das suas posições da esquerda para a direita |
| `colunas` | `Grade -> L (L Pos)` | as n colunas, da esquerda para a direita; cada uma de cima para baixo |
| `vizinhos` | `Grade -> Pos -> L Pos` | vizinhos ortogonais de p dentro da grade: cima, baixo, esquerda, direita |
| `verdadeiro`, `falso` | `Bool` | constantes |
| `e`, `ou` | `Bool -> Bool -> Bool` | conjunção e disjunção (ambos os argumentos são avaliados) |
| `nao` | `Bool -> Bool` | negação |
| `se@B` | `Bool -> Bool -> Bool -> Bool` | condicional; só o ramo escolhido é avaliado |
| `se@LP` | `Bool -> L Pos -> L Pos -> L Pos` | idem, para listas de posições |
| `se@LLP` | `Bool -> L (L Pos) -> L (L Pos) -> L (L Pos)` | idem, para listas de listas |
| `igualP` | `Pos -> Pos -> Bool` | igualdade de posições |
| `vazio@P` | `L Pos` | lista vazia |
| `vazio@LP` | `L (L Pos)` | lista vazia de listas |
| `cons@P` | `Pos -> L Pos -> L Pos` | acrescenta à cabeça (truncado a F(n)) |
| `cons@LP` | `L Pos -> L (L Pos) -> L (L Pos)` | idem para listas de listas |
| `vazia?@P` | `L Pos -> Bool` | a lista é vazia |
| `vazia?@LP` | `L (L Pos) -> Bool` | idem |
| `cabeca@P` | `L Pos -> Pos` | primeiro elemento; **da lista vazia devolve (1,1)** (valor por omissão) |
| `cabeca@LP` | `L (L Pos) -> L Pos` | primeiro elemento; da lista vazia devolve a lista vazia |
| `cauda@P` | `L Pos -> L Pos` | todos menos o primeiro; da lista vazia devolve a vazia |
| `cauda@LP` | `L (L Pos) -> L (L Pos)` | idem |
| `mapear@P>LP` | `(Pos -> L Pos) -> L Pos -> L (L Pos)` | aplica a função a cada posição, na ordem |
| `filtrar@P` | `(Pos -> Bool) -> L Pos -> L Pos` | mantém, na ordem, as posições que satisfazem o predicado |
| `filtrar@LP` | `(L Pos -> Bool) -> L (L Pos) -> L (L Pos)` | idem para listas de listas |
| `algum@P` | `(Pos -> Bool) -> L Pos -> Bool` | existe elemento que satisfaz (curto-circuito, na ordem) |
| `todos@P` | `(Pos -> Bool) -> L Pos -> Bool` | todos satisfazem (verdadeiro na lista vazia) |
| `todos@LP` | `(L Pos -> Bool) -> L (L Pos) -> Bool` | idem para listas de listas |
| `concatenar@P` | `L Pos -> L Pos -> L Pos` | concatenação (truncada a F(n)) |
| `juntar` | `L (L Pos) -> L Pos` | concatenação de todas as listas, na ordem (truncada) |
| `reverter@LP` | `L (L Pos) -> L (L Pos)` | inverte a ordem das listas |
| `pertence` | `Pos -> L Pos -> Bool` | p ocorre na lista |
| `uniao` | `L Pos -> L Pos -> L Pos` | `uniao A B` = os elementos de B que não estão em A, pela ordem de B, seguidos de A (A inalterada, com as suas repetições); truncado |
| `diferenca` | `L Pos -> L Pos -> L Pos` | os elementos de A que não estão em B, pela ordem de A |

Observações: não existe `mapear` com resultado `Pos`, nem `algum`/`reverter`/`concatenar` para listas de listas, nem `se` para `Pos`, nem igualdade de listas, nem aritmética de posições. Os sufixos `@P`, `@LP`, `@LLP`, `@P>LP` distinguem instâncias monomórficas da mesma operação.

### 3.3 Recursão

E0 tem o formador `fix` (recursão geral) para tipos funcionais: `(fix τ (\ (rec τ) (x α) corpo))`. Sob a semântica finita, uma recursão desdobra-se no máximo F(n) = n⁴ vezes; para além disso o resultado é o valor por omissão do tipo. O procedimento de busca do aprendiz enumera termos com `fix` apenas na forma acima (com `rec` aplicado a argumentos que não contêm `rec`), mas o autor não precisa de usar `fix` nas suas testemunhas (§5.6): qualquer programa bem tipado de E0 é aceitável.

### 3.4 Dificuldade e alcance

Toda avaliação de um programa numa entrada tem um orçamento de 100 000 passos de avaliação (cada nó do termo avaliado conta um passo); um programa que o esgote numa entrada tem saída **indefinida** nessa entrada, e isso conta como discordância com a referência (nunca como acerto).

O procedimento de busca do aprendiz enumera programas por tamanho crescente (ou por custo ponderado das folhas, numa segunda política) com poda de programas observacionalmente equivalentes, com um orçamento de 20 000 candidatos por tarefa e por tentativa. Nesse orçamento, o alcance medido na tabela E0 é de programas de até **cerca de 8 a 9 folhas**; programas maiores em E0 raramente são encontrados. O autor pode usar esta informação para calibrar a dificuldade como entender; não é uma indicação do que deve ser incluído.

## 4. Restrições computacionais

| parâmetro | valor |
|---|---|
| candidatos por tarefa e por tentativa (B) | 20 000 |
| rodadas de contraexemplo por tarefa (K) | 12 |
| passos por avaliação de um programa numa entrada | 100 000 |
| tamanho máximo de programa enumerado | 30 |
| lados de grade dos exemplos iniciais | 3 e 4 |
| domínio do oráculo de contraexemplos | predicados: todas as grades dos baldes 0–19 com n ≤ 4, mais um reservatório fixo de grades n = 5 e 6; funções: todas as grades dos baldes 0–19 com n ≤ 3 e um reservatório de 40 grades n = 4, com a bateria de argumentos (§2.3) |
| testes ocultos do avaliador | grades dos baldes 40–49 com n = 5..9 (mistura natural; para predicados também positivos construídos e negativos de igual densidade) |
| testes ocultos do autor | quaisquer grades com 1 ≤ n ≤ 9 (§5.3) |
| tempo | sem limite de parede por tarefa; o custo é contado em passos de avaliação determinísticos |

## 5. Interface para definir tarefas (formato do pacote)

Um **pacote** é uma pasta com os ficheiros abaixo. O kit tem um pacote de exemplo (`kit-autor/exemplo-pacote/`, três tarefas triviais que só ilustram o formato) e o validador autónomo `validar_pacote.py`, que corre sem nada além do Python padrão.

### 5.1 `tarefas.json`

```json
{
 "nome": "nome-do-benchmark", "versao": "1", "autor": "…",
 "tarefas": [
  {"id": "identificador", "tipo": "Grade -> Pos -> L Pos", "natureza": "funcao",
   "comparacao": "conjunto", "descricao": "texto livre, para leitura humana", "grupo": "etiqueta opcional"}
 ]
}
```

- `id`: letras, dígitos e `_`, até 32 caracteres, começando por letra; único no pacote; não use nomes de constantes de E0;
- `tipo`: uma das oito assinaturas de §2.2, exatamente com essa grafia;
- `natureza`: `"predicado"` para `Grade -> Bool`, `"funcao"` para as restantes;
- `comparacao`: `"exata"` (omissão) ou `"conjunto"` (só para resultado `L Pos`);
- `descricao`: texto livre; **não é mostrado ao aprendiz**, serve ao avaliador e ao relatório;
- `grupo`: etiqueta livre opcional (o avaliador não a interpreta durante a execução);
- a **ordem de listagem** é a ordem em que o avaliador apresenta as tarefas ao aprendiz na execução primária (outras ordens também são executadas).

### 5.2 `referencias.py`

Módulo Python que define `REFERENCIAS = {id: função}`. Cada função recebe os argumentos na ordem do tipo (§2.2) — a grade como objeto `Grade` (§1.3), posições como tuplas `(i, j)`, listas de posições como tuplas de tuplas — e devolve `bool`, uma tupla `(i, j)` ou uma coleção de posições. As funções devem ser **puras, determinísticas e totais** nos argumentos da bateria (§2.3): sem aleatoriedade, sem leitura de ficheiros ou relógio, sem exceções. Pode importar `grade` (o módulo do kit) para construir grades.

Opcionais, recomendados:

- `REFERENCIAS_B = {id: função}`: uma **segunda implementação independente** de cada tarefa (escrita de outra maneira); o validador e o avaliador conferem que as duas coincidem em todas as entradas examinadas. Discordância é erro de integridade.
- `POSITIVOS = {id: função(n, rng) -> Grade | None}`: para predicados cujos positivos são raros na mistura natural, um gerador de grades positivas de lado n a partir de um `random.Random`; o ambiente usa-o para construir exemplos e contraexemplos (o rótulo é sempre conferido pela referência).

### 5.3 `testes_ocultos.json` (opcional, selado)

`{"id": ["n:bits", …], …}`: grades (1 ≤ n ≤ 9) em que o avaliador verificará, **depois** da execução, as hipóteses aceitas de cada tarefa, usando a referência do autor e a bateria de argumentos. O aprendiz nunca as vê.

### 5.4 `testemunhas.json` (opcional, selado)

`{"id": "programa E0", …}`: para cada tarefa, um programa de E0 (sintaxe de §3.1) que o autor acredita resolvê-la. Serve para o avaliador confirmar que a tarefa é exprimível em E0 e registar um limite superior do seu tamanho; é verificado depois da execução e nunca é mostrado ao aprendiz. Não é necessário que seja mínimo.

### 5.5 `MANIFESTO.json`

Gerado por `python3 validar_pacote.py <pasta> --congelar`: lista os ficheiros do pacote com os seus SHA-256 e o **hash do pacote** (SHA-256 das linhas `caminho  sha256` ordenadas). Depois de gerado, nenhum ficheiro pode mudar; o avaliador recusa pacotes cujo hash não confere.

### 5.6 Ficheiro selado livre (opcional)

Qualquer outro ficheiro na pasta (por exemplo `notas-do-autor.md`) é incluído no hash e **não** é lido pelo avaliador durante a execução. O autor pode usá-lo para registar, antes do congelamento, observações sobre o conjunto ou expectativas próprias; é aberto só na análise.

## 6. Requisitos de integridade e congelamento

1. `python3 validar_pacote.py <pasta>` termina com `erros: 0`. O validador confere o formato, a existência e o tipo das referências, determinismo e totalidade em todas as grades com n ≤ 3 e em amostras de n = 4 e 5 com a bateria de argumentos, a não degenerescência (a referência não devolve sempre a mesma saída), a presença de ≥ 2 positivos e ≥ 2 negativos nos baldes 0–19 para n ∈ {3, 4} nos predicados, a coincidência com `REFERENCIAS_B` quando existe, os geradores `POSITIVOS` e os ficheiros selados.
2. Avisos do validador (classe rara na mistura natural; ausência de pares de igual densidade; falta de segunda implementação) não impedem o congelamento, mas o autor deve lê-los: uma tarefa cujo positivo nunca aparece em n = 5..9 terá testes ocultos de uma só classe, assinalados como degenerados no relatório.
3. As referências não podem depender de nada fora dos argumentos (sem estado global, sem aleatoriedade, sem relógio, sem ficheiros).
4. O pacote é congelado com `--congelar` **antes** de ser entregue, e não é alterado depois. Se o avaliador encontrar um erro de integridade (por exemplo, uma tarefa que o ambiente não consegue instanciar), comunica-o ao autor, que entrega uma **nova versão** (novo `versao` em `tarefas.json`, novo hash). Os resultados de cada versão são guardados separadamente; nenhum resultado é substituído em silêncio.
5. Número de tarefas: recomenda-se entre 12 e 30, com pelo menos 8. Não há mínimo por tipo, mas recomenda-se cobrir vários tipos de §2.2.

## 7. Comunicação entre o benchmark e o aprendiz

### 7.1 O que o aprendiz recebe de cada tarefa

- O **tipo** da tarefa (§2.2) e a natureza da comparação. Não recebe o `id`, a `descricao`, o `grupo`, a referência, as testemunhas nem os testes ocultos.
- **Exemplos iniciais**: predicados: 2 grades positivas e 2 negativas dos baldes 0–19, com n = 4 (ou 3), em que os negativos têm, quando possível, o mesmo número de pretas que os positivos (negativos emparelhados em densidade; os positivos vêm do gerador `POSITIVOS` se existir, senão de amostragem com rejeição); funções: 4 pares (argumentos, saída da referência) com grades da mistura natural de n = 3 e 4 dos baldes 0–19 e argumentos da bateria, com saídas variadas (para `Bool`, metade verdadeiro e metade falso quando possível).

### 7.2 O protocolo de rodadas

Em cada tarefa, até K = 12 vezes: o aprendiz propõe um programa consistente com os exemplos que tem; o **oráculo** procura, no seu domínio (§4), a **menor** entrada em que o programa discorda da referência (ordem: lado da grade, número de pretas, ordem lexicográfica dos bits; depois a ordem da bateria) e devolve-a com a saída correta; se não encontra nenhuma, o programa é **aceito**. Uma saída indefinida (orçamento de passos esgotado) conta como discordância. O aprendiz termina a tarefa sem aceitação quando esgota B candidatos ou as K rodadas.

### 7.3 O que o avaliador controla

As referências do autor são a única fonte de rótulos e saídas: o avaliador usa-as para os exemplos, para o oráculo e para os testes ocultos, sem as mostrar ao aprendiz. Todos os pedidos do aprendiz ao oráculo e todos os custos são registados num livro-razão determinístico. Depois da execução, cada programa aceito é verificado em todas as grades com n ≤ 4 (com a bateria), em grades dos baldes 40–49 com n = 5..9 e nos testes ocultos do autor; as discordâncias são reportadas como erros de previsão.

### 7.4 O que não acontece

O autor não recebe informação sobre o desempenho do aprendiz antes de o pacote estar congelado e avaliado. Não há ajuste de tarefas depois de ver resultados; uma nova versão só é pedida por erro de integridade (§6.4).

## 8. Lista de entrega

1. `tarefas.json`, `referencias.py` (com `REFERENCIAS`, e de preferência `REFERENCIAS_B` e, se necessário, `POSITIVOS`).
2. Opcional: `testes_ocultos.json`, `testemunhas.json`, notas seladas.
3. `python3 validar_pacote.py <pasta>` com `erros: 0`; leitura dos avisos.
4. `python3 validar_pacote.py <pasta> --congelar` → `MANIFESTO.json`; comunicar o `hash_pacote`.
5. Não alterar nenhum ficheiro depois disso.
