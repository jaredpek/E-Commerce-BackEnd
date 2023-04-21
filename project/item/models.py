from django.db import models
from restaurant.models import Restaurant

class Item(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=100)

    def __str__(self):
        return f'{"Active" if self.active else "Not Active"} | {self.name} | {self.item_type} | {self.restaurant}'
