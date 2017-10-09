from __future__ import unicode_literals

from django.db import migrations


def delete_general_features(apps, schema_editor):
    BoatGeneralFeature = apps.get_model('boats', 'BoatGeneralFeature')
    for general_feature in BoatGeneralFeature.objects.all():
        general_feature.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('boats', '0032_add_length_to_boats'),
    ]

    operations = [
        migrations.RunPython(delete_general_features)
    ]
