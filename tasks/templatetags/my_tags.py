from django import template
from ..models import Task


register = template.Library()


@register.simple_tag
def get_dates():
    return Task.dates.all()