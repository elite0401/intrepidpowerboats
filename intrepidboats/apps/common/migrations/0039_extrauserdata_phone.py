
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0036_article_video'),
    ]

    operations = [
    	migrations.AddField(
            model_name='extrauserdata',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Phone number'),
        ),
    ]
