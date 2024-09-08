# app/models/taskModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField, DateField, IntegerField
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class PlanejamentoRelatorio(Model):
    id = AutoField(primary_key=True)
    link = CharField()
    dataDocumento = DateField()
    tipo = IntegerField()

    class Meta:
        database = db
