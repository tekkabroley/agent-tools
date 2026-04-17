# Photo Metadata MCP Server

This is a Model Context Protocol (MCP) server that provides Claude with the ability to extract and save deep metadata from photograph files.

By leveraging the powerful `exiftool` engine, this server can read standard EXIF data, XMP, and proprietary MakerNotes from a wide variety of image formats, including professional RAW files (e.g., Sony `.arw`).

## Features

- **Deep Metadata Extraction**: Retrieves all available tags, including camera settings, lens info, timestamps, and manufacturer-specific data.
- **Wide Format Support**: Supports `.jpg`, `.png`, `.arw`, and any other format supported by `exiftool`.
- **Save to File**: Ability to export extracted metadata directly to a JSON file.
- **MCP Integrated**: Seamlessly integrates with Claude Desktop as a tool.

## Installation

### System Dependencies
This server requires the `exiftool` binary to be installed on your host system.
- **macOS**: `brew install exiftool`
- **Linux**: `sudo apt-get install libimage-exiftool-perl`
- **Windows**: Install via the official [ExifTool website](https://exiftool.org/).

### Python Setup
1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   ./.venv/bin/pip install -r requirements.txt
   ```

## Configuration for Claude Desktop

To use this server with Claude Desktop, add the following entry to your `claude_desktop_config.json` file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "photo-metadata-server": {
      "command": "/Users/alexbroley/github/agent-tools/.venv/bin/python3",
      "args": [
        "/Users/alexbroley/github/agent-tools/photo_metadata_server.py"
      ]
    }
  }
}
```
*(Note: Replace the paths above with the absolute paths to your specific installation)*

## Available Tools

### `get_photo_metadata`
**Description**: Extracts all available metadata from a photo file and returns it as a formatted JSON string.
- **Input**: `file_path` (The absolute path to the image).

### `save_photo_metadata`
**Description**: Extracts metadata from a photo file and saves the result to a JSON file on disk.
- **Input**:
    - `file_path`: Absolute path to the image.
    - `output_path`: Absolute path where the JSON file should be saved.
# agent-tools
