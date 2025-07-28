from functools import wraps
from flask import jsonify, request
import yaml
from pydantic import BaseModel
import os
from typing import Dict, Any, List, Optional, Callable

from servicos.firebase import Firebase

class Util():
    # Constantes para mensagens de erro
    TOKEN_MISSING = {'message': 'Token is missing!'}
    TOKEN_INVALID = {'message': 'Token is missing or invalid!'}
    TOKEN_ERROR = 'Token is invalid! Error: {}'
    # Domínios permitidos para validação de email (DESABILITADO - permite todos os domínios)
    ALLOWED_DOMAINS = []  # Lista vazia = permite todos os domínios
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    @staticmethod
    def str_to_bool(value: Any) -> bool:
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
                response, status_code = Firebase.verify_id_token(token)
                
                # Verifica se a chamada à API do Firebase foi bem-sucedida
                if status_code != 200:
                    return jsonify(response), status_code
                
                # Armazena a resposta do Firebase no request para uso posterior
                request.firebase_response = response
                
                # Verifica se o email está presente e é válido
                if 'email' not in request.firebase_response:
                    return jsonify(Util.TOKEN_INVALID), 401
                
                # Verifica se o email foi verificado
                if not request.firebase_response.get('email_verified', False):
                    return jsonify({'message': 'Email not verified!'}), 401
                
                # Validação de domínio DESABILITADA - permite todos os domínios
                # Para restringir domínios, use o decorator firebase_token_required(allowed_domains=[...])
                # user_email = request.firebase_response['email']
                # if not any(domain in user_email for domain in Util.ALLOWED_DOMAINS):
                #     return jsonify({'message': 'Email domain not allowed!'}), 401
                    
            except Exception as e:
                return jsonify({'message': Util.TOKEN_ERROR.format(str(e))}), 401

            return f(*args, **kwargs)

        return decorated
    
    @staticmethod
    def firebase_token_required(allowed_domains: Optional[List[str]] = None):
        """
        Decorator mais flexível que permite configurar domínios permitidos
        
        Args:
            allowed_domains (list[str], optional): Lista de domínios permitidos. 
                                                  Se None, não valida domínio.
        """
        def decorator(f):
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
                    response, status_code = Firebase.verify_id_token(token)
                    
                    # Verifica se a chamada à API do Firebase foi bem-sucedida
                    if status_code != 200:
                        return jsonify(response), status_code
                    
                    # Armazena a resposta do Firebase no request para uso posterior
                    request.firebase_response = response
                    
                    # Verifica se o email está presente
                    if 'email' not in request.firebase_response:
                        return jsonify(Util.TOKEN_INVALID), 401
                    
                    # Verifica se o email foi verificado
                    if not request.firebase_response.get('email_verified', False):
                        return jsonify({'message': 'Email not verified!'}), 401
                    
                    # Validação de domínio se especificada
                    if allowed_domains:
                        user_email = request.firebase_response['email']
                        if not any(domain in user_email for domain in allowed_domains):
                            return jsonify({'message': 'Email domain not allowed!'}), 401
                        
                except Exception as e:
                    return jsonify({'message': Util.TOKEN_ERROR.format(str(e))}), 401

                return f(*args, **kwargs)

            return decorated
        return decorator