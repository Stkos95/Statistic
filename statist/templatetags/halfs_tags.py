from django import template


register = template.Library()

@register.filter()
def half_list(halfs: int):
    return range(1, halfs + 1)