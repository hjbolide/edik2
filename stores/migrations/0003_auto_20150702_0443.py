# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topnotchdev.files_widget.fields
import datetime
import django.utils.timezone
import django_countries.fields
from django.utils.timezone import utc
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('stores', '0002_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('phone', models.CharField(max_length=10, blank=True, null=True)),
                ('mobile', models.CharField(max_length=10, blank=True, null=True)),
                ('email', models.EmailField(max_length=75, blank=True, null=True)),
                ('address', models.CharField(max_length=125)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('zoom', models.IntegerField(blank=True, null=True)),
                ('heading', models.FloatField(blank=True, null=True)),
                ('pitch', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('date_of_birth', models.DateField()),
                ('images', topnotchdev.files_widget.fields.ImagesField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RosterRule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('week_mask', models.IntegerField(default=0)),
                ('date', models.DateField(blank=True, null=True)),
                ('person', models.ForeignKey(to='stores.Person', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='store',
            field=models.ForeignKey(to='stores.Store', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='text',
            field=models.CharField(max_length=50, default=datetime.datetime(2015, 7, 2, 4, 43, 49, 756381, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='store',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='store',
            name='theme',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rosterrule',
            name='store',
            field=models.ForeignKey(to='stores.Store', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='store',
            field=models.ForeignKey(to='stores.Store', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='contact',
            name='store',
            field=models.ForeignKey(to='stores.Store', null=True, blank=True),
        ),
    ]
