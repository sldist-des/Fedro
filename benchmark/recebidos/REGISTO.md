# Registo de pacotes recebidos do autor externo

| data | nome | versão | hash do pacote | validação | erros de integridade comunicados | registros de execução |
|---|---|---|---|---|---|---|

## Envios ao autor externo

| data (UTC) | destinatário | sessão | conteúdo enviado | hash do conjunto enviado |
|---|---|---|---|---|
| 2026-10-30 17:21 | Claude Opus 5.5, sessão separada sem repositório (`config:no-git-repo`) | `session_01Cs7W3uj1L2HYX9rKqMuDc4` | `contrato-publico.md` (sha256 1d936b27…) e `kit-autor/` (validar_pacote.py 6f4b096a…, grade.py fadab8dc…, exemplo-pacote: tarefas.json debb17f3…, referencias.py 074becaf…, testes_ocultos.json 08235aef…, testemunhas.json a38a9c13…, MANIFESTO.json 3d387973…), transcritos na mensagem inicial com os SHA-256 para conferência pelo autor | 458eff6fb7d9c8d203259572030c5ee5511d330d29580df3ed05d7ee4723d7b0 (sha256 das linhas `caminho\nsha256` dos 8 ficheiros) |

Instruções dadas ao autor (além do contrato): recriar o kit e conferir os SHA-256; construir o pacote; validar e congelar com `validar_pacote.py --congelar`; entregar todos os ficheiros na íntegra na mensagem final (único canal de entrega); isolamento total (sem repositórios, GitHub, web ou outros ficheiros; sem perguntas; decisões registadas em `notas-do-autor.md`). Limitação declarada: o isolamento é procedimental (instrução ao autor) e por ausência de repositório na sessão; não é uma barreira técnica à rede.

Nenhum pacote recebido até 2026-10-30 17:21 UTC. Cada pacote recebido é copiado para `benchmark/recebidos/<nome>-v<versão>/` sem alterações e a sua linha é acrescentada aqui antes de qualquer execução (protocolo, §2).
