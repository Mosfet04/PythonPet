# app/dtos/requests/createIntegranteRequest.py

from datetime import date
from pydantic import BaseModel


class CreatePlanejamentoRelatorioRequest(BaseModel):
    """
    Objeto de request para criação de uma nova noticia.
    """
    link: str
    anoDocumento: date
    tipoDocumento:str
