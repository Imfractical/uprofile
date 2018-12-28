from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    dob = models.DateField(blank=True, null=True, help_text="Your birthday")
    avatar = models.ImageField(
        blank=True,
        upload_to='avatars/',
        help_text="A profile image used to represent you! Pick something nice",
    )
    bio = models.CharField(
        blank=True,
        max_length=1000,
        help_text="Tell us your life story",
        validators=[MinLengthValidator(10)],
    )
    location = models.CharField(blank=True, max_length=100, help_text="Where do you live?")
    relationship = models.CharField(blank=True, max_length=100, help_text="Who are you seeing?")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
