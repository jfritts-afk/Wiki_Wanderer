import requests
import yaml  # Ensure PyYAML is imported
import os
from datetime import datetime

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
def get_todays_featured_article(access_token):
    today = datetime.now()
    date = today.strftime('%Y/%m/%d')
    url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{date}'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('daily', {}).get('items', [{}])[0]
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Define directory path for Wikipedia data
wikipedia_dir = 'wikipedia_data'
os.makedirs(wikipedia_dir, exist_ok=True)

# Generate filename for Wikipedia data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
wikipedia_filename = f"todays_featured_article_{timestamp}.yaml"
wikipedia_file_path = os.path.join(wikipedia_dir, wikipedia_filename)

# Fetch and save today's featured article
def main():
    access_token = get_access_token()
    if access_token:
        article = get_todays_featured_article(access_token)
        if article:
            with open(wikipedia_file_path, 'w') as file:
                yaml.dump(article, file, default_flow_style=False)
            print(f"Today's featured article saved to {wikipedia_file_path}")
        else:
            print("No featured article found.")
    else:
        print("Failed to fetch access token.")

if __name__ == "__main__":
    main()
