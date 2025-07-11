import datetime
import os.path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token.json'

def get_calendar_service():
    """
    Handles the entire Google OAuth 2.0 flow and returns an authenticated
    Google Calendar API service object.

    This function will:
    1. Look for a valid `token.json` file.
    2. If the token is expired, it will use the refresh token to get a new one.
    3. If `token.json` does not exist, it will trigger the one-time browser
       login flow to create it.
    
    Returns:
        An authorized Google Calendar service object (Resource) or None on failure.
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        try: 
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Error loading credentials from {TOKEN_FILE}: {e}")
            os.remove(TOKEN_FILE)
            creds = None
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials expired. Refreshing token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                print("Could not refresh token. Please re-authenticate.")
                return None
        else:
            # This is the one-time setup flow.
            print("No valid token found. Starting authentication flow...")
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERROR: The credentials file was not found at '{CREDENTIALS_FILE}'")
                print("Please download it from the Google Cloud Console and place it there.")
                return None
            
            # This line will start the local server and open the user's browser.
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            flow.redirect_uri = 'http://localhost:8080/'
            creds = flow.run_local_server(port=8080, authorization_prompt_message="") 
 
        # Save the credentials for the next run
        print(f"Authentication successful. Saving credentials to {TOKEN_FILE}")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the service object that we can use to make API calls
        service = build('calendar', 'v3', credentials=creds)
        print("Google Calendar service created successfully.")
        return service
    except Exception as e:
        print(f"An error occurred while building the service: {e}")
        return None