# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RosterDate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='roster',
            name='person',
        ),
        migrations.RemoveField(
            model_name='roster',
            name='store',
        ),
        migrations.CreateModel(
            name='PersonAdminViewModel',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('stores.person',),
        ),
        migrations.AddField(
            model_name='person',
            name='roster',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Roster',
        ),
        migrations.AddField(
            model_name='rosterdate',
            name='person',
            field=models.ForeignKey(to='stores.Person', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rosterdate',
            name='store',
            field=models.ForeignKey(to='stores.Store', null=True, blank=True),
        ),
    ]
