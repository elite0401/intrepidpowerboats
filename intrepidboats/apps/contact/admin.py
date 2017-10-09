from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import JobApplicant, Inquiry


@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone_number", "attachment", "created")
    ordering = ("-created", )

    def attachment(self, obj):
        if obj.resume:
            return "<a href='{}' download>{}</a>".format(obj.resume.url, _("Download"))
        else:
            return _("No attachment")
    attachment.allow_tags = True
    attachment.short_description = _("resume")


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone_number", "inquiry_type", "created")
    list_filter = ("inquiry_type", )
    ordering = ("-created", )
