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
def add_pesquisa():
    """
    Cria uma nova pesquisa coletiva
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
    ativo = request.args.get("ativo", type=str)
    ativo_bool = Util.str_to_bool(ativo)
    pesquisa = list_pesquisas(ativo_bool)
    
    return jsonify(pesquisa)

@pesquisa_bp.route("/pesquisa/<string:matricula>", methods=["POST"])
@swag_from(documentacao.get('UpdatePesquisa'))
def post_minicursos(matricula):
      """
      Atualiza as informações de uma pesquisa coletiva
      """
      data = request.get_json()
      request_obj = UpdatePesquisaRequest(**data)
      pesquisa = update_pesquisas(request_obj, matricula)
      
      return jsonify(pesquisa)

@pesquisa_bp.route("/pesquisa/<int:idPesquisa>", methods=["DELETE"])
@swag_from(documentacao.get('DeletePesquisa'))
def delete_minicurso(idPesquisa):
    """
      Remove do banco um mini-curso cadastrado
    """
    matricula = request.args.get("matricula", default=None, type=str)
    pesquisa = remove_pesquisa(idPesquisa, matricula)
    
    return jsonify(pesquisa)