# 🚀 Guia Completo: Deploy da API Flask no AWS Lambda com Docker

Este guia detalha **passo a passo** como fazer o deploy de uma aplicação Flask no AWS Lambda usando containers Docker, permitindo ultrapassar o limite de 250MB das funções Lambda tradicionais.

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- ✅ **Node.js** (v14 ou superior) - [Download](https://nodejs.org/)
- ✅ **Python** (3.9 ou superior) - [Download](https://www.python.org/)
- ✅ **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)
- ✅ **AWS CLI** - [Download](https://aws.amazon.com/cli/)
- ✅ **Conta AWS** com credenciais configuradas

---

## 🔧 Passo 1: Configurar Credenciais AWS

### 1.1 Instalar AWS CLI

```bash
# Windows (usando winget)
winget install Amazon.AWSCLI

# Ou baixe o instalador MSI do site oficial
```

### 1.2 Configurar Credenciais

```bash
aws configure
```

Você precisará fornecer:
- **AWS Access Key ID:** (fornecido pelo administrador AWS)
- **AWS Secret Access Key:** (fornecido pelo administrador AWS)
- **Default region:** `us-east-1`
- **Default output format:** `json`

### 1.3 Verificar Configuração

```bash
aws sts get-caller-identity
```

Deve retornar suas informações de conta AWS.

---

## 🔐 Passo 2: Configurar Permissões IAM

O usuário IAM precisa das seguintes permissões. Peça ao administrador AWS para adicionar estas políticas:

### 2.1 Políticas Necessárias

**Opção 1 - Políticas Gerenciadas (Recomendado):**
- `AWSLambdaFullAccess`
- `AmazonEC2ContainerRegistryFullAccess`
- `AWSCloudFormationFullAccess`
- `IAMFullAccess` (ou permissões limitadas de IAM)
- `AmazonS3FullAccess`

**Opção 2 - Política Customizada (Mínimo Necessário):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "logs:*",
        "iam:GetRole",
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:PassRole",
        "iam:TagRole",
        "iam:UntagRole",
        "iam:CreateServiceLinkedRole",
        "lambda:*",
        "apigateway:*",
        "events:*",
        "ecr:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### 2.2 Como Adicionar Permissões (Para Administradores)

1. Acesse o [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Vá em **Users** → Selecione o usuário
3. Clique em **Add permissions** → **Attach policies directly**
4. Selecione as políticas listadas acima
5. Clique em **Next** → **Add permissions**

---

## 📦 Passo 3: Instalar Serverless Framework

```bash
# Instalar globalmente
npm install -g serverless

# Verificar instalação
serverless --version
```

---

## 🐳 Passo 4: Configurar Docker

### 4.1 Instalar Docker Desktop

1. Baixe o [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Instale seguindo as instruções
3. **Inicie o Docker Desktop** (importante!)

### 4.2 Verificar Docker

```bash
docker --version
docker ps
```

Se aparecer erro "cannot find the file specified", significa que o Docker Desktop não está rodando. Inicie-o pelo menu Iniciar.

---

## 📁 Passo 5: Estrutura do Projeto

Certifique-se de que seu projeto tem os seguintes arquivos:

```
PythonPet/
├── main.py                    # Aplicação Flask principal
├── wsgi_handler.py           # Handler para AWS Lambda
├── requirements.txt          # Dependências Python
├── Dockerfile               # Configuração do container
├── serverless.yml           # Configuração do Serverless Framework
├── controllers/             # Controllers da API
├── facade/                  # Facades
├── models/                  # Models do banco
└── servicos/               # Serviços (DB, Firebase, etc)
```

---

## 🔨 Passo 6: Criar Arquivos de Configuração

### 6.1 Criar `Dockerfile`

```dockerfile
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
```

### 6.2 Criar `wsgi_handler.py`

```python
"""
AWS Lambda handler for Flask application using serverless-wsgi
"""
try:
    import unzip_requirements
except ImportError:
    pass

import serverless_wsgi
from main import app

def handler(event, context):
    """Lambda handler function"""
    return serverless_wsgi.handle_request(app, event, context)
```

### 6.3 Atualizar `requirements.txt`

Adicione ao final do arquivo:

```txt
serverless-wsgi==3.0.4
```

### 6.4 Criar `serverless.yml`

```yaml
service: python-pet-api

provider:
  name: aws
  region: us-east-1
  memorySize: 512
  timeout: 30
  deploymentBucket:
    name: python-pet-api-deployments-${aws:accountId}
    serverSideEncryption: AES256
  ecr:
    images:
      appimage:
        path: ./
        platform: linux/amd64
  environment:
    # Variáveis de ambiente do banco de dados
    DB_NAME: seu_db_name
    DB_USER: seu_db_user
    DB_PASSWORD: sua_senha
    DB_HOST: seu_host.aws.neon.tech
    DB_PORT: 5432
    DB_SSL: true
    # Variáveis do Firebase (se usar)
    FIREBASE_API_KEY: sua_api_key
    FIREBASE_AUTH_DOMAIN: seu_projeto.firebaseapp.com
    FIREBASE_PROJECT_ID: seu_projeto_id
    FIREBASE_STORAGE_BUCKET: seu_bucket.appspot.com
    FIREBASE_MESSAGING_SENDER_ID: seu_sender_id
    FIREBASE_APP_ID: seu_app_id

functions:
  api:
    image:
      name: appimage
    events:
      - httpApi: '*'
```

**⚠️ IMPORTANTE:** Substitua os valores das variáveis de ambiente pelos seus valores reais!

---

## 🚀 Passo 7: Deploy

### 7.1 Criar Bucket S3 para Deployments

```bash
aws s3 mb s3://python-pet-api-deployments-SEU_ACCOUNT_ID --region us-east-1
```

**Nota:** Substitua `SEU_ACCOUNT_ID` pelo seu Account ID da AWS (número de 12 dígitos). Para descobrir:

```bash
aws sts get-caller-identity --query Account --output text
```

### 7.2 Configurar Criptografia no Bucket

```bash
aws s3api put-bucket-encryption --bucket python-pet-api-deployments-SEU_ACCOUNT_ID --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

### 7.3 Criar Repositório ECR

```bash
aws ecr create-repository --repository-name serverless-python-pet-api-dev --region us-east-1
```

### 7.4 Fazer o Deploy

```bash
# Certifique-se de estar no diretório do projeto
cd C:\www\PythonPet

# Certifique-se de que o Docker Desktop está rodando
docker ps

# Faça o deploy
serverless deploy
```

O processo pode levar de 2 a 5 minutos. Você verá:

1. **Building Docker image** - Construindo a imagem
2. **Pushing to ECR** - Enviando para o registro de containers
3. **Creating CloudFormation stack** - Criando recursos AWS
4. **Deploying Lambda function** - Fazendo deploy da função

### 7.5 Resultado Esperado

Ao final, você verá algo como:

```
✔ Service deployed to stack python-pet-api-dev (150s)

endpoint: ANY - https://XXXXXXXXXX.execute-api.us-east-1.amazonaws.com
functions:
  api: python-pet-api-dev-api
```

**Copie o endpoint!** Este é o URL da sua API.

---

## ✅ Passo 8: Testar a API

### 8.1 Testar Health Check

```bash
curl https://SEU_ENDPOINT.execute-api.us-east-1.amazonaws.com/api/health
```

Resposta esperada:
```json
{
  "service": "PythonPet API",
  "status": "healthy",
  "timestamp": "2026-01-13T01:40:16.798409+00:00",
  "version": "1.0.0"
}
```

### 8.2 Testar Documentação Swagger

Acesse no navegador:
```
https://SEU_ENDPOINT.execute-api.us-east-1.amazonaws.com/api/docs/
```

### 8.3 Testar Endpoints da API

```bash
# Windows PowerShell
Invoke-WebRequest -Uri "https://SEU_ENDPOINT.execute-api.us-east-1.amazonaws.com/api/integrantes?page=1&size=5" -UseBasicParsing

# Linux/Mac
curl https://SEU_ENDPOINT.execute-api.us-east-1.amazonaws.com/api/integrantes?page=1&size=5
```

---

## 🔄 Passo 9: Atualizar a Aplicação

Quando você fizer alterações no código:

```bash
# 1. Certifique-se de que o Docker está rodando
docker ps

# 2. Faça o deploy novamente
serverless deploy
```

O Serverless Framework irá:
- Reconstruir a imagem Docker
- Fazer upload para o ECR
- Atualizar a função Lambda

**Tempo típico:** 2-5 minutos

---

## 📊 Passo 10: Monitorar e Ver Logs

### 10.1 Ver Logs em Tempo Real

```bash
serverless logs -f api --tail
```

### 10.2 Ver Informações do Deploy

```bash
serverless info
```

### 10.3 Monitorar no AWS Console

1. Acesse o [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Encontre a função `python-pet-api-dev-api`
3. Aba **Monitor** → Métricas e logs
4. Aba **Configuration** → Variáveis de ambiente

### 10.4 Ver Custos

1. Acesse o [AWS Cost Explorer](https://console.aws.amazon.com/cost-management/)
2. Visualize os custos por serviço (Lambda, ECR, API Gateway)

---

## 🗑️ Passo 11: Remover o Deploy (Opcional)

Se precisar remover tudo da AWS:

```bash
serverless remove
```

Isso irá:
- ✅ Deletar a função Lambda
- ✅ Deletar o API Gateway
- ✅ Deletar os logs do CloudWatch
- ✅ Deletar a stack do CloudFormation

**⚠️ Nota:** O bucket S3 e o repositório ECR precisam ser deletados manualmente.

---

## 🐛 Solução de Problemas Comuns

### Problema 1: "Docker não encontrado"

**Erro:** `error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping"`

**Solução:** Inicie o Docker Desktop pelo menu Iniciar do Windows.

### Problema 2: "Access Denied" ao fazer deploy

**Erro:** `User is not authorized to perform: ecr:DescribeRepositories`

**Solução:** Verifique as permissões IAM (Passo 2). Peça ao administrador AWS para adicionar as políticas necessárias.

### Problema 3: "Internal Server Error" na API

**Solução:** Verifique os logs:
```bash
serverless logs -f api --tail
```

Procure por erros de importação ou configuração incorreta das variáveis de ambiente.

### Problema 4: "Unzipped size must be smaller than 262144000 bytes"

**Erro:** O pacote é maior que 250MB

**Solução:** Você já está usando containers Docker, que suportam até 10GB. Se ainda aparecer este erro, significa que está usando a configuração antiga. Verifique se o `serverless.yml` está correto (deve ter `ecr.images` em vez de `runtime`).

### Problema 5: Timeout na API

**Erro:** A requisição demora muito e falha

**Solução:** Aumente o timeout no `serverless.yml`:
```yaml
provider:
  timeout: 60  # Aumentar de 30 para 60 segundos
```

---

## 💰 Estimativa de Custos

### Custos Mensais Esperados

Para uma aplicação de PET universitário com **tráfego baixo/médio**:

| Serviço | Custo Estimado |
|---------|----------------|
| **Lambda** (< 1M requisições) | $0 - $5/mês |
| **API Gateway** | $0 - $2/mês |
| **ECR** (storage de imagens) | $0.50 - $1/mês |
| **CloudWatch Logs** | $0.50/mês |
| **S3** (deployments) | $0.10/mês |
| **TOTAL** | **$1 - $9/mês** |

**Free Tier AWS (primeiro ano):**
- 1 milhão de requisições Lambda/mês GRÁTIS
- 400.000 GB-segundos Lambda/mês GRÁTIS

**Conclusão:** Nos primeiros 12 meses, o custo será provavelmente **$0 - $2/mês**! 🎉

---

## 📚 Recursos Adicionais

- [Documentação AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [Documentação Serverless Framework](https://www.serverless.com/framework/docs/)
- [AWS Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [Calculadora de Custos AWS](https://calculator.aws/)

---

## 🎓 Glossário

- **Lambda:** Serviço serverless da AWS que executa código sem gerenciar servidores
- **ECR:** Elastic Container Registry - registro de imagens Docker da AWS
- **API Gateway:** Serviço que cria e gerencia APIs REST/HTTP
- **CloudFormation:** Infraestrutura como código da AWS
- **IAM:** Identity and Access Management - gerenciamento de permissões
- **Serverless:** Arquitetura onde você não gerencia servidores
- **Container/Docker:** Empacotamento de aplicação com todas dependências
- **Free Tier:** Nível gratuito da AWS para novos usuários (12 meses)

---

## 👥 Suporte

Se encontrar problemas:

1. Consulte a seção **Solução de Problemas** acima
2. Verifique os logs: `serverless logs -f api --tail`
3. Consulte a documentação oficial do Serverless Framework
4. Entre em contato com o administrador AWS do projeto

---

**Criado em:** Janeiro de 2026  
**Versão:** 1.0  
**Autor:** Documentação gerada para o projeto PythonPET

---

## 🔄 Changelog

### Versão 1.0 (13/01/2026)
- ✅ Deploy inicial com Docker containers
- ✅ Configuração de permissões IAM
- ✅ Integração com banco de dados PostgreSQL (Neon)
- ✅ Integração com Firebase
- ✅ Documentação Swagger funcional
- ✅ API funcionando em produção
