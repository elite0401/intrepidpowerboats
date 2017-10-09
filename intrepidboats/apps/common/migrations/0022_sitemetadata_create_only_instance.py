# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_only_instance(apps, schema_editor):
    apps.get_model('common', 'SiteMetaData').objects.create(page_title='Intrepid Powerboats')


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0021_sitemetadata'),
    ]

    operations = [
        migrations.RunPython(create_only_instance)
    ]
