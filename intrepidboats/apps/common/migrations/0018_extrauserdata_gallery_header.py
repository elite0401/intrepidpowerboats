# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-28 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0017_auto_20170323_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrauserdata',
            name='gallery_header',
            field=models.ImageField(blank=True, null=True, upload_to='auth/gallery_headers/', verbose_name='Gallery header'),
        ),
    ]