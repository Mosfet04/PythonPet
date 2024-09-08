# app/models/ProgramacaoJorneqModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField, DateField, ForeignKeyField
from config import DATABASE
from models.JorneqModel import Jorneq
from models.CategoriaEventoJorneqModel import CategoriaEventoJorneq

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class ProgramacaoJorneq(Model):
    id = AutoField(primary_key=True)
    data = DateField() 
    atividadeTitulo = CharField()
    local = CharField()
    idJorneq = ForeignKeyField(Jorneq, backref="programacoes")
    idCategoriaEvento = ForeignKeyField(CategoriaEventoJorneq, backref="programacoes")

    class Meta:
        database = db