import os
import shutil
import pandas as pd
from pathlib import Path

# Path to the main folder containing all case folders
source_path = Path("IARCImageBankColpo")

# Create a destination folder for all images
dest_folder = Path("all_colposcopy_images")
dest_folder.mkdir(exist_ok=True)

# Lists to store data for the CSV
original_paths = []
case_numbers = []
image_filenames = []
new_paths = []

# Count images
total_images = 0
total_copied = 0

print(f"Creating folder: {dest_folder}")

# Go through each case folder (both Case and case formats)
for case_folder in sorted(list(source_path.glob("Case *")) + list(source_path.glob("case *"))):
    case_number = case_folder.name
    
    # Extract the numeric part of the case number
    case_num = int(case_number.split()[1].lstrip('0'))
    
    # Find all jpg files in this case folder
    image_count = 0
    for img_file in case_folder.glob("*.jpg"):
        # Original path information
        original_path = str(img_file.relative_to(source_path))
        original_paths.append(original_path)
        case_numbers.append(case_num)
        image_filenames.append(img_file.name)
        
        # Copy the file to the destination folder
        dest_file = dest_folder / img_file.name
        
        # If file with same name exists, add case number as prefix to avoid overwriting
        if dest_file.exists():
            new_filename = f"{case_num:03d}_{img_file.name}"
            dest_file = dest_folder / new_filename
        else:
            new_filename = img_file.name
            
        # Store the new path
        new_paths.append(str(dest_file.name))
        
        # Copy the file
        try:
            shutil.copy2(img_file, dest_file)
            total_copied += 1
        except Exception as e:
            print(f"Error copying {img_file}: {e}")
        
        image_count += 1
        total_images += 1
    
    print(f"Processed {case_folder.name}: Copied {image_count} images")

# Create a DataFrame
df = pd.DataFrame({
    'Case Number': case_numbers,
    'Original Filename': image_filenames,
    'Original Path': original_paths,
    'New Filename': new_paths
})

# Save to CSV
csv_path = "all_images_mapping.csv"
df.to_csv(csv_path, index=False)

# Summary
print(f"\nTotal images found: {total_images}")
print(f"Total images copied: {total_copied}")
print(f"Total cases processed: {len(set(case_numbers))}")
print(f"Data saved to {csv_path}")
print(f"All images copied to folder: {dest_folder}")

# Generate a summary by case
case_summary = df.groupby('Case Number').size().reset_index(name='Image Count')
case_summary.to_csv("case_copy_summary.csv", index=False) 