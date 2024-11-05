# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel


class UpdateMinicursosRequest(BaseModel):
    """
    Objeto de request para criaação de um novo integrante.
    """
    titulo: str
    descricao: str
    imagem: str
    ativo: bool
