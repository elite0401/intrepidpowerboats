from __future__ import unicode_literals

from django import template
from django.utils.encoding import iri_to_uri
from el_pagination import (
    settings,
    utils,
)

# pylint:disable=C0103
register = template.Library()


@register.inclusion_tag('blog_posts/more.html', takes_context=True)
def more(context, label=None, loading=settings.LOADING, class_name=None):
    """Show the link to get the next page in a Twitter-like pagination.

    Usage::

        {% show_more %}

    Alternatively you can override the label passed to the default template::

        {% show_more "even more" %}

    You can override the loading text too::

        {% show_more "even more" "working" %}

    You could pass in the extra CSS style class name as a third argument

       {% show_more "even more" "working" "class_name" %}

    Must be called after ``{% paginate objects %}``.
    """
    # This template tag could raise a PaginationError: you have to call
    # *paginate* or *lazy_paginate* before including the showmore template.
    data = utils.get_data_from_context(context)
    page = data['page']
    # show the template only if there is a next page
    if page.has_next():
        request = context['request']
        page_number = page.next_page_number()
        # Generate the querystring.
        querystring_key = data['querystring_key']
        querystring = utils.get_querystring_for_page(
            request, page_number, querystring_key,
            default_number=data['default_number'])
        return {
            'label': label,
            'loading': loading,
            'class_name': class_name,
            'path': iri_to_uri(data['override_path'] or request.path),
            'querystring': querystring,
            'querystring_key': querystring_key,
            'request': request,
        }
    # No next page, nothing to see.
    return {}
