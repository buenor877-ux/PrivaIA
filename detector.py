def validar_cpf(cpf):
    # 1. Deixar só os números
    numeros = ""
    for c in cpf:
        if c.isdigit():
            numeros += c

    # 2. Se não tiver 11 dígitos, devolver False
    if len(numeros) != 11:
        return False

    # 3. Se todos os dígitos forem iguais, devolver False
    if len(set(numeros)) == 1:
        return False

    # 4. Calcular o 1º dígito verificador
    soma = sum(int(digito) * peso for digito, peso in zip(numeros[:9], range(10, 1, -1)))
    resto = soma % 11
    primeiro = 0 if resto < 2 else 11 - resto

    # 5. Calcular o 2º dígito verificador
    soma = sum(int(digito) * peso for digito, peso in zip(numeros[:9], range(11, 2, -1)))
    soma += primeiro * 2
    resto = soma % 11
    segundo = 0 if resto < 2 else 11 - resto

    # 6. Comparar os dois com os dois últimos dígitos do CPF
    return numeros[-2:] == f'{primeiro}{segundo}'


print(validar_cpf("123.456.789-09"))  # esperado: True
print(validar_cpf("123.456.789-00"))  # esperado: False
print(validar_cpf("111.111.111-11"))  # esperado: False