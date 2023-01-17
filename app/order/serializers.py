"""
Serializers for Order APIs.
"""
from rest_framework import serializers

from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Orders."""

    class Meta:
        model = Order
        fields = [
            'id',
            'symbol',
            'initial_price',
            'start_date_time',
        ]
        read_only_fields = ['id']


class OrderDetailSerializer(OrderSerializer):
    """Serializer for Order Detail view."""

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + [
            'amount',
            'stop_loss',
            'take_profit',
            'leverage',
            'close_date_time',
            'closing_price',
        ]
