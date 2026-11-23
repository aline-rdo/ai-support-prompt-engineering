"""Apresentação dos quatro formatos de resposta já validados pelo backend."""

import streamlit as st

from support_assistant.evaluation import CRITERIOS


def lista(titulo, itens):
    st.markdown(f"**{titulo}**")
    st.text("\n".join(f"• {item}" for item in itens) or "Nenhum item informado.")


def mostrar_registro(registro):
    saida = registro["output"]
    tipo = registro["content_type"]
    if saida is None:
        st.warning(registro.get("erro", "Execução sem resposta."))
    elif tipo == "diagnosis":
        lista("Evidências observadas", saida["observed_evidence"])
        for hipotese in saida["hypotheses"]:
            st.text(f"Hipótese ({hipotese['likelihood']}): {hipotese['description']}")
            lista("Evidências da hipótese", hipotese["supporting_evidence"])
        lista("Informações ausentes", saida["missing_information"])
        st.text(f"Conclusão: {saida['probable_conclusion']}\nConfiança: {saida['confidence']}")
    elif tipo == "steps":
        for passo in saida["steps"]:
            st.text(f"{passo['number']}. {passo['action']}")
            st.text(f"Resultado esperado: {passo['expected_result']}\nSe falhar: {passo['if_it_fails']}")
        st.text(f"Tempo estimado: {saida['estimated_time']}")
        lista("Quando encaminhar", saida["escalation_criteria"])
    elif tipo == "questions":
        for pergunta in saida["questions"]:
            st.text(f"{pergunta['priority']}. {pergunta['question']}\nMotivo: {pergunta['why_needed']}")
    elif tipo == "flow":
        st.code(saida["ascii_flowchart"], language=None)
        for no in saida["decision_nodes"]:
            st.text(f"{no['id']} · {no['question']}\nSim: {no['yes']}\nNão: {no['no']}")
    with st.expander("Registro JSON original"):
        st.json(registro)


def mostrar_avaliacao(registro):
    notas = registro["evaluation"]
    st.markdown("**Avaliação humana**")
    if not notas:
        st.caption("Sem avaliação registrada.")
        return
    for chave, nome in CRITERIOS.items():
        st.text(f"{nome}: {notas[chave]['score']}/5\n{notas[chave]['justification']}")
