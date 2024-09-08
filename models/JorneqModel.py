# app/models/JorneqModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField, DateField
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class Jorneq(Model):
    id = AutoField(primary_key=True)
    corPrimaria = CharField() 
    corSecundaria = CharField()
    icone = CharField()
    dataInicio = DateField()
    dataFim = DateField()

    class Meta:
        database = db