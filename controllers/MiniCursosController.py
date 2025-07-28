# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.MiniCurso.UpdateMinicursosRequest import UpdateMinicursosRequest
from models.IntegranteModel import Integrante
from models.MiniCursosModel import MiniCursos
from dtos.requests.MiniCurso.CreateMinicursosRequest import CreateMinicursosRequest
from dtos.responses.MinicursosResponse import MinicursosResponse
from servicos.cache_service import cache_result, invalidate_cache

@cache_result("create_minicurso")
def create_minicurso(request: CreateMinicursosRequest) -> MinicursosResponse:
    """
    Função para inserir o mini-curso no banco de dados.
    """
    result = MiniCursos.criarMinicurso(request)
    
    # Invalida cache de listagem após criação
    invalidate_cache("list_minicursos")
    
    return result


@cache_result("list_minicursos")
def list_minicursos(ativo, page, per_page) -> list[MinicursosResponse]:
    """
    Função para listar todos os minicursos do banco de dados.
    """
    response = MiniCursos.listarMiniCursos(ativo, page, per_page)
    return response.to_dict()

@cache_result("update_minicursos")
def update_minicursos(request: UpdateMinicursosRequest, idConteudo: int) -> MinicursosResponse:
    """
    Função para atualizar os dados de um mini-curso.
    """
    minicurso_update : MiniCursos = MiniCursos.listarMiniCursos(None, 1, 1, idConteudo)

    if not minicurso_update:
        raise IntegrityError("Minicurso não encontrado")
    
    result = minicurso_update.atualizarMinicurso(request)
    
    # Invalida cache relacionado após atualização
    invalidate_cache("list_minicursos")
    invalidate_cache("update_minicursos", {"arg_1": idConteudo})
    
    return result

def remove_minicurso(idMinicurso: int) -> bool:
    """
    Função para deletar um mini-curso.
    """
    minicurso_remove :MiniCursos = MiniCursos.listarMiniCursos(None, 1, 1, idMinicurso)

    if not minicurso_remove:
        raise IntegrityError("Minicurso não encontrado")
    
    result = minicurso_remove.deletar()
    
    # Invalida cache relacionado após remoção
    invalidate_cache("list_minicursos")
    
    return result
