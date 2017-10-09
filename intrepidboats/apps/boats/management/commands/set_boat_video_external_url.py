from django.core.management import BaseCommand

from intrepidboats.apps.boats.models import Video
from intrepidboats.apps.common.utils import get_external_url


class Command(BaseCommand):
    help = 'Obtain video external url from Vimeo'

    def handle(self, *args, **options):
        for video in Video.objects.all():
            if video.vimeo_video_code:
                video.video_external_url = get_external_url(video.vimeo_video_code)
                video.save()
