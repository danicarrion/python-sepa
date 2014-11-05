from django.db import models
from django.utils.translation import ugettext_lazy as _

from sepa.django.forms import IBANFormField


class IBANField(models.Field):
    """
    http://en.wikipedia.org/wiki/International_Bank_Account_Number
    """
    description = _("International Bank Account Number")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 34
        super(IBANField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(IBANField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'form_class': IBANFormField}
        defaults.update(kwargs)
        return super(IBANField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ["^sepa\.django\.IBANField"])
