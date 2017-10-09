from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def send_employment_resume_email(job_applicant, domain):
    context = {
        'first_name': job_applicant.first_name,
        'last_name': job_applicant.last_name,
        'email': job_applicant.email,
        'phone_number': job_applicant.phone_number,
        'resume_url': job_applicant.resume.url if job_applicant.resume else None,
        'additional_notes': job_applicant.additional_notes,
        'domain': domain,
    }

    send_mail(
        subject=_("New applicant resume - Intrepid Powerboats"),
        message=render_to_string('contact/emails/employment_resume_email.txt', context),
        from_email=settings.NO_REPLY_EMAIL,
        recipient_list=settings.TO_EMAIL['EMPLOYMENT_PAGE_FORM'],
        html_message=render_to_string('contact/emails/employment_resume_email.html', context))


def send_inquiry_email(inquiry, to):
    subject = inquiry.get_inquiry_type_display()
    from_email = inquiry.email

    ctx = {'inquiry': inquiry}

    message = render_to_string('contact/emails/inquiry_email.txt', ctx)
    html_message = render_to_string('contact/emails/inquiry_email.html', ctx)

    send_mail(
        subject=subject,
        from_email=from_email,
        recipient_list=to,
        message=message,
        html_message=html_message,
    )
