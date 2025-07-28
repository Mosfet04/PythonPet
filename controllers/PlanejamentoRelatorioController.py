# app/controllers/taskController.py

from typing import Optional
from psycopg2 import IntegrityError
from dtos.responses import PaginacaoResponse
from models.IntegranteModel import Integrante
from models.PlanejamentoRelatorioModel import PlanejamentoRelatorio
from dtos.requests.PlanejamentoRelatorio.CreatePlanejamentoRelatorioRequest import CreatePlanejamentoRelatorioRequest
from dtos.requests.Noticias.UpdateNoticiaRequest import UpdateNoticiaRequest
from dtos.responses.PlanejamentoRelatorioResponse import PlanejamentoRelatorioResponse
from servicos.cache_service import cache_result, invalidate_cache

@cache_result("create_planejamentoRelatorio")
def create_planejamentoRelatorio(request: CreatePlanejamentoRelatorioRequest) -> PlanejamentoRelatorioResponse:
    """
    Função para inserir o documento de planejamento ou relatorio anual
    """
    result = PlanejamentoRelatorio.salvarPlanejamentoRelatorio(request)
    
    # Invalida cache de listagem após criação
    invalidate_cache("list_planejamentoRelatorio")
    
    return result


@cache_result("list_planejamentoRelatorio")
def list_planejamentoRelatorio(page: int = 1, per_page: int = 10, idDocumento: Optional[int] = None) -> dict:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    response : PaginacaoResponse[PlanejamentoRelatorioResponse] = PlanejamentoRelatorio.listarPlanejamentoRelatorio(page, per_page, idDocumento)
    return response.to_dict()

def remove_planejamentoRelatorio(idDocumento: int) -> bool:
    """
    Função para deletar uma noticia.
    """
    planejamentoRelatorio : PlanejamentoRelatorio = PlanejamentoRelatorio.listarPlanejamentoRelatorio(1, 10, idDocumento, True)

    if not planejamentoRelatorio:
        raise IntegrityError("Documento não encontrado")
    
    result = planejamentoRelatorio.deletar()
    
    # Invalida cache relacionado após remoção
    invalidate_cache("list_planejamentoRelatorio")
    
    return result
