from os.path import join, basename
from environ import environ

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from ...models import SharedPicture, SharedVideo


class Command(BaseCommand):
    help = 'Create images and videos for user gallery'

    images = {"Image {}".format(index): "img-video-0{}.jpg".format(index) for index in range(1, 8)}
    videos = {
        "Video 1": "207677135",
        "Video 2": "207677748",
    }

    def handle(self, *args, **options):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "gallery")

        for is_public in (True, False):
            for _ in range(2):
                for title, filename in self.images.items():
                    image_path = join(files_path, filename)
                    with open(image_path, "rb") as an_image:
                        SharedPicture.objects.create(
                            uploader=get_user_model().objects.get(username="admin"),
                            title=title,
                            is_public=is_public,
                            is_approved=True,
                            image=ContentFile(an_image.read(), basename(image_path)),
                        )

            for title, vimeo_id in self.videos.items():
                SharedVideo.objects.create(
                    uploader=get_user_model().objects.get(username="admin"),
                    title=title,
                    is_public=is_public,
                    is_approved=True,
                    ticket_id="Unknown",
                    uri="Unknown",
                    vimeo_user="Unknown",
                    upload_link_secure="Unknown",
                    complete_uri="Unknown",
                    completed=True,
                    video_id=vimeo_id,
                )
