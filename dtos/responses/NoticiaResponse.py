# app/dtos/responses/integranteResponse.py

from typing import Optional
from pydantic import BaseModel

class NoticiaResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    titulo: str
    conteudo: str
    autor: str
    atualizador: Optional[str]
    dataCriacao: str
    dataAtualizacao: Optional[str]
    nomeSetorResponsavel: str 
    tituloCategoriaNoticia: str
