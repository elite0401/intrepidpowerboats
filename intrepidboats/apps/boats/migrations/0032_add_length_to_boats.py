from __future__ import unicode_literals

from django.db import migrations


def add_length_to_boats(apps, schema_editor):
    Boat = apps.get_model('boats', 'Boat')
    BoatModelGroup = apps.get_model('boats', 'BoatModelGroup')
    BoatLengthGroup = apps.get_model('boats', 'BoatLengthGroup')
    a_model_group = BoatModelGroup.objects.first()
    if a_model_group:
        img = a_model_group.show_image
        for boat in Boat.objects.all():
            length = boat.title.split(' ')[0]
            boat.length_group = BoatLengthGroup.objects.get_or_create(title=length, show_image=img)[0]
            boat.save()


class Migration(migrations.Migration):
    dependencies = [
        ('boats', '0031_auto_20170621_0929'),
    ]

    operations = [
        migrations.RunPython(add_length_to_boats)
    ]
