from rest_framework import generics, response, status
from order.models import Order, OrderItem, Transaction
from order.serializers import ListOrderItemSerializer, CreateOrderItemSerializer, ListOrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, ListTransactionSerializer, CreateTransactionSerializer
from restaurant.models import Restaurant
from item.models import Item

class ListCreateOrder(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ListOrderSerializer

    def get_queryset(self):
        data = self.request.GET
        if data.get('id'):
            self.queryset = self.queryset.filter(id=data.get('id'))
        if data.get('user'):
            self.queryset = self.queryset.filter(user=data.get('user'))
        if data.get('restaurant'):
            self.queryset = self.queryset.filter(restaurant=data.get('restaurant'))
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        order_serializer = CreateOrderSerializer(data=data)
        if order_serializer.is_valid(raise_exception=True):
            restaurant = Restaurant.objects.get(id=data.get('restaurant'))
            try:
                order = Order.objects.get(status=0, user=self.request.user, restaurant=restaurant)
                return response.Response({'Error': f'Order at {restaurant.name} exists with pk {order.pk}'}, status.HTTP_400_BAD_REQUEST)
            except:
                Order.objects.create(
                    user=self.request.user,
                    restaurant=restaurant,
                )
            return response.Response({'Success': 'Order created successfully'}, status.HTTP_201_CREATED)
        return response.Response({'Error': order_serializer.errors}, status.HTTP_400_BAD_REQUEST)

class UpdateOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        order_serializer = UpdateOrderSerializer(data=data)
        if order_serializer.is_valid(raise_exception=True):
            order = Order.objects.get(id=data.get('id'))
            new_status = int(data.get('status'))
            if order.user == self.request.user:
                if 0 <= new_status and new_status <= 3 and order.status < new_status:
                    if new_status == 1:
                        transaction_serializer = CreateTransactionSerializer(data=data)
                        if not data.get('to_address') and not data.get('to_postal_code'):
                            data._mutable = True
                            data['to_address'] = order.user.profile.address
                            data['to_postal_code'] = order.user.profile.postal_code
                            data._mutable = False
                        if transaction_serializer.is_valid(raise_exception=True):
                            transaction = Transaction.objects.create(
                                order=order,
                                user=order.user,
                                restaurant=order.restaurant,
                                from_address=order.restaurant.address,
                                from_postal_code=order.restaurant.postal_code,
                                to_address=data.get('to_address'),
                                to_postal_code=data.get('to_postal_code'),
                                subtotal=order.subtotal,
                            )
                            transaction.delivery = transaction.get_delivery_cost(transaction.from_postal_code, transaction.to_postal_code)
                            transaction.total = transaction.get_total()
                            transaction.save()
                    order.status = new_status
                    order.save()
                    return response.Response({'Success': 'Order status updated successfully'}, status.HTTP_202_ACCEPTED)
                return response.Response({'Error': 'Not allowed to modify a confirmed order'}, status.HTTP_400_BAD_REQUEST)
            return response.Response({'Error': 'Not allowed to modify another user\'s order'}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': order_serializer.errors}, status.HTTP_400_BAD_REQUEST)
    

class DestroyOrder(generics.DestroyAPIView):
    queryset = Order.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        if order.user == self.request.user:
            if order.status == 0:
                return super().destroy(request, *args, **kwargs)
            return response.Response({'Error': 'Not allowed to delete a confirmed order'}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': 'Not allowed to modify another user\'s order'}, status.HTTP_400_BAD_REQUEST)

class ManageOrderItems(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = ListOrderItemSerializer

    def get_queryset(self):
        data = self.request.GET
        if data.get('order'):
            self.queryset = self.queryset.filter(order=data.get('order'))
        if data.get('item'):
            self.queryset = self.queryset.filter(item=data.get('item'))
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        data = self.request.POST
        order_item_serializer = CreateOrderItemSerializer(data=data)
        if order_item_serializer.is_valid(raise_exception=True):
            order = Order.objects.get(id=data.get('order'))
            if order.user == self.request.user:
                if order.status == 0:
                    try:
                        order_item = OrderItem.objects.get(order=data.get('order'), item=data.get('item'))
                        order_item.quantity = int(data.get('quantity'))
                        order_item.total = order_item.get_total()
                        order_item.save()
                        order.subtotal = order.get_subtotal()
                        order.save()
                        return response.Response({'Success': 'Item updated successfully'}, status.HTTP_202_ACCEPTED)
                    except:
                        item = Item.objects.get(id=data.get('item'))
                        if order.restaurant == item.restaurant:
                            order_item = OrderItem.objects.create(
                                order=order,
                                item=item,
                                price=item.price,
                                quantity=data.get('quantity'),
                            )
                            order_item.total = order_item.get_total()
                            order_item.save()
                            order.subtotal = order.get_subtotal()
                            order.save()
                            return response.Response({'Success': 'Item added to order successfully'}, status.HTTP_201_CREATED)
                        return response.Response({'Error': 'Invalid item selected'}, status.HTTP_400_BAD_REQUEST)
                return response.Response({'Error': 'Not allowed to modify a confirmed order'}, status.HTTP_400_BAD_REQUEST)
            return response.Response({'Error': 'Not allowed to modify another user\'s order'}, status.HTTP_400_BAD_REQUEST)
        return response.Response({'Error': order_item_serializer.errors}, status.HTTP_400_BAD_REQUEST)

class ListTransactions(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = ListTransactionSerializer

    def get_queryset(self):
        data = self.request.GET
        if data.get('order'):
            self.queryset = self.queryset.filter(order=data.get('order'))
        if data.get('user'):
            self.queryset = self.queryset.filter(user=data.get('user'))
        if data.get('date'):
            self.queryset = self.queryset.filter(date=data.get('date'))
        if data.get('restaurant'):
            self.queryset = self.queryset.filter(restaurant=data.get('restaurant'))
        return self.queryset
