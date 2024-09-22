# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel
from datetime import date


class CreateMinicursosRequest(BaseModel):
    """
    Objeto de request para criaação de um novo integrante.
    """
    titulo: str
    descricao: str
    imagem: str
    ativo: bool
    matricula: str
