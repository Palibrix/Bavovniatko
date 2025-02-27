from itertools import chain

from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from components.mixins import BaseModelMixin
from .managers import ListItemManager
from .mixins import BaseListMixin, BaseListItemMixin


class List(BaseListMixin, BaseModelMixin):
    """
    Represents a user's list of favorite components.
    Users can create multiple lists to organize their components.
    """

    COMPONENT_TYPES = [
        'antenna',
        'camera',
        'flight_controller',
        'speed_controller',
        'motor',
        'propeller',
        'receiver',
        'stack',
        'transmitter'
    ]

    def get_all_items(self):
        """
        Returns all items in the list, sorted by when they were added.
        Uses the COMPONENT_TYPES list to ensure we include all component types.
        """
        item_querysets = []
        for component_type in self.COMPONENT_TYPES:
            # Convert 'antenna' to 'antenna_items' to match related_name
            related_name = f"{component_type}_items"
            if hasattr(self, related_name):
                items = getattr(self, related_name).include_component_data()
                item_querysets.append(items)

        all_items = sorted(
            chain(*item_querysets),
            key=lambda x: x.added_at,
            reverse=True
        )
        return all_items

    @property
    def count_all(self):
        """
        Counts all items in the list using a single database query.
        More efficient than counting each type separately.
        """
        counts = {}
        for component_type in self.COMPONENT_TYPES:
            counts[f"{component_type}_count"] = Count(f"{component_type}_items")

        result = List.objects.filter(id=self.id).aggregate(**counts)
        return sum(result.values())

    def count_by_type(self):
        """
        Returns a dictionary with counts for each component type.
        Useful for displaying detailed statistics about the list.
        """
        counts = {}
        for component_type in self.COMPONENT_TYPES:
            related_name = f"{component_type}_items"
            if hasattr(self, related_name):
                counts[component_type] = getattr(self, related_name).count()
        return counts

    class Meta:
        unique_together = [('owner', 'name')]
        ordering = ['owner', 'name']
        verbose_name = _('List')
        verbose_name_plural = _('Lists')


class AntennaListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='antenna_items'
    )
    component = models.ForeignKey(
        'components.Antenna',
        on_delete=models.CASCADE,
        related_name='list_items'
    )

    objects = ListItemManager()

    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Antenna List Item')
        verbose_name_plural = _('Antenna List Items')


class CameraListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='camera_items'
    )
    component = models.ForeignKey(
        'components.Camera',
        on_delete=models.CASCADE,
        related_name='list_items'
    )

    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Camera List Item')
        verbose_name_plural = _('Camera List Items')


class FrameListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='frame_items'
    )
    component = models.ForeignKey(
        'components.Frame',
        on_delete=models.CASCADE,
        related_name='list_items'
    )

    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Frame List Item')
        verbose_name_plural = _('Frame List Items')


class FlightControllerListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='flight_controller_items'
    )
    component = models.ForeignKey(
        'components.FlightController',
        on_delete=models.CASCADE,
        related_name='list_items'
    )

    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Flight Controller List Item')
        verbose_name_plural = _('Flight Controller List Items')


class SpeedControllerListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='speed_controller_items'
    )
    component = models.ForeignKey(
        'components.SpeedController',
        on_delete=models.CASCADE,
        related_name='list_items'
    )

    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Speed Controller List Item')
        verbose_name_plural = _('Speed Controller List Items')


class MotorListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='motor_items'
    )
    component = models.ForeignKey(
        'components.Motor',
        on_delete=models.CASCADE,
        related_name='list_items'
    )
    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Motor List Item')
        verbose_name_plural = _('Motor List Items')


class PropellerListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='propeller_items'
    )
    component = models.ForeignKey(
        'components.Propeller',
        on_delete=models.CASCADE,
        related_name='list_items'
    )
    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Propeller List Item')
        verbose_name_plural = _('Propeller List Items')


class ReceiverListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='receiver_items'
    )
    component = models.ForeignKey(
        'components.Receiver',
        on_delete=models.CASCADE,
        related_name='list_items'
    )

    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        unique_together = [('list', 'component')]
        verbose_name = _('Receiver List Item')
        verbose_name_plural = _('Receiver List Items')


class StackListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='stack_items'
    )
    component = models.ForeignKey(
        'components.Stack',
        on_delete=models.CASCADE,
        related_name='list_items'
    )
    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        unique_together = [('list', 'component')]
        verbose_name = _('Stack List Item')
        verbose_name_plural = _('Stack List Items')


class TransmitterListItem(BaseListItemMixin):
    list = models.ForeignKey(
        'lists.List',
        on_delete=models.CASCADE,
        related_name='transmitter_items'
    )
    component = models.ForeignKey(
        'components.Transmitter',
        on_delete=models.CASCADE,
        related_name='list_items'
    )
    objects = ListItemManager()
    class Meta(BaseListItemMixin.Meta):
        verbose_name = _('Transmitter List Item')
        verbose_name_plural = _('Transmitter List Items')
