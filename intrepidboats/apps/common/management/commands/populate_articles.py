import os
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from intrepidboats.apps.common.models import Article


class Command(BaseCommand):
    help = "Create articles for What's new page"

    def handle(self, *args, **options):
        for title in self.get_titles():
            article, created = Article.objects.get_or_create(title=title)
            if created:
                article.description = self.get_description()
                article.featured = random.choice([True, False])
                self.set_image(article)
                article.save()

    def set_image(self, article):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_url = os.path.join(dir_path, 'blog_post_images', 'article_image.jpg')

        with open(image_url, "rb") as an_image:
            article.image = ContentFile(an_image.read(), os.path.basename(image_url))

    def get_titles(self):
        return ['Technology', 'New boats', 'The best boat', 'Safety in the water',
                'California Boat Show', 'Innovating Design', 'Miami Boat Show']

    def get_description(self):
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ne in odium veniam, si amicum destitero " \
               "tueri. Commoda autem et incommoda in eo genere sunt Lorem ipsum dolor sit amet, consectetur " \
               "adipiscing elit. Ne in odium veniam, si amicum destitero tueri. Commoda autem.Lorem ipsum dolor sit " \
               "amet, consectetur adipiscing elit. Ne in odium veniam, si amicum destitero tueri. Commoda autem et " \
               "incommoda in eo genere sunt Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ne in odium " \
               "veniam, si amicum destitero tueri. Commoda autem."
