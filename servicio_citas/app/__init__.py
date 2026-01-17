from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'odontocare-secret-key-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///odontocare_citas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-odontocare-secret-2024')
    
    # URL del servicio de usuarios (para comunicación entre microservicios)
    app.config['SERVICIO_USUARIOS_URL'] = os.environ.get('SERVICIO_USUARIOS_URL', 'http://localhost:5000')
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Registrar blueprints
    from app.blueprints.citas import citas_bp
    
    app.register_blueprint(citas_bp, url_prefix='/citas')
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app
