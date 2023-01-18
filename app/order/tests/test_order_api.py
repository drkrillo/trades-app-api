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
        'start_date_time': datetime(2023, 1, 13, 14, 30, 12, tzinfo=pytz.UTC),
        'initial_price': 133100.455,
        'stop_loss': 131100.015,
        'take_profit': 163000.355,
        'leverage': 10,
        'title': 'BTC order created on 2023-01-13 14:30:12',
    }
    defaults.update(params)

    order = Order.objects.create(user=user, **defaults)
    return order


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='test123')
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
        other_user = create_user(
            email='other@example.com',
            password='testpass123',
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

    def test_partial_update(self):
        """Test partial update on an order."""
        original_amount = 100.0
        original_stop_loss = 131100.015
        order = create_order(
            user=self.user,
            start_date_time=datetime(
                2023, 1, 13, 14, 30, 12, tzinfo=pytz.UTC
            ),
            amount=original_amount,
            initial_price=133100.455,
            stop_loss=original_stop_loss,
            take_profit=163000.355,
            leverage=10,
        )

        payload = {'amount': 1000.0}
        url = detail_url(order.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.amount, payload['amount'])
        self.assertEqual(order.stop_loss, original_stop_loss)
        self.assertEqual(order.user, self.user)

    def test_full_update(self):
        """Test full update of order."""
        order = create_order(
            user=self.user,
            symbol='ETH',
            start_date_time=datetime(
                2023, 1, 13, 14, 30, 12, tzinfo=pytz.UTC
            ),
            amount=100.0,
            initial_price=133100.455,
            take_profit=163000.355,
            stop_loss=131100.015,
            leverage=10,
        )

        payload = {
            'symbol': 'BTC',
            'start_date_time': datetime(
                2023, 1, 23, 11, 22, 13, tzinfo=pytz.UTC
            ),
            'amount': 250.0,
            'initial_price': 101222.202,
            'take_profit': 102222.202,
            'stop_loss': 100000.100,
            'leverage': 15,
        }
        url = detail_url(order.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(order, k), v)
        self.assertEqual(order.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing order user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        order = create_order(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(order.id)
        self.client.patch(url, payload)

        order.refresh_from_db()
        self.assertEqual(order.user, self.user)

    def test_delete_order(self):
        """Test deleting an order successful."""
        order = create_order(user=self.user)

        url = detail_url(order.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_delete_other_users_order_error(self):
        """Test trying to delete another user's order returns error."""
        new_user = create_user(email='user2@example.com', password='test123')
        order = create_order(user=new_user)

        url = detail_url(order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
