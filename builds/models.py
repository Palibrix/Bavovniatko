from builds.mixins import BaseDroneMixin
from django.utils.translation import gettext_lazy as _

class Drone(BaseDroneMixin):

    class Meta:
        app_label = 'builds'
        db_table = 'builds_drone'

        verbose_name = _('Drone')
        verbose_name_plural = _('Drones')
        ordering = ('manufacturer', 'model')
        unique_together = (('manufacturer', 'model',),)

