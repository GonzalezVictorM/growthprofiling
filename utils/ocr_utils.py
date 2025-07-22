import pytesseract
import re
from config import TESSERACT_PATH, TESSERACT_LANG, TESSERACT_PSM

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def run_ocr(image, psm=TESSERACT_PSM):
    """
    Runs Tesseract OCR on a preprocessed image.
    Returns raw extracted text.
    """
    config = f'--psm {psm}'
    text = pytesseract.image_to_string(image, lang=TESSERACT_LANG, config=config)
    return text.strip()


def clean_text(text):
    """
    Cleans raw OCR output: removes non-alphanumeric noise,
    replaces multiple spaces, trims.
    """
    text = re.sub(r'[^a-zA-Z0-9\s\-_.]', '', text)      # Remove non-alphanumeric except some safe chars
    text = re.sub(r'\s+', ' ', text)                    # Collapse multiple spaces
    return text.strip().replace(' ', '_')               # Underscore for filenames


def create_filename(top_text, bottom_text, extension='tiff'):
    """
    Creates a standardized filename from top/bottom OCR text.
    """
    top_clean = clean_text(top_text)
    bottom_clean = clean_text(bottom_text)
    return f"{top_clean}_{bottom_clean}.{extension}"
