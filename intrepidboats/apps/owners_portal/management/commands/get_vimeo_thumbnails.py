from urllib.request import urlopen
import urllib.parse

import requests
from requests.exceptions import HTTPError
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management import BaseCommand
from django.template.defaultfilters import slugify

from intrepidboats.apps.boats.models import Video
from intrepidboats.apps.difference.models import SharedTestimonial
from intrepidboats.apps.owners_portal.models import SharedVideo
from intrepidboats.libs.vimeo_rate_limiting.models import VimeoRateLimiting


class Command(BaseCommand):
    help = 'Obtain video thumbnails from Vimeo'

    def handle(self, *args, **options):
        gallery_videos_no_thumb = SharedVideo.objects.filter(completed=True, thumbnail='')
        testimonial_videos_no_thumb = SharedTestimonial.objects.filter(video_id__isnull=False, thumbnail='')
        boat_model_videos_no_thumb = Video.objects.filter(thumbnail='') | Video.objects.filter(thumbnail__isnull=True)

        for video in gallery_videos_no_thumb:
            thumbnail_file = self.get_vimeo_thumbnail(video.video_id)
            if thumbnail_file:
                video.thumbnail.save(self.generate_filename(video.comment), thumbnail_file)
                video.save()

        for testimonial in testimonial_videos_no_thumb:
            thumbnail_file = self.get_vimeo_thumbnail(testimonial.video_id)
            if thumbnail_file:
                testimonial.thumbnail.save(self.generate_filename(testimonial.message), thumbnail_file)
                testimonial.save()

        for video in boat_model_videos_no_thumb:
            thumbnail_file = self.get_vimeo_thumbnail(video.vimeo_video_code)
            if thumbnail_file:
                video.thumbnail.save(self.generate_filename(video.vimeo_video_code), thumbnail_file)
                video.save()

    def get_vimeo_thumbnail(self, vimeo_id):

        rate_limit_data = VimeoRateLimiting.get_instance()
        if not rate_limit_data.available_for_request():
            return None

        field = 'pictures'
        vimeo_api_url = settings.VIMEO_CONFIG['VIMEO_API_URL']
        videos_url = urllib.parse.urljoin(vimeo_api_url, 'videos')
        api_url = '{}/{}?fields={}'.format(videos_url, vimeo_id, field)
        headers = {"Authorization": "Bearer %s" % settings.VIMEO_CONFIG['PRO_UPLOAD_TOKEN']}
        response = requests.get(api_url, headers=headers)

        rate_limit_data.update_with(
            reset_time=response.headers._store['x-ratelimit-reset'][1],
            remaining_requests=response.headers._store['x-ratelimit-remaining'][1],
        )

        try:
            response.raise_for_status()
        except HTTPError:
            return None
        try:
            sizes = response.json()[field]['sizes']
            index = 3 if len(sizes) >= 4 else -1
            thumbnail_url = sizes[index]['link']
        except (TypeError, IndexError):
            return None
        return self.download_thumbnail(thumbnail_url)

    def download_thumbnail(self, url):
        img_temp = NamedTemporaryFile(delete=True)
        try:
            img_temp.write(urlopen(url).read())
        except HTTPError:
            return None
        img_temp.flush()
        return File(img_temp)

    def generate_filename(self, text_field):
        return '{}.jpg'.format(slugify(text_field)[:40])
