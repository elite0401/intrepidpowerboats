from django.apps import AppConfig


class OwnersPortalConfig(AppConfig):
    name = 'intrepidboats.apps.owners_portal'
    verbose_name = "Owners Portal"

    def ready(self):
        from . import signals
