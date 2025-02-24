# miapp/templatetags/custom_filters.py
from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def get_item(dictionary, key):
    return  dictionary.get(key)

