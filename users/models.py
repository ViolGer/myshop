from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user', 'first_name', 'last_name']

    def __str__(self):
        return self.email

# Create your models here.
