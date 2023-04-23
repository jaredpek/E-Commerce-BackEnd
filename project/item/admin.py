from django.contrib import admin
from item.models import ItemType, Item

admin.site.register([ItemType, Item])
