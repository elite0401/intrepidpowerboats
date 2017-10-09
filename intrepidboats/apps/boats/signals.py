from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from intrepidboats.apps.common.utils import get_external_url
from .models import Video


# pylint:disable=W0613
@receiver(post_save, sender=Video)
def set_boat_video_external_url(sender, instance, created, **kwargs):
    if created and instance.vimeo_video_code:
        instance.video_external_url = get_external_url(instance.vimeo_video_code)
        instance.save()


# pylint:disable=W0613
@receiver(pre_save, sender=Video)
def update_boat_video_external_url(sender, instance, **kwargs):
    if instance.vimeo_video_code and instance.pk:
        vimeo_video_code_changed = Video.objects.get(id=instance.id).vimeo_video_code != instance.vimeo_video_code
        if vimeo_video_code_changed:
            instance.video_external_url = get_external_url(instance.vimeo_video_code)
