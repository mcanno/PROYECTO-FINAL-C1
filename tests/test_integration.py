"""
Pruebas de integración para el Sistema OdontoCare.
Valida la comunicación entre servicios y el acceso a endpoints.
"""

import unittest
import requests
import json

# URLs de los servicios
SERVICIO_USUARIOS_URL = "http://localhost:5000"
SERVICIO_CITAS_URL = "http://localhost:5001"


class TestAuthEndpoints(unittest.TestCase):
    """Pruebas para endpoints de autenticación"""
    
    def test_login_exitoso(self):
        """Test: Login con credenciales válidas"""
        url = f"{SERVICIO_USUARIOS_URL}/auth/login"
        payload = {
            "nombre_usuario": "admin",
            "password": "admin123"
        }
        
        response = requests.post(url, json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('usuario', data)
        self.assertEqual(data['usuario']['rol'], 'admin')
    
    def test_login_credenciales_invalidas(self):
        """Test: Login con credenciales inválidas"""
        url = f"{SERVICIO_USUARIOS_URL}/auth/login"
        payload = {
            "nombre_usuario": "admin",
            "password": "wrongpassword"
        }
        
        response = requests.post(url, json=payload)
        
        self.assertEqual(response.status_code, 401)
    
    def test_verificar_token(self):
        """Test: Verificar token válido"""
        # Primero obtener token
        login_url = f"{SERVICIO_USUARIOS_URL}/auth/login"
        login_payload = {"nombre_usuario": "admin", "password": "admin123"}
        login_response = requests.post(login_url, json=login_payload)
        token = login_response.json()['token']
        
        # Verificar token
        verify_url = f"{SERVICIO_USUARIOS_URL}/auth/verificar"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(verify_url, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['valido'])


class TestAdminEndpoints(unittest.TestCase):
    """Pruebas para endpoints de administración"""
    
    @classmethod
    def setUpClass(cls):
        """Obtener token de admin para las pruebas"""
        login_url = f"{SERVICIO_USUARIOS_URL}/auth/login"
        login_payload = {"nombre_usuario": "admin", "password": "admin123"}
        response = requests.post(login_url, json=login_payload)
        cls.token = response.json()['token']
        cls.headers = {"Authorization": f"Bearer {cls.token}", "Content-Type": "application/json"}
    
    def test_listar_doctores(self):
        """Test: Listar todos los doctores"""
        url = f"{SERVICIO_USUARIOS_URL}/admin/doctores"
        
        response = requests.get(url, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('doctores', data)
    
    def test_listar_pacientes(self):
        """Test: Listar todos los pacientes"""
        url = f"{SERVICIO_USUARIOS_URL}/admin/pacientes"
        
        response = requests.get(url, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('pacientes', data)
    
    def test_listar_centros(self):
        """Test: Listar todos los centros"""
        url = f"{SERVICIO_USUARIOS_URL}/admin/centros"
        
        response = requests.get(url, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('centros', data)
    
    def test_obtener_doctor_inexistente(self):
        """Test: Obtener doctor que no existe"""
        url = f"{SERVICIO_USUARIOS_URL}/admin/doctores/9999"
        
        response = requests.get(url, headers=self.headers)
        
        self.assertEqual(response.status_code, 404)


class TestCitasEndpoints(unittest.TestCase):
    """Pruebas para endpoints de citas"""
    
    @classmethod
    def setUpClass(cls):
        """Obtener token de admin para las pruebas"""
        login_url = f"{SERVICIO_USUARIOS_URL}/auth/login"
        login_payload = {"nombre_usuario": "admin", "password": "admin123"}
        response = requests.post(login_url, json=login_payload)
        cls.token = response.json()['token']
        cls.headers = {"Authorization": f"Bearer {cls.token}", "Content-Type": "application/json"}
    
    def test_listar_citas(self):
        """Test: Listar todas las citas"""
        url = f"{SERVICIO_CITAS_URL}/citas"
        
        response = requests.get(url, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('citas', data)
    
    def test_crear_cita_sin_datos(self):
        """Test: Crear cita sin datos requeridos"""
        url = f"{SERVICIO_CITAS_URL}/citas"
        payload = {}
        
        response = requests.post(url, json=payload, headers=self.headers)
        
        self.assertEqual(response.status_code, 400)
    
    def test_obtener_cita_inexistente(self):
        """Test: Obtener cita que no existe"""
        url = f"{SERVICIO_CITAS_URL}/citas/9999"
        
        response = requests.get(url, headers=self.headers)
        
        self.assertEqual(response.status_code, 404)


class TestComunicacionServicios(unittest.TestCase):
    """Pruebas de comunicación entre microservicios"""
    
    @classmethod
    def setUpClass(cls):
        """Obtener token de admin para las pruebas"""
        login_url = f"{SERVICIO_USUARIOS_URL}/auth/login"
        login_payload = {"nombre_usuario": "admin", "password": "admin123"}
        response = requests.post(login_url, json=login_payload)
        cls.token = response.json()['token']
        cls.headers = {"Authorization": f"Bearer {cls.token}", "Content-Type": "application/json"}
    
    def test_crear_cita_valida_doctor_inexistente(self):
        """Test: Crear cita con doctor inexistente (validación via REST)"""
        url = f"{SERVICIO_CITAS_URL}/citas"
        payload = {
            "id_paciente": 1,
            "id_doctor": 9999,  # Doctor que no existe
            "id_centro": 1,
            "fecha": "2025-12-20T10:00:00",
            "motivo": "Revisión"
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        
        # Debe fallar porque el servicio de citas consulta al servicio de usuarios
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('error', data)


def run_tests():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*60)
    print("   PRUEBAS DE INTEGRACIÓN - SISTEMA ODONTOCARE")
    print("="*60 + "\n")
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestAuthEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestAdminEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestCitasEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestComunicacionServicios))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()
