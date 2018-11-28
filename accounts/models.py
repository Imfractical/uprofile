from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


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


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, help_text="Your email address")
    first_name = models.CharField(max_length=50, help_text="Your given name")
    last_name = models.CharField(max_length=50, help_text="Your surname")
    dob = models.DateField(help_text="Your birthday")
    avatar = models.ImageField(
        blank=True,
        upload_to='avatars/',
        help_text="A profile image used to represent you! Pick something nice",
    )
    bio = models.CharField(max_length=1000, blank=True, help_text="Tell us your life story")
    location = models.CharField(max_length=100, blank=True, help_text="Where do you live?")
    relationship = models.CharField(max_length=100, blank=True, help_text="Who are you seeing?")

    objects = UserManager()

    # Implementation details for AbstractBaseUser

    USERNAME_FIELD = 'email'
    REQUIRED = ['first_name', 'last_name', 'dob']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name
