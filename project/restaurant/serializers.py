from rest_framework import serializers
from restaurant.models import RestaurantType, Restaurant
from item.serializers import ItemSerializer

class RestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = ['id', 'name']
        read_only_fields = ['id']

class RestaurantSerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'active', 'owner', 'restaurant_type', 'name', 'delivery_charge', 'address', 'postal_code', 'items']
        read_only_fields = ['id']

class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['restaurant_type', 'name', 'delivery_charge', 'address', 'postal_code']
