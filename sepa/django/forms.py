from django import forms

from sepa.django.validators import validate_iban


class IBANFormField(forms.CharField):
    """
    http://en.wikipedia.org/wiki/International_Bank_Account_Number
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 34)
        self.default_validators = [validate_iban]
        super(IBANFormField, self).__init__(*args, **kwargs)

    def prepare_value(self, value):
        """
        IBAN printed format is in groups of 4 (last group may be less).
        """
        try:
            return ' '.join(value[i:i + 4] for i in range(0, len(value), 4))
        except AttributeError:
            return None
