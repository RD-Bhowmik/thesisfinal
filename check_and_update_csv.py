import os
import csv
import random

def main():
    # Path to the images folder and CSV file
    images_folder = 'all_colposcopy_images'
    csv_file = 'all_images_mapping_with_types.csv'
    output_csv = 'updated_images_mapping.csv'
    
    # Get all image names from the folder
    image_files = set()
    for filename in os.listdir(images_folder):
        if filename.lower().endswith('.jpg'):
            image_files.add(filename)
    
    print(f"Found {len(image_files)} images in the folder")
    
    # Read the CSV file
    csv_rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Save the header
        for row in reader:
            csv_rows.append(row)
    
    # Check which images in CSV don't exist in the folder
    missing_images = []
    for row in csv_rows:
        if len(row) >= 4:  # Ensure the row has enough columns
            image_name = row[3]  # New filename column
            if image_name not in image_files:
                missing_images.append(image_name)
    
    print(f"Found {len(missing_images)} images in CSV that don't exist in the folder")
    
    # If we have more than 3 missing images, randomly select 3
    if len(missing_images) > 3:
        to_remove = random.sample(missing_images, 3)
    else:
        to_remove = missing_images
    
    print(f"Will remove these {len(to_remove)} images from CSV: {to_remove}")
    
    # Create a new CSV without the 3 missing images
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # Write the header
        
        for row in csv_rows:
            if len(row) >= 4 and row[3] not in to_remove:
                writer.writerow(row)
    
    print(f"Created updated CSV: {output_csv}")
    print(f"Removed {len(to_remove)} images from the CSV")

if __name__ == "__main__":
    main() 