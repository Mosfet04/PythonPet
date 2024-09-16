# app/controllers/taskController.py

from typing import Optional
from psycopg2 import IntegrityError
from dtos.responses import PaginacaoResponse
from models.IntegranteModel import Integrante
from models.PlanejamentoRelatorioModel import PlanejamentoRelatorio
from dtos.requests.PlanejamentoRelatorio.CreatePlanejamentoRelatorioRequest import CreatePlanejamentoRelatorioRequest
from dtos.requests.Noticias.UpdateNoticiaRequest import UpdateNoticiaRequest
from dtos.responses.PlanejamentoRelatorioResponse import PlanejamentoRelatorioResponse

def create_planejamentoRelatorio(request: CreatePlanejamentoRelatorioRequest) -> PlanejamentoRelatorioResponse:
    """
    Função para inserir o documento de planejamento ou relatorio anual
    """
    integrante = Integrante.encontrarIntegrante(request.matriculaResponsavel, None)
    if not integrante:
        raise IntegrityError("Possivel autor não encontrado")
    
    return PlanejamentoRelatorio.salvarPlanejamentoRelatorio(request)



def list_planejamentoRelatorio(per_page: int = 10, idDocumento: Optional[int] = None) -> dict:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    response : PaginacaoResponse[PlanejamentoRelatorioResponse] = PlanejamentoRelatorio.listarPlanejamentoRelatorio(per_page, idDocumento)
    return response.to_dict()

def remove_planejamentoRelatorio(idDocumento: int, matricula: str) -> bool:
    """
    Função para deletar uma noticia.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula,None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique o ID do integrante")
    
    planejamentoRelatorio : PlanejamentoRelatorio = PlanejamentoRelatorio.listarPlanejamentoRelatorio(1, idDocumento, True)

    if not planejamentoRelatorio:
        raise IntegrityError("Documento não encontrado")
    # Deleta o integrante
    return planejamentoRelatorio.deletar()
