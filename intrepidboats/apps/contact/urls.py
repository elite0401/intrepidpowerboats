from django.conf.urls import url
from django.views.generic import TemplateView

from intrepidboats.apps.contact.views import SendResumeView, SendInquiryView

urlpatterns = [
    url(r'^send_resume/$', SendResumeView.as_view(), name="send_resume"),
    url(r'^send_inquiry/$', SendInquiryView.as_view(), name="send_inquiry"),
    url(r'^success/$', TemplateView.as_view(template_name='contact/success.html'), name="contact_success"),
    url(r'^careers/success/$', TemplateView.as_view(template_name='contact/careers_success.html'), name="careers_success"),
]
