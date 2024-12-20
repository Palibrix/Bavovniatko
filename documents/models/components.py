from django.db import models
from django.utils.translation import gettext_lazy as _

from documents.mixins import BaseDocumentMixin


class AntennaDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Antenna', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_antenna'
        verbose_name = _('Antenna Document')
        verbose_name_plural = _('Antenna Documents')
        ordering = ['object',  '-created_at']


class CameraDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Camera', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_camera'
        verbose_name = _('Camera Document')
        verbose_name_plural = _('Camera Documents')
        ordering = ['object',  '-created_at']


class FrameDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Frame', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_frame'
        verbose_name = _('Frame Document')
        verbose_name_plural = _('Frame Documents')
        ordering = ['object',  '-created_at']


class FlightControllerDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.FlightController', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_flight_controller'
        verbose_name = _('Flight Controller Document')
        verbose_name_plural = _('Flight Controller Documents')
        ordering = ['object',  '-created_at']


class MotorDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Motor', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_motor'
        verbose_name = _('Motor Document')
        verbose_name_plural = _('Motor Documents')
        ordering = ['object',  '-created_at']


class PropellerDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Propeller', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_propeller'
        verbose_name = _('Propeller Document')
        verbose_name_plural = _('Propeller Documents')
        ordering = ['object',  '-created_at']


class ReceiverDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Receiver', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_receiver'
        verbose_name = _('Receiver Document')
        verbose_name_plural = _('Receiver Documents')
        ordering = ['object',  '-created_at']


class StackDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Stack', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_stack'
        verbose_name = _('Stack Document')
        verbose_name_plural = _('Stack Documents')
        ordering = ['object',  '-created_at']


class SpeedControllerDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.SpeedController', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_speed_controller'
        verbose_name = _('Speed Controller Document')
        verbose_name_plural = _('Speed Controller Documents')
        ordering = ['object',  '-created_at']


class TransmitterDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Transmitter', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        db_table = 'documents_transmitter'
        verbose_name = _('Transmitter Document')
        verbose_name_plural = _('Transmitter Documents')
        ordering = ['object',  '-created_at']
