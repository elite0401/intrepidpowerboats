# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-16 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owners_portal', '0010_auto_20170314_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedmedia',
            name='title',
        ),
        migrations.AddField(
            model_name='sharedmedia',
            name='comment',
            field=models.TextField(default='', verbose_name='comment'),
            preserve_default=False,
        ),
    ]