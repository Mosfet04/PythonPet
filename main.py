from flask import Flask
from config import get_database
from facade.IntegrantesFacade import integrantes_bp
from models.IntegranteModel import Integrante
from models.SetorModel import Setor
from models.NoticiasModel import Noticia
from models.NoticiasCategoriaModel import NoticiasCategoria
from models.CategoriaEventoJorneqModel import CategoriaEventoJorneq
from models.JorneqModel import Jorneq
from models.MiniCursosModel import MiniCursos
from models.PatrocinadoresJorneqModel import PatrocinadoresJorneq
from models.PlanejamentoRelatorioModel import PlanejamentoRelatorio
from models.ProcessoSeletivoModel import ProcessoSeletivo
from models.ProgramacaoJorneqModel import ProgramacaoJorneq
from flasgger import Swagger

app = Flask(__name__)

# Configura o banco de dados
db = get_database()

swagger = Swagger(app, config={
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/api/swagger.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
})

# Registra o blueprint das rotas dos integrantes
app.register_blueprint(integrantes_bp, url_prefix="/api")

if __name__ == "__main__":
    try:
        db.connect()
        db.create_tables([Integrante, Setor, Noticia, NoticiasCategoria, CategoriaEventoJorneq, Jorneq, MiniCursos, PatrocinadoresJorneq, PlanejamentoRelatorio, ProcessoSeletivo, ProgramacaoJorneq], safe=True)
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        print(f"Erro ao conectar ou criar tabelas no banco de dados: {e}")
    finally:
        if not db.is_closed():
            db.close()