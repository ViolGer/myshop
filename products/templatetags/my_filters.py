from django import template

register = template.Library()

@register.filter(name="range")
def template_range(value):
    return range(value)

@register.filter(name="subtract")
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (TypeError, ValueError):
        return 0