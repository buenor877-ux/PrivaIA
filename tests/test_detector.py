
from detector import encontrar_emails, validar_cpf, validar_cnpj

def test_texto_com_dois_emails():
    texto = "Falar com teste@example.com ou usuario@example.com"
    assert encontrar_emails(texto) == ["teste@example.com", "usuario@example.com"]


def test_texto_sem_email():
    assert encontrar_emails("texto sem e-mail") == []

# Testes do CPF e CNPJ
def test_cpf_valido():
    assert validar_cpf("123.456.789-09") is True


def test_cpf_digito_errado():
    assert validar_cpf("123.456.789-00") is False


def test_cpf_todos_iguais():
    assert validar_cpf("111.111.111-11") is False

def test_cnpj_digito_errado():
    assert validar_cnpj("11.222.333/0001-00") is False

def test_cnpj_todos_iguais():
    assert validar_cnpj("00.000.000/0000-00") is False

# ... testes do CPF ...
def test_cnpj_valido():
    assert validar_cnpj("11.222.333/0001-81") is True

