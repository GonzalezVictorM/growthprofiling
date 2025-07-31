import os
import shutil
from PIL import Image
import pillow_heif
import cv2
import numpy as np
from config import DEFAULT_OUTPUT_EXT, CROP_PERCENTAGE


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)
    

def convert_to_tiff(input_path, output_dir, output_ext = DEFAULT_OUTPUT_EXT):
    """
    Converts an image to TIFF format. Handles HEIC and general formats.
    """
    base_name = os.path.basename(input_path)
    file_name, ext = os.path.splitext(base_name)
    ext = ext.lower()

    ensure_output_dir(output_dir)

    if ext == f".{output_ext}":
        shutil.copy2(input_path, os.path.join(output_dir, base_name))
        print(f"[SKIP] Already {output_ext.upper()}: {base_name}")
        return os.path.join(output_dir, base_name)

    try:
        if ext == '.heic':
            heif_file = pillow_heif.read_heif(input_path)
            img_pil = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
        else:
            img_pil = Image.open(input_path)

        if img_pil.mode not in ("RGB", "L"):
            img_pil = img_pil.convert("RGB")

        output_file = file_name + '.' + output_ext
        output_path = os.path.join(output_dir, output_file)
        img_pil.save(output_path, format=output_ext.upper(), compression='tiff_deflate')

        print(f"[OK] Converted: {base_name} --> {output_file}")
        return output_path

    except Exception as e:
        print(f"[ERROR] Failed to convert {base_name}: {e}")
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
    Converts to grayscale and applies Otsu thresholding.
    Returns preprocessed binary image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def detect_plate_circle(image, config):
    """
    Detects the largest circular contour (e.g., petri dish) using HoughCircles.
    Returns: (x, y, r) or None
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT,
        dp = config['dp'],
        minDist = config['minDist'],
        param1 = config['param1'],
        param2 = config['param2'],
        minRadius = config['minRadius'],
        maxRadius = config['maxRadius']
    )
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        return tuple(int(v) for v in circles[0][0])  # x, y, radius of first detected circle

    return None

def crop_plate(image, circle):
    """
    Crops a circular region from the image.
    Returns cropped square image (bounding box around the circle).
    """
    x, y, r = circle
    x1, y1 = max(x - r, 0), max(y - r, 0)
    x2, y2 = min(x + r, image.shape[1]), min(y + r, image.shape[0])
    return image[y1:y2, x1:x2]

def mask_to_circle(image):
    """
    Masks the input image so only the inscribed circle is visible.
    Corners are set to black.
    """
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    radius = min(center[0], center[1], w - center[0], h - center[1])
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    if image.ndim == 3 and image.shape[2] == 3:
        masked = cv2.bitwise_and(image, image, mask=mask)
    else:
        masked = cv2.bitwise_and(image, image, mask=mask)
    return masked