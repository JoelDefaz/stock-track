from django.test import TestCase
from django.urls import reverse
from usuarios.models import UsuarioPersonalizado

class TestUrls(TestCase):

    def setUp(self):
        self.user = UsuarioPersonalizado.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='password',
            nombres='John',
            apellidos='Doe',
            telefono='1234567890'
        )

    def test_get_login_url(self):
        url = reverse('usuarios:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_get_signup_url(self):
        url = reverse('usuarios:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_crear_cuenta_url(self):
        url = reverse('usuarios:crearCuenta')
        response = self.client.post(url, {
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo@gmail.com',
            'telefono': '9876543210',
            'password': 'nuevacontraseña'
        })
        self.assertEqual(response.status_code, 302)

    def test_iniciar_sesion_url(self):
        url = reverse('usuarios:iniciarSesion')
        response = self.client.post(url, {
            'email': self.user.email,
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_url(self):
        self.client.login(username='testuser', password='password')
        url = reverse('usuarios:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inicio'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_perfil_url(self):
        self.client.login(username=self.user.username, password='password')
        url = reverse('usuarios:perfil')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 

    def test_update_perfil_url(self):
        self.client.login(username=self.user.username, password='password')
        url = reverse('usuarios:updatePerfil')
        response = self.client.post(url, {
            'nombre': 'Usuario Actualizado',
            'email': self.user.email,
            'telefono': '1234567899',
            'contraseña_actual': 'password',
            'nueva_contraseña': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
