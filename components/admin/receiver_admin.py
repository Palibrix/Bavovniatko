from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from .filters import IsPublicFilter
from components.mixins import IsPublicMixin
from components.models import Receiver, ReceiverDetail, ReceiverProtocolType

from django.utils.translation import gettext_lazy as _


admin.site.register(ReceiverProtocolType)


class ReceiverDetailInline(admin.StackedInline):
    model = ReceiverDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin, IsPublicMixin):
    inlines = [ReceiverDetailInline, ]
    list_display = ('model', 'id', 'processor', 'get_frequency', 'is_public')
    list_filter = ('manufacturer', IsPublicFilter)
    search_fields = ('model', 'id', 'processor', 'manufacturer')

    def get_frequency(self, obj):
        if obj.receiver_details.exists():
            frequencies = list(obj.receiver_details.values_list('frequency', flat=True))
            return frequencies
        return "No ReceiverDetail"

    get_frequency.short_description = _('Frequencies')
