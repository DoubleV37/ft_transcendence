from django.core.exceptions import ValidationError


def validate_file_extension(value: str):
    import os
    # ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.xlsx', '.xls']
    if not value.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# def image_size(value: str):
#         image = cleaned_data.get('image', False)
#         if image:
#             if image._size > 4*1024*1024:
#                 raise ValidationError("Image file too large ( > 4mb )")
#             return image
#         else:
#             raise ValidationError("Couldn't read uploaded image")
