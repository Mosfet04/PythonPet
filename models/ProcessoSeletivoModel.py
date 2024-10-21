# app/models/taskModel.py

from typing import Optional
from peewee import Model, CharField, AutoField, DateField
from psycopg2 import IntegrityError
from dtos.requests.ProcessoSeletivo.CreateProcessoSeletivoRequest import CreateProcessoSeletivoRequest
from dtos.responses.PaginacaoResponse import PaginacaoResponse
from dtos.responses.ProcessoSeletivoResponse import ProcessoSeletivoResponse
from servicos.postegre import Postgre

# Configuração do banco de dados
db = Postgre.get_database()

class ProcessoSeletivo(Model):
    id = AutoField(primary_key=True)
    link = CharField()
    titulo = CharField()
    dataEdital = DateField()

    @staticmethod
    def salvarProcessoSeletivo(request: CreateProcessoSeletivoRequest) -> ProcessoSeletivoResponse:
        """
        Salva o planejamento ou relatorio anual no banco de dados
        """
        try:

            processoSeletivoCriado : ProcessoSeletivo = ProcessoSeletivo.create(
                link=request.link,
                dataEdital=request.dataEdital,
                titulo = request.titulo
            )

            return ProcessoSeletivoResponse(
                id=processoSeletivoCriado.id,
                link=processoSeletivoCriado.link,
                dataEdital=processoSeletivoCriado.dataEdital,
                titulo = processoSeletivoCriado.titulo
            ).dict()

        except IntegrityError as e:
            print(f"Erro ao salvar documento: {e}")
            return None

    @staticmethod
    def listarProcessoSeletivo(
        page: int = 1,
        per_page: int = 10,
        idDocumento: Optional[int] = None,
        NonPaginated: Optional[bool] = False
    ) -> PaginacaoResponse[ProcessoSeletivoResponse]:
        """
        Lista notícias com base nos filtros fornecidos.
        """
        try:
            if idDocumento:
                response = ProcessoSeletivo.get_by_id(idDocumento)
                return response

            query = ProcessoSeletivo.select().order_by(ProcessoSeletivo.dataEdital.desc())
            
            total_items = query.count()
            total_pages = (total_items + per_page - 1) // per_page

            query = query.paginate(page, per_page)

            listaProcessoSeletivo: list[ProcessoSeletivo] = list(query.execute())

            if NonPaginated:
                return listaProcessoSeletivo

            response_list = [
                ProcessoSeletivoResponse(
                    id=processoSeletivo.id,
                    link=processoSeletivo.link,
                    dataEdital=processoSeletivo.dataEdital,
                    titulo=processoSeletivo.titulo
                ).dict() for processoSeletivo in listaProcessoSeletivo
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar processos seletivos: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])
    
    def deletar(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar processo seletivo: {e}")
            return False
    class Meta:
        database = db
