from django.apps import AppConfig


class BoatsConfig(AppConfig):
    name = 'intrepidboats.apps.boats'

    def ready(self):
        from . import signals
