from fastapi.testclient import TestClient
import api
import privaia
import auditoria

app = api.app

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


def test_perguntar_esconde_e_restaura(monkeypatch, tmp_path):
    # 1. troque a CHAVE da auditoria por uma falsa          (igual ao Problema 3)
    monkeypatch.setattr(auditoria, "CHAVE", "chave-falsa")

    # 2. troque o ARQUIVO da auditoria pelo banco temporário (igual ao Problema 3)
    monkeypatch.setattr(auditoria, "ARQUIVO", tmp_path / "teste.db")
    # 3. crie uma lista vazia chamada recebidos
    recebidos = []

    # 4. crie a IA de mentira (uma função que recebe texto)
    def perguntar_ia_falsa(texto):
        recebidos.append(texto)
        return texto

    # 5. troque a perguntar_ia de verdade pela de mentira (no arquivo onde ela é USADA)
    monkeypatch.setattr(privaia, "perguntar_ia", perguntar_ia_falsa)
    # 6. faça o pedido POST para /perguntar com um texto que tenha o CPF 529.982.247-25
    cpf = "529.982.247-25"
    resposta = cliente.post("/perguntar", json={"texto": f"Meu CPF é {cpf}"})

    # 7. confira: o código da resposta é 200
    assert resposta.status_code == 200

    dados = resposta.json()

    # 8. confira: o CPF NÃO está no que a IA recebeu (o primeiro item da lista)
    assert cpf not in recebidos[0]

    # 9. confira: o CPF ESTÁ na resposta final
    assert cpf in dados["resposta"]
