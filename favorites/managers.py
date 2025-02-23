from django.db import models
from django.db.models import QuerySet
from itertools import chain


class ListItemQuerySet(QuerySet):
    """
    Custom QuerySet for list items that provides additional functionality
    for working with components.
    """

    def include_component_data(self):
        """
        Includes the related component data in the queryset to prevent
        additional database queries when accessing component details.
        """
        return self.select_related('component')


class ListItemManager(models.Manager):
    """
    Custom manager for list items that provides methods for efficiently
    working with components in lists.
    """

    def get_queryset(self):
        return ListItemQuerySet(self.model, using=self._db)

    def include_component_data(self):
        """
        Returns a queryset with all component data preloaded.
        This helps prevent the N+1 query problem when accessing component details.
        """
        return self.get_queryset().include_component_data()
