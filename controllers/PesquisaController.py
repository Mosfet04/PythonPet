# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.Pesquisa.CreatePesquisaRequest import CreatePesquisaRequest
from dtos.requests.Pesquisa.UpdatePesquisaRequest import UpdatePesquisaRequest
from dtos.responses.PesquisaResponse import PesquisaResponse
from models.PesquisaModel import Pesquisa
from models.IntegranteModel import Integrante
from servicos.cache_service import cache_result, invalidate_cache


@cache_result("create_pesquisa")
def create_pesquisa(request: CreatePesquisaRequest) -> PesquisaResponse:
    """
    Função para inserir pesquisa coletiva no banco de dados.
    """
    result = Pesquisa.criarPesquisa(request)
    
    # Invalida cache de listagem após criação
    invalidate_cache("list_pesquisas")
    
    return result


@cache_result("list_pesquisas")
def list_pesquisas(ativo, page, per_page) -> list[PesquisaResponse]:
    """
    Função para listar todas as pesquisas coletivas do banco de dados.
    """
    response = Pesquisa.listarPesquisas(ativo, page, per_page)
    return response.to_dict()

@cache_result("update_pesquisas") 
def update_pesquisas(request: UpdatePesquisaRequest, idPesquisa: int) -> PesquisaResponse:
    """
    Função para atualizar os dados de uma pesquisa coletiva
    """
    
    pesquisa_update : Pesquisa = Pesquisa.listarPesquisas(None, 1, 1, idPesquisa)

    if not pesquisa_update:
        raise IntegrityError("Pesquisa coletiva não encontrada")
    
    # Atualiza os dados do integrante
    result = pesquisa_update.atualizarPesquisa(request)
    
    # Invalida cache relacionado após atualização
    invalidate_cache("list_pesquisas")
    invalidate_cache("update_pesquisas", {"arg_1": idPesquisa})
    
    return result

def remove_pesquisa(idMinicurso: int) -> bool:
    """
    Função para deletar uma pesquisa coletiva.
    """
    pesquisa_remove : Pesquisa = Pesquisa.listarPesquisas(None, 1, 1, idMinicurso)

    if not pesquisa_remove:
        raise IntegrityError("Pesquisa coletiva não encontrado")
    
    # Deleta o integrante
    result = pesquisa_remove.deletar()
    
    # Invalida cache relacionado após remoção
    invalidate_cache("list_pesquisas")
    
    return result
