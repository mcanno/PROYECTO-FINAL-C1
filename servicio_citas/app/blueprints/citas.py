from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Cita
from app.services import ServicioUsuarios

citas_bp = Blueprint('citas', __name__)


def obtener_token():
    """Obtiene el token del header Authorization"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return None


def verificar_disponibilidad_doctor(id_doctor, fecha, id_cita_excluir=None):
    """Verifica que el doctor no tenga otra cita en la misma fecha/hora"""
    query = Cita.query.filter(
        Cita.id_doctor == id_doctor,
        Cita.fecha == fecha,
        Cita.estado != 'CANCELADA'
    )
    if id_cita_excluir:
        query = query.filter(Cita.id_cita != id_cita_excluir)
    
    cita_existente = query.first()
    return cita_existente is None


@citas_bp.route('', methods=['POST'])
@jwt_required()
def crear_cita():
    """Crear una nueva cita médica"""
    current_user = get_jwt_identity()
    token = obtener_token()
    
    # Verificar roles permitidos
    roles_permitidos = ['admin', 'paciente', 'secretaria']
    if current_user['rol'] not in roles_permitidos:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    # Campos requeridos
    id_paciente = data.get('id_paciente')
    id_doctor = data.get('id_doctor')
    id_centro = data.get('id_centro')
    fecha_str = data.get('fecha')
    motivo = data.get('motivo')
    
    if not all([id_paciente, id_doctor, id_centro, fecha_str, motivo]):
        return jsonify({'error': 'id_paciente, id_doctor, id_centro, fecha y motivo son requeridos'}), 400
    
    # Parsear fecha
    try:
        fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Validar que el doctor existe (via servicio REST)
    doctor_info = ServicioUsuarios.verificar_doctor(id_doctor, token)
    if not doctor_info.get('existe'):
        return jsonify({'error': 'El doctor no existe'}), 404
    
    # Validar que el paciente existe y está activo
    paciente_info = ServicioUsuarios.verificar_paciente(id_paciente, token)
    if not paciente_info.get('existe'):
        return jsonify({'error': 'El paciente no existe'}), 404
    if not paciente_info.get('activo'):
        return jsonify({'error': 'El paciente no está activo'}), 400
    
    # Validar que el centro existe
    centro_info = ServicioUsuarios.verificar_centro(id_centro, token)
    if not centro_info.get('existe'):
        return jsonify({'error': 'El centro médico no existe'}), 404
    
    # Verificar disponibilidad del doctor
    if not verificar_disponibilidad_doctor(id_doctor, fecha):
        return jsonify({'error': 'El doctor ya tiene una cita programada en esa fecha y hora'}), 409
    
    # Crear la cita
    nueva_cita = Cita(
        fecha=fecha,
        motivo=motivo,
        estado='PROGRAMADA',
        id_paciente=id_paciente,
        id_doctor=id_doctor,
        id_centro=id_centro,
        id_user_registrado=current_user['id_user']
    )
    
    db.session.add(nueva_cita)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Cita creada exitosamente',
        'cita': nueva_cita.to_dict()
    }), 201


@citas_bp.route('', methods=['GET'])
@jwt_required()
def listar_citas():
    """Listar citas con filtros según el rol del usuario"""
    current_user = get_jwt_identity()
    rol = current_user['rol']
    
    query = Cita.query
    
    # Filtros según rol
    if rol == 'medico':
        # El doctor solo ve sus propias citas
        # Necesitamos obtener el id_doctor asociado al usuario
        query = query.filter(Cita.id_doctor == request.args.get('id_doctor', type=int))
    
    elif rol == 'paciente':
        # El paciente solo ve sus propias citas
        id_paciente = request.args.get('id_paciente', type=int)
        if id_paciente:
            query = query.filter(Cita.id_paciente == id_paciente)
    
    elif rol == 'secretaria':
        # Secretaría puede filtrar por fecha
        fecha_str = request.args.get('fecha')
        if fecha_str:
            try:
                fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                query = query.filter(db.func.date(Cita.fecha) == fecha.date())
            except ValueError:
                pass
    
    elif rol == 'admin':
        # Admin puede filtrar por todo
        if request.args.get('id_doctor'):
            query = query.filter(Cita.id_doctor == request.args.get('id_doctor', type=int))
        if request.args.get('id_centro'):
            query = query.filter(Cita.id_centro == request.args.get('id_centro', type=int))
        if request.args.get('id_paciente'):
            query = query.filter(Cita.id_paciente == request.args.get('id_paciente', type=int))
        if request.args.get('estado'):
            query = query.filter(Cita.estado == request.args.get('estado'))
        fecha_str = request.args.get('fecha')
        if fecha_str:
            try:
                fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                query = query.filter(db.func.date(Cita.fecha) == fecha.date())
            except ValueError:
                pass
    
    citas = query.all()
    
    return jsonify({
        'total': len(citas),
        'citas': [c.to_dict() for c in citas]
    }), 200


@citas_bp.route('/<int:id_cita>', methods=['GET'])
@jwt_required()
def obtener_cita(id_cita):
    """Obtener una cita por ID"""
    cita = Cita.query.get(id_cita)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404
    return jsonify(cita.to_dict()), 200


@citas_bp.route('/<int:id_cita>/cancelar', methods=['PUT'])
@jwt_required()
def cancelar_cita(id_cita):
    """Cancelar una cita existente"""
    current_user = get_jwt_identity()
    
    # Verificar roles permitidos
    roles_permitidos = ['admin', 'paciente', 'secretaria']
    if current_user['rol'] not in roles_permitidos:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    cita = Cita.query.get(id_cita)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404
    
    if cita.estado == 'CANCELADA':
        return jsonify({'error': 'La cita ya está cancelada'}), 400
    
    cita.estado = 'CANCELADA'
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Cita cancelada exitosamente',
        'cita': cita.to_dict()
    }), 200


@citas_bp.route('/<int:id_cita>', methods=['PUT'])
@jwt_required()
def modificar_cita(id_cita):
    """Modificar una cita existente (cambiar fecha, doctor, centro, etc.)"""
    current_user = get_jwt_identity()
    token = obtener_token()
    
    # Verificar roles permitidos
    roles_permitidos = ['admin', 'paciente', 'secretaria']
    if current_user['rol'] not in roles_permitidos:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    cita = Cita.query.get(id_cita)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404
    
    if cita.estado == 'CANCELADA':
        return jsonify({'error': 'No se puede modificar una cita cancelada'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    # Obtener nuevos valores o mantener los actuales
    nuevo_id_doctor = data.get('id_doctor', cita.id_doctor)
    nuevo_id_paciente = data.get('id_paciente', cita.id_paciente)
    nuevo_id_centro = data.get('id_centro', cita.id_centro)
    nuevo_motivo = data.get('motivo', cita.motivo)
    
    nueva_fecha = cita.fecha
    if data.get('fecha'):
        try:
            nueva_fecha = datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    # Validar doctor
    if nuevo_id_doctor != cita.id_doctor:
        doctor_info = ServicioUsuarios.verificar_doctor(nuevo_id_doctor, token)
        if not doctor_info.get('existe'):
            return jsonify({'error': 'El doctor no existe', 'cambio_realizado': False}), 404
    
    # Validar paciente
    if nuevo_id_paciente != cita.id_paciente:
        paciente_info = ServicioUsuarios.verificar_paciente(nuevo_id_paciente, token)
        if not paciente_info.get('existe'):
            return jsonify({'error': 'El paciente no existe', 'cambio_realizado': False}), 404
        if not paciente_info.get('activo'):
            return jsonify({'error': 'El paciente no está activo', 'cambio_realizado': False}), 400
    
    # Validar centro
    if nuevo_id_centro != cita.id_centro:
        centro_info = ServicioUsuarios.verificar_centro(nuevo_id_centro, token)
        if not centro_info.get('existe'):
            return jsonify({'error': 'El centro médico no existe', 'cambio_realizado': False}), 404
    
    # Verificar disponibilidad del doctor (excluyendo la cita actual)
    if not verificar_disponibilidad_doctor(nuevo_id_doctor, nueva_fecha, id_cita):
        return jsonify({
            'error': 'El doctor ya tiene una cita programada en esa fecha y hora',
            'cambio_realizado': False
        }), 409
    
    # Cancelar la cita anterior y crear una nueva (según el enunciado)
    cita.estado = 'CANCELADA'
    
    nueva_cita = Cita(
        fecha=nueva_fecha,
        motivo=nuevo_motivo,
        estado='PROGRAMADA',
        id_paciente=nuevo_id_paciente,
        id_doctor=nuevo_id_doctor,
        id_centro=nuevo_id_centro,
        id_user_registrado=current_user['id_user']
    )
    
    db.session.add(nueva_cita)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Cita modificada exitosamente',
        'cambio_realizado': True,
        'cita_anterior': cita.to_dict(),
        'cita_nueva': nueva_cita.to_dict()
    }), 200


@citas_bp.route('/<int:id_cita>', methods=['DELETE'])
@jwt_required()
def eliminar_cita(id_cita):
    """Eliminar una cita (solo admin)"""
    current_user = get_jwt_identity()
    
    if current_user['rol'] != 'admin':
        return jsonify({'error': 'Acceso denegado. Se requiere rol admin'}), 403
    
    cita = Cita.query.get(id_cita)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404
    
    db.session.delete(cita)
    db.session.commit()
    
    return jsonify({'mensaje': 'Cita eliminada exitosamente'}), 200
