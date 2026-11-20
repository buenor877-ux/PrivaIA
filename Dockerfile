# a imagem base: um Linux pequeno que já tem o Python
FROM python:3.14-slim

# a pasta de trabalho dentro do container
WORKDIR /app

# primeiro só a lista de bibliotecas (assim o Docker reaproveita essa etapa se o código mudar)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# depois o resto do código
COPY . .

# a porta em que a API escuta
EXPOSE 8000

# o comando que roda quando o container liga
CMD ["fastapi", "run", "api.py", "--port", "8000"]