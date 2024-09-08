from flask import Flask
from config import get_database
from facade.integrantesFacade import integrantes_bp
from models.integranteModel import Integrante
from models.setorModel import Setor
from models.noticiasModel import Noticia
from models.noticiasCategoria import NoticiasCategoria
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
    db.connect()
    db.create_tables([Integrante, Setor, Noticia, NoticiasCategoria])
    app.run(debug=True)