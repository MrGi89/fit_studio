from django import template

register = template.Library()


@register.filter()
def show_index(value, arg):
    return value + (arg - 1) * 10
