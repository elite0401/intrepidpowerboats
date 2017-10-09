import os
import datetime

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from intrepidboats.apps.common.models import Event


class Command(BaseCommand):
    help = "Create events for Events page"

    events = {
        'Toronto Boat Show': {
            'external_link': 'http://www.torontoboatshow.com/',
            'date': datetime.datetime(2018, 1, 22),
        },
        'Miami Boat Show': {
            'external_link': 'http://www.miamiboatshow.com/',
            'date': datetime.datetime(2017, 10, 19),
        },
        'The Boat event': {
            'external_link': 'http://google.com/',
            'date': datetime.datetime(2017, 7, 7),
        },
        'More boats': {
            'external_link': 'http://www.seattleboatshow.com/',
            'date': datetime.datetime(2017, 4, 3),
        },
        'Boats and water': {
            'external_link': 'http://www.londonboatshow.com/',
            'date': datetime.datetime(2017, 5, 13),
        },
        'Boats, boats and boats': {
            'external_link': 'http://www.vancouverboatshow.ca/',
            'date': datetime.datetime(2017, 9, 3),
        },
    }

    def handle(self, *args, **options):
        for title, attrs in self.events.items():
            Event.objects.get_or_create(
                title=title,
                description=self.get_description(),
                image=self.set_image(),
                date=attrs['date'],
                external_link=attrs['external_link'],
            )

    def set_image(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_url = os.path.join(dir_path, 'blog_post_images', 'event_image.jpg')

        with open(image_url, "rb") as an_image:
            return ContentFile(an_image.read(), os.path.basename(image_url))

    def get_description(self):
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ne in odium veniam, si amicum destitero " \
               "tueri. Commoda autem et incommoda in eo genere sunt Lorem ipsum dolor sit amet, consectetur " \
               "adipiscing elit. Ne in odium veniam, si amicum destitero tueri. Commoda autem.Lorem ipsum dolor sit " \
               "amet, consectetur adipiscing elit."
