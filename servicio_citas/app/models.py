from app import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id_cita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), default='PROGRAMADA')  # PROGRAMADA, COMPLETADA, CANCELADA
    id_paciente = db.Column(db.Integer, nullable=False)
    id_doctor = db.Column(db.Integer, nullable=False)
    id_centro = db.Column(db.Integer, nullable=False)
    id_user_registrado = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id_cita': self.id_cita,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'motivo': self.motivo,
            'estado': self.estado,
            'id_paciente': self.id_paciente,
            'id_doctor': self.id_doctor,
            'id_centro': self.id_centro,
            'id_user_registrado': self.id_user_registrado,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
