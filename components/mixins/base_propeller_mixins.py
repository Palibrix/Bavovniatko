from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class BasePropellerMixin(BaseComponentMixin):
    PROPELLER_FIELDS = [
        'manufacturer', 'model', 'description',
        'size', 'pitch', 'blade_count', 'weight'
    ]

    class BladeChoices(models.TextChoices):
        TWO = '2', _('2 blades')
        THREE = '3', _('3 blades')
        FOUR = '4', _('4 blades')
        FIVE = '5', _('5 blades')
        SIX = '6', _('6 blades')
        SEVEN = '7', _('7 blades')
        EIGHT = '8', _('8 blades')
        ANOTHER = 'another', _('Another')

    size = models.IntegerField(
        validators=[MinValueValidator(2)],
        help_text=_("Size of the propeller in inches"),
        verbose_name=_("Size")
    )
    pitch = models.FloatField(
        help_text=_("Pitch of the propeller in inches"),
        verbose_name=_("Pitch")
    )
    blade_count = models.CharField(
        max_length=8,
        choices=BladeChoices.choices,
        help_text=_("Number of propeller blades"),
        verbose_name=_("Blade Count")
    )
    weight = models.FloatField(
        help_text=_("Weight of propeller in grams"),
        verbose_name=_("Weight"),
        blank=True, null=True
    )

    @property
    @admin.display(description=_('Size/Pitch'))
    def get_size_pitch(self):
        return f'{self.size}x{self.pitch}'

    class Meta:
        abstract = True