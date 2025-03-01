from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_motor_admin_mixins import MotorAdminMixin, RatedVoltageAdminMixin
from components.models import MotorDetail, Motor, RatedVoltage
from documents.admin.components_admin import MotorDocumentInline
from galleries.admin.components_admin import MotorGalleryInline


class MotorDetailInline(admin.StackedInline):
    model = MotorDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'motor'


@admin.register(Motor)
class MotorAdmin(MotorAdminMixin):
    inlines = [MotorDetailInline, MotorGalleryInline, MotorDocumentInline]


@admin.register(RatedVoltage)
class RatedVoltageAdmin(RatedVoltageAdminMixin):
    pass