from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.models import Battery


class Motor(models.Model):
    # TODO: Model fields
    #   * model, manuf
    #   * Stator diameter (2 digits)
    #   * Stator Height
    #   * Configuration
    #   * get_stator_size (rotor)
    # mount_height = models.FloatField(max_length=5, help_text="Height of the motor in mm",
    #                                            verbose_name="Motor mount size height")
    # mount_width = models.FloatField(max_length=5, help_text="Width of the motor in mm",
    #                                           verbose_name="Motor mount size width")
    #
    pass


class MotorDetail(models.Model):
    # TODO: Model fields
    #   * Motor
    #   * Weight
    #   * Max power
    #   * kv_per_volt
    #   * Peak current
    #   * Idle current
    #   * Internal resistance
    #   * FK to MotorRatedVoltage

    pass


class MotorRatedVoltage(models.Model):
    min_cells = models.IntegerField(validators=[MinValueValidator(1)], default=1,
                                    verbose_name=_('Min. number of cells'), help_text=_('In number'))
    max_cells = models.IntegerField(validators=[MinValueValidator(1)], default=1,
                                    verbose_name=_('Max. number of cells'), help_text=_('In number'))
    type = models.CharField(max_length=10, choices=Battery.Types.choices, default=Battery.Types.LIPO)

    def __str__(self):
        return f'{self.min_cells}S-{self.max_cells}S {self.type}'

    class Meta:
        app_label = 'components'
        db_table = 'components_motor_rated_voltage'

        verbose_name = _('Motor Rated Voltage')
        verbose_name_plural = _('Motor Rated Voltages')


class MotorDetailTestFiles(models.Model):
    motor_detail = models.ForeignKey('MotorDetail', on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='motors/tests')

    def __str__(self):
        return f"{self.motor_detail.motor.model} {self.motor_detail.get_kv_per_volt} Test documentation"

    class Meta:
        app_label = 'components'
        db_table = 'components_motor_test_files'

        verbose_name = 'Motor Test Documentation'
        verbose_name_plural = 'Motor Test Documentations'
