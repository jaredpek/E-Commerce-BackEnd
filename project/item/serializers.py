from rest_framework import serializers
from item.models import ItemType, Item

class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'name']
        read_only_fields = ['id']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'active', 'name', 'restaurant', 'item_type', 'price']
        read_only_fields = ['id']

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'restaurant', 'item_type', 'price']