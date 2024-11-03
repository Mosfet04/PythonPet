# app/models/taskModel.py

from typing import Optional
from peewee import Model, CharField, AutoField, BooleanField, TextField
from psycopg2 import IntegrityError
from dtos.requests.Pesquisa.CreatePesquisaRequest import CreatePesquisaRequest
from dtos.requests.Pesquisa.UpdatePesquisaRequest import UpdatePesquisaRequest
from dtos.responses.PesquisaResponse import PesquisaResponse
from dtos.responses.PaginacaoResponse import PaginacaoResponse
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()

class Pesquisa(Model):
    id = AutoField(primary_key=True)
    nome = CharField() 
    ativo = BooleanField()
    descricao = TextField()

    @staticmethod
    def criarPesquisa(request: CreatePesquisaRequest) -> PesquisaResponse:
        try:
            pesquisaCriada : Pesquisa = Pesquisa.create(
                nome=request.nome,
                descricao=request.descricao,
                ativo=True
            )

            return PesquisaResponse(
                id=pesquisaCriada.id,
                nome=pesquisaCriada.nome,
                descricao=pesquisaCriada.descricao,
                ativo=pesquisaCriada.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao criar pesquisa coletiva: {e}")
            return None
        
    @staticmethod
    def listarPesquisas(ativos: Optional[bool], 
        page: int = 1, 
        per_page: int = 10, 
        idPesquisa: Optional[int] = None) -> PaginacaoResponse[PesquisaResponse]:
        try:
            query = Pesquisa.select()
            if ativos:
                query = query.where(Pesquisa.ativo == True)
            elif ativos == False:
                query = query.where(Pesquisa.ativo == False)
            
            if idPesquisa:
                return query.where(Pesquisa.id == idPesquisa).first()
            
            query = query.order_by(Pesquisa.id.desc())
            total_items = query.count()
            total_pages = (total_items +per_page - 1) // per_page

            query = query.paginate(page, per_page)
            listaPesquisa: list[Pesquisa] = list(query.execute())

            response_list = [
                PesquisaResponse(
                    id = pesquisa.id,
                    nome = pesquisa.nome,
                    descricao = pesquisa.descricao,
                    ativo = pesquisa.ativo
                ).dict() for pesquisa in listaPesquisa
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar pesquisa coletiva: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])

    def atualizarPesquisa(self, request: UpdatePesquisaRequest) -> PesquisaResponse:  
        try:
            self.nome = request.nome
            self.descricao = request.descricao
            self.ativo = request.ativo

            self.save()

            return PesquisaResponse(
                id=self.id,
                nome=self.nome,
                descricao=self.descricao,
                ativo=self.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao atualizar pesquisa coletiva: {e}")
            return None

    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar pesquisa coletiva: {e}")
            return False
        
    class Meta:
        database = db
