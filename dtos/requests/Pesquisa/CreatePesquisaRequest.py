# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel

class CreatePesquisaRequest(BaseModel):
    """
    Objeto de request para criaação de um novo integrante.
    """
    nome: str
    descricao: str
    ativo: bool
    matricula: str
