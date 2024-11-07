# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel
from datetime import date


class CreateIntegranteRequest(BaseModel):
    """
    Objeto de request para criação de um novo integrante.
    """
    nome: str
    matricula: str
    email: str
    dataIngresso: date  
    dataDesligamento: date
    linkSelfie: str
    linkedin: str
    setorId: int
