# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-20 06:40
from __future__ import unicode_literals

from django.db import migrations, models
import video.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20170423_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='videofile',
            field=models.FileField(storage=video.models.TaggedVideoStorage(), upload_to='glossvideo', verbose_name='video file'),
        ),
    ]
