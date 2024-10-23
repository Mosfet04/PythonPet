from functools import wraps
from flask import jsonify, request
import yaml
from pydantic import BaseModel

from servicos.microsoftGraph import MicrosoftGraph

class Util():
    # Constantes para mensagens de erro
    TOKEN_MISSING = {'message': 'Token is missing!'}
    TOKEN_INVALID = {'message': 'Token is missing or invalid!'}
    TOKEN_ERROR = 'Token is invalid! Error: {}'
    DOMAIN = "AVLMascaras.onmicrosoft.com"

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    @staticmethod
    def str_to_bool(value: str) -> bool:
        if isinstance(value, str):
            return value.lower() in ("true", "1")
        return bool(value)

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Verifica se o cabeçalho Authorization está presente
            if 'Authorization' not in request.headers:
                return jsonify(Util.TOKEN_MISSING), 401

            # Divide o token em partes e verifica se está no formato correto
            parts = request.headers['Authorization'].split(" ")
            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify(Util.TOKEN_INVALID), 401

            try:
                token = request.headers['Authorization']
                response, status_code = MicrosoftGraph.call_graph_api(token)
                
                # Verifica se a chamada à API do Microsoft Graph foi bem-sucedida
                if status_code != 200:
                    return jsonify(response), status_code
                
                request.graph_response = response
                
                # Verifica se o userPrincipalName está presente e contém o domínio esperado
                if 'userPrincipalName' not in request.graph_response or Util.DOMAIN not in request.graph_response['userPrincipalName']:
                    return jsonify(Util.TOKEN_INVALID), 401
            except Exception as e:
                return jsonify({'message': Util.TOKEN_ERROR.format(str(e))}), 401

            return f(*args, **kwargs)

        return decorated