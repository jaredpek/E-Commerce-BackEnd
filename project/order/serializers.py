from rest_framework import serializers
from order.models import OrderItem, Order, Transaction

class ListCreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class ListCreateOrderSerializer(serializers.ModelSerializer):
    items = ListCreateOrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class ListCreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
