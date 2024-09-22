# app/dtos/responses/integranteResponse.py

from pydantic import BaseModel
from typing import Optional

class MinicursosResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    titulo: str
    descricao: str
    imagem: str
    ativo: bool

