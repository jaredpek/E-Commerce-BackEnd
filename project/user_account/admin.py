from django.contrib import admin
from user_account import models

# Register your models here.
admin.site.register([
    models.Profile,
])