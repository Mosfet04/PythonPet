# app/dtos/responses/integranteResponse.py

from datetime import date
from pydantic import BaseModel

class ProcessoSeletivoResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    link: str
    dataEdital: date
    titulo: str
