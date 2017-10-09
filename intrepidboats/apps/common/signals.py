from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from intrepidboats.apps.common.utils import get_external_url
from .models import PageAsset


# pylint:disable=W0613
@receiver(post_save, sender=PageAsset)
def set_external_url(sender, instance, created, **kwargs):
    if created and instance.vimeo_video_code:
        instance.video_external_url = get_external_url(instance.vimeo_video_code)
        instance.save()


# pylint:disable=W0613
@receiver(pre_save, sender=PageAsset)
def update_external_url(sender, instance, **kwargs):
    if instance.vimeo_video_code and instance.pk:
        vimeo_video_code_changed = PageAsset.objects.get(id=instance.id).vimeo_video_code != instance.vimeo_video_code
        if vimeo_video_code_changed:
            instance.video_external_url = get_external_url(instance.vimeo_video_code)
