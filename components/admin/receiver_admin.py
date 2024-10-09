from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins import BaseModelAdminMixin
from components.models import Receiver, ReceiverDetail, ReceiverProtocolType
from galleries.admin.components_admin import ReceiverGalleryInline


class ReceiverDetailInline(admin.StackedInline):
    model = ReceiverDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'receiver'


@admin.register(Receiver)
class ReceiverAdmin(BaseModelAdminMixin):
    inlines = [ReceiverDetailInline, ReceiverGalleryInline]
    list_display = ('__str__', 'id', 'processor', 'get_voltage')
    list_filter = ('manufacturer',)
    search_fields = ('model', 'id', 'processor', 'manufacturer')
    sortable_by = ('manufacturer', 'voltage_min', 'voltage_max')


@admin.register(ReceiverProtocolType)
class ReceiverProtocolTypeAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id')
    search_fields = ('type',)
