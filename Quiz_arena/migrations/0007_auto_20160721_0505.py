# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-21 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_arena', '0006_auto_20160720_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='options',
            name='option_status',
            field=models.SmallIntegerField(default=0),
        ),
    ]
