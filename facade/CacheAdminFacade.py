"""
Facade para monitoramento e administração do cache da API.
Fornece endpoints para visualizar estatísticas e gerenciar o cache em memória.
"""

from flask import Blueprint, jsonify
from flasgger import swag_from
from servicos.cache_service import cache_service

cache_admin_bp = Blueprint("cache_admin", __name__)

@cache_admin_bp.route("/cache/stats", methods=["GET"])
def get_cache_stats():
    """
    Retorna estatísticas do cache atual
    ---
    tags:
      - Cache Admin
    responses:
      200:
        description: Estatísticas do cache
        schema:
          type: object
          properties:
            current_size:
              type: integer
              description: Número atual de entradas no cache
            max_size:
              type: integer
              description: Número máximo de entradas permitidas
            ttl_seconds:
              type: integer
              description: Tempo de vida padrão em segundos
            ttl_hours:
              type: number
              description: Tempo de vida padrão em horas
            sample_keys:
              type: array
              items:
                type: string
              description: Amostras de chaves no cache (primeiras 5)
    """
    stats = cache_service.get_stats()
    return jsonify({
        "status": "success",
        "data": stats,
        "message": "Estatísticas do cache recuperadas com sucesso"
    })

@cache_admin_bp.route("/cache/clear", methods=["POST"])
def clear_all_cache():
    """
    Limpa todo o cache
    ---
    tags:
      - Cache Admin
    responses:
      200:
        description: Cache limpo com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            message:
              type: string
              example: Cache limpo com sucesso
    """
    cache_service.clear_all()
    return jsonify({
        "status": "success",
        "message": "Cache limpo com sucesso"
    })

@cache_admin_bp.route("/cache/clear/<endpoint_name>", methods=["POST"])
def clear_endpoint_cache(endpoint_name: str):
    """
    Limpa cache de um endpoint específico
    ---
    tags:
      - Cache Admin
    parameters:
      - name: endpoint_name
        in: path
        type: string
        required: true
        description: Nome do endpoint para limpar o cache
    responses:
      200:
        description: Cache do endpoint limpo
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            entries_removed:
              type: integer
              description: Número de entradas removidas
            message:
              type: string
    """
    removed_count = cache_service.clear_endpoint_cache(endpoint_name)
    return jsonify({
        "status": "success",
        "entries_removed": removed_count,
        "message": f"Cache do endpoint '{endpoint_name}' limpo. {removed_count} entradas removidas."
    })
