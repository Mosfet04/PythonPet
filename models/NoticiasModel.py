from datetime import date, datetime
from typing import Optional
from peewee import (
    Model, CharField, TextField, DateField, ForeignKeyField, AutoField, 
    PostgresqlDatabase
)
from psycopg2 import IntegrityError
from dtos.responses.PaginacaoResponse import PaginacaoResponse
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.requests.Noticias.UpdateNoticiaRequest import UpdateNoticiaRequest
from dtos.responses.NoticiaResponse import NoticiaResponse
from .SetorModel import Setor
from .IntegranteModel import Integrante
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
    """
    Modelo para representar uma notícia.
    """
    id = AutoField(primary_key=True)
    titulo = CharField()
    conteudo = TextField()
    criado_dia = DateField()
    atualizado_dia = DateField(null=True)
    setor = ForeignKeyField(Setor, backref="noticias")
    autor = ForeignKeyField(Integrante, backref="noticias")
    atualizador = ForeignKeyField(Integrante, backref="noticias", null=True)
    categoria = ForeignKeyField(NoticiasCategoria, backref="noticias")

    @staticmethod
    def criarNoticia(request: CreateNoticiaRequest, idIntegrante: int) -> NoticiaResponse:
        """
        Cria uma nova notícia.
        """
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
                titulo=noticiaCriada.titulo,
                conteudo=noticiaCriada.conteudo,
                dataCriacao=str(noticiaCriada.criado_dia),
                dataAtualizacao=str(noticiaCriada.atualizado_dia) if noticiaCriada.atualizado_dia else None,
                autor=noticiaCriada.autor.nome,
                atualizador=noticiaCriada.atualizador.nome if noticiaCriada.atualizador else None,
                setor=noticiaCriada.setor.nome,
                tituloCategoriaNoticia=noticiaCriada.categoria.nome,
                nomeSetorResponsavel=noticiaCriada.setor.nome
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao criar notícia: {e}")
            return None

    @staticmethod
    def listarNoticias(
        categoria: Optional[str] = None, data_inicial: Optional[str] = None, 
        data_final: Optional[str] = None, page: int = 1, per_page: int = 10, 
        id: Optional[int] = None, NonPaginated: Optional[bool] = False
    ) -> PaginacaoResponse[NoticiaResponse]:
        """
        Lista notícias com base nos filtros fornecidos.
        """
        try:
            query = Noticia.select().order_by(Noticia.criado_dia.desc())
            
            if categoria:
                query = query.where(Noticia.categoria.nome == categoria)
            
            if data_inicial:
                data_inicial_dt = datetime.strptime(data_inicial, '%Y-%m-%d')
                query = query.where(Noticia.criado_dia >= data_inicial_dt)
            
            if data_final:
                data_final_dt = datetime.strptime(data_final, '%Y-%m-%d')
                query = query.where(Noticia.criado_dia <= data_final_dt)
            
            if id:
                query = query.where(Noticia.id == id)
            
            total_items = query.count()
            total_pages = (total_items + per_page - 1) // per_page
            
            if NonPaginated:
                return query.first()
            
            query = query.paginate(page, per_page)
            listaNoticias = query.execute()

            response_list = [
                NoticiaResponse(
                    id=noticia.id,
                    titulo=noticia.titulo,
                    conteudo=noticia.conteudo,
                    dataCriacao=str(noticia.criado_dia),
                    dataAtualizacao=str(noticia.atualizado_dia) if noticia.atualizado_dia else None,
                    autor=noticia.autor.nome,
                    atualizador=noticia.atualizador.nome if noticia.atualizador else None,
                    setor=noticia.setor.nome,
                    tituloCategoriaNoticia=noticia.categoria.nome,
                    nomeSetorResponsavel=noticia.setor.nome
                ).dict() for noticia in listaNoticias
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar noticias: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])

    def atualizar(self, request: UpdateNoticiaRequest) -> NoticiaResponse:
        """
        Atualiza uma notícia existente.
        """
        try:
            self.titulo = request.titulo
            self.conteudo = request.conteudo
            self.atualizado_dia = date.today()
            self.atualizador = request.idAtualizador
            self.categoria = request.idCategoriaNoticia

            self.save()

            return NoticiaResponse(
                id=self.id,
                titulo=self.titulo,
                conteudo=self.conteudo,
                dataCriacao=str(self.criado_dia),
                dataAtualizacao=str(self.atualizado_dia),
                autor=self.autor.nome,
                atualizador=self.atualizador.nome,
                setor=self.setor.nome,
                tituloCategoriaNoticia=self.categoria.nome,
                nomeSetorResponsavel=self.setor.nome
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao atualizar notícia: {e}")
            return None

    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar noticia: {e}")
            return False

    class Meta:
        database = db