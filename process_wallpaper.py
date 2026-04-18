import os
from photo_metadata_server import save_photo_metadata, create_photo_markdown

source_dir = os.path.expanduser("~/pictures/wallpaper")

files = os.listdir(source_dir)
valid_extensions = ('.jpg', '.jpeg', '.png', '.arw', '.dng')

success_count = 0
error_count = 0

for filename in files:
    if filename.lower().endswith(valid_extensions):
        input_path = os.path.join(source_dir, filename)

        # 1. Save metadata to JSON
        # Using the server's feature where passing a directory as output_path
        # generates <filename_no_ext>.json
        result_save = save_photo_metadata(input_path, source_dir)

        if "successfully saved" in result_save:
            # The server generates the json path as:
            base_name = os.path.splitext(filename)[0]
            json_path = os.path.join(source_dir, f"{base_name}.json")

            # 2. Create markdown file from that JSON
            result_md = create_photo_markdown(json_path, input_path)

            if "successfully created" in result_md:
                success_count += 1
            else:
                print(f"Error creating markdown for {filename}: {result_md}")
                error_count += 1
        else:
            print(f"Error saving metadata for {filename}: {result_save}")
            error_count += 1

print(f"\nProcessing complete.")
print(f"Successfully processed: {success_count}")
print(f"Errors: {error_count}")
