import os
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import datetime
import pytz
from google.oauth2.credentials import Credentials

GOOGLE_CREDENTIALS_FILE = 'credentials.json'
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_credentials():
    creds = None
    if os.path.exists(GOOGLE_CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(GOOGLE_CREDENTIALS_FILE, SCOPES)
    return creds


class GoogleCalendar:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_events(self):
        events_result = self.service.events().list(calendarId='primary',
                                                   timeMin=datetime.datetime.utcnow().isoformat() + 'Z', maxResults=10,
                                                   singleEvents=True, orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_event(self, event):
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        return event['id']

    def update_event(self, event_id, event):
        event = self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return event['id']

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
