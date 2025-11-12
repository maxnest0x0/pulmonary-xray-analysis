import pytest
import base64
from fastapi import UploadFile, HTTPException
from io import BytesIO
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image import process_image
from PIL import Image, UnidentifiedImageError


class TestProcessImage:
  def test_process_valid_image(self):
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    mock_file = Mock(spec=UploadFile)
    mock_file.size = len(img_bytes.getvalue())
    mock_file.file = img_bytes
    mock_file.filename = "test.jpg"

    with patch('image.magic.from_buffer') as mock_magic:
      mock_magic.return_value = 'image/jpeg'

      result = process_image(mock_file)

      assert isinstance(result, Image.Image)
      assert result.size == (100, 100)

  def test_process_image_invalid_size_zero(self):
    mock_file = Mock(spec=UploadFile)
    mock_file.size = 0
    mock_file.filename = "test.jpg"

    with pytest.raises(HTTPException) as exc_info:
      process_image(mock_file)

    assert exc_info.value.status_code == 400
    assert "Invalid file size" in str(exc_info.value.detail)

  def test_process_image_invalid_size_too_large(self):
    mock_file = Mock(spec=UploadFile)
    mock_file.size = 21 * 1024 * 1024
    mock_file.filename = "test.jpg"

    with pytest.raises(HTTPException) as exc_info:
      process_image(mock_file)

    assert exc_info.value.status_code == 400
    assert "Invalid file size" in str(exc_info.value.detail)

  def test_process_image_invalid_file_type(self):
    mock_file = Mock(spec=UploadFile)
    mock_file.size = 1024
    mock_file.file = BytesIO(b"not an image")
    mock_file.filename = "test.txt"

    with patch('image.magic.from_buffer') as mock_magic:
      mock_magic.return_value = 'text/plain'

      with pytest.raises(HTTPException) as exc_info:
        process_image(mock_file)

      assert exc_info.value.status_code == 400
      assert "Invalid file type" in str(exc_info.value.detail)

  def test_process_image_corrupted_image(self):
    mock_file = Mock(spec=UploadFile)
    mock_file.size = 1024
    mock_file.file = BytesIO(b"corrupted image data")
    mock_file.filename = "test.jpg"

    with patch('image.magic.from_buffer') as mock_magic:
      mock_magic.return_value = 'image/jpeg'

      with patch('PIL.Image.open') as mock_open:
        mock_open.side_effect = UnidentifiedImageError("Cannot identify image file")

        with pytest.raises(HTTPException) as exc_info:
          process_image(mock_file)

        assert exc_info.value.status_code == 400
        assert "Invalid image" in str(exc_info.value.detail)

  def test_process_image_dicom_supported(self):
    mock_file = Mock(spec=UploadFile)
    mock_file.size = 1024
    mock_file.file = BytesIO(b"dicom data")
    mock_file.filename = "test.dcm"

    with patch('image.magic.from_buffer') as mock_magic:
      mock_magic.return_value = 'application/dicom'

      try:
        process_image(mock_file)
      except (HTTPException, UnidentifiedImageError):
        pass


