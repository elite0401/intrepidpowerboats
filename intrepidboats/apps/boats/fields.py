from django.conf import settings
from django.db.models import ImageField


class BoatImageField(ImageField):
    def __init__(self, **kwargs):
        defaults = {
            "blank": False,
            "null": False,
            "upload_to": settings.BOAT_CONFIG['BOAT_IMAGES'],
        }
        params = {**defaults, **kwargs}
        super(BoatImageField, self).__init__(**params)
