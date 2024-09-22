# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.MiniCurso.UpdateMinicursosRequest import UpdateMinicursosRequest
from models.IntegranteModel import Integrante
from models.MiniCursosModel import MiniCursos
from dtos.requests.MiniCurso.CreateMinicursosRequest import CreateMinicursosRequest
from dtos.responses.MinicursosResponse import MinicursosResponse

def create_minicurso(request: CreateMinicursosRequest) -> MinicursosResponse:
    """
    Função para inserir o mini-curso no banco de dados.
    """

    integrante = Integrante.encontrarIntegrante(request.matricula, None)
    if integrante == None:
        raise IntegrityError("Integrante já cadastrado")

    # Cria um novo integrante no banco de dados
    return MiniCursos.criarMinicurso(request)


def list_minicursos(ativo) -> list[MinicursosResponse]:
    """
    Função para listar todos os minicursos do banco de dados.
    """
    response = MiniCursos.listarMiniCursos(ativo)
    return response.to_dict()

def update_minicursos(request: UpdateMinicursosRequest, matricula: str) -> MinicursosResponse:
    """
    Função para atualizar os dados de um mini-curso.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula, None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado")
    
    minicurso_update : MiniCursos = MiniCursos.listarMiniCursos(False, 1, 1, request.id)

    if not minicurso_update:
        raise IntegrityError("Minicurso não encontrado")
    
    # Atualiza os dados do integrante
    return minicurso_update.atualizarMinicurso(request)

def remove_minicurso(idMinicurso: int, matricula: str) -> bool:
    """
    Função para deletar um mini-curso.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula, None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique a matricula do integrante")

    minicurso_remove :MiniCursos = MiniCursos.listarMiniCursos(False, 1, 1, idMinicurso)

    if not minicurso_remove:
        raise IntegrityError("Minicurso não encontrado")
    
    # Deleta o integrante
    return minicurso_remove.deletar()
