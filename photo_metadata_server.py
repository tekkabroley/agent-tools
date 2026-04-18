from mcp.server.fastmcp import FastMCP
import exiftool
import json
import os

# Initialize FastMCP server
mcp = FastMCP("photo-metadata-server")

def _extract_metadata(file_path: str) -> dict:
    """Helper function to extract metadata as a dictionary."""
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file_path)
        if not metadata:
            return {}
        tags = metadata[0]
        if "SourceFile" in tags:
            del tags["SourceFile"]
        return tags

@mcp.tool()
def get_photo_metadata(file_path: str) -> str:
    """
    Extracts all available metadata from a photograph file.
    Supports .jpg, .png, .arw and other formats supported by ExifTool.

    Args:
        file_path: The absolute path to the image file.
    """
    try:
        tags = _extract_metadata(file_path)
        if not tags:
            return "No metadata found for the specified file."
        return json.dumps(tags, indent=2)
    except Exception as e:
        return f"Error extracting metadata: {str(e)}"

@mcp.tool()
def save_photo_metadata(file_path: str, output_path: str) -> str:
    """
    Extracts metadata from a photograph file and saves it to a JSON file.
    If output_path is a directory, the file will be saved as <filename>.json
    (stripping the original image extension).

    Args:
        file_path: The absolute path to the image file.
        output_path: The absolute path where the JSON metadata should be saved (can be a file or directory).
    """
    try:
        tags = _extract_metadata(file_path)
        if not tags:
            return "No metadata found for the specified file. Nothing saved."

        # If output_path is a directory, generate a clean filename
        if os.path.isdir(output_path) or output_path.endswith(os.sep):
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(output_path, f"{base_name}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tags, f, indent=2)

        return f"Metadata successfully saved to {output_path}"
    except Exception as e:
        return f"Error saving metadata: {str(e)}"

@mcp.tool()
def create_photo_markdown(json_path: str, image_path: str) -> str:
    """
    Creates a small markdown file with a YAML frontmatter based on a photo's metadata JSON.

    Args:
        json_path: The absolute path to the metadata JSON file.
        image_path: The absolute path to the original image file.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            tags = json.load(f)

        # Find the best date field
        # Priority: Composite:DateTimeCreated -> EXIF:DateTimeOriginal -> IPTC:DateCreated
        date_val = tags.get("Composite:DateTimeCreated") or \
                   tags.get("EXIF:DateTimeOriginal") or \
                   tags.get("IPTC:DateCreated") or \
                   "Unknown"

        # Generate markdown filename: <File NAME WITHOUT SUFFIX>.md
        # e.g., /path/to/DSC01630.json -> /path/to/DSC01630.md
        base_path = os.path.splitext(json_path)[0]
        md_path = f"{base_path}.md"

        content = f"---\ndate: {date_val}\nimage: {image_path}\n---\n"

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return f"Markdown file successfully created at {md_path}"
    except Exception as e:
        return f"Error creating markdown file: {str(e)}"

if __name__ == "__main__":
    mcp.run()
