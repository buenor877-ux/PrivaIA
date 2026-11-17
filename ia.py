from dotenv import load_dotenv
from google import genai

MODELO = "gemini-3.5-flash-lite"

load_dotenv()


def perguntar_ia(texto):
    cliente = genai.Client()
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=texto,
    )
    return resposta.text
