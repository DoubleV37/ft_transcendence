from django.core.exceptions import ValidationError


import logging
logger = logging.getLogger(__name__)


def validate_file_extension(value: str):
    ext = str(value).split('.')  # [0] returns path+filename
    valid_extensions = ['jpg', 'png']
    if ext[1] not in valid_extensions:
        raise ValidationError('Unsupported file extension.')
