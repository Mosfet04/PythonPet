# app/controllers/taskController.py

from typing import Optional
from psycopg2 import IntegrityError
from dtos.requests.ProcessoSeletivo.CreateProcessoSeletivoRequest import CreateProcessoSeletivoRequest
from dtos.responses import PaginacaoResponse, ProcessoSeletivoResponse
from models.IntegranteModel import Integrante
from models.ProcessoSeletivoModel import ProcessoSeletivo


def create_processoSeletivo(request: CreateProcessoSeletivoRequest) -> ProcessoSeletivoResponse:
    """
    Função para inserir o processo seletivo.
    """
    integrante = Integrante.encontrarIntegrante(request.matricula, None)
    if not integrante:
        raise IntegrityError("Possivel autor não encontrado")
    
    return ProcessoSeletivo.salvarProcessoSeletivo(request)



def list_processoSeletivo(page: int = 1, per_page: int = 10, idDocumento: Optional[int] = None) -> dict:
    """
    Função para listar todos os processos seletivos do banco de dados.
    """
    response : PaginacaoResponse[ProcessoSeletivoResponse] = ProcessoSeletivo.listarProcessoSeletivo(page, per_page, idDocumento)
    return response.to_dict()

def remove_processoSeletivo(idDocumento: int, matricula: str) -> bool:
    """
    Função para deletar uma processo seletivo.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula,None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique o ID do integrante")
    
    planejamentoRelatorio : ProcessoSeletivo = ProcessoSeletivo.listarProcessoSeletivo(1, 10, idDocumento, True)

    if not planejamentoRelatorio:
        raise IntegrityError("Documento não encontrado")
    # Deleta o integrante
    return planejamentoRelatorio.deletar()
