from detector import mascarar, restaurar, sobrou_etiqueta
from ia import perguntar_ia


def perguntar_com_privacidade(texto):
    mascarado, etiquetas = mascarar(texto)
    print("Enviado para a IA:", mascarado)
    resposta = perguntar_ia(mascarado)
    restaurado = restaurar(resposta, etiquetas)
    if sobrou_etiqueta(restaurado):
        print("Aviso: a IA alterou alguma etiqueta. Confira a resposta.")
    return restaurado
