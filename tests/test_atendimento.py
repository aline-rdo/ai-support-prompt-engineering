import json
from unittest.mock import Mock

import pytest
import requests

from support_assistant import cli, gemini, storage, evaluation
from support_assistant.generators import GERADORES, gerar, interpretar
from support_assistant.prompts import FORMATOS, montar

CONFIG = gemini.Config("modelo-teste",0.3,4096,45)
PERFIL = storage.catalogo("customers")["c1"]
TICKET = {"description":"Wi-Fi cai na sala."}

@pytest.mark.parametrize("tipo", GERADORES)
def test_cache_e_versao(tmp_path,tipo):
    falso = Mock(return_value=(json.dumps(FORMATOS[tipo]),{}))
    def executar(perfil, versao, modo="normal"):
        return GERADORES[tipo](perfil,TICKET,versao,CONFIG,pasta=tmp_path,provedor=falso,modo=modo)
    primeiro = executar(PERFIL,"v1")
    repetido = executar(dict(reversed(list(PERFIL.items()))),"v1")
    assert repetido["cache_hit"] and repetido["cache_key"] == primeiro["cache_key"]
    assert falso.call_count == 1
    for versao, modo in [("v2","normal"),("v1","refresh"),("v1","no-cache")]:
        assert not executar(PERFIL,versao,modo)["cache_hit"]
    assert falso.call_count == 4
    assert len(storage.listar(tmp_path,prompt_version="v1",customer_id="c1",content_type=tipo)) == 4

def test_prompt():
    v1, dados = montar(PERFIL,TICKET,"diagnosis","v1")
    v2, outros = montar(PERFIL,TICKET,"diagnosis","v2")
    assert dados == outros and json.loads(dados)["ticket"] == TICKET
    assert all(x in v2 for x in ["v2","analista","telefone","hipóteses","evidências","informações faltantes","conclusão","somente JSON"])
    assert "v1" in v1 and v1 != v2
    with pytest.raises(ValueError):
        montar(PERFIL,TICKET,"steps","v3")

@pytest.mark.parametrize("sucesso",[True,False])
def test_reparo(tmp_path,sucesso):
    falso = Mock(side_effect=[("{}",{}),('```json\n{"questions":[]}\n```' if sucesso else '[]',{})])
    def executar():
        return gerar("questions",PERFIL,TICKET,"v2",CONFIG,pasta=tmp_path,provedor=falso)
    if sucesso:
        assert executar()["output"] == {"questions":[]}
    else:
        with pytest.raises(ValueError,match="após reparo"):
            executar()
        assert storage.listar(tmp_path)[0]["output"] is None
    assert falso.call_count == 2

def test_perfil_e_arquivo_corrompido(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,"RAIZ",tmp_path)
    p = tmp_path / "data/customers.json"
    storage.salvar(p,[dict(PERFIL, channel="fax")])
    with pytest.raises(ValueError,match="Perfil inválido"):
        storage.catalogo("customers")
    p.write_text("{","utf-8")
    with pytest.raises(ValueError,match="corrompido"):
        storage.ler(p)

def test_gravacao_atomica(tmp_path,monkeypatch):
    p = tmp_path / "registro.json"
    storage.salvar(p,{"anterior":True})
    monkeypatch.setattr(storage.os,"replace",Mock(side_effect=OSError))
    with pytest.raises(OSError):
        storage.salvar(p,{"novo":True})
    assert storage.ler(p)=={"anterior":True} and list(tmp_path.iterdir())==[p]

@pytest.mark.parametrize("nota,motivo",[(0,"x"),(6,"x"),(True,"x"),(3," ")])
def test_rubrica(nota,motivo):
    with pytest.raises(ValueError):
        evaluation.validar({k:dict(score=nota,justification=motivo) for k in evaluation.CRITERIOS})

@pytest.mark.parametrize("status",[429,503,403,404])
def test_http(monkeypatch,status):
    monkeypatch.setenv("LLM_API_KEY","teste")
    post = Mock(return_value=Mock(status_code=status,headers={}))
    monkeypatch.setattr(requests,"post",post)
    esperar = Mock()
    monkeypatch.setattr(gemini.time,"sleep",esperar)
    with pytest.raises(ValueError,match=str(status)):
        gemini.chamar(CONFIG,"regras","ticket")
    repeticoes = 2 if status in (429,503) else 0
    assert post.call_count == repeticoes+1 and esperar.call_count == repeticoes

def test_chave_e_timeout(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY",raising=False)
    with pytest.raises(ValueError,match="LLM_API_KEY"):
        gemini.chamar(CONFIG,"","")
    monkeypatch.setenv("LLM_API_KEY","teste")
    monkeypatch.setattr(requests,"post",Mock(side_effect=requests.Timeout))
    with pytest.raises(ValueError,match="tempo limite"):
        gemini.chamar(CONFIG,"","")

def test_ticket(capsys):
    for texto in [" ","t99"]:
        with pytest.raises(ValueError):
            cli.resolver_ticket(texto)
    assert len(cli.resolver_ticket("ã"*8100)["description"])==8000
    assert "truncado" in capsys.readouterr().err

def test_cli_comparacao_e_avaliacao(tmp_path,monkeypatch,capsys):
    pasta = tmp_path / "historico"
    monkeypatch.setattr(cli,"HISTORICO",pasta)
    monkeypatch.setattr(evaluation,"RAIZ",tmp_path)
    monkeypatch.setenv("LLM_API_KEY","teste")
    def post(url,json,**kwargs):
        regras = json["systemInstruction"]["parts"][0]["text"]
        formato = regras.split("Formato: ")[1]
        return Mock(status_code=200,json=lambda:{"candidates":[{"finishReason":"STOP","content":{"parts":[{"text":formato}]}}]})
    enviar = Mock(side_effect=post)
    monkeypatch.setattr(requests,"post",enviar)
    def rodar(comando):
        cli.executar(cli.argumentos().parse_args(comando.split()))
    rodar("compare --customer c1 --ticket t1 --type all")
    registros = storage.listar(pasta)
    assert len(registros)==enviar.call_count==8
    assert len({r["comparison_id"] for r in registros})==1
    capsys.readouterr()
    rodar("generate --customer c1 --ticket t1 --type diagnosis --prompt-version v1")
    assert "cache hit" in capsys.readouterr().out and enviar.call_count==8
    grupo = registros[0]["comparison_id"]
    arquivo = tmp_path / "notas.json"
    storage.salvar(arquivo,{r["id"]:{k:dict(score=3,justification="Justificativa de teste") for k in evaluation.CRITERIOS} for r in registros})
    cli.executar(cli.argumentos().parse_args(["evaluate","--comparison-id",grupo,"--file",str(arquivo)]))
    assert all(r["evaluation"] for r in storage.listar(pasta,comparison_id=grupo))
    assert "Justificativa de teste" in (tmp_path/"samples"/grupo/"relatorio.md").read_text("utf-8")
