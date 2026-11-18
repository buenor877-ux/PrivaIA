# importe a caixa de ferramentas;
import sqlite3
import hashlib
import hmac
import os
from dotenv import load_dotenv


load_dotenv()
CHAVE = os.getenv("CHAVE_AUDITORIA")
ARQUIVO = os.getenv("ARQUIVO_AUDITORIA", "auditoria.db")


# crie uma função chamada gerar_hash(dado), dentro dela, use as peças 2, 3 e 4 na ordem certa e devolva o resultado com return.
def gerar_hash(dado):
    """use as peças 2, 3 e 4."""
    if isinstance(dado, str):
        dado = dado.encode("utf-8")
    chave = CHAVE.encode("utf-8")
    return hmac.new(chave, dado, hashlib.sha256).hexdigest()


# crie uma função criar_tabela() que abre o ARQUIVO, cria a tabela registros com as 6 colunas, salva e fecha.
def criar_tabela():
    """Cria a tabela de auditoria e fecha a conexão."""
    conexao = sqlite3.connect(ARQUIVO)
    conexao.execute(
        "CREATE TABLE IF NOT EXISTS registros ("
        "id INTEGER PRIMARY KEY, "
        "data_hora TEXT, "
        "tipo_dado TEXT, "
        "impressao_digital TEXT, "
        "ia_utilizada TEXT, "
        "aviso INTEGER)"
    )
    conexao.commit()
    conexao.close()
