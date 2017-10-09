from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'intrepidboats.apps.common'

    def ready(self):
        from . import signals
