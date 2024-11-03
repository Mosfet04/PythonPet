# app/dtos/requests/createIntegranteRequest.py

from datetime import date
from pydantic import BaseModel


class CreateProcessoSeletivoRequest(BaseModel):
    """
    Objeto de request para inserção de um processo seletivo.
    """
    link: str
    titulo: str
    dataEdital: date
