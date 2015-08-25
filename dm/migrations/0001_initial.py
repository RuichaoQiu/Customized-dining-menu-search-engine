# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('full_address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('stars', models.CharField(max_length=200)),
                ('longitude', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
