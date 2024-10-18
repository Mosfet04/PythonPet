# app/dtos/responses/integranteResponse.py

from pydantic import BaseModel
from typing import Optional

class PesquisaResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    nome: str
    descricao: str
    ativo: bool

