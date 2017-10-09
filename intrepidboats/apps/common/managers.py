from django.db.models import Manager


class PageAssetManager(Manager):
    def get_queryset(self):
        return super(PageAssetManager, self).get_queryset().filter(enabled=True)
