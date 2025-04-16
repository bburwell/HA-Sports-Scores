import requests
import json

# Define the API URL
API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20250415-20250622"

def fetch_and_filter_data(region):
    try:
        # Make the API request
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Filter the events based on the notes field for the specified region
        filtered_events = []
        for event in data.get('events', []):  # Loop through existing events
            if event.get('competitions'):  # Check if competitions exist
                for competition in event['competitions']:
                    # Match the region in the competition's notes
                    if competition.get('notes') and region in competition['notes'][0]['headline']:
                        filtered_events.append(event)  # Add the entire event
                        break  # Avoid duplicates, only add once

        # Return only filtered events wrapped in the original structure
        return {"events": filtered_events}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {"events": []}

def save_to_file(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

# Fetch and save data for East 1st Round
east_1st_round = fetch_and_filter_data("East 1st Round")
save_to_file("/config/www/nba_east_1st_round.json", east_1st_round)

# Fetch and save data for West 1st Round
west_1st_round = fetch_and_filter_data("West 1st Round")
save_to_file("/config/www/nba_west_1st_round.json", west_1st_round)


