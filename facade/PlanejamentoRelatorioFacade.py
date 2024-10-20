from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.PlanejamentoRelatorio.CreatePlanejamentoRelatorioRequest import CreatePlanejamentoRelatorioRequest
from controllers.PlanejamentoRelatorioController import create_planejamentoRelatorio, list_planejamentoRelatorio, remove_planejamentoRelatorio

planejamentoRelatorio_bp = Blueprint("planejamento_relatorio", __name__)
documentacao = Util.read_yaml("facade/DocumentacaoFacade/PlanejamentoRelatorioFacade.yml")

@planejamentoRelatorio_bp.route("/planejamento_relatorio", methods=["POST"])
@swag_from(documentacao.get('AddPlanejamentoRelatorio'))
@Util.token_required
def add_planejamentoRelatorio():
    """
    Cria um novo planejamento ou relatório
    ---
    security:
      - Bearer: []
    """
    data = request.get_json()
    request_obj = CreatePlanejamentoRelatorioRequest(**data)
    planejamentoRelatorio = create_planejamentoRelatorio(request_obj)
    
    return jsonify(planejamentoRelatorio)

@planejamentoRelatorio_bp.route("/planejamento_relatorio", methods=["GET"])
@swag_from(documentacao.get('GetPlanejamentoRelatorio'))
def get_integrantes():
    """
    Lista todos os planejamentos e relatórios
    """
    response = list_planejamentoRelatorio()
    
    return jsonify(response)
      
@planejamentoRelatorio_bp.route("/planejamento_relatorio/<int:idDocumento>", methods=["DELETE"])
@swag_from(documentacao.get('DeletePlanejamentoRelatorio'))
@Util.token_required
def delete_integrantes(idDocumento):
    """
    Remove um planejamento ou relatório do banco de dados
    ---
    security:
      - Bearer: []
    """
    matricula = request.args.get("matricula", default=None, type=str)
    integrantes = remove_planejamentoRelatorio(idDocumento, matricula)
    
    return jsonify(integrantes)