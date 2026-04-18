import os
from photo_metadata_server import save_photo_metadata

source_dir = os.path.expanduser("~/pictures/post")
output_dir = os.path.expanduser("~/claude")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files = os.listdir(source_dir)
valid_extensions = ('.jpg', '.jpeg', '.png', '.arw', '.dng')

success_count = 0
error_count = 0

for filename in files:
    if filename.lower().endswith(valid_extensions):
        input_path = os.path.join(source_dir, filename)
        output_filename = f"{filename}.json"
        output_path = os.path.join(output_dir, output_filename)

        print(f"Processing {filename}...")
        result = save_photo_metadata(input_path, output_path)

        if "successfully saved" in result:
            success_count += 1
        else:
            print(f"Error saving {filename}: {result}")
            error_count += 1

print(f"\nProcessing complete.")
print(f"Successfully saved: {success_count}")
print(f"Errors: {error_count}")
