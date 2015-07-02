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

    @property
    def full_name(self):
        split = ' '
        if not self.first_name:
            split = ''
        result = split.join([self.first_name,self.last_name])
        return result if result else 'NEW'

    def __str__(self):
        return self.full_name


class RosterRule(models.Model):
    week_mask = models.IntegerField(default=0)
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
