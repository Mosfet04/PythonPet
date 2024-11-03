# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel


class UpdatePesquisaRequest(BaseModel):
    """
    Objeto de request para atualização das pesquisas coletivas.
    """
    nome: str
    descricao: str
    ativo: bool
