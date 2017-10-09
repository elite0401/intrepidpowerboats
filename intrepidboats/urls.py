from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from decorator_include import decorator_include
from machina.app import board

from intrepidboats.apps.common.admin import UserAdmin
from intrepidboats.sitemap import SITEMAPS

admin.autodiscover()
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

urlpatterns = [
    url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^403/$', TemplateView.as_view(template_name="403.html")),
    url(r'^500/$', TemplateView.as_view(template_name="500.html")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^owners_portal/forum/', decorator_include(login_required, board.urls)),
    url(r'^owners_portal/', include("intrepidboats.apps.owners_portal.urls", namespace="owners_portal")),
    url(r'^intrepid-difference/', include('intrepidboats.apps.difference.urls', namespace="difference")),
    url(r'^contact/', include('intrepidboats.apps.contact.urls', namespace="contact")),
    url(r'', include('intrepidboats.apps.common.urls', namespace="common")),
    url('^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include("cms.urls")),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
