# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel

from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo

class CreateExtensaoRequest(BaseModel):
    """
    Objeto de request para criação.
    """
    nome: str
    descricao: str
    tipo: ExtensaoTipo
    ativo: bool
    matricula: str
