from rest_framework import generics, response, status
from restaurant.serializers import ListRestaurantSerializer, CreateUpdateRestaurantSerializer
from restaurant.models import Restaurant

class ListCreateRestaurants(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = ListRestaurantSerializer

    def get_queryset(self):
        params = self.request.GET
        if params.get('id'):
            self.queryset = self.queryset.filter(id=params.get('id'))
        if params.get('active'):
            self.queryset = self.queryset.filter(active=params.get('active'))
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        restaurant_serializer = CreateUpdateRestaurantSerializer(data=data)
        if restaurant_serializer.is_valid(raise_exception=True):
            Restaurant.objects.create(
                owner=self.request.user,
                name=data['name'],
                delivery_charge=data['delivery_charge'],
                address=data['address'],
                postal_code=data['postal_code'],
            )
            return response.Response({'Success': 'New restaurant created'}, status.HTTP_200_OK)
        return response.Response({'Error': [restaurant_serializer.errors]}, status.HTTP_200_OK)

class UpdateRestaurants(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = CreateUpdateRestaurantSerializer

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        return response.Response({'test', 'test'}, status.HTTP_202_ACCEPTED)
