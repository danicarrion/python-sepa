from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from sepa.utils.iban import is_valid


def validate_iban(value):
    if not is_valid(value):
        raise ValidationError(_("%s is not an well-formed IBAN") % value)
