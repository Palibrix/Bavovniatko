from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins import BaseModelAdminMixin
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from galleries.admin import AntennaGalleryInline


class AntennaDetailInline(admin.StackedInline):
    model = AntennaDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'antenna'


@admin.register(Antenna)
class AntennaAdmin(BaseModelAdminMixin):
    inlines = [AntennaDetailInline, AntennaGalleryInline]
    list_display = ('__str__', 'id', 'type', 'center_frequency', 'get_bandwidth', 'swr', 'radiation')
    sortable_by = ('swr', 'radiation',)
    list_filter = ('manufacturer', 'type', 'center_frequency', 'swr')
    search_fields = ('manufacturer', 'model', 'id',)


@admin.register(AntennaType)
class AntennaTypeAdmin(BaseModelAdminMixin):
    list_display = ('__str__',)
    list_filter = ('direction', 'polarization',)
    search_fields = ('type',)


@admin.register(AntennaConnector)
class AntennaConnectorAdmin(BaseModelAdminMixin):
    list_display = ('__str__', )
    list_filter = ('type', )
    search_fields = ('type',)
