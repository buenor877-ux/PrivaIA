from fastapi import FastAPI
from pydantic import BaseModel
from detector import mascarar
from privaia import perguntar_com_privacidade


# cria a API (é ela que vai "escutar" os pedidos)
app = FastAPI(title="PrivaIA")


# quando alguém pedir o endereço "/", roda a função logo abaixo
@app.get("/")
def status():
    # devolve um dicionário: o FastAPI transforma isso em resposta para quem pediu
    return {"status": "ok"}


# o "formulário": todo pedido precisa trazer um campo chamado texto
class Pedido(BaseModel):
    texto: str


@app.post("/mascarar")
def rota_mascarar(pedido: Pedido):
    # usa a mesma função do detector (ela devolve DUAS coisas)
    mascarado, etiquetas = mascarar(pedido.texto)

    # devolve só o texto mascarado e QUANTOS dados foram escondidos
    return {"mascarado": mascarado, "encontrados": len(etiquetas)}


@app.post("/perguntar")
def rota_perguntar(pedido: Pedido):
    return {"resposta": perguntar_com_privacidade(pedido.texto)}
