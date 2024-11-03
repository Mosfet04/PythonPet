# app/controllers/taskController.py

from typing import Optional
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
    return Extensao.criarExtensao(request)


def list_extensao(ativo:Optional[bool], tipo : Optional[ExtensaoTipo], page : Optional[int], per_page : Optional[int]) -> list[ExtensaoResponse]:
    """
    Função para listar todas as extensões do banco de dados.
    """
    response = Extensao.listarExtensao(page, per_page, tipo, None, ativo)
    return response.to_dict()

def update_extensao(request: UpdateExtensaoRequest, idConteudo: int) -> ExtensaoResponse:
    """
    Função para atualizar os dados de uma extensão
    """
    
    extensao_update : Extensao = Extensao.listarExtensao(1, 1, None, idConteudo)

    if not extensao_update:
        raise IntegrityError("Extensao coletiva não encontrada")

    return extensao_update.atualizarExtensao(request)

def remove_extensao(idMinicurso: int) -> bool:
    """
    Função para deletar uma extensão.
    """
    extensao_remove : Extensao = Extensao.listarExtensao(False, 1, 1, idMinicurso)

    if not extensao_remove:
        raise IntegrityError("Extensao não encontrado")

    return extensao_remove.deletar()
