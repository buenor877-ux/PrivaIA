import auditoria


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
