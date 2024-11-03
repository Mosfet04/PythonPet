# app/dtos/requests/createIntegranteRequest.py

from typing import Optional
from pydantic import BaseModel

class CreatePesquisaRequest(BaseModel):
    """
    Objeto de request para criaação de um novo integrante.
    """
    nome: str
    descricao: str
    ativo: Optional[bool]
