from rest_framework import generics, response, status
from restaurant.serializers import ListCreateRestaurantTypeSerializer, ListRestaurantSerializer, CreateRestaurantSerializer
from restaurant.models import RestaurantType, Restaurant

class ListCreateRestaurantTypes(generics.ListCreateAPIView):
    queryset = RestaurantType.objects.all()
    serializer_class = ListCreateRestaurantTypeSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        restauranttype_serializer = ListCreateRestaurantTypeSerializer(data=data)
        if restauranttype_serializer.is_valid(raise_exception=True):
            name = data.get('name')
            RestaurantType.objects.create(
                name=name.lower().strip()
            )
            return response.Response({'Success': 'New restaurant type created successfully'}, status.HTTP_201_CREATED)
        return response.Response({'Error': restauranttype_serializer.errors}, status.HTTP_406_NOT_ACCEPTABLE)

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
        restaurant_serializer = CreateRestaurantSerializer(data=data)
        if restaurant_serializer.is_valid(raise_exception=True):
            restaurant = Restaurant.objects.create(
                owner=self.request.user,
                name=data['name'],
                delivery_charge=data['delivery_charge'],
                address=data['address'],
                postal_code=data['postal_code'],
            )
            restaurant.restaurant_type.set(data.getlist('restaurant_type'))
            return response.Response({'Success': 'New restaurant created'}, status.HTTP_200_OK)
        return response.Response({'Error': [restaurant_serializer.errors]}, status.HTTP_406_NOT_ACCEPTABLE)

class UpdateRestaurants(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = ListRestaurantSerializer
    
    def put(self, request, *args, **kwargs):
        data = self.request.POST
        restaurant_id = data.get('id')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        owner = restaurant.owner
        if self.request.user == owner:
            return super().put(request, *args, **kwargs)
        return response.Response({'Error': 'You are not the owner of this restaurant'}, status.HTTP_401_UNAUTHORIZED)
