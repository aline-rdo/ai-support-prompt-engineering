import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

RAIZ = Path(__file__).resolve().parent.parent
HISTORICO = RAIZ / "data/history"

def ler(caminho):
    try:
        return json.loads(caminho.read_text("utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError) as erro:
        raise ValueError(f"JSON corrompido em {caminho}") from erro

def salvar(caminho, valor):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=caminho.parent, delete=False, suffix=".tmp", mode="w", encoding="utf-8") as arquivo:
        temporario = Path(arquivo.name)
        try:
            json.dump(valor, arquivo, ensure_ascii=False, indent=2)
        except BaseException:
            arquivo.close()
            temporario.unlink()
            raise
    try:
        os.replace(temporario, caminho)
    finally:
        temporario.unlink(missing_ok=True)

def listar(pasta, **filtros):
    registros = (ler(p) for p in pasta.glob("*.json"))
    return sorted((r for r in registros if all(v is None or r.get(k) == v for k,v in filtros.items())), key=lambda r: r["timestamp"])

def catalogo(nome):
    linhas = ler(RAIZ / "data" / (nome + ".json"))
    opcoes = {"technical_level": ("leigo","intermediário","avançado"), "communication_style": ("direto","detalhado","didático"), "channel": ("telefone","chat","e-mail")}
    campos = ["id","name",*opcoes] if nome == "customers" else ["id","title","description"]
    itens = {}
    if not isinstance(linhas, list):
        raise ValueError(f"Lista esperada em {nome}.")
    for linha in linhas:
        if not isinstance(linha, dict) or any(not isinstance(linha.get(k), str) or not linha[k].strip() for k in campos):
            raise ValueError(f"Campos obrigatórios inválidos em {nome}.")
        if nome == "customers" and any(linha[k] not in valores for k,valores in opcoes.items()):
            raise ValueError(f"Perfil inválido: {linha['id']}")
        if linha["id"] in itens:
            raise ValueError("Identificador duplicado.")
        itens[linha["id"]] = linha
    return itens
