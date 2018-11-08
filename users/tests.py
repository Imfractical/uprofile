from datetime import date

from django.test import TestCase

from .models import User


class UserTests(TestCase):
    def setUp(self):
        User.objects.create(
            email='bob@bob.com',
            password='Mikey9',
            first_name='Bob',
            last_name='Bobbert',
            dob=date(1955, 3, 14),
        )
        User.objects.create(
            email='rosaline@notyourbusiness.com',
            password='hunter2',
            first_name='Lisa',
            last_name='Leased',
            dob=date(2015, 12, 25),
        )
