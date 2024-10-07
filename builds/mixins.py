from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseDroneMixin(models.Model):
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text=_("Full name of the item"))
    description = RichTextField(blank=True, help_text=_("Long description of the item"))

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
        return f"{self.manufacturer} {self.model}"

    class Meta:
        abstract = True
        unique_together = (('manufacturer', 'model',),)