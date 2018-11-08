from django.db import models


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.pk, filename)


class User(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    avatar = models.ImageField(blank=True, upload_to=user_directory_path)
    bio = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=255)
    relationship_status = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email
