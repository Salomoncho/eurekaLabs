from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.conf import settings
from api import api_messages
import json
from rest_framework.test import APIClient
from rest_framework import status


STOCK_SERVICE_URL = reverse('api:stock-service')
STOCK_API_MOCK_RESPONSE = {
    "Meta Data": {
        "1. Information": "Daily Time Series with Splits and Dividend Events",
        "2. Symbol": "META",
        "3. Last Refreshed": "2023-01-06",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2023-01-06": {
            "1. open": "128.97",
            "2. high": "130.33",
            "3. low": "126.04",
            "4. close": "130.02",
            "5. adjusted close": "130.02",
            "6. volume": "27584498",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2023-01-05": {
            "1. open": "126.125",
            "2. high": "128.52",
            "3. low": "124.54",
            "4. close": "126.94",
            "5. adjusted close": "126.94",
            "6. volume": "25447099",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2023-01-04": {
            "1. open": "127.38",
            "2. high": "129.0498",
            "3. low": "125.85",
            "4. close": "127.37",
            "5. adjusted close": "127.37",
            "6. volume": "32397094",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2023-01-03": {
            "1. open": "122.82",
            "2. high": "126.37",
            "3. low": "122.28",
            "4. close": "124.74",
            "5. adjusted close": "124.74",
            "6. volume": "35528531",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-30": {
            "1. open": "118.16",
            "2. high": "120.42",
            "3. low": "117.74",
            "4. close": "120.34",
            "5. adjusted close": "120.34",
            "6. volume": "19583825",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-29": {
            "1. open": "116.4",
            "2. high": "121.03",
            "3. low": "115.77",
            "4. close": "120.26",
            "5. adjusted close": "120.26",
            "6. volume": "22366192",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-28": {
            "1. open": "116.25",
            "2. high": "118.15",
            "3. low": "115.51",
            "4. close": "115.62",
            "5. adjusted close": "115.62",
            "6. volume": "19612473",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-27": {
            "1. open": "117.93",
            "2. high": "118.6",
            "3. low": "116.0501",
            "4. close": "116.88",
            "5. adjusted close": "116.88",
            "6. volume": "21392311",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-23": {
            "1. open": "116.03",
            "2. high": "118.175",
            "3. low": "115.535",
            "4. close": "118.04",
            "5. adjusted close": "118.04",
            "6. volume": "17796625",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-22": {
            "1. open": "117.2",
            "2. high": "118.62",
            "3. low": "114.38",
            "4. close": "117.12",
            "5. adjusted close": "117.12",
            "6. volume": "23618121",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-21": {
            "1. open": "116.7",
            "2. high": "120.34",
            "3. low": "115.62",
            "4. close": "119.76",
            "5. adjusted close": "119.76",
            "6. volume": "20392799",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-20": {
            "1. open": "113.26",
            "2. high": "117.33",
            "3. low": "112.46",
            "4. close": "117.09",
            "5. adjusted close": "117.09",
            "6. volume": "28742501",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2022-12-19": {
            "1. open": "116.83",
            "2. high": "117.8",
            "3. low": "114.331",
            "4. close": "114.48",
            "5. adjusted close": "114.48",
            "6. volume": "29769875",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
    }
}


class StockServiceApiTests(TestCase):
    """Test Stock Service API"""

    def setUp(self):
        self.client = APIClient()
        self.generic_payload = {
            'email': 'salomontest@gmail.com',
            'password': 'TestPassword',
        }

    @patch('api.views.requests.get')
    def test_valid_stock_service_request(self, mock_get):
        """Test requesting valid facebook data"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = STOCK_API_MOCK_RESPONSE
        payload = {
            "stock_symbol": "META"
        }
        r = self.client.post(
            STOCK_SERVICE_URL,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_API_KEY=settings.STOCK_SERVICE_API_KEY
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        resp = r.json()
        self.assertTrue('data' in resp)
        self.assertEqual(resp['data']["2022-12-20"], {
            'Open Price': '113.26',
            'Higher price': '117.33',
            'Lower price': '112.46',
            'Close price': '117.09',
            'Variation Percentage': '2.23'
        })
        self.assertEqual(resp['data']['2022-12-19']['Variation Percentage'], '0.00')
        self.assertEqual(resp['data']['2022-12-22']['Variation Percentage'], '-2.25')
        self.assertEqual(resp['data']['2023-01-06']['Variation Percentage'], '2.37')

    @patch('api.views.requests.get')
    def test_invalid_stock_service_request_no_api_key(self, mock_get):
        """Test request without API KEY"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = STOCK_API_MOCK_RESPONSE
        payload = {
            "stock_symbol": "META"
        }
        r = self.client.post(
            STOCK_SERVICE_URL,
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        resp = r.json()
        self.assertEqual(resp['detail'], 'Authentication credentials were not provided.')

    @patch('api.views.requests.get')
    def test_stock_symbol_does_not_exist(self, mock_get):
        """Test request with an invalid stock symbols"""
        mock_get.return_value.status_code = status.HTTP_400_BAD_REQUEST
        mock_get.return_value.json.return_value = {
            "Error Message": "Invalid API call. Please retry or visit the documentation for TIME_SERIES_DAILY_ADJUSTED."
        }
        payload = {
            "stock_symbol": "QQQQQ"
        }
        r = self.client.post(
            STOCK_SERVICE_URL,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_API_KEY=settings.STOCK_SERVICE_API_KEY
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        resp = r.json()
        self.assertTrue('error' in resp)
        self.assertEqual(resp['error'], api_messages.INVALID_API_CALL)

    def test_stock_symbol_invalid_len(self):
        """Test sending a stock symbol with more than 5 characters"""
        payload = {
            "stock_symbol": "METAMETA"
        }
        r = self.client.post(
            STOCK_SERVICE_URL,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_API_KEY=settings.STOCK_SERVICE_API_KEY
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        resp = r.json()
        self.assertTrue('stock_symbol' in resp)
        self.assertEqual(resp['stock_symbol'], ['Ensure this field has no more than 5 characters.'])
