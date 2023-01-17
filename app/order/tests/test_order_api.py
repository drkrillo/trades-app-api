"""
Tests for the Order APIs
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import pytz

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Order

from order.serializers import (
    OrderSerializer,
    OrderDetailSerializer,
)


ORDERS_URL = reverse('order:order-list')


def detail_url(order_id):
    """Create and return an order detail URL."""
    return reverse('order:order-detail', args=[order_id])


def create_order(user, **params):
    """Create and return a sample Order"""
    defaults = {
        'symbol': 'BTC',
        'amount': 100.0,
        'start_date_time': datetime(2023, 1, 13, 14, 30, 12),
        'initial_price': 133100.455,
        'stop_loss': 131100.015,
        'take_profit': 163000.355,
        'leverage': 10,
        'title': 'BTC order created on 2023-01-13 14:30:12',
    }
    defaults.update(params)

    order = Order.objects.create(user=user, **defaults)
    return order


class PublicOrderApiTests(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):
    """Test authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com'
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_orders(self):
        """Test retrieving a list of Orders"""
        create_order(user=self.user)
        create_order(user=self.user)

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.all().order_by('-id')
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_order_list_limited_to_user(self):
        """Test list of orders is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com'
            'testpass123'
        )
        create_order(user=other_user)
        create_order(user=self.user)

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data, serializer.data)

    def test_get_order_detail(self):
        """Test get order detail."""
        order = create_order(user=self.user)
        url = detail_url(order.id)
        res = self.client.get(url)
        serializer = OrderDetailSerializer(order)

        self.assertEqual(res.data, serializer.data)

    def test_create_order(self):
        """Test creating an order."""
        payload = {
            'symbol': 'BTC',
            'start_date_time': datetime(
                2023, 1, 13, 14, 30, 12, tzinfo=pytz.UTC
            ),
            'initial_price': 133100.455,
            'stop_loss': 131100.015,
            'take_profit': 163000.355,
            'leverage': 10,
        }
        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(order, k), v)
        self.assertEqual(order.user, self.user)
