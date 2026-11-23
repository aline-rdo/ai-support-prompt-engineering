# Assistente de Atendimento Técnico com IA

## Visão geral

A aplicação transforma um relato de suporte em orientações adaptadas ao nível técnico, ao estilo de comunicação e ao canal de atendimento do cliente. A CLI e a interface Streamlit usam os mesmos geradores Python. Para explorar o projeto sem uma chave de API, abra a comparação histórica de Rosa no Streamlit.

## Funcionalidades

- **Perfis e tickets.** Os catálogos JSON incluem quatro clientes fictícios e três tickets. É possível cadastrar exemplos editando os catálogos ou informar um relato livre na geração. O relato livre integra aquela execução.
- **Quatro conteúdos.** O diagnóstico distingue hipóteses e evidências. Os passos apresentam ações, resultados esperados e alternativas. As perguntas priorizam informações faltantes. O fluxograma combina uma representação ASCII e decisões estruturadas.
- **Prompts versionados.** Cada execução identifica a versão escolhida. A comparação gera respostas para duas versões sob o mesmo perfil, ticket, modelo e parâmetros.
- **Avaliação humana.** Cada resposta recebe três notas de 1 a 5, com justificativas para clareza, adequação ao cliente e acionabilidade.
- **Histórico e cache.** Cada execução grava um JSON local com entrada, saída, horário UTC, versão, modelo, configurações e dados de uso disponíveis. O cache reutiliza respostas válidas para entradas e configurações equivalentes.
- **Duas interfaces.** O Streamlit permite gerar, comparar registros históricos lado a lado e filtrar execuções. A CLI também permite criar comparações e registrar avaliações.

## Tecnologias

Python 3.11+, argparse, API Gemini via HTTP com requests, python-dotenv, Streamlit opcional e pytest. Os registros são arquivos JSON no sistema de arquivos local.

## Pré-requisitos

Python 3.11 ou superior com pip e venv. A instalação inicial das dependências requer acesso aos pacotes. Para gerar respostas novas, é necessária uma chave com acesso ao modelo Gemini configurado. A consulta às amostras e os testes funcionam sem chave.

## Instalação

No Windows, abra o PowerShell na raiz do repositório e execute:

```powershell
py -3 -m venv .venv
$python = ".\.venv\Scripts\python.exe"
& $python -m pip install -r requirements-ui.txt
```

No Linux ou macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-ui.txt
```

Para instalar somente a CLI, use `requirements.txt` no comando de instalação. Nos exemplos seguintes, use `python` no lugar de `& $python` em ambientes ativados. Em uma nova sessão do PowerShell, defina novamente a variável `$python` na raiz do projeto.

## Configuração

Para habilitar a geração, copie o modelo de configuração e preencha `LLM_API_KEY` no arquivo local `.env`. No PowerShell:

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

No Linux ou macOS, use `cp -n .env.example .env`. Variáveis já definidas no processo têm precedência. O arquivo de exemplo mantém a chave vazia.

| Variável | Valor de exemplo | Finalidade |
|---|---|---|
| LLM_API_KEY | vazio | Credencial da API Gemini, usada no servidor local |
| LLM_PROVIDER | gemini | Provedor implementado |
| LLM_MODEL | gemini-3.5-flash-lite | Modelo padrão provisório utilizado nas 27 amostras |
| LLM_TEMPERATURE | 0.3 | Temperatura de geração |
| LLM_MAX_TOKENS | 4096 | Limite de tokens de saída solicitado |
| LLM_TIMEOUT_SECONDS | 45 | Timeout da requisição HTTP, em segundos |

## Execução

### Interface Streamlit

```powershell
& $python -m streamlit run app.py --server.address 127.0.0.1
```

Abra o endereço indicado no terminal. Em **Comparar prompts**, selecione **Rosa · comparação original · v1 × v2** e escolha uma tarefa para consultar as duas respostas e suas justificativas. **Histórico** combina as amostras versionadas com os registros locais por ID. **Gerar resposta** aciona o backend após a seleção explícita da versão e o clique no botão. Encerre o servidor com Ctrl+C.

### CLI

Para consultar catálogos e o histórico local:

```powershell
& $python -m support_assistant.cli customers
& $python -m support_assistant.cli tickets
& $python -m support_assistant.cli history --customer c1 --version v2 --type diagnosis
```

Em uma instalação nova, o histórico da CLI começa vazio. As evidências distribuídas estão em `samples/`.

Para gerar uma orientação ou iniciar uma **nova** comparação com o Gemini:

```powershell
& $python -m support_assistant.cli generate --customer c1 --ticket t1 --type steps --prompt-version v2
& $python -m support_assistant.cli generate --customer c2 --ticket "O aplicativo fecha ao abrir" --type questions --prompt-version v2.2
& $python -m support_assistant.cli compare --customer c1 --ticket t1 --type all --versions v1 v2
```

Os tipos aceitos para geração são `diagnosis`, `steps`, `questions`, `flow` e `all`. Uma comparação com `all` solicita oito respostas novas. Na geração individual, `--refresh` atualiza o cache e `--no-cache` exclui o resultado do reaproveitamento.

Para avaliar uma **comparação local nova**, use o ID exibido por `compare`:

```powershell
$grupo = Read-Host "ID da nova comparação"
& $python -m support_assistant.cli history --comparison-id $grupo
& $python -m support_assistant.cli evaluate --comparison-id $grupo
```

A avaliação salva as notas e justificativas no histórico e atualiza a exportação da comparação. Para importar uma revisão, acrescente `--file notas.json` a `evaluate`. O arquivo deve associar cada ID de execução a `clarity`, `customer_fit` e `actionability`, cada um com `score` inteiro e `justification` textual.

## Estrutura do projeto

```text
app.py                    Navegação e interação no Streamlit
visualizacao.py           Apresentação das respostas e da rubrica
support_assistant/
  cli.py                  Comandos, seleção de entradas e avaliação
  prompts.py              Montagem da instrução, contexto e contrato de saída
  v*.txt, v*.json         Instruções versionadas usadas em execução
  generators.py           Geração, validação, reparo e cache
  gemini.py               Configuração e cliente HTTP
  storage.py              Leitura, filtros e gravação local
  evaluation.py           Validação da rubrica e exportação
data/                     Catálogos de clientes e tickets, propostas de notas
  history/                Execuções locais, fora do Git
samples/                  Respostas reais e relatórios por comparação
experimentos/             Investigação complementar com o Hydrogen
tests/                    Testes do backend, da CLI e da interface
```

## Engenharia de prompt e experimentos

| Versão | Estratégia |
|---|---|
| v1 | Estabelece a referência com instruções curtas por tarefa. |
| v2 | Explicita adaptação ao perfil, ordenação de passos e distinção entre hipótese e evidência. |
| v2.1 | Detalha calibração de hipóteses, orientação dos testes e correspondência dos ramos do fluxo. |
| v2.2 | Prioriza testes de isolamento e exige fundamentação para hipóteses, medições e procedimentos. |

Na comparação original de Rosa, **v1 e v2 obtiveram 41/60**. A v2 melhorou aspectos de personalização, com regressões de acionabilidade e consistência do fluxograma. As 24 notas aprovadas correspondem a oito respostas do mesmo cenário. [Comparação aprovada](samples/51c126cfcbaa47e28c5274008da4dbdb/relatorio.md) · [Revisão humana](REVISAO_HUMANA_ROSA.md)

As avaliações de v2.1 e v2.2 permanecem provisórias. O estudo exploratório com Hydrogen registra um diagnóstico completo, uma saída interrompida por limite de tokens e uma tentativa com timeout e consumo desconhecido. [Notas de engenharia](PROMPT_ENGINEERING_NOTES.md) · [Revisão v2.1](REVISAO_V2_1.md) · [Revisão v2.2](REVISAO_V2_2.md) · [Estudo Hydrogen](experimentos/hydrogen-caio-v22/README.md)

## Testes

```powershell
& $python -m pip check
& $python -m pytest -q
```

A suíte usa mocks para os cenários de geração. Com as dependências opcionais instaladas, também verifica a navegação, os filtros, o envio do formulário e os totais da comparação original.

## Limitações

- O contrato JSON valida a estrutura. A correção técnica e a coerência das orientações dependem de revisão humana. Uma saída inválida admite uma tentativa de reparo.
- A disponibilidade do modelo e a cota dependem da conta Gemini. Novas execuções podem produzir respostas diferentes das amostras, mesmo com os mesmos parâmetros.
- A amostra experimental é pequena. Um empate na soma das notas permite comparar os casos observados, sem determinar uma versão superior para todos os atendimentos.
- A consulta ao histórico percorre arquivos locais. Esse desenho atende a uma demonstração de pequeno porte. Gerações simultâneas equivalentes podem consumir mais de uma requisição.
