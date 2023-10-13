from django import template
import re

register = template.Library()

@register.filter(name='js_variable_name')
def js_variable_name(value):
    # Replace spaces with underscores to be fit for a javascript variable
    return re.sub(r'[^a-zA-Z0-9_]', '_', value).strip('_')
