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
@Util.token_required
def add_extensao():
    """
    Cria um novo projeto de extensão
    ---
    security:
      - Bearer: []
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
    ativo = request.args.get("ativo")
    tipo = request.args.get("tipo")
    if (tipo != None):
      tipo = ExtensaoTipo(tipo)
    if (ativo != None):
      ativo = Util.str_to_bool(ativo)
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    extensao = list_extensao(ativo, tipo, page, per_page)
    
    return jsonify(extensao)

@extensao_bp.route("/extensao/<int:idConteudo>", methods=["POST"])
@swag_from(documentacao.get('UpdateExtensao'))
@Util.token_required
def post_extensao(idConteudo):
      """
      Atualiza as informações de uma extensão
      ---
      security:
        - Bearer: []
      """
      data = request.get_json()
      request_obj = UpdateExtensaoRequest(**data)
      extensao = update_extensao(request_obj, idConteudo)
      
      return jsonify(extensao)

@extensao_bp.route("/extensao/<int:idExtensao>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteExtensao'))
@Util.token_required
def delete_extensao(idExtensao):
    """
      Remove do banco uma extensao
      ---
      security:
        - Bearer: []
    """
    extensao = remove_extensao(idExtensao)
    
    return jsonify(extensao)