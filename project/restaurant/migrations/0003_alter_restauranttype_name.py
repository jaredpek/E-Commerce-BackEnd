# Generated by Django 4.2 on 2023-04-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_restauranttype_restaurant_restaurant_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restauranttype',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]