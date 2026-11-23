"""Interface opcional para gerar e consultar atendimentos."""

import streamlit as st

from support_assistant.cli import resolver_ticket
from support_assistant.evaluation import CRITERIOS
from support_assistant.gemini import Config
from support_assistant.generators import GERADORES
from support_assistant.prompts import VERSOES
from support_assistant.storage import HISTORICO, RAIZ, catalogo, ler, listar
from visualizacao import mostrar_avaliacao, mostrar_registro


TIPOS = {"diagnosis": "Diagnóstico", "steps": "Passos de resolução",
         "questions": "Perguntas", "flow": "Fluxograma"}
ORIGINAL_ROSA = "51c126cfcbaa47e28c5274008da4dbdb"


def registros():
    # As exportações permitem consultar a demonstração em uma instalação nova.
    amostras = (ler(p) for p in (RAIZ / "samples").glob("*/*.json"))
    por_id = {r["id"]: r for r in amostras}
    por_id.update((r["id"], r) for r in listar(HISTORICO))
    return sorted(por_id.values(), key=lambda r: r["timestamp"], reverse=True)


def gerar():
    clientes, tickets = catalogo("customers"), catalogo("tickets")
    cliente = st.selectbox("Cliente", clientes.keys(), format_func=lambda k: clientes[k]["name"])
    ticket = st.selectbox("Ticket", [*tickets, "personalizado"],
                          format_func=lambda k: tickets[k]["title"] if k in tickets else "Ticket personalizado")
    if ticket == "personalizado":
        ticket = st.text_area("Relato do cliente", max_chars=8000)
    else:
        st.text(tickets[ticket]["description"])
    versao = st.selectbox("Versão do prompt", VERSOES, index=None, placeholder="Selecione uma versão")
    tipo = st.selectbox("Tipo de conteúdo", GERADORES.keys(), format_func=TIPOS.get)
    if st.button("Gerar resposta", type="primary", disabled=not (versao and ticket.strip())):
        st.session_state.pop("ultima_resposta", None)
        with st.spinner("Consultando o cache ou gerando a resposta…"):
            st.session_state.ultima_resposta = GERADORES[tipo](
                clientes[cliente], resolver_ticket(ticket), versao, Config.carregar())
    if "ultima_resposta" in st.session_state:
        r = st.session_state.ultima_resposta
        st.subheader("Última resposta gerada")
        st.caption(rotulo(r))
        mostrar_registro(r)


def rotulo(r):
    return f"{r['customer']['name']} · {TIPOS[r['content_type']]} · {r['prompt_version']} · {r['timestamp']}"


def historico():
    dados = registros()
    for campo, titulo in (("customer_id", "Cliente"), ("prompt_version", "Versão"), ("content_type", "Tipo")):
        nomes = {r["customer_id"]: r["customer"]["name"] for r in dados} if campo == "customer_id" else {}
        if campo == "content_type":
            nomes = TIPOS
        opcoes = sorted({r[campo] for r in dados})
        valor = st.selectbox(titulo, opcoes, index=None, placeholder="Todos",
                             format_func=lambda k, nomes=nomes: nomes.get(k, k), key=f"filtro_{campo}")
        if valor is not None:
            dados = [r for r in dados if r[campo] == valor]
    if not dados:
        st.info("Nenhuma execução encontrada.")
        return
    st.caption(f"Execuções encontradas: {len(dados)}")
    r = st.selectbox("Abrir execução", dados, format_func=rotulo)
    st.text(r["ticket"]["description"])
    mostrar_registro(r)


def comparar():
    grupos = {}
    for r in registros():
        if r["comparison_id"]:
            par = grupos.setdefault(r["comparison_id"], {}).setdefault(r["content_type"], {})
            par[r["prompt_version"]] = r
    pares = {grupo: {tipo: par for tipo, par in tarefas.items() if len(par) == 2}
             for grupo, tarefas in grupos.items()}
    opcoes = sorted((g for g in pares if pares[g]), key=lambda g: (g != ORIGINAL_ROSA, g))
    if not opcoes:
        st.info("Nenhuma comparação com duas versões encontrada.")
        return

    def nome(grupo):
        if grupo == ORIGINAL_ROSA:
            return "Rosa · comparação original · v1 × v2"
        par = next(iter(pares[grupo].values()))
        r = next(iter(par.values()))
        return f"{r['customer']['name']} · {' × '.join(sorted(par))} · {grupo[:8]}"

    grupo = st.selectbox("Comparação histórica", opcoes, format_func=nome)
    tarefas = pares[grupo]
    if grupo == ORIGINAL_ROSA:
        for versao in ("v1", "v2"):
            notas = [tarefas[t][versao]["evaluation"] for t in TIPOS
                     if t in tarefas and versao in tarefas[t]]
            if len(notas) == len(TIPOS) and all(notas):
                total = sum(n[c]["score"] for n in notas for c in CRITERIOS)
                st.write(f"**{versao}** · {total}/{len(notas) * len(CRITERIOS) * 5}")
            else:
                st.info(f"{versao} · avaliação incompleta")
    tipo = st.selectbox("Conteúdo comparado", [t for t in TIPOS if t in tarefas], format_func=TIPOS.get)
    par = tarefas[tipo]
    st.text(next(iter(par.values()))["ticket"]["description"])
    for coluna, versao in zip(st.columns(2), sorted(par)):
        with coluna:
            st.subheader(versao)
            mostrar_registro(par[versao])
            mostrar_avaliacao(par[versao])


def main():
    st.set_page_config(page_title="Assistente de atendimento", layout="wide")
    st.title("Assistente de atendimento técnico")
    areas = {"Gerar resposta": gerar, "Comparar prompts": comparar, "Histórico": historico}
    area = st.radio("Área", areas.keys(), horizontal=True)
    try:
        areas[area]()
    except ValueError as erro:
        st.error(str(erro))
    except OSError:
        st.error("Falha de acesso aos arquivos locais do projeto.")


if __name__ == "__main__":
    main()
