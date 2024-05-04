from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_fov_length(value):
    if len(str(value)) not in (2, 3):
        raise ValidationError(
            _("%(value)s length must be between 2 and 3"),
            params={"value": value},
        )
