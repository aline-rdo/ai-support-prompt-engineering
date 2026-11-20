import argparse
import json
import re
import sys
from pathlib import Path
from uuid import uuid4

from .evaluation import CRITERIOS, validar, exportar
from .gemini import Config
from .prompts import VERSOES
from .generators import GERADORES
from .storage import HISTORICO, catalogo, ler, listar, salvar

def mostrar(valor):
    print(json.dumps(valor,ensure_ascii=False,indent=2))

def argumentos():
    p = argparse.ArgumentParser(description="Atendimento técnico personalizado")
    subs = p.add_subparsers(dest="comando",required=True)
    for nome in ("customers","tickets","generate","compare","evaluate","history"):
        s = subs.add_parser(nome)
        if nome in ("generate","compare","history"):
            s.add_argument("--customer")
            s.add_argument("--type", choices=[*GERADORES,"all"] if nome!="history" else list(GERADORES))
        if nome in ("generate","compare"):
            s.add_argument("--ticket")
        if nome == "generate":
            s.add_argument("--prompt-version",choices=VERSOES)
            grupo = s.add_mutually_exclusive_group()
            grupo.add_argument("--no-cache",action="store_true")
            grupo.add_argument("--refresh",action="store_true")
        if nome == "compare":
            s.add_argument("--versions",nargs=2,choices=VERSOES,default=["v1","v2"])
        if nome in ("history","evaluate"):
            s.add_argument("--comparison-id")
        if nome == "history":
            s.add_argument("--version")
        if nome == "evaluate":
            s.add_argument("--file",type=Path,help="JSON de notas por ID de execução")
    return p

def escolher(opcoes,rotulo):
    for chave, item in opcoes.items():
        print(chave, item.get("name") or item.get("title"))
    return input(rotulo).strip()

def resolver_ticket(texto):
    itens = catalogo("tickets")
    texto = texto.strip()
    if texto in itens:
        return itens[texto]
    if not texto or re.fullmatch(r"t\d+",texto):
        raise ValueError("Ticket vazio ou ID inexistente.")
    if len(texto)>8000:
        print("Aviso: ticket truncado em 8000 caracteres.",file=sys.stderr)
    return {"description":texto[:8000]}

def avaliar(args):
    grupo = args.comparison_id or input("ID da comparação: ").strip()
    registros = listar(HISTORICO,comparison_id=grupo)
    if not registros or any(r["output"] is None for r in registros):
        raise ValueError("Comparação ausente ou com falha.")
    arquivo = ler(args.file) if args.file else None
    if args.file and (not isinstance(arquivo,dict) or set(arquivo)!={r["id"] for r in registros}):
        raise ValueError("Informe as notas de todas as execuções da comparação.")
    for r in registros:
        print(r["id"],r["content_type"],r["prompt_version"])
        mostrar(r["output"])
        notas = arquivo[r["id"]] if args.file else {
            k:dict(score=int(input(f"{titulo} (1–5): ")),justification=input("Justificativa: ")) for k,titulo in CRITERIOS.items()}
        validar(notas)
        r["evaluation"] = notas
    for r in registros:
        salvar(HISTORICO / (r["id"]+".json"),r)
    print(exportar(registros))

def executar(args):
    cmd = args.comando
    if cmd in ("customers","tickets"):
        mostrar(list(catalogo(cmd).values()))
        return
    if cmd == "history":
        mostrar(listar(HISTORICO,customer_id=args.customer,prompt_version=args.version,content_type=args.type,comparison_id=args.comparison_id))
        return
    if cmd == "evaluate":
        avaliar(args)
        return
    perfis = catalogo("customers")
    cliente = args.customer or escolher(perfis,"Cliente: ")
    if cliente not in perfis:
        raise ValueError("Cliente inexistente.")
    ticket = resolver_ticket(args.ticket if args.ticket is not None else escolher(catalogo("tickets"),"Ticket (ID ou texto): "))
    tipo = args.type or input("Tipo (diagnosis, steps, questions, flow, all): ").strip()
    if tipo not in (*GERADORES,"all"):
        raise ValueError("Tipo de conteúdo inválido.")
    config = Config.carregar()
    if cmd == "compare":
        versoes = args.versions
        if len(set(versoes)) != 2:
            raise ValueError("Selecione duas versões distintas.")
        grupo, modo = uuid4().hex,"refresh"
        print("Comparação",grupo)
    else:
        versoes = [args.prompt_version or input(f"Versão ({'/'.join(VERSOES)}): ").strip()]
        grupo = None
        modo = "refresh" if args.refresh else "no-cache" if args.no_cache else "normal"
    registros = []
    for t in GERADORES if tipo=="all" else [tipo]:
        for v in versoes:
            r = GERADORES[t](perfis[cliente],ticket,v,config,pasta=HISTORICO,modo=modo,comparacao=grupo)
            registros.append(r)
            print(t,v,"cache hit" if r["cache_hit"] else "nova geração",HISTORICO / (r["id"]+".json"))
            mostrar(r["output"])
            if t == "flow":
                print(r["output"]["ascii_flowchart"])
    if grupo:
        print(exportar(registros))

def main():
    try:
        executar(argumentos().parse_args())
    except (OSError, ValueError, EOFError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
