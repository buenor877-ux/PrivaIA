from streamlit.testing.v1 import AppTest

# Abre a vitrine sem navegador, como o TestClient faz com a API
ARQUIVO = "../vitrine.py"  # o caminho é contado a partir da pasta tests


def test_vitrine_abre_sem_erro():
    app = AppTest.from_file(ARQUIVO, default_timeout=30).run()

    assert not app.exception
    assert app.title[0].value == "PrivaIA"


def test_proteger_esconde_os_dados():
    app = AppTest.from_file(ARQUIVO, default_timeout=30).run()
    app.text_area(key="texto").input("Meu CPF é 111.444.777-35 e meu e-mail é teste@exemplo.com")
    app.button(key="proteger").click().run()

    assert not app.exception
    protegido = app.code[1].value
    assert protegido == "Meu CPF é [CPF_1] e meu e-mail é [EMAIL_1]"
    assert "111.444.777-35" not in protegido


def test_texto_sem_dados_avisa():
    app = AppTest.from_file(ARQUIVO, default_timeout=30).run()
    app.text_area(key="texto").input("Bom dia, tudo bem?")
    app.button(key="proteger").click().run()

    assert not app.exception
    assert "Nenhum dado pessoal" in app.info[0].value
