from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


def send_shared_testimonial_email(testimonial, domain):
    context = {
        'name': '{first_name} {last_name}'.format(first_name=testimonial.first_name, last_name=testimonial.last_name),
        'title': ', {}'.format(testimonial.title) if testimonial.title else '',
        'email': testimonial.email,
        'message': testimonial.message,
        'file_url': domain + testimonial.file.url if testimonial.file else '',
        'admin_url': domain + reverse("admin:difference_sharedtestimonial_change", args=[testimonial.pk]),
    }

    send_mail(
        subject=_('A testimonial has been shared ({name}{title}) - Intrepid Powerboats'.format(
            title=context['title'], name=context['name'])),
        message=render_to_string('difference/emails/shared_testimonial_email.txt', context),
        from_email=settings.NO_REPLY_EMAIL,
        recipient_list=settings.TO_EMAIL['TESTIMONIAL_SHARE'],
        html_message=render_to_string('difference/emails/shared_testimonial_email.html', context),
    )


def send_new_testimonial_video_uploaded_email(testimonial):
    admins = User.objects.filter(is_superuser=True)
    subject = _("New uploaded video to vimeo")
    to = admins.values_list('email', flat=True)
    from_email = settings.NO_REPLY_EMAIL

    site = Site.objects.get_current()
    ctx = {
        'site': site.domain,
        'admin_url': reverse("admin:difference_sharedtestimonial_change", args=[testimonial.pk]),
    }

    message = render_to_string(
        'difference/emails/new_shared_testimonial_email.txt', ctx)
    html_message = render_to_string(
        'difference/emails/new_shared_testimonial_email.html', ctx)

    send_mail(subject=subject, message=message,
              from_email=from_email, recipient_list=to,
              html_message=html_message)
