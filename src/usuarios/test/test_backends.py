from django.test import TestCase
from django.contrib.auth import get_user_model
from usuarios.backends import EmailAuthBackend

class EmailAuthBackendTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword'
        )
        self.backend = EmailAuthBackend()

    def test_authenticate_with_valid_email_and_password(self):
        user = self.backend.authenticate(
            request=None, username='testuser@example.com', password='securepassword'
        )
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_email(self):
        user = self.backend.authenticate(
            request=None, username='wrong@example.com', password='securepassword'
        )
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        user = self.backend.authenticate(
            request=None, username='testuser@example.com', password='wrongpassword'
        )
        self.assertIsNone(user)

    def test_get_user_with_valid_id(self):
        user = self.backend.get_user(self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_get_user_with_invalid_id(self):
        user = self.backend.get_user(999)
        self.assertIsNone(user)
