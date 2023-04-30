from rest_framework import serializers
from restaurant.models import RestaurantType, Restaurant
from item.serializers import ListItemSerializer

class ListCreateRestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = ['id', 'name']
        read_only_fields = ['id']

class ListRestaurantSerializer(serializers.ModelSerializer):
    restaurant_type_name = serializers.StringRelatedField(source='restaurant_type', many=True, read_only=True)
    items = ListItemSerializer(read_only=True, many=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'active', 'owner', 'restaurant_type', 'restaurant_type_name', 'name', 'delivery_charge', 'address', 'postal_code', 'items']
        read_only_fields = ['id']

class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['restaurant_type', 'name', 'delivery_charge', 'address', 'postal_code']
