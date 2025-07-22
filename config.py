import os

# ---- Tesseract Configuration ----
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_LANG = 'eng'
TESSERACT_PSM = 6  # Assume a block of text

# ---- Supported Formats ----
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.tiff', '.heic')
DEFAULT_OUTPUT_EXT = 'tiff'

# ---- OCR Settings ----
CROP_PERCENTAGE = 0.12  # Top/bottom crop % for label detection

# ---- Circle detection settings ----
CIRCLE_DETECTION_CONFIG = {
    'dp': 1,
    'minDist': 200,
    'param1': 100,
    'param2': 30,
    'minRadius': 1000,
    'maxRadius': 0
}

# ---- Paths ----
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, 'raw_pictures')
CONVERTED_DIR = os.path.join(BASE_DIR, 'converted_pictures')
RENAMED_DIR = os.path.join(BASE_DIR, 'renamed_pictures')
CROPPED_DIR = os.path.join(BASE_DIR, 'cropped_pictures')

