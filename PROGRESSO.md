# Progresso: PrivaIA

**Etapa 0.1: concluída.** Funções no `detector.py`: ... so_numeros, validar_cpf, validar_cnpj, validar_cartao, encontrar_emails, encontrar_telefones, encontrar_cpfs e encontrar_cnpjs. Falta também a nona, encontrar_cartoes.
Testes na pasta `tests`, rodar com `python -m pytest`: ... 22 passed

## O que já aprendi (Etapa 0.1)
- Ambiente virtual (.venv) separado para cada projeto
- Dígitos verificadores do CPF e do CNPJ
- Python interativo
- regex. Falso positivo e como evitar com (?<!\d) e (?!\d)
- Algoritimo de luhn. Teste que passa nem sempre testa a função certa.

## O que aprendi (Etapa 0.2)
- O replace troca todas as vezes que o trecho aparece, até dentro de outra palavra.
- sorted(lista, key=len, reverse=True) ordena do maior para o menor.
- Uma função pode devolver duas coisas: texto, dicionario = funcao(...).
- No terminal vai só o comando, sem o texto da explicação.
- sorted(..., key=len, reverse=True) e o caso do a@ dentro de aa@;
-guardar funções numa lista (TIPOS) e a prioridade de busca;
-dicionário de contagem com .get(tipo, 0);
-a chave de API vai no .env, protegido pelo .gitignore;
-ler a última linha dos erros: 404 (modelo não existe), 503 (servidor ocupado);
-a instrução de sistema, e por que [CPF_1] é diferente de [cpf_1].

## O que aprendi (Etapa 0.3)
- gerar_hash com chave secreta (HMAC);
- criar_tabela no SQLite;
- registrar com ? contra SQL injection;
- a auditoria ligada no privaia.py.
- tmp_path: uma pasta temporária que o pytest cria e apaga sozinho;
- monkeypatch no ARQUIVO, para o teste não sujar o banco de verdade;
- SELECT com .fetchall() para ler o que foi gravado.

## O que aprendi (Etapa .04)
- API com FastAPI: @app.get e @app.post;
- BaseModel como “formulário” do pedido;
- TestClient para testar a API sem ligar o servidor;
- monkeypatch para trocar uma função pela de mentira, no arquivo onde ela é usada;
- texto entre aspas é só texto, e o Python não executa;
- git restore arquivo desfaz as mudanças feitas desde o último commit.
- Colocar a API do PrivaIA dentro de um container Docker, para ela rodar igual em qualquer máquina sem depender do Python e do .venv instalados no PC.