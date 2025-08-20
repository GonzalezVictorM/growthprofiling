import os
from config import BASE_DIR, CROPPED_DIR
from utils.figure_utils import load_images, generate_figure 

def main():
    output_pdf = os.path.join(BASE_DIR, 'growth_profile_figure.pdf')
    images, strains, substrates, timepoints = load_images(CROPPED_DIR)
    if not images:
        print("No images found in the cropped directory.")
        return

    print("Axis orientation (strains on vertical or horizontal)?")
    axis_choice = input("Type 'vertical' or 'horizontal': ").strip().lower()
    if axis_choice not in ['vertical', 'horizontal']:
        print("Invalid axis choice.")
        return

    print("\nAvailable strains:")
    for i, s in enumerate(strains):
        print(f"{i+1}: {s}")
    strain_idxs = input("Select strains by number (space separated): ").strip().split()
    selected_strains = [strains[int(idx)-1] for idx in strain_idxs if idx.isdigit() and 1 <= int(idx) <= len(strains)]

    print("\nAvailable substrates:")
    for i, s in enumerate(substrates):
        print(f"{i+1}: {s}")
    substrate_idxs = input("Select substrates by number (space separated): ").strip().split()
    selected_substrates = [substrates[int(idx)-1] for idx in substrate_idxs if idx.isdigit() and 1 <= int(idx) <= len(substrates)]

    print("\nAvailable timepoints:")
    for i, t in enumerate(timepoints):
        print(f"{i+1}: {t}")
    timepoint_idxs = input("Select a single timepoint): ").strip().split()
    selected_timepoints = [timepoints[int(idx)-1] for idx in timepoint_idxs if idx.isdigit() and 1 <= int(idx) <= len(timepoints)]

    if selected_strains and selected_substrates and selected_timepoints:
        # Only use the first selected timepoint for the grid
        generate_figure(selected_strains, selected_substrates, selected_timepoints[0], images, output_pdf, axis_choice)
        print(f"Figure saved as {output_pdf}")
    else:
        print("No images found for the selected criteria.")

if __name__ == "__main__":
    main()