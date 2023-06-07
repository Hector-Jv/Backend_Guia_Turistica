from flask import Flask 
from flask_sqlalchemy import SQLAlchemy # Para interacción con base de datos.
from flask_migrate import Migrate # Para hacer migraciones en la base de datos.
from flask_cors import CORS # Para habilitar y configurar el Cross-Origin Resource Sharing (es un mecanismo de seguridad).
from app.config import Config # Para hacer configuraciones.
from flask_jwt_extended import JWTManager # Para la autenticación y autorización basada en tokens JWT.
from flask_smorest import Api
from datetime import timedelta
import os
import cloudinary
import cloudinary.uploader


db = SQLAlchemy() # Instancia para interactuar con la base de datos.
migrate = Migrate() # Intancia para gestionar las migraciones.

def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class) 

    app.config['JWT_SECRET_KEY'] =  os.environ.get('SECRET_KEY_TOKEN') 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    jwt = JWTManager(app)
    
    db.init_app(app) # Inicializa instancia de SQLAlchemy.
    migrate.init_app(app, db) # Inicializa instancia de Migrate
    CORS(app) # Habilita y configura CORS.
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Sistema de recomendación para guía turística"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/" 
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    cloudinary.config(
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),  
        api_key = os.environ.get('CLOUDINARY_API_KEY'),  
        api_secret = os.environ.get('CLOUDINARY_API_SECRET'), 
        secure = True
    )

    api = Api(app)
    
    with app.app_context():
        db.create_all()
    
    # Rutas que se han registrado
    from .routes.Autenticacion import all_blueprints as autenticacion_blueprints
    from .routes.Sitios import all_blueprints as sitios_blueprints
    
    for bp in autenticacion_blueprints:
        api.register_blueprint(bp)
    for bp in sitios_blueprints:
        app.register_blueprint(bp)
        
    return app 
