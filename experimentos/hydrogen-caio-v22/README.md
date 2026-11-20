# Experimento exploratório com Gemini 4 Hydrogen

O catálogo da chave listou o modelo. Após uma validação curta, as chamadas individuais usaram o mesmo Caio, ticket t1 e prompt v2.2 da [comparação Flash-Lite](../../samples/d81a496ee4784c8bbd4c2b15c1a362b1/relatorio.md). Hydrogen usou LOW, sem temperatura personalizada (o modelo ignora esse ajuste), cache da aplicação, repetição ou reparo. Flash-Lite usou temperatura 0,3 e teto de 4.096. Esses resultados são uma série exploratória separada da matriz de versões.

| Registro original | Teto | Entrada | Resposta | Raciocínio | Total informado | Encerramento |
|---|---:|---:|---:|---:|---:|---|
| [Validação](validacao.json) | 128 | 36 | 5 | 25 | 66 | STOP, resposta OK |
| [Diagnóstico](diagnosis.json) | 1.400 | 646 | 259 | 628 | 1.533 | STOP, JSON válido |
| [Passos](steps.json) | 1.400 | 655 | 382 | 1.018 | 2.055 | MAX_TOKENS, JSON truncado |
| [Passos com teto ampliado](steps-4096.json) | 4.096 | desconhecido | desconhecido | desconhecido | desconhecido | ReadTimeout do cliente após 120 s; nenhum status HTTP ou finishReason recebido |

Houve quatro chamadas de geração e uma consulta ao catálogo. A soma conhecida das três primeiras gerações é 3.654 tokens. O consumo total das quatro é desconhecido. Na terceira, raciocínio e resposta esgotaram exatamente o teto; a quarta não permite afirmar que ampliá-lo resolveria o truncamento.

| Resposta | Clareza | Adequação | Acionabilidade |
|---|---|---|---|
| Diagnóstico · proposta | **5**. Separa observações e hipóteses com confiança baixa. | **5**. “mesma rede e o local (sala) como controle” é preciso para o chat técnico. | **5**. Explica os dois desfechos e o limite sem segundo aparelho. A ausência desse teste ainda aparece indevidamente como evidência de uma hipótese. |
| Passos truncados · proposta apenas para o trecho recebido | **4**. Declara controle e variável, mas conclui “a falha é de cobertura/interferência” com certeza excessiva. | **4**. O vocabulário é compatível com Caio e a banda alternativa é condicional. | **2**. Não ensina a selecionar e retornar à banda original. O JSON incompleto não serve como saída válida para a CLI. |

A tentativa que expirou não recebeu nota. Hydrogen é candidato a exploração futura de diagnóstico; para este desafio o Flash-Lite entregou as quatro tarefas completas. Nenhuma chamada adicional integra a consolidação.
