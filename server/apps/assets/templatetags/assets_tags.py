from django.template import Library
from apps.assets.models import Image

register = Library()


@register.filter
def get_date(value):
    return value[0].created


@register.filter
def get_size(value):
    size = round(value.size / (1024*1024), 2)
    return size


@register.filter
def get_name(value):
    name = str(value).split('images/')[1]
    return name


@register.filter
def get_action(value):
    action = 'mark'
    if value:
        action = 'unmark'

    return action
