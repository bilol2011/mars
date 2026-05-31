from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.wallet.models import Wallet


class RegistrationTests(TestCase):
    def test_user_can_register_and_wallet_is_created(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'username': 'newstudent',
                'email': 'newstudent@example.com',
                'first_name': 'New',
                'last_name': 'Student',
                'phone': '+998901234567',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            },
        )

        self.assertRedirects(response, reverse('accounts:login'))
        user = get_user_model().objects.get(email='newstudent@example.com')
        self.assertTrue(Wallet.objects.filter(user=user).exists())

    def test_duplicate_email_shows_form_error(self):
        User = get_user_model()
        User.objects.create_user(username='oldstudent', email='student@example.com', password='StrongPass12345')

        response = self.client.post(
            reverse('accounts:register'),
            {
                'username': 'newstudent',
                'email': 'student@example.com',
                'first_name': 'New',
                'last_name': 'Student',
                'phone': '',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bu email bilan foydalanuvchi allaqachon mavjud.')


class LoginTests(TestCase):
    def test_user_can_login_with_email_case_insensitive(self):
        User = get_user_model()
        User.objects.create_user(
            username='loginuser',
            email='loginuser@example.com',
            password='StrongPass12345',
        )

        response = self.client.post(
            reverse('accounts:login'),
            {'username': 'LOGINUSER@EXAMPLE.COM', 'password': 'StrongPass12345'},
        )

        self.assertRedirects(response, reverse('dashboard:home'))

    def test_invalid_login_shows_error(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': 'missing@example.com', 'password': 'wrong-password'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email yoki parol noto')
