# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import video.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', models.FileField(upload_to='glossvideo', verbose_name='video file')),
            ],
        )
    ]
