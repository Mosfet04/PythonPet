# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.Integrante.UpdateIntegranteRequest import UpdateIntegranteRequest
from models.IntegranteModel import Integrante
from dtos.requests.Integrante.CreateIntegranteRequest import CreateIntegranteRequest
from dtos.responses.IntegranteResponse import IntegranteResponse
from servicos.cache_service import cache_result, invalidate_cache

@cache_result("create_integrante")
def create_integrante(request: CreateIntegranteRequest) -> IntegranteResponse:
    """
    Função para inserir o integrante
    """
    # Verifica se o integrante já existe na base de dados
    integrante_duplicado = Integrante.encontrarIntegrante(request.matricula, None)
    if integrante_duplicado:
        raise IntegrityError("Integrante já cadastrado")

    # Cria um novo integrante no banco de dados
    result = Integrante.criarIntegrante(request)
    
    # Invalida cache de listagem após criação
    invalidate_cache("list_integrantes")
    
    return result


@cache_result("list_integrantes")
def list_integrantes(ativo, page, per_page) -> list[IntegranteResponse]:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    response = Integrante.listarIntegrantes(ativo, page, per_page)
    return response.to_dict()

@cache_result("update_integrante")
def update_integrante(request: UpdateIntegranteRequest, idIntegrante: bool) -> IntegranteResponse:
    """
    Função para atualizar os dados de um integrante.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(None, idIntegrante)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado")

    # Atualiza os dados do integrante
    result = integrante.atualizarIntegrante(request)
    
    # Invalida cache relacionado após atualização
    invalidate_cache("list_integrantes")
    invalidate_cache("update_integrante", {"arg_1": idIntegrante})
    
    return result

def remove_integrante(idIntegrante: int) -> bool:
    """
    Função para deletar um integrante.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(None, idIntegrante)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique o ID do integrante")

    # Deleta o integrante
    result = integrante.deletarIntegrante()
    
    # Invalida cache relacionado após remoção
    invalidate_cache("list_integrantes")
    
    return result
