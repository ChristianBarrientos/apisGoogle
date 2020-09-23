from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar'] # ['https://www.googleapis.com/auth/calendar.readonly']
SCOPESDRIVE = ['https://www.googleapis.com/auth/drive.metadata.readonly']

#credentialsGoogleDrive.json
def getServiceGoogleDrive():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokenDrive.pickle'):
        with open('tokenDrive.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentialsGoogleDrive.json', SCOPESDRIVE)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokenDrive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def getFile(serviceDrive):
    fileName = "Manual_Google_Meet.docx"

    fileId = serviceDrive.getFilesByName(fileName).next().getId()
    return  fileId

def getServiceCalendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

event = {
  'summary': 'Prueba Adjunto',
  #'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'Ejemplo de creacion de Evento.',
  'start': {
    'dateTime': '2020-09-23T02:30:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2020-09-23T03:40:00-07:00',
    'timeZone': 'America/Argentina/Catamarca',
  },
  #'recurrence': [
  #  'RRULE:FREQ=DAILY;COUNT=2'
  #],
  'attendees': [
    {'email': 'christianbarrientoss@hotmail.com'},
  ],
  'conferenceData': [
      {'createRequest': {'requestId': "7qxalsvy0e"} #EL requestId es un ID interno para identificar la reunion
      }
    #{"createRequest": {
    #        'conferenceSolutionKey': {"type": "hangoutsMeet"}
    #        }
    #},
  ],
  "attachments": [
   {
      "fileUrl": "https://drive.google.com/file/d/1U5XwA3-JrqT1Ks3M3pzrX58mltozxyU2/view?usp=sharing",
      "title": "Instructivo",
      "mimeType": "application/vnd.google-apps.presentation"
   },
   ],
  #"attachments": [
   #{
      #"fileId": "1l5vzEteAKHLxpZee9zk5bj_h5B-JUzrPa1ejKM-cJ6g",
      #"title": "Instructivo",
     # "mimeType": "application/vnd.google-apps.presentation"
   #}
   #],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}


serviceCalendar = getServiceCalendar()

event = serviceCalendar.events().insert(calendarId='primary', supportsAttachments=True,sendNotifications=True, body=event, conferenceDataVersion=1).execute()
print(event)


"""Google Drive
serviceDrive = getServiceGoogleDrive()
#fileDrive = getFile(serviceDrive)
#print(fileDrive)
results = serviceDrive.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
print(results)
items = results.get('files', [])
print('Files:')
for item in items:
    print(item)
    #print(u'{0} ({1})'.format(item['name'], item['id']))
print 'Event created: %s' % (event.get('htmlLink'))

#"""