from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BoatsApphook(CMSApp):
    app_name = "boats"
    name = _("Boats Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["intrepidboats.apps.boats.urls"]


apphook_pool.register(BoatsApphook)
