# app/models/taskModel.py

from typing import Optional
from peewee import Model, CharField, AutoField, BooleanField, TextField
from psycopg2 import IntegrityError
from dtos.requests.MiniCurso.CreateMinicursosRequest import CreateMinicursosRequest
from dtos.requests.MiniCurso.UpdateMinicursosRequest import UpdateMinicursosRequest
from dtos.responses.MinicursosResponse import MinicursosResponse
from dtos.responses.PaginacaoResponse import PaginacaoResponse
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()

class MiniCursos(Model):
    id = AutoField(primary_key=True)
    titulo = CharField() 
    descricao = TextField()
    imagemLink = CharField()
    ativo = BooleanField()

    @staticmethod
    def criarMinicurso(request: CreateMinicursosRequest) -> MinicursosResponse:
        try:
            minicursoCriado = MiniCursos.create(
                titulo=request.titulo,
                descricao=request.descricao,
                imagemLink=request.imagem,
                ativo=True
            )

            return MinicursosResponse(
                id=minicursoCriado.id,
                titulo=minicursoCriado.titulo,
                descricao=minicursoCriado.descricao,
                imagem=minicursoCriado.imagemLink,
                ativo=minicursoCriado.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao criar minicurso: {e}")
            return None
        
    @staticmethod
    def listarMiniCursos(ativos: Optional[bool], 
        page: int = 1, 
        per_page: int = 10, 
        idMiniCurso: Optional[int] = None) -> PaginacaoResponse[MinicursosResponse]:
        try:
            query = MiniCursos.select()
            if ativos == True:
                query = query.where(MiniCursos.ativo == True)
            elif ativos == False:
                query = query.where(MiniCursos.ativo == False)
            
            if idMiniCurso:
                return query.where(MiniCursos.id == idMiniCurso).first()
            
            
            total_items = query.count()
            total_pages = (total_items +per_page - 1) // per_page

            query = query.paginate(page, per_page)
            listaMinicursos : list[MiniCursos] = list(query.execute())

            response_list = [
                MinicursosResponse(
                    id = minicurso.id,
                    titulo = minicurso.titulo,
                    descricao = minicurso.descricao,
                    imagem = minicurso.imagemLink,
                    ativo = minicurso.ativo
                ).dict() for minicurso in listaMinicursos
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar minicurso: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])

    def atualizarMinicurso(self, request: UpdateMinicursosRequest) -> MinicursosResponse:  
        try:
            self.titulo = request.titulo
            self.descricao = request.descricao
            self.imagemLink = request.imagem
            self.ativo = request.ativo

            self.save()

            return MinicursosResponse(
                id=self.id,
                titulo=self.titulo,
                descricao=self.descricao,
                imagem=self.imagemLink,
                ativo=self.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao atualizar minicurso: {e}")
            return None

    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar minicurso: {e}")
            return False

    class Meta:
        database = db
