# Documentación de Endpoints - Sistema OdontoCare

## Servicio de Usuarios (Puerto 5000)

---

### POST /auth/login
**Descripción**: Inicio de sesión y obtención de token JWT

**Archivo de Entrada (JSON)**:
```json
{
    "nombre_usuario": "admin",
    "password": "admin123"
}
```

**Respuesta Exitosa (200)**:
```json
{
    "mensaje": "Login exitoso",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "usuario": {
        "id_user": 1,
        "nombre_usuario": "admin",
        "rol": "admin"
    }
}
```

---

### POST /auth/registro
**Descripción**: Registro de nuevos usuarios (solo admin)

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "nombre_usuario": "nuevo_usuario",
    "password": "password123",
    "rol": "secretaria"
}
```

**Respuesta Exitosa (201)**:
```json
{
    "mensaje": "Usuario registrado exitosamente",
    "usuario": {
        "id_user": 5,
        "nombre_usuario": "nuevo_usuario",
        "rol": "secretaria"
    }
}
```

---

### GET /auth/verificar
**Descripción**: Verificar validez del token

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "valido": true,
    "usuario": {
        "id_user": 1,
        "nombre_usuario": "admin",
        "rol": "admin"
    }
}
```

---

### POST /admin/usuario
**Descripción**: Crear un nuevo usuario

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "nombre_usuario": "secretaria3",
    "password": "secre789",
    "rol": "secretaria"
}
```

**Respuesta Exitosa (201)**:
```json
{
    "mensaje": "Usuario creado exitosamente",
    "usuario": {
        "id_user": 6,
        "nombre_usuario": "secretaria3",
        "rol": "secretaria"
    }
}
```

---

### GET /admin/usuarios
**Descripción**: Listar todos los usuarios

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "total": 3,
    "usuarios": [
        {"id_user": 1, "nombre_usuario": "admin", "rol": "admin"},
        {"id_user": 2, "nombre_usuario": "secretaria1", "rol": "secretaria"},
        {"id_user": 3, "nombre_usuario": "secretaria2", "rol": "secretaria"}
    ]
}
```

---

### POST /admin/doctores
**Descripción**: Crear un nuevo doctor

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "nombre": "Dr. Carlos García López",
    "especialidad": "Odontología General",
    "nombre_usuario": "dr.garcia",
    "password": "doc123"
}
```

**Respuesta Exitosa (201)**:
```json
{
    "mensaje": "Doctor creado exitosamente",
    "doctor": {
        "id_doctor": 1,
        "id_user": 4,
        "nombre": "Dr. Carlos García López",
        "especialidad": "Odontología General"
    }
}
```

---

### GET /admin/doctores
**Descripción**: Listar todos los doctores

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "total": 2,
    "doctores": [
        {"id_doctor": 1, "id_user": 4, "nombre": "Dr. Carlos García López", "especialidad": "Odontología General"},
        {"id_doctor": 2, "id_user": 5, "nombre": "Dra. María Fernández Ruiz", "especialidad": "Ortodoncia"}
    ]
}
```

---

### GET /admin/doctores/{id_doctor}
**Descripción**: Obtener un doctor por ID

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "id_doctor": 1,
    "id_user": 4,
    "nombre": "Dr. Carlos García López",
    "especialidad": "Odontología General",
    "existe": true
}
```

---

### POST /admin/pacientes
**Descripción**: Crear un nuevo paciente

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "nombre": "Juan Pérez Martínez",
    "telefono": "612345678",
    "estado": "ACTIVO",
    "nombre_usuario": "paciente.juan",
    "password": "pac123"
}
```

**Respuesta Exitosa (201)**:
```json
{
    "mensaje": "Paciente creado exitosamente",
    "paciente": {
        "id_paciente": 1,
        "id_user": 10,
        "nombre": "Juan Pérez Martínez",
        "telefono": "612345678",
        "estado": "ACTIVO"
    }
}
```

---

### GET /admin/pacientes
**Descripción**: Listar todos los pacientes

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "total": 2,
    "pacientes": [
        {"id_paciente": 1, "id_user": 10, "nombre": "Juan Pérez Martínez", "telefono": "612345678", "estado": "ACTIVO"},
        {"id_paciente": 2, "id_user": 11, "nombre": "María García López", "telefono": "623456789", "estado": "ACTIVO"}
    ]
}
```

---

### GET /admin/pacientes/{id_paciente}
**Descripción**: Obtener un paciente por ID

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "id_paciente": 1,
    "id_user": 10,
    "nombre": "Juan Pérez Martínez",
    "telefono": "612345678",
    "estado": "ACTIVO",
    "existe": true,
    "activo": true
}
```

---

### POST /admin/centros
**Descripción**: Crear un nuevo centro médico

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "nombre": "Clínica Dental OdontoCare Centro",
    "direccion": "Calle Mayor 15 - 28001 Madrid"
}
```

**Respuesta Exitosa (201)**:
```json
{
    "mensaje": "Centro creado exitosamente",
    "centro": {
        "id_centro": 1,
        "nombre": "Clínica Dental OdontoCare Centro",
        "direccion": "Calle Mayor 15 - 28001 Madrid"
    }
}
```

---

### GET /admin/centros
**Descripción**: Listar todos los centros

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "total": 2,
    "centros": [
        {"id_centro": 1, "nombre": "Clínica Dental OdontoCare Centro", "direccion": "Calle Mayor 15 - 28001 Madrid"},
        {"id_centro": 2, "nombre": "Clínica Dental OdontoCare Norte", "direccion": "Avenida de la Paz 42 - 28002 Madrid"}
    ]
}
```

---

### GET /admin/centros/{id_centro}
**Descripción**: Obtener un centro por ID

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "id_centro": 1,
    "nombre": "Clínica Dental OdontoCare Centro",
    "direccion": "Calle Mayor 15 - 28001 Madrid",
    "existe": true
}
```

---

## Servicio de Citas (Puerto 5001)

---

### POST /citas
**Descripción**: Crear una nueva cita médica

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "id_paciente": 1,
    "id_doctor": 1,
    "id_centro": 1,
    "fecha": "2024-12-20T10:00:00",
    "motivo": "Revisión dental general y limpieza"
}
```

**Respuesta Exitosa (201)**:
```json
{
    "mensaje": "Cita creada exitosamente",
    "cita": {
        "id_cita": 1,
        "fecha": "2024-12-20T10:00:00",
        "motivo": "Revisión dental general y limpieza",
        "estado": "PROGRAMADA",
        "id_paciente": 1,
        "id_doctor": 1,
        "id_centro": 1,
        "id_user_registrado": 1,
        "created_at": "2024-12-19T15:30:00"
    }
}
```

---

### GET /citas
**Descripción**: Listar citas con filtros según rol

**Headers**: `Authorization: Bearer <token>`

**Query Parameters** (según rol):
- Admin: `id_doctor`, `id_centro`, `id_paciente`, `estado`, `fecha`
- Secretaria: `fecha`
- Médico: `id_doctor`
- Paciente: `id_paciente`

**Ejemplo**: `GET /citas?id_doctor=1&estado=PROGRAMADA`

**Respuesta Exitosa (200)**:
```json
{
    "total": 2,
    "citas": [
        {
            "id_cita": 1,
            "fecha": "2024-12-20T10:00:00",
            "motivo": "Revisión dental",
            "estado": "PROGRAMADA",
            "id_paciente": 1,
            "id_doctor": 1,
            "id_centro": 1,
            "id_user_registrado": 1,
            "created_at": "2024-12-19T15:30:00"
        }
    ]
}
```

---

### GET /citas/{id_cita}
**Descripción**: Obtener una cita por ID

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "id_cita": 1,
    "fecha": "2024-12-20T10:00:00",
    "motivo": "Revisión dental general y limpieza",
    "estado": "PROGRAMADA",
    "id_paciente": 1,
    "id_doctor": 1,
    "id_centro": 1,
    "id_user_registrado": 1,
    "created_at": "2024-12-19T15:30:00"
}
```

---

### PUT /citas/{id_cita}
**Descripción**: Modificar una cita existente

**Headers**: `Authorization: Bearer <token>`

**Archivo de Entrada (JSON)**:
```json
{
    "id_doctor": 2,
    "fecha": "2024-12-21T11:00:00",
    "motivo": "Consulta de ortodoncia"
}
```

**Respuesta Exitosa (200)**:
```json
{
    "mensaje": "Cita modificada exitosamente",
    "cambio_realizado": true,
    "cita_anterior": {
        "id_cita": 1,
        "estado": "CANCELADA",
        "...": "..."
    },
    "cita_nueva": {
        "id_cita": 2,
        "fecha": "2024-12-21T11:00:00",
        "estado": "PROGRAMADA",
        "...": "..."
    }
}
```

---

### PUT /citas/{id_cita}/cancelar
**Descripción**: Cancelar una cita existente

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "mensaje": "Cita cancelada exitosamente",
    "cita": {
        "id_cita": 1,
        "estado": "CANCELADA",
        "...": "..."
    }
}
```

---

### DELETE /citas/{id_cita}
**Descripción**: Eliminar una cita (solo admin)

**Headers**: `Authorization: Bearer <token>`

**Respuesta Exitosa (200)**:
```json
{
    "mensaje": "Cita eliminada exitosamente"
}
```

---

## Códigos de Error Comunes

| Código | Descripción |
|--------|-------------|
| 400 | Datos inválidos o faltantes |
| 401 | Credenciales inválidas |
| 403 | Acceso denegado (rol insuficiente) |
| 404 | Recurso no encontrado |
| 409 | Conflicto (usuario duplicado, doble reserva) |
