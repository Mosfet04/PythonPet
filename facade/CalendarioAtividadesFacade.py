from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.CalendarioAtividades.CreateCalendarioAtividadesRequest import CreateCalendarioAtividadesRequest
from controllers.CalendarioAtividadesController import create_calendarioAtividades, list_calendarioAtividades, update_calendarioAtividades, remove_calendarioAtividades
from dtos.requests.CalendarioAtividades.UpdateCalendarioAtividadesRequest import UpdateCalendarioAtividadesRequest

documentacao = Util.read_yaml("facade/DocumentacaoFacade/CalendarioAtividadesFacade.yml")
calendarioAtividades_bp = Blueprint("calendario_atividades", __name__)

@calendarioAtividades_bp.route("/calendario_atividades", methods=["POST"])
@swag_from(documentacao.get('AddCalendarioAtividades'))
@Util.token_required
def add_calendarioAtividades():
    """
    Cria uma nova atividade no calendario
    ---
    security:
      - Bearer: []
    """
    data = request.get_json()
    request_obj = CreateCalendarioAtividadesRequest(**data)
    calendarioAtividades = create_calendarioAtividades(request_obj)
    
    return jsonify(calendarioAtividades)

@calendarioAtividades_bp.route("/calendario_atividades", methods=["GET"])
@swag_from(documentacao.get('GetCalendarioAtividades'))
def get_calendarioAtividadess():
    """
    Lista todas as atividades do calendario
    """
    ativo = request.args.get("ativo")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=3, type=int)
    if(ativo != None):
      ativo = Util.str_to_bool(ativo)
    calendarioAtividadess = list_calendarioAtividades(ativo, page, per_page)
    
    return jsonify(calendarioAtividadess)

@calendarioAtividades_bp.route("/calendario_atividades/<int:idAtividade>", methods=["POST"])
@swag_from(documentacao.get('UpdateCalendarioAtividades'))
@Util.token_required
def post_calendarioAtividadess(idAtividade):
      """
      Atualiza as informações de uma atividade do calendario
      ---
      security:
        - Bearer: []
      """
      data = request.get_json()
      request_obj = UpdateCalendarioAtividadesRequest(**data)
      calendarioAtividades = update_calendarioAtividades(request_obj, idAtividade)
      
      return jsonify(calendarioAtividades)

@calendarioAtividades_bp.route("/calendario_atividades/<int:idAtividade>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteCalendarioAtividades'))
@Util.token_required
def delete_calendarioAtividades(idAtividade):
    """
      Remove do banco uma atividade cadastrada no calendario
      ---
      security:
        - Bearer: []
    """
    calendarioAtividades = remove_calendarioAtividades(idAtividade)
    
    return jsonify(calendarioAtividades)