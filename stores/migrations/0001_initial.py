# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topnotchdev.files_widget.fields
import django.utils.timezone
import taggit.managers
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('phone', models.CharField(null=True, blank=True, max_length=10)),
                ('mobile', models.CharField(null=True, blank=True, max_length=10)),
                ('email', models.EmailField(null=True, blank=True, max_length=75)),
                ('address', models.CharField(max_length=125)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('zoom', models.IntegerField(null=True, blank=True)),
                ('heading', models.FloatField(null=True, blank=True)),
                ('pitch', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('date_of_birth', models.DateField()),
                ('images', topnotchdev.files_widget.fields.ImagesField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('week_mask', models.IntegerField(default=0)),
                ('date', models.DateField(null=True, blank=True)),
                ('person', models.ForeignKey(null=True, to='stores.Person', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('theme', models.CharField(null=True, blank=True, max_length=50)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='roster',
            name='store',
            field=models.ForeignKey(null=True, to='stores.Store', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='store',
            field=models.ForeignKey(null=True, to='stores.Store', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag', through='taggit.TaggedItem'),
        ),
        migrations.AddField(
            model_name='page',
            name='store',
            field=models.ForeignKey(null=True, to='stores.Store', blank=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='store',
            field=models.ForeignKey(null=True, to='stores.Store', blank=True),
        ),
    ]
