
from detector import encontrar_emails, validar_cpf, validar_cnpj, encontrar_telefones, validar_cartao, encontrar_cpfs, encontrar_cnpjs, encontrar_cartoes

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

def test_cnpj_valido():
    assert validar_cnpj("11.222.333/0001-81") is True

def test_texto_com_dois_telefones():
    texto = "Ligue (45) 99999-1234 ou 45 3264-1234"
    assert encontrar_telefones(texto) == ["(45) 99999-1234", "45 3264-1234"]


def test_texto_sem_telefone():
    assert encontrar_telefones("texto sem telefone") == []

def test_numero_comprido_nao_e_telefone():
    assert encontrar_telefones("Pedido 1234567890123") == []


def test_cartao_valido():
    assert validar_cartao("4111 1111 1111 1111") is True


def test_cartao_digito_errado():
    assert validar_cartao("4111 1111 1111 1112") is False


def test_cartao_curto_demais():
    assert validar_cartao("1234") is False

def test_texto_com_cpf_valido_e_invalido():
    texto = "Cliente CPF 123.456.789-09, outro 123.456.789-00"
    assert encontrar_cpfs(texto) == ["123.456.789-09"]


def test_cpf_sem_pontuacao():
    assert encontrar_cpfs("CPF 12345678909") == ["12345678909"]


def test_cnpj_nao_e_confundido_com_cpf():
    assert encontrar_cpfs("CNPJ 11.222.333/0001-81") == []


def test_texto_com_cnpj_valido_e_invalido():
    texto = "Empresa 11.222.333/0001-81, outra 11.222.333/0001-80"
    assert encontrar_cnpjs(texto) == ["11.222.333/0001-81"]


def test_cnpj_sem_pontuacao():
    assert encontrar_cnpjs("CNPJ 11222333000181") == ["11222333000181"]


def test_texto_sem_cnpj():
    assert encontrar_cnpjs("texto sem cnpj") == []


def test_encontrar_cartoes():
    texto = "Cartão válido 4111 1111 1111 1111 e inválido 4111 1111 1111 1112"
    assert encontrar_cartoes(texto) == ["4111 1111 1111 1111"]

def test_texto_sem_cartao():
    assert encontrar_cartoes("texto sem cartao") == []
    