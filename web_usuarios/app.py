"""
Aplicación Web para Mantenimiento de Usuarios - Sistema OdontoCare
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from functools import wraps
import csv
import io

app = Flask(__name__)
app.secret_key = 'odontocare-web-usuarios-secret-2024'

# URL del servicio de usuarios
SERVICIO_USUARIOS_URL = "http://localhost:5000"


def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorador para requerir rol admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for('login'))
        if session.get('usuario', {}).get('rol') != 'admin':
            flash('Acceso denegado. Se requiere rol de administrador', 'danger')
            return redirect(url_for('dashboard'))
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
        return redirect(url_for('dashboard'))
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
                return redirect(url_for('dashboard'))
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


@app.route('/dashboard')
@login_required
def dashboard():
    """Panel principal"""
    stats = {'usuarios': 0, 'doctores': 0, 'pacientes': 0, 'centros': 0}
    
    try:
        usuarios_resp = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/usuarios", headers=get_headers())
        if usuarios_resp.status_code == 200:
            stats['usuarios'] = usuarios_resp.json().get('total', 0)
        
        doctores_resp = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/doctores", headers=get_headers())
        if doctores_resp.status_code == 200:
            stats['doctores'] = doctores_resp.json().get('total', 0)
        
        pacientes_resp = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/pacientes", headers=get_headers())
        if pacientes_resp.status_code == 200:
            stats['pacientes'] = pacientes_resp.json().get('total', 0)
        
        centros_resp = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/centros", headers=get_headers())
        if centros_resp.status_code == 200:
            stats['centros'] = centros_resp.json().get('total', 0)
    except:
        pass
    
    return render_template('dashboard.html', stats=stats)


# ==================== USUARIOS ====================

@app.route('/usuarios')
@admin_required
def usuarios():
    """Listado de usuarios"""
    try:
        response = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/usuarios", headers=get_headers())
        usuarios_data = response.json().get('usuarios', []) if response.status_code == 200 else []
    except:
        usuarios_data = []
    
    return render_template('usuarios.html', usuarios=usuarios_data)


@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_usuario():
    """Crear nuevo usuario (admin, secretaria, medico o paciente)"""
    if request.method == 'POST':
        try:
            rol = request.form.get('rol')
            nombre_usuario = request.form.get('nombre_usuario')
            password = request.form.get('password')
            
            if rol == 'medico':
                # Crear doctor con usuario
                payload = {
                    'nombre': request.form.get('nombre_doctor'),
                    'especialidad': request.form.get('especialidad'),
                    'nombre_usuario': nombre_usuario,
                    'password': password
                }
                response = requests.post(
                    f"{SERVICIO_USUARIOS_URL}/admin/doctores",
                    headers=get_headers(),
                    json=payload
                )
                if response.status_code == 201:
                    flash('Doctor creado exitosamente con acceso al sistema', 'success')
                    return redirect(url_for('doctores'))
                else:
                    error = response.json().get('error', 'Error al crear el doctor')
                    flash(error, 'danger')
                    
            elif rol == 'paciente':
                # Crear paciente con usuario
                payload = {
                    'nombre': request.form.get('nombre_paciente'),
                    'telefono': request.form.get('telefono'),
                    'estado': request.form.get('estado', 'ACTIVO'),
                    'nombre_usuario': nombre_usuario,
                    'password': password
                }
                response = requests.post(
                    f"{SERVICIO_USUARIOS_URL}/admin/pacientes",
                    headers=get_headers(),
                    json=payload
                )
                if response.status_code == 201:
                    flash('Paciente creado exitosamente con acceso al sistema', 'success')
                    return redirect(url_for('pacientes'))
                else:
                    error = response.json().get('error', 'Error al crear el paciente')
                    flash(error, 'danger')
            else:
                # Crear usuario normal (admin o secretaria)
                payload = {
                    'nombre_usuario': nombre_usuario,
                    'password': password,
                    'rol': rol
                }
                response = requests.post(
                    f"{SERVICIO_USUARIOS_URL}/admin/usuario",
                    headers=get_headers(),
                    json=payload
                )
                if response.status_code == 201:
                    flash('Usuario creado exitosamente', 'success')
                    return redirect(url_for('usuarios'))
                else:
                    error = response.json().get('error', 'Error al crear el usuario')
                    flash(error, 'danger')
                    
        except requests.RequestException as e:
            flash(f'Error de conexion: {str(e)}', 'danger')
    
    return render_template('nuevo_usuario.html')


# ==================== DOCTORES ====================

@app.route('/doctores')
@login_required
def doctores():
    """Listado de doctores"""
    try:
        response = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/doctores", headers=get_headers())
        doctores_data = response.json().get('doctores', []) if response.status_code == 200 else []
    except:
        doctores_data = []
    
    return render_template('doctores.html', doctores=doctores_data)


@app.route('/doctores/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_doctor():
    """Crear nuevo doctor"""
    if request.method == 'POST':
        try:
            payload = {
                'nombre': request.form.get('nombre'),
                'especialidad': request.form.get('especialidad'),
                'nombre_usuario': request.form.get('nombre_usuario'),
                'password': request.form.get('password')
            }
            
            response = requests.post(
                f"{SERVICIO_USUARIOS_URL}/admin/doctores",
                headers=get_headers(),
                json=payload
            )
            
            if response.status_code == 201:
                flash('Doctor creado exitosamente', 'success')
                return redirect(url_for('doctores'))
            else:
                error = response.json().get('error', 'Error al crear el doctor')
                flash(error, 'danger')
        except requests.RequestException as e:
            flash(f'Error de conexión: {str(e)}', 'danger')
    
    return render_template('nuevo_doctor.html')


# ==================== PACIENTES ====================

@app.route('/pacientes')
@login_required
def pacientes():
    """Listado de pacientes"""
    try:
        response = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/pacientes", headers=get_headers())
        pacientes_data = response.json().get('pacientes', []) if response.status_code == 200 else []
    except:
        pacientes_data = []
    
    return render_template('pacientes.html', pacientes=pacientes_data)


@app.route('/pacientes/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_paciente():
    """Crear nuevo paciente"""
    if request.method == 'POST':
        try:
            payload = {
                'nombre': request.form.get('nombre'),
                'telefono': request.form.get('telefono'),
                'estado': request.form.get('estado', 'ACTIVO'),
                'nombre_usuario': request.form.get('nombre_usuario'),
                'password': request.form.get('password')
            }
            
            response = requests.post(
                f"{SERVICIO_USUARIOS_URL}/admin/pacientes",
                headers=get_headers(),
                json=payload
            )
            
            if response.status_code == 201:
                flash('Paciente creado exitosamente', 'success')
                return redirect(url_for('pacientes'))
            else:
                error = response.json().get('error', 'Error al crear el paciente')
                flash(error, 'danger')
        except requests.RequestException as e:
            flash(f'Error de conexión: {str(e)}', 'danger')
    
    return render_template('nuevo_paciente.html')


# ==================== CENTROS ====================

@app.route('/centros')
@login_required
def centros():
    """Listado de centros"""
    try:
        response = requests.get(f"{SERVICIO_USUARIOS_URL}/admin/centros", headers=get_headers())
        centros_data = response.json().get('centros', []) if response.status_code == 200 else []
    except:
        centros_data = []
    
    return render_template('centros.html', centros=centros_data)


@app.route('/centros/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_centro():
    """Crear nuevo centro"""
    if request.method == 'POST':
        try:
            payload = {
                'nombre': request.form.get('nombre'),
                'direccion': request.form.get('direccion')
            }
            
            response = requests.post(
                f"{SERVICIO_USUARIOS_URL}/admin/centros",
                headers=get_headers(),
                json=payload
            )
            
            if response.status_code == 201:
                flash('Centro creado exitosamente', 'success')
                return redirect(url_for('centros'))
            else:
                error = response.json().get('error', 'Error al crear el centro')
                flash(error, 'danger')
        except requests.RequestException as e:
            flash(f'Error de conexión: {str(e)}', 'danger')
    
    return render_template('nuevo_centro.html')


# ==================== CARGA MASIVA CSV ====================

@app.route('/carga-masiva')
@admin_required
def carga_masiva():
    """Pagina de carga masiva desde CSV"""
    return render_template('carga_masiva.html')


@app.route('/carga-masiva/procesar', methods=['POST'])
@admin_required
def procesar_carga_masiva():
    """Procesar archivo CSV y cargar registros"""
    tipo = request.form.get('tipo')
    archivo = request.files.get('archivo_csv')
    
    if not archivo or not tipo:
        flash('Debe seleccionar un tipo y un archivo CSV', 'danger')
        return redirect(url_for('carga_masiva'))
    
    try:
        # Leer el archivo CSV
        stream = io.StringIO(archivo.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        
        creados = 0
        errores = 0
        mensajes_error = []
        
        for row in reader:
            try:
                if tipo == 'usuarios':
                    payload = {
                        'nombre_usuario': row.get('nombre_usuario'),
                        'password': row.get('password'),
                        'rol': row.get('rol')
                    }
                    response = requests.post(
                        f"{SERVICIO_USUARIOS_URL}/admin/usuario",
                        headers=get_headers(),
                        json=payload
                    )
                    
                elif tipo == 'doctores':
                    payload = {
                        'nombre': row.get('nombre'),
                        'especialidad': row.get('especialidad'),
                        'nombre_usuario': row.get('nombre_usuario', ''),
                        'password': row.get('password', '')
                    }
                    response = requests.post(
                        f"{SERVICIO_USUARIOS_URL}/admin/doctores",
                        headers=get_headers(),
                        json=payload
                    )
                    
                elif tipo == 'pacientes':
                    payload = {
                        'nombre': row.get('nombre'),
                        'telefono': row.get('telefono'),
                        'estado': row.get('estado', 'ACTIVO'),
                        'nombre_usuario': row.get('nombre_usuario', ''),
                        'password': row.get('password', '')
                    }
                    response = requests.post(
                        f"{SERVICIO_USUARIOS_URL}/admin/pacientes",
                        headers=get_headers(),
                        json=payload
                    )
                    
                elif tipo == 'centros':
                    payload = {
                        'nombre': row.get('nombre'),
                        'direccion': row.get('direccion')
                    }
                    response = requests.post(
                        f"{SERVICIO_USUARIOS_URL}/admin/centros",
                        headers=get_headers(),
                        json=payload
                    )
                else:
                    flash('Tipo de carga no valido', 'danger')
                    return redirect(url_for('carga_masiva'))
                
                if response.status_code == 201:
                    creados += 1
                elif response.status_code == 409:
                    errores += 1
                    mensajes_error.append(f"Duplicado: {row.get('nombre_usuario') or row.get('nombre')}")
                else:
                    errores += 1
                    mensajes_error.append(f"Error: {row.get('nombre_usuario') or row.get('nombre')}")
                    
            except Exception as e:
                errores += 1
                mensajes_error.append(str(e))
        
        flash(f'Carga completada: {creados} registros creados, {errores} errores', 
              'success' if errores == 0 else 'warning')
        
        if mensajes_error and len(mensajes_error) <= 5:
            for msg in mensajes_error:
                flash(msg, 'info')
                
    except Exception as e:
        flash(f'Error procesando archivo: {str(e)}', 'danger')
    
    return redirect(url_for('carga_masiva'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
