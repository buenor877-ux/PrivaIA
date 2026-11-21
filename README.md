# PrivaIA

Protege dados pessoais no uso de IA nas empresas.

O PrivaIA fica entre as pessoas da empresa e a inteligência artificial. Antes de um texto ser enviado para uma IA, ele detecta e esconde os dados pessoais. A IA faz o trabalho dela com o texto protegido, e a resposta volta com os dados originais recolocados, sem que eles tenham saído da empresa.

## Como funciona

```
Texto original:   Meu CPF é 111.444.777-35 e meu e-mail é teste@exemplo.com
Enviado à IA:     Meu CPF é [CPF_1] e meu e-mail é [EMAIL_1]
Resposta da IA:   Recebido! Seu CPF é [CPF_1] e seu e-mail é [EMAIL_1].
Resposta final:   Recebido! Seu CPF é 111.444.777-35 e seu e-mail é teste@exemplo.com.
```

1. **Detecta** os dados pessoais no texto.
2. **Mascara** cada dado com uma etiqueta, como `[CPF_1]`.
3. **Envia** o texto mascarado para a IA (Gemini).
4. **Restaura** os dados originais na resposta e avisa se a IA alterou alguma etiqueta.
5. **Registra** uma auditoria em SQLite, guardando um hash (HMAC) no lugar do dado.

## O que detecta hoje

| Dado | Validação |
|---|---|
| CPF | dígitos verificadores |
| CNPJ | dígitos verificadores |
| Cartão | algoritmo de Luhn |
| E-mail | formato |
| Telefone | formato |

## Tecnologias

- **Python** e **pytest**
- **FastAPI**: API com as rotas `/mascarar` e `/perguntar`
- **Google Gemini**: a IA
- **SQLite**: auditoria
- **Docker**: container com volume para a auditoria
- **n8n**: automação por Webhook chamando a API

## Como rodar

Crie um arquivo `.env` na pasta do projeto:
```
GEMINI_API_KEY=sua_chave_do_gemini
CHAVE_AUDITORIA=uma_chave_secreta_qualquer
```

### Com Docker
```bash
docker build -t privaia .
docker run --rm -p 8000:8000 --env-file .env -e ARQUIVO_AUDITORIA=/dados/auditoria.db -v privaia-dados:/dados privaia
```
Abra http://localhost:8000/docs para testar as rotas.

### Sem Docker
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
fastapi dev api.py
```

### Testes
```bash
python -m pytest
```

### n8n
O fluxo está em `n8n/privaia-webhook.json`. Importe no n8n e envie um POST para `/webhook/privaia` com `{"texto": "..."}`.

## Próximos passos

- Detectar nomes, endereços e dados bancários
- Suportar outras IAs além do Gemini
- Docker Compose para subir a API e o n8n juntos

## Privacidade

Os testes e exemplos usam **apenas dados fictícios**. As chaves ficam no `.env`, que não vai para o git.
