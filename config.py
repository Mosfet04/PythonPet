import os
from peewee import PostgresqlDatabase
from dotenv import load_dotenv

load_dotenv()

# Configurações do banco de dados
DATABASE = {
    'name': os.environ['DB_NAME'], #'petEq
    'user': os.environ['DB_USER'], #'postgres'
    'password': os.environ['DB_PASSWORD'], #'123',
    'host': os.environ['DB_HOST'], #'localhost',
    'port': os.environ['DB_PORT'],
    'ssl': os.environ.get('DB_SSL', 'false').lower() == 'true'
}

# Função para conectar ao banco de dados
def get_database():
    if DATABASE['ssl']:
        return PostgresqlDatabase(
            DATABASE['name'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port'],
            sslmode='require'
        )
    else:
        return PostgresqlDatabase(
            DATABASE['name'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port']
        )

# Outras configurações globais
DEBUG = True
SECRET_KEY = os.urandom(24)