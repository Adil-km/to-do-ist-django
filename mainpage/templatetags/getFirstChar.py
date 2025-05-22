from django import template

register = template.Library()

@register.filter
def getFirstChar(username):
    if username:
        return username[0].upper()
    return ''