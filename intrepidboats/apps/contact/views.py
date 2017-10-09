from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.http import BadHeaderError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from intrepidboats.apps.contact.utils import send_employment_resume_email, send_inquiry_email
from .models import JobApplicant, Inquiry


class SendInformationFormInvalidMixin:
    def form_invalid(self, form):
        super().form_invalid(form)
        error_text = '\n'.join('\n'.join(error_list) for error_list in form.errors.values())
        messages.error(self.request, error_text)
        return redirect(self.success_url)


class SendInquiryView(SendInformationFormInvalidMixin, CreateView):
    model = Inquiry
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'inquiry_type', 'comments']
    success_url = reverse_lazy('contact:contact_success')

    def form_valid(self, form):
        super().form_valid(form)

        email_recipients = {
            Inquiry.GENERAL_INQUIRY: settings.INQUIRY_EMAIL_ADDRESS,
            Inquiry.GENERAL_BOAT_INFORMATION: settings.BOAT_INFORMATION_EMAIL_ADDRESS,
            Inquiry.SALES: settings.SALES_EMAIL_ADDRESS,
        }

        try:
            send_inquiry_email(self.object, email_recipients[self.object.inquiry_type])
        except BadHeaderError as err:
            messages.error(self.request, err)

        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def write_email_content(self):
        email_content = ["Sender info:"]

        sender_info = [
            ('First name', self.object.first_name),
            ('Last name', self.object.last_name),
            ('Email address', self.object.email),
        ]

        if self.object.phone_number:
            sender_info.append(('Phone number', self.object.phone_number), )

        sender_info_dict = OrderedDict(sender_info)
        email_content.extend(["{}: {}".format(key, value) for key, value in sender_info_dict.items()])
        email_content.extend(["", self.object.comments])

        return "\n".join(email_content)


class SendResumeView(SendInformationFormInvalidMixin, CreateView):
    model = JobApplicant
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'resume', 'additional_notes']
    success_url = reverse_lazy('contact:careers_success')

    def form_valid(self, form):
        super().form_valid(form)
        send_employment_resume_email(self.object, self.request.META['HTTP_HOST'])
        return redirect(self.success_url)
