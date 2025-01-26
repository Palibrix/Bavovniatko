from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins.base_frame_mixins import (
    BaseFrameMixin,
    BaseFrameCameraDetailMixin,
    BaseFrameMotorDetailMixin,
    BaseFrameVTXDetailMixin
)


class Frame(BaseFrameMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_frame'
        verbose_name = _('Frame')
        verbose_name_plural = _('Frames')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class FrameCameraDetail(BaseFrameCameraDetailMixin):
    frame = models.ForeignKey('components.Frame', on_delete=models.CASCADE, related_name='camera_details')

    def delete(self, *args, **kwargs):
        if self.frame.camera_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Camera Detail for this Frame."), self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_camera_detail'
        verbose_name = _('Frame Camera Detail')
        verbose_name_plural = _('Frame Camera Details')
        ordering = ('id',)
        unique_together = ['frame', 'camera_mount_height', 'camera_mount_width']


class FrameMotorDetail(BaseFrameMotorDetailMixin):
    frame = models.ForeignKey('components.Frame', on_delete=models.CASCADE, related_name='motor_details')

    def delete(self, *args, **kwargs):
        if self.frame.motor_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Motor Detail for this Frame."), self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_motor_detail'
        verbose_name = _('Frame Motor Detail')
        verbose_name_plural = _('Frame Motor Details')
        ordering = ('id',)
        unique_together = ['frame', 'motor_mount_height', 'motor_mount_width']


class FrameVTXDetail(BaseFrameVTXDetailMixin):
    frame = models.ForeignKey('components.Frame', on_delete=models.CASCADE, related_name='vtx_details')

    def delete(self, *args, **kwargs):
        if self.frame.vtx_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only VTX Detail for this Frame."), self)

    class Meta:
        app_label = 'components'
        db_table = 'components_frame_vtx_detail'
        verbose_name = _('Frame VTX Detail')
        verbose_name_plural = _('Frame VTX Details')
        ordering = ('id',)
        unique_together = ['frame', 'vtx_mount_height', 'vtx_mount_width']