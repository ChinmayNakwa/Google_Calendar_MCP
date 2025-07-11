# Google Calendar MCP Tool Server

A standalone, runnable tool server that provides a complete set of functions for interacting with the Google Calendar API. This server is built using the Model-Context-Protocol (`mcp`) library and is designed to be called by an external AI agent or orchestrator.

This server acts as the "hardware" or "limbs" of an AI agent, handling all the secure authentication and direct API calls to Google, while exposing a simple, clean interface.

## Features

- **Standalone & Executable:** Runs as a separate process, listening for tool call requests on standard I/O (`stdio`).
- **Secure Authentication:** Manages the entire Google OAuth 2.0 flow, including initial user login and subsequent token refreshes.
- **Robust Toolset:** Provides a comprehensive set of tools for calendar management.
- **JSON Interface:** Accepts and returns data in clean, easy-to-parse JSON format.

## Provided Tools

This server exposes the following functions, which can be called by name:

- **`list_events(calendar_id, max_results, time_min)`**: Lists events from a calendar.
- **`create_event(summary, start_datetime, end_datetime, ...)`**: Creates a new event.
- **`get_event_by_id(event_id, calendar_id)`**: Retrieves a single event by its unique ID.
- **`update_event(event_id, updated_summary, ...)`**: Updates an existing event.
- **`delete_event(event_id, calendar_id)`**: Deletes an event.

## Setup and Installation

### Prerequisites

- Python 3.10+
- A Google Account
- A Google Cloud Platform project with the Google Calendar API enabled.

### 1. Setup Google Cloud Credentials

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Navigate to `APIs & Services > Credentials`.
3.  Click **+ CREATE CREDENTIALS** -> **OAuth client ID**.
4.  Select **Desktop app** for the Application type.
5.  Click **DOWNLOAD JSON** and rename the downloaded file to `credentials.json`.
6.  Place this file inside a `credentials/` directory in the project root.

### 2. Install Dependencies

1.  **Clone the repository and navigate into it.**

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure `requirements.txt` contains `mcp`, `google-api-python-client`, `google-auth-oauthlib`, etc.)*

## How to Run the Server

You can run the tool server directly from your terminal.

```bash
python run_calendar_mcp.py
```

The server will start and print  Starting MCP server 'GoogleCalendar' with transport 'stdio'.

The very first time you run a command that requires calendar access, the server will trigger the Google OAuth flow:
1.  Your web browser will open.
2.  You must log in and grant the requested permissions.
3.  A `token.json` file will be created in the `credentials/` folder.
This is a one-time process. Subsequent runs will use the saved token.


### How it Works

The `Dockerfile` defines the steps to create an image:
1.  It starts from a base Python image.
2.  It sets up a working directory and copies the `requirements.txt` file.
3.  It installs all Python dependencies.
4.  It copies your application source code (`main.py`, `mcp_server/`, etc.).
5.  **Crucially, it copies the `credentials/` folder (containing both `credentials.json` and your generated `token.json`) into the image.**
6.  It exposes port 8000 and defines the command to start the Uvicorn server.

### Building the Docker Image

From the project's root directory, run the following command to build the image. Replace `mcp-server` with your desired image name.

```bash
docker build -t mcp-server .
```

### Running the Docker Container

Once the image is built, you can run it as a container. This command maps port 8000 inside the container to port 8000 on your local machine.

```bash
docker run -p 8000:8000 --env-file .env mcp-server
```

- `-p 8000:8000`: Maps the container's port 8000 to your host's port 8000.
- `--env-file .env`: Securely passes the API keys from your local `.env` file into the container's environment.


## Edit this in claude_desktop_config.json
{
  "mcpServers": {
    "GoogleCalendar": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v", "${PWD}/credentials:/app/credentials",
        "claude-calendar-tool"
      ]
    }
  }
}