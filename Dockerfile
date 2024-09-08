# Use a imagem base do Python
FROM python:3.11.4

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

ARG DB_NAME 
ARG DB_USER 
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_SSL

ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_SSL=${DB_SSL}

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do aplicativo para o contêiner
COPY . .

EXPOSE 5000

# Defina o comando para executar o aplicativo
CMD ["python", "main.py"]
