from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class BaseListMixin(models.Model):
    """
    Base mixin for list functionality. Provides common fields and methods
    that any type of list might need.

    This mixin focuses on the core list attributes, making it reusable if we
    need to create other types of lists in the future (like wishlists, comparisons, etc.)
    """
    name = models.CharField(
        max_length=100,
        help_text=_('Name of your list')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Optional description for this list')
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss'  # Will become 'lists' for List model
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.owner}'s {self.name}"


class BaseListItemMixin(models.Model):
    """
    Base mixin for items in a list. Provides the common structure for
    any type of item that can be added to a list.

    This mixin handles the relationship with the list and tracks when
    items were added, providing a foundation for list item functionality.
    """
    list = models.ForeignKey(
        'favorites.List',
        on_delete=models.CASCADE,
        related_name='+'  # Will become 'antenna_items' for AntennaListItem
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.component} in {self.list}"

    class Meta:
        abstract = True
        unique_together = [('list', 'component')]
        ordering = ['-added_at']