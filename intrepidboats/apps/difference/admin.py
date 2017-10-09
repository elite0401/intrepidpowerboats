from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import SharedTestimonial


@admin.register(SharedTestimonial)
class SharedTestimonialAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'title', 'truncated_message']

    def has_add_permission(self, request):
        return False

    # pylint:disable=E1136
    def truncated_message(self, obj):
        return (obj.message[:47] + '...') if len(obj.message) > 50 else obj.message
    truncated_message.short_description = _('message')
