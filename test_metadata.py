from photo_metadata_server import get_photo_metadata
import os

file_path = os.path.expanduser("~/github/agent-tools/test-photos/DSC00037.jpg")
output_path = os.path.expanduser("~/github/agent-tools/test-photos/test_extraction_output.json")

print(f"Testing metadata extraction for: {file_path}")
metadata = get_photo_metadata(file_path)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(metadata)

print(f"Output written to: {output_path}")
print(metadata)
