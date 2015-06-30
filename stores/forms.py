from django import forms


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
