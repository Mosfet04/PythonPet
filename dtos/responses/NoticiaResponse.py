# app/dtos/responses/integranteResponse.py

from pydantic import BaseModel

class NoticiaResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    titulo: str
    conteudo: str
    autor: str
    dataCriacao: str
    nomeSetorResponsavel: str 
    tituloCategoriaNoticia: str
