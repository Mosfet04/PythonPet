# app/models/taskModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField, BooleanField
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class MiniCursos(Model):
    id = AutoField(primary_key=True)
    titulo = CharField() 
    descricao = CharField()
    imagemLink = CharField()
    ativo = BooleanField()

    class Meta:
        database = db
