from peewee import Model, CharField, TextField, DateField, ForeignKeyField, AutoField, PostgresqlDatabase
from .SetorModel import Setor  # Importe o modelo Setor (se estiver em um arquivo separado)
from .IntegranteModel import Integrante  # Importe o modelo Integrante (se estiver em um arquivo separado)
from .NoticiasCategoriaModel import NoticiasCategoria
from config import DATABASE

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class Noticia(Model):
    id = AutoField(primary_key=True)
    titulo = CharField()
    conteudo = TextField()  # Texto com muitas linhas
    criado_dia = DateField()
    setor = ForeignKeyField(Setor, backref="noticias")  # Relacionamento com Setor
    autor = ForeignKeyField(Integrante, backref="noticias")  # Relacionamento com Integrante
    categoria = ForeignKeyField(NoticiasCategoria, backref="noticias")

    class Meta:
        database = db
