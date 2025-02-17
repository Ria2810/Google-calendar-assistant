# google_calendar.py
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("Missing credentials.json file for Google Calendar API.")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def schedule_event(summary, start_time, end_time, description="", attendees=None):
    """
    Create a calendar event.
    
    Parameters:
        summary (str): Title of the meeting.
        start_time (str): Start time in ISO 8601 format (e.g. "2025-02-20T14:00:00").
        end_time (str): End time in ISO 8601 format.
        description (str): Description or agenda.
        attendees (list): List of attendee email addresses.
    
    Returns:
        htmlLink (str): URL to the created event.
    """
    if attendees is None:
        attendees = []
    
    service = get_calendar_service()
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',  # Replace with your local timezone
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in attendees],
    }
    
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')
