# app/models/ProgramacaoJorneqModel.py

from peewee import Model, CharField, AutoField, DateField, ForeignKeyField
from models.JorneqModel import Jorneq
from models.CategoriaEventoJorneqModel import CategoriaEventoJorneq
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()

class ProgramacaoJorneq(Model):
    id = AutoField(primary_key=True)
    data = DateField() 
    atividadeTitulo = CharField()
    local = CharField()
    idJorneq = ForeignKeyField(Jorneq, backref="programacoes")
    idCategoriaEvento = ForeignKeyField(CategoriaEventoJorneq, backref="programacoes")

    class Meta:
        database = db