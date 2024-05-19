# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/userinfo.profile"]

def FORMAT(start: str, end: str, description: str) -> dict:
    start_date, end_date = start[:10], end[:10]
    original_time_zone = start[-6:]

    x = original_time_zone.split(':')
    if int(x[0]) < 0:
        y = int(x[0]) - int(x[1])
    else:
        y = int(x[0]) + int(x[1])

    s, e = start[11:15].split(':'), end[11:15].split(':')
    start_decimal = int(s[0]) + int(s[1]) / 60
    end_decimal = int(e[0]) + int(e[1]) / 60

    start_num = start_decimal - y
    start_floor = (start_decimal - y) // 1
    start_time = (f"0{int(start_floor)}:"[-3:] +
                  f"0{int(round(60 * (start_num - start_floor), 0))}"[-2:])

    end_num = end_decimal - y
    end_floor = (end_decimal - y) // 1
    end_time = (f"0{int(end_floor)}:"[-3:] +
                f"0{int(round(60 * (end_num - end_floor), 0))}"[-2:])

    return {"start date": start_date, "start time": start_time,
            "end date": end_date, "end time": end_time,
            "Original time zone": original_time_zone,
            "description": description}


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            # people api call
            
        try:
            # Build the People API service
            people_service = build("people", "v1", credentials=creds)

            # Call the People API to get the user's profile information
            profile = people_service.people().get(resourceName="people/me", personFields="names").execute()
            
            # Extract the user's name from the profile response
            names = profile.get('names', [])
            if names:
                user_name = names[0].get('displayName')
                print(f"User's name: {user_name}")
            else:
                print("No name found in profile.")

        except HttpError as error:
                print(f"An error occurred: {error}")

                return FORMAT(start, end, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    print(main())
# [END calendar_quickstart]
