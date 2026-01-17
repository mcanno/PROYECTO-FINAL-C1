from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_user = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin, medico, secretaria, paciente
    
    # Relaciones
    paciente = db.relationship('Paciente', backref='usuario', uselist=False)
    doctor = db.relationship('Doctor', backref='usuario', uselist=False)
    
    def to_dict(self):
        return {
            'id_user': self.id_user,
            'nombre_usuario': self.nombre_usuario,
            'rol': self.rol
        }


class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id_paciente = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(10), default='ACTIVO')  # ACTIVO/INACTIVO
    
    def to_dict(self):
        return {
            'id_paciente': self.id_paciente,
            'id_user': self.id_user,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'estado': self.estado
        }


class Doctor(db.Model):
    __tablename__ = 'doctores'
    
    id_doctor = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'id_doctor': self.id_doctor,
            'id_user': self.id_user,
            'nombre': self.nombre,
            'especialidad': self.especialidad
        }


class Centro(db.Model):
    __tablename__ = 'centros'
    
    id_centro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id_centro': self.id_centro,
            'nombre': self.nombre,
            'direccion': self.direccion
        }
