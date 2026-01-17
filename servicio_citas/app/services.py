import requests
from flask import current_app

class ServicioUsuarios:
    """Cliente para comunicarse con el servicio de usuarios via REST"""
    
    @staticmethod
    def _get_base_url():
        return current_app.config.get('SERVICIO_USUARIOS_URL', 'http://localhost:5000')
    
    @staticmethod
    def _get_headers(token):
        return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    @classmethod
    def verificar_doctor(cls, id_doctor, token):
        """Verifica si un doctor existe consultando el servicio de usuarios"""
        try:
            url = f"{cls._get_base_url()}/admin/doctores/{id_doctor}"
            response = requests.get(url, headers=cls._get_headers(token), timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {'existe': True, 'doctor': data}
            return {'existe': False, 'doctor': None}
        except requests.RequestException as e:
            return {'existe': False, 'error': str(e)}
    
    @classmethod
    def verificar_paciente(cls, id_paciente, token):
        """Verifica si un paciente existe y está activo"""
        try:
            url = f"{cls._get_base_url()}/admin/pacientes/{id_paciente}"
            response = requests.get(url, headers=cls._get_headers(token), timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'existe': True, 
                    'activo': data.get('estado') == 'ACTIVO',
                    'paciente': data
                }
            return {'existe': False, 'activo': False, 'paciente': None}
        except requests.RequestException as e:
            return {'existe': False, 'activo': False, 'error': str(e)}
    
    @classmethod
    def verificar_centro(cls, id_centro, token):
        """Verifica si un centro médico existe"""
        try:
            url = f"{cls._get_base_url()}/admin/centros/{id_centro}"
            response = requests.get(url, headers=cls._get_headers(token), timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {'existe': True, 'centro': data}
            return {'existe': False, 'centro': None}
        except requests.RequestException as e:
            return {'existe': False, 'error': str(e)}
    
    @classmethod
    def verificar_token(cls, token):
        """Verifica si el token es válido"""
        try:
            url = f"{cls._get_base_url()}/auth/verificar"
            response = requests.get(url, headers=cls._get_headers(token), timeout=5)
            if response.status_code == 200:
                return response.json()
            return {'valido': False}
        except requests.RequestException as e:
            return {'valido': False, 'error': str(e)}
