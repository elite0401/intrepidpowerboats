from django.conf.urls import url

from .views import DashboardView, create_upload_ticket, complete_upload_ticket, StepFeedbackCreateView, \
    change_notification, EditBoatNameView, AccountSettingsView, UploadPictureView, GalleryView, get_slide

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name="owners_portal"),
    url(r'^gallery/$', GalleryView.as_view(), name="gallery"),
    url(r'^create_ticket/$', create_upload_ticket, name="create_ticket"),
    url(r'^complete_ticket/(?P<ticket_id>\w+)/$', complete_upload_ticket, name="complete_ticket"),
    url(r'^upload_picture/$', UploadPictureView.as_view(), name="upload_picture"),

    # Ajax!
    url(r'^steps/(?P<pk>\d+)/feedback/$', StepFeedbackCreateView.as_view(), name="step_feedback"),
    url(r'^edit_boat_name/(?P<pk>\d+)/$', EditBoatNameView.as_view(), name="edit_boat_name"),
    url(r'^account_settings/(?P<pk>\d+)/$', AccountSettingsView.as_view(), name="account_settings"),
    url(r'^steps/(?P<step_pk>\d+)/notify_change/$', change_notification, name="change_notification"),
    url(r'^get_slide/(?P<media_id>\d+)/$', get_slide, name="get_slide"),
]
