from django import template
from django.contrib.auth.models import User, Group

from ..models import Task


register = template.Library()


@register.simple_tag
def get_dates():
    return Task.dates.all()

@register.filter
def is_in_group(user, group):
    try:
        gr = Group.objects.get(name=group)
    except Group.DoesNotExist:
        print('dont')
        return False

    return gr in user.groups.all()
