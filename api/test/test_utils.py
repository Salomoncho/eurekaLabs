from django.test import TestCase
from rest_framework import status

from api import utils, api_messages


class UtilTests(TestCase):

    def test_isfloat(self):
        """Test the is float function with multiple inputs"""
        self.assertTrue(utils.isfloat(0))
        self.assertFalse(utils.isfloat('0'))
        self.assertTrue(utils.isfloat(1.1234567))
        self.assertFalse(utils.isfloat('1.1234567'))
        self.assertTrue(utils.isfloat(-5.1234567))
        self.assertFalse(utils.isfloat('-5.1234567'))
        self.assertFalse(utils.isfloat('abcde'))

    def test_format_two_digit(self):
        """Test the format two digit function with multiple inputs"""
        self.assertEqual(utils.format_two_digit(0), '0.00')
        self.assertEqual(utils.format_two_digit(1.12234), '1.12')
        self.assertEqual(utils.format_two_digit('1.12234'), '1.12234')
        self.assertEqual(utils.format_two_digit(-5.1234567), '-5.12')
        self.assertEqual(utils.format_two_digit('-5.1234567'), '-5.1234567')

    def test_calculate_last_two_variation(self):
        """Test the calculate_last_two_variation function"""
        previous = {
            "1. open": "126.125",
            "2. high": "128.52",
            "3. low": "124.54",
            "4. close": "126.94",
            "5. adjusted close": "126.94",
            "6. volume": "25447099",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        }
        current = {
            "1. open": "127.38",
            "2. high": "129.0498",
            "3. low": "125.85",
            "4. close": "127.37",
            "5. adjusted close": "127.37",
            "6. volume": "32397094",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        }
        r = utils.calculate_last_two_variation(previous, current)
        self.assertEqual(r, '0.34')

    def test_output(self):
        """Test output function"""
        stock_info = {
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
            }
        }
        r = utils.output(stock_info, list(stock_info.keys()))

        self.assertEqual(r['2023-01-05'], {'Open Price': '126.125',
                                           'Higher price': '128.52',
                                           'Lower price': '124.54',
                                           'Close price': '126.94',
                                           'Variation Percentage': '0.00'
                                           })

        self.assertEqual(r['2023-01-04'], {'Open Price': '127.38',
                                           'Higher price': '129.0498',
                                           'Lower price': '125.85',
                                           'Close price': '127.37',
                                           'Variation Percentage': '0.34'
                                           })

    def test_validate_response(self):
        """Test Validate Response function"""
        valid_data = {
            'Time Series (Daily)': {}
        }
        r = utils.validate_response(valid_data)

        self.assertEqual(r['status'], status.HTTP_200_OK)
        self.assertEqual(r['data'], {})

    def test_validate_response_bad_request(self):
        """Test Validate Response without the Time Series (Daily) key"""
        invalid_data = {
            "Error Message": "This is a test message"
        }
        r = utils.validate_response(invalid_data)

        self.assertEqual(r['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r['data'], None)
        self.assertEqual(r['error'], api_messages.INVALID_API_CALL)

