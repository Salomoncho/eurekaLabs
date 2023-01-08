from django.test import TestCase
from unittest.mock import patch


class BaseTestCase(TestCase):
    def setUp(self):
        self.patcher = patch('rest_framework.throttling.ScopedRateThrottle.allow_request')
        self.mock_throttling = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
