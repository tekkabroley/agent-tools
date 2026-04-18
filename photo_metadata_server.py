from mcp.server.fastmcp import FastMCP
import exiftool
import json

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

    Args:
        file_path: The absolute path to the image file.
        output_path: The absolute path where the JSON metadata should be saved.
    """
    try:
        tags = _extract_metadata(file_path)
        if not tags:
            return "No metadata found for the specified file. Nothing saved."

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tags, f, indent=2)

        return f"Metadata successfully saved to {output_path}"
    except Exception as e:
        return f"Error saving metadata: {str(e)}"

if __name__ == "__main__":
    mcp.run()
