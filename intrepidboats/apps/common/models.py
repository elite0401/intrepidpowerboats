from random import sample

from ckeditor.fields import RichTextField
from cms.models.pagemodel import Page
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from django.db.models import ForeignKey, BooleanField, IntegerField
from django.db.models import ImageField
from django.db.models import Model, CharField, EmailField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from intrepidboats.apps.boats.models import Video


class PageSetting(Model):
    name = CharField(max_length=255, unique=True, verbose_name=_("name"))
    preferred_assets_len = IntegerField(default=3, verbose_name=_("preferred_assets_len"))  # Magic numbers

    class Meta:
        verbose_name = _("page setting")
        verbose_name_plural = _("page settings")

    def random_assets(self, is_mobile=False):
        assets = list(self.at_first_random_assets(is_mobile))
        assets += list(self.assets_queryset(is_mobile).filter(is_second_to_last=True))
        assets += list(self.assets_queryset(is_mobile).filter(is_last=True))
        return assets

    def at_first_random_assets(self, is_mobile=False):
        queryset = self.assets_queryset(is_mobile).filter(is_last=False, is_second_to_last=False).all()
        pks = list(queryset.values_list('pk', flat=True))
        sample_len = len(pks) if len(pks) < self.default_assets_len() else self.default_assets_len()
        samples = sample(pks, sample_len)
        return [queryset.get(pk=pk) for pk in samples]

    def assets_queryset(self, is_mobile=False):
        if is_mobile:
            return self.assets.filter(enabled=True, vimeo_video_code__isnull=True)
        return self.assets.filter(enabled=True)

    def default_assets_len(self):
        return self.preferred_assets_len

    def __str__(self):
        return self.name


class PageAsset(TimeStampedModel):
    page = ForeignKey("PageSetting", related_name="assets", verbose_name=_("page"))
    vimeo_video_code = CharField(max_length=255, blank=True, null=True, verbose_name=_("vimeo video code"))
    video_external_url = CharField(max_length=255, blank=True, null=True, verbose_name=_("video external url"))
    image = ImageField(upload_to="page_settings/", blank=True, null=True, verbose_name=_("image"))
    enabled = BooleanField(default=False, verbose_name=_("enabled"))
    is_last = BooleanField(default=False, verbose_name=_("is last"))
    is_second_to_last = BooleanField(default=False, verbose_name=_("is second to last"))

    class Meta:
        verbose_name = _("page asset")
        verbose_name_plural = _("page assets")
        ordering = ['is_last', 'is_second_to_last']

    def __str__(self):
        if self.is_vimeo_video():
            return "Vimeo: %s" % self.vimeo_video_code
        else:
            return "Image: %s" % self.image.name

    def is_vimeo_video(self):
        return bool(self.vimeo_video_code)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.is_last:
            PageAsset.objects.filter(page=self.page).update(is_last=False)
        if self.is_second_to_last:
            PageAsset.objects.filter(page=self.page).update(is_second_to_last=False)
        super(PageAsset, self).save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.is_last and self.is_second_to_last:
            raise ValidationError(_("The asset can't be both last and second to last"))


class NewsletterSubscriber(TimeStampedModel):
    class Meta:
        verbose_name = _('newsletter subscriber')
        verbose_name_plural = _('newsletter subscribers')

    first_name = CharField(max_length=255, verbose_name=_("first name"))
    last_name = CharField(max_length=255, verbose_name=_("last name"))
    email = EmailField(verbose_name=_("email"))

    def __str__(self):
        return self.email


class Article(models.Model):
    class Meta:
        ordering = ('-created_at', )

    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = RichTextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='articles/images/', verbose_name=_('Image'), null=True, blank=True)
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    created_at = models.DateTimeField(verbose_name=_('Created at'))
    video = models.OneToOneField(Video, related_name="article", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    class Meta:
        ordering = ('date', )

    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = RichTextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='events/images/', verbose_name=_('Image'))
    date = models.DateTimeField(verbose_name=_('Date'))
    external_link = models.URLField(verbose_name=_('External link'))

    def __str__(self):
        return self.title


class ExtraUserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    purchased_boat_info = models.TextField(blank=True, null=True, verbose_name=_('Purchased boat info'))
    details_for_staff = models.TextField(blank=True, null=True, verbose_name=_('Details for staff'))
    profile_picture = models.ImageField(upload_to='auth/profile_pictures/', verbose_name=_('Profile picture'),
                                        blank=True, null=True)
    gallery_header = models.ImageField(upload_to='auth/gallery_headers/', verbose_name=_('Gallery header'),
                                       blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('Extra user information')
        verbose_name_plural = _('Extra user information')


class AbstractMetaData(models.Model):
    page_title = models.CharField(max_length=500, verbose_name=_('Page title'))
    description = models.CharField(max_length=1000, verbose_name=_('Description'))
    og_title = models.CharField(max_length=500, verbose_name=_('Open graph: title'))
    og_description = models.CharField(max_length=1000, verbose_name=_('Open graph: description'))

    class Meta:
        abstract = True


class SiteMetaData(AbstractMetaData):
    og_image = models.ImageField(upload_to='site_metadata/', verbose_name=_('Open graph: image'), blank=True, null=True)

    owners_portal_description = models.CharField(
        max_length=1000, verbose_name=_("Owner's portal: Description"), blank=True, null=True)
    owners_portal_og_title = models.CharField(
        max_length=500, verbose_name=_("Owner's portal: open graph: title"), blank=True, null=True)
    owners_portal_og_description = models.CharField(
        max_length=1000, verbose_name=_("Owner's portal: open graph: description"), blank=True, null=True)

    whats_new_description = models.CharField(
        max_length=1000, verbose_name=_("What's new: Description"), blank=True, null=True)
    whats_new_og_title = models.CharField(
        max_length=500, verbose_name=_("What's new: open graph: title"), blank=True, null=True)
    whats_new_og_description = models.CharField(
        max_length=1000, verbose_name=_("What's new: open graph: description"), blank=True, null=True)

    events_description = models.CharField(
        max_length=1000, verbose_name=_("Events: Description"), blank=True, null=True)
    events_og_title = models.CharField(
        max_length=500, verbose_name=_("Events: open graph: title"), blank=True, null=True)
    events_og_description = models.CharField(
        max_length=1000, verbose_name=_("Events: open graph: description"), blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = _('Site metadata')

    def __str__(self):
        return 'Site metadata'


class CMSPageMetaData(AbstractMetaData):
    og_image = models.ImageField(upload_to='site_metadata/cms/', verbose_name=_('Open graph: image'), blank=True, null=True)

    page = models.OneToOneField(Page, verbose_name=_("Page"), related_name='metadata')

    class Meta:
        verbose_name = verbose_name_plural = _('CMS page metadata')

    def __str__(self):
        return 'Metadata for {page}'.format(page=self.page)
