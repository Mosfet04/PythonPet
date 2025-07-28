# app/controllers/taskController.py

from typing import Optional
from psycopg2 import IntegrityError
from dtos.requests.ProcessoSeletivo.CreateProcessoSeletivoRequest import CreateProcessoSeletivoRequest
from dtos.responses import PaginacaoResponse, ProcessoSeletivoResponse
from models.IntegranteModel import Integrante
from models.ProcessoSeletivoModel import ProcessoSeletivo
from servicos.cache_service import cache_result, invalidate_cache


@cache_result("create_processoSeletivo")
def create_processoSeletivo(request: CreateProcessoSeletivoRequest) -> ProcessoSeletivoResponse:
    """
    Função para inserir o processo seletivo.
    """
    result = ProcessoSeletivo.salvarProcessoSeletivo(request)
    
    # Invalida cache de listagem após criação
    invalidate_cache("list_processoSeletivo")
    
    return result


@cache_result("list_processoSeletivo")
def list_processoSeletivo(page: int = 1, per_page: int = 10, idDocumento: Optional[int] = None) -> dict:
    """
    Função para listar todos os processos seletivos do banco de dados.
    """
    response : PaginacaoResponse[ProcessoSeletivoResponse] = ProcessoSeletivo.listarProcessoSeletivo(page, per_page, idDocumento)
    return response.to_dict()

def remove_processoSeletivo(idDocumento: int) -> bool:
    """
    Função para deletar uma processo seletivo.
    """
    
    planejamentoRelatorio : ProcessoSeletivo = ProcessoSeletivo.listarProcessoSeletivo(1, 10, idDocumento, True)

    if not planejamentoRelatorio:
        raise IntegrityError("Documento não encontrado")
    
    result = planejamentoRelatorio.deletar()
    
    # Invalida cache relacionado após remoção
    invalidate_cache("list_processoSeletivo")
    
    return result
