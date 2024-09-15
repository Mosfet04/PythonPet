# app/controllers/taskController.py

from typing import Optional
from psycopg2 import IntegrityError
from dtos.responses import PaginacaoResponse
from models.IntegranteModel import Integrante
from models.NoticiasModel import Noticia
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.requests.Noticias.UpdateNoticiaRequest import UpdateNoticiaRequest
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


def listarNoticias(categoria: Optional[str] = None, data_inicial: Optional[str] = None, data_final: Optional[str] = None, page: int = 1, per_page: int = 10) -> dict:
    """
    Função para listar todos os integrantes do banco de dados.
    """
    response : PaginacaoResponse[NoticiaResponse] = Noticia.listarNoticias(categoria, data_inicial, data_final, page, per_page)
    return response.to_dict()

def update_noticia(request: UpdateNoticiaRequest, idNoticia: bool) -> NoticiaResponse:
    """
    Função para atualizar os dados de uma noticia.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(None, request.idAtualizador)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado")
    
    noticia : Noticia = Noticia.listarNoticias(None, None, None, 1, 1, idNoticia, True)

    if not noticia:
        raise IntegrityError("Notícia não encontrada")

    
    return noticia.atualizar(request)

def remove_noticia(idNoticia: int, matricula: str) -> bool:
    """
    Função para deletar uma noticia.
    """
    # Verifica se o integrante existe na base de dados
    integrante : Integrante = Integrante.encontrarIntegrante(matricula,None)
    
    if not integrante:
        raise IntegrityError("Integrante não encontrado, verifique o ID do integrante")
    
    noticia : Noticia = Noticia.listarNoticias(None, None, None, 1, 1, idNoticia, True)

    if not noticia:
        raise IntegrityError("Notícia não encontrada")
    # Deleta o integrante
    return noticia.deletar()
