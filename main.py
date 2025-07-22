import os
import cv2
from config import RAW_DIR, CONVERTED_DIR, RENAMED_DIR
from utils.image_utils import convert_to_tiff, preprocess_for_ocr, crop_top_bottom, ensure_output_dir
from utils.ocr_utils import run_ocr, create_filename

def process_image(image_path):
    print(f"Processing: {os.path.basename(image_path)}")

    # Step 1: Convert to TIFF
    converted_path = convert_to_tiff(image_path, CONVERTED_DIR)
    if not converted_path:
        print(f"[ERROR] Conversion failed. Skipping.")
        return

    # Step 2: Load with OpenCV
    image = cv2.imread(converted_path)
    if image is None:
        print(f"[ERROR] Failed to load converted image. Skipping.")
        return

    # Step 3: Preprocess for OCR
    thresh = preprocess_for_ocr(image)

    # Step 4: Crop label regions
    top_crop, bottom_crop = crop_top_bottom(thresh)

    # Step 5: Run OCR
    top_text = run_ocr(top_crop)
    bottom_text = run_ocr(bottom_crop)

    print(f"Top text: {top_text}")
    print(f"Bottom text: {bottom_text}")

    # # Step 6: Create new filename
    # new_filename = create_filename(top_text, bottom_text)
    # new_path = os.path.join(RENAMED_DIR, new_filename)

    # # Step 7: Save renamed image
    # ensure_output_dir(RENAMED_DIR)
    # try:
    #     os.rename(converted_path, new_path)
    #     print(f"[OK] Renamed to: {new_filename}")
    # except Exception as e:
    #     print(f"[ERROR] Could not rename file: {e}")


def batch_process():
    print("Starting batch processing...")
    if not os.path.exists(RAW_DIR):
        print(f"[ERROR] Input folder '{RAW_DIR}' does not exist.")
        return

    for file_name in os.listdir(RAW_DIR):
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.heic')):
            continue
        file_path = os.path.join(RAW_DIR, file_name)
        if os.path.isfile(file_path):
            process_image(file_path)


if __name__ == "__main__":
    batch_process()
