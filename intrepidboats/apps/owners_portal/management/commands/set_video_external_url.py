from django.core.management import BaseCommand
from django.db.models import Q

from intrepidboats.apps.common.utils import get_external_url
from intrepidboats.apps.owners_portal.models import SharedVideo


class Command(BaseCommand):
    help = 'Obtain video external url from Vimeo'

    def handle(self, *args, **options):
        gallery_videos = SharedVideo.objects.exclude(Q(video_id__exact='') | Q(video_id__isnull=True)).filter(
            Q(video_external_url__exact='') | Q(video_external_url__isnull=True))
        for video in gallery_videos:
            video.video_external_url = get_external_url(video.video_id)
            if video.video_external_url:
                video.completed = True
            video.save()
