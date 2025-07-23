# growthprofiling

This tool processes a batch of growth profiling images (HEIC, JPG, PNG, etc.), converts them to TIFF, relabels them based on a rename matrix, and crops the plate for use in publication figures. In the absence of a rename matrics, it extracts top and bottom labels from the picture using OCR, and renames the images accordingly.

---

## Features

- Supports `.heic`, `.jpg`, `.png`, `.tiff`, `.jpeg`
- Batch convert images to `.tiff` format
- Rename based on a rename matrix
- Crops the petri dish
In case there is no rename matrix:
- Automatically crop label regions (top & bottom)
- Run OCR using Tesseract
- Clean and use text to rename image files
- Crops as before

---

## Configuration

Settings such as paths, supported formats, circle recognition, and OCR behavior can be adjusted in config.py.

---

## Directory architechture

project_root/  
├── main.py  
├── config.py  
├── requirements.txt  
├── utils/  
│   ├── image_utils.py  
│   └── ocr_utils.py  
├── local_data/  
│   ├── rename_matrix.csv   
│   ├── raw_pictures/          # Input images  
│   ├── converted_pictures/    # Intermediate TIFFs  
│   ├── renamed_pictures/      # Renamed output  
│   └── cropped_pictures/      # Cropped output  

---

## Requirements

### Python Packages

Install the required packages with:

```bash
pip install -r requirements.txt
