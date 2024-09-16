from flask import Blueprint, request, jsonify
from dtos.requests.PlanejamentoRelatorio.CreatePlanejamentoRelatorioRequest import CreatePlanejamentoRelatorioRequest
from controllers.PlanejamentoRelatorioController import create_planejamentoRelatorio, list_planejamentoRelatorio, remove_planejamentoRelatorio

planejamentoRelatorio_bp = Blueprint("planejamento_relatorio", __name__)

@planejamentoRelatorio_bp.route("/planejamento_relatorio", methods=["POST"])
def add_planejamentoRelatorio():
    """
    Cria um novo planejamento ou relatório
    ---
    tags:
      - PlanejamentoRelatorio
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreatePlanejamentoRelatorioRequest
          required:
            - link
            - anoDocumento
            - tipoDocumento
          properties:
            link:
              type: string
              description: O link do documento
              example: "http://example.com/documento.pdf"
            anoDocumento:
              type: string
              description: O ano do documento
              example: "2023"
            tipoDocumento:
              type: string
              description: O tipo do documento (planejamento ou relatorio)
              example: "planejamento"
    responses:
      200:
        description: Planejamento ou Relatório criado com sucesso
        schema:
          id: PlanejamentoRelatorioResponse
          properties:
            id:
              type: integer
              description: O ID do documento
              example: 1
            link:
              type: string
              description: O link do documento
              example: "http://example.com/documento.pdf"
            anoDocumento:
              type: string
              description: O ano do documento
              example: "2023"
            tipo:
              type: string
              description: O tipo do documento (planejamento ou relatorio)
              example: "planejamento"
    """
    data = request.get_json()
    request_obj = CreatePlanejamentoRelatorioRequest(**data)
    planejamentoRelatorio = create_planejamentoRelatorio(request_obj)
    
    return jsonify(planejamentoRelatorio)

@planejamentoRelatorio_bp.route("/planejamento_relatorio", methods=["GET"])
def get_integrantes():
    """
    Lista todos os planejamentos e relatórios
    ---
    tags:
      - PlanejamentoRelatorio
    responses:
      200:
        description: Lista de planejamentos e relatórios
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                $ref: '#/definitions/PlanejamentoRelatorioResponse'
            hasNextPage:
              type: boolean
              description: Indica se há mais páginas
              example: true
            page:
              type: integer
              description: Página atual
              example: 1
            totalPage:
              type: integer
              description: Total de páginas
              example: 10
            qtdItens:
              type: integer
              description: Quantidade total de itens
              example: 100
    """
    response = list_planejamentoRelatorio()
    
    return jsonify(response)
      
@planejamentoRelatorio_bp.route("/planejamento_relatorio/<int:idDocumento>", methods=["DELETE"])
def delete_integrantes(idDocumento):
    """
    Remove um planejamento ou relatório do banco de dados
    ---
    tags:
      - PlanejamentoRelatorio
    parameters:
      - name: idDocumento
        in: path
        required: true
        type: integer
        description: O ID do documento
        example: 1
      - name: matricula
        in: query
        required: true
        type: string
        description: A matrícula do integrante
        example: 2019000000
    responses:
      200:
        description: Documento removido com sucesso
        schema:
          type: boolean
          description: Retorna True se o documento foi removido com sucesso
          example: true
    """
    matricula = request.args.get("matricula", default=None, type=str)
    integrantes = remove_planejamentoRelatorio(idDocumento, matricula)
    
    return jsonify(integrantes)