"""
Script cliente para carga inicial de datos del sistema OdontoCare.
Lee los archivos CSV y envía los registros a la API REST.
"""

import csv
import requests
from datetime import datetime, timedelta

# Configuración de URLs de los servicios
SERVICIO_USUARIOS_URL = "http://localhost:5000"
SERVICIO_CITAS_URL = "http://localhost:5001"

# Credenciales del admin
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"


def login(nombre_usuario, password):
    """Realiza login y retorna el token JWT"""
    url = f"{SERVICIO_USUARIOS_URL}/auth/login"
    payload = {
        "nombre_usuario": nombre_usuario,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Login exitoso para: {nombre_usuario}")
            return data.get('token')
        else:
            print(f"[ERROR] Error en login: {response.json()}")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion: {e}")
        return None


def get_headers(token):
    """Retorna headers con el token de autorización"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def cargar_usuarios(token, archivo_csv):
    """Carga usuarios desde archivo CSV"""
    print("\n" + "="*50)
    print("CARGANDO USUARIOS")
    print("="*50)
    
    url = f"{SERVICIO_USUARIOS_URL}/admin/usuario"
    registros_creados = 0
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Saltar el admin que ya existe
                if row['nombre_usuario'] == 'admin':
                    print(f"  [SKIP] Saltando usuario admin (ya existe)")
                    continue
                
                payload = {
                    "nombre_usuario": row['nombre_usuario'],
                    "password": row['password'],
                    "rol": row['rol']
                }
                
                response = requests.post(url, json=payload, headers=get_headers(token))
                
                if response.status_code == 201:
                    print(f"  [OK] Usuario creado: {row['nombre_usuario']}")
                    registros_creados += 1
                elif response.status_code == 409:
                    print(f"  [SKIP] Usuario ya existe: {row['nombre_usuario']}")
                else:
                    print(f"  [ERROR] Error creando usuario {row['nombre_usuario']}: {response.json()}")
    
    except FileNotFoundError:
        print(f"  [ERROR] Archivo no encontrado: {archivo_csv}")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
    
    print(f"\nTotal usuarios creados: {registros_creados}")
    return registros_creados


def cargar_doctores(token, archivo_csv):
    """Carga doctores desde archivo CSV"""
    print("\n" + "="*50)
    print("CARGANDO DOCTORES")
    print("="*50)
    
    url = f"{SERVICIO_USUARIOS_URL}/admin/doctores"
    registros_creados = 0
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                payload = {
                    "nombre": row['nombre'],
                    "especialidad": row['especialidad'],
                    "nombre_usuario": row['nombre_usuario'],
                    "password": row['password']
                }
                
                response = requests.post(url, json=payload, headers=get_headers(token))
                
                if response.status_code == 201:
                    print(f"  [OK] Doctor creado: {row['nombre']}")
                    registros_creados += 1
                elif response.status_code == 409:
                    print(f"  [SKIP] Doctor ya existe: {row['nombre']}")
                else:
                    print(f"  [ERROR] Error creando doctor {row['nombre']}: {response.json()}")
    
    except FileNotFoundError:
        print(f"  [ERROR] Archivo no encontrado: {archivo_csv}")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
    
    print(f"\nTotal doctores creados: {registros_creados}")
    return registros_creados


def cargar_pacientes(token, archivo_csv):
    """Carga pacientes desde archivo CSV"""
    print("\n" + "="*50)
    print("CARGANDO PACIENTES")
    print("="*50)
    
    url = f"{SERVICIO_USUARIOS_URL}/admin/pacientes"
    registros_creados = 0
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                payload = {
                    "nombre": row['nombre'],
                    "telefono": row['telefono'],
                    "estado": row['estado'],
                    "nombre_usuario": row['nombre_usuario'],
                    "password": row['password']
                }
                
                response = requests.post(url, json=payload, headers=get_headers(token))
                
                if response.status_code == 201:
                    print(f"  [OK] Paciente creado: {row['nombre']}")
                    registros_creados += 1
                elif response.status_code == 409:
                    print(f"  [SKIP] Paciente ya existe: {row['nombre']}")
                else:
                    print(f"  [ERROR] Error creando paciente {row['nombre']}: {response.json()}")
    
    except FileNotFoundError:
        print(f"  [ERROR] Archivo no encontrado: {archivo_csv}")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
    
    print(f"\nTotal pacientes creados: {registros_creados}")
    return registros_creados


def cargar_centros(token, archivo_csv):
    """Carga centros médicos desde archivo CSV"""
    print("\n" + "="*50)
    print("CARGANDO CENTROS MÉDICOS")
    print("="*50)
    
    url = f"{SERVICIO_USUARIOS_URL}/admin/centros"
    registros_creados = 0
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                payload = {
                    "nombre": row['nombre'],
                    "direccion": row['direccion']
                }
                
                response = requests.post(url, json=payload, headers=get_headers(token))
                
                if response.status_code == 201:
                    print(f"  [OK] Centro creado: {row['nombre']}")
                    registros_creados += 1
                else:
                    print(f"  [ERROR] Error creando centro {row['nombre']}: {response.json()}")
    
    except FileNotFoundError:
        print(f"  [ERROR] Archivo no encontrado: {archivo_csv}")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
    
    print(f"\nTotal centros creados: {registros_creados}")
    return registros_creados


def crear_cita_ejemplo(token):
    """Crea una cita médica de ejemplo"""
    print("\n" + "="*50)
    print("CREANDO CITA MÉDICA DE EJEMPLO")
    print("="*50)
    
    url = f"{SERVICIO_CITAS_URL}/citas"
    
    # Fecha para mañana a las 10:00
    fecha_cita = (datetime.now() + timedelta(days=1)).replace(
        hour=10, minute=0, second=0, microsecond=0
    )
    
    payload = {
        "id_paciente": 1,
        "id_doctor": 1,
        "id_centro": 1,
        "fecha": fecha_cita.isoformat(),
        "motivo": "Revisión dental general y limpieza"
    }
    
    try:
        response = requests.post(url, json=payload, headers=get_headers(token))
        
        if response.status_code == 201:
            cita = response.json()
            print("\n[OK] CITA CREADA EXITOSAMENTE")
            print("\n" + "-"*40)
            print("JSON DE LA CITA CREADA:")
            print("-"*40)
            import json
            print(json.dumps(cita, indent=2, ensure_ascii=False))
            return cita
        else:
            print(f"[ERROR] Error creando cita: {response.json()}")
            return None
    
    except requests.RequestException as e:
        print(f"[ERROR] Error de conexion con servicio de citas: {e}")
        return None


def main():
    """Función principal del script de carga inicial"""
    print("\n" + "="*60)
    print("   SISTEMA ODONTOCARE - CARGA INICIAL DE DATOS")
    print("="*60)
    
    # 1. Login con usuario admin
    print("\n[1] Realizando login con usuario admin...")
    token = login(ADMIN_USER, ADMIN_PASSWORD)
    
    if not token:
        print("\n[ERROR] No se pudo obtener el token. Abortando carga.")
        return
    
    # 2. Cargar usuarios
    print("\n[2] Cargando usuarios...")
    cargar_usuarios(token, "datos/usuarios.csv")
    
    # 3. Cargar doctores
    print("\n[3] Cargando doctores...")
    cargar_doctores(token, "datos/doctores.csv")
    
    # 4. Cargar pacientes
    print("\n[4] Cargando pacientes...")
    cargar_pacientes(token, "datos/pacientes.csv")
    
    # 5. Cargar centros
    print("\n[5] Cargando centros médicos...")
    cargar_centros(token, "datos/centros.csv")
    
    # 6. Crear cita de ejemplo
    print("\n[6] Creando cita médica de ejemplo...")
    crear_cita_ejemplo(token)
    
    print("\n" + "="*60)
    print("   CARGA INICIAL COMPLETADA")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
