from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from Utils.Util import Util
from dtos.requests.Integrante.UpdateIntegranteRequest import UpdateIntegranteRequest
from dtos.requests.Integrante.CreateIntegranteRequest import CreateIntegranteRequest
from controllers.IntegranteController import create_integrante, list_integrantes, update_integrante, remove_integrante

documentacao = Util.read_yaml("facade/DocumentacaoFacade/IntegrantesFacade.yml")
integrantes_bp = Blueprint("integrantes", __name__)

@integrantes_bp.route("/integrantes", methods=["POST"])
@swag_from(documentacao.get('AddIntegrante'))
@Util.token_required
def add_integrante():
    """
    Cria um novo integrante
    ---
    security:
      - Bearer: []
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
    page = request.args.get("pagina", default=1, type=int)
    per_page = request.args.get("qtd_pagina", default=10, type=int)
    integrantes = list_integrantes(ativo, page, per_page)
    
    return jsonify(integrantes)

@integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["POST"])
@swag_from(documentacao.get('UpdateIntegrante'))
@Util.token_required
def post_integrantes(idIntegrante):
      """
      Atualiza as informações de um integrante
      ---
      security:
        - Bearer: []
      """
      data = request.get_json()
      request_obj = UpdateIntegranteRequest(**data)
      integrante = update_integrante(request_obj, idIntegrante)
      
      return jsonify(integrante)
@integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteIntegrante'))
@Util.token_required
def delete_integrantes(idIntegrante):
    """
      Remove do banco um integrante cadastrado
      ---
      security:
        - Bearer: []
    """
    integrantes = remove_integrante(idIntegrante)
    
    return jsonify(integrantes)