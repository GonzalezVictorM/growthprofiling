import os
import numpy as np
from PIL import Image
import pillow_heif
import cv2
from config import DEFAULT_OUTPUT_EXT, CROP_PERCENTAGE

def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)

def convert_to_tiff(input_path, output_dir, output_ext=DEFAULT_OUTPUT_EXT):
    """
    Converts an image to TIFF format. Handles HEIC and general formats.
    """
    base_name = os.path.basename(input_path)
    file_name, ext = os.path.splitext(base_name)
    ext = ext.lower()
    ensure_output_dir(output_dir)
    output_path = os.path.join(output_dir, f"{file_name}.{output_ext}")

    if ext == f".{output_ext}":
        # Already in desired format, just copy
        if not os.path.exists(output_path):
            Image.open(input_path).save(output_path)
        return output_path

    try:
        if ext == '.heic':
            heif_file = pillow_heif.read_heif(input_path)
            img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
        else:
            img = Image.open(input_path)
        
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"[ERROR] Could not convert {input_path}: {e}")
        return None

def crop_top_bottom(image, crop_pct=CROP_PERCENTAGE):
    """
    Crops the top and bottom X% of the image height.
    Returns: (top_crop, bottom_crop)
    """
    height, width = image.shape[:2]
    delta = int(height * crop_pct)
    top_crop = image[0:delta, :]
    bottom_crop = image[-delta:, :]
    return top_crop, bottom_crop

def preprocess_for_ocr(image):
    """
    Preprocesses an image for OCR: grayscale and Otsu thresholding.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def detect_plate_circle(image, config):
    """
    Detects a circle in the image using HoughCircles.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT,
        dp=config['dp'],
        minDist=config['minDist'],
        param1=config['param1'],
        param2=config['param2'],
        minRadius=config['minRadius'],
        maxRadius=config['maxRadius']
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        return tuple(int(v) for v in circles[0][0])  # x, y, radius
    return None

def detect_plate_circle_fast(tiff_path, config, jpeg_resize_factor=0.25):
    """
    Detects the plate circle on a JPEG version of the TIFF for speed.
    Returns (x, y, r) in TIFF coordinates.
    """
    img_pil = Image.open(tiff_path)
    orig_size = img_pil.size  # (width, height)
    new_size = (int(orig_size[0] * jpeg_resize_factor), int(orig_size[1] * jpeg_resize_factor))
    img_pil_small = img_pil.resize(new_size, Image.LANCZOS)
    img_jpeg = np.array(img_pil_small.convert('RGB'))
    img_jpeg = cv2.cvtColor(img_jpeg, cv2.COLOR_RGB2BGR)
    circle = detect_plate_circle(img_jpeg, config)
    if circle is not None:
        x, y, r = circle
        scale = 1.0 / jpeg_resize_factor
        x, y, r = int(x * scale), int(y * scale), int(r * scale)
        return (x, y, r)
    return None

def crop_plate(image, circle):
    """
    Crops the image to the bounding box of the detected circle.
    """
    x, y, r = circle
    x1, y1 = max(0, x - r), max(0, y - r)
    x2, y2 = min(image.shape[1], x + r), min(image.shape[0], y + r)
    return image[y1:y2, x1:x2]

def mask_to_circle(image):
    """
    Masks the image to a circle (sets outside to black).
    """
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w // 2, h // 2), min(h, w) // 2, 255, -1)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result