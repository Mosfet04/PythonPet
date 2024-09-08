# app/models/taskModel.py

from peewee import Model, CharField, PostgresqlDatabase, AutoField, DateField, ForeignKeyField
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class ProcessoSeletivo(Model):
    id = AutoField(primary_key=True)
    link = CharField()
    titulo = CharField()
    dataEdital = DateField()


    class Meta:
        database = db
