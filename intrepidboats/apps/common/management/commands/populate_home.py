import glob
from os.path import join, basename

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from environ import environ

from intrepidboats.apps.common.models import PageSetting, PageAsset


class Command(BaseCommand):
    help = 'Create home images and video slides'

    def handle(self, *args, **options):
        instance, created = PageSetting.objects.get_or_create(name=settings.HOME_PAGE_SETTINGS_NAME)
        if created:
            for image in self.get_images():
                self.create_page_asset(page=instance, enabled=True).image.save(image.name, image)
            for video_code in self.get_videos():
                self.create_page_asset(page=instance, vimeo_video_code=video_code, enabled=True)
            self.create_page_asset(page=instance, vimeo_video_code=self.get_last_video_code(), enabled=True,
                                   is_last=True)

    def create_page_asset(self, **kwargs):
        return PageAsset.objects.create(**kwargs)

    def get_images(self):
        this_dir = environ.Path(__file__) - 1
        images = []
        for path in glob.glob(join(str(this_dir), "images/*")):
            with open(path, "rb") as a_file:
                images.append(ContentFile(a_file.read(), basename(path)))
        return images

    def get_videos(self):
        return [
            "200855282",
            "200855313"
        ]

    def get_last_video_code(self):
        return "200855260"
