from django.contrib import admin
from order.models import OrderItem, Order, Transaction

admin.site.register([OrderItem, Order, Transaction])
