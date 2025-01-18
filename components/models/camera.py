from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin
from components.mixins.base_camera_mixins import BaseCameraMixin, BaseCameraDetailMixin, BaseVideoFormatMixin


class Camera(BaseCameraMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_camera'

        verbose_name = _('Camera')
        verbose_name_plural = _('Cameras')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class CameraDetail(BaseCameraDetailMixin):

    camera = models.ForeignKey('components.Camera', on_delete=models.CASCADE, related_name="details")

    class Meta:
        app_label = 'components'
        db_table = 'components_camera_detail'

        verbose_name = _('Camera Detail')
        verbose_name_plural = _('Camera Details')
        unique_together = ['camera', 'height', 'width']

    def delete(self, *args, **kwargs):
        if self.camera.details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only detail for this Camera."), self)


class VideoFormat(BaseVideoFormatMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_video_format'

        verbose_name = _('Video Format')
        verbose_name_plural = _('Video Formats')
