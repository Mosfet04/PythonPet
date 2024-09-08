from flask import Blueprint, request, jsonify
from dtos.requests.UpdateIntegranteRequest import UpdateIntegranteRequest
from dtos.requests.CreateIntegranteRequest import CreateIntegranteRequest
from controllers.IntegranteController import create_integrante, list_integrantes, update_integrante, remove_integrante

integrantes_bp = Blueprint("integrantes", __name__)

@integrantes_bp.route("/integrantes", methods=["POST"])
def add_integrante():
    """
    Cria um novo integrante
    ---
    tags:
      - Integrantes
    parameters:
      - nome: body
        in: body
        required: true
        schema:
          id: CreateIntegranteRequest
          required:
            - nome
          properties:
            nome:
              type: string
              description: O nome do integrante
              example: "Mateus Meireles Ribeiro"
            matricula:
              type: string
              description: A matrícula do integrante
            email:
              type: string
              description: O email do integrante
            dataIngresso:
              type: string
              format: date
              description: A data de ingresso do integrante
            dataDesligamento:
              type: string
              format: date
              description: A data de desligamento do integrante (pode ser nula)
            linkSelfie:
              type: string
              description: O link da selfie do integrante
    responses:
      200:
        description: Integrante criado com sucesso
        schema:
          id: IntegranteResponse
          properties:
            id:
              type: integer
              description: O ID do integrante
              example: 1
            nome:
              type: string
              description: O nome do integrante
              example: "Mateus Meireles Ribeiro"
            matricula:
              type: string
              description: A matrícula do integrante
              example: "2019000000"
            email:
              type: string
              description: O email do integrante
              example: "mateus@teste.com"
            dataIngresso:
              type: datetime
              description: A data de ingresso do integrante
              example: "2021-01-01"
            dataDesligamento:
              type: datetime
              description: A data de desligamento do integrante (pode ser nula)
              example: "2021-01-01"
    """
    data = request.get_json()
    request_obj = CreateIntegranteRequest(**data)
    integrante = create_integrante(request_obj)
    
    return jsonify(integrante)

@integrantes_bp.route("/integrantes", methods=["GET"])
def get_integrantes():
    """
    Lista todas os integrantes
    ---
    tags:
      - Integrantes
    responses:
      200:
        nome: Lista os integrantes
        schema:
          type: array
          items:
            $ref: '#/definitions/IntegranteResponse'
    """
    ativo = request.args.get("ativo", default=False, type=bool)
    integrantes = list_integrantes(ativo)
    
    return jsonify(integrantes)

@integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["POST"])
def post_integrantes(idIntegrante):
      """
      Atualiza as informações de um integrante
      ---
      tags:
        - Integrantes
      parameters:
        - nome: idIntegrante
          in: path
          required: true
          type: integer
          description: O ID do integrante
          example: 1
        - nome: body
          in: body
          required: true
          schema:
            id: UpdateIntegranteRequest
            required:
              - nome
            properties:
              nome:
                type: string
                description: O nome do integrante
                example: "Mateus Meireles Ribeiro"
              matricula:
                type: string
                description: A matrícula do integrante
              email:
                type: string
                description: O email do integrante
              dataIngresso:
                type: string
                format: date
                description: A data de ingresso do integrante
              desligamento:
                type: boolean
                format: bool
                description: Se o integrante deve ser desligado
              linkSelfie:
                type: string
                description: O link da selfie do integrante
      responses:
        200:
          description: Integrante atualizado com sucesso
          schema:
            id: IntegranteResponse
            properties:
              id:
                type: integer
                description: O ID do integrante
                example: 1
              nome:
                type: string
                description: O nome do integrante
                example: "Mateus Meireles Ribeiro"
              matricula:
                type: string
                description: A matrícula do integrante
                example: "2019000000"
              email:
                type: string
                description: O email do integrante
                example: "mateus@teste.com"
              dataIngresso:
                type: datetime
                description: A data de ingresso do integrante
                example: "2021-01-01"
              dataDesligamento:
                type: datetime
                description: A data de desligamento do integrante (pode ser nula)
                example: "2021-01-01"
      """
      data = request.get_json()
      request_obj = UpdateIntegranteRequest(**data)
      integrante = update_integrante(request_obj, idIntegrante)
      
      return jsonify(integrante)
@integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["DELETE"])
def delete_integrantes(idIntegrante):
    """
      Remove do banco um integrante cadastrado
      ---
      tags:
        - Integrantes
      parameters:
        - nome: idIntegrante
          in: path
          required: true
          type: integer
          description: O ID do integrante
          example: 1
        - nome: matricula
          in: query
          required: true
          type: string
          description: A matrícula do integrante
          example: 2019000000
      responses:
        200:
          description: Integrante removido com sucesso
          schema:
            type: boolean
            description: Retorna True se o integrante foi removido com sucesso
    """
    matricula = request.args.get("matricula", default=None, type=str)
    integrantes = remove_integrante(idIntegrante, matricula)
    
    return jsonify(integrantes)