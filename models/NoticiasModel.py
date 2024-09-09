from datetime import date
from peewee import Model, CharField, TextField, DateField, ForeignKeyField, AutoField, PostgresqlDatabase, DoesNotExist, OperationalError
from psycopg2 import IntegrityError
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.responses.NoticiaResponse import NoticiaResponse
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

    def criarNoticia(request : CreateNoticiaRequest, idIntegrante: int) -> NoticiaResponse:
        try:
            noticiaCriada = Noticia.create(
                titulo=request.titulo,
                conteudo=request.conteudo,
                criado_dia=date.today(),
                autor=idIntegrante,
                setor=request.idSetorResponsavel,
                categoria=request.idCategoriaNoticia,
            )

            return NoticiaResponse(
                id=noticiaCriada.id,
                conteudo=noticiaCriada.conteudo,
                criado_dia=str(noticiaCriada.criado_dia),
                autor=noticiaCriada.autor.nome,
                setor=noticiaCriada.setor.nome,
                tituloCategoriaNoticia=noticiaCriada.categoria.titulo).dict()
        except IntegrityError as e:
            print(f"Erro ao criar notícia: {e}")
            return None

    def listarNoticias() -> list[NoticiaResponse]:
        try:
            listaNoticias: list[NoticiaResponse] = None
            
            try:
                listaNoticias = Noticia.select()
            except (DoesNotExist, OperationalError) as e:
                print(f"Erro ao buscar todas as noticias: {e}")
                return []
           

            response_list = [
                NoticiaResponse(
                    id = noticia.id,
                    titulo = noticia.titulo,
                    conteudo = noticia.conteudo,
                    autor = noticia.autor.nome,
                    dataCriacao = str(noticia.criado_dia),
                    nomeSetorResponsavel = noticia.setor.nome,
                    tituloCategoriaNoticia = noticia.categoria.nome
                ).dict() for noticia in listaNoticias
            ]

            return response_list
        except Exception as e:
            print(f"Erro inesperado ao listar integrantes: {e}")
            return []
    class Meta:
        database = db
