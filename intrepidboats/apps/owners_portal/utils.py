from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _


def send_report_email(user_boat):
    context = {
        'user': user_boat.user,
        'user_boat': user_boat,
        'boat': user_boat.boat,
        'site': Site.objects.get_current().domain,
        'dashboard_url': reverse("owners_portal:owners_portal"),
    }

    send_mail(
        subject=_("New boat report - Intrepid Powerboats"),
        message=render_to_string('owners_portal/emails/report_email.txt', context),
        from_email=settings.BUILD_A_BOAT['NO_REPLY_EMAIL_REPORTS'],
        recipient_list=[user_boat.user.email],
        html_message=render_to_string('owners_portal/emails/report_email.html', context),
    )


def send_step_feedback_email(step_feedback):
    context = {
        'comments': step_feedback.comments,
        'user': step_feedback.user,
        'step': '{title} (phase: {phase})'.format(title=step_feedback.step.title, phase=step_feedback.step.phase),
        'boat': '{boat} (model: {model})'.format(boat=step_feedback.step.user_boat,
                                                 model=step_feedback.step.user_boat.boat)
    }

    send_mail(
        subject=_("{user} has sent feedback on {step} in Owner's portal - Intrepid Powerboats".format(
            user=context['user'],
            step=context['step'],
        )),
        message=render_to_string('owners_portal/emails/step_feedback_email.txt', context),
        from_email=settings.NO_REPLY_EMAIL,
        recipient_list=settings.TO_EMAIL['OWNERS_PORTAL_FEEDBACK_FORM'],
        html_message=render_to_string('owners_portal/emails/step_feedback_email.html', context),
    )


def send_new_shared_video_uploaded_email(shared_video):
    from django.contrib.auth.models import User
    admins = User.objects.filter(is_superuser=True)
    subject = _("New uploaded video to vimeo")
    to = admins.values_list('email', flat=True)
    from_email = settings.NO_REPLY_EMAIL

    site = Site.objects.get_current()
    ctx = {
        'user': shared_video.uploader,
        'site': site.domain,
        'admin_url': reverse("admin:owners_portal_sharedvideo_change", args=[shared_video.pk]),
    }

    message = render_to_string('owners_portal/emails/new_shared_video_email.txt', ctx)
    html_message = render_to_string('owners_portal/emails/new_shared_video_email.html', ctx)

    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=to, html_message=html_message)
