from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(get_user_model, on_delete=models.CASCADE)
    dob = models.DateField()
    avatar = models.ImageField(blank=True, upload_to='avatars/{}/'.format(user.username))
    bio = models.CharField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
