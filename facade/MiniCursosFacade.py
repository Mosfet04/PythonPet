from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.MiniCurso.CreateMinicursosRequest import CreateMinicursosRequest
from controllers.MiniCursosController import create_minicurso, list_minicursos, update_minicursos, remove_minicurso
from dtos.requests.MiniCurso.UpdateMinicursosRequest import UpdateMinicursosRequest

documentacao = Util.read_yaml("facade/DocumentacaoFacade/MiniCursosFacade.yml")
minicursos_bp = Blueprint("mini_cursos", __name__)

@minicursos_bp.route("/mini_cursos", methods=["POST"])
@swag_from(documentacao.get('AddMinicurso'))
@Util.token_required
def add_minicurso():
    """
    Cria um novo mini-curso
    ---
    security:
      - Bearer: []
    """
    data = request.get_json()
    request_obj = CreateMinicursosRequest(**data)
    minicurso = create_minicurso(request_obj)
    
    return jsonify(minicurso)

@minicursos_bp.route("/mini_cursos", methods=["GET"])
@swag_from(documentacao.get('GetMinicursos'))
def get_minicursos():
    """
    Lista todos os mini-cursos
    """
    ativo = request.args.get("ativo", default=False, type=bool)
    minicursos = list_minicursos(ativo)
    
    return jsonify(minicursos)

@minicursos_bp.route("/mini_cursos/<string:matricula>", methods=["POST"])
@swag_from(documentacao.get('UpdateMinicurso'))
@Util.token_required
def post_minicursos(matricula):
      """
      Atualiza as informações de um mini-curso
      ---
      security:
        - Bearer: []
      """
      data = request.get_json()
      request_obj = UpdateMinicursosRequest(**data)
      minicurso = update_minicursos(request_obj, matricula)
      
      return jsonify(minicurso)

@minicursos_bp.route("/mini-cursos/<int:idMinicurso>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteMinicurso'))
@Util.token_required
def delete_minicurso(idMinicurso):
    """
      Remove do banco um mini-curso cadastrado
      ---
      security:
        - Bearer: []
    """
    matricula = request.args.get("matricula", default=None, type=str)
    minicurso = remove_minicurso(idMinicurso, matricula)
    
    return jsonify(minicurso)