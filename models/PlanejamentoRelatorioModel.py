# app/models/taskModel.py

from typing import Optional
from peewee import Model, CharField, AutoField, DateField, IntegerField
from psycopg2 import IntegrityError
from dtos.requests.PlanejamentoRelatorio.CreatePlanejamentoRelatorioRequest import CreatePlanejamentoRelatorioRequest
from dtos.responses.PlanejamentoRelatorioResponse import PlanejamentoRelatorioResponse
from dtos.responses.PaginacaoResponse import PaginacaoResponse
from servicos.postegre import Postgre
from flask import abort

# Configuração do banco de dados
db = Postgre.get_database()

class PlanejamentoRelatorio(Model):
    id = AutoField(primary_key=True)
    link = CharField()
    dataDocumento = DateField()
    tipo = IntegerField()
    
    @staticmethod
    def salvarPlanejamentoRelatorio(request: CreatePlanejamentoRelatorioRequest) -> PlanejamentoRelatorioResponse:
        """
        Salva o planejamento ou relatorio anual no banco de dados
        """
        try:
            tipo_documento = request.tipoDocumento.lower()

            if tipo_documento not in ["planejamento", "relatorio"]:
                raise IntegrityError("Tipo de documento inválido")

            planejamentoRelatorioCriado = PlanejamentoRelatorio.create(
                link=request.link,
                dataDocumento=request.anoDocumento,
                tipo=1 if tipo_documento == "planejamento" else 2
            )

            return PlanejamentoRelatorioResponse(
                id=planejamentoRelatorioCriado.id,
                link=planejamentoRelatorioCriado.link,
                anoDocumento=planejamentoRelatorioCriado.dataDocumento,
                tipo = "planejamento" if planejamentoRelatorioCriado.tipo == 1 else "relatorio"
            ).dict()

        except IntegrityError as e:
            print(f"Erro ao salvar documento: {e}")
            abort(500, description=f"Erro ao salvar documento: {e}")

    @staticmethod
    def listarPlanejamentoRelatorio(
        page: int = 1,
        per_page: int = 10, 
        idDocumento: Optional[int] = None,
        NonPaginated: Optional[bool] = False
    ) -> PaginacaoResponse[PlanejamentoRelatorioResponse]:
        """
        Lista notícias com base nos filtros fornecidos.
        """
        try:
            if idDocumento:
                response = PlanejamentoRelatorio.get_by_id(idDocumento)
                return response

            # Calcula o número de registros por tipo
            per_type = per_page // 2

            # Consulta para buscar registros do tipo 1
            planejamento = PlanejamentoRelatorio.select().where(PlanejamentoRelatorio.tipo == 1).order_by(PlanejamentoRelatorio.dataDocumento).paginate(page, per_type)
            # Consulta para buscar registros do tipo 2
            relatorio = PlanejamentoRelatorio.select().where(PlanejamentoRelatorio.tipo == 2).order_by(PlanejamentoRelatorio.dataDocumento).paginate(page, per_type)

            response = []

            for pr in planejamento:
                response.append(PlanejamentoRelatorioResponse(
                    id=pr.id,
                    link=pr.link,
                    anoDocumento=pr.dataDocumento,
                    tipo="planejamento" 
                ))

            for pr in relatorio:
                response.append(PlanejamentoRelatorioResponse(
                    id=pr.id,
                    link=pr.link,
                    anoDocumento=pr.dataDocumento,
                    tipo="relatorio"
                ))

            if NonPaginated:
                return response

            total_items = PlanejamentoRelatorio.select().count()
            total_pages = (total_items + per_page - 1) // per_page

            response_list = [
                PlanejamentoRelatorioResponse(
                    id=planejamentoRelatorio.id,
                    link=planejamentoRelatorio.link,
                    anoDocumento=planejamentoRelatorio.anoDocumento,
                    tipo=planejamentoRelatorio.tipo
                ).dict() for planejamentoRelatorio in response
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar planejamentos: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])
    
    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar documento: {e}")
            abort(500, description=f"Erro ao deletar documento: {e}")
    class Meta:
        database = db
