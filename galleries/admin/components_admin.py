from django.contrib import admin

from galleries.mixins import BaseGalleryInlineAdminMixin
from galleries.models import *


class AntennaGalleryInline(BaseGalleryInlineAdminMixin):
    model = AntennaGallery
    readonly_fields = ('object', 'suggestion', 'accepted', 'created_at')

admin.site.register(AntennaGallery)

class CameraGalleryInline(BaseGalleryInlineAdminMixin):
    model = CameraGallery


class FrameGalleryInline(BaseGalleryInlineAdminMixin):
    model = FrameGallery


class FlightControllerGalleryInline(BaseGalleryInlineAdminMixin):
    model = FlightControllerGallery


class MotorGalleryInline(BaseGalleryInlineAdminMixin):
    model = MotorGallery


class PropellerGalleryInline(BaseGalleryInlineAdminMixin):
    model = PropellerGallery


class ReceiverGalleryInline(BaseGalleryInlineAdminMixin):
    model = ReceiverGallery


class StackGalleryInline(BaseGalleryInlineAdminMixin):
    model = StackGallery


class SpeedControllerGalleryInline(BaseGalleryInlineAdminMixin):
    model = SpeedControllerGallery


class TransmitterGalleryInline(BaseGalleryInlineAdminMixin):
    model = TransmitterGallery
