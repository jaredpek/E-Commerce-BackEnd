from rest_framework import serializers
from restaurant.models import Restaurant
from item.serializers import ItemSerializer

class ListRestaurantSerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'active', 'owner', 'name', 'delivery_charge', 'address', 'postal_code', 'items']
        read_only_fields = ['id']

class CreateUpdateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'delivery_charge', 'address', 'postal_code']
