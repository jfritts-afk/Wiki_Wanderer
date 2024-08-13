import requests
import yaml
import os
from datetime import datetime, timedelta
import shutil

# Define client credentials
CLIENT_ID = '14c7a3e6c4b0122215440fd0e3510fea'
CLIENT_SECRET = '50b5b939674114087bd574108d7ffca551c3bc64'

# Function to get an access token
def get_access_token():
    url = 'https://meta.wikimedia.org/w/rest.php/oauth2/access_token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to get access token: {response.status_code}")
        return None

# Function to fetch today's featured content from Wikipedia
def get_todays_featured_content(access_token):
    today = datetime.now()
    date = today.strftime('%Y/%m/%d')
    url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{date}'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Fetch Wikipedia data
def fetch_wikipedia_data():
    access_token = get_access_token()
    if access_token:
        featured_content = get_todays_featured_content(access_token)
        return {
            "featured_content": featured_content
        }
    else:
        return None

# Define directory paths
most_recent_dir = 'most_recent_fetch'
old_fetch_dir = 'old_fetch_data'
os.makedirs(most_recent_dir, exist_ok=True)
os.makedirs(old_fetch_dir, exist_ok=True)

# Generate filename for Wikipedia data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
wikipedia_filename = f"wikipedia_data_{timestamp}.yaml"
wikipedia_file_path = os.path.join(most_recent_dir, wikipedia_filename)

# Function to move old files
def move_old_files():
    now = datetime.now()
    print(f"Current time: {now}")
    print(f"Files in '{most_recent_dir}': {os.listdir(most_recent_dir)}")
    for file in os.listdir(most_recent_dir):
        file_path = os.path.join(most_recent_dir, file)
        if os.path.isfile(file_path) and file.endswith('.yaml'):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"Checking file: {file_path}, last modified: {file_time}")
            if (now - file_time).total_seconds() > 15:  # 15 seconds old
                try:
                    print(f"Moving file: {file_path} to {old_fetch_dir}")
                    shutil.move(file_path, old_fetch_dir)
                except Exception as e:
                    print(f"Error moving file {file_path}: {e}")
            else:
                print(f"File is not old enough to move: {file_path}")

# Fetch Wikipedia data
wikipedia_data = fetch_wikipedia_data()

# Save Wikipedia data to YAML file
if wikipedia_data:
    with open(wikipedia_file_path, 'w') as file:
        yaml.dump(wikipedia_data, file, default_flow_style=False)
    print(f"Wikipedia data saved to {wikipedia_file_path}")

    # Move old files to old files directory
    move_old_files()
else:
    print("Failed to fetch Wikipedia data.")
