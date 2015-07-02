from django import forms

# local imports
from .models import Contact, Person
from .widgets import GoogleMapWidget, FilesWidget_ImagesWidget


class ModelFormByStore(forms.ModelForm):

    rel_field_model_map = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.current_user.is_superuser:
            if 'store' in self.fields:
                self.fields['store'].queryset = self.current_user.site_set
            for field, model in self.rel_field_model_map.iteritems():
                self.fields[field].queryset = model.objects.filter(
                    store__in=self.current_user.site_set.all)


class HiddenFieldsForm(ModelFormByStore):
    hidden_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.hidden_fields:
            self.fields[f].widget = forms.HiddenInput()


class ContactAdminForm(HiddenFieldsForm):

    hidden_fields = ['latitude', 'longitude', 'zoom', 'heading', 'pitch']

    google_map = forms.Field(
        widget=GoogleMapWidget(
            data={
                'elem_id': 'map_canvas',
                'source_elem_id': 'id_address',
                'elem_inline_styles': ['width:380px;', 'height:200px;', 'margin-right:20px;', ],
                'has_pano': True,
            }
        ), required=False)

    class Meta:
        model = Contact
        fields = '__all__'


class PersonAdminForm(HiddenFieldsForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'images': FilesWidget_ImagesWidget(),
        }
