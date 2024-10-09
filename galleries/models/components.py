from django.db import models
from django.utils.translation import gettext_lazy as _

from galleries.mixins import BaseImageMixin


class AntennaGallery(BaseImageMixin):
    object = models.ForeignKey('components.Antenna', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_antenna'
        verbose_name = _('Antenna Gallery')
        verbose_name_plural = _('Antenna Galleries')


class CameraGallery(BaseImageMixin):
    object = models.ForeignKey('components.Camera', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_camera'
        verbose_name = _('Camera Gallery')
        verbose_name_plural = _('Camera Galleries')


class FrameGallery(BaseImageMixin):
    object = models.ForeignKey('components.Frame', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_frame'
        verbose_name = _('Frame Gallery')
        verbose_name_plural = _('Frame Galleries')


class FlightControllerGallery(BaseImageMixin):
    object = models.ForeignKey('components.FlightController', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_flight_controller'
        verbose_name = _('Flight Controller Gallery')
        verbose_name_plural = _('Flight Controller Galleries')


class MotorGallery(BaseImageMixin):
    object = models.ForeignKey('components.Motor', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_motor'
        verbose_name = _('Motor Gallery')
        verbose_name_plural = _('Motor Galleries')


class PropellerGallery(BaseImageMixin):
    object = models.ForeignKey('components.Propeller', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_propeller'
        verbose_name = _('Propeller Gallery')
        verbose_name_plural = _('Propeller Galleries')


class ReceiverGallery(BaseImageMixin):
    object = models.ForeignKey('components.Receiver', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_receiver'
        verbose_name = _('Receiver Gallery')
        verbose_name_plural = _('Receiver Galleries')


class StackGallery(BaseImageMixin):
    object = models.ForeignKey('components.Stack', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_stack'
        verbose_name = _('Stack Gallery')
        verbose_name_plural = _('Stack Galleries')


class SpeedControllerGallery(BaseImageMixin):
    object = models.ForeignKey('components.SpeedController', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_speed_controller'
        verbose_name = _('Speed Controller Gallery')
        verbose_name_plural = _('Speed Controller Galleries')


class TransmitterGallery(BaseImageMixin):
    object = models.ForeignKey('components.Transmitter', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'gallery_transmitter'
        verbose_name = _('Transmitter Gallery')
        verbose_name_plural = _('Transmitter Galleries')
