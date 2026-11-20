# Comparação de prompts

## Cenário

```json
{
  "customer": {
    "id": "c2",
    "name": "Caio",
    "technical_level": "avançado",
    "communication_style": "direto",
    "channel": "chat"
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

## steps

- [v1](steps-v1.json)
- [v2](steps-v2.json)

| Critério | v1 | v2 |
|---|---|---|
| Clareza | Pendente | Pendente |
| Adequação ao nível do cliente | Pendente | Pendente |
| Acionabilidade | Pendente | Pendente |
