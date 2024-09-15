# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel
from datetime import date


class UpdateNoticiaRequest(BaseModel):
    """
    Objeto de request para atualização de uma nova noticia.
    """
    titulo: str
    conteudo: str
    idAtualizador: int  
    idCategoriaNoticia: int
