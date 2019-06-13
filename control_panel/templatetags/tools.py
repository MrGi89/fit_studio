from django import template

register = template.Library()


@register.filter()
def member_index(value, arg):
    return value + (arg - 1) * 10
