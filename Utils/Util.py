from functools import wraps
from flask import jsonify, request
import requests
import yaml
from pydantic import BaseModel

class Util(BaseModel):
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
            if 'Authorization' in request.headers:
                parts = request.headers['Authorization'].split(" ")
                if len(parts) != 2 or parts[0] != "Bearer":
                    return jsonify({'message': 'Token is missing or invalid!'}), 401

            try:
                graph_url = 'https://graph.microsoft.com/v1.0/me'
                headers = {'Authorization': request.headers['Authorization']}
                graph_response = requests.get(graph_url, headers=headers)
                if graph_response.status_code != 200:
                    return jsonify({'message': 'Failed to call Microsoft Graph API', 'error': graph_response.json()}), graph_response.status_code
            except Exception as e:
                return jsonify({'message': f'Token is invalid! Error: {str(e)}'}), 401
            
            request.graph_response = graph_response.json()
            if 'userPrincipalName' not in request.graph_response or "AVLMascaras.onmicrosoft.com" not in request.graph_response['userPrincipalName']:
                return jsonify({'message': 'Token is invalid!'}), 401
            return f(*args, **kwargs)

        return decorated