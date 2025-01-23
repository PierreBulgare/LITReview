from django import template

register = template.Library()

@register.filter(name='iteration')
def iteration(value):
    if isinstance(value, int):
        return range(value)
    
@register.filter(name='remaining_stars')
def remaining_stars(value):
    return range(5 - value)
