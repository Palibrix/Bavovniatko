from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins import BaseModelAdminMixin
from components.models import MotorDetail, Motor, RatedVoltage


class MotorDetailInline(admin.StackedInline):
    model = MotorDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'motor'


@admin.register(Motor)
class MotorAdmin(BaseModelAdminMixin):
    inlines = [MotorDetailInline, ]

    list_display = ('__str__', 'id', 'configuration', 'get_stator_size', 'get_mount_dimensions')
    list_filter = ('manufacturer', 'configuration')
    search_fields = ('manufacturer', 'model')


@admin.register(RatedVoltage)
class RatedVoltageAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'get_cells', 'type')
    list_filter = ('type', 'min_cells', 'max_cells')
    sortable_by = ('min_cells', 'max_cells')
