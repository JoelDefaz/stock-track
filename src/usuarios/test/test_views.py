from django.test import TestCase
from django.urls import reverse
from usuarios.models import UsuarioPersonalizado
from django.contrib.messages import get_messages

class TestUserViews(TestCase):

    def setUp(self):
        self.user = UsuarioPersonalizado.objects.create_user(
            nombres='Test',
            username='TestPrueba',
            email='test@example.com',
            telefono='123456789',
            password='password123'
        )

    # Prueba para iniciar sesión
    def test_login_success(self):
        response = self.client.post(reverse('usuarios:iniciarSesion'), {
            'email': 'test@example.com',
            'password': 'password123'
        })

        self.assertRedirects(response, '/compras/')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Inicio de sesión exitoso.')

    def test_update_profile_invalid_current_password(self):         
        self.client.force_login(self.user)
   
        update_response = self.client.post(reverse('usuarios:updatePerfil'), {
            'nombres': 'Updated Name',
            'email': 'test@example.com',
            'telefono': '987654321',
            'contraseña_actual': 'wrongpassword',
            'nueva_contraseña': 'newpassword123'
        })

        self.assertRedirects(update_response, reverse('usuarios:perfil'))
        messages = list(get_messages(update_response.wsgi_request))
        self.assertEqual(str(messages[0]), 'La contraseña actual es incorrecta.')

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('usuarios:iniciarSesion'), {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })
        self.assertRedirects(response, 'usuarios:login')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Correo electrónico o contraseña incorrectos.')

    # Prueba para crear cuenta (vista crear_cuenta)
    def test_signup_success(self):
        response = self.client.post(reverse('usuarios:crearCuenta'), {
            'nombres': 'New User',
            'email': 'newuser@example.com',
            'telefono': '123456789',
            'password': 'password123'
        })
        self.assertRedirects(response, 'usuarios:login')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Cuenta creada exitosamente.')

    def test_signup_email_exists(self):
        response = self.client.post(reverse('usuarios:crearCuenta'), {
            'nombres': 'Another User',
            'email': 'test@example.com',
            'telefono': '987654321',
            'password': 'password456'
        })
        self.assertRedirects(response, 'usuarios:signup')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'El email ya está registrado.')

    def test_signup_empty_fields(self):
        response = self.client.post(reverse('usuarios:crearCuenta'), {
            'nombres': '', 
            'email': '',
            'telefono': '',
            'password': ''
        })
        self.assertRedirects(response, 'usuarios:signup')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Los campos obligatorios no deben estar vacíos.')

    # Prueba para actualizar perfil
    def test_update_profile_success(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('usuarios:updatePerfil'), {
            'nombres': 'Test Name',
            'email': 'test@example.com',
            'telefono': '987654321',
            'contraseña_actual': 'password123',
            'nueva_contraseña': 'newpassword123'
        })
        self.assertRedirects(response, 'usuarios:perfil')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Tu perfil ha sido actualizado correctamente.')

        # Verificar los cambios en la base de datos
        self.user.refresh_from_db()
        self.assertEqual(self.user.nombres, 'Test Name')
        self.assertEqual(self.user.telefono, '987654321')
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_update_profile_short_new_password(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('usuarios:updatePerfil'), {
            'nombres': 'Test Name', 
            'email': 'test@example.com',
            'telefono': '987654321',
            'contraseña_actual': 'password123',
            'nueva_contraseña': 'short'
        })
        self.assertRedirects(response, 'usuarios:perfil')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'La nueva contraseña debe tener al menos 8 caracteres.')