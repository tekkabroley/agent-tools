from photo_metadata_server import create_photo_markdown
import os

image_path = os.path.expanduser("~/github/agent-tools/test-photos/DSC00037.jpg")
json_path = os.path.expanduser("~/github/agent-tools/test-photos/test_save_output.json")

print(f"Testing markdown creation from: {json_path}")
print(f"Using image path: {image_path}")
result = create_photo_markdown(json_path, image_path)
print(result)

# The tool saves it as <JSON_NAME>.md
md_path = os.path.splitext(json_path)[0] + ".md"

if os.path.exists(md_path):
    with open(md_path, 'r') as f:
        content = f.read()
        print("\n--- Generated Markdown Content ---")
        print(content)
        print("----------------------------------")
else:
    print(f"Error: Markdown file {md_path} was not created.")
