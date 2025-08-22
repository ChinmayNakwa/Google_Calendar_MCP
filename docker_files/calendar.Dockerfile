# Start from a slim Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Corrected COPY Commands ---
# Copy the specific tool server script we need from the mcp_server directory
COPY mcp_server/run_calendar_mcp.py .

# Copy the entire google_auth package, as the tool server depends on it.
# This makes the 'from google_auth.services...' import work inside the container.
COPY google_auth/ /app/google_auth/

# The command that runs when the container starts
CMD ["python", "run_calendar_mcp.py"]