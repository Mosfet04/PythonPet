from datetime import date
from flask import Blueprint, request, jsonify
from dtos.requests.CreateIntegranteRequest import CreateIntegranteRequest
from controllers.IntegranteController import create_integrante, list_integrantes
from pydantic import BaseModel, Field

integrantes_bp = Blueprint("integrantes", __name__)

class CreateIntegranteRequest(BaseModel):
    nome: str = Field(..., nome="O nome do integrante")
    matricula: str = Field(..., matricula="Matricula do integrante")
    email: str = Field(..., email="O email do integrante")
    dataIngresso: date = Field(..., date="A data de Ingresso")  # Define a data de ingresso como a data atual
    dataDesligamento: date = Field(..., dataDesligamento="Data de desligamento do integrante")  # Deixa a data de desligamento como nula (None)
    linkSelfie: str = Field(..., linkSelfie="Link da selfie")
    setorId: int = Field(..., setorId = "Id do setor do integrante")

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