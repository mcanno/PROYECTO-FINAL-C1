"""
Aplicación Web para Administración de Citas - Sistema OdontoCare
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'odontocare-web-citas-secret-2024'

# URLs de los servicios backend
SERVICIO_USUARIOS_URL = "http://localhost:5000"
SERVICIO_CITAS_URL = "http://localhost:5001"


def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_headers():
    """Obtiene headers con token de autorización"""
    return {
        'Authorization': f"Bearer {session.get('token', '')}",
        'Content-Type': 'application/json'
    }


@app.route('/')
def index():
    """Página principal"""
    if 'token' in session:
        return redirect(url_for('citas'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f"{SERVICIO_USUARIOS_URL}/auth/login",
                json={'nombre_usuario': nombre_usuario, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                session['token'] = data['token']
                session['usuario'] = data['usuario']
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('citas'))
            else:
                flash('Credenciales inválidas', 'danger')
        except requests.RequestException:
            flash('Error de conexión con el servidor', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))


@app.route('/citas')
@login_required
def citas():
    """Listado de citas"""
    try:
        # Obtener filtros
        filtros = {}
        if request.args.get('id_doctor'):
            filtros['id_doctor'] = request.args.get('id_doctor')
        if request.args.get('id_paciente'):
            filtros['id_paciente'] = request.args.get('id_paciente')
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('fecha'):
            filtros['fecha'] = request.args.get('fecha')
        
        # Obtener citas
        response = requests.get(
            f"{SERVICIO_CITAS_URL}/citas",
            headers=get_headers(),
            params=filtros
        )
        
        citas_data = []
        if response.status_code == 200:
            citas_data = response.json().get('citas', [])
        
        # Obtener doctores para el filtro
        doctores_response = requests.get(
            f"{SERVICIO_USUARIOS_URL}/admin/doctores",
            headers=get_headers()
        )
        doctores = doctores_response.json().get('doctores', []) if doctores_response.status_code == 200 else []
        
        # Obtener pacientes para el filtro
        pacientes_response = requests.get(
            f"{SERVICIO_USUARIOS_URL}/admin/pacientes",
            headers=get_headers()
        )
        pacientes = pacientes_response.json().get('pacientes', []) if pacientes_response.status_code == 200 else []
        
        return render_template('citas.html', 
                             citas=citas_data, 
                             doctores=doctores,
                             pacientes=pacientes,
                             filtros=filtros)
    
    except requests.RequestException as e:
        flash(f'Error de conexión: {str(e)}', 'danger')
        return render_template('citas.html', citas=[], doctores=[], pacientes=[], filtros={})


@app.route('/citas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_cita():
    """Crear nueva cita"""
    if request.method == 'POST':
        try:
            payload = {
                'id_paciente': int(request.form.get('id_paciente')),
                'id_doctor': int(request.form.get('id_doctor')),
                'id_centro': int(request.form.get('id_centro')),
                'fecha': request.form.get('fecha'),
                'motivo': request.form.get('motivo')
            }
            
            response = requests.post(
                f"{SERVICIO_CITAS_URL}/citas",
                headers=get_headers(),
                json=payload
            )
            
            if response.status_code == 201:
                flash('Cita creada exitosamente', 'success')
                return redirect(url_for('citas'))
            else:
                error = response.json().get('error', 'Error al crear la cita')
                flash(error, 'danger')
        
        except requests.RequestException as e:
            flash(f'Error de conexión: {str(e)}', 'danger')
    
    # Obtener datos para los selectores
    try:
        doctores = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/doctores", headers=get_headers()).json().get('doctores', [])
        pacientes = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/pacientes", headers=get_headers()).json().get('pacientes', [])
        centros = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/centros", headers=get_headers()).json().get('centros', [])
    except:
        doctores, pacientes, centros = [], [], []
    
    return render_template('nueva_cita.html', doctores=doctores, pacientes=pacientes, centros=centros)


@app.route('/citas/<int:id_cita>/cancelar', methods=['POST'])
@login_required
def cancelar_cita(id_cita):
    """Cancelar una cita"""
    try:
        response = requests.put(
            f"{SERVICIO_CITAS_URL}/citas/{id_cita}/cancelar",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            flash('Cita cancelada exitosamente', 'success')
        else:
            error = response.json().get('error', 'Error al cancelar la cita')
            flash(error, 'danger')
    
    except requests.RequestException as e:
        flash(f'Error de conexión: {str(e)}', 'danger')
    
    return redirect(url_for('citas'))


@app.route('/citas/<int:id_cita>/editar', methods=['GET', 'POST'])
@login_required
def editar_cita(id_cita):
    """Editar una cita"""
    if request.method == 'POST':
        try:
            payload = {
                'id_paciente': int(request.form.get('id_paciente')),
                'id_doctor': int(request.form.get('id_doctor')),
                'id_centro': int(request.form.get('id_centro')),
                'fecha': request.form.get('fecha'),
                'motivo': request.form.get('motivo')
            }
            
            response = requests.put(
                f"{SERVICIO_CITAS_URL}/citas/{id_cita}",
                headers=get_headers(),
                json=payload
            )
            
            if response.status_code == 200:
                flash('Cita modificada exitosamente', 'success')
                return redirect(url_for('citas'))
            else:
                error = response.json().get('error', 'Error al modificar la cita')
                flash(error, 'danger')
        
        except requests.RequestException as e:
            flash(f'Error de conexión: {str(e)}', 'danger')
    
    # Obtener datos de la cita
    try:
        cita_response = requests.get(f"{SERVICIO_CITAS_URL}/citas/{id_cita}", headers=get_headers())
        cita = cita_response.json() if cita_response.status_code == 200 else None
        
        doctores = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/doctores", headers=get_headers()).json().get('doctores', [])
        pacientes = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/pacientes", headers=get_headers()).json().get('pacientes', [])
        centros = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/centros", headers=get_headers()).json().get('centros', [])
    except:
        cita, doctores, pacientes, centros = None, [], [], []
    
    if not cita:
        flash('Cita no encontrada', 'danger')
        return redirect(url_for('citas'))
    
    return render_template('editar_cita.html', cita=cita, doctores=doctores, pacientes=pacientes, centros=centros)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
