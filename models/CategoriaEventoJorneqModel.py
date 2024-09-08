# app/models/taskModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class CategoriaEventoJorneq(Model):
    id = AutoField(primary_key=True)
    titulo = CharField()


    class Meta:
        database = db
