from flask import Blueprint, request, jsonify
from dtos.requests.Noticias.CreateNoticiaRequest import CreateNoticiaRequest
from dtos.requests.Noticias.UpdateNoticiaRequest import UpdateNoticiaRequest
from controllers.NoticiaController import create_noticia, listarNoticias, update_noticia, remove_noticia

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
    noticia = create_noticia(request_obj)
    
    return jsonify(noticia)

@noticias_bp.route("/noticias", methods=["GET"])
def get_noticias():
    """
    Lista todas as noticias 
    ---
    tags:
      - Noticias
    parameters:
      - name: categoria
        in: query
        type: string
        description: Categoria da noticia
      - name: data_inicial
        in: query
        type: string
        format: date
        description: Data inicial no formato YYYY-MM-DD
      - name: data_final
        in: query
        type: string
        format: date
        description: Data final no formato YYYY-MM-DD
      - name: page
        in: query
        type: integer
        description: Número da página
      - name: per_page
        in: query
        type: integer
        description: Itens por página
    responses:
      200:
        description: Lista as noticias
        schema:
          type: array
          items:
            $ref: '#/definitions/NoticiaResponse'
    """
    categoria = request.args.get('categoria')
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    noticias = listarNoticias(categoria, data_inicial, data_final, page, per_page)
    
    return jsonify(noticias)

@noticias_bp.route("/noticias/<int:idNoticia>", methods=["POST"])
def post_noticia(idNoticia):
      """
      Atualiza as informações de uma notícia
      ---
      tags:
        - Noticias
      parameters:
        - name: idNoticia
          in: path
          required: true
          type: integer
          description: O ID da notícia
          example: 1
        - name: body
          in: body
          required: true
          schema:
            id: UpdateNoticiaRequest
            required:
              - titulo
              - conteudo
              - idAtualizador
              - idCategoriaNoticia
            properties:
              titulo:
                type: string
                description: O título da notícia
                example: "Novo Projeto Anunciado"
              conteudo:
                type: string
                description: O conteúdo da notícia
                example: "Detalhes sobre o novo projeto..."
              idAtualizador:
                type: integer
                description: O ID do atualizador da notícia
                example: 2
              idCategoriaNoticia:
                type: integer
                description: O ID da categoria da notícia
                example: 3
      responses:
        200:
          description: Notícia atualizada com sucesso
          schema:
            id: NoticiaResponse
            properties:
              id:
                type: integer
                description: O ID da notícia
                example: 1
              titulo:
                type: string
                description: O título da notícia
                example: "Novo Projeto Anunciado"
              conteudo:
                type: string
                description: O conteúdo da notícia
                example: "Detalhes sobre o novo projeto..."
              autor:
                type: string
                description: O autor da notícia
                example: "João Silva"
              atualizador:
                type: string
                description: O atualizador da notícia (pode ser nulo)
                example: "Maria Souza"
              dataCriacao:
                type: string
                format: date-time
                description: A data de criação da notícia
                example: "2023-01-01T12:00:00Z"
              dataAtualizacao:
                type: string
                format: date-time
                description: A data de atualização da notícia (pode ser nula)
                example: "2023-01-02T12:00:00Z"
              nomeSetorResponsavel:
                type: string
                description: O nome do setor responsável pela notícia
                example: "Comunicação"
              tituloCategoriaNoticia:
                type: string
                description: O título da categoria da notícia
                example: "Projetos"
      """
      data = request.get_json()
      request_obj = UpdateNoticiaRequest(**data)
      noticia = update_noticia(request_obj, idNoticia)
      
      return jsonify(noticia)

@noticias_bp.route("/noticias/<int:idNoticia>", methods=["DELETE"])
def delete_noticia(idNoticia):
    """
      Remove do banco um integrante cadastrado
      ---
      tags:
        - Noticias
      parameters:
        - nome: idNoticia
          in: path
          required: true
          type: integer
          description: O ID da noticia
          example: 1
        - nome: matricula
          in: query
          required: true
          type: string
          description: A matrícula do integrante responsavel pela remoção
          example: 2019000000
      responses:
        200:
          description: Noticia removida com sucesso
          schema:
            type: boolean
            description: Retorna True se a noticia foi removida com sucesso
    """
    matricula = request.args.get("matricula", default=None, type=str)
    noticia = remove_noticia(idNoticia, matricula)

    return jsonify(noticia)