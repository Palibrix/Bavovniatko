from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_frame_admin_mixins import FrameAdminMixin
from components.models import Frame, FrameMotorDetail, FrameCameraDetail, FrameVTXDetail
from documents.admin.components_admin import FrameDocumentInline
from galleries.admin.components_admin import FrameGalleryInline


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
class FrameAdmin(FrameAdminMixin):
    inlines = [FrameMotorDetailInline, FrameCameraDetailInline, FrameVTXDetailInline, FrameGalleryInline, FrameDocumentInline]