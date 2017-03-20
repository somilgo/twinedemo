# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='permission.SystemUser')),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='permission.SystemUser')),
                ('jobs', models.ManyToManyField(to='permission.Job', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='systemuser',
            name='jobs',
        ),
    ]
