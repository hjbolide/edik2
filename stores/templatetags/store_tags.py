from django import template
import json

register = template.Library()


def htmlsafe_dumps(value):
    return json.dumps(value)\
               .replace(u'<', u'\\u003c')\
               .replace(u'>', u'\\u003e')\
               .replace(u'&', u'\\u0026')\
               .replace(u"'", u'\\u0027')


@register.filter(name="tojson")
def tojson(value, args=None):
    return htmlsafe_dumps(value)
