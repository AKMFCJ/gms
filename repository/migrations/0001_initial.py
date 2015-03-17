# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('path', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateField()),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'repository_repository',
            },
            bases=(models.Model,),
        ),
    ]
