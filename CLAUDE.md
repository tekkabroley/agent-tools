# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
- Install dependencies: `.venv/bin/pip install -r requirements.txt`
- System dependency: `exiftool` must be installed (e.g., `brew install exiftool` on macOS).

### Running & Testing
- Run the server (stdio): `.venv/bin/python3 photo_metadata_server.py`
- Test metadata extraction: `.venv/bin/python3 test_metadata.py`
- Test metadata saving: `.venv/bin/python3 test_save_metadata.py`

## Architecture

This repository contains a collection of MCP (Model Context Protocol) servers.

### Photo Metadata Server (`photo_metadata_server.py`)
- **Framework**: Built using `FastMCP`.
- **Engine**: Wraps the `exiftool` binary via `pyexiftool` to handle complex image formats (JPEG, PNG, ARW) and proprietary MakerNotes.
- **Transport**: Uses `stdio` for communication with Claude Desktop.
- **Key Tools**:
    - `get_photo_metadata`: Returns all available metadata as a JSON string.
    - `save_photo_metadata`: Exports metadata to a local JSON file.
    - `create_photo_markdown`: Generates a markdown file with YAML frontmatter.

### S3 Server (`s3_server.py`)
- **Framework**: Built using `FastMCP`.
- **Engine**: Uses `boto3` to interact with AWS S3.
- **Key Tools**: `list_s3_files`, `download_s3_file`.

### Telegram Notification Server (`telegram_mcp.py`)
- **Framework**: Built using `FastMCP`.
- **Engine**: Uses `python-telegram-bot`.
- **Key Tools**: `send_telegram_notification`, `send_terminal_output`, `request_approval`, `get_latest_messages`.
- **Requirement**: Needs `.env` file with `TELEGRAM_BOT_TOKEN` and `AUTHORIZED_USER_ID`.
