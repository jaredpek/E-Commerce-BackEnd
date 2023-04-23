from rest_framework import serializers
from django.contrib.auth.models import User
from user_account.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['mobile_number', 'date_of_birth', 'address', 'postal_code', 'date_joined']
        read_only_fields = ['date_joined']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, many=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        read_only_fields = ['id', 'username']
