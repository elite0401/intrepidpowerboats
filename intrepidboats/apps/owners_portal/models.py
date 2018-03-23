from django.conf import settings
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel

from intrepidboats.apps.common.utils import get_external_url
from intrepidboats.apps.owners_portal.utils import send_new_shared_video_uploaded_email
from intrepidboats.libs.vimeo_video_upload.models import Builder
from .managers import BoatStepManager, SharedMediaManager


class UserBoat(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_boats", verbose_name=_("user"))
    boat = models.ForeignKey("boats.Boat", verbose_name=_("boat model"))
    design = models.ImageField(verbose_name=_("design"), upload_to="boat_designs/")

    notes = models.TextField(verbose_name=_("notes"), null=True, blank=True, default="")

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name

    def active_step(self):
        if self.steps.filter(active=True).exists():
            return self.steps.filter(active=True).get()
        else:
            return None
    def last_step(self):
        return self.steps.order_by('start_date').last()


class BoatPhase(TimeStampedModel, TitleDescriptionModel):
    def __str__(self):
        return self.title


class BoatManualGroup(TimeStampedModel):
    name = models.CharField(
        max_length=255,
    )
    user_boat = models.ForeignKey(
        "UserBoat",
    )

    class Meta:
        verbose_name = verbose_name_plural = _('user boat manuals')

    def __str__(self):
        return '{} ({})'.format(self.name, self.user_boat)


class BoatManual(TimeStampedModel):
    group = models.ForeignKey(
        BoatManualGroup,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    vimeo_video_code = models.CharField(
        max_length=255,
        verbose_name=_("vimeo video code"),
        help_text='Add the ID that appears in the video url. ''Example: https://vimeo.com/123456, the code is 123456.',
        blank=True,
        null=True,
    )
    video_external_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("video external url"),
    )
    thumbnail = models.ImageField(
        verbose_name=_("Thumbnail for Facebook share"),
        upload_to="owners_gallery/manual_thumbnails/",
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description for Facebook share"),
        blank=True,
        null=True,
    )
    link = models.URLField(
        verbose_name=_("link"),
        blank=True,
        null=True,
    )
    manual = models.FileField(
        upload_to="boat_manuals/",
        verbose_name=_("manual"),
        null=True,
        blank=True,
    )

    def save(self, **kwargs):
        if self.vimeo_video_code:
            self.video_external_url = get_external_url(self.vimeo_video_code)
        super().save(**kwargs)

    class Meta:
        verbose_name = _('user boat manual')

    def __str__(self):
        if self.vimeo_video_code:
            manual_type = 'video'
        elif self.link:
            manual_type = 'link'
        elif self.manual:
            manual_type = 'file'
        else:
            manual_type = 'empty'
        return '{} ({})'.format(self.title, manual_type)


class BoatStep(OrderedModel):
    user_boat = models.ForeignKey("UserBoat", related_name="steps")
    title = models.CharField(max_length=30, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))
    phase = models.ForeignKey("BoatPhase", related_name="steps")

    start_date = models.DateTimeField(verbose_name=_("start date"))
    active = models.BooleanField(default=False, verbose_name=_("active"))

    objects = BoatStepManager()

    def __str__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        pass

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.active:
            BoatStep.objects.filter(user_boat=self.user_boat).update(active=False)
        super(BoatStep, self).save(*args, **kwargs)


class BoatStepAsset(TimeStampedModel):
    boat_step = models.ForeignKey("BoatStep", related_name="assets")
    image = models.ImageField(upload_to="boat_designs/step_images/", )
    vimeo_video_code = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("vimeo video code"))

    def asset_url(self):
        if self.vimeo_video_code:
            return "https://player.vimeo.com/video/%s" % self.vimeo_video_code
        else:
            return self.image.url


class StepFeedback(TimeStampedModel):
    comments = models.TextField(verbose_name=_("comments"))
    step = models.ForeignKey("BoatStep", verbose_name=_("step"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name="step_feedbacks")


IS_PUBLIC_CHOICES = ((True, _('Public')), (False, _('Private')))


class SharedMedia(PolymorphicModel, TimeStampedModel):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="shared_media", verbose_name=_("uploader"))
    comment = models.TextField(verbose_name=_("comment"))
    is_public = models.BooleanField(choices=IS_PUBLIC_CHOICES, default=False, verbose_name=_("is public"))
    is_approved = models.BooleanField(default=False, verbose_name=_("is approved"))

    objects = SharedMediaManager()

    def comment_preview(self):
        return (self.comment[:47] + '...') if len(self.comment) > 50 else self.comment

    def __str__(self):
        return self.comment_preview()

    def media_type(self):
        raise NotImplementedError


class SharedPicture(SharedMedia):
    image = models.ImageField(upload_to="shared_images/", )

    class Meta:
        verbose_name = _("shared picture")
        verbose_name_plural = _("shared pictures")

    def media_type(self):
        return "picture"


class SharedVideo(SharedMedia):
    ticket_id = models.CharField(max_length=610, verbose_name=_("ticket id"))
    uri = models.CharField(max_length=255, verbose_name=_("uri"))
    vimeo_user = models.TextField(verbose_name=_("vimeo user"))
    upload_link_secure = models.CharField(max_length=610, verbose_name=_("upload link secure"))
    complete_uri = models.CharField(max_length=610, verbose_name=_("complete uri"))
    completed = models.BooleanField(default=False, verbose_name=_("completed"))
    video_id = models.CharField(max_length=127, null=True, verbose_name=_("video id"))
    thumbnail = models.ImageField(verbose_name=_("thumbnail"), upload_to="owners_gallery/", blank=True, null=True)
    video_external_url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("video external url"))

    class Meta:
        verbose_name = _("shared video")
        verbose_name_plural = _("shared videos")

    def __str__(self):
        return 'Video shared by %s' % self.uploader

    def media_type(self):
        return "video"


class SharedVideoBuilder(Builder):
    def create_video(self, user, **kwargs):
        data = self.create_ticket()
        return SharedVideo.objects.create(
            uploader=user,
            comment=kwargs.get('comment', 'No comment'),
            is_public=kwargs.get('is_public', False),
            ticket_id=data['ticket_id'],
            uri=data['uri'],
            vimeo_user=data['user'],
            upload_link_secure=data['upload_link_secure'],
            complete_uri=data['complete_uri']
        )

    def get_instance(self, ticket_id, user):
        return user.shared_media.instance_of(SharedVideo).get(sharedvideo__ticket_id=ticket_id)

    def send_new_uploaded_video_email(self, ticket_id, user):
        send_new_shared_video_uploaded_email(self.get_instance(ticket_id, user))

    def get_text_field_for(self, instance):
        return instance.comment

    def set_video_id(self, instance, vimeo_video_id):
        instance.video_id = vimeo_video_id
        instance.video_external_url = get_external_url(vimeo_video_id)

    def save_thumbnail(self, instance, filename, thumbnail_file):
        instance.thumbnail.save(filename, thumbnail_file)

    def set_to_completed(self, instance):
        if instance.video_external_url:
            instance.completed = True


class Survey(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    enabled = models.BooleanField(default=False, verbose_name=_("enabled"))
    script = models.TextField(verbose_name=_("script"))
