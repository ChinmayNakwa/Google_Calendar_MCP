# google_auth/services/google_meet.py

import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.apps import meet_v2 

SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token_meet.json'

def get_meet_service():
    """
    Handles the entire Google OAuth 2.0 flow and returns an authenticated
    Google Meet API service object.
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        try: 
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Error loading credentials from {TOKEN_FILE}: {e}")
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Meet credentials expired. Refreshing token...")
            try: 
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing Meet token: {e}")
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                print("Could not refresh token. Please re-authenticate.")
                return None
        else:
            print("No valid Meet token found. Starting authentication flow...")
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERROR: The credentials file was not found at '{CREDENTIALS_FILE}'")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            flow.redirect_uri = 'http://localhost:8080/'
            creds = flow.run_local_server(port=8080, authorization_prompt_message="")
        
        print(f"Authentication successful. Saving Meet credentials to {TOKEN_FILE}")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        print("Google Meet service created successfully.")

        service = meet_v2.SpacesServiceClient(credentials=creds)
        return service
    except Exception as e:
        print(f"An error occurred while building the service: {e}")
        return None