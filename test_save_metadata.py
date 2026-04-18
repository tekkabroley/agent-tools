from photo_metadata_server import save_photo_metadata
import os
import json

image_path = os.path.expanduser("~/github/agent-tools/test-photos/DSC00037.jpg")
output_path = os.path.expanduser("~/github/agent-tools/test-photos/test_save_output.json")

print(f"Testing metadata saving from: {image_path}")
print(f"Saving to: {output_path}")
result = save_photo_metadata(image_path, output_path)
print(result)

if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        data = json.load(f)
        print(f"Successfully verified JSON output. Found {len(data)} tags.")
        print(f"Example tag: {list(data.keys())[0]}: {data[list(data.keys())[0]]}")
else:
    print("Error: Output file was not created.")
