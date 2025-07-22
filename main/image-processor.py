import os
import shutil
import pandas as pd
import cv2
from PIL import Image
import pillow_heif
import numpy
import pytesseract

# ------ Configuration  ------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

SUPPORTED_IMAGE_FORMATS = ('.png','.jpg','.jpeg','.tiff','.heic')
DEFAULT_OUTPUT_EXT = 'tiff'

# ------ Functions      ------
def convert_image(input_path, output_dir):
    """
    Converts the image to the DEFAULT_OUTPUT_EXT.
    """
    base_name = os.path.basename(input_path)
    file_name, ext = os.path.splitext(base_name)
    ext = ext.lower()

    try:
        os.makedirs(output_dir, exist_ok = True)

        if ext == f".{DEFAULT_OUTPUT_EXT}":
            shutil.copy2(input_path, os.path.join(output_dir, base_name))
            print(f"[SKIP] Already {DEFAULT_OUTPUT_EXT.upper()}: {base_name}")  
        else:
            if ext == '.heic':
                heif_file = pillow_heif.read_heif(input_path)
                img_pil = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            else:
                img_pil = Image.open(input_path)
            
            # Convert to RGB for broader compatibility
            if img_pil.mode not in ("RGB", "L"):
                img_pil = img_pil.convert("RGB")

            output_file = file_name + '.' + DEFAULT_OUTPUT_EXT
            output_path = os.path.join(output_dir, output_file)
            
            img_pil.save(output_path, format = DEFAULT_OUTPUT_EXT.upper(), compression = 'tiff_deflate')

        print(f"[OK] Converted: {base_name} ---> {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to convert {base_name}: {e}")


def batch_convert(input_dir, output_dir):
    """
    Iterates through all pictures in a folder and uses the convert_image function.
    """
    if not os.path.isdir(input_dir):
        print(f"[ERROR] Folder '{input_dir}' does not exist or is not a directory.")
        return
    
    print(f"Processing files in: {input_dir}")
    os.makedirs(output_dir, exist_ok = True)

    for item_name in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item_name)

        if not os.path.isfile(item_path):
            print(f"[WARN] Skipping non-file: {item_name}")
            continue
        if not item_name.lower().endswith(SUPPORTED_IMAGE_FORMATS):
            print(f"[WARN] Unsupported format: {item_name}")
            continue

        convert_image(item_path, output_dir)

def main():
    # -- Paths          ---
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'raw_pictures')
    converted_dir = os.path.join(base_dir, 'converted_pictures')
    # renamed_dir = os.path.join(base_dir, 'renamed_pictures')
     
    print("Converting files...")
    batch_convert(raw_dir, converted_dir)    

    
    # Load image and preprocess
    temp_image = os.path.join(converted_dir, "IMG_4480.tiff")
    image = cv2.imread(temp_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Keep text black on white

    height, width = thresh.shape

    # Define top and bottom slice (adjust % as needed)
    crop_pct = 0.12  # 12% top and bottom
    top_crop = thresh[0:int(height * crop_pct), :]
    bottom_crop = thresh[int(height * (1 - crop_pct)):, :]

    # OCR each part
    config = '--psm 6'  # Assume a single uniform block of text
    top_text = pytesseract.image_to_string(top_crop, lang='eng', config=config)
    bottom_text = pytesseract.image_to_string(bottom_crop, lang='eng', config=config)

    # Show for debug
    cv2.imshow('Top Crop', top_crop)
    cv2.imshow('Bottom Crop', bottom_crop)
    cv2.waitKey()

    # Print OCR results
    print("Top Text OCR:", top_text.strip())
    print("Bottom Text OCR:", bottom_text.strip())

if __name__ == "__main__":
    main()