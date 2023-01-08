from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from api import serializers, api_messages

from rest_framework.test import APIClient
from rest_framework import status
from api.test.base_test_class import BaseTestCase
LOGIN_USER_URL = reverse('api:login')


class LoginApiTests(BaseTestCase):
    """Test the User API (Non-Auth User)"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.generic_payload = {
            'email': 'salomontest@gmail.com',
            'password': 'TestPassword',
        }
        self.createdUser = get_user_model().objects.create_user(
            username='Salomon',
            email=self.generic_payload['email'],
            last_name='Hidalgo',
            password=self.generic_payload['password'],
        )
        self.createdUser.save()

    def test_login_user_success(self):
        """Test login user"""

        resp = self.client.post(LOGIN_USER_URL, self.generic_payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['message'], api_messages.LOGIN_USER_AUTHENTICATED)
        self.assertEqual(resp.data['API_KEY'], settings.STOCK_SERVICE_API_KEY)

    def test_login_email_does_not_exist(self):
        """Test the login API with a wrong email"""
        payload = {
            'email': 'wrong@email.com',
            'password': 'ABCdef'
        }
        resp = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['message'], api_messages.LOGIN_USER_DOES_NOT_EXIST)

    def test_login_wrong_password(self):
        """Test the login API with a wrong password"""
        payload = {
            'email': self.generic_payload['email'],
            'password': 'ABCdef'
        }
        resp = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['message'], api_messages.LOGIN_PASS_INCORRECT)

    def test_login_invalid_data(self):
        """Test the login API with invalid data"""
        payload = {
            'email': 'this is not an email',
            'password': 'ABCdef'
        }
        resp = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        serializer = serializers.LoginSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
