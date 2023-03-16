from __future__ import print_function

import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from collections import namedtuple

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = '../credentials.json'
# Path of the "client_id.json" file
JSON_FILEPATH = os.path.join('../credentials.json')
REDIRECT_URL = 'http://127.0.0.1:8000/'


# API_SERVICE_NAME = api_name
# API_VERSION = api_version


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        GMT_OFF = '+05:00'  # PDT/MST/GMT-7
        EVENT = {
            'summary': 'Dinner with friends',
            'start': {'dateTime': '2023-03-3T19:00:00%s' % GMT_OFF},
            'end': {'dateTime': '2023-03-4T22:00:00%s' % GMT_OFF},
            'attendees': [
                {'email': 'friend1@example.com'},
                {'email': 'friend2@example.com'},
            ],
        }

        e = service.events().insert(calendarId='primary',
                                    sendNotifications=True, body=EVENT).execute()

        print('''*** %r event added:
            Start: %s
            End:   %s''' % (e['summary'].encode('utf-8'),
                            e['start']['dateTime'], e['end']['dateTime']))
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
