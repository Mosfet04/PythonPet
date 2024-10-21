# app/models/taskModel.py

from peewee import Model, CharField, AutoField, DateField, IntegerField, BooleanField
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()

class PatrocinadoresJorneq(Model):
    id = AutoField(primary_key=True)
    razaoSocial = CharField()
    ativo = BooleanField()
    logo = CharField()
    contato = CharField()
    
    class Meta:
        database = db
