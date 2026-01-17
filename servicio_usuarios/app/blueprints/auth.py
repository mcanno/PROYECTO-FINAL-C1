from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicio de sesión - Retorna token JWT"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')
    
    if not nombre_usuario or not password:
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
    
    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
    
    if not usuario or not check_password_hash(usuario.password, password):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    # Crear token con información del usuario
    access_token = create_access_token(
        identity={
            'id_user': usuario.id_user,
            'nombre_usuario': usuario.nombre_usuario,
            'rol': usuario.rol
        }
    )
    
    return jsonify({
        'mensaje': 'Login exitoso',
        'token': access_token,
        'usuario': usuario.to_dict()
    }), 200


@auth_bp.route('/registro', methods=['POST'])
@jwt_required()
def registro():
    """Registro de nuevos usuarios - Solo admin"""
    current_user = get_jwt_identity()
    
    if current_user['rol'] != 'admin':
        return jsonify({'error': 'Acceso denegado. Se requiere rol admin'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')
    rol = data.get('rol')
    
    if not nombre_usuario or not password or not rol:
        return jsonify({'error': 'nombre_usuario, password y rol son requeridos'}), 400
    
    roles_validos = ['admin', 'medico', 'secretaria', 'paciente']
    if rol not in roles_validos:
        return jsonify({'error': f'Rol inválido. Roles válidos: {roles_validos}'}), 400
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return jsonify({'error': 'El nombre de usuario ya existe'}), 409
    
    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        password=generate_password_hash(password),
        rol=rol
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Usuario registrado exitosamente',
        'usuario': nuevo_usuario.to_dict()
    }), 201


@auth_bp.route('/verificar', methods=['GET'])
@jwt_required()
def verificar_token():
    """Verificar validez del token"""
    current_user = get_jwt_identity()
    return jsonify({
        'valido': True,
        'usuario': current_user
    }), 200


@auth_bp.route('/usuario/<int:id_user>', methods=['GET'])
@jwt_required()
def obtener_usuario(id_user):
    """Obtener información de un usuario por ID"""
    usuario = Usuario.query.get(id_user)
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify(usuario.to_dict()), 200
