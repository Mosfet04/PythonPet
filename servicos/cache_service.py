"""
Serviço de Cache em Memória para a API do PET
Implementa cache com TTL (Time To Live) de 5 horas para otimizar consultas ao banco de dados.
"""

import hashlib
import json
import time
from typing import Any, Dict, Optional
from functools import wraps
import threading

class CacheService:
    """
    Serviço de cache em memória com TTL configurável.
    Thread-safe e otimizado para consultas de API.
    """
    
    def __init__(self, default_ttl: int = 18000, max_size: int = 1000):
        """
        Inicializa o serviço de cache.
        
        Args:
            default_ttl (int): Tempo de vida padrão em segundos (5 horas = 18000 segundos)
            max_size (int): Número máximo de entradas no cache
        """
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.cache = {}  # Dict[str, Dict[str, Any]]
        self.access_times = {}  # Dict[str, float]
        self.lock = threading.RLock()
        
    def _generate_cache_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera uma chave única para o cache baseada no endpoint e parâmetros.
        """
        if params is None:
            params = {}
            
        # Ordena os parâmetros para garantir consistência na chave
        sorted_params = json.dumps(params, sort_keys=True, default=str)
        cache_string = f"{endpoint}:{sorted_params}"
        
        # Gera hash MD5 da string para ter uma chave única e compacta
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _cleanup_expired(self) -> None:
        """Remove entradas expiradas do cache."""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time > entry['expires_at']:
                expired_keys.append(key)
        
        for key in expired_keys:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
    
    def _ensure_size_limit(self) -> None:
        """Garante que o cache não exceda o tamanho máximo."""
        if len(self.cache) >= self.max_size:
            # Remove a entrada menos acessada recentemente
            if self.access_times:
                oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
                if oldest_key in self.cache:
                    del self.cache[oldest_key]
                if oldest_key in self.access_times:
                    del self.access_times[oldest_key]
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """Recupera um valor do cache."""
        cache_key = self._generate_cache_key(endpoint, params)
        
        with self.lock:
            self._cleanup_expired()
            
            if cache_key in self.cache:
                entry = self.cache[cache_key]
                if time.time() <= entry['expires_at']:
                    # Atualiza tempo de acesso
                    self.access_times[cache_key] = time.time()
                    return entry['data']
                else:
                    # Entrada expirada
                    if cache_key in self.cache:
                        del self.cache[cache_key]
                    if cache_key in self.access_times:
                        del self.access_times[cache_key]
            
            return None
    
    def set(self, endpoint: str, data: Any, params: Optional[Dict[str, Any]] = None, ttl: Optional[int] = None) -> None:
        """Armazena um valor no cache."""
        cache_key = self._generate_cache_key(endpoint, params)
        used_ttl = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + used_ttl
        
        with self.lock:
            self._cleanup_expired()
            self._ensure_size_limit()
            
            self.cache[cache_key] = {
                'data': data,
                'expires_at': expires_at,
                'created_at': time.time()
            }
            self.access_times[cache_key] = time.time()
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """Remove uma entrada específica do cache."""
        cache_key = self._generate_cache_key(endpoint, params)
        
        with self.lock:
            found = cache_key in self.cache
            if found:
                if cache_key in self.cache:
                    del self.cache[cache_key]
                if cache_key in self.access_times:
                    del self.access_times[cache_key]
            return found
    
    def clear_endpoint_cache(self, endpoint: str) -> int:
        """Remove todas as entradas de cache relacionadas a um endpoint específico."""
        removed_count = 0
        keys_to_remove = []
        
        with self.lock:
            # Gera um hash de exemplo para comparação
            example_key = self._generate_cache_key(endpoint, {})
            endpoint_prefix = example_key[:8]  # Usa primeiros 8 caracteres como identificador
            
            for cache_key in list(self.cache.keys()):
                if cache_key.startswith(endpoint_prefix):
                    keys_to_remove.append(cache_key)
            
            for key in keys_to_remove:
                if key in self.cache:
                    del self.cache[key]
                    removed_count += 1
                if key in self.access_times:
                    del self.access_times[key]
                    
        return removed_count
    
    def clear_all(self) -> None:
        """Remove todas as entradas do cache."""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        with self.lock:
            self._cleanup_expired()
            return {
                'current_size': len(self.cache),
                'max_size': self.max_size,
                'ttl_seconds': self.default_ttl,
                'ttl_hours': self.default_ttl / 3600,
                'sample_keys': list(self.cache.keys())[:5]  # Primeiras 5 chaves para debug
            }


# Instância global do serviço de cache
cache_service = CacheService()


def cache_result(endpoint_name: str = None, ttl: int = None, exclude_params: list = None):
    """
    Decorator para cache automático de resultados de funções.
    
    Args:
        endpoint_name (str): Nome do endpoint (usar nome da função se None)
        ttl (int): Tempo de vida personalizado em segundos
        exclude_params (list): Lista de parâmetros a excluir da chave de cache
        
    Usage:
        @cache_result("list_pesquisas", ttl=7200)
        def list_pesquisas(ativo, page, per_page):
            # função que será cacheada
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Define o nome do endpoint
            endpoint = endpoint_name or func.__name__
            
            # Prepara parâmetros para a chave de cache
            params = {}
            
            # Adiciona argumentos posicionais
            if args:
                for i, arg in enumerate(args):
                    params[f'arg_{i}'] = arg
            
            # Adiciona argumentos nomeados
            if kwargs:
                params.update(kwargs)
            
            # Remove parâmetros excluídos se especificados
            if exclude_params:
                for param in exclude_params:
                    params.pop(param, None)
            
            # Tenta recuperar do cache primeiro
            cached_result = cache_service.get(endpoint, params)
            if cached_result is not None:
                return cached_result
            
            # Executa a função original
            result = func(*args, **kwargs)
            
            # Armazena o resultado no cache
            cache_service.set(endpoint, result, params, ttl)
            
            return result
        
        return wrapper
    return decorator


def invalidate_cache(endpoint_name: str, params: Optional[Dict[str, Any]] = None):
    """
    Função utilitária para invalidar cache específico.
    
    Args:
        endpoint_name (str): Nome do endpoint
        params (Dict): Parâmetros específicos (None para invalidar todo o endpoint)
    """
    if params is None:
        return cache_service.clear_endpoint_cache(endpoint_name)
    else:
        return cache_service.delete(endpoint_name, params)
