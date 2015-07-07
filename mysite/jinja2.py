from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from jinja2 import Environment, environmentfilter, Markup

import json


def htmlsafe_dumps(value):
    return json.dumps(value)\
               .replace(u'<', u'\\u003c')\
               .replace(u'>', u'\\u003e')\
               .replace(u'&', u'\\u0026')\
               .replace(u"'", u'\\u0027')


@environmentfilter
def tojson(env, value):
    return Markup(htmlsafe_dumps(value))


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.filters['tojson'] = tojson
    return env
