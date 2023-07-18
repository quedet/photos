from django.template import Library
from apps.assets.models import Image

register = Library()


@register.filter
def get_date(value):
    return value[0].created
