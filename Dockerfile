# Use a imagem base do Python
FROM python:3.11.4

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do aplicativo para o contêiner
COPY . .

EXPOSE 5000

# Defina o comando para executar o aplicativo
CMD ["python", "main.py"]
