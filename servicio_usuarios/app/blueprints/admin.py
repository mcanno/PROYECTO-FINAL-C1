from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app import db
from app.models import Usuario, Paciente, Doctor, Centro

admin_bp = Blueprint('admin', __name__)


def requiere_admin(func):
    """Decorador para verificar rol admin"""
    from functools import wraps
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['rol'] != 'admin':
            return jsonify({'error': 'Acceso denegado. Se requiere rol admin'}), 403
        return func(*args, **kwargs)
    return wrapper


# ==================== USUARIOS ====================

@admin_bp.route('/usuario', methods=['POST'])
@requiere_admin
def crear_usuario():
    """Crear un nuevo usuario"""
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
        'mensaje': 'Usuario creado exitosamente',
        'usuario': nuevo_usuario.to_dict()
    }), 201


@admin_bp.route('/usuarios', methods=['GET'])
@requiere_admin
def listar_usuarios():
    """Listar todos los usuarios"""
    usuarios = Usuario.query.all()
    return jsonify({
        'total': len(usuarios),
        'usuarios': [u.to_dict() for u in usuarios]
    }), 200


@admin_bp.route('/usuario/<int:id_user>', methods=['GET'])
@requiere_admin
def obtener_usuario(id_user):
    """Obtener un usuario por ID"""
    usuario = Usuario.query.get(id_user)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(usuario.to_dict()), 200


# ==================== DOCTORES ====================

@admin_bp.route('/doctores', methods=['POST'])
@requiere_admin
def crear_doctor():
    """Crear un nuevo doctor (y su usuario asociado)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    nombre = data.get('nombre')
    especialidad = data.get('especialidad')
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')
    
    if not nombre or not especialidad:
        return jsonify({'error': 'nombre y especialidad son requeridos'}), 400
    
    id_user = None
    
    # Si se proporcionan credenciales, crear usuario
    if nombre_usuario and password:
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            return jsonify({'error': 'El nombre de usuario ya existe'}), 409
        
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            password=generate_password_hash(password),
            rol='medico'
        )
        db.session.add(nuevo_usuario)
        db.session.flush()
        id_user = nuevo_usuario.id_user
    
    nuevo_doctor = Doctor(
        id_user=id_user,
        nombre=nombre,
        especialidad=especialidad
    )
    
    db.session.add(nuevo_doctor)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Doctor creado exitosamente',
        'doctor': nuevo_doctor.to_dict()
    }), 201


@admin_bp.route('/doctores', methods=['GET'])
@jwt_required()
def listar_doctores():
    """Listar todos los doctores"""
    doctores = Doctor.query.all()
    return jsonify({
        'total': len(doctores),
        'doctores': [d.to_dict() for d in doctores]
    }), 200


@admin_bp.route('/doctores/<int:id_doctor>', methods=['GET'])
@jwt_required()
def obtener_doctor(id_doctor):
    """Obtener un doctor por ID"""
    doctor = Doctor.query.get(id_doctor)
    if not doctor:
        return jsonify({'error': 'Doctor no encontrado', 'existe': False}), 404
    return jsonify({**doctor.to_dict(), 'existe': True}), 200


# ==================== PACIENTES ====================

@admin_bp.route('/pacientes', methods=['POST'])
@requiere_admin
def crear_paciente():
    """Crear un nuevo paciente (y su usuario asociado)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    estado = data.get('estado', 'ACTIVO')
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')
    
    if not nombre or not telefono:
        return jsonify({'error': 'nombre y telefono son requeridos'}), 400
    
    id_user = None
    
    # Si se proporcionan credenciales, crear usuario
    if nombre_usuario and password:
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            return jsonify({'error': 'El nombre de usuario ya existe'}), 409
        
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            password=generate_password_hash(password),
            rol='paciente'
        )
        db.session.add(nuevo_usuario)
        db.session.flush()
        id_user = nuevo_usuario.id_user
    
    nuevo_paciente = Paciente(
        id_user=id_user,
        nombre=nombre,
        telefono=telefono,
        estado=estado
    )
    
    db.session.add(nuevo_paciente)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Paciente creado exitosamente',
        'paciente': nuevo_paciente.to_dict()
    }), 201


@admin_bp.route('/pacientes', methods=['GET'])
@jwt_required()
def listar_pacientes():
    """Listar todos los pacientes"""
    pacientes = Paciente.query.all()
    return jsonify({
        'total': len(pacientes),
        'pacientes': [p.to_dict() for p in pacientes]
    }), 200


@admin_bp.route('/pacientes/<int:id_paciente>', methods=['GET'])
@jwt_required()
def obtener_paciente(id_paciente):
    """Obtener un paciente por ID"""
    paciente = Paciente.query.get(id_paciente)
    if not paciente:
        return jsonify({'error': 'Paciente no encontrado', 'existe': False, 'activo': False}), 404
    return jsonify({
        **paciente.to_dict(), 
        'existe': True, 
        'activo': paciente.estado == 'ACTIVO'
    }), 200


# ==================== CENTROS ====================

@admin_bp.route('/centros', methods=['POST'])
@requiere_admin
def crear_centro():
    """Crear un nuevo centro médico"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    
    if not nombre or not direccion:
        return jsonify({'error': 'nombre y direccion son requeridos'}), 400
    
    nuevo_centro = Centro(
        nombre=nombre,
        direccion=direccion
    )
    
    db.session.add(nuevo_centro)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Centro creado exitosamente',
        'centro': nuevo_centro.to_dict()
    }), 201


@admin_bp.route('/centros', methods=['GET'])
@jwt_required()
def listar_centros():
    """Listar todos los centros"""
    centros = Centro.query.all()
    return jsonify({
        'total': len(centros),
        'centros': [c.to_dict() for c in centros]
    }), 200


@admin_bp.route('/centros/<int:id_centro>', methods=['GET'])
@jwt_required()
def obtener_centro(id_centro):
    """Obtener un centro por ID"""
    centro = Centro.query.get(id_centro)
    if not centro:
        return jsonify({'error': 'Centro no encontrado', 'existe': False}), 404
    return jsonify({**centro.to_dict(), 'existe': True}), 200
