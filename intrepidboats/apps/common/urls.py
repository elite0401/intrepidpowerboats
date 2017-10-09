from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import logout, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import TemplateView

from .views import HomeView, NewsletterSubmission, activate_lang, WhatIsNewView, ArticleDetailView, \
    EventsView, RegistrationView, password_reset, login_view

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^newsletter_subscribe/$', NewsletterSubmission.as_view(), name="newsletter"),
    url(r'^newsletter_success/$', TemplateView.as_view(template_name='newsletter_success.html'),
        name="newsletter_success"),
    url(r'^activate_lang/$', activate_lang, name="activate_lang"),
    url(r'^what-is-new/$', WhatIsNewView.as_view(), name='what-is-new'),
    url(r'^article/(?P<pk>\d+)/(?P<title>[\w-]+)$', ArticleDetailView.as_view(), name='article'),
    url(r'^events/$', EventsView.as_view(), name='events'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^register/done/$', TemplateView.as_view(template_name="registration/done.html"), name='register-done'),
    url(r'^password/reset/$', password_reset,
        {
            'template_name': 'password_reset/form.html',
            'email_template_name': 'password_reset/email.html',
            'subject_template_name': 'password_reset/subject.txt',
            'post_reset_redirect': 'common:password_reset_done',
            'from_email': settings.NO_REPLY_EMAIL,
        },
        name='password_reset'),
    url(r'^password/reset/done/$', password_reset_done,
        {
            'template_name': 'password_reset/done.html'
        },
        name="password_reset_done"),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {
            'template_name': 'password_reset/confirm.html',
            'post_reset_redirect': 'common:password_reset_complete',
        },
        name="password_reset_confirm"),
    url(r'^password/done/$', password_reset_complete,
        {
            'template_name': 'password_reset/complete.html'
        },
        name="password_reset_complete"),
    url(r'^terms_of_use/$', TemplateView.as_view(template_name="terms_of_use.html"), name='terms_of_use'),
]
