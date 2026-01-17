# Sistema OdontoCare

Sistema de gestión de citas para una red de clínicas dentales, implementado con arquitectura de microservicios.

## Arquitectura

El sistema está compuesto por dos microservicios independientes:

### 1. Servicio de Usuarios (Puerto 5000)
- **auth_bp**: Autenticación y gestión de tokens JWT
- **admin_bp**: Gestión de usuarios, doctores, pacientes y centros médicos

### 2. Servicio de Citas (Puerto 5001)
- **citas_bp**: Gestión operativa de citas médicas
- Se comunica con el servicio de usuarios via REST para validaciones

## Tecnologías Utilizadas

- **Backend**: Flask 3.0
- **ORM**: SQLAlchemy
- **Base de Datos**: SQLite
- **Autenticación**: JWT (Flask-JWT-Extended)
- **Contenedores**: Docker

## Estructura del Proyecto

```
PROYECTO-FINAL-C1/
├── servicio_usuarios/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── blueprints/
│   │       ├── auth.py
│   │       └── admin.py
│   ├── run.py
│   ├── requirements.txt
│   └── Dockerfile
├── servicio_citas/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── blueprints/
│   │       └── citas.py
│   ├── run.py
│   ├── requirements.txt
│   └── Dockerfile
├── datos/
│   ├── usuarios.csv
│   ├── doctores.csv
│   ├── pacientes.csv
│   └── centros.csv
├── carga_inicial.py
├── docker-compose.yml
└── README.md
```

## Instalación y Ejecución

### Opción 1: Docker (Recomendado)

```bash
# Construir y levantar los servicios
docker-compose up --build

# En otra terminal, ejecutar la carga inicial
python carga_inicial.py
```

### Opción 2: Ejecución Local

```bash
# Terminal 1 - Servicio de Usuarios
cd servicio_usuarios
pip install -r requirements.txt
python run.py

# Terminal 2 - Servicio de Citas
cd servicio_citas
pip install -r requirements.txt
python run.py

# Terminal 3 - Carga inicial de datos
python carga_inicial.py
```

## Endpoints de la API

### Autenticación (auth_bp)

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Iniciar sesión | Público |
| POST | `/auth/registro` | Registrar usuario | Admin |
| GET | `/auth/verificar` | Verificar token | Autenticado |

### Administración (admin_bp)

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| POST | `/admin/usuario` | Crear usuario | Admin |
| GET | `/admin/usuarios` | Listar usuarios | Admin |
| POST | `/admin/doctores` | Crear doctor | Admin |
| GET | `/admin/doctores` | Listar doctores | Autenticado |
| GET | `/admin/doctores/<id>` | Obtener doctor | Autenticado |
| POST | `/admin/pacientes` | Crear paciente | Admin |
| GET | `/admin/pacientes` | Listar pacientes | Autenticado |
| GET | `/admin/pacientes/<id>` | Obtener paciente | Autenticado |
| POST | `/admin/centros` | Crear centro | Admin |
| GET | `/admin/centros` | Listar centros | Autenticado |
| GET | `/admin/centros/<id>` | Obtener centro | Autenticado |

### Citas (citas_bp)

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| POST | `/citas` | Crear cita | Admin, Paciente, Secretaria |
| GET | `/citas` | Listar citas (con filtros) | Autenticado |
| GET | `/citas/<id>` | Obtener cita | Autenticado |
| PUT | `/citas/<id>` | Modificar cita | Admin, Paciente, Secretaria |
| PUT | `/citas/<id>/cancelar` | Cancelar cita | Admin, Paciente, Secretaria |
| DELETE | `/citas/<id>` | Eliminar cita | Admin |

## Ejemplos de Uso

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"nombre_usuario": "admin", "password": "admin123"}'
```

### Crear Cita
```bash
curl -X POST http://localhost:5001/citas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "id_paciente": 1,
    "id_doctor": 1,
    "id_centro": 1,
    "fecha": "2024-12-20T10:00:00",
    "motivo": "Revisión dental"
  }'
```

### Listar Citas (Admin con filtros)
```bash
curl -X GET "http://localhost:5001/citas?id_doctor=1&estado=PROGRAMADA" \
  -H "Authorization: Bearer <TOKEN>"
```

## Modelo de Datos

### Usuario
- `id_user` (PK)
- `nombre_usuario`
- `password`
- `rol` (admin, medico, secretaria, paciente)

### Paciente
- `id_paciente` (PK)
- `id_user` (FK, opcional)
- `nombre`
- `telefono`
- `estado` (ACTIVO/INACTIVO)

### Doctor
- `id_doctor` (PK)
- `id_user` (FK, opcional)
- `nombre`
- `especialidad`

### Centro
- `id_centro` (PK)
- `nombre`
- `direccion`

### Cita
- `id_cita` (PK)
- `fecha`
- `motivo`
- `estado` (PROGRAMADA, COMPLETADA, CANCELADA)
- `id_paciente` (FK)
- `id_doctor` (FK)
- `id_centro` (FK)
- `id_user_registrado` (FK)

## Reglas de Negocio

1. **Doble reserva**: No se permite agendar una cita si el doctor ya tiene otra en la misma fecha y hora.
2. **Paciente activo**: Solo se pueden crear citas para pacientes con estado ACTIVO.
3. **Cancelación**: Al cancelar una cita, se cambia el estado a "CANCELADA".
4. **Modificación**: Al modificar una cita, se cancela la anterior y se crea una nueva.

## Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin123

## Autor

Proyecto Final - Escuela de Programación Python
