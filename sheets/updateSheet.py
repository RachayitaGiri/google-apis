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

# [START sheets_quickstart]
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "14eIWaB05tRUKXtp4QPCGunCcNH0Kq1w7s4BkqipBZko"
SAMPLE_RANGE_NAME = "A1:D4"


def update_values(value_input_option, data):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        body = {"values" : data}
        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                range=SAMPLE_RANGE_NAME,
                valueInputOption=value_input_option,
                body=body,)
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result

    except HttpError as err:
        print(f"An error occurred: {err}")
        return err

if __name__ == "__main__":
    values = [
        ["Item", "Cost", "Stocked", "Ship Date"],
        ["Wheel", "$20.50", "4", "3/1/2016"],
        ["Door", "$15", "2", "3/15/2016"],
        ["Engine", "$100", "1", "3/20/2016"]
    ]
    # Pass: value_input_option and _values
    update_values(
      "USER_ENTERED",
      values,
    )
# [END sheets_quickstart]