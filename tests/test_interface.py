"""Integração da interface opcional, sem rede ou escrita no histórico."""

from unittest.mock import Mock

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest

from support_assistant.generators import GERADORES
from support_assistant.storage import RAIZ, ler


def abrir(monkeypatch):
    def bloquear(*args, **kwargs):
        pytest.fail("A interface tentou acessar a rede durante o teste.")

    monkeypatch.setattr("requests.sessions.Session.request", bloquear)
    return AppTest.from_file(str(RAIZ / "app.py"), default_timeout=30).run()


def test_geracao_exige_clique_e_preserva_escolhas(monkeypatch):
    registro = ler(next((RAIZ / "samples").glob("*/steps-v2.json")))
    gerar = Mock(return_value=registro)
    monkeypatch.setitem(GERADORES, "steps", gerar)
    tela = abrir(monkeypatch)
    assert tela.button[0].disabled
    tela.selectbox[1].set_value("personalizado").run()
    tela.text_area[0].set_value("Aplicativo fecha ao abrir.")
    tela.selectbox[2].set_value("v2")
    tela.selectbox[3].set_value("steps").run()
    gerar.assert_not_called()
    tela.button[0].click().run()
    assert not tela.exception
    gerar.assert_called_once()
    perfil, ticket, versao, _ = gerar.call_args.args
    assert (perfil["id"], ticket, versao) == ("c1", {"description": "Aplicativo fecha ao abrir."}, "v2")
    assert tela.json
    tela.run()
    gerar.assert_called_once()


def test_consulta_comparacao_e_historico(monkeypatch):
    tela = abrir(monkeypatch)
    tela.radio[0].set_value("Comparar prompts").run()
    assert not tela.exception
    assert sum("41/60" in item.value for item in tela.markdown) == 2
    for tipo in GERADORES:
        tela.selectbox[1].set_value(tipo).run()
        assert not tela.exception
        assert len(tela.json) == 2
        assert sum("Acionabilidade:" in item.value for item in tela.text) == 2
    tela.radio[0].set_value("Histórico").run()
    tela.selectbox[0].set_value("c2").run()
    tela.selectbox[1].set_value("v2.2").run()
    tela.selectbox[2].set_value("steps").run()
    assert not tela.exception
    r = tela.selectbox[3].value
    assert (r["customer_id"], r["prompt_version"], r["content_type"]) == ("c2", "v2.2", "steps")
    assert len(tela.json) == 1
