from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from api import serializers, api_messages

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse('api:register')


class RegisterApiTests(TestCase):
    """Test the User API (Non-Auth User)"""

    def setUp(self):
        self.client = APIClient()
        self.generic_payload = {
            'name': 'Salomon',
            'last_name': 'Hidalgo',
            'email': 'salomontest@gmail.com',
            'password': 'TestPassword',
            'password2': 'TestPassword',
        }

    def test_register_user_success(self):
        """Test registering a new user returning the API_KEY"""

        resp = self.client.post(REGISTER_USER_URL, self.generic_payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username=self.generic_payload['name'], email=self.generic_payload['email'])
        self.assertTrue(user.check_password(self.generic_payload['password']))
        self.assertNotIn('password', resp.data)
        self.assertEqual(resp.data['message'], api_messages.REGISTER_USER_CREATED)
        self.assertEqual(resp.data['API_KEY'], settings.STOCK_SERVICE_API_KEY)

    def test_register_email_exist_in_db(self):
        """Test registering a user with an email that already exist in db"""
        usr = get_user_model().objects.create_user(
            username=self.generic_payload['name'],
            email=self.generic_payload['email'],
            last_name=self.generic_payload['last_name'],
            password=self.generic_payload['password'],
        )
        usr.save()

        payload = {
            'name': 'Reynaldo',
            'last_name': 'Bracho',
            'email': self.generic_payload['email'],
            'password': 'MyPass',
            'password2': 'MyPass',
        }

        resp = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        serializer = serializers.RegisterSerializer(data=payload)
        self.assertFalse(serializer.is_valid())

    def test_register_invalid_email(self):
        """Test registering a user with an invalid email"""
        self.generic_payload['email'] = 'thisIsNotAnEmail'

        resp = self.client.post(REGISTER_USER_URL, self.generic_payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        serializer = serializers.RegisterSerializer(data=self.generic_payload)
        self.assertFalse(serializer.is_valid())

    def test_register_passwords_did_not_match(self):
        """Test registering a user with password not equal to password confirmation"""
        self.generic_payload['password2'] = 'OtherPassword'

        resp = self.client.post(REGISTER_USER_URL, self.generic_payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json()['password'], [api_messages.REGISTER_PASSWORDS_DID_NOT_MATCH])
        serializer = serializers.RegisterSerializer(data=self.generic_payload)
        self.assertFalse(serializer.is_valid())
