from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.requests.Noticias.UpdateNoticiaRequest import UpdateNoticiaRequest
from controllers.NoticiaController import create_noticia, listarNoticias, update_noticia, remove_noticia

documentacao = Util.read_yaml("facade/DocumentacaoFacade/NoticiasFacade.yml")

noticias_bp = Blueprint("noticias", __name__)

@noticias_bp.route("/noticias", methods=["POST"])
@swag_from(documentacao.get('AddNoticia'))
@Util.token_required
def add_noticia():
    """
    Cria uma nova noticia
    ---
    security:
      - Bearer: []
    """
    data = request.get_json()
    request_obj = CreateNoticiaRequest(**data)
    noticia = create_noticia(request_obj)
    
    return jsonify(noticia)

@noticias_bp.route("/noticias", methods=["GET"])
@swag_from(documentacao.get('GetNoticias'))
def get_noticias():
    """
    Lista todas as noticias 
    """
    categoria = request.args.get('categoria')
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    noticias = listarNoticias(categoria, data_inicial, data_final, page, per_page)
    
    return jsonify(noticias)

@noticias_bp.route("/noticias/<int:idNoticia>", methods=["POST"])
@swag_from(documentacao.get('UpdateNoticia'))
@Util.token_required
def post_noticia(idNoticia):
      """
      Atualiza as informações de uma notícia
      ---
      security:
        - Bearer: []
      """
      data = request.get_json()
      request_obj = UpdateNoticiaRequest(**data)
      noticia = update_noticia(request_obj, idNoticia)
      
      return jsonify(noticia)

@noticias_bp.route("/noticias/<int:idNoticia>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteNoticia'))
@Util.token_required
def delete_noticia(idNoticia):
    """
      Remove do banco um integrante cadastrado
      ---
      security:
        - Bearer: []
    """
    matricula = request.args.get("matricula", default=None, type=str)
    noticia = remove_noticia(idNoticia, matricula)

    return jsonify(noticia)