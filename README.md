# growthprofiling

This tool processes a batch of images (HEIC, JPG, PNG, etc.), converts them to TIFF, extracts top and bottom labels using OCR, and renames the images accordingly.

---

## Features

- Batch convert images to `.tiff` format
- Automatically crop label regions (top & bottom)
- Run OCR using Tesseract
- Clean and use text to rename image files
- Supports `.heic`, `.jpg`, `.png`, `.tiff`, `.jpeg`

---

## Configuration

Settings such as paths, supported formats, and OCR behavior can be adjusted in config.py.

---

## Directory architechture

project_root/
├── main.py
├── config.py
├── requirements.txt
├── utils/
│   ├── image_utils.py
│   └── ocr_utils.py
├── raw_pictures/          # Input images
├── converted_pictures/    # Intermediate TIFFs
└── renamed_pictures/      # Final renamed output

---

## Requirements

### Python Packages

Install the required packages with:

```bash
pip install -r requirements.txt
