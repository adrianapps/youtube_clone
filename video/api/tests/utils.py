from io import BytesIO

import PIL.Image
from django.core.files.uploadedfile import SimpleUploadedFile


def create_image_file(name, size=(100, 100), content_type='image/jpeg'):
    img = PIL.Image.new('RGB', size, color='red')
    byte_io = BytesIO()
    img.save(byte_io, format='JPEG')
    byte_io.seek(0)
    return SimpleUploadedFile(name, byte_io.read(), content_type=content_type)
