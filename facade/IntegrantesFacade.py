from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.Integrante.UpdateIntegranteRequest import UpdateIntegranteRequest
from dtos.requests.Integrante.CreateIntegranteRequest import CreateIntegranteRequest
from controllers.IntegranteController import create_integrante, list_integrantes, update_integrante, remove_integrante

documentacao = Util.read_yaml("facade/DocumentacaoFacade/IntegrantesFacade.yml")
integrantes_bp = Blueprint("integrantes", __name__)

@integrantes_bp.route("/integrantes", methods=["POST"])
@swag_from(documentacao.get('AddIntegrante'))
def add_integrante():
    """
    Cria um novo integrante
    """
    data = request.get_json()
    request_obj = CreateIntegranteRequest(**data)
    integrante = create_integrante(request_obj)
    
    return jsonify(integrante)

@integrantes_bp.route("/integrantes", methods=["GET"])
@swag_from(documentacao.get('GetIntegrantes'))
def get_integrantes():
    """
    Lista todas os integrantes
    """
    ativo = request.args.get("ativo", default=False, type=bool)
    integrantes = list_integrantes(ativo)
    
    return jsonify(integrantes)

@integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["POST"])
@swag_from(documentacao.get('UpdateIntegrante'))
def post_integrantes(idIntegrante):
      """
      Atualiza as informações de um integrante
      """
      data = request.get_json()
      request_obj = UpdateIntegranteRequest(**data)
      integrante = update_integrante(request_obj, idIntegrante)
      
      return jsonify(integrante)
@integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteIntegrante'))
def delete_integrantes(idIntegrante):
    """
      Remove do banco um integrante cadastrado
    """
    matricula = request.args.get("matricula", default=None, type=str)
    integrantes = remove_integrante(idIntegrante, matricula)
    
    return jsonify(integrantes)