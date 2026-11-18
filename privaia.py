from detector import mascarar, restaurar, sobrou_etiqueta
from auditoria import registrar
from ia import perguntar_ia, MODELO


def perguntar_com_privacidade(texto):
    mascarado, etiquetas = mascarar(texto)
    print("Enviado para a IA:", mascarado)
    resposta = perguntar_ia(mascarado)
    restaurado = restaurar(resposta, etiquetas)
    aviso = sobrou_etiqueta(restaurado)
    if aviso:
        print("Aviso: a IA alterou alguma etiqueta. Confira a resposta.")
    for marcador, dado in etiquetas.items():
        tipo = marcador.strip("[]").split("_")[0]
        registrar(tipo, dado, MODELO, aviso)
    return restaurado
