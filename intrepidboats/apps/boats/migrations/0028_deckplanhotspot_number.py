# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-09 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0027_merge_20170609_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckplanhotspot',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number displayed on top of hotspot'),
        ),
    ]