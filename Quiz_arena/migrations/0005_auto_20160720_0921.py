# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-20 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_arena', '0004_auto_20160720_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='options',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='number_of_questions',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='user_info',
            name='quizes',
        ),
        migrations.AddField(
            model_name='options',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Quiz_arena.questions'),
        ),
        migrations.AddField(
            model_name='questions',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Quiz_arena.quiz'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='creater',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Quiz_arena.user_info'),
        ),
    ]
