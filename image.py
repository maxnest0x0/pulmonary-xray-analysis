import base64
from typing import cast
from io import BytesIO

import magic
import numpy as np
from fastapi import UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError

type GrayscaleImage[W: int, H: int] = np.ndarray[tuple[H, W], np.dtype[np.uint8]]

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

def prepare_image(im: Image.Image) -> GrayscaleImage[int, int]:
    output = np.array(im.convert('L'))
    return cast(GrayscaleImage[int, int], output)

def encode_image(im: Image.Image) -> str:
    buf = BytesIO()
    im.save(buf, 'png')
    return base64.b64encode(buf.getvalue()).decode()
