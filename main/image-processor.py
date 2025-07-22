import os
import shutil
import pandas as pd
import cv2
from PIL import Image
import pillow_heif
import numpy

# ------ Configuration  ------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

SUPPORTED_IMAGE_FORMATS = ('.png','.jpg','jpeg','TIFF','.heic')
DEFAULT_OUTPUT_EXT = 'TIFF'

# ------ Functions      ------
def main():
    # -- Paths          ---
    base_dir = os.path.join('..')
    input_dir = os.path.join(base_dir, 'raw_pictures')
    renamed_dir = os.path.join(base_dir, 'renamed_pictures')

    input_picture = os.path.join(input_dir, '')

if __name__ == "__main__":
    main()