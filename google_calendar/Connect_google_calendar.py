from __future__ import print_function

import os.path
import datetime
import pickle
from datetime import timedelta
import datefinder

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events.owned', 'https://www.googleapis.com/auth/calendar.readonly']

# flow = InstalledAppFlow.from_client_secrets_file("F:\Desktop\THHT_13\calendar_manager\google_calendar\client_secret.json", scopes=scopes)
# credentials = flow.run_console()

# pickle.dump(credentials, open("token.pkl", "wb"))
# credentials = pickle.load(open("token.pkl", "rb"))
# service = build("calendar", "v3", credentials=credentials)

def get_token(path_file):
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("done token")
    try: 
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('An error occurred: %s' %error)

    
def view_calendar():
    # Call the calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items',[])

    if not events:
        print('No upcoming events found.')
        return

  # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        print(start,end_time,event['summary'])


def create_event(start_time_str, end_time_str, summary,description=None, location=None):
    timezone = 'Asia/Ho_Chi_Minh'
    matches_start = list(datefinder.find_dates(start_time_str))
    matches_end = list(datefinder.find_dates(end_time_str))
    if len(matches_start):
        start_time = matches_start[0]
        end_time = matches_end[0]
    
    event = {
        'summary':summary,
        'location':location,
        'description': description,
        'start':{
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone':'Asia/Ho_Chi_Minh',
        },
        'end':{
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone':'Asia/Ho_Chi_Minh',
        },
        'reminders':{
            'useDefault':False,
            'overrides': [
                            {'method': 'email', 'minutes':24*60},
                            {'method': 'popup', 'minutes':10},
            ],
        },
    }
    return service.events().insert(calendarId='primary',body=event).execute()

if __name__ == '__main__':
    path_file = 'F:\Desktop\THHT_13\calendar_manager\google_calendar\client_secret.json'
    try:
        service = get_token(path_file)
        event = create_event("15 June 9 PM","15 June 10PM","Tich hop he thong")
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('An error occurred: %s' %error)
    