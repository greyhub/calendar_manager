from __future__ import print_function

import os.path
import datetime
from datetime import timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle 

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events.owned']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

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

    # start_time = datetime.datetime(2021, 12, 26, 19, 30, 0)
    # end_time = start_time + timedelta(hours=5)
    # timezone = 'Asia/Ho_Chi_Minh'

    # event = {
    #     'summary': 'AOEclien hoan',
    #     'location': 'Ho Chi Minh',
    #     'description': 'MI vs TBD',
    #     'start': {
    #         'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #         'timeZone': timezone,
    #     },
    #     'end': {
    #         'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #         'timeZone': timezone,
    #     },
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #         {'method': 'email', 'minutes': 24 * 60},
    #         {'method': 'popup', 'minutes': 10},
    #         ],
    #     },
    # }

    # event = service.events().insert(calendarId='primary', body=event).execute()
    # print('Event created: %s' %(event.get('htmlLink')))

if __name__ == '__main__':
    main()