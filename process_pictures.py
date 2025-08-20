import os
import cv2
import pandas as pd
from config import SUPPORTED_FORMATS, DEFAULT_OUTPUT_EXT, DATA_DIR, RAW_DIR, CONVERTED_DIR, RENAMED_DIR, CROPPED_DIR, CIRCLE_DETECTION_CONFIG, THREADS
from utils.image_utils import convert_to_tiff, preprocess_for_ocr, crop_top_bottom, ensure_output_dir, detect_plate_circle, crop_plate, mask_to_circle
from utils.ocr_utils import run_ocr, create_filename
from concurrent.futures import ThreadPoolExecutor

def process_image(image_path, rename_map = None):
    original_name = os.path.basename(image_path)
    file_stem, _ = os.path.splitext(original_name)
    print(f"Processing: {original_name}")

    # Step 1: Convert to TIFF
    output_file = file_stem + '.' + DEFAULT_OUTPUT_EXT
    output_path = os.path.join(CONVERTED_DIR, output_file)

    if not os.path.exists(output_path):
        converted_path = convert_to_tiff(image_path, CONVERTED_DIR)
        if not converted_path:
            print(f"[ERROR] Conversion failed. Skipping.")
            return
    else:
        print(f"[SKIP] Already exists: {output_path}")

    # Step 2: Try to rename from CSV
    new_filename = None
    if rename_map:
        match = rename_map.get(file_stem.lower())
        if match:
            new_filename = f"{match}.tiff"
            print(f"[INFO] Using CSV rename: {new_filename}")

    # Step 3: OCR fallback
    if not new_filename:
        print("[INFO] No rename match. Falling back to OCR...")
        image = cv2.imread(converted_path)
        if image is None:
            print(f"[ERROR] Failed to load converted image. Skipping.")
            return
    
        thresh = preprocess_for_ocr(image)
        top_crop, bottom_crop = crop_top_bottom(thresh)
        top_text = run_ocr(top_crop)
        bottom_text = run_ocr(bottom_crop)
        new_filename = create_filename(top_text, bottom_text)
        print(f"[INFO] Using OCR rename: {new_filename}")
    
    # Step 4: Rename the file
    new_path = os.path.join(RENAMED_DIR, new_filename)
    ensure_output_dir(RENAMED_DIR)

    if not os.path.exists(new_path):
        try:
            os.rename(converted_path, new_path)
            print(f"[OK] Renamed to: {new_filename}")
        except Exception as e:
            print(f"[ERROR] Could not rename file: {e}")
            return
    else:
        print(f"[SKIP] Already exists: {new_path}")

    # Step 4: Circle Detection, Crop and Mask
    cropped_path = os.path.join(CROPPED_DIR, new_filename)

    if not os.path.exists(cropped_path):
        print("[INFO] Starting circle detection...")
        image = cv2.imread(new_path)
        if image is None:
            print("[ERROR] Could not load image for cropping.")
            return

        circle = detect_plate_circle(image, CIRCLE_DETECTION_CONFIG)
        if circle is None:
            print("[WARN] No circular plate detected.")
            return

        cropped = crop_plate(image, circle)
        masked = mask_to_circle(cropped)
        ensure_output_dir(CROPPED_DIR)
        cv2.imwrite(cropped_path, masked)
        print(f"[OK] Cropped circular region saved: {os.path.basename(cropped_path)}")
    else:
        print(f"[SKIP] Already exists: {cropped_path}")


def batch_process(rename_csv = None, max_workers = THREADS):
    print("Starting batch processing...")

    if not os.path.exists(RAW_DIR):
        print(f"[ERROR] Input folder '{RAW_DIR}' does not exist.")
        return
    
    # Load rename map if CSV provided
    rename_map = {}
    if rename_csv:
        rename_csv_path = os.path.join(DATA_DIR, rename_csv)
        if os.path.isfile(rename_csv_path):
            df = pd.read_csv(rename_csv_path)
            if {'old_name', 'new_name'}.issubset(df.columns):
                rename_map = {
                    str(row['old_name']).lower(): str(row['new_name'])
                    for _, row in df.iterrows()
                }
                print(f"[OK] Loaded rename matrix with {len(rename_map)} entries.")
            else:
                print(f"[WARN] CSV missing required columns. Will fallback to OCR.")
        else:
            print(f"[WARN] Rename CSV not found. Will fallback to OCR.")
    else:
        print("[INFO] No rename CSV provided. Using OCR for all files.")

    # Gather all valid image files
    file_paths = [
        os.path.join(RAW_DIR, fname)
        for fname in os.listdir(RAW_DIR)
        if os.path.isfile(os.path.join(RAW_DIR, fname)) and fname.lower().endswith(SUPPORTED_FORMATS)
    ]
    print(f"[INFO] Found {len(file_paths)} supported image files.")

    # Process images in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, fp, rename_map) for fp in file_paths]
        for i, future in enumerate(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] Exception in file {file_paths[i]}: {e}")

    print("[DONE] Batch processing complete.")


if __name__ == "__main__":
    batch_process(rename_csv = "rename_matrix.csv")
