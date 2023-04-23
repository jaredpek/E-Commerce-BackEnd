from django.contrib import admin
from restaurant.models import RestaurantType, Restaurant

admin.site.register([RestaurantType, Restaurant])
