from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins import BaseModelAdminMixin
from components.models import Frame, FrameMotorDetail, FrameCameraDetail, FrameVTXDetail


class FrameMotorDetailInline(admin.StackedInline):
    model = FrameMotorDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'frame'


class FrameCameraDetailInline(admin.StackedInline):
    model = FrameCameraDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'frame'


class FrameVTXDetailInline(admin.StackedInline):
    model = FrameVTXDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'frame'


@admin.register(Frame)
class FrameAdmin(BaseModelAdminMixin):
    inlines = [FrameMotorDetailInline, FrameCameraDetailInline, FrameVTXDetailInline]
    list_display = ('__str__', 'id', 'prop_size', 'size',  'material', 'configuration')
    list_filter = ('manufacturer', 'material', 'configuration')
    sortable_by = ('weight', )
    search_fields = ('model', 'id', 'prop_size', 'size')
