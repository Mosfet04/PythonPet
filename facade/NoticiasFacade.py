from flask import Blueprint, request, jsonify
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from controllers.NoticiaController import create_noticia, list_noticias

noticias_bp = Blueprint("noticias", __name__)

@noticias_bp.route("/noticias", methods=["POST"])
def add_noticia():
    """
    Cria uma nova noticia
    ---
    tags:
      - Noticias
    parameters:
      - nome: body
        in: body
        required: true
        schema:
          id: CreateNoticiaRequest
          required:
            - nome
          properties:
            titulo:
              type: string
              description: Titulo da noticia
              example: "Noticia 1"
            conteudo:
              type: string
              description: Descrição da noticia
              example: "Descrição da noticia 1"
            matriculaAutor:
              type: string
              description: matricula do integrante responsavel por publicar a noticia
            idSetorResponsavel:
              type: string
              format: date
              description: A data de ingresso do integrante
            idCategoriaNoticia:
              type: string
              format: date
              description: A data de desligamento do integrante (pode ser nula)

    responses:
      200:
        description: Noticia criada com sucesso
        schema:
          id: NoticiaResponse
          properties:
            id:
              type: integer
              description: O ID da noticia
              example: 1
            titulo:
              type: string
              description: O titulo da noticia
              example: "Noticia 1"
            conteudo:
              type: string
              description: A descrição da noticia
              example: "Descrição da noticia 1"
            autor:
              type: string
              description: O nome do autor da noticia
              example: "Mateus Meireles Ribeiro"
            dataCriacao:
              type: datetime
              description: A data de criação da noticia
              example: "2021-01-01"
            nomeSetorResponsavel:
              type: string
              description: O nome do setor responsavel pela noticia
              example: "Setor 1"
            tituloCategoriaNoticia:
              type: string
              description: O titulo da categoria da noticia
              example: "Categoria 1"
    """
    data = request.get_json()
    request_obj = CreateNoticiaRequest(**data)
    integrante = create_noticia(request_obj)
    
    return jsonify(integrante)
#TODO: Implementar os filtros de categoria, data incial e data final para a noticia. Além disso o retorno deve ser de um objeto com parametros de paginação
@noticias_bp.route("/noticias", methods=["GET"])
def get_noticias():
    """
    Lista todas as noticias 
    ---
    tags:
      - Noticias
    responses:
      200:
        nome: Lista as noticias
        schema:
          type: array
          items:
            $ref: '#/definitions/IntegranteResponse'
    """
    noticias = list_noticias()
    
    return jsonify(noticias)

# @integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["POST"])
# def post_integrantes(idIntegrante):
#       """
#       Atualiza as informações de um integrante
#       ---
#       tags:
#         - Integrantes
#       parameters:
#         - nome: idIntegrante
#           in: path
#           required: true
#           type: integer
#           description: O ID do integrante
#           example: 1
#         - nome: body
#           in: body
#           required: true
#           schema:
#             id: UpdateIntegranteRequest
#             required:
#               - nome
#             properties:
#               nome:
#                 type: string
#                 description: O nome do integrante
#                 example: "Mateus Meireles Ribeiro"
#               matricula:
#                 type: string
#                 description: A matrícula do integrante
#               email:
#                 type: string
#                 description: O email do integrante
#               dataIngresso:
#                 type: string
#                 format: date
#                 description: A data de ingresso do integrante
#               desligamento:
#                 type: boolean
#                 format: bool
#                 description: Se o integrante deve ser desligado
#               linkSelfie:
#                 type: string
#                 description: O link da selfie do integrante
#       responses:
#         200:
#           description: Integrante atualizado com sucesso
#           schema:
#             id: IntegranteResponse
#             properties:
#               id:
#                 type: integer
#                 description: O ID do integrante
#                 example: 1
#               nome:
#                 type: string
#                 description: O nome do integrante
#                 example: "Mateus Meireles Ribeiro"
#               matricula:
#                 type: string
#                 description: A matrícula do integrante
#                 example: "2019000000"
#               email:
#                 type: string
#                 description: O email do integrante
#                 example: "mateus@teste.com"
#               dataIngresso:
#                 type: datetime
#                 description: A data de ingresso do integrante
#                 example: "2021-01-01"
#               dataDesligamento:
#                 type: datetime
#                 description: A data de desligamento do integrante (pode ser nula)
#                 example: "2021-01-01"
#       """
#       data = request.get_json()
#       request_obj = UpdateIntegranteRequest(**data)
#       integrante = update_integrante(request_obj, idIntegrante)
      
#       return jsonify(integrante)
# @integrantes_bp.route("/integrantes/<int:idIntegrante>", methods=["DELETE"])
# def delete_integrantes(idIntegrante):
#     """
#       Remove do banco um integrante cadastrado
#       ---
#       tags:
#         - Integrantes
#       parameters:
#         - nome: idIntegrante
#           in: path
#           required: true
#           type: integer
#           description: O ID do integrante
#           example: 1
#         - nome: matricula
#           in: query
#           required: true
#           type: string
#           description: A matrícula do integrante
#           example: 2019000000
#       responses:
#         200:
#           description: Integrante removido com sucesso
#           schema:
#             type: boolean
#             description: Retorna True se o integrante foi removido com sucesso
#     """
#     matricula = request.args.get("matricula", default=None, type=str)
#     integrantes = remove_integrante(idIntegrante, matricula)
    
#     return jsonify(integrantes)