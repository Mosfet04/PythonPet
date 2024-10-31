# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.Integrante.UpdateIntegranteRequest import UpdateIntegranteRequest
from models.IntegranteModel import Integrante
from dtos.requests.Integrante.CreateIntegranteRequest import CreateIntegranteRequest
from dtos.responses.IntegranteResponse import IntegranteResponse

def create_integrante(request: CreateIntegranteRequest) -> IntegranteResponse:
    """
    Função para inserir o integrante
    """
    # Verifica se o integrante já existe na base de dados
    integrante_duplicado = Integrante.encontrarIntegrante(request.matricula, None)
    if integrante_duplicado:
        raise IntegrityError("Integrante já cadastrado")

    # Cria um novo integrante no banco de dados
    return Integrante.criarIntegrante(request.nome, request.matricula, request.email, request.linkSelfie, request.setorId)


def list_integrantes(ativo, page, per_page) -> list[IntegranteResponse]:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    response = Integrante.listarIntegrantes(ativo, page, per_page)
    return response.to_dict()

def update_integrante(request: UpdateIntegranteRequest, idIntegrante: bool) -> IntegranteResponse:
    """
    Função para atualizar os dados de um integrante.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(None, idIntegrante)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado")

    # Atualiza os dados do integrante
    return integrante.atualizarIntegrante(request)

def remove_integrante(idIntegrante: int, matricula: str) -> bool:
    """
    Função para deletar um integrante.
    """
    # Deleta o integrante
    return integrante.deletarIntegrante()
