from cms.sitemaps import CMSSitemap
from django.contrib import sitemaps
from django.urls import reverse
from django.utils.text import slugify

from intrepidboats.apps.boats.models import Boat
from intrepidboats.apps.common.models import Article


class IntrepidSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"
    i18n = True

    def __init__(self, url_names):
        self.url_names = url_names

    def items(self):
        return self.url_names

    def location(self, item):
        return reverse(item)


class HomeSitemap(IntrepidSitemap):
    priority = 1.0
    changefreq = "daily"


class IntrepidStaticSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"
    i18n = True

    def __init__(self, urls):
        self.urls = urls

    def items(self):
        return self.urls

    def location(self, item):
        return item


class BoatSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Boat.objects.exclude(model_group=None)

    def location(self, item):
        return reverse('boats:boat_detail', args=(item.model_group.pk, item.slug,))


class ArticleSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Article.objects.all()

    def location(self, item):
        return reverse('common:article', args=(item.pk, slugify(item.title),))


class CustomCMSSitemap(CMSSitemap):
    priority = 0.6
    changefreq = "weekly"


SITEMAPS = {
    'home': HomeSitemap([
        'common:home',
    ]),
    'intrepid': IntrepidSitemap([
        'common:what-is-new', 'common:events',
        'common:register', 'common:login',
        'owners_portal:owners_portal',
    ]),
    'cmspages': CustomCMSSitemap,
    'intrepid-static': IntrepidStaticSitemap([
        '/contact/careers/', '/owners_portal/forum/',
    ]),
    'boats': BoatSitemap,
    'articles': ArticleSitemap,
}
