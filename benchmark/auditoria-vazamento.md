# Auditoria de vazamento — contrato público e kit do autor

**NÃO ENVIAR ao autor externo**: este relatório lista os termos proibidos.

## Ficheiros auditados (os únicos a enviar)

- `benchmark/contrato-publico.md`: 0 violações
- `benchmark/kit-autor/validar_pacote.py`: 0 violações
- `benchmark/kit-autor/grade.py`: 0 violações
- `benchmark/kit-autor/exemplo-pacote/tarefas.json`: 0 violações
- `benchmark/kit-autor/exemplo-pacote/referencias.py`: 0 violações
- `benchmark/kit-autor/exemplo-pacote/testes_ocultos.json`: 0 violações
- `benchmark/kit-autor/exemplo-pacote/testemunhas.json`: 0 violações
- `benchmark/kit-autor/exemplo-pacote/MANIFESTO.json`: 0 violações

## Violações: 0

Nenhuma.

## Verificação automática

- 65 identificadores proibidos (tarefas do currículo, famílias de transferência, escada do piloto, conceitos do registo, nomes de entradas de biblioteca), com fronteira de palavra;
- 38 radicais de mecanismo/resultado (case-insensitive), com exceções de palavra ['degradar', 'grade', 'grades'];
- identificadores que coincidem com palavras comuns e são aceites fora de código: ['passo'].

### Identificadores proibidos

`CantoSupEsq`, `ColunaDoisVazia`, `ColunasIguais`, `Diagonal`, `DoisSeparados`, `ExisteCompContemCanto`, `ExisteCompMin3`, `ExisteCompReto`, `ExisteCompTocaBorda`, `ExistePreta`, `Igual_col1_colN`, `Igual_linha1_linhaN`, `Igual_metadeEsq_metadeDir`, `LinhaOcupada`, `LinhasIguais`, `MaiorCompPeloMenosLinha1`, `MaiorTocaBorda`, `NenhumaIsolada`, `NoMax_col1_colN`, `NoMax_colN_col1`, `NoMax_linha1_linhaN`, `NoMax_linhaN_linha1`, `NoMax_metadeDir_metadeEsq`, `NoMax_metadeEsq_metadeDir`, `NoMaximoDois`, `NumCompIgualCol1`, `NumCompIgualLinha1`, `ParAdjacente`, `PeloMenosDois`, `PrimeiraUltimaIguais`, `TodosCompReto`, `TodosCompTocaBorda`, `TodosMesmoTamanho`, `TopoCheio`, `TresComponentes`, `UmComponente`, `abs1`, `abs2`, `abs3`, `abs4`, `abs5`, `abs6`, `abs7`, `abs8`, `abs9`, `absExp`, `absViz`, `componenteDe`, `descartar`, `duasVizinhas`, `expandir`, `expandir2`, `fecho`, `fronteira`, `isoladaP`, `mesmoNumero`, `noMaximo`, `passo`, `pretasColuna1`, `pretasComVizinha`, `pretasDe`, `pretasUltimaColuna`, `semColuna1`, `semLinha1`, `vizPretos`

### Radicais proibidos

`bibliotec`, `abstra`, `reutiliz`, `reuso`, `transfer`, `promo`, `compress`, `lesão`, `lesao`, `currícul`, `curricul`, `autodirig`, `consolid`, `operação intermedi`, `operacao intermedi`, `L-fix`, `L-lib`, `unigrama`, `no-go`, `NO-GO`, `documento 0`, `docs/0`, `doc. 0`, `experimento mínimo`, `experimento minimo`, `replica`, `veredito`, `H-B1`, `H-B2`, `H-B3`, `bootstrap`, `emerg`, `degrau`, `escada`, `Fedro`, `Opus`, `Fable`, `Claude`

## Verificação manual (lista de conferência)

1. O contrato descreve só o ambiente, os tipos, as primitivas de E0 e a sua semântica, as restrições computacionais, a interface, a integridade e a comunicação (contrato §1–§8).
2. Nenhuma solução, nenhum programa de referência das nossas tarefas, nenhum nome de entrada de biblioteca, nenhum número de resultado.
3. Os programas em código nos ficheiros enviados (2: ['(\\ (g Grade) (vazia?@P (pretas g)))', '(\\ (g Grade) (celula g (cabeca@P (posicoes g))))']) não são α-equivalentes a nenhuma hipótese aceita em qualquer registro de runs/, a nenhuma entrada de biblioteca registada nem a nenhum programa de referência interno (conferido automaticamente: tipo de violação 'programa-e-solucao-conhecida').
4. As tarefas do pacote de exemplo são triviais e não se parecem com nenhuma tarefa nossa (primeira célula preta; ser canto; identidade).
5. O aprendiz é descrito apenas como 'um sistema de síntese de programas em E0 que pode manter estado interno entre tarefas'.
6. A capacidade de busca é declarada como alcance medido da linguagem base (≈ 8–9 folhas), sem dizer o que gostaríamos que fosse resolvido.
