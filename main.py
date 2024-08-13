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
wikipedia_dir = 'wikipedia_data'
old_files_dir = 'old_files'
os.makedirs(wikipedia_dir, exist_ok=True)
os.makedirs(old_files_dir, exist_ok=True)

# Generate filename for Wikipedia data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
wikipedia_filename = f"wikipedia_data_{timestamp}.yaml"
wikipedia_file_path = os.path.join(wikipedia_dir, wikipedia_filename)

# Function to check file age and move it if necessary
def handle_old_files(file_path, old_files_dir):
    file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_path))
    if file_age > timedelta(minutes=1):
        new_path = os.path.join(old_files_dir, os.path.basename(file_path))
        shutil.move(file_path, new_path)
        print(f"Moved old file to {new_path}")

# Fetch Wikipedia data
wikipedia_data = fetch_wikipedia_data()

# Save Wikipedia data to YAML file
if wikipedia_data:
    with open(wikipedia_file_path, 'w') as file:
        yaml.dump(wikipedia_data, file, default_flow_style=False)
    print(f"Wikipedia data saved to {wikipedia_file_path}")

    # Check if file needs to be moved to old files directory
    handle_old_files(wikipedia_file_path, old_files_dir)
else:
    print("Failed to fetch Wikipedia data.")
