from django.conf.urls import url

from .views import BuildABoatView, BoatModelGroupListView, ModelPageHome, colorize, BoatLengthGroupDetailView, \
    BoatListPerGroupCompare, BoatModelListView, BoatListCompare, BuiltBoatEmailCreateView, BuiltBoatShareCreateView, \
    MotorsView, VideoView, AboutView, OptionalEquipmentView, DeckPlanView, FeaturesView

urlpatterns = [
    url(r'^$', BoatModelGroupListView.as_view(), name="all_boats"),

    # Use these with ajax!
    url(r'^boats/$', BoatModelListView.as_view(), name="boat_list"),
    url(r'^boats/compare/$', BoatListCompare.as_view(), name="compare_all_boats"),

    # Ajax per group!
    url(r'^boat_groups/(?P<pk>\w+)/$', BoatLengthGroupDetailView.as_view(), name="boat_group"),
    url(r'^boat_groups/(?P<pk>\w+)/boats/compare/$', BoatListPerGroupCompare.as_view(), name="compare_boats"),

    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/$', ModelPageHome.as_view(), name="boat_detail"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/build_a_boat/$', BuildABoatView.as_view(),
        name="build_a_boat"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/built-boat-email/$', BuiltBoatEmailCreateView.as_view(),
        name="built_boat_email"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/built-boat-share/$', BuiltBoatShareCreateView.as_view(),
        name="built_boat_share"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/motors/$', MotorsView.as_view(), name="motors"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/video/$', VideoView.as_view(), name="video"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/about/$', AboutView.as_view(), name="about"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/optional-equipment/$', OptionalEquipmentView.as_view(),
        name="optional-equipment"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/deck-plan/$', DeckPlanView.as_view(), name="deck-plan"),
    url(r'^boat_groups/(?P<group_pk>\w+)/boats/(?P<slug>[-\w]+)/features/$', FeaturesView.as_view(), name="features"),
    url(r'^(?P<slug>[-\w]+)/build_a_boat/(?P<image>[-\w]+)/color/(?P<color>[-\w]+)$', colorize, name="colorize"),

]
