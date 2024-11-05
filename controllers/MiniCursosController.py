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
    # Cria um novo integrante no banco de dados
    return MiniCursos.criarMinicurso(request)


def list_minicursos(ativo, page, per_page) -> list[MinicursosResponse]:
    """
    Função para listar todos os minicursos do banco de dados.
    """
    response = MiniCursos.listarMiniCursos(ativo, page, per_page)
    return response.to_dict()

def update_minicursos(request: UpdateMinicursosRequest, idConteudo: int) -> MinicursosResponse:
    """
    Função para atualizar os dados de um mini-curso.
    """
    minicurso_update : MiniCursos = MiniCursos.listarMiniCursos(None, 1, 1, idConteudo)

    if not minicurso_update:
        raise IntegrityError("Minicurso não encontrado")
    
    # Atualiza os dados do integrante
    return minicurso_update.atualizarMinicurso(request)

def remove_minicurso(idMinicurso: int) -> bool:
    """
    Função para deletar um mini-curso.
    """
    minicurso_remove :MiniCursos = MiniCursos.listarMiniCursos(None, 1, 1, idMinicurso)

    if not minicurso_remove:
        raise IntegrityError("Minicurso não encontrado")
    
    # Deleta o integrante
    return minicurso_remove.deletar()
