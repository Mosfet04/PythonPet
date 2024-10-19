# app/models/taskModel.py

from typing import Optional
from peewee import Model, CharField, PostgresqlDatabase, AutoField, BooleanField, TextField, IntegerField
from psycopg2 import IntegrityError
from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo
from dtos.requests.Extensao.CreateExtensaoRequest import CreateExtensaoRequest
from dtos.requests.Extensao.UpdateExtensaoRequest import UpdateExtensaoRequest
from dtos.responses.ExtensaoResponse import ExtensaoResponse
from config import DATABASE
from dtos.responses.PaginacaoResponse import PaginacaoResponse

# Configuração do banco de dados
db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class Extensao(Model):
    id = AutoField(primary_key=True)
    nome = CharField() 
    ativo = BooleanField()
    tipo = IntegerField()
    descricao = TextField()

    @staticmethod
    def criarExtensao(request: CreateExtensaoRequest) -> ExtensaoResponse:
        try:
            extensaoCriada : Extensao = Extensao.create(
                nome=request.nome,
                descricao=request.descricao,
                ativo=True,
                tipo=request.tipo.value
            )

            return ExtensaoResponse(
                id=extensaoCriada.id,
                nome=extensaoCriada.nome,
                descricao=extensaoCriada.descricao,
                tipo = extensaoCriada.tipo,
                ativo=extensaoCriada.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao criar extensao: {e}")
            return None
        
    @staticmethod
    def listarExtensao( 
        page: int = 1, 
        per_page: int = 10,
        tipo: Optional[ExtensaoTipo] = None,
        idExtensao: Optional[int] = None,
        ativos: Optional[bool] = None) -> PaginacaoResponse[ExtensaoResponse]:
        try:
            query = Extensao.select()
            if ativos:
                query = query.where(Extensao.ativo == True)
            elif ativos == False:
                query = query.where(Extensao.ativo == False)
            
            if idExtensao:
                return query.where(Extensao.id == idExtensao).first()
            else:
                query.where(Extensao.tipo == tipo.value)
            
            total_items = query.count()
            total_pages = (total_items +per_page - 1) // per_page

            query = query.paginate(page, per_page)
            listaExtensao: list[Extensao] = list(query.execute())

            response_list = [
                ExtensaoResponse(
                    id = extensao.id,
                    nome = extensao.nome,
                    descricao = extensao.descricao,
                    tipo = extensao.tipo,
                    ativo = extensao.ativo
                ).dict() for extensao in listaExtensao
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar extensão: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])

    def atualizarExtensao(self, request: UpdateExtensaoRequest) -> ExtensaoResponse:  
        try:
            self.nome = request.nome
            self.descricao = request.descricao
            self.ativo = request.ativo
            self.tipo = request.tipo.value

            self.save()

            return ExtensaoResponse(
                id=self.id,
                nome=self.nome,
                descricao=self.descricao,
                tipo=self.tipo,
                ativo=self.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao atualizar extensao: {e}")
            return None

    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar extensao: {e}")
            return False
        
    class Meta:
        database = db
