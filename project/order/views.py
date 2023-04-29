from rest_framework import generics, response, status
from order.models import Order, OrderItem, Transaction
from order.serializers import ListCreateOrderSerializer, UpdateOrderSerializer
from restaurant.models import Restaurant

class ListCreateOrder(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ListCreateOrderSerializer

    def get_queryset(self):
        data = self.request.GET
        if data.get('status'):
            self.queryset = self.queryset.filter(status=data.get('status'))
        if data.get('user'):
            self.queryset = self.queryset.filter(user=data.get('user'))
        if data.get('date'):
            self.queryset = self.queryset.filter(status=data.get('date'))
        if data.get('restaurant'):
            self.queryset = self.queryset.filter(restaurant=data.get('restaurant'))
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        order_serializer = ListCreateOrderSerializer(data=data)
        if order_serializer.is_valid(raise_exception=True):
            try:
                order = Order.objects.get(status=0, user=self.request.user, restaurant=data.get('restaurant'))
                return response.Response({'Error': f'Order for this restaurant already exists with id {order.pk}'}, status.HTTP_400_BAD_REQUEST)
            except:
                Order.objects.create(
                    user=self.request.user,
                    restaurant=Restaurant.objects.get(id=data.get('restaurant'))
                )
                return response.Response({'Success': 'New order created successfully'}, status.HTTP_201_CREATED)

class UpdateDestroyOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = ListCreateOrderSerializer
    
    def put(self, request, *args, **kwargs):
        data = self.request.data
        order_serializer = UpdateOrderSerializer(data=data)
        order = Order.objects.get(id=self.kwargs['pk'])
        if order_serializer.is_valid(raise_exception=True):
            new_status = int(data.get('status'))
            if order.user == self.request.user and 0 <= new_status and new_status <= 3 and order.status < new_status:
                return super().put(request, *args, **kwargs)
            return response.Response({'Error': 'Not allowed to modify a confirmed order'}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': order_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        if order.user == self.request.user and order.status == 0:
            return super().destroy(request, *args, **kwargs)
        return response.Response({'Error': 'Not allowed to modify a confirmed order'}, status.HTTP_400_BAD_REQUEST)

