from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        try:
            instance.groups.add(Group.objects.get(name='Bežný uživateľ'))
        except:
            pass


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
