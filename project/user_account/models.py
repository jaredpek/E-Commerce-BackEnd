from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20, validators=[RegexValidator('^\+\d{6,20}$')])
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6, validators=[RegexValidator('^\d{6}$')])
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
