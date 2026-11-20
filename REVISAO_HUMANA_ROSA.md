# Revisão humana · Atendimento de Rosa por telefone

**Aprovado pela candidata.** A comparação resultou em 41/60 para v1 e 41/60 para v2. As tabelas e os oito registros integrais abaixo contêm as notas definitivas desta comparação. Cada trecho foi conferido no campo `output` do registro. A escala vai de 1 (insuficiente), 2 (fraco), 3 (adequado), 4 (bom) a 5 (excelente).

Rosa informou que o celular perde o Wi-Fi na sala, funciona perto do roteador e ainda é o único aparelho testado. O mesmo Gemini 3.5 Flash-Lite gerou as quatro tarefas em v1 e v2, com temperatura 0,3 e limite de 4.096 tokens. A questão prática é se uma pessoa leiga consegue seguir a orientação ouvindo o atendente.

## Ajustes aprovados

| Resposta e critério | Proposta anterior | Nota aprovada | Motivo decisivo |
|---|---:|---:|---|
| Passos v1 · acionabilidade | 4 | **3** | O teste com outro celular é útil, mas fica no passo 3. A condição do passo 1 só manda avançar se continuar caindo perto do roteador. Rosa já disse que perto funciona. O passo 2 ainda interrompe a rede antes de isolar o problema. |
| Passos v2 · adequação | 5 | **4** | A linguagem é falável, mas “vamos desligar o aparelho da tomada” vem logo depois de falar no celular. Rosa precisa inferir que o atendente se refere ao roteador. |
| Perguntas v2 · acionabilidade | 4 | **3** | Pergunta pelo resultado de um teste que Rosa declarou não ter feito. A v1 pede explicitamente que o faça. A clareza da pergunta v2 continua merecendo 5. |

As outras 21 notas e suas justificativas foram mantidas conforme a revisão humana.

## Diagnóstico · v1

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/diagnosis-v1.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 4 | “Perto do roteador funciona” | A evidência é curta e a conclusão é provisória. A hipótese de alta probabilidade agrupa alcance e interferência, que o relato não distingue. |
| Adequação ao nível de Rosa | 3 | “limitacao de alcance” | A expressão é relativamente simples, mas falta explicar por telefone como o sinal pode variar entre os dois locais. |
| Acionabilidade | 3 | “Modelo do roteador e operadora de internet” | Lista dados a coletar sem priorizar o teste que melhor separaria aparelho e ambiente. |

**Registro JSON completo**

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
  "content_type": "diagnosis",
  "prompt_version": "v1",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "666302d11cc64a20a8d652c36a64920d",
  "timestamp": "2026-11-20T21:00:43.354949+00:00",
  "customer_id": "c1",
  "cache_key": "10a4729b7e5f896f3acc1ba660a333a17019ea73f8e2647993dee4bfd8418049",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "hypotheses": [
      {
        "description": "Interferencia ou sinal fraco de Wi-Fi devido a distancia e barreiras fisicas entre a sala e o roteador.",
        "likelihood": "alta",
        "supporting_evidence": [
          "O celular perde a conexao na sala",
          "Perto do roteador funciona"
        ]
      }
    ],
    "observed_evidence": [
      "O celular perde a conexao especificamente na sala",
      "A conexao funciona normalmente proximo ao roteador",
      "Ainda nao foi feito o teste com outro aparelho"
    ],
    "missing_information": [
      "Distancia exata entre o roteador e a sala",
      "Presenca de paredes grossas, espelhos ou outros obstaculos no caminho",
      "Modelo do roteador e operadora de internet"
    ],
    "probable_conclusion": "O problema parece ser uma limitacao de alcance ou barreira de sinal entre o roteador e o comodo (sala), causando a perda de conexao a distancia.",
    "confidence": "media"
  },
  "evaluation": {
    "clarity": {
      "score": 4,
      "justification": "A evidência é curta e a conclusão é provisória. A hipótese de alta probabilidade agrupa alcance e interferência, que o relato não distingue."
    },
    "customer_fit": {
      "score": 3,
      "justification": "A expressão é relativamente simples, mas falta explicar por telefone como o sinal pode variar entre os dois locais."
    },
    "actionability": {
      "score": 3,
      "justification": "Lista dados a coletar sem priorizar o teste que melhor separaria aparelho e ambiente."
    }
  },
  "uso": [
    {
      "promptTokenCount": 205,
      "candidatesTokenCount": 199,
      "totalTokenCount": 404,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 205
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1788
}
```

## Diagnóstico · v2

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/diagnosis-v2.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 4 | “O problema parece ser a distancia ou barreiras fisicas” | A conclusão preserva incerteza, mas a descrição da hipótese já afirma que os obstáculos bloqueiam o sinal. |
| Adequação ao nível de Rosa | 4 | “uma parede grossa que esconde a luz de uma lampada” | A imagem é familiar para Rosa. Pode, contudo, fazê-la tomar uma barreira ainda não observada como causa. |
| Acionabilidade | 4 | “Se outros aparelhos tambem perdem o sinal na sala.” | Identifica a lacuna decisiva para a triagem. O 4 pressupõe que o atendente converterá a lacuna em teste; para autonomia de Rosa, 3 também seria defensável. |

**Registro JSON completo**

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
  "content_type": "diagnosis",
  "prompt_version": "v2",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "1ff2d75decaf42a1b5e20b3e72792cdf",
  "timestamp": "2026-11-20T21:00:45.145133+00:00",
  "customer_id": "c1",
  "cache_key": "f79f5c869ce76f74da90c0d51d99f2f3d91d3c2d60e8c225d0d96cd0a360b364",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "hypotheses": [
      {
        "description": "Obstaculos fisicos entre a sala e o roteador bloqueiam o sinal do Wi-Fi, igual a uma parede grossa que esconde a luz de uma lampada.",
        "likelihood": "alta",
        "supporting_evidence": [
          "O celular perde a conexao na sala.",
          "Perto do roteador funciona."
        ]
      }
    ],
    "observed_evidence": [
      "O celular perde a conexao na sala.",
      "Perto do roteador funciona.",
      "Ainda nao testou outro aparelho."
    ],
    "missing_information": [
      "Se outros aparelhos tambem perdem o sinal na sala.",
      "Qual a distancia exata e quais obstaculos existem entre o roteador e a sala."
    ],
    "probable_conclusion": "O problema parece ser a distancia ou barreiras fisicas enfraquecendo o sinal do Wi-Fi na sala.",
    "confidence": "media"
  },
  "evaluation": {
    "clarity": {
      "score": 4,
      "justification": "A conclusão preserva incerteza, mas a descrição da hipótese já afirma que os obstáculos bloqueiam o sinal."
    },
    "customer_fit": {
      "score": 4,
      "justification": "A imagem é familiar para Rosa. Pode, contudo, fazê-la tomar uma barreira ainda não observada como causa."
    },
    "actionability": {
      "score": 4,
      "justification": "Identifica a lacuna decisiva para a triagem. O 4 pressupõe que o atendente converterá a lacuna em teste; para autonomia de Rosa, 3 também seria defensável."
    }
  },
  "uso": [
    {
      "promptTokenCount": 420,
      "candidatesTokenCount": 185,
      "totalTokenCount": 605,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 420
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1615
}
```

## Passos de resolução · v1

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/steps-v1.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 4 | “Se continuar caindo mesmo perto, vá para o próximo passo.” | A condição é legível, mas a sequência não diz como prosseguir quando o celular funciona perto, exatamente o caso relatado. |
| Adequação ao nível de Rosa | 3 | “será necessário realizar o escalonamento” | É uma expressão interna do suporte. O terceiro passo compensa em parte ao dar exemplos de aparelhos comuns. |
| Acionabilidade | 3 | “Teste a conexão Wi-Fi na sala usando um segundo aparelho” | É a ação mais útil e está ensinada. Porém, vem após repetir a aproximação e reiniciar a rede. No percurso compatível com o relato, Rosa nem chega a este passo pela condição escrita. |

**Registro JSON completo**

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
  "content_type": "steps",
  "prompt_version": "v1",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "fd796cdb66a84d618f5ae154194351ba",
  "timestamp": "2026-11-20T21:00:46.762510+00:00",
  "customer_id": "c1",
  "cache_key": "a8fa6b2c4a68ebb964820f9800380b32e35d03a224fb27e336d7d9e7ee062504",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "steps": [
      {
        "number": 1,
        "action": "Aproxime-se do roteador com o celular na sala e verifique se o ícone do Wi-Fi volta a aparecer cheio.",
        "expected_result": "A conexão de internet é estabilizada quando você está mais próximo do aparelho.",
        "if_it_fails": "Se continuar caindo mesmo perto, vá para o próximo passo."
      },
      {
        "number": 2,
        "action": "Desligue o roteador da tomada, aguarde 10 segundos e depois ligue-o novamente.",
        "expected_result": "As luzes do aparelho piscam e a rede Wi-Fi é reiniciada com sucesso.",
        "if_it_fails": "Se as quedas na sala persistirem, vá para o próximo passo."
      },
      {
        "number": 3,
        "action": "Teste a conexão Wi-Fi na sala usando um segundo aparelho, como outro celular ou um notebook.",
        "expected_result": "Identificar se o problema ocorre apenas no seu celular ou em todos os dispositivos na sala.",
        "if_it_fails": "Se o problema persistir e afetar mais de um aparelho, será necessário realizar o escalonamento."
      }
    ],
    "estimated_time": "10 a 15 minutos",
    "escalation_criteria": [
      "Quedas de Wi-Fi continuam afetando múltiplos dispositivos após reiniciar o roteador",
      "Presença de barreiras físicas muito densas (como paredes de concreto espessas ou espelhos grandes) entre a sala e o roteador"
    ]
  },
  "evaluation": {
    "clarity": {
      "score": 4,
      "justification": "A condição é legível, mas a sequência não diz como prosseguir quando o celular funciona perto, exatamente o caso relatado."
    },
    "customer_fit": {
      "score": 3,
      "justification": "É uma expressão interna do suporte. O terceiro passo compensa em parte ao dar exemplos de aparelhos comuns."
    },
    "actionability": {
      "score": 3,
      "justification": "É a ação mais útil e está ensinada. Porém, vem após repetir a aproximação e reiniciar a rede. No percurso compatível com o relato, Rosa nem chega a este passo pela condição escrita."
    }
  },
  "uso": [
    {
      "promptTokenCount": 204,
      "candidatesTokenCount": 385,
      "totalTokenCount": 589,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 204
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 2074
}
```

## Passos de resolução · v2

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/steps-v2.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 4 | “o sinal de internet será atualizado” | Os verbos das ações são concretos, mas esse resultado não diz a Rosa o que observar para saber se resolveu. |
| Adequação ao nível de Rosa | 4 | “igualzinho a quando reiniciamos a televisão” | A comparação com um aparelho conhecido ajuda por telefone. O termo “aparelho” na transição do celular para o roteador é ambíguo, o que enfraquece a nota máxima. |
| Acionabilidade | 3 | “será preciso testar com outro telefone para tirar a dúvida” | O teste aparece só após o reinício e não orienta como interpretar se apenas um telefone falhar. |

**Registro JSON completo**

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
  "content_type": "steps",
  "prompt_version": "v2",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "83a00665bcaa4febb7b9114b0746b338",
  "timestamp": "2026-11-20T21:00:48.839756+00:00",
  "customer_id": "c1",
  "cache_key": "fc2f2fa22c7b60fbd0247c9e16beadd594f335c92d3a5380439106b3bd75a60a",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "steps": [
      {
        "number": 1,
        "action": "Aproxime o celular um pouco mais do roteador, como se estivesse chegando perto da porta de um cômodo vizinho.",
        "expected_result": "O sinal deve melhorar e a internet voltar a carregar as páginas.",
        "if_it_fails": "Se continuar caindo, vamos desligar o aparelho da tomada."
      },
      {
        "number": 2,
        "action": "Desconecte a caixa do Wi-Fi da tomada por dez segundos e volte a ligar, igualzinho a quando reiniciamos a televisão.",
        "expected_result": "As luzes do aparelho vão piscar e o sinal de internet será atualizado.",
        "if_it_fails": "Se o problema persistir na sala, será preciso testar com outro telefone para tirar a dúvida."
      }
    ],
    "estimated_time": "5 minutos",
    "escalation_criteria": [
      "Se o Wi-Fi continuar caindo mesmo após reiniciar o roteador.",
      "Se outro aparelho também perder a conexão no mesmo local."
    ]
  },
  "evaluation": {
    "clarity": {
      "score": 4,
      "justification": "Os verbos das ações são concretos, mas esse resultado não diz a Rosa o que observar para saber se resolveu."
    },
    "customer_fit": {
      "score": 4,
      "justification": "A comparação com um aparelho conhecido ajuda por telefone. O termo “aparelho” na transição do celular para o roteador é ambíguo, o que enfraquece a nota máxima."
    },
    "actionability": {
      "score": 3,
      "justification": "O teste aparece só após o reinício e não orienta como interpretar se apenas um telefone falhar."
    }
  },
  "uso": [
    {
      "promptTokenCount": 414,
      "candidatesTokenCount": 266,
      "totalTokenCount": 680,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 414
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1723
}
```

## Perguntas de esclarecimento · v1

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/questions-v1.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 4 | “também perde a conexão quando você está na sala?” | A primeira pergunta identifica o sintoma e o local. As quatro perguntas em sequência exigem atenção durante a ligação. |
| Adequação ao nível de Rosa | 4 | “como um notebook ou outro celular” | Os exemplos ajudam Rosa a escolher o que testar. A pergunta sobre luzes acesas normalmente exige que ela conheça o padrão do roteador. |
| Acionabilidade | 4 | “Você poderia testar se outro aparelho” | O pedido inicial gera uma ação executável. As questões sobre luzes e reinício poderiam aguardar o resultado do primeiro teste. |

**Registro JSON completo**

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
  "content_type": "questions",
  "prompt_version": "v1",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "b1a76032604c49aea33017e847f0dce6",
  "timestamp": "2026-11-20T21:00:50.565057+00:00",
  "customer_id": "c1",
  "cache_key": "8023f32832f96b7ee96e14bfd66322685e60b652b59da54e8060a93266d1c300",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "questions": [
      {
        "priority": 1,
        "question": "Você poderia testar se outro aparelho, como um notebook ou outro celular, também perde a conexão quando você está na sala?",
        "why_needed": "Ajuda a identificar se o problema está apenas no primeiro celular ou na cobertura do sinal do roteador para o cômodo."
      },
      {
        "priority": 2,
        "question": "Existe algum obstáculo grosso entre o roteador e a sala, como paredes de concreto, espelhos grandes ou móveis metálicos?",
        "why_needed": "Esses materiais podem bloquear ou enfraquecer o sinal de Wi-Fi facilmente."
      },
      {
        "priority": 3,
        "question": "As luzes indicadoras (lâmpadas pequenas) no roteador continuam acesas normalmente quando o celular perde a conexão?",
        "why_needed": "Permite verificar se a internet da operadora está caindo por completo ou se é apenas o sinal sem fio."
      },
      {
        "priority": 4,
        "question": "Você já tentou reiniciar o roteador tirando ele da tomada por dez segundos e depois ligando de novo?",
        "why_needed": "Reiniciar corrige pequenos travamentos temporários no equipamento de Wi-Fi."
      }
    ]
  },
  "evaluation": {
    "clarity": {
      "score": 4,
      "justification": "A primeira pergunta identifica o sintoma e o local. As quatro perguntas em sequência exigem atenção durante a ligação."
    },
    "customer_fit": {
      "score": 4,
      "justification": "Os exemplos ajudam Rosa a escolher o que testar. A pergunta sobre luzes acesas normalmente exige que ela conheça o padrão do roteador."
    },
    "actionability": {
      "score": 4,
      "justification": "O pedido inicial gera uma ação executável. As questões sobre luzes e reinício poderiam aguardar o resultado do primeiro teste."
    }
  },
  "uso": [
    {
      "promptTokenCount": 179,
      "candidatesTokenCount": 252,
      "totalTokenCount": 431,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 179
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1884
}
```

## Perguntas de esclarecimento · v2

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/questions-v2.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 5 | “O problema acontece com outros aparelhos na sala?” | Uma frase aborda um único sintoma no local certo. |
| Adequação ao nível de Rosa | 4 | “apenas no seu celular ou na rede da sala” | O motivo é compreensível por telefone. Falta um exemplo do segundo aparelho que Rosa pode usar. |
| Acionabilidade | 3 | “O problema acontece com outros aparelhos na sala?” | A resposta permitiria escolher o próximo ramo, mas o ticket já informa que ela não testou. A formulação pode obter apenas “não sei” e exigir outra intervenção do atendente. |

**Registro JSON completo**

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
  "content_type": "questions",
  "prompt_version": "v2",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "eba2cccd5b1e4a07b277518f0e81205f",
  "timestamp": "2026-11-20T21:00:52.451411+00:00",
  "customer_id": "c1",
  "cache_key": "5b72028d10cb581b2a6151473e39f4cf9891fe1347e481b971bb2d9258c83ef0",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "questions": [
      {
        "priority": 1,
        "question": "O problema acontece com outros aparelhos na sala?",
        "why_needed": "Precisamos saber se a falha é apenas no seu celular ou na rede da sala."
      }
    ]
  },
  "evaluation": {
    "clarity": {
      "score": 5,
      "justification": "Uma frase aborda um único sintoma no local certo."
    },
    "customer_fit": {
      "score": 4,
      "justification": "O motivo é compreensível por telefone. Falta um exemplo do segundo aparelho que Rosa pode usar."
    },
    "actionability": {
      "score": 3,
      "justification": "A resposta permitiria escolher o próximo ramo, mas o ticket já informa que ela não testou. A formulação pode obter apenas “não sei” e exigir outra intervenção do atendente."
    }
  },
  "uso": [
    {
      "promptTokenCount": 392,
      "candidatesTokenCount": 48,
      "totalTokenCount": 440,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 392
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1291
}
```

## Fluxograma · v1

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/flow-v1.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 3 | “Outro aparelho apresenta o mesmo problema?” | A pergunta existe nos nós; o desenho chega ao fim sem mostrar os destinos correspondentes aos dois resultados. |
| Adequação ao nível de Rosa | 3 | “Testar outro celular” | Essa instrução pode ser lida ao telefone. Os destinos técnicos como problema_roteador precisam ser traduzidos pelo atendente. |
| Acionabilidade | 3 | “Fim do atendimento” | O desenho encerra logo após testar. O nó d2 distingue os resultados, mas atribui o problema ao roteador ou celular sem orientar o próximo teste. |

**Registro JSON completo**

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
  "content_type": "flow",
  "prompt_version": "v1",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "11387831904b41878dee44fd26a8d352",
  "timestamp": "2026-11-20T21:00:53.745879+00:00",
  "customer_id": "c1",
  "cache_key": "ca76cb502f620b0ebdafa9097f799995a775a5fe27dd7df80bd4aaf31eeaa700",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "ascii_flowchart": "[Inicio: Queda de Wi-Fi]\n          |\n          v\n[Esta proximo ao roteador?]\n  |                    |\n(Sim)                 (Nao)\n  |                    |\n  v                    v\n[Funciona normal]   [Problema de sinal]\n  |                    |\n  v                    v\n[Testar outro celular] [Aproximar da sala]\n  |                    |\n  +---------+----------+\n            |\n            v\n    [Fim do atendimento]",
    "decision_nodes": [
      {
        "id": "d1",
        "question": "O celular funciona perto do roteador?",
        "yes": "d2",
        "no": "sinal_fraco"
      },
      {
        "id": "d2",
        "question": "Outro aparelho apresenta o mesmo problema?",
        "yes": "problema_roteador",
        "no": "problema_celular"
      }
    ]
  },
  "evaluation": {
    "clarity": {
      "score": 3,
      "justification": "A pergunta existe nos nós; o desenho chega ao fim sem mostrar os destinos correspondentes aos dois resultados."
    },
    "customer_fit": {
      "score": 3,
      "justification": "Essa instrução pode ser lida ao telefone. Os destinos técnicos como problema_roteador precisam ser traduzidos pelo atendente."
    },
    "actionability": {
      "score": 3,
      "justification": "O desenho encerra logo após testar. O nó d2 distingue os resultados, mas atribui o problema ao roteador ou celular sem orientar o próximo teste."
    }
  },
  "uso": [
    {
      "promptTokenCount": 199,
      "candidatesTokenCount": 205,
      "totalTokenCount": 404,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 199
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1652
}
```

## Fluxograma · v2

[Registro original](samples/51c126cfcbaa47e28c5274008da4dbdb/flow-v2.json)

| Critério | Nota aprovada | Trecho literal | Justificativa aprovada |
|---|---:|---|---|
| Clareza | 2 | “do roteia” | O texto truncado prejudica a leitura. O ramo negativo do desenho sugere cabo ou outro cômodo, enquanto o nó descreve um teste em outro cômodo. |
| Adequação ao nível de Rosa | 2 | “afaste barreiras físicas como paredes” | A orientação é impraticável. A analogia da porta fechada não resolve o problema de execução. |
| Acionabilidade | 2 | “Usar cabo” | A sugestão presume um recurso disponível para o celular; além disso, a pergunta inicial já foi respondida pelo ticket. |

**Registro JSON completo**

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
  "content_type": "flow",
  "prompt_version": "v2",
  "provider": "gemini",
  "model": "gemini-3.5-flash-lite",
  "settings": {
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "id": "59fea67cee6542b2b44459438256fdb1",
  "timestamp": "2026-11-20T21:00:55.399858+00:00",
  "customer_id": "c1",
  "cache_key": "4d611493275e900b0153dcc4e20d4dd4c2f9172b8853ca4030443ada9b842b1a",
  "cache_mode": "refresh",
  "cache_hit": false,
  "comparison_id": "51c126cfcbaa47e28c5274008da4dbdb",
  "output": {
    "ascii_flowchart": "+-----------------------+\n| O sinal cai na sala?  |\n+-----------------------+\n      |           |\n    (Sim)       (Não)\n      v           v\n+-----------+ +-----------+\n| Aproximar | | Usar cabo |\n| do roteia | | ou outro  |\n| ou parede | | comodo    |\n+-----------+ +-----------+",
    "decision_nodes": [
      {
        "id": "node_1",
        "question": "O celular perde a conexão na sala e funciona perto do roteador?",
        "yes": "Aproxime-se do roteador ou afaste barreiras físicas como paredes, pois obstáculos bloqueiam as ondas de rádio assim como uma porta fechada abafa o som.",
        "no": "Teste o acesso à internet em outro cômodo da casa para verificar se o problema ocorre em toda a residência ou apenas na sala."
      }
    ]
  },
  "evaluation": {
    "clarity": {
      "score": 2,
      "justification": "O texto truncado prejudica a leitura. O ramo negativo do desenho sugere cabo ou outro cômodo, enquanto o nó descreve um teste em outro cômodo."
    },
    "customer_fit": {
      "score": 2,
      "justification": "A orientação é impraticável. A analogia da porta fechada não resolve o problema de execução."
    },
    "actionability": {
      "score": 2,
      "justification": "A sugestão presume um recurso disponível para o celular; além disso, a pergunta inicial já foi respondida pelo ticket."
    }
  },
  "uso": [
    {
      "promptTokenCount": 400,
      "candidatesTokenCount": 219,
      "totalTokenCount": 619,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 400
        }
      ],
      "serviceTier": "standard"
    }
  ],
  "latencia_ms": 1765
}
```
