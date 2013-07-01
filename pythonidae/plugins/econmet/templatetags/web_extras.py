from django import template

register = template.Library()

@register.filter
def getkey(value, arg):
    try:
        if value[arg]:
            return value[arg]
        return ""
    except:
        return "" 

@register.filter
def isModel(value):
    try:
        if value.__module__ == 'django.db.models.query':
            return True
        return False
    except:
        return type(value) == type([])

@register.filter
def isList(value):
    if type(value) == type([]):
        return True
    return False

@register.filter
def isDict(value):
    if type(value) == type({}):
        return True
    return False

