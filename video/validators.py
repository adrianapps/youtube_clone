import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    allowed_extensions = ['.mp4', '.avi', '.mkv', '.webm', '.mov', '.wmv']
    if not ext.lower() in allowed_extensions:
        raise ValidationError('Unsupported file extension.')
