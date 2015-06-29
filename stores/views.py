from django.views import generic

from .models import Page


class IndexView(generic.ListView):
    template_name = 'stores/techgut/index.html'
    context_object_name = 'stores'

    def get_queryset(self):
        return Page.objects.all()[:5]
