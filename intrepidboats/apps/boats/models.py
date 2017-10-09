import base64

from colorfield.fields import ColorField
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db import transaction
from django.db.models import ImageField
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

from .fields import BoatImageField
from .utils import send_built_boat_email, send_built_boat_email_sales


class BoatModelGroup(TitleSlugDescriptionModel):
    class Meta:
        verbose_name = _("boat model group")
        verbose_name_plural = _("boat model groups")

    show_image = BoatImageField(verbose_name=_("show image"))

    def __str__(self):
        return self.title


class BoatLengthGroup(TitleSlugDescriptionModel):
    class Meta:
        verbose_name = _("boat length group")
        verbose_name_plural = _("boat length groups")

    show_image = BoatImageField(verbose_name=_("show image"))

    def __str__(self):
        return self.title


class Boat(TimeStampedModel, TitleSlugDescriptionModel):
    class Meta:
        verbose_name = _("boat model")
        verbose_name_plural = _("boat models")
        ordering = ['title']

    base = BoatImageField(verbose_name=_("base"))
    hull = BoatImageField(verbose_name=_("hull"))
    boot_stripe = BoatImageField(verbose_name=_("boot stripe"))
    boot_stripe_accent = BoatImageField(verbose_name=_("boot stripe accent"))
    sheer_stripe = ImageField(
        verbose_name=_("sheer stripe"),
        upload_to=settings.BOAT_CONFIG['BOAT_IMAGES'],
        blank=True,
        null=True,
    )
    sheer_stripe_accent = ImageField(
        verbose_name=_("sheer stripe accent"),
        upload_to=settings.BOAT_CONFIG['BOAT_IMAGES'],
        blank=True,
        null=True,
    )
    model_group = models.ForeignKey("BoatModelGroup", null=True, blank=True, related_name="boats",
                                    verbose_name=_("model group"))
    length_group = models.ForeignKey("BoatLengthGroup", null=True, blank=True, related_name="boats",
                                     verbose_name=_("length group"))
    logo = BoatImageField(verbose_name=_("logo"))

    thumbnail = ImageField(verbose_name=_("thumbnail"), upload_to="boats_thumbnails/")

    # Comparable attributes

    standard_fuel = models.CharField(max_length=255, verbose_name=_("standard fuel"))
    beam = models.CharField(max_length=255, verbose_name=_("beam"))
    length = models.CharField(max_length=255, verbose_name=_("length"))
    water = models.CharField(max_length=255, verbose_name=_("water"))

    def __str__(self):
        return self.title

    def get_available_features(self):
        return self.features.filter(available=True).all()

    def has_all_images(self):
        image_fields = ['base', 'hull', 'boot_stripe', 'boot_stripe_accent', 'logo', 'thumbnail']
        return all([getattr(self, attr) for attr in image_fields])


class Motor(TimeStampedModel, TitleSlugDescriptionModel):
    class Meta:
        verbose_name = _("motor")

    image = BoatImageField(verbose_name=_("image"))

    def __str__(self):
        return self.title


class MotorSelection(TimeStampedModel):
    class Meta:
        verbose_name = _("motor selection")
        verbose_name_plural = _("motors selection")

    motor = models.ForeignKey("Motor", verbose_name=_("motor"))
    boat = models.ForeignKey("Boat", related_name="motor_selections", verbose_name=_("boat"))

    def __str__(self):
        return "%s at %s" % (self.motor, self.boat)


class MotorColorOption(TimeStampedModel):
    motor_selection = models.ForeignKey("MotorSelection", verbose_name=_("motor selection"), related_name="options")
    title = models.CharField(max_length=255, verbose_name=_("title"))
    image = BoatImageField(verbose_name=_("image"))
    color = ColorField(default='#FFFFFF')
    color2 = ColorField(default='#FFFFFF')


TOP_FEATURE = "TOP"
ANCHOR_FEATURE = "ANCHOR"
DIVE_DOOR_FEATURE = "DIVE_DOOR"
SS_RUB_RAIL_INSERT_FEATURE = "SS_RUB_RAIL_INSERT"
RUB_RAIL_FEATURE = "RUB_RAIL"

# If you're going to add a new feature, please add it to canvas_boat.js rendering order!
FEATURE_CODE_CHOICES = (
    (TOP_FEATURE, _('top')),
    (ANCHOR_FEATURE, _('anchor')),
    ('BOW_RAIL', _('bow rail')),
    (RUB_RAIL_FEATURE, _('rub rail')),
    ('REAR_CLOSEOUT', _('rear closeout')),
    (DIVE_DOOR_FEATURE, _('dive door')),
    ('PORT_LIGHTS', _('port lights')),
    (SS_RUB_RAIL_INSERT_FEATURE, _('rub rail insert'))
)


class Feature(TimeStampedModel):
    boat = models.ForeignKey("Boat", related_name="features")
    title = models.CharField(max_length=255, verbose_name=_("title"), )
    kind = models.CharField(max_length=25, verbose_name=_("kind"), choices=FEATURE_CODE_CHOICES, default=TOP_FEATURE)
    available = models.BooleanField(default=False, verbose_name=_("available"))

    class Meta:
        verbose_name = _("feature")
        verbose_name_plural = _("features")

    def __str__(self):
        return self.title

    def template_display_kind(self):
        return "".join([word.lower().capitalize() for word in self.kind.split('_')])

    def template_middle_kind(self):
        return "-".join([word.lower() for word in self.kind.split('_')])


class FeatureOption(TimeStampedModel):
    feature = models.ForeignKey("Feature", related_name="options")
    title = models.CharField(max_length=255, verbose_name=_("title"))
    image = models.ImageField(verbose_name=_("image"), upload_to="other_features/")
    default = models.BooleanField(default=False, verbose_name=_("default"))
    display_value = models.CharField(max_length=255, verbose_name=_("display value"), default="", blank=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.default:
            FeatureOption.objects.filter(feature=self.feature).update(default=False)
        super(FeatureOption, self).save(*args, **kwargs)


class AbstractBuiltBoatShare(TimeStampedModel):
    image_url = models.TextField(verbose_name=_("image url"))
    image = models.ImageField(verbose_name=_("image"), upload_to="built_boats/")
    boat = models.ForeignKey("Boat", verbose_name=_("boat"), )

    class Meta:
        abstract = True

    def decode_image(self):
        image_data = base64.b64decode(self.image_url.replace("data:image/png;base64", ""))
        self.image = ContentFile(image_data, 'boat.png')
        self.save()


class BuiltBoatShare(AbstractBuiltBoatShare):
    class Meta:
        verbose_name = _("built boat share")
        verbose_name_plural = _("built boat shares")


class BuiltBoatEmail(AbstractBuiltBoatShare):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    email = models.EmailField(verbose_name=_("email"))

    phone = models.CharField(max_length=255, verbose_name=_("phone"), null=True, blank=True)
    contact_sales = models.BooleanField(default=False, verbose_name=_("contact sales"))

    class Meta:
        verbose_name = _("built boat email")
        verbose_name_plural = _("built boat emails")

    def send_email(self):
        send_built_boat_email(self, self.contact_sales)
        if self.contact_sales:
            send_built_boat_email_sales(self)


class DeckPlan(TimeStampedModel):
    image = BoatImageField(verbose_name=_("image"))
    boat = models.OneToOneField("Boat", related_name="deck_plan", verbose_name=_("boat"))

    def __str__(self):
        return 'Deck Plan: %s' % self.boat


class DeckPlanHotspot(TimeStampedModel):
    deck_plan = models.ForeignKey(DeckPlan, verbose_name=_("Deck plan"))
    text = models.CharField(max_length=255, verbose_name="Popover content")
    top_percentage = models.DecimalField(max_digits=7, decimal_places=4,
                                         verbose_name=_("distance from the top border (in %)"))
    left_percentage = models.DecimalField(max_digits=7, decimal_places=4,
                                          verbose_name=_("distance from the left border (in %)"))
    number = models.IntegerField(verbose_name="Number displayed on top of hotspot", null=True, blank=True)

    def __str__(self):
        return "Hotspot for {boat}'s deck plan : '{text}...'".format(
            boat=self.deck_plan.boat,
            text=self.text,
        )


class BoatGeneralFeature(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    boat = models.ForeignKey("Boat", related_name="general_features", verbose_name=_("boat"))

    def __str__(self):
        return self.title


class BoatGeneralFeatureItem(models.Model):
    boat_general_feature = models.ForeignKey(BoatGeneralFeature)
    description = models.CharField(max_length=255, verbose_name=_("description"))
    thumbnail = models.ImageField(blank=True, null=True, verbose_name=_("thumbnail"),
                                  upload_to=settings.BOAT_CONFIG['BOAT_IMAGES'] + 'general_features/')
    vimeo_id = models.CharField(max_length=31, blank=True, null=True, verbose_name=_("vimeo ID"))


class OptionalEquipment(models.Model):
    class Meta:
        verbose_name = _("optional equipment")
        verbose_name_plural = _("optional equipments")

    description = models.CharField(max_length=255, verbose_name=_("description"))
    thumbnail = models.ImageField(blank=True, null=True, verbose_name=_("thumbnail"),
                                  upload_to=settings.BOAT_CONFIG['BOAT_IMAGES'] + 'optionals/')
    vimeo_id = models.CharField(max_length=31, blank=True, null=True, verbose_name=_("vimeo ID"))
    boat_model = models.ForeignKey(Boat, related_name='optional_equipments', verbose_name=_('boat model'))

    def admin_thumbnail(self):
        if self.thumbnail:
            return format_html('<img height="30" src="%s"/>' % self.thumbnail.url)
        return None

    admin_thumbnail.short_description = _('thumbnail')

    # pylint:disable=E1136
    def truncated_description(self):
        return (self.description[:47] + '...') if len(self.description) > 50 else self.description

    def __str__(self):
        return self.truncated_description()


class AboutTheBoat(TimeStampedModel, TitleSlugDescriptionModel):
    brochure = models.FileField(upload_to="boat_brochures/", verbose_name=_("brochure"), null=True, blank=True)
    virtual_tour_link = models.URLField(verbose_name=_("virtual tour link"), blank=True, null=True)
    boat = models.OneToOneField("Boat", related_name="about", verbose_name=_("boat"))

    def __str__(self):
        return "%s: %s" % (self.boat, self.title)

    def interior_gallery(self):
        return self.gallery.filter(kind=AboutTheBoatImage.INTERIOR)

    def exterior_gallery(self):
        return self.gallery.filter(kind=AboutTheBoatImage.EXTERIOR)

    def cabin_gallery(self):
        return self.gallery.filter(kind=AboutTheBoatImage.CABIN)


class AboutTheBoatImage(TimeStampedModel):
    EXTERIOR = "EXTERIOR"
    INTERIOR = "INTERIOR"
    CABIN = "CABIN"

    IMAGE_KIND_CHOICES = (
        (EXTERIOR, _('exterior')),
        (INTERIOR, _('interior')),
        (CABIN, _('cabin')),
    )

    image = BoatImageField(verbose_name=_("image"))
    kind = models.CharField(max_length=25, verbose_name=_("kind"), choices=IMAGE_KIND_CHOICES)
    about_the_boat = models.ForeignKey("AboutTheBoat", related_name="gallery", verbose_name=_("about"))

    def __str__(self):
        return '%s image of %s' % (self.kind, self.about_the_boat.boat)


class Video(models.Model):
    vimeo_video_code = models.CharField(max_length=255, verbose_name=_("vimeo video code"),
                                        help_text='Add the ID that appears in the video url. '
                                                  'Example: https://vimeo.com/123456, the code is 123456.')
    boat = models.ForeignKey("Boat", related_name="videos", verbose_name=_("boat"), null=True, blank=True)
    thumbnail = models.ImageField(verbose_name=_("thumbnail"), upload_to="boat_video_thumbnails/",
                                  blank=True, null=True)
    video_external_url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("video external url"))

    def __str__(self):
        return "Vimeo: %s" % self.vimeo_video_code
