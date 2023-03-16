import datetime
from datetime import timedelta

import pytz
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

service_account_email = "INSERT_HERE"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLIENT_SECRETS_FILE = 'credentials.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    filename=CLIENT_SECRETS_FILE, scopes=SCOPES
)


def build_service():
    service = build("calendar", "v3", credentials=credentials)
    return service


def create_event():
    service = build_service()

    start_datetime = datetime.datetime.now(tz=pytz.utc)
    event = (
        service.events()
        .insert(
            calendarId="7e6adb1482638703506d6c9395673a577701f82bfd8c59113f55b487299cc437@group.calendar.google.com",
            body={
                "summary": "Foo",
                "description": "Bar",
                "start": {"dateTime": start_datetime.isoformat()},
                "end": {
                    "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                },
            },
        )
        .execute()
    )
    print(event)


create_event()
