from detector import mascarar, restaurar
from ia import perguntar_ia


def perguntar_com_privacidade(texto):
    mascarado, etiquetas = mascarar(texto)
    print("Enviado para a IA:", mascarado)
    resposta = perguntar_ia(mascarado)
    return restaurar(resposta, etiquetas)
