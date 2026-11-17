import re


def encontrar_emails(texto):
    # devolve uma lista com todos os emails encontrados no texto
    padrao = r"[A-Za-z0-9_+.-]+@(?:[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\.)+[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
    return re.findall(padrao, texto)


def encontrar_telefones(texto):
    # devolve uma lista com todos os telefones encontrados no texto
    padrao = r"(?<!\d)(?:\+?\d{2}\s*)?(?:\(\d{2}\)\s*)?\d{4,5}-?\d{4}(?!\d)"
    return re.findall(padrao, texto)


def encontrar_cartoes(texto):
    candidatos = re.findall(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)", texto)
    return [candidato for candidato in candidatos if validar_cartao(candidato)]


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
    soma = sum(
        int(digito) * peso for digito, peso in zip(numeros[:9], range(10, 1, -1))
    )
    resto = soma % 11
    primeiro = 0 if resto < 2 else 11 - resto

    # 5. Calcular o 2º dígito verificador
    soma = sum(
        int(digito) * peso for digito, peso in zip(numeros[:9], range(11, 2, -1))
    )
    soma += primeiro * 2
    resto = soma % 11
    segundo = 0 if resto < 2 else 11 - resto

    # 6. Comparar os dois com os dois últimos dígitos do CPF
    return numeros.endswith(f"{primeiro}{segundo}")


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
    return numeros.endswith(f"{primeiro}{segundo}")


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
    padrao = r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)"
    candidatos = re.findall(padrao, texto)
    # 2. Devolver só os candidatos que passam no validar_cpf
    return [candidato for candidato in candidatos if validar_cpf(candidato)]


def encontrar_cnpjs(texto):
    # Encontrar candidatos e devolver apenas os CNPJs válidos
    padrao = r"(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?-?\d{4}-?\d{2}(?!\d)"
    candidatos = re.findall(padrao, texto)
    return [candidato for candidato in candidatos if validar_cnpj(candidato)]


TIPOS = [
    ("EMAIL", encontrar_emails),
    ("CPF", encontrar_cpfs),
    ("CNPJ", encontrar_cnpjs),
    ("TELEFONE", encontrar_telefones),
    ("CARTAO", encontrar_cartoes),
]


def mascarar(texto):
    mascarado = texto
    contagem = {}
    dados_por_marcador = {}
    marcador_por_dado = {}

    for tipo, encontrar in TIPOS:
        for dado in encontrar(texto):
            if dado not in marcador_por_dado:
                numero = contagem.get(tipo, 0) + 1
                marcador = f"[{tipo}_{numero}]"
                while marcador in texto:
                    numero += 1
                    marcador = f"[{tipo}_{numero}]"

                contagem[tipo] = numero
                marcador_por_dado[dado] = marcador
                dados_por_marcador[marcador] = dado

    for dado in sorted(marcador_por_dado, key=len, reverse=True):
        mascarado = mascarado.replace(dado, marcador_por_dado[dado])

    return mascarado, dados_por_marcador


def restaurar(texto, emails_por_marcador):
    restaurado = texto
    for marcador, email in emails_por_marcador.items():
        restaurado = restaurado.replace(marcador, email)
    return restaurado

def sobrou_etiqueta(texto):
    # True se ainda tiver alguma etiqueta, como [CPF_1] ou [cpf_1]
    padrao = r"\[[A-Za-z]+_\d+\]"
    return re.search(padrao, texto) is not None