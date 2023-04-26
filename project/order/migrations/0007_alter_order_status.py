# Generated by Django 4.2 on 2023-04-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_completed_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Ordering'), (1, 'Processing'), (2, 'Delivering'), (3, 'Completed')], default=0),
        ),
    ]
