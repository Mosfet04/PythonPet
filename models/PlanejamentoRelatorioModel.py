# app/models/taskModel.py

from typing import Optional
from peewee import Model, CharField, PostgresqlDatabase, AutoField, DateField, IntegerField
from psycopg2 import IntegrityError
from config import DATABASE
from dtos.requests.PlanejamentoRelatorio.CreatePlanejamentoRelatorioRequest import CreatePlanejamentoRelatorioRequest
from dtos.responses.PlanejamentoRelatorioResponse import PlanejamentoRelatorioResponse
from dtos.responses.PaginacaoResponse import PaginacaoResponse

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
            return None

    @staticmethod
    def listarPlanejamentoRelatorio(
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


            response :list[PlanejamentoRelatorioResponse] = []
            planejamentoRelatorio1 = PlanejamentoRelatorio.select().where(PlanejamentoRelatorio.tipo == 1).order_by(PlanejamentoRelatorio.dataDocumento).limit(per_page // 2)
            planejamentoRelatorio2 = PlanejamentoRelatorio.select().where(PlanejamentoRelatorio.tipo == 2).order_by(PlanejamentoRelatorio.dataDocumento).limit(per_page // 2)

            for pr in planejamentoRelatorio1:
                response.append(PlanejamentoRelatorioResponse(
                    id=pr.id,
                    link=pr.link,
                    anoDocumento=pr.dataDocumento,
                    tipo="planejamento" if pr.tipo == 1 else "relatorio"
                ))

            for pr in planejamentoRelatorio2:
                response.append(PlanejamentoRelatorioResponse(
                    id=pr.id,
                    link=pr.link,
                    anoDocumento=pr.dataDocumento,
                    tipo="planejamento" if pr.tipo == 1 else "relatorio"
                ))

            if NonPaginated:
                return response
            
            response_list = [
                PlanejamentoRelatorioResponse(
                    id=planejamentoRelatorio.id,
                    link=planejamentoRelatorio.link,
                    anoDocumento=planejamentoRelatorio.anoDocumento,
                    tipo = "planejamento" if planejamentoRelatorio.tipo == 1 else "relatorio"
                ).dict() for planejamentoRelatorio in response
            ]

            return PaginacaoResponse(
                hasNextPage=True,
                page=1,
                totalPage=None,
                qtdItens=per_page,
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
            return False
    class Meta:
        database = db
