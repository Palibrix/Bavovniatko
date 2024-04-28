from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .mixins import IsPublicMixin
from .models import Frame, Propeller, Camera


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


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin, IsPublicMixin):

    list_display = ('model', 'id', 'prop_size', 'size', 'user', 'is_public')
    list_filter = ('manufacturer', IsPublicFilter)
    search_fields = ('model', 'id', 'prop_size', 'size')


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
