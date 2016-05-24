import re
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


@register.simple_tag(takes_context=True)
def active(context, pattern):
    try:
        request = context['request']
    except KeyError:
        # fails silently
        return ''
    if pattern == '/':
        if pattern == request.path:
            return 'active'
    elif re.search(pattern, request.path):
        return 'active'
    return ''
