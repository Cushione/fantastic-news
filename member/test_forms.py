from django.test import TestCase
from .forms import RegisterForm
from django.contrib.auth.models import User


class TestRegisterForm(TestCase):

    def test_first_name_is_required(self):
        form = RegisterForm({
            'username': 'TestUsername',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
            'first_name': '',
            'email': 'test@email.com'
        })

        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys()) 

    def test_email_is_required(self):
        form = RegisterForm({
            'username': 'TestUsername',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
            'first_name': 'Tester',
            'email': ''
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys()) 

    def test_user_creation_saves_all_fields(self):
        form = RegisterForm({
            'username': 'TestUsername',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
            'first_name': 'Tester',
            'email': 'test@email.com'
        })
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, 'Tester')
        self.assertEqual(user.email, 'test@email.com')
        