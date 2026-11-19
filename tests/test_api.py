from fastapi.testclient import TestClient
from fastapi.testclient import TestClient

from api import app

# o "navegador de mentira" ligado na sua API
cliente = TestClient(app)


def test_status_responde_ok():
    resposta = cliente.get("/")

    # 200 é o código de "deu certo"
    assert resposta.status_code == 200
    # .json() transforma a resposta num dicionário
    assert resposta.json() == {"status": "ok"}


def test_mascarar_esconde_cpf_e_email():
    texto = "Meu CPF é 529.982.247-25 e meu e-mail é teste@exemplo.com"
    resposta = cliente.post("/mascarar", json={"texto": texto})

    dados = resposta.json()
    assert resposta.status_code == 200
    assert dados["encontrados"] == 2
    assert "529.982.247-25" not in dados["mascarado"]


def test_mascarar_sem_texto_da_erro():
    # pedido sem o campo "texto": o formulário Pedido deve recusar
    resposta = cliente.post("/mascarar", json={})

    assert resposta.status_code == 422
