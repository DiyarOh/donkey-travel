from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationViewTest(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_form_submission(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'testpassword',
            'password_verify': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        })

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_form_validation(self):
        response = self.client.post(reverse('register'), {
            'username': '',  # Missing username
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'invalid-email',  # Invalid email
            'first_name': 'Test',
            'last_name': 'User',
        })

        # Check if the response returns a status code of 200 (form errors)
        self.assertEqual(response.status_code, 200)

        # Check if the expected error messages are in the response content
        self.assertContains(response, "This field is required.")  # Username is required
        self.assertContains(response, "Enter a valid email address.")  # Invalid email

class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_form_submission(self):
        User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })

        self.assertRedirects(response, reverse('index'))

    def test_login_form_validation(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'invalid-password',  # Invalid password
        })

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Please enter a correct username and password.")
