from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.contrib.auth.models import User

from functools import wraps
from itertools import groupby

from .models import Page, Store, Person, Contact
from .forms import PersonAdminForm, ContactAdminForm, RosterAdminForm
from .view_models import PersonAdminViewModel


def filter_by_store(request, queryset):
    if request.user.is_superuser:
        return queryset
    return queryset.filter(store__in=request.user.store_set.all)


def superuser_only_view(original_func):
    """
    Decorator for views that are only available for superuser.
    Otherwise it will redirect to the index page.
    """
    @wraps(original_func, assigned=available_attrs(original_func))
    def new_func(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return original_func(self, request, *args, **kwargs)
        return HttpResponseRedirect('/admin')
    return new_func


class StoreBaseAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        form.current_user = request.user
        return form

    def get_queryset(self, request):
        return filter_by_store(request, super().get_queryset(request))


class AdminOnlyModel(admin.ModelAdmin):

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if request.user.is_superuser:
            return perms
        return {}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        queryset.delete()
        return queryset

AdminOnlyModel.changelist_view = superuser_only_view(AdminOnlyModel.changelist_view)
AdminOnlyModel.add_view = superuser_only_view(AdminOnlyModel.add_view)
AdminOnlyModel.history_view = superuser_only_view(AdminOnlyModel.history_view)
AdminOnlyModel.delete_view = superuser_only_view(AdminOnlyModel.delete_view)
AdminOnlyModel.change_view = superuser_only_view(AdminOnlyModel.change_view)


class StoreAdmin(AdminOnlyModel):
    pass


class PersonAdmin(StoreBaseAdmin):
    list_display = ('full_name', 'date_of_birth', 'country')
    form = PersonAdminForm


class ContactAdmin(StoreBaseAdmin):
    list_display = ('store_name', 'address', 'phone', 'mobile', 'email')
    form = ContactAdminForm


class RosterAdmin(StoreBaseAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^.*/$', self.admin_site.admin_view(self.my_view, cacheable=True)),
        ]

        return my_urls + urls

    def my_view(self, request):
        user = User.objects.get(username=request.user.username)
        store = user.store_set.all()[0]
        people = Person.objects.filter(store=store)
        context = dict(
            self.admin_site.each_context(request),
            key="hello",
            people=people,
            store=store,
        )

        return TemplateResponse(request, 'admin/roster.html', context)


RosterAdmin.add_view = superuser_only_view(RosterAdmin.add_view)
RosterAdmin.delete_view = superuser_only_view(RosterAdmin.delete_view)



admin.site.register(Page)
admin.site.register(Store, StoreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(PersonAdminViewModel, RosterAdmin)
