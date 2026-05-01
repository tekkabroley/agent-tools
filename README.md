# agent-tools

A collection of Model Context Protocol (MCP) servers for agentic workflows.

## Servers

### 1. Photo Metadata Server (`photo_metadata_server.py`)
Extracts and saves deep metadata from photograph files (JPEG, PNG, ARW) using `exiftool`.

- **Dependencies**: `brew install exiftool`
- **Config**: 
  ```json
  "photo-metadata": {
    "command": "/Users/alexbroley/github/agent-tools/.venv/bin/python3",
    "args": ["/Users/alexbroley/github/agent-tools/photo_metadata_server.py"]
  }
  ```

### 2. S3 Server (`s3_server.py`)
Interacts with AWS S3 buckets.

- **Config**:
  ```json
  "s3-server": {
    "command": "/Users/alexbroley/github/agent-tools/.venv/bin/python3",
    "args": ["/Users/alexbroley/github/agent-tools/s3_server.py"]
  }
  ```

### 3. Telegram Notification Server (`telegram_mcp.py`)
Sends notifications and requests approvals via Telegram.

- **Setup**: Create a `.env` file:
  ```env
  TELEGRAM_BOT_TOKEN=your_token
  AUTHORIZED_USER_ID=your_id
  ```
- **Config**:
  ```json
  "telegram-notifications": {
    "command": "/Users/alexbroley/github/agent-tools/.venv/bin/python3",
    "args": ["/Users/alexbroley/github/agent-tools/telegram_mcp.py"]
  }
  ```

## Installation

1. Clone the repo.
2. Setup virtual environment:
   ```bash
   python3 -m venv .venv
   ./.venv/bin/pip install -r requirements.txt
   ```
