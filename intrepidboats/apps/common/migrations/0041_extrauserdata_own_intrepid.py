
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0039_extrauserdata_phone'),
    ]

    operations = [
    	migrations.AddField(
            model_name='extrauserdata',
            name='fan',
            field=models.BooleanField(default=False, verbose_name='Not Own Intrepid'),
        ),

        migrations.AddField(
            model_name='extrauserdata',
            name='intrepid_model',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Intrepid Model'),
        ),

        migrations.AddField(
            model_name='extrauserdata',
            name='intrepid_year',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Intrepid Year'),
        ),

        migrations.AddField(
            model_name='extrauserdata',
            name='intrepid_hull_id',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Intrepid Hull ID'),
        ),
    ]
