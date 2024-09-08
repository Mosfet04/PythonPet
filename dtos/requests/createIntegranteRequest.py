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
    dataIngresso: date = date.today()  # Define a data de ingresso como a data atual
    dataDesligamento: date = None  # Deixa a data de desligamento como nula (None)
    linkSelfie: str
    setorId: int
