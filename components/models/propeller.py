from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from components.mixins import UniqueConstraintMixin

User = get_user_model()


class Propeller(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model', 'size', 'pitch', 'blade_count', 'weight']
    fields_private = ['manufacturer', 'model', 'size', 'pitch', 'blade_count', 'user']
    error_message = 'A Propeller with these attributes already exists for this user.'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")
    size = models.IntegerField(validators=[MinValueValidator(2)],
                               help_text="Size of the propeller in inches")
    pitch = models.FloatField(help_text="Pitch of the propeller in inches")
    blade_count = models.CharField(max_length=8,
                                   choices=[(str(i), str(i)) for i in range(2, 9)] + [('another', 'Another')], )
    weight = models.FloatField(help_text="Weight of propeller in grams",
                               blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_propeller'

        verbose_name = 'Propeller'
        verbose_name_plural = 'Propellers'
        ordering = ['model', ]
