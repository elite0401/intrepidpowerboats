from django.conf.urls import url

from .views import SharedTestimonialCreateView, create_upload_ticket, complete_upload_ticket

urlpatterns = [
    url(r'^shared_testimonial/$', SharedTestimonialCreateView.as_view(), name="shared_testimonials"),
    url(r'^create_ticket/$', create_upload_ticket, name="create_ticket"),
    url(r'^complete_ticket/(?P<ticket_id>\w+)/$', complete_upload_ticket, name="complete_ticket"),
]
