# app/controllers/taskController.py

from datetime import date
from psycopg2 import IntegrityError
from models.integranteModel import Integrante
from dtos.requests.createIntegranteRequest import CreateIntegranteRequest
from dtos.responses.integranteResponse import IntegranteResponse

def create_integrante(request: CreateIntegranteRequest) -> IntegranteResponse:
    """
    Função para inserir o integrante
    """
    # Verifica se o integrante já existe na base de dados
    integrante_duplicado = Integrante.encontrarIntegrante(request.matricula)
    if integrante_duplicado:
        raise IntegrityError("Integrante já cadastrado")

    # Cria um novo integrante no banco de dados
    return Integrante.criarIntegrante(request.nome, request.matricula, request.email, request.linkSelfie, request.setorId)


def list_integrantes(ativo) -> list[IntegranteResponse]:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    return Integrante.listarIntegrantes(ativo)
