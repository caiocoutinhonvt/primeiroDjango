from django import template
register = template.Library()
from django.template import defaultfilters

@register.filter
def replace(value):
    return value.replace(",",".")