from django.contrib import admin

from components.mixins.admin.base_stack_admin_mixins import (
    StackAdminMixin, FlightControllerAdminMixin, SpeedControllerAdminMixin,
    GyroAdminMixin, FlightControllerFirmwareAdminMixin, SpeedControllerFirmwareAdminMixin,
    SpeedControllerProtocolAdminMixin
)
from components.models import SpeedControllerProtocol, SpeedControllerFirmware, FlightControllerFirmware, Gyro, Stack, \
    FlightController, SpeedController
from documents.admin.components_admin import FlightControllerDocumentInline, SpeedControllerDocumentInline, \
    StackDocumentInline
from galleries.admin.components_admin import SpeedControllerGalleryInline, FlightControllerGalleryInline, \
    StackGalleryInline


@admin.register(Stack)
class StackAdmin(StackAdminMixin):
    inlines = [StackGalleryInline, StackDocumentInline]


@admin.register(FlightController)
class FlightControllerAdmin(FlightControllerAdminMixin):
    inlines = [FlightControllerGalleryInline, FlightControllerDocumentInline]


@admin.register(SpeedController)
class SpeedControllerAdmin(SpeedControllerAdminMixin):
    inlines = [SpeedControllerGalleryInline, SpeedControllerDocumentInline]


@admin.register(Gyro)
class GyroAdmin(GyroAdminMixin):
    pass


@admin.register(FlightControllerFirmware)
class FlightControllerFirmwareAdmin(FlightControllerFirmwareAdminMixin):
    pass


@admin.register(SpeedControllerFirmware)
class SpeedControllerFirmwareAdmin(SpeedControllerFirmwareAdminMixin):
    pass


@admin.register(SpeedControllerProtocol)
class SpeedControllerProtocolAdmin(SpeedControllerProtocolAdminMixin):
    pass