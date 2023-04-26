from rest_framework import generics, response, status
from order.models import OrderItem, Order
from order.serializers import CreateOrderItemSerializer, OrderItemSerializer, AddressSerializer, CreateOrderSerializer, OrderSerializer
from item.models import Item
from restaurant.models import Restaurant
from order.credentials import BING_APIKEY
import requests

class OrderDetails(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_location(self, postal_code, key):
        url = 'http://dev.virtualearth.net/REST/v1/Locations'
        params = {
            'countryRegion': 'SG',
            'postalCode': postal_code,
            'key': key,
        }
        coordinates = requests.get(url=url, params=params).json()['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates']
        return coordinates

    def get_distance(self, start, end, key):
        url = 'http://dev.virtualearth.net/REST/v1/Routes'
        params = {
            'wp.0': f'{start[0]},{start[1]}',
            'wp.1': f'{end[0]},{end[1]}',
            'key': key,
        }
        distance = requests.get(url=url, params=params).json()['resourceSets'][0]['resources'][0]['routeLegs'][0]['routeSubLegs'][0]['travelDistance']
        return distance

    def get_queryset(self):
        data = self.request.GET
        if data.get('status'):
            self.queryset = self.queryset.filter(status=data.get('status'))
        if data.get('order'):
            self.queryset = self.queryset.filter(order=data.get('order'))
        if data.get('user_id'):
            self.queryset = self.queryset.filter(user=data.get('user_id'))
        if data.get('restaurant_id'):
            self.queryset = self.queryset.filter(restaurant=data.get('restaurant_id'))
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        create_order_serializer = CreateOrderSerializer(data=data)
        if create_order_serializer.is_valid(raise_exception=True):
            deliver_to = {
                'to_address': None,
                'to_postal_code': None,
            }
            if data.get('to_address') and data.get('to_postal_code'):
                deliver_to['to_address'] = data.get('to_address')
                deliver_to['to_postal_code'] = data.get('to_postal_code')
            else:
                deliver_to['to_address'] = self.request.user.profile.address
                deliver_to['to_postal_code'] = self.request.user.profile.postal_code
            address_serializer = AddressSerializer(data=deliver_to)
            if address_serializer.is_valid(raise_exception=True):
                restaurant = Restaurant.objects.get(id=data.get('restaurant'))
                distance = self.get_distance(
                    start=self.get_location(restaurant.postal_code, BING_APIKEY),
                    end=self.get_location(deliver_to['to_postal_code'], BING_APIKEY),
                    key=BING_APIKEY,
                )
                delivery_cost = round(float(distance) * float(restaurant.delivery_charge), 2)
                Order.objects.create(
                    user=self.request.user,
                    restaurant=restaurant,
                    from_address=restaurant.address,
                    from_postal_code=restaurant.postal_code,
                    to_address=deliver_to['to_address'],
                    to_postal_code=deliver_to['to_postal_code'],
                    delivery_cost=delivery_cost,
                    total_cost=delivery_cost,
                )
                return response.Response({'Success': 'New order created successfully'}, status.HTTP_201_CREATED)
            return response.Response({'Error': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': create_order_serializer.errors}, status.HTTP_400_BAD_REQUEST)

class UpdateOrderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, *args, **kwargs):
        data = self.request.data
        order_serializer = OrderSerializer(data=data)
        order_id = int(self.kwargs['pk'])
        order = Order.objects.get(id=order_id)
        if order_serializer.is_valid(raise_exception=True):
            new_status = int(data.get('status'))
            if order.status == 0:
                return super().put(request, *args, **kwargs)
            elif 0 <= new_status and new_status <= 3 and new_status > order.status:
                order.status = new_status
                order.save()
                return response.Response({'Success': 'Successfully updated order status'}, status.HTTP_202_ACCEPTED)
            return response.Response({'Error': 'Not allowed to modify a confirmed order'}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': order_serializer.errors}, status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        order_id = int(self.kwargs['pk'])
        order = Order.objects.get(id=order_id)
        if order.status == 0:
            return super().destroy(request, *args, **kwargs)
        return response.Response({'Error': 'Not allowed to cancel a confirmed order'}, status.HTTP_400_BAD_REQUEST)

class OrderItemDetails(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        data = self.request.GET
        if data.get('order_id'):
            self.queryset = self.queryset.filter(order=data.get('order_id'))
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        orderitem_serializer = CreateOrderItemSerializer(data=data)
        if orderitem_serializer.is_valid(raise_exception=True):
            order = Order.objects.get(id=data.get('order'))
            if order.status == 0:
                item = Item.objects.get(id=data.get('item'))
                if order.restaurant == item.restaurant:
                    quantity = data.get('quantity')
                    total_cost = round(float(quantity) * item.price, 2)
                    OrderItem.objects.create(
                        order=order,
                        item=item,
                        price=item.price,
                        quantity=quantity,
                        total_cost=total_cost,
                    )
                    order.items_subtotal += total_cost
                    order.total_cost += total_cost
                    order.save()
                    return response.Response({'Success': 'Item added to order successfully'}, status.HTTP_201_CREATED)
                return response.Response({'Error': 'Invalid item selected'}, status.HTTP_400_BAD_REQUEST)
            return response.Response({'Error': 'Not allowed to modify a confirmed order'}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': orderitem_serializer.errors}, status.HTTP_400_BAD_REQUEST)
    
class UpdateOrderItemDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
