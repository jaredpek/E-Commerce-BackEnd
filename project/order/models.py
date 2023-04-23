from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import User
from restaurant.models import Restaurant
from item.models import Item

class Order(models.Model):
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    from_address = models.CharField(max_length=100)
    from_postal_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$')])
    to_address = models.CharField(max_length=100)
    to_postal_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$')])
    items_subtotal = models.FloatField(validators=[MinValueValidator(0)], default=0)
    delivery_cost = models.FloatField(validators=[MinValueValidator(0)], default=0)
    total_cost = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'{"Completed" if self.completed else "Incomplete"} | {self.user.username} | {self.restaurant.name} | {self.total_cost} | {self.to_address}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    total_cost = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.order.user.username} | {self.order.restaurant.name} | {self.item.name} | {self.quantity} | {self.total_cost}'
