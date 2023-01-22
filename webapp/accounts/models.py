from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model

from tournaments.models import Club


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=255, unique=False)
    last_name = models.CharField(max_length=255, unique=False)
    username = models.CharField(max_length=255, blank=True, null=True, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.user.last_name, self.user.first_name)
