from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from builds.forms import RequiredInlineFormSet
from .filters import IsPublicFilter
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from components.mixins import IsPublicMixin


class AntennaDetainInline(admin.StackedInline):
    model = AntennaDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet


@admin.register(Antenna)
class AntennaAdmin(admin.ModelAdmin, IsPublicMixin):
    inlines = [AntennaDetainInline, ]
    list_display = ('model', 'id', 'type', 'center_frequency', 'bandwidth_range', 'user', 'is_public')
    list_filter = ('manufacturer', 'type', IsPublicFilter)
    search_fields = ('model', 'id', 'type', 'swr')

    @admin.display(description=_('Bandwidth Range'))
    def bandwidth_range(self, obj):
        return f'{obj.bandwidth_min} - {obj.bandwidth_max}'
    

@admin.register(AntennaType)
class AntennaTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'direction', 'polarization', 'is_public')
    list_filter = ('type', 'direction', 'polarization', 'is_public')
    search_fields = ('type',)


@admin.register(AntennaConnector)
class AntennaConnectorAdmin(admin.ModelAdmin):
    list_display = ('type', 'is_public')
    list_filter = ('type', 'is_public')
    search_fields = ('type',)
