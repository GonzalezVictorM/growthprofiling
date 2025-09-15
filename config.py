import os
import csv

# ---- System settings ----
THREADS = os.cpu_count() or 1  # Use all available cores, default to 1 if not available

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
    'dp': 1.5,
    'minDist': 125, # old 500
    'param1': 100,
    'param2': 40,
    'minRadius': 275, # old 1100
    'maxRadius': 375 # old 1500
}

# ---- Paths ----
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'local_data')
RAW_DIR = os.path.join(DATA_DIR, 'raw_pictures')
CONVERTED_DIR = os.path.join(DATA_DIR, 'converted_pictures')
RENAMED_DIR = os.path.join(DATA_DIR, 'renamed_pictures')
CROPPED_DIR = os.path.join(DATA_DIR, 'cropped_pictures')


# ---- Logs ----
def log_action(log_file, filename, stage, status, message=''):
    with open(log_file, 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([filename, stage, status, message])
