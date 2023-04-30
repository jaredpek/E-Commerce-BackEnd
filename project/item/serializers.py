from rest_framework import serializers
from item.models import ItemType, Item

class ListCreateItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'name']
        read_only_fields = ['id']

class ListItemSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    item_type_name = serializers.StringRelatedField(source='item_type', many=True, read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'active', 'name', 'restaurant', 'restaurant_name', 'item_type', 'item_type_name', 'price']
        read_only_fields = ['id']

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'restaurant', 'item_type', 'price']