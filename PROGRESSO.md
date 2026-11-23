# Progresso: PrivaIA

**Etapa 0.1: concluída.** Funções no `detector.py`: ... so_numeros, validar_cpf, validar_cnpj, validar_cartao, encontrar_emails, encontrar_telefones, encontrar_cpfs e encontrar_cnpjs. Falta também a nona, encontrar_cartoes.
Testes na pasta `tests`, rodar com `python -m pytest`: ... 22 passed
**Etapa 0.2: concluída.** No `detector.py`: mascarar, restaurar e sobrou_etiqueta, com a lista TIPOS definindo a prioridade de busca. No `ia.py`: perguntar_ia, que chama o Gemini com a instrução de sistema. No `privaia.py`: perguntar_com_privacidade, que mascara, envia para a IA e restaura os dados na resposta.
**Etapa 0.3: concluída.** No `auditoria.py`: gerar_hash (HMAC com a CHAVE_AUDITORIA do .env), criar_tabela e registrar. Cada dado enviado vira um registro no SQLite com data, tipo, hash, modelo e aviso, nunca o dado em si. Testes em `tests/test_auditoria.py` usando um banco temporário.
**Etapa 0.4: concluída.** No `api.py`, uma API com FastAPI e as rotas GET `/`, POST `/mascarar` e POST `/perguntar`, testadas em `tests/test_api.py` com TestClient e uma IA de mentira. A API roda no Docker (`Dockerfile` e `.dockerignore`), com as chaves passadas por `--env-file` e a auditoria guardada no volume `privaia-dados`. O n8n chama a API por um Webhook; o fluxo está em `n8n/privaia-webhook.json`.
**Etapa 0.5: concluída.** No `docker-compose.yml`, os serviços `api` (porta 8000, com o `.env`, `ARQUIVO_AUDITORIA` e o volume `privaia-dados`) e `n8n` (porta 5678, com o volume `n8n_data`). Os volumes antigos foram reaproveitados com `name:`. O fluxo do n8n passou a chamar a API por `http://api:8000/mascarar`. Testado de ponta a ponta pelo Webhook.
**Etapa 0.6: concluída.** No `vitrine.py`, uma página em Streamlit: caixa de texto com exemplo fictício, botão Proteger, texto original × protegido, tabela dos dados encontrados e a resposta da IA simulada, já com os dados restaurados. Não chama o Gemini nem grava auditoria. Testes em `tests/test_vitrine.py` com o AppTest do Streamlit (37 testes passando). Cor do tema em `.streamlit/config.toml` e print em `imagens/vitrine.png`. Publicada no Streamlit Cloud em https://privaia-leonardo.streamlit.app (atualiza sozinha a cada `git push` na `master`), sem nenhuma chave em Secrets.

Para rodar:
- Tudo junto: `docker compose up --build` (API em http://localhost:8000/docs e n8n em http://localhost:5678)
- Desligar: `docker compose down`
- Vitrine: `streamlit run vitrine.py`
- Webhook: POST em `http://localhost:5678/webhook/privaia` com `{"texto": "..."}`

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
- Volume é uma pasta guardada pelo Docker, fora do container. Ela sobrevive quando o container é apagado.
- -v privaia-dados:/dados pendura o volume na pasta /dados do container.
- -e ARQUIVO_AUDITORIA=... passa uma variável na hora de rodar e vale mais que o --env-file. O código não precisou mudar, porque o auditoria.py já lia o caminho com os.getenv.
- O sqlite3.connect cria um arquivo vazio se o banco não existe. Por isso o primeiro erro foi no such table.
- Só a /perguntar grava auditoria; a /mascarar não grava.
- docker volume ls lista os volumes.
- n8n monta automações ligando nós; cada nó faz uma coisa.
- O nó HTTP Request faz o mesmo que o botão Execute do /docs, só que automático.
- Dentro de um container, localhost é o próprio container. Para chegar ao PC, usa-se host.docker.internal.
- Webhook é um endereço que dispara o fluxo quando recebe um pedido.
- A Test URL (/webhook-test/) aceita um pedido por clique; a Production URL (/webhook/) funciona sempre, depois de publicar.
- {{ $json.body.texto }} é uma expressão que pega um campo do pedido que chegou.
- Um terminal ocupado com um servidor não executa comandos; para isso, abra outro.
- Um fluxo exportado sem credenciais pode ir para o git.

## O que aprendi (Etapa 0.5)
- Docker Compose liga vários containers com um só comando, no lugar de vários `docker run`.
- O `docker-compose.yml` é escrito em YAML: `chave: valor`, indentação com espaços (nunca Tab) e `- ` para itens de lista.
- Cada opção do `docker run` vira uma linha: `-p` vira `ports`, `--env-file` vira `env_file`, `-e` vira `environment` e `-v` vira `volumes`.
- `build: .` monta a imagem com o meu Dockerfile; `image:` usa uma imagem pronta, como a do n8n.
- `name:` no volume reaproveita o volume que já existia; sem ele, o Compose cria um novo com o nome da pasta na frente.
- `docker compose config --quiet` confere o arquivo sem mostrar a chave do `.env`.
- "port is already allocated": duas coisas não usam a mesma porta; `docker ps` mostra quem está usando e `docker stop` para.
- Na mesma rede do Compose, um container chama o outro pelo nome do serviço (`http://api:8000`), sem `host.docker.internal`.
- `depends_on` define a ordem de ligar os serviços.
- `docker compose down` apaga os containers, mas os volumes continuam.
- Rodei o Bandit (análise de segurança do código) e o pip-audit (falhas conhecidas nas bibliotecas): nenhum problema encontrado.
