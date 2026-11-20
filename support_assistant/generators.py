import hashlib
import json
import re
import time
from datetime import datetime, timezone
from uuid import uuid4

from .gemini import chamar
from .prompts import FORMATOS, montar
from .storage import HISTORICO, listar, salvar

def conferir(valor, molde, campo):
    if type(valor) is not type(molde):
        raise ValueError(f"Tipo inválido em {campo}.")
    if isinstance(molde, dict):
        if valor.keys() != molde.keys():
            raise ValueError(f"Campos incorretos em {campo}.")
        for k in molde:
            conferir(valor[k], molde[k], k)
    elif isinstance(molde, list):
        for item in valor:
            conferir(item, molde[0], campo)
    elif isinstance(valor, str) and not valor.strip():
        raise ValueError(f"Texto vazio em {campo}.")

def interpretar(texto, tipo):
    cerca = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", texto.strip(), re.S | re.I)
    valor = json.loads(cerca[1] if cerca else texto)
    conferir(valor, FORMATOS[tipo], tipo)
    if tipo == "questions":
        prioridades = [q["priority"] for q in valor["questions"]]
        if len(prioridades) > 5 or prioridades != list(range(1,len(prioridades)+1)):
            raise ValueError("Use até cinco perguntas com prioridades consecutivas.")
    if tipo == "steps" and [s["number"] for s in valor["steps"]] != list(range(1,len(valor["steps"])+1)):
        raise ValueError("Numere os passos a partir de 1.")
    for campo in ("steps","hypotheses","decision_nodes"):
        if campo in valor and not valor[campo]:
            raise ValueError(f"Lista vazia em {campo}.")
    if tipo == "flow" and len(valor["ascii_flowchart"].splitlines()) > 25:
        raise ValueError("Fluxograma excede 25 linhas.")
    return valor

def gerar(tipo, perfil, ticket, versao, config, *, pasta=HISTORICO, provedor=chamar, modo="normal", comparacao=None):
    regras, contexto = montar(perfil,ticket,tipo,versao)
    entrada = dict(customer=perfil, ticket=ticket, content_type=tipo, prompt_version=versao, provider="gemini", model=config.model,
                   settings=dict(temperature=config.temperature,max_tokens=config.max_tokens))
    canonico = json.dumps(entrada,sort_keys=True,ensure_ascii=False,separators=(",",":"))
    chave = hashlib.sha256(canonico.encode()).hexdigest()
    anteriores = listar(pasta, cache_key=chave) if modo == "normal" else []
    anterior = next((r for r in reversed(anteriores) if r["output"] is not None and r["cache_mode"] != "no-cache"), None)
    inicio = time.monotonic()
    registro = dict(entrada, id=uuid4().hex, timestamp=datetime.now(timezone.utc).isoformat(), customer_id=perfil["id"], cache_key=chave, cache_mode=modo,
                    cache_hit=bool(anterior), comparison_id=comparacao, output=None, evaluation=None, uso=[])
    try:
        if anterior:
            registro["output"] = anterior["output"]
        else:
            for tentativa in range(2):
                texto, uso = provedor(config,regras,contexto)
                registro["uso"].append(uso)
                try:
                    registro["output"] = interpretar(texto,tipo)
                    break
                except ValueError as erro:
                    if tentativa:
                        raise ValueError(f"JSON inválido após reparo: {erro}") from erro
                    contexto = json.dumps({"contexto":json.loads(contexto),"resposta_anterior":texto,"erro":str(erro)},ensure_ascii=False)
                    regras += "\nCorrija a resposta anterior conforme o formato original. Retorne somente JSON."
    except ValueError as erro:
        registro["erro"] = str(erro)
        raise
    finally:
        registro["latencia_ms"] = round((time.monotonic()-inicio)*1000)
        salvar(pasta / (registro["id"]+".json"),registro)
    return registro

def generate_diagnosis(*args, **kwargs):
    return gerar("diagnosis", *args, **kwargs)

def generate_resolution_steps(*args, **kwargs):
    return gerar("steps", *args, **kwargs)

def generate_clarifying_questions(*args, **kwargs):
    return gerar("questions", *args, **kwargs)

def generate_flow_summary(*args, **kwargs):
    return gerar("flow", *args, **kwargs)

GERADORES = dict(diagnosis=generate_diagnosis, steps=generate_resolution_steps, questions=generate_clarifying_questions, flow=generate_flow_summary)
