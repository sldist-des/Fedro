# Notas do autor — benchmark "grades-e0-independente", versão 1

Escritas antes do congelamento. Este ficheiro é selado e não é lido pelo avaliador durante a execução.

## 1. Fontes e isolamento

O conjunto foi construído só a partir do contrato público v1.0 e do kit do autor (validador, `grade.py`,
pacote de exemplo), tal como vinham na mensagem inicial da sessão. Não consultei nenhum repositório, página
web ou outro material, e não tentei adivinhar que tarefas o projeto já usou. Os problemas são escolhas minhas:
operações "naturais" sobre grades binárias e listas de posições, com tamanhos de programa em E0 bem espalhados.

## 2. Organização do conjunto

28 tarefas, todos os oito tipos de §2.2:

| tipo | n.º | tarefas |
|---|---|---|
| `Grade -> Bool` | 7 | todaLinhaTemPreta, colunaVazia, algumaLinhaCheia, semPretaIsolada, semPretasAdjacentes, pretasEmDomino, pretasConexas |
| `Grade -> Pos -> Bool` | 2 | naBorda, linhaTemPretaEm |
| `Grade -> Pos -> L Pos` | 4 | vizinhosPretos, linhaDaPosicao, cruzDaPosicao, componenteDe |
| `Grade -> L Pos -> Bool` | 2 | contemTodasPretas, tocaPreta |
| `Grade -> L Pos -> L Pos` | 3 | complementoDe, brancasDaLista, vizinhancaExterna |
| `Grade -> L Pos` | 5 | ultimaLinha, pretasPorColunas, pretasOrdemInversa, colunasBrancas, bordaPreta |
| `L Pos -> L Pos -> Bool` | 2 | contidoEm, mesmoConjunto |
| `L Pos -> L Pos -> L Pos` | 3 | intersecaoOrdenada, juntarSemRepetir, diferencaSimetrica |

O campo `grupo` é um nível de dificuldade definido pelo tamanho da MINHA testemunha (que não é
necessariamente mínima):

- `nivel1`: testemunha de tamanho ≤ 8 (12 tarefas);
- `nivel2`: tamanho 9–12 (12 tarefas);
- `nivel3`: tamanho 13–22 (2 tarefas: cruzDaPosicao 15, pretasEmDomino 22);
- `nivel4`: exige recursão (`fix`) na minha testemunha (2 tarefas: pretasConexas e componenteDe, tamanho 37).

Tamanhos das testemunhas (contagem minha, ver §4): ultimaLinha 5, contidoEm 6, complementoDe 6,
brancasDaLista 6, todaLinhaTemPreta 7, pretasPorColunas 7, intersecaoOrdenada 7, contemTodasPretas 7,
juntarSemRepetir 7, vizinhosPretos 8, colunaVazia 8, linhaDaPosicao 8, naBorda 9, diferencaSimetrica 9,
algumaLinhaCheia 9, pretasOrdemInversa 10, linhaTemPretaEm 11, semPretaIsolada 11, colunasBrancas 11,
mesmoConjunto 11, tocaPreta 11, bordaPreta 12, vizinhancaExterna 12, semPretasAdjacentes 12,
cruzDaPosicao 15, pretasEmDomino 22, pretasConexas 37, componenteDe 37.

Ordem de listagem: aproximadamente crescente em dificuldade, intercalando tipos, para que a execução
primária seja um percurso do fácil ao difícil. A ordem foi decidida antes de qualquer informação sobre o
aprendiz (não tenho nenhuma).

## 3. Expectativas (registadas antes da avaliação)

- Com o alcance anunciado (§3.4: cerca de 8–9 folhas), espero que a maioria das tarefas `nivel1` seja
  aceite, uma parte das `nivel2` também (sobretudo as de 9–10), e que `nivel3`/`nivel4` raramente o sejam
  sem algum mecanismo de reutilização entre tarefas. As tarefas de `nivel2`/`nivel3` foram pensadas para que
  sub-termos de tarefas anteriores (p. ex. `(filtrar@LP (pertence p) (linhas g))`, `(filtrar@P (celula g)
  (vizinhos g p))`, `(algum@P (celula g) ...)`) reapareçam em tarefas posteriores: linhaDaPosicao →
  linhaTemPretaEm → cruzDaPosicao; vizinhosPretos → semPretaIsolada → semPretasAdjacentes → pretasEmDomino;
  vizinhancaExterna → componenteDe. Isto é uma propriedade do meu conjunto, não uma hipótese sobre o sistema.
- Algumas tarefas admitem programas mais curtos do que as minhas testemunhas (p. ex. brancasDaLista com
  `diferenca`; talvez semPretasAdjacentes com outra composição). Os tamanhos acima são limites superiores.
- Tarefas com armadilhas de ordem (`exata`): pretasPorColunas, pretasOrdemInversa, colunasBrancas,
  juntarSemRepetir (que difere de `uniao` precisamente na ordem), intersecaoOrdenada.

## 4. Decisões e dúvidas sobre o contrato

1. **Tamanho com λ de vários parâmetros.** O contrato diz "+ número de ligadores λ". Em
   `(\ (g Grade) (p Pos) corpo)` contei 2 (um por parâmetro, leitura currificada). Se o avaliador contar 1
   por λ sintático, os meus tamanhos das tarefas de dois argumentos baixam 1. Em `fix` contei +1, e o
   ligador `rec` e o parâmetro como 2 ligadores.
2. **Aviso do validador sobre `->`.** As testemunhas de pretasConexas e componenteDe usam
   `(fix (-> LP LP) (\ (rec (-> LP LP)) (x LP) ...))`, exatamente a forma de §3.3 com tipos de §3.1. O
   validador assinala `->` como "símbolo fora de E0" porque a sua lista de tokens não inclui `->`; julgo que
   é um falso positivo (a sintaxe `(-> A B)` está em §3.1).
3. **Interpretador próprio.** Para conferir as testemunhas escrevi um interpretador E0 (fora do pacote) com
   a semântica de §3 como a li: aplicação currificada, `se@*` preguiçoso, truncamento a n⁴, `fix` com no
   máximo n⁴ desdobramentos e valor por omissão depois disso. Todas as 28 testemunhas coincidem com
   `REFERENCIAS` em todas as grades com n ≤ 3 e em 15 grades naturais por n = 4..9, com a bateria completa.
   A minha contagem de passos (um por nó avaliado, primitivas a custo 1 independentemente do comprimento da
   lista) deu no máximo ~900 passos; se o avaliador contar o trabalho interno das primitivas, as testemunhas
   com `fix` (cada iteração faz `diferenca`/`uniao` quadráticas) podem custar muito mais em n = 9 — penso que
   continuam abaixo de 100 000, mas não o posso garantir sem o avaliador. Isto afeta só as testemunhas, não as
   referências.
4. **Semântica de `uniao`.** Segui literalmente §3.2: `uniao A B` = (B \ A pela ordem de B) ++ A. A tarefa
   juntarSemRepetir (B ++ (A \ B)) foi escolhida por ser parecida mas diferente na ordem.
5. **Convenções vácuas.** Nos predicados "toda preta tem…" (semPretaIsolada, pretasEmDomino) e em
   pretasConexas, a grade sem pretas é positiva. Em componenteDe, p branca dá conjunto vazio.
   Em bordaPreta, os limites da grade não contam como brancos (uma preta de canto cujos vizinhos dentro da
   grade são todos pretos não está na borda).
6. **Totalidade fora da bateria.** As referências são totais em quaisquer listas de posições válidas (com
   repetições, em qualquer ordem). intersecaoOrdenada preserva as repetições de A; complementoDe e
   brancasDaLista estão definidas para qualquer S.
7. **Comparação exata e tipo do contentor.** O validador compara REFERENCIAS e REFERENCIAS_B com `==`
   nas tarefas `exata`; por isso ambas devolvem `list` nessas tarefas (uma tupla e uma lista iguais
   seriam dadas como diferentes). Nas tarefas `conjunto` devolvem `set`/`frozenset`.
8. **Aviso de classe única (pretasEmDomino).** Em grades naturais de n = 6 o positivo quase nunca aparece
   (freq. 0,00 em 300); em n = 5 é 0,003. Há gerador em POSITIVOS (taxa 1,0), e os meus testes ocultos
   incluem 4 positivos e 4 negativos em n = 5..9. Mantive a tarefa porque o contrato diz que o ambiente usa
   positivos construídos também nos testes do avaliador; se mesmo assim os testes dos baldes 40–49 forem de
   uma só classe, o relatório assinalará degenerescência — aceito isso.
9. **Requisito de 2+2 nos baldes 0–19.** Conferido pelo validador para os 7 predicados (o mais apertado é
   pretasEmDomino: 5 positivos em n = 3, 61 em n = 4).
10. **POSITIVOS** só para os três predicados com positivos raros em n grande (semPretasAdjacentes,
    pretasEmDomino, pretasConexas). O gerador de dominós devolve `None` para n = 1 (impossível colocar um
    dominó; a grade vazia seria um positivo trivial).

## 5. Testes ocultos do autor

`testes_ocultos.json` foi gerado por um script meu com semente fixa (20261030): por predicado, 4 positivos
e 4 negativos em n = 5..9 (negativos de densidade próxima dos positivos quando possível), mais uma grade
toda branca e uma toda preta; por função, 6 grades naturais em n = 5..9, a toda branca, a toda preta e
uma grade com uma só preta. Total 259 grades (7 × 10 + 21 × 9).

## 6. Verificação do kit

Os SHA-256 dos sete ficheiros do kit recriados coincidem com os listados. O `MANIFESTO.json` do exemplo só
coincide sem quebra de linha final (o `json.dump` do validador não a escreve), ao contrário da nota geral
"cada um termina com uma única quebra de linha final"; recriei-o sem ela.
