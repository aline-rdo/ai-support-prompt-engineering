# Revisão v2.2 · notas propostas à candidata

## Hipóteses e mudanças

A v2.1 já pedia cautela, mas Caio recebeu uma hipótese de alta probabilidade para uma banda desconhecida e limiares de rede sem instruções de medição. Rosa recebeu uma sequência que voltava ao roteador, embora já tivesse informado o resultado. Na v2.2:

- **Diagnóstico.** A instrução “Formule hipóteses no nível que esses fatos permitem” limita a especificidade; a conclusão deve interpretar os dois desfechos de um teste. Por telefone, a persona passa a explicar o motivo literalmente, sem sugerir analogias.
- **Passos.** “Mantenha as condições conhecidas e varie uma coisa” torna a comparação reproduzível. A nova regra exige método e fundamento para métricas e pede que a configuração original possa ser restaurada.
- **Perguntas.** A primeira lacuna deve mudar a decisão seguinte. O segundo aparelho é pertinente ao Wi-Fi; identificar o aplicativo pode ser suficiente como primeira pergunta no outro ticket.
- **Fluxo.** A decisão deve perguntar pelo resultado do teste novo. Os destinos sim/não devem ser diferentes, e vale o mesmo formato literal de três linhas por nó usado na v2.1.

As instruções completas estão em [v2.2.txt](support_assistant/v2.2.txt) e [v2.2.json](support_assistant/v2.2.json). O formato JSON, o cliente Gemini, a política de reparo e o processamento da saída permaneceram iguais. Os testes estruturais são posteriores à geração.

## Execuções e reprodução

Sete respostas reais de Gemini 3.5 Flash-Lite, temperatura 0,3 e máximo de 4096 tokens. Todas têm cache_hit falso, uma resposta do provedor registrada sem reparo e correspondência com o histórico local pelo ID. Foram comparadas às amostras anteriores correspondentes de mesmo perfil, ticket, tarefa, modelo e configurações.

| Cenário | Amostras v2.2 | Referências |
|---|---|---|
| Rosa, Wi-Fi, quatro tarefas | [JSONs e IDs](samples/9c6a6307fcee4b8c9dd0e5821796e295/relatorio.md) | [v2.1](samples/be2ff482e488422b970aa90ef9527c49/relatorio.md), [v1 e v2](samples/51c126cfcbaa47e28c5274008da4dbdb/relatorio.md) |
| Caio, Wi-Fi, diagnóstico e passos | [JSONs e IDs](samples/d81a496ee4784c8bbd4c2b15c1a362b1/relatorio.md) | [v2.1](samples/604bd2f9a9474fe0ac7bea635faa5205/relatorio.md), [diagnósticos anteriores](samples/bbbcd0edf722441290b24a311d276cdf/relatorio.md), [passos anteriores](samples/6d88a80272aa42e9810e17645e9c3331/relatorio.md) |
| Rosa, aplicativo que fecha, perguntas | [JSON e ID](samples/96919e92d9fb424cb1ae7a8055e8c78c/relatorio.md) | [v2 e v2.1](samples/20b06ab06ac749d08a12397fc5f8f683/relatorio.md) |

Após a instalação descrita no README, estes comandos reproduzem as sete condições com novas gerações:

```powershell
$python = ".\.venv\Scripts\python.exe"
$env:LLM_MODEL = "gemini-3.5-flash-lite"
$env:LLM_TEMPERATURE = "0.3"
$env:LLM_MAX_TOKENS = "4096"
& $python -m support_assistant.cli generate --customer c1 --ticket t1 --type all --prompt-version v2.2 --no-cache
foreach ($tipo in "diagnosis","steps") {
    & $python -m support_assistant.cli generate --customer c2 --ticket t1 --type $tipo --prompt-version v2.2 --no-cache
}
& $python -m support_assistant.cli generate --customer c1 --ticket t2 --type questions --prompt-version v2.2 --no-cache
```

## Avaliação provisória

Cada célula mostra **v2.1 → v2.2** e a evidência para a nota nova. A escala é a mesma do edital, de 1 a 5. As propostas anteriores estão nas revisões [original](PROMPT_ENGINEERING_NOTES.md) e [v2.1](REVISAO_V2_1.md).

| Tarefa | Clareza | Adequação ao cliente | Acionabilidade |
|---|---|---|---|
| Rosa · diagnóstico | **3 → 5**. Distingue os dois desfechos com “Se outro aparelho perder a conexão” e “Se o segundo aparelho funcionar”. | **4 → 4**. Linguagem acessível, embora “o indicativo aponta” seja pouco natural por telefone. | **3 → 4**. Diz onde comparar e como interpretar; falta orientar a usar o mesmo Wi-Fi. |
| Rosa · passos | **3 → 4**. O primeiro passo localiza o teste “no mesmo lugar da sala”; “o problema é apenas no seu aparelho” afirma mais do que ele demonstra. | **3 → 4**. “Pegue outro celular” é uma instrução fácil de seguir ouvindo; pressupõe que haja um disponível. | **2 → 3**. O primeiro teste é novo, mas “tente acessar a internet” permite usar dados móveis e o segundo passo repete um resultado conhecido. |
| Rosa · perguntas | **5 → 5**. Identifica aparelho, local e sintoma em uma pergunta. | **5 → 5**. “um notebook ou outro celular” dá exemplos familiares. | **5 → 5**. Pede observar se o outro aparelho “também perde a conexão na sala”, suficiente para iniciar a triagem; a mesma rede poderia ser explícita. |
| Rosa · fluxo | **4 → 3**. Os destinos são compreensíveis, mas o segundo nó aparece embutido no ramo NÃO. | **4 → 3**. A frase “A distância gera barreiras físicas” oferece uma explicação enganosa para a pessoa leiga. | **3 → 2**. “Chegue mais perto do roteador” repete o teste conhecido. O ramo SIM encerra com uma afirmação; o teste útil fica no ramo contrário ao relato. |
| Caio · diagnóstico | **3 → 3**. O grau moderado é coerente com a lacuna, mas a conclusão “a variável limitante é” transforma um indício em causa estabelecida. | **4 → 3**. “ponto de acesso na sala” sugere uma topologia desconhecida; a referência à pilha do sistema operacional também é especulativa. | **3 → 4**. Ensina a comparar “na mesma sala” e “à mesma rede” e interpreta os dois resultados. |
| Caio · passos | **3 → 3**. O primeiro teste é reproduzível; “a falha reside no adaptador” confunde isolamento do aparelho com confirmação da peça. | **3 → 3**. A linguagem é técnica, mas a instrução pressupõe acesso ao ponto de acesso e confunde mudança de banda com troca de canal. | **2 → 2**. Recomenda mudar a frequência sem ensinar execução ou reversão. “RSSI abaixo de -75 dBm” não tem método nem fundamento no ticket. |
| Rosa · aplicativo · perguntas | **5 → 5**. A pergunta “Qual é o nome exato do aplicativo que está fechando sozinho?” é idêntica nas versões. | **5 → 4**. A pergunta continua natural, mas a justificativa exibida “Identificar o objeto da falha” é mais abstrata para Rosa. | **4 → 4**. Saber o nome permite direcionar a próxima orientação; a plataforma continua em aberto. |

## Verificação estrutural e decisão

Os **27 testes passaram**. Nos dois nós reais da v2.2, IDs, alcançabilidade, referências posteriores e distinção entre os dois destinos passaram na auditoria estrutural. A comparação literal do desenho **falhou**: cinco linhas recebidas, seis esperadas. Os caminhos são reconhecíveis, mas a referência D2 foi expandida na linha do ramo. A amostra foi preservada como recebida. Nenhuma alteração programática produziu os ganhos de conteúdo ou corrigiu a falha. Os testes com grafos inválidos cobrem ciclo, referência inexistente e destinos iguais.

**Recomendação provisória: v2.1 como padrão único para apoio ao atendente.** A v2.2 é preferível no passo inicial de Rosa e oferece um teste de isolamento melhor nos diagnósticos. Ainda assim, regrediu no fluxo, manteve o problema das métricas e passou a orientar explicitamente uma mudança de banda sem método de reversão. Na v2.1, o fluxo observado atende ao formato e a pergunta de Wi-Fi já obtinha bom resultado. As amostras também mostram limitações da v2.1 para o perfil avançado; ambas requerem revisão técnica antes de orientar mudanças de rede. A escolha do padrão não foi aplicada à CLI.

Há uma resposta por condição, referências históricas, revisão não cega e apenas uma tarefa no segundo ticket. Os resultados permitem comparar respostas concretas; não medem taxa de falha, significância estatística ou superioridade geral. Os campos evaluation permanecem pendentes da revisão da candidata.
