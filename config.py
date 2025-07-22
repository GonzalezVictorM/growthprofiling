import os

# ---- Tesseract Configuration ----
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_LANG = 'eng'
TESSERACT_PSM = 6  # Assume a block of text

# ---- Supported Formats ----
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.tiff', '.heic')

# ---- OCR Settings ----
CROP_PERCENTAGE = 0.12  # Top/bottom crop % for label detection

# ---- Paths ----
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DIR = os.path.join(BASE_DIR, 'raw_pictures')
CONVERTED_DIR = os.path.join(BASE_DIR, 'converted_pictures')
RENAMED_DIR = os.path.join(BASE_DIR, 'renamed_pictures')
