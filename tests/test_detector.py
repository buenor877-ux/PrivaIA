# Testes para o detector de CPF e CNPJ, from detector import validar_cpf, validar_cnpj
from detector import validar_cpf, validar_cnpj

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