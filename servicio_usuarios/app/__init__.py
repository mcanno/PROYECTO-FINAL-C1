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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///odontocare_usuarios.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-odontocare-secret-2024')
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Registrar blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Crear tablas
    with app.app_context():
        db.create_all()
        # Crear usuario admin por defecto si no existe
        from app.models import Usuario
        admin = Usuario.query.filter_by(nombre_usuario='admin').first()
        if not admin:
            from werkzeug.security import generate_password_hash
            admin = Usuario(
                nombre_usuario='admin',
                password=generate_password_hash('admin123'),
                rol='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    return app
