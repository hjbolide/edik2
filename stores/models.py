from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 3rd party libs
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from topnotchdev import files_widget

# local import
from .util import get_week


class Store(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, blank=True, null=True)
    theme = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=50)
    store = models.ForeignKey(Store, blank=True, null=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = CountryField()
    date_of_birth = models.DateField()
    tags = TaggableManager()
    store = models.ForeignKey(Store, blank=True, null=True)
    images = files_widget.ImagesField(blank=True, null=True)
    roster = models.IntegerField(default=0)

    @property
    def full_name(self):
        split = ' '
        if not self.first_name:
            split = ''
        result = split.join([self.first_name,self.last_name])
        return result if result else 'NEW'

    def get_name_link(self):
        return """
        <a href="{%% static 'admin:stores_person_change' %s %%}">%s</a>
        """ % (self.id, self.full_name)

    def get_roster_content(self):
        content = ''
        for i in range(7):
            content += """
            <td><input type="checkbox" name="roster_day" value="{i}" {checked}/></td>
            """.format(
                i=1<<i,
                checked='checked="checked"' if 1<<i & self.roster != 0 else ''
            )
        return content

    def get_roster_row(self):
        return """
        <tr data-edik-elem="roster_{id}">
          <td>
            {name_link}
            <input type="hidden" name="person" value="{id}"/>
            <input type="hidden" name="roster" value="{roster}"/>
          </td>
          {roster_content}
        </tr>
        """.format(
            id=self.id,
            roster=self.roster,
            name_link=self.get_name_link(),
            roster_content=self.get_roster_content()
        )

    def __str__(self):
        return self.full_name


class RosterDate(models.Model):
    date = models.DateField(blank=True, null=True)
    person = models.ForeignKey(Person, blank=True, null=True)
    store = models.ForeignKey(Store, blank=True, null=True)

    def display_week(self):
        return ', '.join(get_week(self.week_mask, translate=True))


class Contact(models.Model):
    phone = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=75, blank=True, null=True)
    address = models.CharField(max_length=125)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    zoom = models.IntegerField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    pitch = models.FloatField(blank=True, null=True)
    store = models.ForeignKey(Store, blank=True, null=True)

    @property
    def store_name(self):
        return self.store.name if self.store else 'NEW STORE'

    def __str__(self):
        return self.address
