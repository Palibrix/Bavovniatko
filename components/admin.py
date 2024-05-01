from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from builds.forms import RequiredInlineFormSet
from .mixins import IsPublicMixin
from .models import Frame, Propeller, Camera, FrameDetail, ReceiverDetail, Receiver, AntennaConnector, ReceiverProtocol

admin.site.register(AntennaConnector)
admin.site.register(ReceiverProtocol)


class IsPublicFilter(admin.SimpleListFilter):
    title = _('Public status')
    parameter_name = 'is_public'

    def lookups(self, request, model_admin):
        return (
            ('true', _('Public')),
            ('false', _('Private')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(user__isnull=True)
        if self.value() == 'false':
            return queryset.filter(user__isnull=False)
        return queryset


class FrameDetailInline(admin.StackedInline):
    model = FrameDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet


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


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin, IsPublicMixin):
    inlines = [FrameDetailInline, ]
    list_display = ('model', 'id', 'prop_size', 'size', 'user', 'is_public', 'frame_detail_info')
    list_filter = ('manufacturer', IsPublicFilter)
    search_fields = ('model', 'id', 'prop_size', 'size')

    def frame_detail_info(self, obj):
        if obj.frame_details.exists():
            return obj.frame_details.count()
        return 'No FrameDetail'

    frame_detail_info.short_description = _('Mounting Types Q-ty')


@admin.register(Propeller)
class PropellerAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'id', 'size', 'pitch', 'blade_count', 'user', 'is_public')
    list_filter = ('manufacturer', 'blade_count', IsPublicFilter)
    search_fields = ('model', 'id', 'size', 'pitch', 'blade_count')


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'manufacturer', 'id', 'tvl', 'light_sens', 'ratio', 'user', 'is_public')
    list_filter = ('manufacturer', 'light_sens', 'output_type', 'ratio', IsPublicFilter)
    search_fields = ('model', 'manufacturer', 'id', 'tvl')
