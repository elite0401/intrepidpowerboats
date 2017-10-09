import re

from django.conf import settings
from django_mobile import set_flavour
from django_mobile.middleware import MobileDetectionMiddleware


class MobileTabletDetectionMiddleware(MobileDetectionMiddleware):
    user_agents_android_search = u"(?:android)"
    user_agents_mobile_search = u"(?:mobile)"
    user_agents_tablets_search = u"(?:%s)" % u'|'.join(('ipad', 'tablet', ))

    def __init__(self):
        super(MobileTabletDetectionMiddleware, self).__init__()
        self.user_agents_android_search_regex = re.compile(self.user_agents_android_search,
                                                           re.IGNORECASE)
        self.user_agents_mobile_search_regex = re.compile(self.user_agents_mobile_search,
                                                          re.IGNORECASE)
        self.user_agents_tablets_search_regex = re.compile(self.user_agents_tablets_search,
                                                           re.IGNORECASE)

    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')
        is_tablet = False

        if user_agent:
            is_ipad = self.user_agents_tablets_search_regex.search(user_agent)

            is_android = self.user_agents_android_search_regex.search(user_agent)
            is_not_mobile = not self.user_agents_mobile_search_regex.search(user_agent)
            is_android_tablet = is_android and is_not_mobile

            is_tablet = is_ipad or is_android_tablet

        if is_tablet:
            set_flavour(settings.FLAVOURS[2], request)
        else:
            super(MobileTabletDetectionMiddleware, self).process_request(request)
