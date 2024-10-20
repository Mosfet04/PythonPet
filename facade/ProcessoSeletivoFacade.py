from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Utils.Util import Util
from dtos.requests.ProcessoSeletivo.CreateProcessoSeletivoRequest import CreateProcessoSeletivoRequest
from controllers.ProcessoSeletivoController import create_processoSeletivo, list_processoSeletivo, remove_processoSeletivo

processoSeletivo_bp = Blueprint("processo_seletivo", __name__)
documentacao = Util.read_yaml("facade/DocumentacaoFacade/ProcessoSeletivoFacade.yml")

@processoSeletivo_bp.route("/processo_seletivo", methods=["POST"])
@swag_from(documentacao.get('AddProcessoSeletivo'))
@Util.token_required
def add_processoSeletivo():
    """
    Cria um novo processo seletivo
    ---
    security:
      - Bearer: []
    """
    data = request.get_json()
    request_obj = CreateProcessoSeletivoRequest(**data)
    planejamentoRelatorio = create_processoSeletivo(request_obj)
    
    return jsonify(planejamentoRelatorio)

@processoSeletivo_bp.route("/processo_seletivo", methods=["GET"])
@swag_from(documentacao.get('GetProcessoSeletivo'))
def get_processoSeletivo():
    """
    Lista todos os processos seletivos
    """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    response = list_processoSeletivo(page, per_page)
    
    return jsonify(response)
      
@processoSeletivo_bp.route("/pprocesso_seletivo/<int:idDocumento>", methods=["DELETE"])
@swag_from(documentacao.get('DeleteProcessoSeletivo'))
@Util.token_required
def delete_processoSeletivo(idDocumento):
    """
    Remove um processo seletivo do banco de dados
    ---
    security:
      - Bearer: []
    """
    matricula = request.args.get("matricula", default=None, type=str)
    integrantes = remove_processoSeletivo(idDocumento, matricula)
    
    return jsonify(integrantes)