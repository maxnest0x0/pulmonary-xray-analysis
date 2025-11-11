import magic
from fastapi import UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError

MAX_SIZE = 20 * 1024 * 1024
MIME_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/bmp',
    'image/tiff',
    'application/dicom', # todo
]

def process_image(file: UploadFile) -> Image.Image:
    if file.size is None or file.size == 0 or file.size > MAX_SIZE:
        raise HTTPException(400, 'Invalid file size')

    content = file.file.read()
    try:
        mime = magic.from_buffer(content, mime=True)
    except magic.MagicException:
        mime = None
    if mime not in MIME_TYPES:
        raise HTTPException(400, 'Invalid file type')

    try:
        im = Image.open(file.file)
    except UnidentifiedImageError:
        raise HTTPException(400, 'Invalid image')
    return im
