# Assistente de atendimento técnico

CLI em português que transforma um perfil e um relato de suporte em diagnóstico, passos de resolução, perguntas priorizadas e fluxograma. Cada geração produz um registro JSON. A comparação usa o mesmo cenário nas duas versões e permite à candidata avaliar as respostas lado a lado.

A comparação obrigatória de Rosa foi aprovada pela candidata: v1 e v2 obtiveram **41/60**. Consulte o [relatório com as 24 notas e justificativas](samples/51c126cfcbaa47e28c5274008da4dbdb/relatorio.md).

Para revisar a entrega sem usar uma chave, abra a [matriz de avaliação com os 27 JSONs](PROMPT_ENGINEERING_NOTES.md), o [estudo separado com Hydrogen](experimentos/hydrogen-caio-v22/README.md) e o [checklist de publicação](ENTREGA.md).

## Instalação no Windows

Na raiz do repositório, com Python 3.11 ou superior e PowerShell, execute os comandos abaixo. Se o launcher `py` não encontrar o interpretador, substitua `py -3` por `python` ou pelo caminho de um Python que tenha o módulo venv.

```powershell
py -3 -m venv .venv
$python = ".\.venv\Scripts\python.exe"
& $python -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
& $python -m pytest -q
& $python -m support_assistant.cli customers
& $python -m support_assistant.cli tickets
```

No Linux ou macOS, crie o ambiente com `python3 -m venv .venv`, ative com `source .venv/bin/activate` e use `python` no lugar de `& $python`. Os testes substituem a camada HTTP ou o provedor e usam diretórios temporários.

Para gerar conteúdo, crie uma chave no [Google AI Studio](https://aistudio.google.com/apikey), selecione um projeto com cota gratuita e preencha `LLM_API_KEY` no arquivo local `.env`. As variáveis do processo têm precedência sobre o arquivo. A temperatura padrão é 0,3 para reduzir a variação entre respostas. O limite é de 4096 tokens por geração e o timeout de rede é de 45 segundos.

O padrão provisório é `gemini-3.5-flash-lite`. Esse modelo produziu todas as 27 amostras do experimento principal. A disponibilidade e a cota dependem do projeto Gemini. O campo `LLM_MODEL` permite selecionar o modelo. A CLI pede a versão de prompt quando ela é omitida em `generate`; a escolha de um padrão único aguarda revisão.

## Interface visual opcional

Na raiz do projeto, instale a dependência opcional uma vez com `& .\.venv\Scripts\python.exe -m pip install -r requirements-ui.txt`. Para abrir a interface no Windows, execute:

```powershell
& .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Abra o endereço local indicado no terminal. Para demonstrar o projeto sem chave, selecione **Comparar prompts** e abra a comparação original de Rosa. Troque o conteúdo para ver cada par de respostas, as notas e as justificativas. O **Histórico** reúne as amostras versionadas e as execuções locais, com preferência pelo registro local quando o ID coincide.

Em **Gerar resposta**, escolha o cliente, o ticket, a versão e o tipo de conteúdo. O botão aciona o mesmo gerador da CLI, que verifica o cache e usa o Gemini quando precisa de uma nova resposta. A chave fica no ambiente do servidor. Para encerrar a interface, pressione Ctrl+C no terminal.

## Uso

A [revisão v2.2](REVISAO_V2_2.md) preserva as condições e conclusões daquela rodada. A decisão proposta após comparar as quatro versões está nas [notas consolidadas](PROMPT_ENGINEERING_NOTES.md).

Para reproduzir os experimentos registrados, use `LLM_MODEL=gemini-3.5-flash-lite` no arquivo local ou defina a variável no PowerShell. Neste projeto, a API recusou o 2.5 Flash para novos usuários (404) e o 3.8 Flash retornou 503. Os JSONs identificam o modelo efetivamente solicitado em cada chamada.

```powershell
$env:LLM_MODEL = "gemini-3.5-flash-lite"
$env:LLM_TEMPERATURE = "0.3"
$env:LLM_MAX_TOKENS = "4096"
& $python -m support_assistant.cli generate --customer c1 --ticket t1 --type all --prompt-version v2.1 --no-cache
& $python -m support_assistant.cli generate --customer c2 --ticket t1 --type diagnosis --prompt-version v2.1 --no-cache
& $python -m support_assistant.cli generate --customer c2 --ticket t1 --type steps --prompt-version v2.1 --no-cache
& $python -m support_assistant.cli compare --customer c1 --ticket t2 --type questions --versions v2 v2.1
& $python -m support_assistant.cli generate --customer c1 --ticket t2 --type questions --prompt-version v2.1
```

A última linha recupera o resultado recém-comparado do cache. A v1 estabelece a referência simples; a v2 adapta a comunicação ao perfil; a v2.1 acrescenta instruções para calibrar hipóteses, ensinar os testes, solicitar observações e alinhar os ramos do fluxo. Veja os [casos, amostras e avaliações provisórias](REVISAO_V2_1.md).

O catálogo inclui Rosa (`c1`, leiga, telefone) e Caio (`c2`, avançado, chat). O ticket `t1` relata queda de Wi-Fi na sala. O `t2` descreve um aplicativo que fecha e deixa aparelho, sistema e versão em aberto. Use o ID cadastrado ou escreva o relato entre aspas. Os comandos de geração pedem os campos omitidos no terminal.

```powershell
& $python -m support_assistant.cli generate --customer c1 --ticket t1 --type steps --prompt-version v2
& $python -m support_assistant.cli generate --customer c1 --ticket t1 --type steps --prompt-version v2
& $python -m support_assistant.cli generate --customer c2 --ticket "O aplicativo fecha ao abrir" --type questions --prompt-version v1
& $python -m support_assistant.cli compare --customer c1 --ticket t1 --versions v1 v2 --type all
& $python -m support_assistant.cli history --customer c1 --version v2 --type diagnosis
```

A segunda geração equivalente exibe `cache hit` e o caminho do novo registro. Os tipos são `diagnosis`, `steps`, `questions`, `flow` e `all`. Compare gera oito respostas para `all`, sempre com chamadas novas. Para observar outro perfil, repita com `--customer c2 --ticket t1 --type steps`. Somente compare versões dentro do mesmo cenário.

Copie o identificador exibido por compare para consultar e avaliar o grupo:

```powershell
$grupo = Read-Host "ID da comparação"
& $python -m support_assistant.cli history --comparison-id $grupo
& $python -m support_assistant.cli evaluate --comparison-id $grupo
```

Para cada resposta, avalie **clareza** (organização e ausência de ambiguidade), **adequação ao nível do cliente** (vocabulário e profundidade) e **acionabilidade** (próximo passo identificável). Use 1 para insuficiente, 2 para fraco, 3 para adequado, 4 para bom e 5 para excelente. Justifique cada nota com um trecho da resposta. Execute o mesmo comando para editar. Para importar notas revisadas, acrescente `--file notas.json`. O objeto JSON deve mapear cada ID de execução do grupo a um objeto com `clarity`, `customer_fit` e `actionability`. Cada critério contém `score` inteiro e `justification` textual.

## Organização e persistência

| Caminho | Responsabilidade |
|---|---|
| data/customers.json e data/tickets.json | Perfis e relatos de exemplo |
| support_assistant/cli.py | Entrada, seleção e exibição de resultados |
| support_assistant/prompts.py, v1.txt e v2.txt | Instruções de cada tarefa, contexto e contrato JSON |
| support_assistant/generators.py | Quatro geradores, validação, reparo e reaproveitamento |
| support_assistant/gemini.py | Configuração e chamada HTTP com timeout e até três tentativas para 429/5xx |
| support_assistant/storage.py | Leitura, filtros e escrita atômica por arquivo |
| support_assistant/evaluation.py | Rubrica, exportação e relatório |
| tests/ | Testes com dados controlados |
| samples/ | Exportações das comparações reais |

O histórico local usa um arquivo por execução em `data/history/<id>.json`. Cada arquivo registra horário UTC, perfil, ticket, tarefa, versão, configurações, provedor, modelo solicitado, saída, cache, latência, uso informado pelo Gemini, ID da comparação e avaliação. Falhas de geração registram o erro com saída nula. A resposta inválida recebe uma tentativa de reparo.

O cache procura o registro válido mais recente pelo SHA-256 do JSON canônico do perfil, ticket, tipo, versão, provedor, modelo, temperatura e limite de tokens. `--no-cache` ignora o cache e exclui o novo resultado das consultas futuras. `--refresh` gera um novo resultado que passa a ser o preferido. Ao alterar instruções, versione o prompt ou use refresh. O histórico é adequado para experimentos pequenos, pois a consulta lê os arquivos locais. Chamadas simultâneas equivalentes podem consumir duas requisições.

A comparação exporta os registros e uma tabela em `samples/<comparison_id>/relatorio.md`. A avaliação atualiza os JSONs e o relatório. A validação do formato detecta campos e tipos incorretos, mas a correção técnica, a coerência do fluxo e a adequação ao cliente dependem da revisão humana. Uma execução por versão permite descrever diferenças observadas naquele caso, sem estabelecer superioridade geral.
