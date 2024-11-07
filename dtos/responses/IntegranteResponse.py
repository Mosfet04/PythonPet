# app/dtos/responses/integranteResponse.py

from pydantic import BaseModel
from typing import Optional

class IntegranteResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    nome: str
    matricula: str
    email: str
    dataIngresso: str
    dataDesligamento: Optional[str] 
    linkSelfie: str
    linkedin: str
    setorNome: str
