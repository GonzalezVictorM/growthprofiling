import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image

def get_image_info(filename):
    """
    Extracts strain, substrate, and timepoint from the filename.
    Assumes the filename format is 'strain_substrate_timepoint.tiff'.
    """
    match = re.match(r'(.+?)_(.+?)_(.+?)\.tiff$', filename)
    if match:
        return match.groups()
    return None, None, None

def load_images(cropped_dir):
    """
    Loads images from the cropped directory and organizes them by strain, substrate, and timepoint.
    """
    images = {}
    strains, substrates, timepoints = set(), set(), set()
    for filename in os.listdir(cropped_dir):
        if filename.lower().endswith('.tiff'):
            strain, substrate, timepoint = get_image_info(filename)
            if strain and substrate and timepoint:
                key = (strain, substrate, timepoint)
                images[key] = os.path.join(cropped_dir, filename)
                strains.add(strain)
                substrates.add(substrate)
                timepoints.add(timepoint)
    return images, sorted(strains), sorted(substrates), sorted(timepoints)

def generate_figure(selected_strains, selected_substrates, selected_timepoint, images, output_pdf, axis_choice):
    """
    Generates a grid figure with strains on one axis and substrates on the other.
    """
    n_rows = len(selected_strains) if axis_choice == 'vertical' else len(selected_substrates)
    n_cols = len(selected_substrates) if axis_choice == 'vertical' else len(selected_strains)
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(4*n_cols, 4*n_rows))

    # Ensure axes is always 2D array
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = np.array([axes])
    elif n_cols == 1:
        axes = np.array([[ax] for ax in axes])

    for i, strain in enumerate(selected_strains if axis_choice == 'vertical' else selected_substrates):
        for j, substrate in enumerate(selected_substrates if axis_choice == 'vertical' else selected_strains):
            ax = axes[i, j]
            if axis_choice == 'vertical':
                key = (strain, substrate, selected_timepoint)
            else:
                key = (substrate, strain, selected_timepoint)
            img_path = images.get(key)
            if img_path and os.path.exists(img_path):
                img = Image.open(img_path)
                ax.imshow(img)
            else:
                ax.text(0.5, 0.5, 'No image', ha='center', va='center')
            ax.set_xticks([])
            ax.set_yticks([])

            # Add axis labels
            if j == 0:
                ax.set_ylabel(substrate if axis_choice == 'vertical' else strain, fontsize=12)
            if i == 0:
                ax.set_title(strain if axis_choice == 'vertical' else substrate, fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    with PdfPages(output_pdf) as pdf:
        pdf.savefig(fig)
    plt.close(fig)