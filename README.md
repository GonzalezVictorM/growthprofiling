# growthprofiling

This tool processes a batch of growth profiling images, converting them to TIFF, relabeling them, and cropping the plate for publication. It supports various image formats including `.heic`, `.jpg`, `.png`, `.tiff`, and `.jpeg`.

When a `rename_matrix.csv` is provided, images are renamed based on the specified labels. If no rename matrix exists, the tool uses Tesseract OCR to automatically extract and clean text from the top and bottom labels of the pictures to rename the files.

***

## Features

* **Batch conversion**: Converts various image formats to `.tiff`.
* **Renaming**: Renames images using a provided `rename_matrix.csv` or through OCR.
* **Automated cropping**: Crops the petri dish from the image for figure preparation.
* **Multithreaded processing**: Automatically uses all available CPU cores for fast batch processing. You can override the number of threads in `config.py`.
* **Publishable figure creation**: Easily generate grid figures from cropped images, with customizable axis labels and layout, ready for publication.

***

## Usage

1.  **Clone the [repository](https://github.com/GonzalezVictorM/growthprofiling.git)**:

    ```bash
    git clone https://github.com/GonzalezVictorM/growthprofiling.git
    cd growthprofiling
    ```
2.  **(Optional/recommended) Build a conda environment**:

    ```bash
    conda create --name growthprofiling python=3.13.5
    ```

    You can activate and deactivate the environment using the following code.

    ```bash
    conda activate growthprofiling
    conda deactivate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Place your images**:

    Put your raw images inside the `local_data/raw_pictures/` directory.

5. **(Optional) Provide a Rename Matrix**: 

    If you want to rename your images using a predefined list, create or edit the `local_data/rename_matrix.csv` file. The file needs to include a column `old_name` with the file names without the extension (e.g. `IMG_4469.HEIC` → `IMG_4469`) and a column `new_name` (e.g. `strainA_substrateB_ndays`) The tool will use this file to rename images, ignoring the OCR step.

6.  **Run the picture processing tool**:

    ```bash
    python process_pictures.py
    ```

The script will process the images and save the output in the following directories:

* `local_data/converted_pictures/`: Intermediate .tiff files.
* `local_data/renamed_pictures/`: The images after being renamed.
* `local_data/cropped_pictures/`: The final, cropped images ready for publication.

The script will skip parts of the process for which the output is ready, making it possible to run the command without re-doing all the work.

6.  **Run the figure making tool**:

    ```bash
    python generate_figure.py
    ```

You will be prompted to select:
* Axis orientation (strains on vertical or horizontal axis)
* Which strains, substrates, and timepoints to include

The script will create a grid PDF with your selections, with no space between images and clear axis labels.

***

## Prerequisites

### 1. Conda installation

Install **Anaconda** from your institution's **Software Center** or by downloading the installer from the [Anaconda downloadpage](https://www.anaconda.com/download).

### 2. Tesseract OCR

If you do not plan to use a `rename_matrix.csv`and instead want the tool to automatically rename files, you must install Tesseract OCR.

**Download**: Tesseract installers and instructions for various operating systems are available on the [Tesseract-OCR Downloads page](https://tesseract-ocr.github.io/tessdoc/Downloads.html).

**Windows**: UB Mannheim provides reliable Windows installers.

## Configuration

You can adjust various settings by editing `config.py`. These settings include file paths, supported formats, and OCR behavior. For example, you can change the input and output directories or fine-tune the circle recognition parameters.

**Important**: When using the OCR features, remember to update the path to the Tesseract-OCR executable in `config.py`.

## Directory architechture

```
project_root/  
├── main.py                     # The main script to run
├── config.py                   # Configuration settings for the tool
├── requirements.txt            # List of Python dependencies
├── utils/                      # Helper scripts
│   ├── image_utils.py          # Functions for image processing
│   └── ocr_utils.py            # Functions for OCR operations
├── local_data/                 # All data and output files are stored here
│   ├── rename_matrix.csv       # (Optional) CSV file for renaming images
│   ├── raw_pictures/           # Place your input images here
│   ├── converted_pictures/     # Intermediate TIFF files are saved here
│   ├── renamed_pictures/       # Renamed TIFF files are saved here
│   └── cropped_pictures/       # Final, cropped images are saved here
```