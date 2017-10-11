# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-12 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0024_auto_20170512_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemetadata',
            name='description',
            field=models.CharField(max_length=1000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='sitemetadata',
            name='og_description',
            field=models.CharField(max_length=1000, verbose_name='Open graph: description'),
        ),
    ]