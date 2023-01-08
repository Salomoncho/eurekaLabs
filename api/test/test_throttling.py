from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch
import json

LOGIN_USER_URL = reverse('api:login')
REGISTER_USER_URL = reverse('api:register')
STOCK_SERVICE_URL = reverse('api:stock-service')


class ThrottlingTests(TestCase):
    def setUp(self):
        self.throttling_limit = 6
        self.client = APIClient()
        self.login_payload = {
            'email': 'notRegistered@gmail.com',
            'password': 'TestPassword',
        }
        self.register_payload = {
            'name': 'Salomon',
            'last_name': 'Hidalgo',
            'email': 'wrong email',
            'password': 'TestPassword',
            'password2': 'TestPassword',
        }

    def test_login_api_throttling(self):
        with self.assertRaises(Exception) as context:
            for i in range(self.throttling_limit):
                resp = self.client.post(LOGIN_USER_URL, self.login_payload)
                if resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    raise Exception('Throttling working')

        self.assertTrue('Throttling working' in str(context.exception))

    def test_register_api_throttling(self):
        with self.assertRaises(Exception) as context:
            for i in range(self.throttling_limit):
                resp = self.client.post(REGISTER_USER_URL, self.register_payload)
                if resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    raise Exception('Throttling working')

        self.assertTrue('Throttling working' in str(context.exception))

    @patch('api.views.requests.get')
    def test_stock_service_api_throttling(self, mock_get):
        mock_get.return_value.status_code = status.HTTP_400_BAD_REQUEST
        mock_get.return_value.json.return_value = {
            "Error Message": "Invalid API call. Please retry or visit the documentation for TIME_SERIES_DAILY_ADJUSTED."
        }
        with self.assertRaises(Exception) as context:
            for i in range(self.throttling_limit):
                payload = {
                    "stock_symbol": "QQQQQ"
                }
                r = self.client.post(
                    STOCK_SERVICE_URL,
                    data=json.dumps(payload),
                    content_type='application/json',
                    HTTP_X_API_KEY=settings.STOCK_SERVICE_API_KEY
                )
                if r.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    raise Exception('Throttling working')

        self.assertTrue('Throttling working' in str(context.exception))
