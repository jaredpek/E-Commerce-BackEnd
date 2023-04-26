from rest_framework import serializers
from order.models import OrderItem, Order

class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'price', 'quantity', 'total_cost']
        read_only_fields = ['id', 'order']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['restaurant']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['to_address', 'to_postal_code']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'status', 'user', 'date', 'restaurant', 'items', 'from_address', 'from_postal_code', 'to_address', 'to_postal_code', 'items_subtotal', 'delivery_cost', 'total_cost']
        read_only_fields = ['id', 'user', 'date', 'restaurant']
