from django.contrib import admin
from guardian.admin import GuardedModelAdminMixin

from apps.assets.models import Image, Tag
# Register your models here.


@admin.register(Image)
class ImageAdmin(GuardedModelAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'owner', 'created', 'updated']
    exclude = ['slug']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    exclude = ['slug']
