from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def validate_only_letters_or_space(value):
    for ch in value:
        if not ch.isalpha() or ' ':
            raise ValidationError('Value must contain only letters')


# def validate_file_max_size_in_mb(max_size):
#     def validate(value):
#         filesize = value.file.size
#         if filesize > max_size * 1024 * 1024:
#             raise ValidationError("Max file size is %sMB" % str(max_size))
#
#     return validate


# class MaxFileSizeInMbValidator:
#     def __init__(self, max_size):
#         self.max_size = max_size
#
#     def __call__(self, value):
#         filesize = value.file.size
#         if filesize > self.max_size * 1024 * 1024:
#             raise ValidationError("Max file size is %sMB" % str(self.max_size))

from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880 :
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value
