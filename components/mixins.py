from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class IsPublicMixin:
    @admin.display(boolean=True, description=_('Is Public?'))
    def is_public(self, obj):
        return obj.user is None


class UniqueConstraintMixin:
    # Define class-level attributes for fields and error message
    fields_public = []
    fields_private = []
    error_message = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.constraints = self.get_unique_constraints()

    def get_unique_constraints(self):
        # Generate constraints based on class-level attributes

        constraints = [
            # For user == null only
            models.UniqueConstraint(fields=self.fields_public, name='unique_component_when_public',
                                    condition=Q(user__isnull=True),
                                    violation_error_message=self.error_message),
            # For user != null only
            models.UniqueConstraint(fields=self.fields_private, name='unique_component_when_private',
                                    violation_error_message=self.error_message)
        ]
        return constraints


class UniqueItemConstraintMixin:
    """
    For small, helper models like 'AntennaType', not 'Antenna', etc.
    """
    fields = []
    error_message = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.constraints = self.get_unique_constraints()

    def get_unique_constraints(self):
        constraints = [
            # For item is_public == False
            models.UniqueConstraint(fields=self.fields, name='unique_component_when_public',
                                    condition=Q(is_public=False),
                                    violation_error_message=self.error_message),
        ]
        return constraints
