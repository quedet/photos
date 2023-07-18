from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from guardian.shortcuts import assign_perm

from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

from server.utils import generate_identifier

from django.utils.text import slugify


class Image(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    source = models.ImageField(upload_to='images')
    alt = models.CharField(max_length=255, null=True, blank=True)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assets')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = generate_identifier()

        self.alt = self.source

        if update_fields is not None and 'source' in update_fields:
            update_fields = {"alt"}.union(update_fields)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created'])
        ]


@receiver(post_save, sender=Image)
def image_post_create(sender, instance, created, **kwargs):
    """
    Assign permission for all newly created image instances.
    """
    if created and instance.owner.username != settings.ANONYMOUS_USER_NAME:
        owner = User.objects.get(email=instance.owner.email)
        permissions = ['assets.add_image', 'assets.change_image',
                       'assets.delete_image', 'assets.view_image']
        for perm in permissions:
            assign_perm(perm, owner, instance)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)

        if update_fields is not None and 'name' in update_fields:
            update_fields = {"slug"}.union(update_fields)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        indexes = [
            models.Index(fields=['slug'])
        ]


class TaggedItem(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='items')
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='tags')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
