from django.test import TestCase
from .models import CustomUser
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from unittest.mock import patch
from accounts.serializers import UserSerializer

class SignupTestCase(TestCase):
    def test_signup_success(self):
        # Test successful signup
        response = self.client.post(reverse('signup'), {'email': 'test@example.com', 'name': 'Test User', 'password': 'password'})
        self.assertEqual(response.status_code, 201)  # Assuming signup redirects to login page

        # Check if user is created in the database
        self.assertTrue(CustomUser.objects.filter(email='test@example.com').exists())

    def test_signup_missing_fields(self):
        # Test signup with missing fields
        response = self.client.post(reverse('signup'), {'email': 'test@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 400)  # Assuming signup page is re-rendered with error message

        # Check if user is not created in the database
        self.assertFalse(CustomUser.objects.filter(email='test@example.com').exists())

    def test_signup_existing_user(self):
        # Test signup with existing email
        CustomUser.objects.create_user(email='test@example.com', name='Test User', password='password')
        response = self.client.post(reverse('signup'), {'email': 'test@example.com', 'name': 'Another User', 'password': 'password'})
        self.assertEqual(response.status_code, 400)  # Assuming signup page is re-rendered with error message

        # Check if user is not created in the database
        self.assertEqual(CustomUser.objects.filter(email='test@example.com').count(), 1)  # Only one user with this email exists

class LoginTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.name = 'testuser'
        self.password = 'password'
        self.email = 'test@email.com'
        self.user = CustomUser.objects.create_user(name=self.name, password=self.password, email=self.email)

    def test_login_success(self):
        # Test successful login
        response = self.client.post(reverse('login'), {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 200)  # Assuming login redirects to home page

    def test_login_failure(self):
        # Test login failure with incorrect password
        response = self.client.post(reverse('login'), {'email': self.email, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)  # Assuming login page is re-rendered with error message

    def test_login_invalid_user(self):
        # Test login with invalid name
        response = self.client.post(reverse('login'), {'email': 'invalid_user', 'password': 'password'})
        self.assertEqual(response.status_code, 401)  # Assuming login page is re-rendered with error message


class PasswordResetAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('password_reset_api')
        mail.outbox = []  # Clear the outbox before each test

    @patch('accounts.views.account_activation_token.make_hash_value')
    def test_password_reset_success(self, mock_make_hash_value):
        # Mock the make_hash_value function
        mock_make_hash_value.return_value = 'mocked_token'

        # Create a test user
        email = 'test@example.com'
        user = get_user_model().objects.create(email=email, name='Test User')

        # Get the current site's domain
        # current_site = Site.objects.get_current()

        # Construct the reset link
        reset_link = f'http://127.0.0.1:3000/pwdUpdate/{user.id}/mocked_token/'

        # Send a POST request to the password reset endpoint
        response = self.client.post(self.url, {'email': email})

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Other test methods remain unchanged

    def test_password_reset_missing_email(self):
        # Send a POST request without an email
        response = self.client.post(self.url, {})

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the error message
        self.assertIn('Email is required.', response.data['error'])

    def test_password_reset_user_not_found(self):
        # Send a POST request with an email that does not exist
        response = self.client.post(self.url, {'email': 'nonexistent@example.com'})

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Assert that the response contains the error message
        self.assertIn('User not found.', response.data['error'])


class UserDataViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password123')
        self.url = reverse('user-data')

    def test_user_data_retrieval(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send a GET request to retrieve user data
        response = self.client.get(self.url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the expected user data
        expected_data = UserSerializer(instance=self.user, context={'request': None}).data
        self.assertEqual(response.data, expected_data)

    def test_user_data_update(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send a PUT request to update user data
        data = {'name': 'New Name'}
        response = self.client.put(self.url, data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the user's name has been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'New Name')

    # Add more test cases as needed
