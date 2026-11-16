import re

def encontrar_emails(texto):
    # devolve uma lista com todos os emails encontrados no texto
    padrao = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(padrao, texto)


def encontrar_telefones(texto):
    # devolve uma lista com todos os telefones encontrados no texto
    padrao = r'(?<!\d)(?:\+?\d{2}\s*)?(?:\(\d{2}\)\s*)?\d{4,5}-?\d{4}(?!\d)'
    return re.findall(padrao, texto)

def so_numeros(texto):
    # devolve só os dígitos do texto
    numeros = ""
    for c in texto:
        if c.isdigit():
            numeros += c
    return numeros


def validar_cpf(cpf):
    # 1. Deixar só os números
    numeros = so_numeros(cpf)

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

def validar_cnpj(cnpj):
    # 1. Deixar só os números
    numeros = so_numeros(cnpj)

    # 2. Se não tiver 14 dígitos, devolver False
    if len(numeros) != 14:
        return False

    # 3. Se todos os dígitos forem iguais, devolver False
    if len(set(numeros)) == 1:
        return False

    # 4. Calcular o 1º dígito verificador
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(digito) * peso for digito, peso in zip(numeros[:12], pesos))
    resto = soma % 11
    primeiro = 0 if resto < 2 else 11 - resto

    # 5. Calcular o 2º dígito verificador
    pesos = [6] + pesos
    soma = sum(int(digito) * peso for digito, peso in zip(numeros[:12], pesos))
    soma += primeiro * pesos[-1]
    resto = soma % 11
    segundo = 0 if resto < 2 else 11 - resto

    # 6. Comparar os dois com os dois últimos dígitos do CNPJ
    return numeros[-2:] == f'{primeiro}{segundo}'

def validar_cartao(cartao):
    # Deixar só os números e validar o tamanho
    numeros = so_numeros(cartao)
    if not 13 <= len(numeros) <= 19:
        return False

    # Aplicar o algoritmo de Luhn da direita para a esquerda
    soma = 0
    dobrar = False
    for digito in reversed(numeros):
        valor = int(digito)
        if dobrar:
            valor *= 2
            if valor > 9:
                valor -= 9
        soma += valor
        dobrar = not dobrar

    return soma % 10 == 0

def encontrar_cpfs(texto):
    # 1. Achar todos os candidatos com re.findall
    padrao = r'(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)'
    candidatos = re.findall(padrao, texto)
    # 2. Criar uma lista vazia para os válidos
    cpfs_validos = []
    # 3. Para cada candidato, se validar_cpf der True, colocar na lista
    for candidato in candidatos:
        if validar_cpf(candidato):
            cpfs_validos.append(candidato)
    # 4. Devolver a lista
    return cpfs_validos