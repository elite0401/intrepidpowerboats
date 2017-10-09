from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from machina.apps.forum_conversation.models import Post


# pylint:disable=W0613
@receiver(post_save, sender=Post)
def send_email_after_post_submission(sender, instance, created, **kwargs):
    deletion_url = Site.objects.get_current().domain + reverse(
        'forum_conversation:post_delete',
        args=(instance.topic.forum.slug, instance.topic.forum.pk, instance.topic.slug, instance.topic.pk, instance.pk)
    )
    context = {
        'is_edit': not created,
        'who_posted': instance.poster,
        'who_saved': instance.updated_by,
        'subject': instance.subject,
        'content': instance.content,
        'deletion_url': deletion_url,
    }

    send_mail(
        subject=_("New Forum post" if created else "Edited Forum post" + " - Intrepid Powerboats"),
        from_email=settings.NO_REPLY_EMAIL,
        recipient_list=settings.TO_EMAIL['POST_SUBMISSION_NOTIFICATION'],
        message=render_to_string('owners_portal/emails/forum_post.txt', context),
        html_message=render_to_string('owners_portal/emails/forum_post.html', context)
    )
