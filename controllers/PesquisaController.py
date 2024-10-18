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

    integrante = Integrante.encontrarIntegrante(request.matricula, None)
    if integrante == None:
        raise IntegrityError("Integrante já cadastrado")

    # Cria um novo integrante no banco de dados
    return Pesquisa.criarPesquisa(request)


def list_pesquisas(ativo) -> list[PesquisaResponse]:
    """
    Função para listar todas as pesquisas coletivas do banco de dados.
    """
    response = Pesquisa.listarPesquisas(ativo)
    return response.to_dict()

def update_pesquisas(request: UpdatePesquisaRequest, matricula: str) -> PesquisaResponse:
    """
    Função para atualizar os dados de uma pesquisa coletiva
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula, None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado")
    
    pesquisa_update : Pesquisa = Pesquisa.listarPesquisas(False, 1, 1, request.id)

    if not pesquisa_update:
        raise IntegrityError("Pesquisa coletiva não encontrada")
    
    # Atualiza os dados do integrante
    return pesquisa_update.atualizarPesquisa(request)

def remove_pesquisa(idMinicurso: int, matricula: str) -> bool:
    """
    Função para deletar uma pesquisa coletiva.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula, None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique a matricula do integrante")

    pesquisa_remove : Pesquisa = Pesquisa.listarPesquisas(False, 1, 1, idMinicurso)

    if not pesquisa_remove:
        raise IntegrityError("Pesquisa coletiva não encontrado")
    
    # Deleta o integrante
    return pesquisa_remove.deletar()
