# app/dtos/requests/createIntegranteRequest.py

from typing import Optional
from pydantic import BaseModel

class CreateCalendarioAtividadesRequest(BaseModel):
    """
    Objeto de request para criaação de um novo integrante.
    """
    titulo: str
    descricao: str
    ativo: bool
    dataInicio: str
    local: str
