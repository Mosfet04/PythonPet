from flask import Flask
from config import get_database
from facade.IntegrantesFacade import integrantes_bp
from facade.NoticiasFacade import noticias_bp
from facade.PlanejamentoRelatorioFacade import planejamentoRelatorio_bp
from facade.ProcessoSeletivoFacade import processoSeletivo_bp
from facade.MiniCursosFacade import minicursos_bp
from facade.PesquisaFacade import pesquisa_bp
from facade.ExtensaoFacade import extensao_bp
from facade.CalendarioAtividadesFacade import calendarioAtividades_bp
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
from models.PesquisaModel import Pesquisa
from models.ExtensaoModel import Extensao
from models.CalendarioAtividadesModel import CalendarioAtividades
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Authorization", "Content-Type"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})
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
    "specs_route": "/api/docs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "info": {
        "title": "API de gerenciamento de registros do PET",
        "description": "Esta é a documentação da API de registros do PET. Aqui você pode encontrar todos os endpoints disponíveis e como utilizá-los.",
        "version": "1.0.0",
        "termsOfService": "/terms",
        "contact": {
            "name": "Desenvolvedor - Mateus Meireles Ribeiro",
            "email": "mateusmr4@gmail.com"
        }
    }
})

# Registra o blueprint das rotas dos integrantes
app.register_blueprint(integrantes_bp, url_prefix="/api")
app.register_blueprint(noticias_bp, url_prefix="/api")
app.register_blueprint(planejamentoRelatorio_bp, url_prefix="/api")
app.register_blueprint(processoSeletivo_bp, url_prefix="/api")
app.register_blueprint(minicursos_bp, url_prefix="/api")
app.register_blueprint(pesquisa_bp, url_prefix="/api")
app.register_blueprint(extensao_bp, url_prefix="/api")
app.register_blueprint(calendarioAtividades_bp, url_prefix="/api")

if __name__ == "__main__":
    try:
        # Teste de conexão com o banco
        print("Tentando conectar ao banco de dados...")
        db.connect()
        print("Conexão com o banco estabelecida com sucesso!")
        
        # Para Neon PostgreSQL: definir search_path após a conexão (não nas startup options)
        print("Configurando schema público para Neon...")
        try:
            db.execute_sql("SET search_path TO public;")
            print("Schema público configurado!")
        except Exception as schema_error:
            print(f"Aviso: Não foi possível definir schema explicitamente: {schema_error}")
            print("Continuando com schema padrão...")
        
        # Criação das tabelas
        print("Criando tabelas...")
        db.create_tables([Integrante, Setor, Noticia, NoticiasCategoria, CategoriaEventoJorneq, Jorneq, MiniCursos, PatrocinadoresJorneq, PlanejamentoRelatorio, ProcessoSeletivo, ProgramacaoJorneq, Pesquisa, Extensao, CalendarioAtividades], safe=True)
        print("Tabelas criadas com sucesso!")
        
        # Inserção de dados iniciais
        if Setor.select().count() == 0:
            print("Inserindo setores padrão...")
            # Inserir registros
            Setor.insert_many([
                {'id': 1, 'nome': 'Computação'},
                {'id': 2, 'nome': 'Ata'},
                {'id': 3, 'nome': 'Marketing'},
                {'id': 4, 'nome': 'Orientador'},
            ]).execute()
            print("Setores inseridos com sucesso!")
        
        if NoticiasCategoria.select().count() == 0:
            print("Inserindo categorias de notícias padrão...")
            NoticiasCategoria.insert_many([
                {'id': 1, 'nome': 'Ensino'},
                {'id': 2, 'nome': 'Pesquisa'},
                {'id': 3, 'nome': 'Extensão'},
                {'id': 4, 'nome': 'Processo Seletivo'}
            ]).execute()
            print("Categorias de notícias inseridas com sucesso!")
            
        print("Iniciando servidor Flask...")
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        print(f"Erro ao conectar ou criar tabelas no banco de dados: {e}")
        print("Verifique se:")
        print("1. O arquivo .env está configurado corretamente")
        print("2. As credenciais do Neon estão corretas")
        print("3. A connection string do Neon está válida")
        print("4. O schema público está acessível no Neon")
        print("5. Para Neon: use conexão pooled (padrão) sem parâmetros startup customizados")
    finally:
        if not db.is_closed():
            print("Fechando conexão com o banco...")
            db.close()