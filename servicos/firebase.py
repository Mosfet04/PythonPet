import requests
import json
import os
from typing import Tuple, Dict, Any, Optional

try:
    import firebase_admin
    from firebase_admin import credentials, auth
    from google.auth.exceptions import GoogleAuthError
    FIREBASE_ADMIN_AVAILABLE = True
except ImportError:
    FIREBASE_ADMIN_AVAILABLE = False

# Importar configurações do Firebase
try:
    from config import get_firebase_config
    firebase_config = get_firebase_config()
except ImportError:
    # Fallback para configuração manual se config.py não estiver disponível
    firebase_config = {
        'projectId': os.getenv('FIREBASE_PROJECT_ID', 'pet-eq-auth')
    }

class Firebase:
    """
    Classe para autenticação e validação de tokens usando Firebase Auth
    Suporta tanto verificação via REST API quanto via SDK do Firebase Admin
    """
    
    _app = None
    _initialized = False
    
    @classmethod
    def initialize_app(cls, service_account_path: Optional[str] = None) -> bool:
        """
        Inicializa o Firebase Admin SDK
        
        Args:
            service_account_path (str, optional): Caminho para o arquivo de credenciais
            
        Returns:
            bool: True se inicializado com sucesso, False caso contrário
        """
        if cls._initialized or not FIREBASE_ADMIN_AVAILABLE:
            return cls._initialized
            
        try:
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                cls._app = firebase_admin.initialize_app(cred)
            else:
                # Tenta usar as credenciais padrão do ambiente
                cls._app = firebase_admin.initialize_app()
            
            cls._initialized = True
            return True
        except Exception:
            cls._initialized = False
            return False
    
    @classmethod
    def verify_id_token_admin_sdk(cls, token: str) -> Tuple[Dict[str, Any], int]:
        """
        Verifica um token ID usando o Firebase Admin SDK
        
        Args:
            token (str): Token ID do Firebase para verificação
            
        Returns:
            Tuple[Dict[str, Any], int]: Resposta da verificação e código de status
        """
        if not cls._initialized:
            return {'message': 'Firebase Admin SDK not initialized'}, 500
            
        try:
            # Remove o prefixo "Bearer " se presente
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")
            
            # Verifica o token usando o Admin SDK
            decoded_token = auth.verify_id_token(token)
            
            # Formatação padronizada dos dados do usuário
            formatted_response = {
                'uid': decoded_token.get('uid'),
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False),
                'display_name': decoded_token.get('name'),
                'picture': decoded_token.get('picture'),
                'firebase': decoded_token.get('firebase', {}),
                'auth_time': decoded_token.get('auth_time'),
                'iat': decoded_token.get('iat'),
                'exp': decoded_token.get('exp'),
                'aud': decoded_token.get('aud'),
                'iss': decoded_token.get('iss'),
                'sub': decoded_token.get('sub')
            }
            
            return formatted_response, 200
            
        except auth.InvalidIdTokenError:
            return {'message': 'Token ID inválido'}, 401
        except auth.ExpiredIdTokenError:
            return {'message': 'Token ID expirado'}, 401
        except auth.RevokedIdTokenError:
            return {'message': 'Token ID revogado'}, 401
        except GoogleAuthError as e:
            return {'message': f'Erro de autenticação: {str(e)}'}, 401
        except Exception as e:
            return {'message': f'Erro inesperado: {str(e)}'}, 500
    
    @staticmethod
    def verify_id_token(token: str, project_id: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """
        Verifica um token ID do Firebase Auth usando REST API
        
        Args:
            token (str): Token ID do Firebase para verificação
            project_id (str): ID do projeto Firebase (opcional, pode ser obtido do token)
            
        Returns:
            Tuple[Dict[str, Any], int]: Resposta da verificação e código de status
        """
        # Se o Admin SDK estiver disponível e inicializado, usa ele primeiro
        if FIREBASE_ADMIN_AVAILABLE and Firebase._initialized:
            return Firebase.verify_id_token_admin_sdk(token)
        
        try:
            # Remove o prefixo "Bearer " se presente
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")
            
            # Obter a API Key das configurações
            api_key = firebase_config.get('apiKey')
            if not api_key:
                return {'message': 'API Key do Firebase não configurada'}, 500
            
            # URL para verificação de token do Firebase com API Key
            verify_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}"
            
            payload = {
                "idToken": token
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(verify_url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Verifica se o usuário foi encontrado
                if 'users' in user_data and len(user_data['users']) > 0:
                    user_info = user_data['users'][0]
                    
                    # Formatação padronizada dos dados do usuário
                    formatted_response = {
                        'uid': user_info.get('localId'),
                        'email': user_info.get('email'),
                        'email_verified': user_info.get('emailVerified', False),
                        'display_name': user_info.get('displayName'),
                        'photo_url': user_info.get('photoUrl'),
                        'provider_data': user_info.get('providerUserInfo', []),
                        'custom_claims': user_info.get('customAttributes', {}),
                        'creation_time': user_info.get('createdAt'),
                        'last_sign_in_time': user_info.get('lastLoginAt'),
                        'disabled': user_info.get('disabled', False)
                    }
                    
                    return formatted_response, 200
                else:
                    return {'message': 'Usuário não encontrado'}, 404
            else:
                error_data: Dict[str, Any] = response.json() if response.content else {}
                return {
                    'message': 'Falha na verificação do token Firebase',
                    'error': error_data
                }, response.status_code
                
        except requests.exceptions.RequestException as e:
            return {
                'message': f'Erro de conexão ao verificar token: {str(e)}'
            }, 500
        except json.JSONDecodeError as e:
            return {
                'message': f'Erro ao processar resposta do Firebase: {str(e)}'
            }, 500
        except Exception as e:
            return {
                'message': f'Token inválido! Erro: {str(e)}'
            }, 401
    
    @staticmethod
    def verify_custom_token(custom_token: str, api_key: str) -> Tuple[Dict[str, Any], int]:
        """
        Troca um custom token por um ID token
        
        Args:
            custom_token (str): Custom token do Firebase
            api_key (str): Chave da API do Firebase
            
        Returns:
            Tuple[Dict[str, Any], int]: Resposta da verificação e código de status
        """
        try:
            # URL para trocar custom token por ID token
            exchange_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={api_key}"
            
            payload: Dict[str, Any] = {
                "token": custom_token,
                "returnSecureToken": True
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(exchange_url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                return {
                    'id_token': token_data.get('idToken'),
                    'refresh_token': token_data.get('refreshToken'),
                    'local_id': token_data.get('localId'),
                    'expires_in': token_data.get('expiresIn')
                }, 200
            else:
                error_data: Dict[str, Any] = response.json() if response.content else {}
                return {
                    'message': 'Falha na troca do custom token',
                    'error': error_data
                }, response.status_code
                
        except Exception as e:
            return {
                'message': f'Erro ao processar custom token: {str(e)}'
            }, 401
