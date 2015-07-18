from django.views import generic
from django.conf import settings
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

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

#    def get_queryset(self):
#        qs = super().get_queryset()
#        qs.prefetch_related('pages').prefetch_related('persons').prefetch_related('rosters')
#        return qs

    @property
    def template_name(self):
        store = self.get_object()
        return 'stores/{}/index.html'.format(store.theme if store.theme else settings.DEFAULT_TEMPLATE)


def page_view(request, storeid, page):
    store = Store.objects.get(pk=storeid)
    if not page:
        page = 'index'
    theme = store.theme if store.theme else settings.DEFAULT_TEMPLATE
    template = 'stores/{}/{}.html'.format(theme, page)
    return render(request, template, { "object": store })


@csrf_exempt
def chatter(request):
    try:
        sessionid = request.POST.get('sessionid')
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        r.publish('stores_chat', sessionid + ': ' + request.POST.get('message'))
        return HttpResponse('Everything worked!')
    except Exception as e:
        return HttpResponseServerError(str(e))
