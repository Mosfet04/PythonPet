# app/dtos/requests/UpdateIntegranteRequest.py

from pydantic import BaseModel
from datetime import date


class UpdateIntegranteRequest(BaseModel):
    """
    Objeto de request para atualização de dados de um integrante.
    """
    nome: str
    matricula: str
    email: str
    dataIngresso: date  # Define a data de ingresso como a data atual
    desligamento: bool = False  # Deixa a data de desligamento como nula (None)
    linkSelfie: str
    linkedin: str
    setorId: int
