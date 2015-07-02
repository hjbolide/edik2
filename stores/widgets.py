from django import forms
from django.conf import settings
from django.template import loader

# 3rd party imports
from topnotchdev.files_widget.forms.widgets import ImagesWidget


class GoogleMapWidget(forms.Widget):

    template_name = 'admin/google_map.html'

    class Media:
        js = (
            settings.GOOGLE_MAPS_URL % settings.GOOGLE_MAPS_API_KEY,
            'stores/js/gmap.js'
        )

    def __init__(self, attrs=None, data=None):
        super().__init__(attrs=attrs)
        self.data = data

    def _get_options(self, defaults, options):
        return {x: options.get(x, y) for x, y in defaults}

    def get_map_options(self, options):

        lat, lng = settings.DEFAULT_MAP_CENTRE

        defaults = [('lat', lat),
                    ('lng', lng),
                    ('zoom', settings.DEFAULT_MAP_ZOOM),
                    ('reflect_longitude_elem_id', 'id_longitude'),
                    ('reflect_latitude_elem_id', 'id_latitude'),
                    ('reflect_zoom_elem_id', 'id_zoom')]
        return self._get_options(defaults, options)

    def get_pano_options(self, options):

        defaults = [('heading', 0),
                    ('pitch', 0),
                    ('reflect_heading_elem_id', 'id_heading'),
                    ('reflect_pitch_elem_id', 'id_pitch')]
        return self._get_options(defaults, options)

    def make_map_context(self, attrs=None):
        return self.build_attrs(
            attrs,
            elem_id=self.data.get('elem_id', 'map_canvas'),
            source_elem_id=self.data.get('source_elem_id', 'id_address'),
            map_options=self.get_map_options(self.data.get('map_options', {})),
            has_pano=self.data.get('has_pano', True),
            pano_options=self.get_pano_options(self.data.get('pano_options', {})),
            elem_inline_styles=self.data.get('elem_inline_styles', None))

    def render(self, name, value, attrs=None):
        context = self.make_map_context(attrs=attrs)
        return loader.render_to_string(self.template_name, context)


class WeekMaskWidget(forms.CheckboxSelectMultiple):

    CHOICES = (
        (0b00000001, 'Monday'),
        (0b00000010, 'Tuesday'),
        (0b00000100, 'Wednesday'),
        (0b00001000, 'Thursday'),
        (0b00010000, 'Friday'),
        (0b00100000, 'Saturday'),
        (0b01000000, 'Sunday'),
    )

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, choices=self.CHOICES)

    def render(self, name, value, attrs=None, choices=()):
        from .util import get_week
        data = get_week(value)
        return super().render(name, data, attrs=attrs, choices=choices)

    def value_from_datadict(self, data, files, name):
        days = super().value_from_datadict(data, files, name)
        result = 0
        if not days:
            return result
        for d in days:
            result |= d
        return result


class FilesWidget_ImagesWidget(ImagesWidget):

    @property
    def is_hidden(self):
        return False
