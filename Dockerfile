# Use a imagem base do Python para AWS Lambda
FROM public.ecr.aws/lambda/python:3.9

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Instale as dependências do Python
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copie o código do aplicativo para o contêiner
COPY . ${LAMBDA_TASK_ROOT}/

# Defina o handler do Lambda
CMD ["wsgi_handler.handler"]
