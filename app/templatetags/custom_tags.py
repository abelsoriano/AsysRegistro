# en tu archivo templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter(name='extract_id')
def extract_id(value):
    parts = value.split()
    for part in parts:
        if part.startswith('miembro_id:'):
            return part.split(':')[1]
    return None
