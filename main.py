import datetime
import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from prayer_time_API_reader import find_prayer_times, get_date_range
from datetime import timedelta
# If modifying these scopes, delete the file token.json.
#SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():

  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  current_directory = os.getcwd()
  print("Current Directory:", current_directory)
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    start = input("Enter start date (DD-MM-YYYY):")
    end = input ("Enter End date:")
    city = input("Enter City:")
    country = input("Enter country (alpha-2 code):")
    date_list = get_date_range(start,end)
    p_names = ["Fajr","Dhuhr","Asr","Maghrib","Isha"]
    p_duration = [35,30,30,15,30] #duration of event/prayer

    t,a,b,c,d,e = find_prayer_times(city,country,date_list)
    p_timings = [a,b,c,d,e]
    #loops through the list of dates
    for i in range(len(date_list)):
      
      for j in range(5): #j is index of prayer (0 is "Fajr", etc )
        #find the start time of the event by replacing the hour and the minute.
        start = date_list[i].replace(hour = int(p_timings[j][i].split(":")[0]), minute = int(p_timings[j][i].split(":")[1]))
        #print(start)
        event = {
        'summary': f'{p_names[j]} Prayer in {country}',
        'start': {
            'dateTime': start.isoformat() ,
            'timeZone': t,
        },
        'end': {
            'dateTime': (start + timedelta(minutes=p_duration[j])).isoformat(),
            'timeZone': t,
        },
        } 
        #insert the event into the calendar. If no specific calendar for prayers. just use calendarId = "primary"
        event = service.events().insert(calendarId='primary', body=event).execute() 
        print('Event created: %s' % (event.get('htmlLink')))


  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()