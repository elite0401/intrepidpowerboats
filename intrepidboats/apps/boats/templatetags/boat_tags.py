from django import template

from django.conf import settings

# pylint:disable=C0103
register = template.Library()


@register.filter
def get_range(value):
    return range(value)


@register.filter
def slide_index(photo_index, page_index):
    return photo_index + settings.THUMBNAILS_PER_PAGE * page_index
