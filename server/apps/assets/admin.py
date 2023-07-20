from django.contrib import admin
from guardian.admin import GuardedModelAdminMixin

from apps.assets.models import Image, Favorite
# Register your models here.


@admin.register(Image)
class ImageAdmin(GuardedModelAdminMixin, admin.ModelAdmin):
    list_display = ['slug', 'source', 'owner', 'created', 'updated']
    # exclude = ['slug']


@admin.register(Favorite)
class FavoriteAdmin(GuardedModelAdminMixin, admin.ModelAdmin):
    list_display = ['owner', 'image', 'created']
