from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class Frame(BaseComponentMixin):

    class MaterialChoice(models.TextChoices):
        ALUMINIUM = 'aluminum', _('Aluminium')
        FIBRE = 'fibre', _('Carbon fibre')
        ANOTHER = 'another', _('Another')

    class ConfigurationChoice(models.TextChoices):
        H_FRAME = 'h', _('H Frame')
        X = 'x', _('X Frame')
        HYBRID = 'hybrid', _('Hybrid-X')
        BOX = 'box', _('Box')
        ANOTHER = 'another', _('Another')

    prop_size = models.CharField(max_length=50, help_text=_("Propeller size in inches"),
                                 verbose_name=_("Propeller size"))
    size = models.CharField(max_length=50, help_text=_("Size(Diagonal) of the frame in mm"),
                            verbose_name=_("Frame size"))

    weight = models.FloatField(help_text=_('Weight oh the frame in grams'),
                               blank=True, null=True)
    material = models.CharField(max_length=50, choices=MaterialChoice.choices)
    configuration = models.CharField(max_length=50, choices=ConfigurationChoice.choices)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame'

        verbose_name = _('Frame')
        verbose_name_plural = _('Frames')
        ordering = ['manufacturer', 'model', ]
        unique_together = (('manufacturer', 'model', ),)


class FrameCameraDetail(BaseModelMixin):
    frame = models.ForeignKey('Frame', on_delete=models.CASCADE, related_name='camera_details')

    camera_mount_height = models.FloatField(max_length=5, help_text=_("Height of the camera in mm"),
                                            verbose_name=_("Camera mount size height"))
    camera_mount_width = models.FloatField(max_length=5, help_text=_("Width of the camera in mm"),
                                           verbose_name=_("Camera mount size width"))

    @property
    @admin.display(description=_("Camera mount dimensions"))
    def get_camera_mount_dimensions(self):
        return f'{self.camera_mount_height}x{self.camera_mount_width}mm'

    def __str__(self):
        return f'Camera: {self.get_camera_mount_dimensions}'

    def delete(self, *args, **kwargs):
        if self.frame.camera_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only Camera Mounting Detail for this Frame.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_camera_detail'

        verbose_name = _('Frame Camera Detail')
        verbose_name_plural = _('Frame Camera Details')
        ordering = ('id', )
        unique_together = ['frame', 'camera_mount_height', 'camera_mount_width']


class FrameMotorDetail(BaseModelMixin):
    frame = models.ForeignKey('Frame', on_delete=models.CASCADE, related_name='motor_details')

    motor_mount_height = models.FloatField(max_length=5, help_text=_("Height of the motor in mm"),
                                           verbose_name=_("Motor mount size height"))
    motor_mount_width = models.FloatField(max_length=5, help_text=_("Width of the motor in mm"),
                                          verbose_name=_("Motor mount size width"))

    @property
    @admin.display(description=_("Motor mount dimensions"))
    def get_motor_mount_dimensions(self):
        return f'{self.motor_mount_height}x{self.motor_mount_width}mm'

    def __str__(self):
        return f'Motor: {self.get_motor_mount_dimensions}'

    def delete(self, *args, **kwargs):
        if self.frame.motor_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only Motor Mount Detail for this Frame.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_motor_detail'

        verbose_name = _('Frame Motor Detail')
        verbose_name_plural = _('Frame Motor Details')
        ordering = ('id', )
        unique_together = ['frame', 'motor_mount_height', 'motor_mount_width']


class FrameVTXDetail(BaseModelMixin):
    frame = models.ForeignKey('Frame', on_delete=models.CASCADE, related_name='vtx_details')

    vtx_mount_height = models.FloatField(max_length=5, help_text=_("Height of the vtx in mm"),
                                         verbose_name=_("VTX mount size height"))
    vtx_mount_width = models.FloatField(max_length=5, help_text=_("Width of the vtx in mm"),
                                        verbose_name=_("VTX mount size width"))

    @property
    @admin.display(description=_("VTX mount dimensions"))
    def get_vtx_mount_dimensions(self):
        return f'{self.vtx_mount_height}x{self.vtx_mount_width}mm'

    def __str__(self):
        return f'VTX: {self.get_vtx_mount_dimensions}'

    def delete(self, *args, **kwargs):
        if self.frame.vtx_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only VTX Mounting Detail for this Frame.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_vtx_detail'

        verbose_name = _('Frame VTX Detail')
        verbose_name_plural = _('Frame VTX Details')
        ordering = ('id', )
        unique_together = ['frame', 'vtx_mount_height', 'vtx_mount_width']
