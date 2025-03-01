from itertools import chain

from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from components.mixins import BaseModelMixin
from .managers import ListItemManager
from .mixins import BaseListMixin, BaseListItemMixin
from .registry import ComponentRegistry


class List(BaseListMixin, BaseModelMixin):
    """
    Represents a user's list of favorite components.
    Users can create multiple lists to organize their components.
    """

    def get_all_items(self):
        """
        Returns all items in the list, sorted by when they were added.
        Uses a more efficient approach that works with all databases.
        """
        # Use a list to collect all items
        all_items = []

        for component_type in ComponentRegistry.get_all_types():
            related_name = f"{component_type}_items"
            if not hasattr(self, related_name):
                continue

            # Get items for this component type
            items = getattr(self, related_name).include_component_data()

            # Add component type info to each item
            for item in items:
                # Set an attribute so the template can determine the component type
                item.component_type = component_type
                all_items.append(item)

        # Sort by added_at (newest first)
        return sorted(all_items, key=lambda x: x.added_at, reverse=True)
    
    

    @property
    def count_all(self) -> int:
        """
        Counts all items in the list using a single database query.
        More efficient than counting each type separately.
        """
        return sum(self.count_by_type().values())

    def count_by_type(self) -> dict:
        """
        Returns a dictionary with counts for each component type.
        Useful for displaying detailed statistics about the list.
        """
        counts = {}
        for component_type in ComponentRegistry.get_all_types():
            counts[f"{component_type}"] = Count(f"{component_type}_items", distinct=True)

        result = List.objects.filter(id=self.id).aggregate(**counts)
        return result

    def filter_by_type(self, component_type):
        """
        Return all items of a specific component type, sorted by added_at.
        """
        related_name = f"{component_type}_items"
        if hasattr(self, related_name):
            return getattr(self, related_name).include_component_data().order_by('-added_at')
        return []

    def remove_items_bulk(self, items_data):
        """
        Remove multiple items at once.

        items_data should be a list of dicts like:
        [
            {'component_type': 'antenna', 'component_id': 1},
            {'component_type': 'camera', 'component_id': 3},
        ]

        Returns number of items removed.
        """
        removed_count = 0

        for item_data in items_data:
            component_type = item_data.get('component_type')
            component_id = item_data.get('component_id')

            if not component_type or not component_id:
                continue

            related_name = f"{component_type}_items"
            if not hasattr(self, related_name):
                continue

            result = getattr(self, related_name).filter(component_id=component_id).delete()
            removed_count += result[0]  # Django delete() returns (count, details) tuple

        return removed_count

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
