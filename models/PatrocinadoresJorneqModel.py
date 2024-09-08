# app/models/taskModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField, DateField, IntegerField, BooleanField
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class PatrocinadoresJorneq(Model):
    id = AutoField(primary_key=True)
    razaoSocial = CharField()
    ativo = BooleanField()
    logo = CharField()
    contato = CharField()
    
    class Meta:
        database = db
