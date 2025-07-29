import time
from datetime import datetime, timezone
from peewee import DoesNotExist
from config import get_database
from models.IntegranteModel import Integrante

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False

def get_basic_health():
    """
    Verifica a saúde básica da aplicação
    """
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "PythonPet API",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "PythonPet API",
            "version": "1.0.0",
            "error": str(e)
        }

def get_detailed_health():
    """
    Verifica a saúde detalhada da aplicação incluindo dependências
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "PythonPet API",
        "version": "1.0.0",
        "checks": {}
    }
    
    overall_healthy = True
    
    # Verificação do banco de dados
    db_health = check_database_health()
    health_status["checks"]["database"] = db_health
    if db_health["status"] != "healthy":
        overall_healthy = False
    
    # Verificação do cache
    cache_health = check_cache_health()
    health_status["checks"]["cache"] = cache_health
    if cache_health["status"] != "healthy" and cache_health["status"] != "degraded":
        overall_healthy = False
    
    # Verificação dos recursos do sistema (se psutil estiver disponível)
    if _PSUTIL_AVAILABLE:
        system_health = check_system_resources()
        health_status["checks"]["system"] = system_health
        if system_health["status"] != "healthy" and system_health["status"] != "degraded":
            overall_healthy = False
    else:
        health_status["checks"]["system"] = {
            "status": "unknown",
            "details": "psutil library not available"
        }
    
    # Status geral
    health_status["status"] = "healthy" if overall_healthy else "unhealthy"
    
    return health_status

def check_database_health():
    """
    Verifica a conectividade e saúde do banco de dados
    """
    db = None
    try:
        db = get_database()
        start_time = time.time()
        
        # Testa a conexão
        if db.is_closed():
            db.connect()
        
        # Executa uma query simples para testar
        db.execute_sql("SELECT 1")
        
        # Testa se consegue acessar uma tabela (usando Integrante como exemplo)
        list(Integrante.select().limit(1))
        
        response_time = (time.time() - start_time) * 1000  # em milissegundos
        
        return {
            "status": "healthy",
            "response_time_ms": round(response_time, 2),
            "details": "Database connection successful"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "details": "Database connection failed"
        }
    finally:
        if db and not db.is_closed():
            db.close()

def check_cache_health():
    """
    Verifica a saúde do sistema de cache
    """
    try:
        # Importa a instância do cache
        from servicos.cache_service import cache_service
        
        # Testa operações básicas do cache
        test_key = "health_check_test"
        test_data = {"test": "cache_health"}
        
        # Tenta salvar no cache
        cache_service.set(test_key, test_data, ttl=30)
        
        # Tenta recuperar do cache
        cached_data = cache_service.get(test_key)
        
        # Limpa o teste
        cache_service.delete(test_key)
        
        if cached_data == test_data:
            return {
                "status": "healthy",
                "details": "Cache service is working properly"
            }
        else:
            return {
                "status": "degraded",
                "details": "Cache service responded but data doesn't match"
            }
            
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "details": "Cache service check failed but application can continue"
        }

def check_system_resources():
    """
    Verifica os recursos do sistema (CPU, Memória, Disco)
    """
    if not _PSUTIL_AVAILABLE:
        return {
            "status": "unknown",
            "details": "psutil library not available"
        }
    
    try:
        import psutil
        
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory Usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk Usage (usando C: no Windows)
        try:
            disk = psutil.disk_usage('C:' if psutil.WINDOWS else '/')
            disk_percent = disk.percent
        except:
            disk_percent = 0
        
        # Determina o status baseado nos thresholds
        status = "healthy"
        warnings = []
        
        if cpu_percent > 80:
            status = "degraded"
            warnings.append(f"High CPU usage: {cpu_percent}%")
        
        if memory_percent > 80:
            status = "degraded"
            warnings.append(f"High memory usage: {memory_percent}%")
        
        if disk_percent > 80:
            status = "degraded"
            warnings.append(f"High disk usage: {disk_percent}%")
        
        if cpu_percent > 95 or memory_percent > 95 or disk_percent > 95:
            status = "unhealthy"
        
        return {
            "status": status,
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory_percent,
            "disk_usage_percent": disk_percent,
            "warnings": warnings if warnings else None
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "details": "System resources check failed"
        }

def get_readiness():
    """
    Verifica se a aplicação está pronta para receber tráfego
    """
    try:
        # Verifica se o banco está acessível
        db_health = check_database_health()
        
        if db_health["status"] == "healthy":
            return {
                "status": "ready",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": "Application is ready to serve traffic"
            }
        else:
            return {
                "status": "not_ready",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": "Database is not available",
                "database_status": db_health
            }
            
    except Exception as e:
        return {
            "status": "not_ready",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
            "details": "Readiness check failed"
        }

def get_liveness():
    """
    Verifica se a aplicação está viva (não travada)
    """
    try:
        # Verificação simples de que a aplicação está respondendo
        start_time = time.time()
        
        # Simula uma operação básica
        test_data = {"test": "alive"}
        
        response_time = (time.time() - start_time) * 1000
        
        return {
            "status": "alive",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "response_time_ms": round(response_time, 2),
            "details": "Application is alive and responding"
        }
        
    except Exception as e:
        return {
            "status": "dead",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
            "details": "Liveness check failed"
        }
