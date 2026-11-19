from fastapi import FastAPI

# cria a API (é ela que vai "escutar" os pedidos)
app = FastAPI(title="PrivaIA")


# quando alguém pedir o endereço "/", roda a função logo abaixo
@app.get("/")
def status():
    # devolve um dicionário: o FastAPI transforma isso em resposta para quem pediu
    return {"status": "ok"}
