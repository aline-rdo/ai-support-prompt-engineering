# Auditoria e checklist antes da publicação

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
| Rubrica fixa e autoavaliação | Três notas e justificativas propostas para cada amostra. A CLI valida e grava a avaliação. **Pendente:** aprovação pela candidata e gravação junto aos resultados. |
| Entrega reproduzível | Dependências em requirements.txt, código, README, amostras, notas técnicas e histórico Git. O diretório samples é versionado; o histórico de uso local é privado e começa vazio em uma cópia nova. |

O edital permite ferramentas de IA e exige que a candidata saiba explicar e modificar a solução. Web e deploy são opcionais.

### Verificações executadas na consolidação

- Em uma cópia isolada dos arquivos de entrega com .env de exemplo e sem credencial, `python -m pytest -q` passou nos 27 testes. A CLI retornou 4 itens em customers, 3 em tickets e 0 em history, como esperado em uma instalação nova. Os testes de geração, comparação e avaliação usam mocks.
- O ambiente virtual de validação já instalado satisfez `pip install --no-index -r requirements.txt`; `pip check` não encontrou dependências quebradas. A geração externa é comprovada pelos registros preservados. Esta auditoria não fez chamadas ao Gemini.
- As 27 amostras passaram na validação local do contrato JSON, coincidiram integralmente com seus registros locais por ID e mantiveram evaluation nulo. Os links relativos dos documentos foram verificados.
- A inspeção das árvores de todos os commits alcançáveis, conteúdo dos arquivos, mensagens de commit e arquivos de entrega não encontrou a credencial local, padrões comuns de chaves ou arquivos locais indevidos. Essa busca verifica os padrões examinados.

## Antes de publicar

- [ ] Candidata revisar a documentação e as propostas na matriz, corrigindo notas e justificativas por tarefa, critério e versão.
- [ ] Decidir a versão de prompt para uso padrão após considerar os riscos dos passos e as diferenças por tarefa. O modelo já está configurado; o prompt ainda é selecionado na CLI.
- [ ] Após aprovação, registrar as notas no histórico e exportar os relatórios avaliados, preservando as respostas originais. Conferir pelo ID os três critérios e justificativas da comparação mínima.
- [ ] Candidata reproduzir um fluxo e explicar cache, calibração de hipóteses, limites do JSON e decisões de versão na defesa técnica.
- [ ] Rodar a suíte final e repetir a verificação do índice e do histórico antes da publicação. Manter .env, PDFs do edital, roteiro local, ambientes virtuais e histórico de uso fora do Git.
- [ ] Definir destino e acesso para a equipe avaliadora. Na consolidação, o repositório local ainda não tem remoto configurado.
