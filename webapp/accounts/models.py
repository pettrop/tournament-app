from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import Model
#from ..tournaments.models import Club


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=255, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25)
    #club = models.CharField(max_length=64, choices=list([club for club in Club.club_name.]))

    def __str__(self):
        return self.user.email
