import math
import os
import re
import time
from dataclasses import dataclass

import requests
from dotenv import load_dotenv
from .storage import RAIZ

@dataclass(frozen=True)
class Config:
    model: str
    temperature: float
    max_tokens: int
    timeout: float

    @classmethod
    def carregar(cls):
        load_dotenv(RAIZ / ".env")
        if os.getenv("LLM_PROVIDER", "gemini") != "gemini":
            raise ValueError("Provedor suportado: gemini.")
        try:
            c = cls(os.getenv("LLM_MODEL", "gemini-3.5-flash-lite"), float(os.getenv("LLM_TEMPERATURE", ".3")), int(os.getenv("LLM_MAX_TOKENS", "4096")), float(os.getenv("LLM_TIMEOUT_SECONDS", "45")))
        except ValueError as erro:
            raise ValueError("Configuração numérica inválida no .env.") from erro
        if not re.fullmatch(r"[a-zA-Z0-9._-]+", c.model) or not 0 <= c.temperature <= 2 or c.max_tokens < 1 or not math.isfinite(c.timeout) or c.timeout <= 0:
            raise ValueError("Modelo, temperatura, limite de tokens ou timeout inválido.")
        return c

def chamar(config, regras, contexto):
    chave = os.getenv("LLM_API_KEY")
    if not chave:
        raise ValueError("Configure LLM_API_KEY localmente no .env.")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model}:generateContent"
    corpo = {"systemInstruction": {"parts": [{"text": regras}]}, "contents": [{"role":"user","parts":[{"text": contexto}]}],
             "generationConfig": {"temperature": config.temperature, "maxOutputTokens": config.max_tokens, "responseMimeType":"application/json"}}
    for tentativa in range(3):
        try:
            resposta = requests.post(url, json=corpo, headers={"x-goog-api-key":chave}, timeout=config.timeout)
        except requests.RequestException:
            raise ValueError("Falha de conexão ou tempo limite do Gemini.") from None
        status = resposta.status_code
        if status == 200:
            try:
                dados = resposta.json()
                candidato = dados["candidates"][0]
                if candidato.get("finishReason") != "STOP":
                    raise ValueError
                texto = "".join(p.get("text","") for p in candidato["content"]["parts"] if not p.get("thought"))
                return texto, dados.get("usageMetadata", {})
            except (ValueError, IndexError, KeyError, TypeError, AttributeError):
                raise ValueError("Gemini devolveu resposta incompleta ou bloqueada.") from None
        if status != 429 and not 500 <= status < 600:
            mensagem = {400:"Verifique a chave e as configurações.",403:"Chave inválida ou acesso negado.",401:"Chave inválida.",404:"Modelo indisponível."}
            raise ValueError(f"Gemini HTTP {status}. " + mensagem.get(status,"Requisição recusada."))
        if tentativa < 2:
            espera = resposta.headers.get("Retry-After","")
            segundos = int(espera) if espera.isdecimal() else 0
            if segundos > 60:
                break
            time.sleep(max(2 ** tentativa, segundos))
    raise ValueError(f"Gemini HTTP {status}. Limite de requisições ou indisponibilidade. Tente mais tarde.")
