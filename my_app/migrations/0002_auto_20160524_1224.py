# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='tag',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='num_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to=b'uploads/'),
        ),
    ]
