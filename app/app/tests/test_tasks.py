"""
Tests for Celery Tasks functions.
"""
from django.test import SimpleTestCase

from app import tasks

import sys
import requests
from datetime import datetime, timedelta

SYMBOLS_VALID = ['BTC-USD',]
SYMBOLS_NOT_VALID = ['ASDASD']
COINBASE_URL = 'https://api.pro.coinbase.com/'


class TasksTest(SimpleTestCase):
    """Test Celery tasks."""

    def test_get_data_from_api(self):
        """Test the response of the API ticker endpoint is OK."""

        res, status = tasks.get_data_from_api(SYMBOLS_VALID)

        self.assertEqual(status, 200)

    def test_substract(self):
        """Test the response of the API ticker endpoint fails."""
        pass
