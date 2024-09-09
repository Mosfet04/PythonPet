# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel
from datetime import date


class CreateNoticiaRequest(BaseModel):
    """
    Objeto de request para criação de uma nova noticia.
    """
    titulo: str
    conteudo: str
    dataCriacao: date = date.today()
    matriculaAutor: str  # Define a data de ingresso como a data atual
    idSetorResponsavel: int
    idCategoriaNoticia: int
