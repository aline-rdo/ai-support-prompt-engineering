import json
from .storage import RAIZ, salvar

CRITERIOS = {"clarity":"Clareza","customer_fit":"Adequação ao nível do cliente","actionability":"Acionabilidade"}

def validar(notas):
    if not isinstance(notas,dict) or set(notas) != set(CRITERIOS):
        raise ValueError("Informe os três critérios da rubrica.")
    for nome, item in notas.items():
        if not isinstance(item,dict) or type(item.get("score")) is not int or not 1 <= item["score"] <= 5:
            raise ValueError(f"Nota de {nome} deve ser inteira entre 1 e 5.")
        if not isinstance(item.get("justification"),str) or not item["justification"].strip():
            raise ValueError(f"Justifique a nota de {nome}.")

def exportar(registros, pasta=None):
    primeiro = registros[0]
    pasta = (pasta or RAIZ / "samples") / primeiro["comparison_id"]
    linhas = ["# Comparação de prompts", "", "## Cenário", "", "```json", json.dumps({k:primeiro[k] for k in ("customer","ticket","provider","model","settings")},ensure_ascii=False,indent=2), "```"]
    for tipo in dict.fromkeys(r["content_type"] for r in registros):
        par = {r["prompt_version"]:r for r in registros if r["content_type"]==tipo}
        linhas.extend(["",f"## {tipo}",""])
        for versao,r in par.items():
            nome = f"{tipo}-{versao}.json"
            salvar(pasta / nome,r)
            linhas.append(f"- [{versao}]({nome})")
        linhas.extend(["","| Critério | " + " | ".join(par) + " |","|" + "---|" * (len(par)+1)])
        for k,titulo in CRITERIOS.items():
            celulas = [titulo]
            for versao in par:
                item = (par.get(versao,{}).get("evaluation") or {}).get(k)
                celulas.append(f"{item['score']} — {item['justification']}".replace("|","\\|").replace("\n"," ") if item else "Pendente")
            linhas.append("| "+" | ".join(celulas)+" |")
    destino = pasta / "relatorio.md"
    destino.write_text("\n".join(linhas)+"\n","utf-8")
    return destino
