from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from guardian.shortcuts import assign_perm

# Create your models here.


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Create favorite object while user registered
    """
    if created and instance.username != settings.ANONYMOUS_USER_NAME:
        permissions = ['auth.view_user', 'auth.change_user',
                       'auth.delete_user', 'auth.add_user']

        for perm in permissions:
            assign_perm(perm, instance, instance)
