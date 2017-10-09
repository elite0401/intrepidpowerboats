from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import MotorSelection, DeckPlan, BoatGeneralFeature, OptionalEquipment, AboutTheBoat, Video


class BoatPropertyInlineAdmin(admin.TabularInline):
    classes = ['collapse']
    extra = 0

    readonly_fields = ['edit_with_cms']

    def edit_with_cms(self, instance):
        boat = instance.boat if hasattr(instance, 'boat') else instance.boat_model
        if self.tab and boat.has_all_images():
            url = reverse('boats:boat_detail', args=(boat.model_group.pk, boat.slug,)) + '?edit#%s' % self.tab
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (url, 'Edit with CMS'))
        else:
            return '-'

    edit_with_cms.short_description = 'Edit with CMS'


class AboutTheBoatInlineAdmin(BoatPropertyInlineAdmin):
    model = AboutTheBoat
    verbose_name = 'About'
    verbose_name_plural = 'About'
    tab = 'about'

    show_change_link = True

    class Media:
        js = ('boats/js/boat_admin.js',)


class DeckPlanInlineAdmin(BoatPropertyInlineAdmin):
    model = DeckPlan
    verbose_name_plural = 'Deck Plan'
    tab = 'deck-plan'


class MotorSelectionInlineAdmin(BoatPropertyInlineAdmin):
    model = MotorSelection
    verbose_name = 'Motor'
    verbose_name_plural = 'Motors'
    tab = 'motors'


class OptionalEquipmentInlineAdmin(BoatPropertyInlineAdmin):
    model = OptionalEquipment
    tab = 'optional-equipment'


class VideoInlineAdmin(admin.StackedInline, BoatPropertyInlineAdmin):
    model = Video
    tab = None
