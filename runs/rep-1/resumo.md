# Replicação — sementes [10003, 10004, 10005, 10006], políticas ['tamanho', 'unigrama'], B = 20000

| política \| braço | sementes | tarefas aceitas (min/med/max) | aceitas por tarefa | cumul. até T3 (min/med/max) | com reutilização | falhas |
|---|---|---|---|---|---|---|
| tamanho|L-fix | 4 | 1/1.0/1 | {'vizPretos': 4, 'expandir': 0, 'ParAdjacente': 0, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 211,476,680/259,456,734/261,342,020 | 0 | 0 |
| tamanho|L-lib | 4 | 1/1.0/1 | {'vizPretos': 4, 'expandir': 0, 'ParAdjacente': 0, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 211,476,773/259,456,827/261,342,113 | 0 | 0 |
| tamanho|L-lib+f | 4 | 3/3.0/3 | {'vizPretos': 4, 'expandir': 4, 'ParAdjacente': 4, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 14,308,248/14,533,838/14,738,947 | 4 | 0 |
| tamanho|L-lib+f/controle | 4 | 2/2.0/2 | {'vizPretos': 0, 'expandir': 0, 'ParAdjacente': 0, 'NenhumaIsolada': 0, 'pretasColuna1': 4, 'semLinha1': 4} | 90,784,455/101,628,068/102,261,360 | 0 | 0 |
| tamanho|L-lib+f/lesao | 4 | 2/2.0/2 | {'vizPretos': 4, 'expandir': 4, 'ParAdjacente': 0, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 103,811,128/150,314,625/150,592,183 | 0 | 0 |
| unigrama|L-fix | 4 | 3/3.0/3 | {'vizPretos': 4, 'expandir': 4, 'ParAdjacente': 4, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 268,369,379/271,603,607/272,894,356 | 0 | 0 |
| unigrama|L-lib | 4 | 3/3.0/3 | {'vizPretos': 4, 'expandir': 4, 'ParAdjacente': 4, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 268,830,222/271,727,188/273,328,987 | 0 | 0 |
| unigrama|L-lib+f | 4 | 3/3.0/3 | {'vizPretos': 4, 'expandir': 4, 'ParAdjacente': 4, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 27,466,397/27,606,815/28,366,527 | 4 | 0 |
| unigrama|L-lib+f/controle | 4 | 2/2.0/2 | {'vizPretos': 0, 'expandir': 0, 'ParAdjacente': 0, 'NenhumaIsolada': 0, 'pretasColuna1': 4, 'semLinha1': 4} | 275,695,429/338,686,810/341,598,133 | 0 | 0 |
| unigrama|L-lib+f/lesao | 4 | 3/3.0/3 | {'vizPretos': 4, 'expandir': 4, 'ParAdjacente': 4, 'NenhumaIsolada': 0, 'pretasColuna1': 0, 'semLinha1': 0} | 99,164,991/99,316,669/101,042,627 | 0 | 0 |

Vereditos (critério central de cinco condições) por política: {"tamanho": [true, true, true, true], "unigrama": [true, true, true, true]}

## Hipóteses aceitas distintas por tarefa
- tamanho|L-fix / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- tamanho|L-lib / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- tamanho|L-lib+f / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- tamanho|L-lib+f / expandir: `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)`
- tamanho|L-lib+f / ParAdjacente: `λx0. nao (vazia?@P (abs2 x0 (pretas x0)))`
- tamanho|L-lib+f/controle / pretasColuna1: `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))`
- tamanho|L-lib+f/controle / semLinha1: `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))`
- tamanho|L-lib+f/lesao / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- tamanho|L-lib+f/lesao / expandir: `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)`
- unigrama|L-fix / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- unigrama|L-fix / expandir: `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))`
- unigrama|L-fix / ParAdjacente: `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))`
- unigrama|L-lib / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- unigrama|L-lib / expandir: `λx0 x1. filtrar@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) x1))`
- unigrama|L-lib / ParAdjacente: `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))`
- unigrama|L-lib+f / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- unigrama|L-lib+f / expandir: `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)`
- unigrama|L-lib+f / ParAdjacente: `λx0. algum@P (celula x0) (abs2 x0 (pretas x0))`
- unigrama|L-lib+f/controle / pretasColuna1: `λx0 x1. filtrar@P (celula x0) (cabeca@LP (colunas x0))`
- unigrama|L-lib+f/controle / semLinha1: `λx0 x1. diferenca x1 (cabeca@LP (linhas x0))`
- unigrama|L-lib+f/lesao / vizPretos: `λx0 x1. filtrar@P (celula x0) (vizinhos x0 x1)`
- unigrama|L-lib+f/lesao / expandir: `λx0 x1. juntar (mapear@P>LP (abs1 x0) x1)`
- unigrama|L-lib+f/lesao / ParAdjacente: `λx0. algum@P (celula x0) (juntar (mapear@P>LP (vizinhos x0) (pretas x0)))`
