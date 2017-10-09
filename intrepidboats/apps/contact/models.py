from ckeditor.fields import RichTextField
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class JobDescriptionPlugin(CMSPlugin):
    job_title = models.CharField(max_length=50, verbose_name=_("job title"))
    job_description = RichTextField(verbose_name=_("job description"))

    class Meta:
        verbose_name = _("job description plugin")
        verbose_name_plural = _("job description plugins")

    def __str__(self):
        return self.job_title


class CompanyAreaPlugin(CMSPlugin):
    title = models.CharField(max_length=255, verbose_name=_("title"))

    def __str__(self):
        return self.title


class EmployeeProfilePlugin(CMSPlugin):
    full_name = models.CharField(max_length=255, verbose_name=_("full name"))
    occupation = models.CharField(max_length=255, verbose_name=_("occupation"))
    phone_number = models.CharField(max_length=255, verbose_name=_("phone number"))
    email = models.EmailField(verbose_name=_("email"))
    image = models.ImageField(upload_to='cms/', blank=True, verbose_name=_("image"))

    def __str__(self):
        return self.full_name


class BaseUserInformationModel(TimeStampedModel):
    first_name = models.CharField(max_length=255, verbose_name=_("first name"))
    last_name = models.CharField(max_length=255, verbose_name=_("last name"))
    email = models.EmailField(verbose_name=_("email"))
    phone_number = models.CharField(max_length=255, blank=True, verbose_name=_("phone number"))

    class Meta:
        abstract = True


class JobApplicant(BaseUserInformationModel):
    class Meta:
        verbose_name = _("job applicant")
        verbose_name_plural = _("job applicants")

    additional_notes = models.TextField(blank=True, verbose_name=_("additional notes"))
    resume = models.FileField(upload_to='applicant_uploads/', blank=True, verbose_name=_("resume"))

    def __str__(self):
        return self.email


class Inquiry(BaseUserInformationModel):
    class Meta:
        verbose_name = _("inquiry")
        verbose_name_plural = _("inquiries")

    comments = models.TextField(verbose_name=_("comments"))

    GENERAL_INQUIRY = 'I'
    SALES = 'S'
    GENERAL_BOAT_INFORMATION = 'B'

    TYPE_CHOICES = (
        (GENERAL_INQUIRY, _('General inquiry')),
        (SALES, _('Sales')),
        (GENERAL_BOAT_INFORMATION, _('General boat information')),
    )
    inquiry_type = models.CharField(max_length=1, choices=TYPE_CHOICES,
                                    default=GENERAL_INQUIRY, verbose_name=_('inquiry type'))

    def __str__(self):
        return self.email
