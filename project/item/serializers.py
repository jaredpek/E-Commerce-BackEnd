from rest_framework import serializers

class ItemSerializer(serializers.Serializer):
    class Meta:
        fields = ['id', 'active', 'name', 'restaurant', 'item_type']
        read_only_fields = ['id']
