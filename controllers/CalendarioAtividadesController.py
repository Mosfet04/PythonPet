# app/controllers/taskController.py

from psycopg2 import IntegrityError
from dtos.requests.CalendarioAtividades.UpdateCalendarioAtividadesRequest import UpdateCalendarioAtividadesRequest
from models.IntegranteModel import Integrante
from models.CalendarioAtividadesModel import CalendarioAtividades
from dtos.requests.CalendarioAtividades.CreateCalendarioAtividadesRequest import CreateCalendarioAtividadesRequest
from dtos.responses.CalendarioAtividadesResponse import CalendarioAtividadesResponse

def create_calendarioAtividades(request: CreateCalendarioAtividadesRequest) -> CalendarioAtividadesResponse:
    """
    Função para inserir atividades no banco de dados.
    """
    return CalendarioAtividades.salvarCalendarioAtividades(request)


def list_calendarioAtividades(ativo, page, per_page) -> list[CalendarioAtividadesResponse]:
    """
    Função para listar todas as atividades do banco de dados.
    """
    response = CalendarioAtividades.listarAtividades(page, per_page, ativo)
    return response.to_dict()

def update_calendarioAtividades(request: UpdateCalendarioAtividadesRequest, idAtividade: int) -> CalendarioAtividadesResponse:
    """
    Função para atualizar os dados de uma atividade do calendario.
    """
    atividade_update : CalendarioAtividades = CalendarioAtividades.listarAtividades(1, 1, None, idAtividade)

    if not atividade_update:
        raise IntegrityError("Minicurso não encontrado")
    
    # Atualiza os dados do integrante
    return atividade_update.atualizarCalendarioAtividades(request)

def remove_calendarioAtividades(idAtividade: int) -> bool:
    """
    Função para deletar uma atividade do calendario.
    """
    atividade_remove :CalendarioAtividades = CalendarioAtividades.listarAtividades(1, 1, None, idAtividade)

    if not atividade_remove:
        raise IntegrityError("Minicurso não encontrado")
    
    # Deleta o integrante
    return atividade_remove.deletar()
