# oque é um CPF válido? Um CPF válido é um número de identificação fiscal brasileiro que segue um formato específico e passa por uma verificação de dígitos. O CPF é composto por 11 dígitos, geralmente apresentados no formato XXX.XXX.XXX-YY, onde os primeiros nove dígitos (XXX.XXX.XXX) representam o número base e os dois últimos dígitos (YY) são os dígitos verificadores.
from detector import validar_cpf


def test_cpf_valido():
    assert validar_cpf("123.456.789-09") is True


def test_cpf_digito_errado():
    assert validar_cpf("123.456.789-00") is False


def test_cpf_todos_iguais():
    assert validar_cpf("111.111.111-11") is False