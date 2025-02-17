from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins.base_motor_mixins import (
    BaseMotorMixin,
    BaseMotorDetailMixin,
    BaseRatedVoltageMixin
)


class Motor(BaseMotorMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_motor'
        verbose_name = _("Motor")
        verbose_name_plural = _("Motors")
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class MotorDetail(BaseMotorDetailMixin):
    motor = models.ForeignKey('Motor', on_delete=models.CASCADE, related_name='details')

    def delete(self, *args, **kwargs):
        if self.motor.details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only MotorDetail for this Motor."), self)

    class Meta:
        app_label = 'components'
        db_table = 'components_motor_details'
        verbose_name = _("Motor Detail")
        verbose_name_plural = _("Motor Details")
        unique_together = ('motor', 'kv_per_volt')


class RatedVoltage(BaseRatedVoltageMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_rated_voltage'
        verbose_name = _('Rated Voltage')
        verbose_name_plural = _('Rated Voltages')