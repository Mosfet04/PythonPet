# app/__init__.py

# Importações necessárias para inicializar o pacote
from .controllers import *
from .models import *
from .dtos.requests import *
from .dtos.responses import *

# Código de inicialização, se necessário
# Por exemplo, configuração de logging ou inicialização de variáveis globais
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Pacote app inicializado com sucesso.")
