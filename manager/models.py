from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    def get_absolute_url(self):
        return reverse('users_list')

    def __str__(self):
        return f'{self.get_full_name()}'
