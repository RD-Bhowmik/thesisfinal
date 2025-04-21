import pandas as pd

# Step 1: Convert Cases - Images.xlsx to CSV
print("Converting 'Cases - Images.xlsx' to CSV...")
cases_images_df = pd.read_excel("Cases - Images.xlsx")
cases_images_csv_path = "cases_images.csv"
cases_images_df.to_csv(cases_images_csv_path, index=False)
print(f"Saved to {cases_images_csv_path}")

# Show sample of the source file
print("\nSample of Cases - Images.xlsx:")
print(cases_images_df.head())

# Step 2: Load the all_images_mapping.csv
print("\nLoading all_images_mapping.csv...")
all_images_df = pd.read_csv("all_images_mapping.csv")
print(f"Loaded {len(all_images_df)} image records")

# Show sample of the mapping file
print("\nSample of all_images_mapping.csv before adding types:")
print(all_images_df.head())

# Step 3: Create a lookup dictionary for the image types
# Key: (Case Number, Filename) -> Value: Type
type_lookup = {}
for _, row in cases_images_df.iterrows():
    type_lookup[(row['Case Number'], row['File'])] = row['Type']

print(f"\nCreated lookup dictionary with {len(type_lookup)} entries")

# Step 4: Add Type column to all_images_mapping.csv
all_images_df['Image Type'] = all_images_df.apply(
    lambda row: type_lookup.get((row['Case Number'], row['Original Filename']), "Unknown"),
    axis=1
)

# Count images with unknown type
unknown_types = all_images_df[all_images_df['Image Type'] == 'Unknown']
if len(unknown_types) > 0:
    print(f"\nWARNING: {len(unknown_types)} images could not be matched with a type")
    print("Sample of unmatched images:")
    print(unknown_types.head())
else:
    print("\nAll images successfully matched with a type")

# Step 5: Save the updated mapping
updated_csv_path = "all_images_mapping_with_types.csv"
all_images_df.to_csv(updated_csv_path, index=False)

print(f"\nSaved updated mapping to {updated_csv_path}")
print("\nSample of updated mapping:")
print(all_images_df.head())

# Step 6: Generate a summary of image types
print("\nSummary of image types:")
type_summary = all_images_df['Image Type'].value_counts()
print(type_summary)

# Also save type summary to CSV
type_summary.to_csv("image_type_summary.csv", header=['Count']) 