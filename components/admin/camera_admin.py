from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_camera_admin_mixins import CameraAdminMixin, VideoFormatAdminMixin
from components.models import Camera, VideoFormat, CameraDetail
from documents.admin.components_admin import CameraDocumentInline
from galleries.admin.components_admin import CameraGalleryInline


class CameraDetailInline(admin.StackedInline):
    model = CameraDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'camera'


@admin.register(Camera)
class CameraAdmin(CameraAdminMixin):
    inlines = [CameraDetailInline, CameraGalleryInline, CameraDocumentInline]


@admin.register(VideoFormat)
class VideoFormatAdmin(VideoFormatAdminMixin):
    pass