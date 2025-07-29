from flask import Blueprint, jsonify
from flasgger import swag_from
from controllers.HealthController import (
    get_basic_health,
    get_detailed_health,
    get_readiness,
    get_liveness
)

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def basic_health():
    """
    Endpoint básico de health check
    ---
    tags:
      - Health
    summary: Verifica a saúde básica da aplicação
    description: |
      Retorna o status básico da aplicação.
      Este endpoint é útil para verificações rápidas de saúde.
    responses:
      200:
        description: Status da aplicação
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
              description: Status da aplicação (healthy/unhealthy)
            timestamp:
              type: string
              format: date-time
              example: "2024-01-01T12:00:00.000Z"
              description: Timestamp da verificação
            service:
              type: string
              example: "PythonPet API"
              description: Nome do serviço
            version:
              type: string
              example: "1.0.0"
              description: Versão da aplicação
            error:
              type: string
              description: Mensagem de erro (apenas quando status é unhealthy)
    """
    result = get_basic_health()
    status_code = 200 if result["status"] == "healthy" else 503
    return jsonify(result), status_code

@health_bp.route("/health/detailed", methods=["GET"])
def detailed_health():
    """
    Endpoint detalhado de health check
    ---
    tags:
      - Health
    summary: Verifica a saúde detalhada da aplicação
    description: |
      Retorna o status detalhado da aplicação, incluindo verificações
      de dependências como banco de dados, cache e recursos do sistema.
    responses:
      200:
        description: Status detalhado da aplicação
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
              description: Status geral da aplicação
            timestamp:
              type: string
              format: date-time
              description: Timestamp da verificação
            service:
              type: string
              example: "PythonPet API"
              description: Nome do serviço
            version:
              type: string
              example: "1.0.0"
              description: Versão da aplicação
            checks:
              type: object
              properties:
                database:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "healthy"
                    response_time_ms:
                      type: number
                      example: 25.5
                    details:
                      type: string
                      example: "Database connection successful"
                cache:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "healthy"
                    details:
                      type: string
                      example: "Cache service is working properly"
                system:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "healthy"
                    cpu_usage_percent:
                      type: number
                      example: 15.2
                    memory_usage_percent:
                      type: number
                      example: 45.8
                    disk_usage_percent:
                      type: number
                      example: 35.1
      503:
        description: Aplicação não saudável
    """
    result = get_detailed_health()
    status_code = 200 if result["status"] == "healthy" else 503
    return jsonify(result), status_code

@health_bp.route("/health/ready", methods=["GET"])
def readiness():
    """
    Endpoint de readiness check
    ---
    tags:
      - Health
    summary: Verifica se a aplicação está pronta para receber tráfego
    description: |
      Verifica se a aplicação está pronta para receber e processar requisições.
      Este endpoint é útil para load balancers e sistemas de orquestração
      determinarem quando rotear tráfego para a instância.
    responses:
      200:
        description: Aplicação pronta para receber tráfego
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ready"
              description: Status de prontidão (ready/not_ready)
            timestamp:
              type: string
              format: date-time
              description: Timestamp da verificação
            details:
              type: string
              example: "Application is ready to serve traffic"
              description: Detalhes do status de prontidão
      503:
        description: Aplicação não está pronta
        schema:
          type: object
          properties:
            status:
              type: string
              example: "not_ready"
            timestamp:
              type: string
              format: date-time
            details:
              type: string
              example: "Database is not available"
            database_status:
              type: object
              description: Status detalhado do banco de dados
    """
    result = get_readiness()
    status_code = 200 if result["status"] == "ready" else 503
    return jsonify(result), status_code

@health_bp.route("/health/live", methods=["GET"])
def liveness():
    """
    Endpoint de liveness check
    ---
    tags:
      - Health
    summary: Verifica se a aplicação está viva (não travada)
    description: |
      Verifica se a aplicação está viva e respondendo.
      Este endpoint é útil para sistemas de orquestração determinarem
      se precisam reiniciar a instância da aplicação.
    responses:
      200:
        description: Aplicação está viva
        schema:
          type: object
          properties:
            status:
              type: string
              example: "alive"
              description: Status de vida (alive/dead)
            timestamp:
              type: string
              format: date-time
              description: Timestamp da verificação
            response_time_ms:
              type: number
              example: 1.5
              description: Tempo de resposta em milissegundos
            details:
              type: string
              example: "Application is alive and responding"
              description: Detalhes do status
      503:
        description: Aplicação não está respondendo
        schema:
          type: object
          properties:
            status:
              type: string
              example: "dead"
            timestamp:
              type: string
              format: date-time
            error:
              type: string
              description: Mensagem de erro
            details:
              type: string
              example: "Liveness check failed"
    """
    result = get_liveness()
    status_code = 200 if result["status"] == "alive" else 503
    return jsonify(result), status_code
