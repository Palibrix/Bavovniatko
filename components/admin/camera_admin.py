from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins import BaseModelAdminMixin
from components.models import Camera, VideoFormat, CameraDetail


class CameraDetailInline(admin.StackedInline):
    model = CameraDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'camera'


@admin.register(Camera)
class CameraAdmin(BaseModelAdminMixin):
    inlines = [CameraDetailInline,]

    list_display = ('__str__', 'id', 'output_type', 'tvl', 'get_voltage', 'light_sens', 'ratio', 'fov')
    list_filter = ('manufacturer', 'light_sens', 'output_type', 'ratio')
    sortable_by = ('weight',)
    search_fields = ('model', 'manufacturer', 'id', 'tvl')


@admin.register(VideoFormat)
class VideoFormatAdmin(BaseModelAdminMixin):
    list_display = ('__str__',)
    list_filter = ('format',)
    search_fields = ('format',)
