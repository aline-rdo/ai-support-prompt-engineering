# Comparação de prompts

## Cenário

```json
{
  "customer": {
    "id": "c1",
    "name": "Rosa",
    "technical_level": "leigo",
    "communication_style": "didático",
    "channel": "telefone"
  },
  "ticket": {
    "id": "t1",
    "title": "Quedas de Wi-Fi",
    "description": "O celular perde a conexão na sala. Perto do roteador funciona. Ainda não testei outro aparelho."
  },
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  }
}
```

## diagnosis

- [v1](diagnosis-v1.json)
- [v2](diagnosis-v2.json)

| Critério | v1 | v2 |
|---|---|---|
| Clareza | 4 — A evidência é curta e a conclusão é provisória. A hipótese de alta probabilidade agrupa alcance e interferência, que o relato não distingue. | 4 — A conclusão preserva incerteza, mas a descrição da hipótese já afirma que os obstáculos bloqueiam o sinal. |
| Adequação ao nível do cliente | 3 — A expressão é relativamente simples, mas falta explicar por telefone como o sinal pode variar entre os dois locais. | 4 — A imagem é familiar para Rosa. Pode, contudo, fazê-la tomar uma barreira ainda não observada como causa. |
| Acionabilidade | 3 — Lista dados a coletar sem priorizar o teste que melhor separaria aparelho e ambiente. | 4 — Identifica a lacuna decisiva para a triagem. O 4 pressupõe que o atendente converterá a lacuna em teste; para autonomia de Rosa, 3 também seria defensável. |

## steps

- [v1](steps-v1.json)
- [v2](steps-v2.json)

| Critério | v1 | v2 |
|---|---|---|
| Clareza | 4 — A condição é legível, mas a sequência não diz como prosseguir quando o celular funciona perto, exatamente o caso relatado. | 4 — Os verbos das ações são concretos, mas esse resultado não diz a Rosa o que observar para saber se resolveu. |
| Adequação ao nível do cliente | 3 — É uma expressão interna do suporte. O terceiro passo compensa em parte ao dar exemplos de aparelhos comuns. | 4 — A comparação com um aparelho conhecido ajuda por telefone. O termo “aparelho” na transição do celular para o roteador é ambíguo, o que enfraquece a nota máxima. |
| Acionabilidade | 3 — É a ação mais útil e está ensinada. Porém, vem após repetir a aproximação e reiniciar a rede. No percurso compatível com o relato, Rosa nem chega a este passo pela condição escrita. | 3 — O teste aparece só após o reinício e não orienta como interpretar se apenas um telefone falhar. |

## questions

- [v1](questions-v1.json)
- [v2](questions-v2.json)

| Critério | v1 | v2 |
|---|---|---|
| Clareza | 4 — A primeira pergunta identifica o sintoma e o local. As quatro perguntas em sequência exigem atenção durante a ligação. | 5 — Uma frase aborda um único sintoma no local certo. |
| Adequação ao nível do cliente | 4 — Os exemplos ajudam Rosa a escolher o que testar. A pergunta sobre luzes acesas normalmente exige que ela conheça o padrão do roteador. | 4 — O motivo é compreensível por telefone. Falta um exemplo do segundo aparelho que Rosa pode usar. |
| Acionabilidade | 4 — O pedido inicial gera uma ação executável. As questões sobre luzes e reinício poderiam aguardar o resultado do primeiro teste. | 3 — A resposta permitiria escolher o próximo ramo, mas o ticket já informa que ela não testou. A formulação pode obter apenas “não sei” e exigir outra intervenção do atendente. |

## flow

- [v1](flow-v1.json)
- [v2](flow-v2.json)

| Critério | v1 | v2 |
|---|---|---|
| Clareza | 3 — A pergunta existe nos nós; o desenho chega ao fim sem mostrar os destinos correspondentes aos dois resultados. | 2 — O texto truncado prejudica a leitura. O ramo negativo do desenho sugere cabo ou outro cômodo, enquanto o nó descreve um teste em outro cômodo. |
| Adequação ao nível do cliente | 3 — Essa instrução pode ser lida ao telefone. Os destinos técnicos como problema_roteador precisam ser traduzidos pelo atendente. | 2 — A orientação é impraticável. A analogia da porta fechada não resolve o problema de execução. |
| Acionabilidade | 3 — O desenho encerra logo após testar. O nó d2 distingue os resultados, mas atribui o problema ao roteador ou celular sem orientar o próximo teste. | 2 — A sugestão presume um recurso disponível para o celular; além disso, a pergunta inicial já foi respondida pelo ticket. |
