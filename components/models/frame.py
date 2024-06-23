from django.contrib.auth import get_user_model
from django.db import models

from components.mixins import UniqueConstraintMixin

User = get_user_model()


class Frame(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model', 'prop_size', 'size',
                     'weight', 'material', 'configuration'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A Frame with these attributes already exists for this user.'

    class MaterialChoice(models.TextChoices):
        ALUMINIUM = 'aluminum', 'Aluminium'
        FIBRE = 'fibre', 'Carbon fibre'

    class ConfigurationChoice(models.TextChoices):
        H_FRAME = 'h', 'H Frame'
        X = 'x', 'X Frame'
        HYBRID = 'hybrid', 'Hybrid-X'
        BOX = 'box', 'Box'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")
    prop_size = models.CharField(max_length=50, help_text="Propeller size in inches",
                                 verbose_name="Propeller size")
    size = models.CharField(max_length=50, help_text="Size(Diagonal) of the frame in mm",
                            verbose_name="Frame size",
                            blank=True, null=True)

    weight = models.FloatField(help_text='Weight oh the frame in grams',
                               blank=True, null=True)
    material = models.CharField(max_length=50, choices=MaterialChoice.choices,
                                blank=True, null=True)
    configuration = models.CharField(max_length=50, choices=ConfigurationChoice.choices,
                                     blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame'

        verbose_name = 'Frame'
        verbose_name_plural = 'Frames'
        ordering = ['manufacturer', 'model', ]


class FrameDetail(models.Model):
    frame = models.ForeignKey('Frame', on_delete=models.CASCADE, related_name='frame_details')

    camera_mount_height = models.FloatField(max_length=5, help_text="Height of the camera in mm",
                                            verbose_name="Camera mount size height")
    camera_mount_width = models.FloatField(max_length=5, help_text="Width of the camera in mm",
                                           verbose_name="Camera mount size width")

    motor_mount_height = models.FloatField(max_length=5, help_text="Height of the motor in mm",
                                           verbose_name="Motor mount size height")
    motor_mount_width = models.FloatField(max_length=5, help_text="Width of the motor in mm",
                                          verbose_name="Motor mount size width")

    vtx_mount_height = models.FloatField(max_length=5, help_text="Height of the vtx in mm",
                                         verbose_name="VTX mount size height")
    vtx_mount_width = models.FloatField(max_length=5, help_text="Width of the vtx in mm",
                                        verbose_name="VTX mount size width")

    def __str__(self):
        return self.frame.model

    def delete(self, *args, **kwargs):
        if self.frame.frame_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only FrameDetail for this Frame.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_detail'

        verbose_name = 'FrameDetail'
        verbose_name_plural = 'FrameDetails'
        ordering = ('frame__manufacturer', 'frame__model')
        unique_together = ['frame', 'camera_mount_height', 'camera_mount_width',
                           'motor_mount_height', 'motor_mount_width',
                           'vtx_mount_height', 'vtx_mount_width']
