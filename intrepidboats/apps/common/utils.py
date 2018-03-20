import urllib.parse

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from intrepidboats.libs.vimeo_rate_limiting.models import VimeoRateLimiting


def send_successful_registration_emails(user_registration_form):
    def send_successful_registration_user_email(user_registration_form):
        context = {
            'first_name': user_registration_form.cleaned_data['first_name'],
            'last_name': user_registration_form.cleaned_data['last_name'],
            'username': user_registration_form.cleaned_data['username'],
        }

        send_mail(
            subject=_("Registration successful - Intrepid Powerboats"),
            message=render_to_string('registration/emails/successful_registration_user.txt', context),
            from_email=settings.NO_REPLY_EMAIL,
            recipient_list=[user_registration_form.cleaned_data['email']],
            html_message=render_to_string('registration/emails/successful_registration_user.html', context),
        )

    def send_successful_registration_intrepid_email(user_registration_form):
        context = {
            'email': user_registration_form.cleaned_data['email'],
            'first_name': user_registration_form.cleaned_data['first_name'],
            'last_name': user_registration_form.cleaned_data['last_name'],
            'username': user_registration_form.cleaned_data['username'],
        }

        send_mail(
            subject=_("A user has registered - Intrepid Powerboats"),
            message=render_to_string('registration/emails/successful_registration_intrepid.txt', context),
            from_email=settings.NO_REPLY_EMAIL,
            recipient_list=settings.TO_EMAIL['REGISTRATION_FORM'],
            html_message=render_to_string('registration/emails/successful_registration_intrepid.html', context),
        )

    send_successful_registration_user_email(user_registration_form)
    send_successful_registration_intrepid_email(user_registration_form)


def send_new_newsletter_subscriber_email(newsletter_form):
    context = {
        'email': newsletter_form.cleaned_data['email'],
        'first_name': newsletter_form.cleaned_data['first_name'],
        'last_name': newsletter_form.cleaned_data['last_name'],
    }

    send_mail(
        subject=_("New newsletter subscriber - Intrepid Powerboats"),
        message=render_to_string('registration/emails/newsletter_subscription_email.txt', context),
        from_email=settings.NO_REPLY_EMAIL,
        recipient_list=settings.TO_EMAIL['NEWSLETTER_FORM'],
        html_message=render_to_string('registration/emails/newsletter_subscription_email.html', context),
    )


def send_new_registered_user_email(user, register_form):
    admins = User.objects.filter(is_superuser=True)
    subject = _("New registered user")
    to = admins.values_list('email', flat=True)
    from_email = settings.NO_REPLY_EMAIL

    site = Site.objects.get_current()
    ctx = {
        'user': user,
        'site': site.domain,
        'admin_url': reverse("admin:auth_user_change", args=[user.pk]),
        'model': register_form.cleaned_data['intrepid_model'],
        'year': register_form.cleaned_data['intrepid_year'],
        'hull_id': register_form.cleaned_data['intrepid_hull_id'],
        'own_intrepid': 'Yes'
    }

    if register_form.cleaned_data['fan']:
        ctx['own_intrepid'] = 'No'

    message = render_to_string(
        'common/emails/new_registered_user_email.txt', ctx)
    html_message = render_to_string(
        'common/emails/new_registered_user_email.html', ctx)

    send_mail(subject=subject, message=message,
              from_email=from_email, recipient_list=to,
              html_message=html_message)


def get_external_url(vimeo_video_code):

    rate_limit_data = VimeoRateLimiting.get_instance()
    if not rate_limit_data.available_for_request():
        return None

    vimeo_api_url = settings.VIMEO_CONFIG['VIMEO_API_URL']
    token = settings.VIMEO_CONFIG['PRO_UPLOAD_TOKEN']
    headers = {"Authorization": "Bearer %s" % token}
    videos_url = urllib.parse.urljoin(vimeo_api_url, 'me/videos/')
    field = 'files'
    json_filters = '?fields={}'.format(field)
    response = requests.get('%s%s%s' % (videos_url, vimeo_video_code, json_filters), headers=headers)

    if response.status_code == 404:
        return '/'

    rate_limit_data.update_with(
        reset_time=response.headers._store['x-ratelimit-reset'][1],
        remaining_requests=response.headers._store['x-ratelimit-remaining'][1],
    )

    video_data = response.json()
    if field not in video_data or not video_data[field]:
        return None
    # check for HD version first
    if [data['link_secure'] for data in video_data[field] if data['quality'] == 'hd']:
        return [data['link_secure'] for data in video_data[field] if data['quality'] == 'hd'][0]
    return [data['link_secure'] for data in video_data[field] if data['quality'] == 'sd'][
        0] if field in video_data and video_data[field] else None


def split_queryset(queryset, size):
    return [queryset[index:index + size] for index in range(0, queryset.count(), size)]
