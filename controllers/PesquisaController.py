# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.Pesquisa.CreatePesquisaRequest import CreatePesquisaRequest
from dtos.requests.Pesquisa.UpdatePesquisaRequest import UpdatePesquisaRequest
from dtos.responses.PesquisaResponse import PesquisaResponse
from models.PesquisaModel import Pesquisa
from models.IntegranteModel import Integrante


def create_pesquisa(request: CreatePesquisaRequest) -> PesquisaResponse:
    """
    Função para inserir pesquisa coletiva no banco de dados.
    """

    # Cria um novo integrante no banco de dados
    return Pesquisa.criarPesquisa(request)


def list_pesquisas(ativo, page, per_page) -> list[PesquisaResponse]:
    """
    Função para listar todas as pesquisas coletivas do banco de dados.
    """
    response = Pesquisa.listarPesquisas(ativo, page, per_page)
    return response.to_dict()

def update_pesquisas(request: UpdatePesquisaRequest, idPesquisa: int) -> PesquisaResponse:
    """
    Função para atualizar os dados de uma pesquisa coletiva
    """
    
    pesquisa_update : Pesquisa = Pesquisa.listarPesquisas(None, 1, 1, idPesquisa)

    if not pesquisa_update:
        raise IntegrityError("Pesquisa coletiva não encontrada")
    
    # Atualiza os dados do integrante
    return pesquisa_update.atualizarPesquisa(request)

def remove_pesquisa(idMinicurso: int) -> bool:
    """
    Função para deletar uma pesquisa coletiva.
    """
    pesquisa_remove : Pesquisa = Pesquisa.listarPesquisas(None, 1, 1, idMinicurso)

    if not pesquisa_remove:
        raise IntegrityError("Pesquisa coletiva não encontrado")
    
    # Deleta o integrante
    return pesquisa_remove.deletar()
