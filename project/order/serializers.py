from rest_framework import serializers
from order.models import OrderItem, Order, Transaction

class ListOrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'item_name', 'price', 'quantity', 'total']

class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity']

class ListOrderSerializer(serializers.ModelSerializer):
    items = ListOrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'status', 'user', 'username', 'restaurant', 'restaurant_name', 'items', 'subtotal']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'restaurant']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class ListTransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    items = serializers.StringRelatedField(source='order.items', many=True, read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'user', 'username', 'date', 'restaurant', 'restaurant_name', 'items', 'from_address', 'from_postal_code', 'to_address', 'to_postal_code', 'subtotal' , 'delivery', 'total']
    
class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['to_address', 'to_postal_code']
