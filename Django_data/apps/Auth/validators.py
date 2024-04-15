from django.core.exceptions import ValidationError


def validate_file_extension(value: str):
    import os
    # ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.xlsx', '.xls']
    if not value.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
