from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.Pesquisa.CreatePesquisaRequest import CreatePesquisaRequest
from controllers.PesquisaController import create_pesquisa, list_pesquisas, update_pesquisas, remove_pesquisa
from dtos.requests.Pesquisa.UpdatePesquisaRequest import UpdatePesquisaRequest

documentacao = Util.read_yaml("facade/DocumentacaoFacade/PesquisaFacade.yml")
pesquisa_bp = Blueprint("pesquisa", __name__)

@pesquisa_bp.route("/pesquisa", methods=["POST"])
@swag_from(documentacao.get('AddPesquisa'))
@Util.token_required
def add_pesquisa():
    """
    Cria uma nova pesquisa coletiva
    ---
    security:
      - Bearer: []
    """
    data = request.get_json()
    request_obj = CreatePesquisaRequest(**data)
    pesquisa = create_pesquisa(request_obj)
    
    return jsonify(pesquisa)

@pesquisa_bp.route("/pesquisa", methods=["GET"])
@swag_from(documentacao.get('GetPesquisa'))
def get_minicursos():
    """
    Lista todas as pesquisas coletivas
    """
    ativo = request.args.get("ativo")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    if(ativo != None):
      ativo = Util.str_to_bool(ativo)
    pesquisa = list_pesquisas(ativo, page, per_page)
    
    return jsonify(pesquisa)

@pesquisa_bp.route("/pesquisa/<int:idPesquisa>", methods=["POST"])
@swag_from(documentacao.get('UpdatePesquisa'))
@Util.token_required
def post_minicursos(idPesquisa):
      """
      Atualiza as informações de uma pesquisa coletiva
      ---
        security:
            - Bearer: []
      """
      data = request.get_json()
      data["ativo"] = Util.str_to_bool(data["ativo"])
      request_obj = UpdatePesquisaRequest(**data)
      pesquisa = update_pesquisas(request_obj, idPesquisa)
      
      return jsonify(pesquisa)

@pesquisa_bp.route("/pesquisa/<int:idPesquisa>", methods=["DELETE"])
@swag_from(documentacao.get('DeletePesquisa'))
@Util.token_required
def delete_minicurso(idPesquisa):
    """
      Remove do banco um mini-curso cadastrado
      ---
      security:
        - Bearer: []
    """
    pesquisa = remove_pesquisa(idPesquisa)
    
    return jsonify(pesquisa)