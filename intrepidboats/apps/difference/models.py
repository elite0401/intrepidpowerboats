import requests
from ckeditor.fields import RichTextField
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from intrepidboats.libs.vimeo_video_upload.models import Builder


class IntrepidDifferenceSectionPlugin(CMSPlugin):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    section_text = RichTextField(verbose_name=_("Section Text"))

    def __str__(self):
        return self.title


class ImageWithTextPlugin(CMSPlugin):
    image = models.ImageField(upload_to='cms/', verbose_name=_("Image"))
    section_text = models.TextField(verbose_name=_("Section Text"), null=True, blank=True)

    def __str__(self):
        return self.section_text


class SharedTestimonialUploadInfo(TimeStampedModel):
    ticket_id = models.CharField(max_length=610, verbose_name=_("ticket id"))
    uri = models.CharField(max_length=255, verbose_name=_("uri"))
    upload_link_secure = models.CharField(max_length=610, verbose_name=_("upload link secure"))
    complete_uri = models.CharField(max_length=610, verbose_name=_("complete uri"))
    completed = models.BooleanField(default=False, verbose_name=_("completed"))
    vimeo_user = models.TextField(verbose_name=_("vimeo user"))

    class Meta:
        verbose_name = _("shared testimonial info")
        verbose_name_plural = _("shared testimonial info")

    def __str__(self):
        return 'Ticket id: %s' % self.ticket_id


class SharedTestimonial(TimeStampedModel):
    first_name = models.CharField(max_length=255, verbose_name=_("first name"))
    last_name = models.CharField(max_length=255, verbose_name=_("last name"))
    title = models.CharField(max_length=100, verbose_name=_("title"), blank=True, null=True)
    email = models.EmailField(verbose_name=_("email"))
    message = models.TextField(verbose_name=_("text"))
    file = models.FileField(upload_to="shared_testimonials/", verbose_name=_("file"), blank=True, null=True)
    video_id = models.CharField(max_length=127, blank=True, null=True, verbose_name=_("video id"))
    thumbnail = models.ImageField(verbose_name=_("thumbnail"), upload_to="owners_gallery/", blank=True, null=True)
    info = models.OneToOneField(SharedTestimonialUploadInfo, related_name="shared_testimonial",
                                verbose_name=_("upload information"), null=True, blank=True)

    class Meta:
        verbose_name = _("shared testimonial")
        verbose_name_plural = _("shared testimonials")

    # pylint:disable=E1136
    def __str__(self):
        return '{first_name} {last_name}, {title}: {message}'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            title=self.title,
            message=self.message[:100] + '...' if len(self.message) > 100 else self.message
        )


class TestimonialPlugin(CMSPlugin):
    testimonial = models.ForeignKey(SharedTestimonial)

    def __str__(self):
        return str(self.testimonial)


class TestimonialVideoPlugin(CMSPlugin):
    movie_url = models.URLField(verbose_name=_('Movie URL'))

    def __str__(self):
        return self.movie_url

    def thumbnail_url(self):
        video_id = self.movie_url.split(sep='/')[-1]
        json_request = requests.get(url='https://vimeo.com/api/v2/video/{id}.json'.format(id=video_id))
        return json_request.json()[0]['thumbnail_large']


class SharedTestimonialInfoBuilder(Builder):
    def create_testimonial_info(self):
        data = self.create_ticket()
        return SharedTestimonialUploadInfo.objects.create(
            ticket_id=data['ticket_id'],
            uri=data['uri'],
            upload_link_secure=data['upload_link_secure'],
            complete_uri=data['complete_uri'],
            vimeo_user=data['user']
        )

    def get_instance(self, ticket_id, user):
        return SharedTestimonialUploadInfo.objects.get(ticket_id=ticket_id)

    def get_text_field_for(self, instance):
        return instance.shared_testimonial.message

    def set_video_id(self, instance, vimeo_video_id):
        instance.shared_testimonial.video_id = vimeo_video_id
        instance.shared_testimonial.save()

    def save_thumbnail(self, instance, filename, thumbnail_file):
        instance.shared_testimonial.thumbnail.save(filename, thumbnail_file)
        instance.shared_testimonial.save()

    def set_to_completed(self, instance):
        instance.completed = True
