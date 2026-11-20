"""Auditoria posterior à geração. Não modifica nem seleciona respostas."""
from pathlib import Path

import pytest

from support_assistant.storage import ler


def conferir_arvore(nos):
    ids = [no["id"] for no in nos]
    assert ids == [f"D{i}" for i in range(1, len(nos) + 1)]
    encontrados = {"D1"}
    for indice, no in enumerate(nos):
        assert no["id"] in encontrados
        assert no["yes"] != no["no"]
        for ramo in (no["yes"], no["no"]):
            if ramo.startswith("D") and ramo[1:].isdigit():
                assert ramo in ids[indice + 1:]
                encontrados.add(ramo)
            else:
                assert ramo.strip()


def test_arvore_real_v22():
    amostras = list((Path(__file__).resolve().parents[1] / "samples").glob("*/flow-v2.2.json"))
    assert amostras
    for arquivo in amostras:
        conferir_arvore(ler(arquivo)["output"]["decision_nodes"])


@pytest.mark.parametrize("destino", ["D1", "D9", "Encerrar"])
def test_detecta_ciclo_referencia_inexistente_ou_ramos_iguais(destino):
    with pytest.raises(AssertionError):
        conferir_arvore([{"id": "D1", "yes": destino, "no": "Encerrar"}])
