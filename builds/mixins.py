# from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    antenna_receiver = models.ForeignKey('components.Antenna', on_delete=models.SET_NULL, null=True, blank=True, related_name='antenna_receiver')
    antenna_transmitter = models.ForeignKey('components.Antenna', on_delete=models.SET_NULL, null=True, blank=True, related_name='antenna_transmitter')
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

    total_weight = models.FloatField(
        verbose_name=_("Total Weight"),
        help_text=_("Approximate total weight of the drone in grams"),
        validators=[MinValueValidator(0)],
        blank=True, null=True
    )

    flight_duration = models.FloatField(
        verbose_name=_("Flight Duration"),
        help_text=_("Expected flight time in minutes at normal usage"),
        validators=[MinValueValidator(0)],
        blank=True, null=True
    )

    max_speed = models.FloatField(
        verbose_name=_("Maximum Speed"),
        help_text=_("Maximum speed in km/h"),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )

    control_range = models.PositiveIntegerField(
        verbose_name=_("Control Range"),
        help_text=_("Maximum control distance in meters"),
        null=True,
        blank=True
    )

    max_altitude = models.PositiveIntegerField(
        verbose_name=_("Maximum Altitude"),
        help_text=_("Maximum flying height in meters"),
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manufacturer} {self.model}" if self.manufacturer else self.model

    class Meta:
        abstract = True
