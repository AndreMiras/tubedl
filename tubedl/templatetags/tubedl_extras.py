from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def bootstrap_tags(value):
    """
    Makes Django tags compliant with Twitter Bootstrap 3 tags.
    """
    return 'danger' if value == 'error' else value
