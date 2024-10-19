# app/dtos/requests/createIntegranteRequest.py

from pydantic import BaseModel

from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo


class UpdateExtensaoRequest(BaseModel):
    """
    Objeto de request para atualização das pesquisas coletivas.
    """
    id: int
    nome: str
    descricao: str
    tipo: ExtensaoTipo
    ativo: bool
    matricula: str
