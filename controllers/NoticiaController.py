# app/controllers/taskController.py

from psycopg2 import IntegrityError
from models.IntegranteModel import Integrante
from models.NoticiasModel import Noticia
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.responses.NoticiaResponse import NoticiaResponse
def create_noticia(request: CreateNoticiaRequest) -> NoticiaResponse:
    """
    Função para inserir o integrante
    """
    integrante = Integrante.encontrarIntegrante(request.matriculaAutor, None)
    if not integrante:
        raise IntegrityError("Possivel autor não encontrado")
    # Cria uma nova noticia no banco de dados
    return Noticia.criarNoticia(request, integrante.id)


def list_noticias() -> list[NoticiaResponse]:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    return Noticia.listarNoticias()

# def update_integrante(request: UpdateIntegranteRequest, idIntegrante: bool) -> IntegranteResponse:
#     """
#     Função para atualizar os dados de um integrante.
#     """
#     # Verifica se o integrante existe na base de dados
#     integrante : Integrante = Integrante.encontrarIntegrante(None, idIntegrante)
    
#     if not integrante:
#         raise IntegrityError("Integrante não encontrado")

#     # Atualiza os dados do integrante
#     return integrante.atualizarIntegrante(request)

# def remove_integrante(idIntegrante: int, matricula: str) -> bool:
#     """
#     Função para deletar um integrante.
#     """
#     # Verifica se o integrante existe na base de dados
#     integrante : Integrante = Integrante.encontrarIntegrante(None, idIntegrante)
    
#     if not integrante:
#         raise IntegrityError("Integrante não encontrado, verifique o ID do integrante")
#     if integrante.matricula != matricula:
#         raise IntegrityError("Matrícula inválida")

#     # Deleta o integrante
#     return integrante.deletarIntegrante()
