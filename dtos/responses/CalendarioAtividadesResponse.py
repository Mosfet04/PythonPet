# app/dtos/responses/integranteResponse.py

from datetime import date
from pydantic import BaseModel

class CalendarioAtividadesResponse(BaseModel):
    """
    Objeto de resposta para retornos de ações do backend
    """
    id: int
    titulo: str
    descricao: str
    dataInicio: date
    ativo: bool
    local: str

