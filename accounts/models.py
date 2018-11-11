from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    avatar = models.ImageField(blank=True, upload_to='avatars/')
    bio = models.CharField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=100, blank=True)

    # Implementation details for AbstractBaseUser
    USERNAME_FIELD = 'email'
    REQUIRED = ['first_name', 'last_name', 'dob']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, dob, password):
        new_user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )
        new_user.set_password(password)
        new_user.save()

    def create_superuser(self, email, first_name, last_name, dob, password):
        new_user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )
        new_user.set_password(password)
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.save()
