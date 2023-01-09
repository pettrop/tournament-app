from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=255, unique=True)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

