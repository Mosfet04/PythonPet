# app/dtos/responses/integranteResponse.py

from pydantic import BaseModel
from typing import Optional

from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo

class ExtensaoResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    nome: str
    tipo: int
    descricao: str
    ativo: bool