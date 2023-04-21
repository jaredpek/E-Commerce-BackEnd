from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from user_account import serializers
from django.contrib.auth.models import User

class AccountDetails(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
    
    def post(self, request, *args, **kwargs):
        user_serializer = serializers.UserSerializer(instance=self.request.user, data=self.request.POST)
        profile_serializer = serializers.ProfileSerializer(instance=self.request.user.profile, data=self.request.POST)
        if user_serializer.is_valid(raise_exception=True) and profile_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            profile_serializer.save()
            return Response({'Success': 'Account successfully updated'}, status.HTTP_200_OK)
        return Response({'Error': [user_serializer.errors, profile_serializer.errors]})
