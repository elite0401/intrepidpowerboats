from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.urls import reverse

from .models import UserBoat, BoatStep, BoatStepAsset, StepFeedback, BoatPhase, SharedPicture, SharedVideo, Survey, \
    BoatManualGroup, BoatManual


class BoatStepAssetInline(admin.TabularInline):
    extra = 0
    model = BoatStepAsset

    class Media:
        css = {"all": ("css/admin/hide_inline_object_name.css",)}


class BoatStepAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name="boat_steps"))

    class Meta:
        exclude = ()
        model = BoatStep


@admin.register(BoatPhase)
class BoatPhaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)


@admin.register(BoatStep)
class BoatStepAdmin(admin.ModelAdmin):
    list_filter = ('start_date', 'active', 'user_boat', 'user_boat__boat', 'user_boat__user')
    list_display = ('title', 'phase', 'start_date', 'active', 'user_boat_link',)
    list_display_links = ('title',)
    form = BoatStepAdminForm
    inlines = [
        BoatStepAssetInline
    ]

    def user_boat_link(self, boat_step):
        path = reverse("admin:owners_portal_userboat_change", args=[boat_step.user_boat.pk])
        return "<a href='{}'>{}</a>".format(path, boat_step.user_boat.name)

    user_boat_link.allow_tags = True


class BoatStepForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name="boat_steps_inline"))

    class Meta:
        fields = ('title', 'description', 'phase', 'start_date', 'active',)
        model = BoatStep


class BoatStepInline(admin.StackedInline):
    extra = 0
    model = BoatStep
    form = BoatStepForm
    ordering = ('order',)
    fields = (('title', 'description', 'phase', 'start_date', 'active'),)

    class Media:
        css = {"all": ("css/admin/hide_inline_object_name.css",)}


class BoatManualInline(admin.TabularInline):
    model = BoatManual


@admin.register(BoatManualGroup)
class BoatManualGroupAdmin(admin.ModelAdmin):
    inlines = [BoatManualInline]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', 'owners_portal/js/add_help_text.js')


class UserBoatForm(forms.ModelForm):
    notes = forms.CharField(widget=CKEditorWidget(config_name="default"))

    class Meta:
        exclude = ()
        model = BoatStep


@admin.register(UserBoat)
class UserBoatAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'boat', 'active_step']
    list_filter = ['user', 'boat']
    form = UserBoatForm
    inlines = [
        BoatStepInline,
    ]

    def active_step(self, boat):
        return boat.active_step()

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', 'owners_portal/js/add_help_text.js')


@admin.register(StepFeedback)
class StepFeedbackAdmin(admin.ModelAdmin):
    list_display = ("step", "user")
    list_filter = ("step__active", "user")


@admin.register(SharedPicture)
class SharedPictureAdmin(admin.ModelAdmin):
    list_display = ("pk", "uploader", "comment_preview", "image", "is_public", "is_approved", )
    list_filter = ("is_public", "is_approved", )


class SharedVideoAdminForm(forms.ModelForm):
    class Meta:
        model = SharedVideo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SharedVideoAdminForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = False
        self.fields['video_id'].required = False


@admin.register(SharedVideo)
class SharedVideoAdmin(admin.ModelAdmin):
    list_display = ("pk", "uploader", "comment_preview", "video_id", "is_public", "completed", "is_approved", )
    list_filter = ("completed", "is_public", "is_approved", )
    form = SharedVideoAdminForm


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled',)
