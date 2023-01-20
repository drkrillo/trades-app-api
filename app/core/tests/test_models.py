"""
Tests for models.
"""
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

import pytz

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email sucessful"""
        email = "test@template.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.COM", "Test2@example.com"],
            ["TEST3@Example.Com", "TEST3@example.com"]
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_order(self):
        """Test creating an order is successful"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123',
        )
        order = models.Order.objects.create(
            user=user,
            symbol='BTC',
            start_date_time=datetime(2023, 1, 13, 14, 30, 12, tzinfo=pytz.UTC),
            initial_price=133100000,
            stop_loss=131100000,
            take_profit=163000000,
            leverage=10,
            title='BTC order created on 2023-01-13T14:30:12.000Z',
        )
        self.assertEqual(str(order), order.title)

    def test_crypto_table_not_empty(self):
        """Test retrieving Crypto Data Table is not empty."""
        crypto_table_length = models.Crypto.objects.count()

        self.assertNotEqual(crypto_table_length, 0)