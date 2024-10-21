# app/models/taskModel.py

from peewee import Model, CharField, AutoField
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()
class CategoriaEventoJorneq(Model):
    id = AutoField(primary_key=True)
    titulo = CharField()


    class Meta:
        database = db
