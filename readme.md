## Wiki_Wanderer

Wiki_Wanderer is a Python script that fetches today's featured content from Wikipedia and stores it in a YAML file. It also manages older files by moving them to a separate directory if they are older than 15 seconds.
## Overview

    - Fetch Wikipedia Data: Retrieves today's featured content from Wikipedia using an access token.
    - Save Data: Stores the fetched data in a YAML file within the most_recent_fetch directory.
    - Manage Files: Automatically moves older files from most_recent_fetch to the old_fetch_data directory.

## Directory Structure

    - most_recent_fetch/: Contains the most recent Wikipedia data fetch.
    - old_fetch_data/: Stores older data fetches.

## Usage

Simply run the script to fetch and store Wikipedia data, and manage old files.