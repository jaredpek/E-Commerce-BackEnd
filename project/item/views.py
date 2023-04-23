from rest_framework import generics, response, status
from item.models import ItemType, Item
from item.serializers import ItemTypeSerializer, ItemSerializer, CreateItemSerializer
from restaurant.models import Restaurant

class ListCreateItemTypes(generics.ListCreateAPIView):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        itemtype_serailizer = ItemTypeSerializer(data=data)
        if itemtype_serailizer.is_valid(raise_exception=True):
            name = data.get('name')
            ItemType.objects.create(
                name=name.lower().strip()
            )
            return response.Response({'Success': 'New item type created'}, status.HTTP_201_CREATED)
        return response.Response({'Error': itemtype_serailizer.errors}, status.HTTP_406_NOT_ACCEPTABLE)

class ListCreateItems(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        data = self.request.GET
        if data.get('item_id'):
            self.queryset = self.queryset.filter(id=data.get('item_id'))
        if data.get('restaurant_id'):
            self.queryset = self.queryset.filter(restaurant=data.get('restaurant_id'))
        return self.queryset

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        item_serializer = CreateItemSerializer(data=data)
        if item_serializer.is_valid(raise_exception=True):
            restaurant = Restaurant.objects.get(id=data.get('restaurant'))
            if restaurant.owner == self.request.user:
                item = Item.objects.create(
                    name=data.get('name'), 
                    restaurant=restaurant, 
                )
                item.item_type.set(data.getlist('item_type'))
                return response.Response({'Success': 'Successfully added a new item'}, status.HTTP_201_CREATED)
            else:
                return response.Response({'Error': 'You are not the owner of this restaurant'}, status.HTTP_401_UNAUTHORIZED)
        return response.Response({'Error': item_serializer.errors}, status.HTTP_406_NOT_ACCEPTABLE)

class UpdateItems(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    def put(self, request, *args, **kwargs):
        data = self.request.data
        item_serializer = ItemSerializer(data=data)
        if item_serializer.is_valid(raise_exception=True):
            restaurant = Restaurant.objects.get(id=data.get('restaurant'))
            if self.request.user == restaurant.owner:
                return super().put(request, *args, **kwargs)
            return response.Response({'Error': 'You are not the owner of this restaurant'}, status.HTTP_401_UNAUTHORIZED)
        return response.Response({'Error': item_serializer.errors}, status.HTTP_406_NOT_ACCEPTABLE)

