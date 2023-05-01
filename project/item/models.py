from django.db import models
from restaurant.models import Restaurant
from django.core.validators import MinValueValidator

class ItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.pk} | {self.name}'

class Item(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='items')
    item_type = models.ManyToManyField(ItemType)
    price = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.pk} | {"Active" if self.active else "Not Active"} | {self.name} | {self.restaurant.name} | {self.price}'
