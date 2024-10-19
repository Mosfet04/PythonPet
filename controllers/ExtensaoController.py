# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo
from dtos.requests.Extensao.CreateExtensaoRequest import CreateExtensaoRequest
from dtos.requests.Extensao.UpdateExtensaoRequest import UpdateExtensaoRequest
from dtos.responses.ExtensaoResponse import ExtensaoResponse
from models.ExtensaoModel import Extensao
from models.IntegranteModel import Integrante


def create_extensao(request: CreateExtensaoRequest) -> ExtensaoResponse:
    """
    Função para inserir uma extensão no banco de dados.
    """

    integrante = Integrante.encontrarIntegrante(request.matricula, None)
    if integrante == None:
        raise IntegrityError("Integrante já cadastrado")

    return Extensao.criarExtensao(request)


def list_extensao(ativo:bool, tipo : ExtensaoTipo) -> list[ExtensaoResponse]:
    """
    Função para listar todas as extensões do banco de dados.
    """
    response = Extensao.listarExtensao(1, 5, tipo, None, ativo)
    return response.to_dict()

def update_extensao(request: UpdateExtensaoRequest, matricula: str) -> ExtensaoResponse:
    """
    Função para atualizar os dados de uma extensão
    """
    integrante : Integrante = Integrante.encontrarIntegrante(matricula, None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado")
    
    extensao_update : Extensao = Extensao.listarExtensao(1, 1, None, request.id)

    if not extensao_update:
        raise IntegrityError("Extensao coletiva não encontrada")

    return extensao_update.atualizarExtensao(request)

def remove_extensao(idMinicurso: int, matricula: str) -> bool:
    """
    Função para deletar uma extensão.
    """
    integrante : Integrante = Integrante.encontrarIntegrante(matricula, None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique a matricula do integrante")

    extensao_remove : Extensao = Extensao.listarExtensao(False, 1, 1, idMinicurso)

    if not extensao_remove:
        raise IntegrityError("Extensao não encontrado")

    return extensao_remove.deletar()
