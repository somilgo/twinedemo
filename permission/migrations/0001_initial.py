# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Job Title')),
                ('description', models.TextField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('first_name', models.CharField(default=b'', max_length=30, verbose_name=b'First Name')),
                ('last_name', models.CharField(default=b'', max_length=30, verbose_name=b'Last Name')),
                ('email', models.EmailField(default=b'', unique=True, max_length=255, verbose_name=b'Email Address')),
                ('user_type', models.CharField(default=b'R', max_length=1, choices=[(b'A', b'Admin'), (b'R', b'Recruiter')])),
                ('jobs', models.ManyToManyField(to='permission.Job', blank=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
