from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from .filters import IsPublicFilter
from components.mixins import IsPublicMixin
from components.models import Frame, FrameDetail

from django.utils.translation import gettext_lazy as _


class FrameDetailInline(admin.StackedInline):
    model = FrameDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet


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
