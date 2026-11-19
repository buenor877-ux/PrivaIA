import auditoria
import sqlite3


def test_mesmo_dado_gera_mesmo_hash(monkeypatch):
    monkeypatch.setattr(auditoria, "CHAVE", "chave-de-teste")

    hash1 = auditoria.gerar_hash("123.456.789-09")
    hash2 = auditoria.gerar_hash("123.456.789-09")

    assert hash1 == hash2


def test_dados_diferentes_geram_hash_diferente(monkeypatch):
    monkeypatch.setattr(auditoria, "CHAVE", "chave-de-teste")

    hash1 = auditoria.gerar_hash("123.456.789-09")
    hash2 = auditoria.gerar_hash("987.654.321-00")

    assert hash1 != hash2


def test_hash_nao_mostra_o_dado(monkeypatch):
    monkeypatch.setattr(auditoria, "CHAVE", "chave-de-teste")

    dado = "123.456.789-09"
    resultado = auditoria.gerar_hash(dado)

    assert dado not in resultado


def test_registrar_anota_uma_linha(monkeypatch, tmp_path):
    # troca a chave de verdade por uma falsa
    monkeypatch.setattr(auditoria, "CHAVE", "chave-de-teste")
    # troca o banco de verdade por um banco temporário
    monkeypatch.setattr(auditoria, "ARQUIVO", str(tmp_path / "teste.db"))

    # anota um CPF fictício
    auditoria.registrar("CPF", "123.456.789-09", "modelo-teste", 0)

    # abre o banco temporário e lê o que foi anotado
    conexao = sqlite3.connect(auditoria.ARQUIVO)
    linhas = conexao.execute(
        "SELECT tipo_dado, impressao_digital FROM registros"
    ).fetchall()
    conexao.close()

    # 1) foi anotada exatamente quantas linhas?
    assert len(linhas) == 1

    # 2) separa as duas colunas da primeira linha
    tipo, impressao = linhas[0]
    assert tipo == "CPF"

    # 3) o CPF NÃO pode aparecer no banco (peça 5)
    assert "123.456.789-09" not in impressao
