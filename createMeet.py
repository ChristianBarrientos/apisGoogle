from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar'] # ['https://www.googleapis.com/auth/calendar.readonly']


class EventPlanner:

    def __init__(self, guests: Dict[str, str], schedule: Dict[str, str]):
        guests = [{"email": email} for email in guests.values()]
        service = self._authorize()
        self.event_states = self._plan_event(guests, schedule, service)

    @staticmethod
    def _authorize():
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service

    @staticmethod
    def _plan_event(attendees: List[Dict[str, str]], event_time, service: build):
        event = {"summary": "test meeting",
                 "start": {"dateTime": event_time["start"]},
                 "end": {"dateTime": event_time["end"]},
                 "attendees": attendees,
                 "conferenceData": {"createRequest": {
                                                        "requestId": f"{uuid4().hex}",
                                                      "conferenceSolutionKey": {"type": "hangoutsMeet"}
                                                      }
                                    },
                 "reminders": {"useDefault": True}
                 }
        event = service.events().insert(calendarId="primary", sendNotifications=True, body=event, conferenceDataVersion=1).execute()

        return event


if __name__ == "__main__":
    plan = EventPlanner({"test_guest": "test.guest@gmail.com"}, {"start": "2020-07-31T16:00:00",
                                                                          "end": "2020-07-31T16:30:00"})
    print(plan.event_states)