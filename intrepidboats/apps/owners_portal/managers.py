from django.db import models

from polymorphic.managers import PolymorphicManager


class BoatStepManager(models.Manager):
    def for_user(self, user):
        return self.filter(user_boat__user=user)


class SharedMediaManager(PolymorphicManager):
    def media_content(self, attrs):
        from intrepidboats.apps.owners_portal.models import SharedPicture, SharedVideo
        pictures = self.instance_of(SharedPicture)
        videos = self.instance_of(SharedVideo).exclude(SharedVideo___completed=False)
        return (pictures | videos).filter(**attrs).order_by('-created')
