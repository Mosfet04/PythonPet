# app/models/JorneqModel.py

from sqlite3 import IntegrityError
from typing import Optional
from peewee import Model, CharField, AutoField, DateField, TextField, BooleanField
from dtos.requests.CalendarioAtividades.CreateCalendarioAtividadesRequest import CreateCalendarioAtividadesRequest
from dtos.requests.CalendarioAtividades.UpdateCalendarioAtividadesRequest import UpdateCalendarioAtividadesRequest
from dtos.responses.CalendarioAtividadesResponse import CalendarioAtividadesResponse
from dtos.responses.PaginacaoResponse import PaginacaoResponse
from servicos.postegre import Postgre
from flask import abort
# Configuração do banco de dados
db = Postgre.get_database()

class CalendarioAtividades(Model):
    id = AutoField(primary_key=True)
    titulo = CharField() 
    descricao = TextField()
    dataInicio = DateField()
    ativo = BooleanField()
    local = CharField()

    @staticmethod
    def salvarCalendarioAtividades(request: CreateCalendarioAtividadesRequest) -> CalendarioAtividadesResponse:
        """
        Salva o planejamento ou relatorio anual no banco de dados
        """
        try:

            AtividadeCriada : CalendarioAtividades = CalendarioAtividades.create(
                titulo=request.titulo,
                descricao=request.descricao,
                dataInicio = request.dataInicio,
                ativo = request.ativo,
                local = request.local
            )

            return CalendarioAtividadesResponse(
                id=AtividadeCriada.id,
                titulo=AtividadeCriada.titulo,
                descricao=AtividadeCriada.descricao,
                dataInicio = AtividadeCriada.dataInicio,
                ativo = AtividadeCriada.ativo,
                local = AtividadeCriada.local
            ).dict()

        except IntegrityError as e:
            print(f"Erro ao salvar atividade: {e}")
            abort(500, description=f"Erro ao salvar atividade: {e}")

    @staticmethod
    def listarAtividades(
        page: int = 1,
        per_page: int = 10,
        ativo: Optional[bool] = None,
        idAtividade: Optional[int] = None,
        NonPaginated: Optional[bool] = False
    ) -> PaginacaoResponse[CalendarioAtividadesResponse]:
        """
        Lista notícias com base nos filtros fornecidos.
        """
        try:
            if idAtividade:
                response = CalendarioAtividades.get_by_id(idAtividade)
                return response

            query = CalendarioAtividades.select().order_by(CalendarioAtividades.dataInicio.desc())
            
            if ativo is not None:
                query = query.where(CalendarioAtividades.ativo == ativo)

            total_items = query.count()
            total_pages = (total_items + per_page - 1) // per_page

            query = query.paginate(page, per_page)

            listaAtividades: list[CalendarioAtividades] = list(query.execute())

            if NonPaginated:
                return listaAtividades

            response_list = [
                CalendarioAtividadesResponse(
                    id=Atividade.id,
                    titulo=Atividade.titulo,
                    descricao=Atividade.descricao,
                    dataInicio=Atividade.dataInicio,
                    local = Atividade.local,
                    ativo = Atividade.ativo
                ).dict() for Atividade in listaAtividades
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar atividades: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])
    

    def atualizarCalendarioAtividades(self, request: UpdateCalendarioAtividadesRequest) -> CalendarioAtividadesResponse:  
        try:
            self.titulo = request.titulo
            self.descricao = request.descricao
            self.dataInicio = request.dataInicio
            self.ativo = request.ativo
            self.local = request.local

            self.save()

            return CalendarioAtividadesResponse(
                id=self.id,
                titulo=self.titulo,
                descricao=self.descricao,
                imagem=self.imagemLink,
                ativo=self.ativo
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao atualizar atividade: {e}")
            abort(500, description=f"Erro ao atualizar atividade: {e}")

    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar atividade: {e}")
            abort(500, description=f"Erro ao deletar atividade: {e}")

    class Meta:
        database = db