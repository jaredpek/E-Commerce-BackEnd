from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import User
from restaurant.models import Restaurant
from item.models import Item
from order.credentials import BING_APIKEY
import requests

class Order(models.Model):
    status_choices = [(0, 'Ordering'), (1, 'Processing'), (2, 'Delivering'), (3, 'Completed')]
    status = models.IntegerField(choices=status_choices, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    subtotal = models.FloatField(validators=[MinValueValidator(0)], default=0)
    
    def get_subtotal(self):
        subtotal = 0
        for item in self.items.all():
            subtotal += item.total
        return round(subtotal, 2)

    def __str__(self):
        return f'{self.pk} | {self.status_choices[self.status][1]} | {self.user.username} | {self.restaurant.name} | {self.subtotal}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    total = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def get_total(self):
        total = float(self.quantity) * float(self.price)
        return round(total, 2)

    def __str__(self):
        return f'{self.pk} | {self.order.user.username} | {self.order.restaurant.name} | {self.item.name} | {self.quantity} | {self.total}'

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    from_address = models.CharField(max_length=100)
    from_postal_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$')])
    to_address = models.CharField(max_length=100)
    to_postal_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$')])
    subtotal = models.FloatField(validators=[MinValueValidator(0)], default=0)
    delivery = models.FloatField(validators=[MinValueValidator(0)], default=0)
    total = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def get_location(self, postal_code, key=BING_APIKEY):
        url = 'http://dev.virtualearth.net/REST/v1/Locations'
        params = {
            'countryRegion': 'SG',
            'postalCode': postal_code,
            'key': key,
        }
        coordinates = requests.get(url=url, params=params).json()['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates']
        return coordinates

    def get_distance(self, start, end, key=BING_APIKEY):
        url = 'http://dev.virtualearth.net/REST/v1/Routes'
        params = {
            'wp.0': f'{start[0]},{start[1]}',
            'wp.1': f'{end[0]},{end[1]}',
            'key': key,
        }
        distance = requests.get(url=url, params=params).json()['resourceSets'][0]['resources'][0]['routeLegs'][0]['routeSubLegs'][0]['travelDistance']
        return distance
    
    def get_delivery_cost(self, start, end):
        distance = self.get_distance(
            start=self.get_location(start),
            end=self.get_location(end),
        )
        delivery_cost = float(distance) * self.restaurant.delivery_charge
        return round(delivery_cost, 2)
    
    def get_total(self):
        total = self.subtotal + self.delivery
        return round(total, 2)

    def __str__(self):
        return f'{self.pk} | {self.date} | {self.user.username} | {self.restaurant.name} | {self.total}'
