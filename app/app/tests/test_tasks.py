"""
Tests for Celery Tasks functions.
"""
from django.test import SimpleTestCase

from app import tasks


SYMBOLS_VALID = ['BTC-USD', ]
SYMBOLS_NOT_VALID = ['ASDASD']
COINBASE_URL = 'https://api.pro.coinbase.com/'


class TasksTest(SimpleTestCase):
    """Test Celery tasks."""

    def test_get_data_from_api_ok(self):
        """Test the response of the API ticker endpoint is OK."""

        res, status = tasks.get_data_from_api(SYMBOLS_VALID)

        self.assertEqual(status, 200)

    def test_get_data_from_api_error(self):
        """Test the response of the API ticker endpoint fails."""
        
        res, status = tasks.get_data_from_api(SYMBOLS_NOT_VALID)

        self.assertEqual(status, 404)
