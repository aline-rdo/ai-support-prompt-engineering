# Verificação da entrega

## Requisitos do edital

| Item obrigatório | Situação e evidência |
|---|---|
| Linguagem, API e interface | Python 3.11+, CLI argparse e Gemini via requests. O [README](README.md) cobre instalação, variáveis, seis subcomandos e reprodução dos cenários. |
| Configuração | [.env.example](.env.example) com chave vazia; .env local ignorado. Modelo provisório Gemini 3.5 Flash-Lite. |
| Perfis e problema de entrada | [Quatro perfis](data/customers.json) com nome, nível, estilo e canal. [Três tickets](data/tickets.json) e entrada livre pela CLI. |
| Engenharia de prompt | [Montagem versionada](support_assistant/prompts.py) com persona, contexto, tarefa, decomposição de diagnóstico e formatos específicos. As [notas](PROMPT_ENGINEERING_NOTES.md) justificam as intervenções e regressões. |
| Quatro conteúdos distintos | [Geradores](support_assistant/generators.py) e JSONs reais de diagnóstico, passos, perguntas e fluxo. A correção técnica do conteúdo exige revisão humana. |
| Histórico e cache | Registro local em JSON com horário, perfil, ticket, versão, modelo, saída e avaliação. Escrita atômica, filtros e teste que conta as chamadas ao repetir a entrada. |
| Comparação controlada | 27 registros Flash-Lite. O [cenário original de Rosa](samples/51c126cfcbaa47e28c5274008da4dbdb/relatorio.md) tem as duas versões no mesmo grupo, com perfil, ticket, modelo e parâmetros equivalentes. |
| Rubrica fixa e autoavaliação | **Atendido.** A candidata aprovou 24 notas com justificativas nas oito respostas originais de Rosa; registro por ID no histórico e no [relatório exportado](samples/51c126cfcbaa47e28c5274008da4dbdb/relatorio.md). v1 e v2 somaram 41/60 cada. |
| Entrega reproduzível | O [README](README.md) descreve a instalação da CLI com `requirements.txt` e da interface Streamlit com `requirements-ui.txt`. As amostras acompanham o repositório. O histórico de uso local começa vazio em uma cópia nova. |

A [interface Streamlit](app.py) usa os mesmos geradores da CLI. Ela permite gerar respostas sob demanda, comparar respostas históricas lado a lado e consultar o histórico. A comparação aprovada de Rosa pode ser consultada localmente sem chave de API.

### Verificações da versão publicada

- Na preparação da publicação, os 29 testes do backend, da CLI e da interface passaram sem chamadas reais ao Gemini. A inicialização do Streamlit também foi verificada em localhost.
- O ambiente virtual de validação já instalado satisfez `pip install --no-index -r requirements.txt`; `pip check` não encontrou dependências quebradas. A geração externa é comprovada pelos registros preservados. Esta auditoria não fez chamadas ao Gemini.
- As 27 amostras passaram na validação local do contrato JSON, coincidiram integralmente com seus registros locais por ID; oito contêm avaliações aprovadas e 19 continuam com evaluation nulo. Os links relativos dos documentos foram verificados.
- A inspeção das árvores de todos os commits alcançáveis, conteúdo dos arquivos, mensagens de commit e arquivos de entrega não encontrou a credencial local, padrões comuns de chaves ou arquivos locais indevidos. Essa busca verifica os padrões examinados.

## Situação após a aprovação da comparação obrigatória

- [x] Registrar as 24 notas e justificativas aprovadas e conferir por ID o histórico, as oito amostras e o relatório.
- [x] Preservar respostas, versões e metadados; documentar o resultado de 41/60 para cada versão.
- [x] Manter as demais avaliações como propostas, o Hydrogen como apêndice exploratório e a seleção de versão explícita na CLI.
- [x] Executar os testes automatizados e verificar o material de entrega.

Os requisitos obrigatórios de implementação, comparação e documentação estão atendidos.

## Publicação

A entrega foi publicada na branch `main` do [repositório no GitHub](https://github.com/aline-rdo/ai-support-prompt-engineering), inicialmente com visibilidade privada.

Uma versão de prompt padrão e a avaliação dos demais cenários são decisões opcionais. A comparação aprovada não depende delas.
