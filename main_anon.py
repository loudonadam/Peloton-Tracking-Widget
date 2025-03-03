import requests
import time
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Peloton API credentials
person1_username = ""
person1_password = ""

person2_username = ""
person2_password = ""

# Google Sheets API credentials
credentials_file = ""

# Function to get Peloton session ID
def get_peloton_session(username, password):
    login_url = 'https://api.onepeloton.com/auth/login'
    payload = {
        'username_or_email': username,
        'password': password
    }
    response = requests.post(login_url, json=payload)
    
    # Debugging response content
    print(f"Login response: {response.status_code} - {response.text}")
    
    response.raise_for_status()
    return response.cookies['peloton_session_id']

# Function to fetch all workout data
def get_all_workout_data(session_id):
    headers = {'Cookie': f'peloton_session_id={session_id}'}
    user_url = 'https://api.onepeloton.com/api/me'
    user_response = requests.get(user_url, headers=headers)
    user_response.raise_for_status()
    user_id = user_response.json()['id']
    
    print(f"Fetched user ID: {user_id}") 
    
    all_workouts = []
    page = 0
    limit = 100  

    while True:
        workouts_url = f'https://api.onepeloton.com/api/user/{user_id}/workouts?limit={limit}&page={page}'
        workouts_response = requests.get(workouts_url, headers=headers)
        workouts_response.raise_for_status()
        workouts_data = workouts_response.json()['data']
        
        if not workouts_data:
            break
        
        all_workouts.extend(workouts_data)
        page += 1

    print(f"Fetched total workouts: {len(all_workouts)}")
    
    return all_workouts

# Function to get existing workout IDs from Google Sheets
def get_existing_workout_ids(service, spreadsheet_id, sheet_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A2:A"  # Assuming workout IDs are in column A starting from row 2
    ).execute()
    values = result.get('values', [])
    return {row[0] for row in values}  # Return a set of existing workout IDs

# Get Peloton session ID for person1
try:
    person1_session_id = get_peloton_session(person1_username, person1_password)
except requests.exceptions.HTTPError as e:
    print(f"Failed to get session ID for person1: {e}")


time.sleep(1)

# Get Peloton session ID for person2
try:
    person2_session_id = get_peloton_session(person2_username, person2_password)
except requests.exceptions.HTTPError as e:
    print(f"Failed to get session ID for person2: {e}")

# Only proceed if both session IDs are successfully retrieved
if 'person1_session_id' in locals() and 'person2_session_id' in locals():
    # Get all workout data
    person1_workouts = get_all_workout_data(person1_session_id)
    person2_workouts = get_all_workout_data(person2_session_id)

    # Connect to Google Sheet
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(credentials_file, scopes=scope)

    service = build('sheets', 'v4', credentials=creds)

    # Your spreadsheet and sheet name (replace with yours)
    spreadsheet_id = ""  # Replace with ID from URL
    sheet_name = ""

    # Get existing workout IDs
    existing_workout_ids = get_existing_workout_ids(service, spreadsheet_id, sheet_name)
    #print(f"Existing workout IDs: {existing_workout_ids}")

    # Define the headers data
    data_headers = ["ID", "User ID", "Workout Type", "Name", "Metric Type", "Workout Begin Time", "Total Work"]

    # Define data row, only include workouts not already in the sheet
    person1_data_row = []
    for workout in person1_workouts:
        if workout["id"] not in existing_workout_ids:
            #print(f"Adding person1's workout data: {workout}")  # Debug statement
            person1_data_row.append([workout["id"], workout["user_id"], workout["workout_type"], workout["name"], workout["metrics_type"], workout["created_at"], workout["total_work"]])

    person2_data_row = []
    for workout in person2_workouts:
        if workout["id"] not in existing_workout_ids:
            #print(f"Adding person2's workout data: {workout}")  # Debug statement
            person2_data_row.append([workout["id"], workout["user_id"], workout["workout_type"], workout["name"], workout["metrics_type"], workout["created_at"], workout["total_work"]])

    # Append data to the sheet (replace sheet name if different)
    if person1_data_row or person2_data_row:
        body = {
            "values": person1_data_row + person2_data_row
        }
        service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                               range=f"{sheet_name}!A1",
                                               valueInputOption="USER_ENTERED",
                                               body=body).execute()
        print("New workout data populated to Google Sheet!")
    else:
        print("No new workout data to append.")
else:
    print("Failed to get session IDs, cannot proceed with fetching workout data.")