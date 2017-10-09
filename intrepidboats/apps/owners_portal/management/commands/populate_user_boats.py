from os.path import join, basename

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.timezone import datetime
from environ import environ

from intrepidboats.apps.boats.models import Boat
from intrepidboats.apps.owners_portal.models import UserBoat, BoatPhase


class Command(BaseCommand):
    help = 'Create boats and boat groups'

    objects = {
        "Fancy Dolphin": {
            "boat_name": "245 Center Console",
            "user_name": "admin",
            "design": "design.png",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt",
            "boat_step": {
                "title": "Build phase",
                "phase": {
                    "title": "The MECHANICS",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt",
                },
                "images": {
                    "boat-01.jpg": {
                        "vimeo_code": "200855282"
                    },
                    "boat-02.jpg": {},
                    "boat-03.jpg": {},
                }
            },
            "manuals": [
                {"title": "Devartis link", "link": "http://www.intrepidboats.com"},
                {"title": "Intrepidboats link", "link": "https://devartis.com"},
            ]
        },
    }

    def handle(self, *args, **options):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "boats")

        for boat_name, attrs in self.objects.items():
            boat = Boat.objects.get(title=attrs["boat_name"])
            admin_user = get_user_model().objects.get(username=attrs["user_name"])
            design_path = join(files_path, attrs["design"], )
            with open(design_path, "rb") as design:
                user_boat = UserBoat.objects.create(
                    name=boat_name,
                    user=admin_user,
                    boat=boat,
                    design=ContentFile(design.read(), basename(design_path)),
                    notes=attrs["notes"]
                )
                step = attrs["boat_step"]
                self.create_steps(user_boat, step)

    def create_steps(self, user_boat, step):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "boats")
        phase_attrs = step['phase']

        for index in range(4):
            phase, _ = BoatPhase.objects.get_or_create(
                title="%s %s" % (phase_attrs['title'], index),
                defaults={
                    "description": phase_attrs['description'],
                }
            )
            boat_step = user_boat.steps.create(
                title=step["title"] + " " + str(index),
                description="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore "
                            "eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt "
                            "in culpa qui officia deserunt mollit anim id est laborum.",
                phase=phase,
                start_date=datetime.now()
            )
            for image, asset_attrs in step["images"].items():
                asset_path = join(files_path, image)
                with open(asset_path, "rb") as asset_image:
                    boat_step.assets.create(
                        image=ContentFile(asset_image.read(), basename(asset_path)),
                        vimeo_video_code=asset_attrs.get("vimeo_code", None)
                    )

        first_step = user_boat.steps.first()
        first_step.active = True
        first_step.save()
