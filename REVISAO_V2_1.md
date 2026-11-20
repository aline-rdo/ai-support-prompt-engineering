# Refinamento v2.1 · proposta para revisão da candidata

O experimento usa o Gemini 3.5 Flash-Lite, temperatura 0,3 e 4096 tokens. Para o Wi-Fi, cada um dos seis casos tem uma geração nova v2.1 sem cache e duas amostras históricas, v1 e v2, obtidas em outro momento. Para o aplicativo que fecha, as duas versões foram geradas na mesma rodada, sem reutilização. A ordem não foi aleatória e a revisão não foi cega. As notas descrevem estas respostas individuais.

O contrato JSON, o validador de geração e o reparo são os mesmos nas três versões. A v2.1 instrui o modelo a copiar os destinos dos nós para o desenho. Nenhum desenho foi renderizado ou corrigido pelo aplicativo. Um teste posterior verifica a igualdade linha a linha e alcançabilidade dos nós na amostra real. Isso não garante a coerência de toda resposta futura.

## Evidências

- Rosa, t1: [quatro respostas v2.1](samples/be2ff482e488422b970aa90ef9527c49/relatorio.md) e [oito originais](samples/51c126cfcbaa47e28c5274008da4dbdb/relatorio.md).
- Caio, t1: [duas respostas v2.1](samples/604bd2f9a9474fe0ac7bea635faa5205/relatorio.md), [diagnósticos originais](samples/bbbcd0edf722441290b24a311d276cdf/relatorio.md) e [passos originais](samples/6d88a80272aa42e9810e17645e9c3331/relatorio.md).
- Rosa, t2: [duas respostas contemporâneas](samples/20b06ab06ac749d08a12397fc5f8f683/relatorio.md).

## Proposta de avaliação

Escala de 1 (insuficiente) a 5 (excelente). As notas das [respostas anteriores](PROMPT_ENGINEERING_NOTES.md) continuam provisórias.

| Perfil, tarefa e versão | Clareza | Adequação ao cliente | Acionabilidade |
|---|---|---|---|
| Rosa · diagnóstico v2.1 | **3**. A hipótese de antena “usada apenas naquele ambiente” é confusa. Persistem palavras sem acentos, como “conexao”. | **4**. A imagem da “mangueira de agua” torna a perda de intensidade acessível por telefone. | **3**. Identifica o “Comportamento de outro aparelho na sala” como lacuna, mas a conclusão não ensina o teste nem como interpretar o resultado. |
| Rosa · passos v2.1 | **3**. “Aproxime-se do roteador na sala” presume uma localização incerta. O resultado esperado é observável. | **3**. O vocabulário é simples, mas a analogia da janela para “ouvir melhor um som distante” dificulta uma orientação oral curta. | **2**. O único passo repete a condição já conhecida. Se funcionar perto, como o ticket prevê, a sequência não investiga a queda na sala. |
| Rosa · perguntas v2.1 | **5**. Uma frase identifica o teste e o local. | **5**. “outro celular ou computador” oferece exemplos concretos para quem vai seguir a orientação por telefone. | **5**. “Você poderia testar” transforma a lacuna em ação; o resultado a relatar é se o outro aparelho também perde a conexão na sala. |
| Rosa · fluxo v2.1 | **4**. Os três nós têm ramos legíveis e destinos idênticos aos do desenho; o primeiro repete uma informação conhecida. | **4**. “Teste outro aparelho na sala para comparar” funciona em voz alta. Os IDs servem melhor ao atendente. | **3**. Há um teste viável; “Você já testou” pergunta pela realização, sem distinguir se o segundo aparelho falhou. |
| Caio · diagnóstico v2.1 | **3**. Classifica a hipótese de 5 GHz como “alta” e lista a banda entre os dados faltantes. A instrução de calibrar a probabilidade falhou. | **4**. “degradação do enlace” é compatível com o perfil e a conclusão cabe no chat. | **3**. Indica o segundo dispositivo como lacuna, mas não propõe na conclusão um teste com desfechos interpretáveis. |
| Caio · passos v2.1 | **3**. “AP da sala com RSSI nominal” presume um ponto de acesso no cômodo e não define a leitura esperada. | **3**. BSSID e RSSI cabem no vocabulário avançado, mas a precisão aparente pressupõe uma topologia desconhecida. | **2**. O segundo dispositivo é um bom controle. “Packet loss superior a 15%” e o limite de −65 dBm aparecem sem procedimento de medição nem fundamento no relato. |
| Rosa · perguntas, t2 · v2 e v2.1 | **5 em ambas**. Pedem o “nome exato do aplicativo” com a mesma frase. | **5 em ambas**. A pergunta é curta, concreta e adequada para telefone. | **4 em ambas**. Identificar o aplicativo orienta a triagem seguinte; plataforma e alcance da falha ainda estão em aberto. |

## Auditoria do edital

| Verificação | Evidência |
|---|---|
| 4 perfis e 4 geradores | `data/customers.json` e `support_assistant/generators.py`; Rosa tem amostras reais de todos os tipos. |
| Persona, contexto, formatos e versões | `support_assistant/prompts.py`, `v1.txt`, `v2.txt` e `v2.1.json`. |
| Histórico e cache | Cada amostra corresponde ao seu registro local em `data/history/<id>.json`. A CLI retornou cache hit ao repetir as perguntas de Rosa em t2 após a comparação. |
| Comparação e CLI | Relatórios acima; README com comandos; o relatório agora usa as versões selecionadas nas colunas. |
| Rubrica | Três critérios com justificativas. A revisão humana e a gravação das notas definitivas estão pendentes. |
| Testes, configuração e Git | `python -m pytest -q`; `.env.example`, `requirements.txt`, `git check-ignore .env prompt_desafio_tecnico_ia.md` e `git log --oneline`. Repositório local sem remoto configurado no momento da auditoria. |
