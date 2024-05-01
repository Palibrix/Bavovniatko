from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_integer_length(value):
    if len(str(value)) not in (2, 3):
        raise ValidationError(
            _("%(value)s length must be between 2 and 3"),
            params={"value": value},
        )


def validate_even_number(value):
    if value % 2 == 0:
        raise ValidationError(
            _("%(value)s even number must be even"),
        )
