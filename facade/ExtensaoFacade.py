from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.enums.ExtensaoTipoEnum import ExtensaoTipo
from dtos.requests.Extensao.CreateExtensaoRequest import CreateExtensaoRequest
from controllers.ExtensaoController import create_extensao, list_extensao, update_extensao, remove_extensao
from dtos.requests.Extensao.UpdateExtensaoRequest import UpdateExtensaoRequest

documentacao = Util.read_yaml("facade/DocumentacaoFacade/ExtensaoFacade.yml")
extensao_bp = Blueprint("extensao", __name__)

@extensao_bp.route("/extensao", methods=["POST"])
@swag_from(documentacao.get('AddExtensao'))
def add_extensao():
    """
    Cria um novo projeto de extensão
    """
    data = request.get_json()
    request_obj = CreateExtensaoRequest(**data)
    extensao = create_extensao(request_obj)
    
    return jsonify(extensao)

@extensao_bp.route("/extensao", methods=["GET"])
@swag_from(documentacao.get('GetExtensao'))
def get_extensao():
    """
    Lista as extensões
    """
    ativo = request.args.get("ativo", type=str)
    tipo = ExtensaoTipo(request.args.get("tipo", type=int))
    ativo_bool = Util.str_to_bool(ativo)
    extensao = list_extensao(ativo_bool, tipo)
    
    return jsonify(extensao)

@extensao_bp.route("/extensao/<string:matricula>", methods=["POST"])
@swag_from(documentacao.get('UpdateExtensao'))
def post_extensao(matricula):
      """
      Atualiza as informações de uma extensão
      """
      data = request.get_json()
      request_obj = UpdateExtensaoRequest(**data)
      extensao = update_extensao(request_obj, matricula)
      
      return jsonify(extensao)

@extensao_bp.route("/extensao/<int:idExtensao>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteExtensao'))
def delete_extensao(idExtensao):
    """
      Remove do banco uma extensao
    """
    matricula = request.args.get("matricula", default=None, type=str)
    extensao = remove_extensao(idExtensao, matricula)
    
    return jsonify(extensao)