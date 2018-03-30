from cms.models.pagemodel import Page
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .export_csv import download_as_csv
from .models import CMSPageMetaData
from .models import PageSetting, PageAsset, NewsletterSubscriber, Article, ExtraUserData, Event, SiteMetaData


class PageAssetInline(admin.TabularInline):
    model = PageAsset

    class Media:
        css = {"all": ("css/admin/hide_inline_object_name.css",)}


@admin.register(PageSetting)
class PageSettingAdmin(ModelAdmin):
    inlines = [PageAssetInline, ]


@admin.register(PageAsset)
class PageAssetAdmin(ModelAdmin):
    list_display = ("pk", "vimeo_video_code", "image", "enabled", "is_last",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ("email", "first_name", "last_name", "created",)
    ordering = ("-created",)
    actions = [download_as_csv]
    download_as_csv_fields = ["email", "first_name", "last_name", "created"]


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_filter = ('featured',)
    list_display = ('title', 'created_at', 'featured',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj is None:
            return readonly_fields + ('created_at',)
        return readonly_fields


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('title', 'date', 'external_link',)


class ExtraUserDataInline(admin.TabularInline):
    can_delete = False
    model = ExtraUserData
    fields = ['profile_picture', 'gallery_header', 'intrepid_hull_id']

    class Media:
        css = {"all": ("css/admin/hide_inline_object_name.css",)}


class UserAdmin(BaseUserAdmin):
    inlines = [ExtraUserDataInline, ]


@admin.register(ExtraUserData)
class DetailsForStaffAdmin(ModelAdmin):
    model = ExtraUserData
    fields = ['user', 'purchased_boat_info', 'details_for_staff', 'intrepid_hull_id']
    list_display = ['user', 'truncated_purchased_boat_info', 'truncated_details_for_staff', 'intrepid_hull_id']
    search_fields = ['user__username']

    def get_readonly_fields(self, request, obj=None):
        return ['user'] if obj else []  # Allow adding for a new user, but disallow changing users when editing

    # pylint:disable=E1136
    def truncated_purchased_boat_info(self, obj):
        return truncate(obj.purchased_boat_info)
    truncated_purchased_boat_info.short_description = 'Purchased boat info'

    # pylint:disable=E1136
    def truncated_details_for_staff(self, obj):
        return truncate(obj.details_for_staff)
    truncated_details_for_staff.short_description = 'Details for staff'


def truncate(string):
    if not string:
        return None
    return (string[:47] + '...') if len(string) > 50 else string


@admin.register(SiteMetaData)
class SiteMetaDataAdmin(ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page_title', 'description', 'og_title', 'og_description', 'og_image',)
        }),
        ("Owner's portal", {
            'fields': ('owners_portal_description', 'owners_portal_og_title', 'owners_portal_og_description'),
        }),
        ("What's new", {
            'fields': ('whats_new_description', 'whats_new_og_title', 'whats_new_og_description'),
        }),
        ("Events", {
            'fields': ('events_description', 'events_og_title', 'events_og_description'),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CMSPageMetaData)
class CMSPageMetaDataAdmin(ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "page":
            kwargs["queryset"] = Page.objects.filter(publisher_is_draft=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
