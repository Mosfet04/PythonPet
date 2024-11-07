# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel


class UpdateCalendarioAtividadesRequest(BaseModel):
    """
    Objeto de request para atualização das pesquisas coletivas.
    """
    titulo: str
    descricao: str
    ativo: bool
    dataInicio: str
    local: str
