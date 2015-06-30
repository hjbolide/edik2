# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 6, 30, 0, 43, 3, 408085, tzinfo=utc), blank=True)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 6, 30, 0, 43, 3, 408108, tzinfo=utc), blank=True)),
                ('theme', models.CharField(max_length=50, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
