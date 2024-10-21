# app/models/JorneqModel.py

from peewee import Model, CharField, AutoField, DateField
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()

class Jorneq(Model):
    id = AutoField(primary_key=True)
    corPrimaria = CharField() 
    corSecundaria = CharField()
    icone = CharField()
    dataInicio = DateField()
    dataFim = DateField()

    class Meta:
        database = db