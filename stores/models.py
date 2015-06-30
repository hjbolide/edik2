from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Page(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    created = models.DateTimeField(blank=True, default=timezone.now())
    modified = models.DateTimeField(blank=True, default=timezone.now())
    user = models.ForeignKey(User, blank=True)
    theme = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
