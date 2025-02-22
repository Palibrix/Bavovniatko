from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_motor_mixins import BaseMotorMixin, BaseMotorDetailMixin, BaseRatedVoltageMixin
from components.models import Motor, MotorDetail, RatedVoltage
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin, MediaHandlerMixin


class MotorSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseMotorMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Motor', blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)
        self._handle_details(instance)

    def _handle_details(self, motor):
        for suggested_detail in self.suggested_details.all():
            motor_detail = MotorDetail.objects.create(
                motor=motor,
                **{field: getattr(suggested_detail, field)
                   for field in BaseMotorDetailMixin.DETAIL_FIELDS}
            )
            motor_detail.full_clean()
            motor_detail.save()

            suggested_detail.related_instance = motor_detail
            suggested_detail.save()

    def _create_instance(self):
        motor = Motor.objects.create(
            **{field: getattr(self, field)
               for field in self.MOTOR_FIELDS}
        )
        motor.full_clean()
        motor.save()

        self.related_instance = motor
        self.save()
        return motor

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_motor'
        verbose_name = _('Motor Suggestion')
        verbose_name_plural = _('Motor Suggestions')
        ordering = ['manufacturer', 'model']


class RatedVoltageSuggestion(BaseRatedVoltageMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.RatedVoltage', blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       on_delete=models.CASCADE)

    def _create_instance(self):
        voltage = RatedVoltage.objects.create(
            **{field: getattr(self, field)
               for field in self.VOLTAGE_FIELDS}
        )
        voltage.full_clean()
        voltage.save()

        self.related_instance = voltage
        self.save()
        return voltage

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_rated_voltage'
        verbose_name = _('Rated Voltage Suggestion')
        verbose_name_plural = _('Rated Voltage Suggestions')
        ordering = ['min_cells', 'max_cells']


class SuggestedMotorDetailSuggestion(BaseMotorDetailMixin):
    suggestion = models.ForeignKey('suggestions.MotorSuggestion', on_delete=models.CASCADE,
                                 related_name='suggested_details',
                                 verbose_name='details')
    related_instance = models.ForeignKey('components.MotorDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       verbose_name='submitted_suggestions')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Detail for this Motor."), self)

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_motor_detail'
        verbose_name = _('Suggested Motor Detail')
        verbose_name_plural = _('Suggested Motor Details')
        ordering = ['related_instance']


class ExistingMotorDetailSuggestion(BaseMotorDetailMixin, BaseSuggestionMixin):
    motor = models.ForeignKey('components.Motor', on_delete=models.CASCADE,
                           related_name='suggested_details',
                           verbose_name='Motor')
    related_instance = models.ForeignKey('components.MotorDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='suggested_details')

    def _create_instance(self):
        instance = MotorDetail.objects.create(
            motor=self.motor,
            **{field: getattr(self, field)
               for field in self.DETAIL_FIELDS}
        )
        instance.full_clean()
        instance.save()
        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_motor_detail'
        verbose_name = _('Existing Motor Detail Suggestion')
        verbose_name_plural = _('Existing Motor Detail Suggestions')
        ordering = ['motor']