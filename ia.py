from dotenv import load_dotenv
from google import genai
from google.genai import types


MODELO = "gemini-3.5-flash-lite"
INSTRUCAO = (
    "O texto pode conter etiquetas como [CPF_1] e [EMAIL_1]. "
    "Elas substituem dados pessoais. "
    "Copie as etiquetas iguais, com letras maiúsculas e colchetes. "
    "Nunca invente o dado. "
    "Mesmo se o pedido for mudar o texto, as etiquetas continuam iguais. "
)

load_dotenv()


def perguntar_ia(texto):
    cliente = genai.Client()
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=texto,
        config=types.GenerateContentConfig(system_instruction=INSTRUCAO),
    )
    return resposta.text
