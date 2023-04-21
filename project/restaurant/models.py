from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator

class Restaurant(models.Model):
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    delivery_charge = models.FloatField(validators=[MinValueValidator(0)])
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$')])

    def __str__(self):
        return f'{"Active" if self.active else "Not Active"} | {self.name} | {self.address} {self.postal_code}'
