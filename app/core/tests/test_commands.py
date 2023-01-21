"""
Test Django Custom management commands
"""

from unittest import TestCase
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import (
    TestCase,
    SimpleTestCase,
)
from core.models import Crypto

from rest_framework import status


@patch('core.management.commands.wait_for_db.Command.check')
class CommandDBTests(SimpleTestCase):
    """ Test Database Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""

        patched_check.return_value = True

        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delayed(self, patched_sleeep, patched_check):
        """Test waiting for database when getting OperationalError"""

        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


@patch('core.management.commands.populate_crypto_tables.Command.check')
class CommandCryptoTests(TestCase):
    """Test Populate Crypto table command."""

    def test_command_run_successfully(self, patched_check):
        """Test command run successfully"""

        patched_check.return_value = True

        call_command('populate_crypto_tables')

        self.assertNotEqual(Crypto.objects.all().count(), 0)
