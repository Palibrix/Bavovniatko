from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.admin import IsPublicFilter
from components.mixins import IsPublicMixin
from components.models import MotorDetail, Motor, RatedVoltage


class MotorDetailInline(admin.StackedInline):
    model = MotorDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet


@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'get_stator_size', 'get_mount_params')
    list_filter = ('manufacturer', IsPublicFilter)
    search_fields = ('manufacturer', 'model')
    inlines = [MotorDetailInline, ]


@admin.register(RatedVoltage)
class RatedVoltageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'min_cells', 'max_cells', 'type')
    list_filter = ('type',)
