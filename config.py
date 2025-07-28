import os
from peewee import PostgresqlDatabase
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env, se existir
load_dotenv()

# Função para obter variáveis de ambiente com valor padrão
def get_env_variable(var_name, default_value=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default_value is not None:
            return default_value
        else:
            raise KeyError(f"A variável de ambiente {var_name} não está definida e nenhum valor padrão foi fornecido.")

# Verifica se as variáveis de ambiente estão sendo carregadas corretamente
print("Variáveis de ambiente carregadas:")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")
print(f"DB_SSL: {os.getenv('DB_SSL')}")
print(f"FIREBASE_PROJECT_ID: {os.getenv('FIREBASE_PROJECT_ID')}")
print(f"FIREBASE_AUTH_DOMAIN: {os.getenv('FIREBASE_AUTH_DOMAIN')}")

# Configurações do banco de dados
DATABASE = {
    'name': get_env_variable('DB_NAME', 'default_db_name'),
    'user': get_env_variable('DB_USER', 'default_user'),
    'password': get_env_variable('DB_PASSWORD', 'default_password'),
    'host': get_env_variable('DB_HOST', 'localhost'),
    'port': get_env_variable('DB_PORT', '5432'),
    'ssl': get_env_variable('DB_SSL', 'true').lower() == 'true'  # SSL habilitado por padrão para Neon
}

# Função para conectar ao banco de dados
def get_database():
    if DATABASE['ssl']:
        return PostgresqlDatabase(
            DATABASE['name'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=int(DATABASE['port']),
            sslmode='require'
        )
    else:
        return PostgresqlDatabase(
            DATABASE['name'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=int(DATABASE['port'])
        )

# Outras configurações globais
DEBUG = True
SECRET_KEY = os.urandom(24)

# Configurações do Firebase
FIREBASE_CONFIG = {
    'apiKey': get_env_variable('FIREBASE_API_KEY'),
    'authDomain': get_env_variable('FIREBASE_AUTH_DOMAIN'),
    'projectId': get_env_variable('FIREBASE_PROJECT_ID'),
    'storageBucket': get_env_variable('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': get_env_variable('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': get_env_variable('FIREBASE_APP_ID')
}

def get_firebase_config():
    """
    Retorna a configuração do Firebase
    """
    return FIREBASE_CONFIG