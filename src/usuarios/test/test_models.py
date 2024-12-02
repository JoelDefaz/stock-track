from django.test import TestCase
from usuarios.models import UsuarioPersonalizado

class UsuarioPersonalizadoModelTest(TestCase):
    def test_creacion_usuario_personalizado(self):
        usuario = UsuarioPersonalizado.objects.create_user(
            username='usuario1',
            email='usuario1@example.com',
            nombres='Juan',
            apellidos='Pérez',
            telefono='123456789',
            password='password123'
        )
        self.assertEqual(usuario.nombres, 'Juan')
        self.assertEqual(usuario.apellidos, 'Pérez')
        self.assertEqual(usuario.email, 'usuario1@example.com')
        self.assertEqual(usuario.telefono, '123456789')
        self.assertTrue(usuario.check_password('password123'))

    def test_str_representacion(self):
        usuario = UsuarioPersonalizado.objects.create_user(
            username='usuario1',
            email='usuario1@example.com',
            nombres='Juan',
            apellidos='Pérez',
            password='password123'
        )
        
        self.assertEqual(str(usuario), 'Juan Pérez (usuario1)')

    def test_creacion_superusuario(self):
        superuser = UsuarioPersonalizado.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            nombres='Admin',
            apellidos='User',
            telefono='987654321',
            password='adminpassword'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.nombres, 'Admin')
        self.assertEqual(superuser.telefono, '987654321')
