# from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class BaseDroneMixin(models.Model):

    class TypeChoices(models.TextChoices):
        PHOTOGRAPHY = 'photography', _('Photography')
        SPORT = 'sport', _('Sport')
        FREESTYLE = 'freestyle', _('Freestyle')
        ANOTHER = 'another', _('Another')

    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, help_text=_("Full name of the Drone"))
    description = CKEditor5Field('Text', blank=True, help_text=_("Long description of the Drone"))
    short_description = models.CharField(max_length=256, help_text=_("Short description of the Drone"),
                                         blank=True, null=True)
    type = models.CharField(choices=TypeChoices.choices, max_length=50, default=TypeChoices.PHOTOGRAPHY)

    antenna = models.ForeignKey('components.Antenna', on_delete=models.SET_NULL, null=True, blank=True)
    battery = models.OneToOneField('components.Battery', on_delete=models.SET_NULL, null=True, blank=True)
    camera = models.ForeignKey('components.Camera', on_delete=models.SET_NULL, null=True, blank=True)
    frame = models.ForeignKey('components.Frame', on_delete=models.SET_NULL, null=True, blank=True)
    motor = models.ForeignKey('components.Motor', on_delete=models.SET_NULL, null=True, blank=True)
    propeller = models.ForeignKey('components.Propeller', on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey('components.Receiver', on_delete=models.SET_NULL, null=True, blank=True)
    transmitter = models.ForeignKey('components.Transmitter', on_delete=models.SET_NULL, null=True, blank=True)

    flight_controller = models.ForeignKey('components.FlightController', on_delete=models.SET_NULL,
                                          null=True, blank=True)
    speed_controller = models.ForeignKey('components.SpeedController', on_delete=models.SET_NULL,
                                         null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manufacturer} {self.model}" if self.manufacturer else self.model

    class Meta:
        abstract = True
