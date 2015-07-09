from django.views import generic
from django.conf import settings
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError

import logging
chat_log = logging.getLogger('chat')

# 3rd party imports
import redis

# local imports
from .models import Page, Store


class IndexView(generic.ListView):
    template_name = 'stores/zVossen/index.html'
    context_object_name = 'stores'

    def get_queryset(self):
        return Page.objects.all()[:5]

    def get_search_context(self):
        return {
            'person': ['name', 'nationality', 'age'],
            'store': ['name', 'address', 'phone'],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_context'] = self.get_search_context()
        return context


class DetailView(generic.DetailView):

    model = Store

    @property
    def template_name(self):
        store = self.get_object()
        return 'stores/{}/index.html'.format(store.theme if store.theme else settings.DEFAULT_TEMPLATE)


@csrf_exempt
def chatter(request):
    try:
        sessionid = request.POST.get('sessionid')
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        r.publish('stores_chat', sessionid + ': ' + request.POST.get('message'))
        return HttpResponse('Everything worked!')
    except Exception as e:
        return HttpResponseServerError(str(e))
