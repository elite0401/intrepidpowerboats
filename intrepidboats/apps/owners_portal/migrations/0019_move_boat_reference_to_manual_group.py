from __future__ import unicode_literals

from django.db import migrations


def move_boat_reference_to_manual_group(apps, schema_editor):
    UserBoat = apps.get_model('owners_portal', 'UserBoat')
    BoatManualGroup = apps.get_model('owners_portal', 'BoatManualGroup')
    for boat in UserBoat.objects.all():
        group = BoatManualGroup.objects.create(user_boat=boat, name='OPERATING YOUR INTREPID')
        for manual in boat.manuals.all():
            manual.group = group
            manual.save()


class Migration(migrations.Migration):
    dependencies = [
        ('owners_portal', '0018_auto_20170711_0946'),
    ]

    operations = [
        migrations.RunPython(move_boat_reference_to_manual_group)
    ]
