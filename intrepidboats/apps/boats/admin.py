from ckeditor.widgets import CKEditorWidget
from django.contrib import admin, messages
from django.db import models
from django.utils.translation import ugettext_lazy as _

from intrepidboats.apps.boats.boat_property_inline_admins import AboutTheBoatInlineAdmin, DeckPlanInlineAdmin, \
    MotorSelectionInlineAdmin, OptionalEquipmentInlineAdmin, VideoInlineAdmin
from .models import BoatModelGroup, Boat, Motor, MotorSelection, MotorColorOption, Feature, \
    FeatureOption, BuiltBoatEmail, BuiltBoatShare, DeckPlan, BoatGeneralFeature, OptionalEquipment, \
    AboutTheBoat, AboutTheBoatImage, Video, DeckPlanHotspot, BoatGeneralFeatureItem, BoatLengthGroup


@admin.register(BoatModelGroup)
class BoatModelGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(BoatLengthGroup)
class BoatLengthGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


class MotorColorOptionInline(admin.TabularInline):
    model = MotorColorOption

    class Media:
        css = {"all": ("css/admin/hide_inline_object_name.css",)}


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'model_group',)
    list_filter = ('model_group',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'model_group', 'length_group',)
        }),
        (_('images'), {
            'classes': ('collapse',),
            'fields': ('base', 'hull', 'boot_stripe', 'boot_stripe_accent',
                       'sheer_stripe', 'sheer_stripe_accent', 'logo', 'thumbnail',),
        }),
        (_('comparable attributes'), {
            'classes': ('collapse',),
            'fields': ('standard_fuel', 'beam', 'length', 'water',)
        }),
    )

    inlines = [
        AboutTheBoatInlineAdmin, DeckPlanInlineAdmin,
        MotorSelectionInlineAdmin, OptionalEquipmentInlineAdmin, VideoInlineAdmin
    ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        boat = self.get_object(request, object_id)
        if not boat.model_group:
            self.message_user(request, 'This boat has not GROUP. Add one to be able to edit with CMS',
                              level=messages.ERROR)
        if not boat.has_all_images():
            self.message_user(request, 'This boat has not all IMAGES. Add all to be able to edit with CMS',
                              level=messages.ERROR)
        if not hasattr(boat, 'about'):
            self.warning_message('ABOUT data', request)
        if hasattr(boat, 'about') and not boat.about.gallery.exists():
            self.warning_message('ABOUT photos', request)
        if not boat.general_features.exists():
            self.warning_message('FEATURES', request)
        if not hasattr(boat, 'deck_plan'):
            self.warning_message('DECK PLAN', request)
        if not boat.optional_equipments.exists():
            self.warning_message('OPTIONAL EQUIPMENTS', request)
        if not boat.motor_selections.exists():
            self.warning_message('MOTORS', request)
        if not boat.videos.exists():
            self.warning_message('VIDEOS', request)
        return super(BoatAdmin, self).change_view(request, object_id, form_url)

    def warning_message(self, text, request):
        self.message_user(request, 'This boat has not %s' % text, level=messages.WARNING)


@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


@admin.register(MotorSelection)
class MotorSelectionAdmin(admin.ModelAdmin):
    inlines = [
        MotorColorOptionInline,
    ]
    list_filter = ['boat', 'motor', ]


class FeatureOptionInline(admin.TabularInline):
    model = FeatureOption

    class Media:
        css = {"all": ("css/admin/hide_inline_object_name.css",)}


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'boat', 'kind', 'available',)
    list_filter = ('boat',)
    inlines = [
        FeatureOptionInline
    ]


@admin.register(BuiltBoatEmail)
class BuiltBoatEmailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'name', 'contact_sales',)


@admin.register(BuiltBoatShare)
class BuiltBoatShareAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created')


class DeckPlanHotspotInline(admin.TabularInline):
    model = DeckPlanHotspot


@admin.register(DeckPlan)
class DeckPlanAdmin(admin.ModelAdmin):
    inlines = [
        DeckPlanHotspotInline
    ]


class BoatGeneralFeatureItemInline(admin.TabularInline):
    model = BoatGeneralFeatureItem


@admin.register(BoatGeneralFeature)
class BoatGeneralFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'boat')
    list_filter = ('boat',)
    inlines = [
        BoatGeneralFeatureItemInline
    ]


@admin.register(OptionalEquipment)
class OptionalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('truncated_description', 'boat_model', 'admin_thumbnail', 'vimeo_id')
    list_filter = ('boat_model',)
    OptionalEquipment.truncated_description.short_description = _('item')


class AboutTheBoatImageInline(admin.TabularInline):
    model = AboutTheBoatImage


@admin.register(AboutTheBoat)
class AboutTheBoatAdmin(admin.ModelAdmin):
    list_display = ('title', 'boat')
    inlines = [
        AboutTheBoatImageInline
    ]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('vimeo_video_code', 'boat')
    list_filter = ('boat',)

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', 'boats/js/video_admin.js',)


@admin.register(AboutTheBoatImage)
class AboutTheBoatImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
