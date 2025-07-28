# app/controllers/taskController.py

from typing import Optional
from psycopg2 import IntegrityError
from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo
from dtos.requests.Extensao.CreateExtensaoRequest import CreateExtensaoRequest
from dtos.requests.Extensao.UpdateExtensaoRequest import UpdateExtensaoRequest
from dtos.responses.ExtensaoResponse import ExtensaoResponse
from models.ExtensaoModel import Extensao
from models.IntegranteModel import Integrante
from servicos.cache_service import cache_result, invalidate_cache


@cache_result("create_extensao")
def create_extensao(request: CreateExtensaoRequest) -> ExtensaoResponse:
    """
    Função para inserir uma extensão no banco de dados.
    """
    result = Extensao.criarExtensao(request)
    
    # Invalida cache de listagem após criação
    invalidate_cache("list_extensao")
    
    return result


@cache_result("list_extensao")
def list_extensao(ativo:Optional[bool], tipo : Optional[ExtensaoTipo], page : Optional[int], per_page : Optional[int]) -> list[ExtensaoResponse]:
    """
    Função para listar todas as extensões do banco de dados.
    """
    response = Extensao.listarExtensao(page, per_page, tipo, None, ativo)
    return response.to_dict()

@cache_result("update_extensao")
def update_extensao(request: UpdateExtensaoRequest, idConteudo: int) -> ExtensaoResponse:
    """
    Função para atualizar os dados de uma extensão
    """
    
    extensao_update : Extensao = Extensao.listarExtensao(1, 1, None, idConteudo)

    if not extensao_update:
        raise IntegrityError("Extensao coletiva não encontrada")

    result = extensao_update.atualizarExtensao(request)
    
    # Invalida cache relacionado após atualização
    invalidate_cache("list_extensao")
    invalidate_cache("update_extensao", {"arg_1": idConteudo})
    
    return result

def remove_extensao(idMinicurso: int) -> bool:
    """
    Função para deletar uma extensão.
    """
    extensao_remove : Extensao = Extensao.listarExtensao(False, 1, 1, idMinicurso)

    if not extensao_remove:
        raise IntegrityError("Extensao não encontrado")

    result = extensao_remove.deletar()
    
    # Invalida cache relacionado após remoção
    invalidate_cache("list_extensao")
    
    return result
