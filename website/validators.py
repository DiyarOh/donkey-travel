from django.core.exceptions import ValidationError

def validate_phonenumber(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only numeric characters.')
