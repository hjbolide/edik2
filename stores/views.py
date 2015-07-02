from django.views import generic
from django.conf import settings

from .models import Page, Store


class IndexView(generic.ListView):
    template_name = 'stores/techgut/index.html'
    context_object_name = 'stores'

    def get_queryset(self):
        return Page.objects.all()[:5]


class DetailView(generic.DetailView):

    model = Store

    @property
    def template_name(self):
        store = self.get_object()
        return 'stores/{}/index.html'.format(store.theme if store.theme else settings.DEFAULT_TEMPLATE)
